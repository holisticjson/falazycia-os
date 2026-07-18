package com.hermes.messenger.db

import android.content.ContentValues
import android.content.Context
import net.sqlcipher.database.SQLiteDatabase
import net.sqlcipher.database.SQLiteOpenHelper
import java.io.File

class DatabaseHelper private constructor(context: Context, dbName: String, private val dbPassword: String) :
  SQLiteOpenHelper(context, dbName, null, DATABASE_VERSION) {

  companion object {
    private const val DATABASE_VERSION = 1
    
    @Volatile
    private var instance: DatabaseHelper? = null

    // Initialize SQLCipher native libraries. MUST be called on app startup.
    fun initLibraries(context: Context) {
      SQLiteDatabase.loadLibs(context)
    }

    // Opens or returns the singleton instance of the encrypted database
    fun getInstance(context: Context, dbPassword: String): DatabaseHelper {
      return instance ?: synchronized(this) {
        val activeInstance = instance ?: DatabaseHelper(
          context.applicationContext,
          "hermes_secure.db",
          dbPassword
        )
        instance = activeInstance
        activeInstance
      }
    }

    // Discards the current singleton instance (e.g. on decryption failure / wrong PIN)
    fun discardInstance() {
      synchronized(this) {
        instance = null
      }
    }
  }

  override fun onCreate(db: SQLiteDatabase) {
    // 1. Settings Table (stores user's own profile, public/private keys)
    db.execSQL("""
      CREATE TABLE settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
      )
    """)

    // 2. Contacts Table (stores registered contacts and their Curve25519 public keys)
    db.execSQL("""
      CREATE TABLE contacts (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        public_key TEXT NOT NULL
      )
    """)

    // 3. Messages Table (stores E2EE decrypted chat history locally)
    db.execSQL("""
      CREATE TABLE messages (
        id TEXT PRIMARY KEY,
        contact_id TEXT NOT NULL,
        sender_id TEXT NOT NULL,
        text TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        is_ai_assistant INTEGER DEFAULT 0,
        FOREIGN KEY(contact_id) REFERENCES contacts(id)
      )
    """)
  }

  override fun onUpgrade(db: SQLiteDatabase, oldVersion: Int, newVersion: Int) {
    db.execSQL("DROP TABLE IF EXISTS messages")
    db.execSQL("DROP TABLE IF EXISTS contacts")
    db.execSQL("DROP TABLE IF EXISTS settings")
    onCreate(db)
  }

  // --- CRUD Operations (Fully Synchronized to prevent SQLCipher/concurrency-related native crashes) ---

  @Synchronized
  fun saveSetting(key: String, value: String) {
    val db = getWritableDatabase(dbPassword)
    val values = ContentValues().apply {
      put("key", key)
      put("value", value)
    }
    db.insertWithOnConflict("settings", null, values, SQLiteDatabase.CONFLICT_REPLACE)
  }

  @Synchronized
  fun getSetting(key: String): String? {
    val db = getReadableDatabase(dbPassword)
    val cursor = db.rawQuery("SELECT value FROM settings WHERE key = ?", arrayOf(key))
    var value: String? = null
    if (cursor.moveToFirst()) {
      value = cursor.getString(0)
    }
    cursor.close()
    return value
  }

  @Synchronized
  fun saveContact(id: String, username: String, publicKey: String) {
    val db = getWritableDatabase(dbPassword)
    db.delete("contacts", "LOWER(username) = LOWER(?)", arrayOf(username))
    val values = ContentValues().apply {
      put("id", id)
      put("username", username)
      put("public_key", publicKey)
    }
    db.insertWithOnConflict("contacts", null, values, SQLiteDatabase.CONFLICT_REPLACE)
  }

  @Synchronized
  fun listContacts(): List<Map<String, String>> {
    val db = getReadableDatabase(dbPassword)
    val cursor = db.rawQuery("SELECT id, username, public_key FROM contacts ORDER BY username ASC", null)
    val contacts = mutableListOf<Map<String, String>>()
    while (cursor.moveToNext()) {
      contacts.add(
        mapOf(
          "id" to cursor.getString(0),
          "username" to cursor.getString(1),
          "public_key" to cursor.getString(2)
        )
      )
    }
    cursor.close()
    return contacts
  }

  @Synchronized
  fun saveMessage(id: String, contactId: String, senderId: String, text: String, isAiAssistant: Boolean = false) {
    val db = getWritableDatabase(dbPassword)
    val values = ContentValues().apply {
      put("id", id)
      put("contact_id", contactId)
      put("sender_id", senderId)
      put("text", text)
      put("is_ai_assistant", if (isAiAssistant) 1 else 0)
    }
    db.insert("messages", null, values)
  }

  @Synchronized
  fun getMessagesForContact(contactId: String): List<Map<String, Any>> {
    val db = getReadableDatabase(dbPassword)
    val cursor = db.rawQuery(
      "SELECT id, sender_id, text, timestamp, is_ai_assistant FROM messages WHERE contact_id = ? ORDER BY timestamp ASC",
      arrayOf(contactId)
    )
    val messages = mutableListOf<Map<String, Any>>()
    while (cursor.moveToNext()) {
      messages.add(
        mapOf(
          "id" to cursor.getString(0),
          "sender_id" to cursor.getString(1),
          "text" to cursor.getString(2),
          "timestamp" to cursor.getString(3),
          "is_ai_assistant" to (cursor.getInt(4) == 1)
        )
      )
    }
    cursor.close()
    return messages
  }

  @Synchronized
  fun deleteContact(id: String) {
    val db = getWritableDatabase(dbPassword)
    val cursor = db.rawQuery("SELECT username FROM contacts WHERE id = ?", arrayOf(id))
    var usernameToBlock: String? = null
    if (cursor.moveToFirst()) {
        usernameToBlock = cursor.getString(0)
    }
    cursor.close()

    db.delete("messages", "contact_id = ?", arrayOf(id))
    db.delete("contacts", "id = ?", arrayOf(id))
    if (usernameToBlock != null) {
        markContactAsDeleted(usernameToBlock)
    }
  }

  @Synchronized
  fun markContactAsDeleted(username: String) {
    val deleted = getDeletedContactIds().toMutableSet()
    deleted.add(username)
    saveSetting("deleted_contacts", deleted.joinToString(","))
  }

  @Synchronized
  fun restoreContact(id: String) {
    val deleted = getDeletedContactIds().toMutableSet()
    if (deleted.remove(id)) {
      saveSetting("deleted_contacts", deleted.joinToString(","))
    }
  }

  @Synchronized
  fun getDeletedContactIds(): Set<String> {
    val value = getSetting("deleted_contacts") ?: ""
    if (value.isEmpty()) return emptySet()
    return value.split(",").toSet()
  }

  @Synchronized
  fun saveContactsBulk(contactsList: List<Map<String, String>>) {
    val db = getWritableDatabase(dbPassword)
    val deletedUsernames = getDeletedContactIds()
    db.beginTransaction()
    try {
      val values = ContentValues()
      for (contact in contactsList) {
        val id = contact["id"] ?: continue
        val username = contact["username"] ?: continue
        if (deletedUsernames.contains(username)) continue
        val publicKey = contact["public_key"] ?: continue
        
        db.delete("contacts", "LOWER(username) = LOWER(?)", arrayOf(username))
        values.clear()
        values.put("id", id)
        values.put("username", username)
        values.put("public_key", publicKey)
        db.insertWithOnConflict("contacts", null, values, SQLiteDatabase.CONFLICT_REPLACE)
      }
      db.setTransactionSuccessful()
    } finally {
      db.endTransaction()
    }
  }
}
