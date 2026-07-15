import sqlite3 from 'sqlite3';
import path from 'path';

const dbPath = path.resolve(__dirname, '../hermes.db');
const db = new sqlite3.Database(dbPath);

// Custom wrappers for SQLite methods to ensure proper TypeScript typing
function dbRun(sql: string, params: any[] = []): Promise<void> {
  return new Promise((resolve, reject) => {
    db.run(sql, params, (err) => {
      if (err) reject(err);
      else resolve();
    });
  });
}

function dbGet(sql: string, params: any[] = []): Promise<any> {
  return new Promise((resolve, reject) => {
    db.get(sql, params, (err, row) => {
      if (err) reject(err);
      else resolve(row);
    });
  });
}

function dbAll(sql: string, params: any[] = []): Promise<any[]> {
  return new Promise((resolve, reject) => {
    db.all(sql, params, (err, rows) => {
      if (err) reject(err);
      else resolve(rows);
    });
  });
}

export interface User {
  id: string;
  username: string;
  public_key: string;
  created_at: string;
}

export interface PendingMessage {
  id: string;
  recipient_id: string;
  sender_id: string;
  encrypted_payload: string;
  created_at: string;
}

export async function initDb() {
  // Users table
  await dbRun(`
    CREATE TABLE IF NOT EXISTS users (
      id TEXT PRIMARY KEY,
      username TEXT UNIQUE NOT NULL,
      public_key TEXT NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);

  // Pending messages table (acts as a mailbox queue, cleared immediately upon delivery)
  await dbRun(`
    CREATE TABLE IF NOT EXISTS messages (
      id TEXT PRIMARY KEY,
      recipient_id TEXT NOT NULL,
      sender_id TEXT NOT NULL,
      encrypted_payload TEXT NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);

  // Leads table for form submission
  await dbRun(`
    CREATE TABLE IF NOT EXISTS leads (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      first_name TEXT NOT NULL,
      email TEXT NOT NULL,
      rodo_consent INTEGER NOT NULL,
      messenger TEXT,
      phone_model TEXT,
      additional_info TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);

  // Secure migration in case of existing table on production server
  try { await dbRun("ALTER TABLE leads ADD COLUMN messenger TEXT"); } catch (e) {}
  try { await dbRun("ALTER TABLE leads ADD COLUMN phone_model TEXT"); } catch (e) {}
  try { await dbRun("ALTER TABLE leads ADD COLUMN additional_info TEXT"); } catch (e) {}

  // Mail queue table for local transactional outbox
  await dbRun(`
    CREATE TABLE IF NOT EXISTS mail_queue (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      to_email TEXT NOT NULL,
      to_name TEXT NOT NULL,
      subject TEXT NOT NULL,
      body_html TEXT NOT NULL,
      status TEXT DEFAULT 'pending',
      attempts INTEGER DEFAULT 0,
      last_error TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);

  console.log('Database initialized successfully.');
}

export async function registerUser(id: string, username: string, publicKey: string): Promise<void> {
  await dbRun('DELETE FROM users WHERE LOWER(username) = LOWER(?)', [username]);
  await dbRun(
    'INSERT OR REPLACE INTO users (id, username, public_key) VALUES (?, ?, ?)',
    [id, username, publicKey]
  );
}

export async function getUser(id: string): Promise<User | undefined> {
  const row = await dbGet('SELECT * FROM users WHERE id = ?', [id]);
  return row as User | undefined;
}

export async function getUserByUsername(username: string): Promise<User | undefined> {
  const row = await dbGet('SELECT * FROM users WHERE username = ?', [username]);
  return row as User | undefined;
}

export async function listUsers(): Promise<User[]> {
  const rows = await dbAll('SELECT id, username, public_key, created_at FROM users');
  return rows as User[];
}

export async function queueMessage(id: string, recipientId: string, senderId: string, encryptedPayload: string): Promise<void> {
  await dbRun(
    'INSERT INTO messages (id, recipient_id, sender_id, encrypted_payload) VALUES (?, ?, ?, ?)',
    [id, recipientId, senderId, encryptedPayload]
  );
}

export async function popPendingMessages(recipientId: string): Promise<PendingMessage[]> {
  // Retrieve pending messages
  const rows = await dbAll(
    'SELECT * FROM messages WHERE recipient_id = ? ORDER BY created_at ASC',
    [recipientId]
  ) as PendingMessage[];

  if (rows.length > 0) {
    // Delete immediately so no trace is left on the server
    await dbRun('DELETE FROM messages WHERE recipient_id = ?', [recipientId]);
    console.log(`Delivered and deleted ${rows.length} messages for user ${recipientId}.`);
  }

  return rows;
}

export interface Lead {
  id: number;
  first_name: string;
  email: string;
  rodo_consent: number;
  messenger?: string;
  phone_model?: string;
  additional_info?: string;
  created_at: string;
}

export interface MailQueueItem {
  id: number;
  to_email: string;
  to_name: string;
  subject: string;
  body_html: string;
  status: string;
  attempts: number;
  last_error: string | null;
  created_at: string;
  updated_at: string;
}

export async function saveLead(
  firstName: string,
  email: string,
  rodoConsent: number,
  messenger?: string,
  phoneModel?: string,
  additionalInfo?: string
): Promise<void> {
  await dbRun(
    'INSERT INTO leads (first_name, email, rodo_consent, messenger, phone_model, additional_info) VALUES (?, ?, ?, ?, ?, ?)',
    [firstName, email, rodoConsent, messenger || null, phoneModel || null, additionalInfo || null]
  );
}

export async function enqueueEmail(toEmail: string, toName: string, subject: string, bodyHtml: string): Promise<void> {
  await dbRun(
    'INSERT INTO mail_queue (to_email, to_name, subject, body_html) VALUES (?, ?, ?, ?)',
    [toEmail, toName, subject, bodyHtml]
  );
}

export async function getPendingEmails(): Promise<MailQueueItem[]> {
  const rows = await dbAll(
    "SELECT * FROM mail_queue WHERE status = 'pending' OR (status = 'failed' AND attempts < 3) ORDER BY created_at ASC"
  );
  return rows as MailQueueItem[];
}

export async function markEmailSent(id: number): Promise<void> {
  await dbRun(
    "UPDATE mail_queue SET status = 'sent', attempts = attempts + 1, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
    [id]
  );
}

export async function markEmailFailed(id: number, error: string, attempts: number): Promise<void> {
  await dbRun(
    "UPDATE mail_queue SET status = 'failed', attempts = ?, last_error = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
    [attempts, error, id]
  );
}

