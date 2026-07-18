package com.hermes.messenger

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import android.util.Base64
import java.util.concurrent.TimeUnit
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.*
import androidx.compose.foundation.Image
import androidx.compose.ui.res.painterResource
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.rotate
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.vector.*
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.graphics.PathFillType
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.unit.IntOffset
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.animation.core.*
import androidx.core.content.ContextCompat
import androidx.lifecycle.lifecycleScope
import com.hermes.messenger.crypto.CryptoHelper
import kotlin.math.roundToInt
import com.hermes.messenger.db.DatabaseHelper
import com.hermes.messenger.network.WebSocketClient
import com.hermes.messenger.network.WebRTCManager
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.security.KeyPair
import java.security.PrivateKey
import java.security.PublicKey
import java.util.UUID
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.MediaType.Companion.toMediaType
import java.io.IOException

val SparklesIcon: ImageVector
    get() = ImageVector.Builder(
        name = "Sparkles",
        defaultWidth = 24.dp,
        defaultHeight = 24.dp,
        viewportWidth = 24f,
        viewportHeight = 24f
    ).apply {
        // Główna gwiazdka (środek)
        path(fill = SolidColor(Color.White)) {
            moveTo(12f, 3f)
            quadTo(12f, 12f, 21f, 12f)
            quadTo(12f, 12f, 12f, 21f)
            quadTo(12f, 12f, 3f, 12f)
            quadTo(12f, 12f, 12f, 3f)
            close()
        }
        // Mała gwiazdka (prawa góra)
        path(fill = SolidColor(Color.White)) {
            moveTo(19f, 3f)
            quadTo(19f, 6f, 22f, 6f)
            quadTo(19f, 6f, 19f, 9f)
            quadTo(19f, 6f, 16f, 6f)
            quadTo(19f, 6f, 19f, 3f)
            close()
        }
        // Średnia gwiazdka (lewy dół)
        path(fill = SolidColor(Color.White)) {
            moveTo(6f, 15f)
            quadTo(6f, 18f, 9f, 18f)
            quadTo(6f, 18f, 6f, 21f)
            quadTo(6f, 18f, 3f, 18f)
            quadTo(6f, 18f, 6f, 15f)
            close()
        }
    }.build()

class MainActivity : ComponentActivity() {

  // Local state references
  private var dbHelper: DatabaseHelper? = null
  private val wsClient = WebSocketClient()
  private val messageListeners = mutableListOf<() -> Unit>()
  private var currentlyViewedChatId: String? = null
  private var onIncomingCallListener: ((String, String, String) -> Unit)? = null
  private var isAppInForeground = false
  
  // WebRTC
  private var webRTCManager: WebRTCManager? = null
  private var activeCallPeerId: String? = null
  private var incomingOfferDescription: String? = null
  
  // Decrypted keys in memory (cleared on app close/lock)
  private var myPrivateKey: PrivateKey? = null
  private var myPublicKey: PublicKey? = null
  private var myUserId: String = ""
  private var myUsername: String = ""
  
  // Call permissions launcher
  private val requestPermissionLauncher = registerForActivityResult(
    ActivityResultContracts.RequestMultiplePermissions()
  ) { permissions ->
    val audioGranted = permissions[android.Manifest.permission.RECORD_AUDIO] ?: false
    if (!audioGranted) {
      Toast.makeText(this, "Microphone permission is required for calling", Toast.LENGTH_SHORT).show()
    }
  }

  private fun hasCallPermissions(): Boolean {
    val audio = androidx.core.content.ContextCompat.checkSelfPermission(this, android.Manifest.permission.RECORD_AUDIO) == android.content.pm.PackageManager.PERMISSION_GRANTED
    val bt = if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.S) {
      androidx.core.content.ContextCompat.checkSelfPermission(this, android.Manifest.permission.BLUETOOTH_CONNECT) == android.content.pm.PackageManager.PERMISSION_GRANTED
    } else true
    return audio && bt
  }

  private fun setSpeakerphoneEnabled(enabled: Boolean) {
    val audioManager = getSystemService(android.content.Context.AUDIO_SERVICE) as android.media.AudioManager
    audioManager.mode = android.media.AudioManager.MODE_IN_COMMUNICATION
    audioManager.isSpeakerphoneOn = enabled
  }

  private fun requestCallPermissions() {
    val perms = mutableListOf(android.Manifest.permission.RECORD_AUDIO)
    if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.S) {
      perms.add(android.Manifest.permission.BLUETOOTH_CONNECT)
    }
    requestPermissionLauncher.launch(perms.toTypedArray())
  }

  // Notification permission launcher (Android 13+)
  private val requestNotifPermissionLauncher = registerForActivityResult(
    ActivityResultContracts.RequestPermission()
  ) { _ -> /* User choice recorded by system */ }

  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState);
    
    // Initialize SQLCipher libraries
    DatabaseHelper.initLibraries(this)
    
    // Request POST_NOTIFICATIONS on Android 13+
    if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.TIRAMISU) {
      if (androidx.core.content.ContextCompat.checkSelfPermission(
          this, android.Manifest.permission.POST_NOTIFICATIONS
        ) != android.content.pm.PackageManager.PERMISSION_GRANTED
      ) {
        requestNotifPermissionLauncher.launch(android.Manifest.permission.POST_NOTIFICATIONS)
      }
    }

    // Create notification channel (required for Android 8+)
    if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
      val channel = android.app.NotificationChannel(
        "merkury_messages",
        "Wiadomości J(AI)Son",
        android.app.NotificationManager.IMPORTANCE_HIGH
      ).apply {
        description = "Powiadomienia o nowych wiadomościach i połączeniach"
        enableVibration(true)
        setShowBadge(true)
      }
      val notifManager = getSystemService(android.app.NotificationManager::class.java)
      notifManager.createNotificationChannel(channel)
    }
    
    // UI Setup
    setContent {
      HermesTheme {
        MainAppNavigation()
      }
    }
  }

  override fun onResume() {
    super.onResume()
    isAppInForeground = true
  }

  override fun onPause() {
    super.onPause()
    isAppInForeground = false
  }

  @OptIn(ExperimentalAnimationApi::class)
  @Composable
  fun MainAppNavigation() {
    val context = LocalContext.current
    var isUnlocked by remember { mutableStateOf(false) }
    var isProfileSetupNeeded by remember { mutableStateOf(false) }
    
    var currentScreen by remember { mutableStateOf<Screen>(Screen.Unlock) }
    var activeChatId by remember { mutableStateOf<String?>(null) }
    var activeChatUsername by remember { mutableStateOf<String>("") }
    
    // Call States
    var isInCall by remember { mutableStateOf(false) }
    var callPeerName by remember { mutableStateOf("") }
    var callStatus by remember { mutableStateOf("Calling...") }
    var isSpeakerOn by remember { mutableStateOf(false) }

    // Register listener for incoming WebRTC calls to update Compose UI state
    DisposableEffect(Unit) {
      onIncomingCallListener = { senderId, callerName, sdp ->
        activeCallPeerId = senderId
        callPeerName = callerName
        callStatus = "Incoming call..."
        isInCall = true
        currentScreen = Screen.Call
        incomingOfferDescription = sdp
      }
      onDispose {
        onIncomingCallListener = null
      }
    }

    LaunchedEffect(currentScreen) {
      if (currentScreen is Screen.Home && !hasCallPermissions()) {
        requestCallPermissions()
      }
    }

    // Connect to Websocket once unlocked
    fun initWebSocket() {
      val wsUrl = "wss://api.jaison.pl"
      
      wsClient.connect(wsUrl, object : WebSocketClient.Listener {
        override fun onConnected() {
          runOnUiThread {
            android.util.Log.d("MerkuryWS", "Connected to server")
            
            // Inicjalizacja WebRTC
            webRTCManager = WebRTCManager(
              context = applicationContext,
              onSignalingMessage = { payload ->
                val signalMsg = JSONObject().apply {
                  put("type", "signaling")
                  put("recipientId", activeCallPeerId)
                  put("senderId", myUserId)
                  put("payload", payload)
                }
                wsClient.send(signalMsg.toString())
              },
              onCallStateChanged = { newState ->
                runOnUiThread {
                  callStatus = newState
                  if (newState == "Disconnected") {
                    isInCall = false
                    currentScreen = Screen.Home
                    activeCallPeerId = null
                    incomingOfferDescription = null
                    isSpeakerOn = false
                    val audioManager = getSystemService(android.content.Context.AUDIO_SERVICE) as android.media.AudioManager
                    audioManager.mode = android.media.AudioManager.MODE_NORMAL
                    audioManager.isSpeakerphoneOn = false
                    // Cancel call notification (ID 1001)
                    try {
                      androidx.core.app.NotificationManagerCompat.from(this@MainActivity).cancel(1001)
                    } catch (e: Exception) {
                      e.printStackTrace()
                    }
                  }
                }
              }
            )

            // Register my public key on server
            val regMessage = JSONObject().apply {
              put("type", "register")
              put("payload", JSONObject().apply {
                put("id", myUserId)
                put("username", myUsername)
                put("publicKey", CryptoHelper.encodePublicKey(myPublicKey!!))
              })
            }
            wsClient.send(regMessage.toString())
          }
        }

        override fun onDisconnected() {
          runOnUiThread {
            android.util.Log.d("MerkuryWS", "Connection lost. Reconnecting...")
            lifecycleScope.launch(Dispatchers.IO) {
              kotlinx.coroutines.delay(3000)
              initWebSocket()
            }
          }
        }

        override fun onMessageReceived(text: String) {
          handleIncomingServerMessage(text, context)
        }

        override fun onError(t: Throwable) {
          runOnUiThread {
            val msg = t.localizedMessage ?: ""
            if (!msg.contains("Unable to resolve host") && !msg.contains("Software caused connection abort") && !msg.contains("failed to connect")) {
              android.util.Log.e("MerkuryWS", "Socket error: ${msg}. Reconnecting...")
            }
            lifecycleScope.launch(Dispatchers.IO) {
              kotlinx.coroutines.delay(3000)
              initWebSocket()
            }
          }
        }
      })
    }

    AnimatedContent(targetState = currentScreen, label = "ScreenTransition") { screen ->
      when (screen) {
        is Screen.Unlock -> {
          UnlockScreen(onUnlock = { pin ->
            // Use PIN to open SQLCipher database
            try {
              dbHelper = DatabaseHelper.getInstance(context, pin)
              
              // Check if profile exists
              val userId = dbHelper?.getSetting("my_id")
              val username = dbHelper?.getSetting("my_username")
              val privKeyB64 = dbHelper?.getSetting("my_private_key")
              val pubKeyB64 = dbHelper?.getSetting("my_public_key")
              
              if (userId != null && username != null && privKeyB64 != null && pubKeyB64 != null) {
                myUserId = userId
                myUsername = username
                
                // Derive public key & recreate keypair in memory
                myPublicKey = CryptoHelper.decodePublicKey(pubKeyB64)
                
                // For simplicity, we regenerate Keypair or load private key bytes
                // Normally private key is stored securely, we restore it here from base64 bytes
                val keyFactory = java.security.KeyFactory.getInstance("EC")
                val privKeyBytes = Base64.decode(privKeyB64, Base64.NO_WRAP)
                val privKeySpec = java.security.spec.PKCS8EncodedKeySpec(privKeyBytes)
                myPrivateKey = keyFactory.generatePrivate(privKeySpec)
                
                initWebSocket()
                currentScreen = Screen.Home
              } else {
                isProfileSetupNeeded = true
                currentScreen = Screen.SetupProfile(pin)
              }
            } catch (e: Exception) {
              DatabaseHelper.discardInstance()
              dbHelper = null
              Toast.makeText(context, "Incorrect PIN", Toast.LENGTH_LONG).show()
            }
          })
        }
        is Screen.SetupProfile -> {
          SetupProfileScreen(onProfileCreated = { username, keypair ->
            myUserId = UUID.randomUUID().toString()
            myUsername = username
            myPublicKey = keypair.public
            myPrivateKey = keypair.private
            
            // Save keys & profile to SQLCipher
            dbHelper?.saveSetting("my_id", myUserId)
            dbHelper?.saveSetting("my_username", myUsername)
            dbHelper?.saveSetting("my_public_key", CryptoHelper.encodePublicKey(keypair.public))
            dbHelper?.saveSetting("my_private_key", Base64.encodeToString(keypair.private.encoded, Base64.NO_WRAP))
            
            initWebSocket()
            currentScreen = Screen.Home
          })
        }
        is Screen.Home -> {
          HomeScreen(
            dbHelper = dbHelper!!,
            wsClient = wsClient,
            myUserId = myUserId,
            myPrivateKey = myPrivateKey!!,
            onChatSelected = { contactId, name ->
              activeChatId = contactId
              activeChatUsername = name
              currentlyViewedChatId = contactId
              currentScreen = Screen.Chat
            },
            onCallStarted = { id, name ->
              if (hasCallPermissions()) {
                activeCallPeerId = id
                callPeerName = name
                callStatus = "Calling..."
                isInCall = true
                currentScreen = Screen.Call
                webRTCManager?.startCall(id)
              } else {
                requestCallPermissions()
              }
            }
          )
        }
        is Screen.Chat -> {
          ChatScreen(
            dbHelper = dbHelper!!,
            wsClient = wsClient,
            contactId = activeChatId!!,
            contactName = activeChatUsername,
            myUserId = myUserId,
            myPrivateKey = myPrivateKey!!,
            onBack = { 
              currentScreen = Screen.Home
              currentlyViewedChatId = null
            },
            onCallStarted = {
              if (hasCallPermissions()) {
                activeCallPeerId = activeChatId
                callPeerName = activeChatUsername
                callStatus = "Calling..."
                isInCall = true
                currentScreen = Screen.Call
                webRTCManager?.startCall(activeChatId!!)
              } else {
                requestCallPermissions()
              }
            }
          )
        }
        is Screen.Call -> {
          CallScreen(
            peerName = callPeerName,
            status = callStatus,
            isSpeakerOn = isSpeakerOn,
            onToggleSpeaker = {
              isSpeakerOn = !isSpeakerOn
              setSpeakerphoneEnabled(isSpeakerOn)
            },
            onAnswer = if (incomingOfferDescription != null) {
              {
                try {
                  androidx.core.app.NotificationManagerCompat.from(this@MainActivity).cancel(1001)
                } catch (e: Exception) {
                  e.printStackTrace()
                }
                if (hasCallPermissions()) {
                  if (incomingOfferDescription != null && activeCallPeerId != null) {
                    callStatus = "Connecting..."
                    webRTCManager?.handleIncomingOffer(incomingOfferDescription!!, activeCallPeerId!!)
                  }
                } else {
                  Toast.makeText(this@MainActivity, "Brak uprawnień do mikrofonu", Toast.LENGTH_SHORT).show()
                  requestCallPermissions()
                }
              }
            } else null,
            onHangup = {
              try {
                androidx.core.app.NotificationManagerCompat.from(this@MainActivity).cancel(1001)
              } catch (e: Exception) {
                e.printStackTrace()
              }
              webRTCManager?.endCall()
              isInCall = false
              currentScreen = Screen.Home
              activeCallPeerId = null
              incomingOfferDescription = null
              isSpeakerOn = false
              val audioManager = getSystemService(android.content.Context.AUDIO_SERVICE) as android.media.AudioManager
              audioManager.mode = android.media.AudioManager.MODE_NORMAL
              audioManager.isSpeakerphoneOn = false
            }
          )
        }
      }
    }
  }

  // Show Android Heads-Up notification (floating banner on top of screen)
  private fun showHeadsUpNotification(title: String, body: String, context: android.content.Context, notifId: Int = System.currentTimeMillis().toInt()) {
    // Check permission on Android 13+
    if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.TIRAMISU) {
      val perm = android.Manifest.permission.POST_NOTIFICATIONS
      if (androidx.core.content.ContextCompat.checkSelfPermission(context, perm) != android.content.pm.PackageManager.PERMISSION_GRANTED) {
        return // Permission not granted — skip silently
      }
    }

    // Create a pending intent to open the app on tap
    val tapIntent = android.content.Intent(context, MainActivity::class.java).apply {
      action = android.content.Intent.ACTION_MAIN
      addCategory(android.content.Intent.CATEGORY_LAUNCHER)
      flags = android.content.Intent.FLAG_ACTIVITY_NEW_TASK or android.content.Intent.FLAG_ACTIVITY_SINGLE_TOP
    }
    val pendingFlags = android.app.PendingIntent.FLAG_UPDATE_CURRENT or android.app.PendingIntent.FLAG_IMMUTABLE
    val pendingIntent = android.app.PendingIntent.getActivity(context, 0, tapIntent, pendingFlags)

    val notification = androidx.core.app.NotificationCompat.Builder(context, "merkury_messages")
      .setSmallIcon(android.R.drawable.ic_dialog_email)
      .setContentTitle(title)
      .setContentText(body)
      .setPriority(androidx.core.app.NotificationCompat.PRIORITY_HIGH)
      .setCategory(androidx.core.app.NotificationCompat.CATEGORY_MESSAGE)
      .setAutoCancel(true)
      .setContentIntent(pendingIntent)
      .build()

    val notifManager = androidx.core.app.NotificationManagerCompat.from(context)
    notifManager.notify(notifId, notification)
  }

  // Handle incoming E2EE messages from WebSocket
  private fun handleIncomingServerMessage(jsonText: String, context: android.content.Context) {
    try {
      val obj = JSONObject(jsonText)
      val type = obj.optString("type")
      
      if (type == "chat_message") {
        val senderId = obj.getString("senderId")
        val recipientId = obj.getString("recipientId")
        val payload = obj.getJSONObject("payload")
        
        val encryptedData = payload.getString("data")
        val ephemeralPubKeyB64 = payload.getString("publicKey")
        
        // If this contact was deleted, restore them
        val deletedIds = dbHelper?.getDeletedContactIds() ?: emptySet()
        if (deletedIds.contains(senderId)) {
          dbHelper?.restoreContact(senderId)
          dbHelper?.saveContact(senderId, "User_" + senderId.take(5), ephemeralPubKeyB64)
          // Request refresh from server to restore correct username/key
          wsClient.send(JSONObject().apply { put("type", "get_users") }.toString())
        }
        
        // Fetch sender details
        val contact = dbHelper?.listContacts()?.find { it["id"] == senderId }
        val senderPubKeyB64 = contact?.get("public_key") ?: ephemeralPubKeyB64
        
        val senderPubKey = CryptoHelper.decodePublicKey(senderPubKeyB64)
        
        // Derive shared AES key using my Private Key and sender Public Key
        val aesKey = CryptoHelper.deriveSharedKey(myPrivateKey!!, senderPubKey)
        val decryptedText = CryptoHelper.decrypt(encryptedData, aesKey)
        
        // Save message locally in SQLCipher
        dbHelper?.saveMessage(
          UUID.randomUUID().toString(),
          senderId,
          senderId,
          decryptedText,
          false
        )
        // Show Heads-Up notification if the user is not currently in this chat or app is in background
        if (currentlyViewedChatId != senderId || !isAppInForeground) {
          val contactName = dbHelper?.listContacts()?.find { it["id"] == senderId }?.get("username") ?: senderId
          val previewText = if (decryptedText.startsWith("{\"type\":\"attachment\"")) "📎 Załącznik" else decryptedText
          showHeadsUpNotification("J(AI)Son: $contactName", previewText, context)
        }
        runOnUiThread {
          messageListeners.toList().forEach { it.invoke() }
        }
      } else if (type == "signaling") {
        val senderId = obj.getString("senderId")
        val payload = obj.getJSONObject("payload")
        val signalType = payload.optString("type")
        
        if (signalType == "offer") {
          val sdp = payload.getString("sdp")
          val callerName = dbHelper?.listContacts()?.find { it["id"] == senderId }?.get("username") ?: "Unknown User"
          // Heads-Up notification for incoming call
          showHeadsUpNotification("📞 Połączenie przychodzące", "Dzwoni: $callerName", context, 1001)
          runOnUiThread {
            onIncomingCallListener?.invoke(senderId, callerName, sdp)
          }
        } else if (signalType == "answer") {
          val sdp = payload.getString("sdp")
          webRTCManager?.handleIncomingAnswer(sdp)
        } else if (signalType == "candidate") {
          val sdp = payload.getString("sdp")
          val sdpMid = payload.getString("sdpMid")
          val sdpMLineIndex = payload.getInt("sdpMLineIndex")
          webRTCManager?.handleIncomingIceCandidate(sdpMid, sdpMLineIndex, sdp)
        }
      } else if (type == "users_list") {
        val usersArr = obj.getJSONArray("payload")
        val contactsList = mutableListOf<Map<String, String>>()
        for (i in 0 until usersArr.length()) {
          val userObj = usersArr.getJSONObject(i)
          val uid = userObj.getString("id")
          val uName = userObj.getString("username")
          val uKey = userObj.getString("public_key")
          
          if (uid != myUserId) {
            contactsList.add(mapOf("id" to uid, "username" to uName, "public_key" to uKey))
          }
        }
        dbHelper?.saveContactsBulk(contactsList)
        runOnUiThread {
          messageListeners.toList().forEach { it.invoke() }
        }
      }
    } catch (e: Exception) {
      e.printStackTrace()
    }
  }

  // --- Screens ---

  @Composable
  fun UnlockScreen(onUnlock: (String) -> Unit) {
    var pin by remember { mutableStateOf("") }
    val context = LocalContext.current
    val dbFile = context.getDatabasePath("hermes_secure.db")
    val dbExists = dbFile.exists()
    
    val titleText = if (dbExists) "Wprowadź klucz zabezpieczeń (PIN)" else "Ustal klucz zabezpieczeń (PIN)"
    val buttonText = if (dbExists) "Odblokuj" else "Ustanów PIN i przejdź dalej"
    val labelText = if (dbExists) "Wprowadź PIN" else "Utwórz nowy PIN"

    Column(
      modifier = Modifier
        .fillMaxSize()
        .padding(24.dp),
      horizontalAlignment = Alignment.CenterHorizontally,
      verticalArrangement = Arrangement.Center
    ) {
      Image(
        painter = painterResource(id = R.mipmap.ic_launcher),
        contentDescription = "J(AI)Son Logo",
        modifier = Modifier
          .size(220.dp)
      )
      Spacer(modifier = Modifier.height(24.dp))
      Icon(
        imageVector = Icons.Filled.Lock,
        contentDescription = "Lock Icon",
        tint = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.5f),
        modifier = Modifier.size(32.dp)
      )
      Spacer(modifier = Modifier.height(12.dp))
      Text(
        text = titleText,
        color = MaterialTheme.colorScheme.onBackground,
        fontSize = 16.sp,
        fontWeight = FontWeight.SemiBold
      )
      Spacer(modifier = Modifier.height(16.dp))
      OutlinedTextField(
        value = pin,
        onValueChange = { if (it.length <= 8) pin = it },
        label = { Text(labelText) },
        visualTransformation = PasswordVisualTransformation(),
        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.NumberPassword),
        modifier = Modifier.fillMaxWidth(0.8f)
      )
      Spacer(modifier = Modifier.height(24.dp))
      Button(
        onClick = { if (pin.isNotEmpty()) onUnlock(pin) },
        shape = RoundedCornerShape(12.dp)
      ) {
        Text(buttonText)
      }
    }
  }

  @Composable
  fun SetupProfileScreen(onProfileCreated: (String, KeyPair) -> Unit) {
    var username by remember { mutableStateOf("") }
    var isGenerating by remember { mutableStateOf(false) }

    Column(
      modifier = Modifier
        .fillMaxSize()
        .padding(24.dp),
      horizontalAlignment = Alignment.CenterHorizontally,
      verticalArrangement = Arrangement.Center
    ) {
      Text(
        text = "Skonfiguruj swój profil",
        color = MaterialTheme.colorScheme.onBackground,
        fontSize = 20.sp,
        fontWeight = FontWeight.Bold
      )
      Spacer(modifier = Modifier.height(16.dp))
      Text(
        text = "Twój profil będzie anonimowy. Klucze kryptograficzne wygenerują się na Twoim urządzeniu.",
        color = MaterialTheme.colorScheme.secondary,
        fontSize = 14.sp
      )
      Spacer(modifier = Modifier.height(24.dp))
      OutlinedTextField(
        value = username,
        onValueChange = { username = it },
        label = { Text("Nazwa użytkownika") },
        modifier = Modifier.fillMaxWidth()
      )
      Spacer(modifier = Modifier.height(24.dp))
      
      if (isGenerating) {
        CircularProgressIndicator()
      } else {
        Button(
          onClick = {
            if (username.isNotEmpty()) {
              isGenerating = true
              lifecycleScope.launch(Dispatchers.Default) {
                // Generate Curve25519 keypair
                val keypair = CryptoHelper.generateKeyPair()
                withContext(Dispatchers.Main) {
                  onProfileCreated(username, keypair)
                }
              }
            }
          },
          shape = RoundedCornerShape(12.dp)
        ) {
          Text("Generuj klucze i wejdź")
        }
      }
    }
  }

  @OptIn(ExperimentalMaterial3Api::class)
  @Composable
  fun HomeScreen(
    dbHelper: DatabaseHelper,
    wsClient: WebSocketClient,
    myUserId: String,
    myPrivateKey: PrivateKey,
    onChatSelected: (String, String) -> Unit,
    onCallStarted: (String, String) -> Unit
  ) {
    var tabIndex by remember { mutableStateOf(0) }
    var contacts by remember { mutableStateOf<List<Map<String, String>>>(emptyList()) }
    var showAddContact by remember { mutableStateOf(false) }
    var newContactUsername by remember { mutableStateOf("") }
    var newContactId by remember { mutableStateOf("") }
    var newContactKey by remember { mutableStateOf("") }
    
    // AI Assistant floating button & overlay states
    var isAIAssistantOpen by remember { mutableStateOf(false) }
    var buttonOffsetX by remember { mutableStateOf(0f) }
    var buttonOffsetY by remember { mutableStateOf(0f) }

    val scope = rememberCoroutineScope()
    
    fun refreshContacts() {
      scope.launch(Dispatchers.IO) {
        val list = dbHelper.listContacts()
        withContext(Dispatchers.Main) {
          contacts = list
        }
      }
    }

    // Refresh user list from server and load initial contacts
    LaunchedEffect(Unit) {
      refreshContacts()
      wsClient.send(JSONObject().apply { put("type", "get_users") }.toString())
    }

    // Register listener to update contacts in real-time when websocket updates
    DisposableEffect(Unit) {
      val listener = { refreshContacts() }
      messageListeners.add(listener)
      onDispose {
        messageListeners.remove(listener)
      }
    }

    Box(modifier = Modifier.fillMaxSize()) {
      Scaffold(
        floatingActionButton = {
          if (tabIndex == 0) {
            FloatingActionButton(onClick = { showAddContact = true }) {
              Icon(imageVector = Icons.Filled.Add, contentDescription = "Add Contact")
            }
          }
        }
      ) { padding ->
        Column(
          modifier = Modifier
            .fillMaxSize()
            .padding(padding)
        ) {
          TabRow(selectedTabIndex = tabIndex) {
            Tab(selected = tabIndex == 0, onClick = { tabIndex = 0 }) {
              Text("Kontakty", modifier = Modifier.padding(12.dp), fontSize = 13.sp)
            }
            Tab(selected = tabIndex == 1, onClick = { tabIndex = 1 }) {
              Text("Zrzut Myśli", modifier = Modifier.padding(12.dp), fontSize = 13.sp)
            }
            Tab(selected = tabIndex == 2, onClick = { tabIndex = 2 }) {
              Text("Ustawienia", modifier = Modifier.padding(12.dp), fontSize = 13.sp)
            }
          }

          when (tabIndex) {
            0 -> {
              LazyColumn(
                modifier = Modifier.fillMaxSize(),
                contentPadding = PaddingValues(16.dp)
              ) {
                items(contacts) { contact ->
                  Card(
                    modifier = Modifier
                      .fillMaxWidth()
                      .padding(vertical = 6.dp)
                      .clickable { onChatSelected(contact["id"]!!, contact["username"]!!) },
                    shape = RoundedCornerShape(12.dp)
                  ) {
                    Row(
                      modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                      verticalAlignment = Alignment.CenterVertically,
                      horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                      Row(verticalAlignment = Alignment.CenterVertically) {
                        Box(
                          modifier = Modifier
                            .size(40.dp)
                            .background(MaterialTheme.colorScheme.primaryContainer, CircleShape),
                          contentAlignment = Alignment.Center
                        ) {
                          Text(
                            text = contact["username"]!!.first().toString().uppercase(),
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onPrimaryContainer
                          )
                        }
                        Spacer(modifier = Modifier.width(16.dp))
                        Column {
                          Text(text = contact["username"]!!, fontWeight = FontWeight.Bold)
                          Text(text = "E2EE Aktywne", fontSize = 12.sp, color = MaterialTheme.colorScheme.secondary)
                        }
                      }
                      
                      Row(verticalAlignment = Alignment.CenterVertically) {
                        IconButton(onClick = { onCallStarted(contact["id"]!!, contact["username"]!!) }) {
                          Icon(imageVector = Icons.Filled.Phone, contentDescription = "Call", tint = MaterialTheme.colorScheme.primary)
                        }
                        IconButton(onClick = {
                          scope.launch(Dispatchers.IO) {
                            dbHelper.deleteContact(contact["id"]!!)
                            refreshContacts()
                          }
                        }) {
                          Icon(imageVector = Icons.Filled.Delete, contentDescription = "Delete Contact", tint = MaterialTheme.colorScheme.error)
                        }
                      }
                    }
                  }
                }
              }
            }
            1 -> {
              BrainDumpScreen(dbHelper)
            }
            2 -> {
              SettingsScreen(dbHelper, myUserId)
            }
          }
        }
      }

      // 1. Draggable Pulsing Cloud Floating Button
      val infiniteTransition = rememberInfiniteTransition(label = "CloudPulse")
      val pulseScale by infiniteTransition.animateFloat(
        initialValue = 0.94f,
        targetValue = 1.06f,
        animationSpec = infiniteRepeatable(
          animation = tween(1200, easing = FastOutSlowInEasing),
          repeatMode = RepeatMode.Reverse
        ),
        label = "pulseScale"
      )

      Box(
        modifier = Modifier
          .align(Alignment.BottomEnd)
          .offset { IntOffset(buttonOffsetX.roundToInt(), buttonOffsetY.roundToInt()) }
          .padding(bottom = 80.dp, end = 20.dp) // starting offset in bottom right
          .pointerInput(Unit) {
            detectDragGestures { change, dragAmount ->
              change.consume()
              buttonOffsetX += dragAmount.x
              buttonOffsetY += dragAmount.y
            }
          }
          .shadow(
            elevation = 12.dp,
            shape = CircleShape,
            ambientColor = Color(0xFF82B1FF),
            spotColor = Color(0xFF82B1FF)
          )
          .background(
            brush = Brush.linearGradient(
              colors = listOf(Color(0xFF82B1FF), Color(0xFFB388FF))
            ),
            shape = CircleShape
          )
          .clickable { isAIAssistantOpen = true }
          .size(60.dp * pulseScale),
        contentAlignment = Alignment.Center
      ) {
        Icon(
          imageVector = SparklesIcon,
          contentDescription = "AI Assistant",
          tint = Color.White,
          modifier = Modifier.size(30.dp)
        )
      }

      // 2. Full-screen Modal Overlay for AI Assistant
      if (isAIAssistantOpen) {
        Box(
          modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFA121212)) // semi-transparent very dark background
            .clickable(enabled = true, onClick = {}) // block clicks through
        ) {
          Column(
            modifier = Modifier.fillMaxSize()
          ) {
            // Header
            Row(
              modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
              verticalAlignment = Alignment.CenterVertically,
              horizontalArrangement = Arrangement.SpaceBetween
            ) {
              Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(
                  imageVector = SparklesIcon,
                  contentDescription = "AI Cloud",
                  tint = Color(0xFF82B1FF),
                  modifier = Modifier.size(26.dp)
                )
                Spacer(modifier = Modifier.width(12.dp))
                Column {
                  Text(
                    text = "Asystent AI J(AI)Son",
                    fontWeight = FontWeight.Bold,
                    fontSize = 18.sp,
                    color = Color.White
                  )
                  Text(
                    text = "Twój cyfrowy zarząd w kieszeni",
                    fontSize = 11.sp,
                    color = MaterialTheme.colorScheme.secondary
                  )
                }
              }
              IconButton(onClick = { isAIAssistantOpen = false }) {
                Icon(
                  imageVector = Icons.Filled.Close,
                  contentDescription = "Close",
                  tint = Color.White
                )
              }
            }

            Box(
              modifier = Modifier
                .fillMaxWidth()
                .height(1.dp)
                .background(MaterialTheme.colorScheme.outlineVariant)
            )

            Box(modifier = Modifier.weight(1f)) {
              AIAssistantScreen(dbHelper, myUserId, myPrivateKey)
            }
          }
        }
      }
    }

    if (showAddContact) {
      AlertDialog(
        onDismissRequest = { showAddContact = false },
        title = { Text("Dodaj kontakt ręcznie") },
        text = {
          Column {
            OutlinedTextField(
              value = newContactUsername,
              onValueChange = { newContactUsername = it },
              label = { Text("Nazwa użytkownika") }
            )
            Spacer(modifier = Modifier.height(8.dp))
            OutlinedTextField(
              value = newContactId,
              onValueChange = { newContactId = it },
              label = { Text("User ID") }
            )
            Spacer(modifier = Modifier.height(8.dp))
            OutlinedTextField(
              value = newContactKey,
              onValueChange = { newContactKey = it },
              label = { Text("Klucz Publiczny Curve25519 (Base64)") }
            )
          }
        },
        confirmButton = {
          Button(onClick = {
            if (newContactUsername.isNotEmpty() && newContactId.isNotEmpty() && newContactKey.isNotEmpty()) {
              scope.launch(Dispatchers.IO) {
                dbHelper.saveContact(newContactId, newContactUsername, newContactKey)
                refreshContacts()
              }
              showAddContact = false
            }
          }) {
            Text("Dodaj")
          }
        }
      )
    }
  }

  @OptIn(ExperimentalMaterial3Api::class)
  @Composable
  fun ChatScreen(
    dbHelper: DatabaseHelper,
    wsClient: WebSocketClient,
    contactId: String,
    contactName: String,
    myUserId: String,
    myPrivateKey: PrivateKey,
    onBack: () -> Unit,
    onCallStarted: () -> Unit
  ) {
    val context = LocalContext.current
    var messages by remember { mutableStateOf<List<Map<String, Any>>>(emptyList()) }
    var textMsg by remember { mutableStateOf("") }
    
    val scope = rememberCoroutineScope()
    
    fun refreshMessages() {
      scope.launch(Dispatchers.IO) {
        val list = dbHelper.getMessagesForContact(contactId)
        withContext(Dispatchers.Main) {
          messages = list
        }
      }
    }
    
    LaunchedEffect(contactId) {
      refreshMessages()
    }
    
    // Attachment file picker launcher
    val attachmentPickerLauncher = androidx.activity.compose.rememberLauncherForActivityResult(
      contract = androidx.activity.result.contract.ActivityResultContracts.GetContent()
    ) { uri ->
      if (uri != null) {
        lifecycleScope.launch(Dispatchers.IO) {
          uploadEncryptedAttachment(uri, context, contactId)
        }
      }
    }
    
    // Periodically refresh list of messages and register real-time push callback
    DisposableEffect(contactId) {
      val listener = { refreshMessages() }
      messageListeners.add(listener)
      onDispose {
        messageListeners.remove(listener)
      }
    }

    Scaffold(
      topBar = {
        TopAppBar(
          title = { Text(contactName) },
          navigationIcon = {
            IconButton(onClick = onBack) {
              Icon(imageVector = Icons.Filled.ArrowBack, contentDescription = "Back")
            }
          },
          actions = {
            IconButton(onClick = onCallStarted) {
              Icon(imageVector = Icons.Filled.Phone, contentDescription = "Call")
            }
          }
        )
      }
    ) { padding ->
      Column(
        modifier = Modifier
          .fillMaxSize()
          .padding(padding)
      ) {
        LazyColumn(
          modifier = Modifier
            .weight(1f)
            .fillMaxWidth()
            .padding(16.dp),
          reverseLayout = true
        ) {
          items(messages.reversed()) { msg ->
            val isMine = msg["sender_id"] == myUserId
            val msgText = msg["text"] as String
            val isAttachment = msgText.startsWith("{\"type\":\"attachment\"") || msgText.startsWith("{\"type\": \"attachment\"")
            // Pre-parse attachment metadata outside of Composable scope
            var attachFileName = ""
            var attachSizeStr = ""
            var attachParsed = false
            if (isAttachment) {
              try {
                val obj = org.json.JSONObject(msgText)
                attachFileName = obj.optString("name", "Plik")
                val fileSize = obj.optLong("size", 0L)
                attachSizeStr = if (fileSize > 1024*1024) "${fileSize/1024/1024} MB" else "${fileSize/1024} KB"
                attachParsed = true
              } catch (_: Exception) { }
            }

            Row(
              modifier = Modifier.fillMaxWidth(),
              horizontalArrangement = if (isMine) Arrangement.End else Arrangement.Start
            ) {
              if (isAttachment && attachParsed) {
                // Attachment bubble
                Card(
                  modifier = Modifier
                    .padding(vertical = 4.dp)
                    .widthIn(max = 240.dp),
                  shape = RoundedCornerShape(12.dp),
                  colors = CardDefaults.cardColors(
                    containerColor = if (isMine) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surfaceVariant
                  )
                ) {
                  Column(modifier = Modifier.padding(12.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                      Icon(
                        imageVector = AttachmentIcon,
                        contentDescription = "File",
                        tint = MaterialTheme.colorScheme.primary,
                        modifier = Modifier.size(20.dp)
                      )
                      Spacer(modifier = Modifier.width(6.dp))
                      Column {
                        Text(text = attachFileName, fontSize = 13.sp, fontWeight = FontWeight.Bold)
                        Text(text = attachSizeStr, fontSize = 11.sp, color = MaterialTheme.colorScheme.secondary)
                      }
                    }
                    if (!isMine) {
                      Spacer(modifier = Modifier.height(8.dp))
                      Button(
                        onClick = {
                          scope.launch {
                            downloadAndOpenAttachment(msgText, context)
                          }
                        },
                        modifier = Modifier.fillMaxWidth(),
                        shape = RoundedCornerShape(8.dp)
                      ) {
                        Text("Pobierz i otwórz", fontSize = 12.sp)
                      }
                    }
                  }
                }
              } else {
                // Normal text bubble (also fallback for malformed attachment JSON)
                Card(
                  modifier = Modifier.padding(vertical = 4.dp),
                  shape = RoundedCornerShape(12.dp),
                  colors = CardDefaults.cardColors(
                    containerColor = if (isMine) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surfaceVariant
                  )
                ) {
                  Text(
                    text = msgText,
                    modifier = Modifier.padding(12.dp),
                    color = if (isMine) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onSurfaceVariant
                  )
                }
              }
            }
          }
        }

        Row(
          modifier = Modifier
            .fillMaxWidth()
            .padding(12.dp),
          verticalAlignment = Alignment.CenterVertically
        ) {
          // Attachment picker button
          IconButton(onClick = { attachmentPickerLauncher.launch("*/*") }) {
            Icon(
              imageVector = AttachmentIcon,
              contentDescription = "Wyślij załącznik",
              tint = MaterialTheme.colorScheme.primary,
              modifier = Modifier.rotate(45f)
            )
          }
          OutlinedTextField(
            value = textMsg,
            onValueChange = { textMsg = it },
            placeholder = { Text("Zaszyfrowana wiadomość...") },
            modifier = Modifier.weight(1f),
            shape = RoundedCornerShape(24.dp)
          )
          Spacer(modifier = Modifier.width(8.dp))
          IconButton(
            onClick = {
              if (textMsg.isNotEmpty()) {
                val currentTextMsg = textMsg
                textMsg = ""
                scope.launch(Dispatchers.IO) {
                  // Get recipient public key
                  val contact = dbHelper.listContacts().find { it["id"] == contactId }
                  val pubKeyB64 = contact?.get("public_key") ?: ""
                  
                  if (pubKeyB64.isNotEmpty()) {
                    val recipientPubKey = CryptoHelper.decodePublicKey(pubKeyB64)
                    // Derive Shared Secret Key
                    val aesKey = CryptoHelper.deriveSharedKey(myPrivateKey, recipientPubKey)
                    // Encrypt message
                    val encryptedData = CryptoHelper.encrypt(currentTextMsg, aesKey)
                    
                    // Package WebSocket Message
                    val wsMessage = JSONObject().apply {
                      put("type", "chat_message")
                      put("senderId", myUserId)
                      put("recipientId", contactId)
                      put("payload", JSONObject().apply {
                        put("data", encryptedData)
                        put("publicKey", CryptoHelper.encodePublicKey(myPublicKey!!))
                      })
                    }
                    
                    wsClient.send(wsMessage.toString())
                    
                    // Save message locally
                    dbHelper.saveMessage(UUID.randomUUID().toString(), contactId, myUserId, currentTextMsg, false)
                    refreshMessages()
                  }
                }
              }
            }
          ) {
            Icon(imageVector = Icons.Filled.Send, contentDescription = "Send")
          }
        }
      }
    }
  }

  @Composable
  fun AIAssistantScreen(dbHelper: DatabaseHelper, myUserId: String, myPrivateKey: PrivateKey) {
    var messages by remember { mutableStateOf<List<Map<String, Any>>>(emptyList()) }
    var promptText by remember { mutableStateOf("") }
    var isWaitingForResponse by remember { mutableStateOf(false) }

    val scope = rememberCoroutineScope()

    fun refreshMessages() {
      scope.launch(Dispatchers.IO) {
        val list = dbHelper.getMessagesForContact("ai_assistant_id")
        withContext(Dispatchers.Main) {
          messages = list
        }
      }
    }

    LaunchedEffect(Unit) {
      refreshMessages()
    }

    Column(
      modifier = Modifier
        .fillMaxSize()
        .padding(16.dp)
    ) {
      LazyColumn(
        modifier = Modifier.weight(1f),
        reverseLayout = true
      ) {
        items(messages.reversed()) { msg ->
          val isMine = msg["sender_id"] == myUserId
          Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = if (isMine) Arrangement.End else Arrangement.Start
          ) {
            Card(
              modifier = Modifier.padding(vertical = 4.dp),
              shape = RoundedCornerShape(12.dp),
              colors = CardDefaults.cardColors(
                containerColor = if (isMine) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surfaceVariant
              )
            ) {
              Column(modifier = Modifier.padding(12.dp)) {
                Text(
                  text = if (isMine) "Ty" else "Asystent AI",
                  fontWeight = FontWeight.Bold,
                  fontSize = 11.sp,
                  color = MaterialTheme.colorScheme.secondary
                )
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                  text = msg["text"] as String,
                  color = if (isMine) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onSurfaceVariant
                )
              }
            }
          }
        }
      }

      if (isWaitingForResponse) {
        Row(modifier = Modifier.fillMaxWidth().padding(8.dp), horizontalArrangement = Arrangement.Start) {
          Text("Pisze...", fontSize = 12.sp, color = MaterialTheme.colorScheme.secondary)
        }
      }

      Row(
        modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp),
        verticalAlignment = Alignment.CenterVertically
      ) {
        OutlinedTextField(
          value = promptText,
          onValueChange = { promptText = it },
          placeholder = { Text("Zapytaj asystenta AI...") },
          modifier = Modifier.weight(1f),
          shape = RoundedCornerShape(24.dp)
        )
        Spacer(modifier = Modifier.width(8.dp))
        IconButton(
          onClick = {
            if (promptText.isNotEmpty()) {
              val prompt = promptText
              promptText = ""
              isWaitingForResponse = true
              
              scope.launch(Dispatchers.IO) {
                // Save user prompt
                dbHelper.saveMessage(UUID.randomUUID().toString(), "ai_assistant_id", myUserId, prompt, true)
                refreshMessages()

                try {
                  val client = OkHttpClient.Builder()
                    .connectTimeout(15, TimeUnit.SECONDS)
                    .readTimeout(60, TimeUnit.SECONDS)
                    .build()

                  val customGeminiKey = dbHelper.getSetting("custom_gemini_key") ?: ""
                  val customNvidiaKey = dbHelper.getSetting("custom_nvidia_key") ?: ""

                  val request = when {
                    customGeminiKey.isNotEmpty() -> {
                      val url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=$customGeminiKey"
                      val payload = geminiPayload(dbHelper, myUserId)
                      Request.Builder()
                        .url(url)
                        .post(payload.toString().toRequestBody("application/json".toMediaType()))
                        .build()
                    }
                    customNvidiaKey.isNotEmpty() -> {
                      val url = "https://integrate.api.nvidia.com/v1/chat/completions"
                      val jsonPayload = JSONObject().apply {
                        put("model", "meta/llama-3.1-70b-instruct")
                        put("messages", jsonArrayOfPrompts(dbHelper, myUserId))
                      }
                      Request.Builder()
                        .url(url)
                        .header("Authorization", "Bearer $customNvidiaKey")
                        .post(jsonPayload.toString().toRequestBody("application/json".toMediaType()))
                        .build()
                    }
                    else -> {
                      // Fallback to our GCP server proxy over HTTPS
                      val jsonPayload = JSONObject().apply {
                        put("messages", jsonArrayOfPrompts(dbHelper, myUserId))
                      }
                      Request.Builder()
                        .url("https://api.jaison.pl/api/chat")
                        .post(jsonPayload.toString().toRequestBody("application/json".toMediaType()))
                        .build()
                    }
                  }

                  client.newCall(request).execute().use { response ->
                    if (!response.isSuccessful) throw IOException("Unexpected code $response")

                    val responseBody = response.body?.string() ?: ""
                    
                    val assistantResponseText = if (customGeminiKey.isNotEmpty()) {
                      parseGeminiResponse(responseBody)
                    } else {
                      parseSSEResponse(responseBody)
                    }
                    
                    dbHelper.saveMessage(UUID.randomUUID().toString(), "ai_assistant_id", "ai_assistant_id", assistantResponseText, true)
                    withContext(Dispatchers.Main) {
                      isWaitingForResponse = false
                    }
                    refreshMessages()
                  }
                } catch (e: Exception) {
                  dbHelper.saveMessage(UUID.randomUUID().toString(), "ai_assistant_id", "ai_assistant_id", "Błąd połączenia z asystentem AI: ${e.localizedMessage}", true)
                  withContext(Dispatchers.Main) {
                    isWaitingForResponse = false
                  }
                  refreshMessages()
                }
              }
            }
          }
        ) {
          Icon(imageVector = Icons.Filled.Send, contentDescription = "Send")
        }
      }
    }
  }

  @OptIn(ExperimentalMaterial3Api::class)
  @Composable
  fun BrainDumpScreen(dbHelper: DatabaseHelper) {
    val context = LocalContext.current
    var content by remember { mutableStateOf("") }
    var tagsInput by remember { mutableStateOf("") }
    var isSending by remember { mutableStateOf(false) }
    val scope = rememberCoroutineScope()

    Column(
      modifier = Modifier
        .fillMaxSize()
        .padding(20.dp)
        .verticalScroll(rememberScrollState()),
      horizontalAlignment = Alignment.CenterHorizontally,
      verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
      Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
      ) {
        Column(modifier = Modifier.padding(20.dp)) {
          Row(verticalAlignment = Alignment.CenterVertically) {
            Box(
              modifier = Modifier
                .size(42.dp)
                .background(
                  brush = Brush.linearGradient(colors = listOf(Color(0xFF82B1FF), Color(0xFFB388FF))),
                  shape = CircleShape
                ),
              contentAlignment = Alignment.Center
            ) {
              Icon(
                imageVector = Icons.Filled.Create,
                contentDescription = "Brain",
                tint = Color.White,
                modifier = Modifier.size(22.dp)
              )
            }
            Spacer(modifier = Modifier.width(16.dp))
            Column {
              Text(
                text = "Zrzut Myśli",
                fontWeight = FontWeight.ExtraBold,
                fontSize = 18.sp,
                color = MaterialTheme.colorScheme.primary
              )
              Text(
                text = "Przelej myśli bezpośrednio do Zrzutu Myśli",
                fontSize = 12.sp,
                color = MaterialTheme.colorScheme.secondary
              )
            }
          }
        }
      }

      Text(
        text = "Czujesz chaos lub nadmiar bodźców? Uwolnij głowę. Wpisz tutaj swoje inspiracje, notatki, linki lub zadania. Trafią natychmiast do Twojego Inboxu.",
        fontSize = 13.sp,
        lineHeight = 18.sp,
        color = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.8f),
        modifier = Modifier.fillMaxWidth().padding(horizontal = 4.dp)
      )

      OutlinedTextField(
        value = content,
        onValueChange = { content = it },
        placeholder = { 
          Text(
            "Uwolnij głowę – zapisz co tylko chcesz...",
            color = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.4f)
          ) 
        },
        label = { Text("Twoja myśl / notatka / link") },
        modifier = Modifier
          .fillMaxWidth()
          .height(180.dp),
        maxLines = 10,
        shape = RoundedCornerShape(12.dp)
      )

      OutlinedTextField(
        value = tagsInput,
        onValueChange = { tagsInput = it },
        placeholder = { 
          Text(
            "np. praca, pomysl, nawyki", 
            color = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.4f)
          ) 
        },
        label = { Text("Tagi (oddzielone przecinkami, opcjonalnie)") },
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(12.dp)
      )

      Spacer(modifier = Modifier.height(8.dp))

      if (isSending) {
        CircularProgressIndicator(color = MaterialTheme.colorScheme.primary)
      } else {
        Button(
          onClick = {
            if (content.trim().isEmpty()) {
              Toast.makeText(context, "Treść nie może być pusta!", Toast.LENGTH_SHORT).show()
              return@Button
            }
            isSending = true
            scope.launch(Dispatchers.IO) {
              try {
                val tagsList = tagsInput.split(",")
                  .map { it.trim() }
                  .filter { it.isNotEmpty() }

                val payload = org.json.JSONObject().apply {
                  put("content", content)
                  val tagsJsonArr = org.json.JSONArray()
                  tagsList.forEach { tagsJsonArr.put(it) }
                  put("tags", tagsJsonArr)
                }

                val client = okhttp3.OkHttpClient.Builder()
                  .connectTimeout(15, java.util.concurrent.TimeUnit.SECONDS)
                  .readTimeout(15, java.util.concurrent.TimeUnit.SECONDS)
                  .build()

                val request = okhttp3.Request.Builder()
                  .url("https://api.jaison.pl/api/dump")
                  .post(payload.toString().toRequestBody("application/json".toMediaType()))
                  .build()

                client.newCall(request).execute().use { response ->
                  withContext(Dispatchers.Main) {
                    isSending = false
                    if (response.isSuccessful) {
                      Toast.makeText(context, "🧠 Zsynchronizowano z Bazą Wiedzy!", Toast.LENGTH_LONG).show()
                      content = ""
                      tagsInput = ""
                    } else {
                      Toast.makeText(context, "Błąd synchronizacji: Kod ${response.code}", Toast.LENGTH_LONG).show()
                    }
                  }
                }
              } catch (e: Exception) {
                withContext(Dispatchers.Main) {
                  isSending = false
                  Toast.makeText(context, "Błąd połączenia: ${e.localizedMessage}", Toast.LENGTH_LONG).show()
                }
              }
            }
          },
          modifier = Modifier
            .fillMaxWidth()
            .height(50.dp),
          shape = RoundedCornerShape(12.dp),
          colors = ButtonDefaults.buttonColors(
            containerColor = MaterialTheme.colorScheme.primary
          )
        ) {
          Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(8.dp)
          ) {
            Icon(imageVector = Icons.Filled.Send, contentDescription = "Sync", modifier = Modifier.size(18.dp))
            Text("Zsynchronizuj z Bazą Wiedzy 🚀", fontWeight = FontWeight.Bold)
          }
        }
      }
    }
  }

  // Parse SSE response payload for local mock streaming
  private fun parseSSEResponse(body: String): String {
    // Basic SSE parsing logic for OpenAI compatible response formatting
    var text = ""
    try {
      val lines = body.split("\n")
      for (line in lines) {
        if (line.startsWith("data: ")) {
          val dataStr = line.substring(6).trim()
          if (dataStr == "[DONE]") continue
          val obj = JSONObject(dataStr)
          val choices = obj.optJSONArray("choices")
          if (choices != null && choices.length() > 0) {
            val delta = choices.getJSONObject(0).optJSONObject("delta")
            val content = delta?.optString("content")
            if (content != null) {
              text += content
            }
          }
        }
      }
    } catch (e: Exception) {
      e.printStackTrace()
    }
    
    if (text.isEmpty()) {
      // Try fallback parsing standard JSON
      try {
        val obj = JSONObject(body)
        text = obj.getJSONArray("choices").getJSONObject(0).getJSONObject("message").getString("content")
      } catch (e: Exception) {
        text = body // Raw text fallback
      }
    }
    return text
  }

  private fun jsonArrayOfPrompts(dbHelper: DatabaseHelper, myUserId: String): org.json.JSONArray {
    val array = org.json.JSONArray()
    val history = dbHelper.getMessagesForContact("ai_assistant_id")
    
    // Add system instruction for ADHD-friendly outputs
    array.put(JSONObject().apply {
      put("role", "system")
      put("content", "Jesteś wspierającym asystentem AI. Twoje odpowiedzi muszą być ADHD-friendly: strukturyzowane, zwięzłe, używaj pogrubień i wypunktowań. Unikaj długich bloków tekstu.")
    })
    
    // Feed last 10 messages for conversation context
    val recent = history.takeLast(10)
    for (msg in recent) {
      val role = if (msg["sender_id"] == myUserId) "user" else "assistant"
      array.put(JSONObject().apply {
        put("role", role)
        put("content", msg["text"] as String)
      })
    }
    return array
  }

  private fun geminiPayload(dbHelper: DatabaseHelper, myUserId: String): JSONObject {
    val history = dbHelper.getMessagesForContact("ai_assistant_id")
    val contents = org.json.JSONArray()
    val recent = history.takeLast(10)
    for (msg in recent) {
      val role = if (msg["sender_id"] == myUserId) "user" else "model"
      contents.put(JSONObject().apply {
        put("role", role)
        put("parts", org.json.JSONArray().put(JSONObject().apply {
          put("text", msg["text"] as String)
        }))
      })
    }
    return JSONObject().apply {
      put("contents", contents)
      put("systemInstruction", JSONObject().apply {
        put("parts", org.json.JSONArray().put(JSONObject().apply {
          put("text", "Jesteś wspierającym asystentem AI o nazwie J(AI)Son. Twoje odpowiedzi muszą być ADHD-friendly: strukturyzowane, zwięzłe, używaj pogrubień i wypunktowań. Odpowiadaj po polsku. Unikaj długich bloków tekstu.")
        }))
      })
    }
  }

  private fun parseGeminiResponse(body: String): String {
    return try {
      val obj = JSONObject(body)
      val candidate = obj.getJSONArray("candidates").getJSONObject(0)
      val content = candidate.getJSONObject("content")
      val part = content.getJSONArray("parts").getJSONObject(0)
      part.getString("text")
    } catch (e: Exception) {
      "Błąd parsowania Gemini: $body"
    }
  }

  // --- Attachment encryption, upload and download helpers ---

  private fun uploadEncryptedAttachment(uri: android.net.Uri, context: android.content.Context, contactId: String) {
    try {
      // Read original file bytes
      val inputStream = context.contentResolver.openInputStream(uri) ?: return
      val originalBytes = inputStream.readBytes()
      inputStream.close()

      // Generate random AES-256 Key
      val aesKey = javax.crypto.KeyGenerator.getInstance("AES").apply {
        init(256)
      }.generateKey()

      // Encrypt bytes with AES-GCM
      val cipher = javax.crypto.Cipher.getInstance("AES/GCM/NoPadding")
      cipher.init(javax.crypto.Cipher.ENCRYPT_MODE, aesKey)
      val iv = cipher.iv
      val encryptedBytes = cipher.doFinal(originalBytes)
      
      // Combine IV (12 bytes) and encrypted content: [IV] + [Encrypted Data]
      val payloadBytes = ByteArray(iv.size + encryptedBytes.size)
      System.arraycopy(iv, 0, payloadBytes, 0, iv.size)
      System.arraycopy(encryptedBytes, 0, payloadBytes, iv.size, encryptedBytes.size)

      // Upload to VPS
      val uuid = UUID.randomUUID().toString()
      val originalFileName = getFileName(uri, context) ?: "file"
      val ext = originalFileName.substringAfterLast('.', "")
      val encFileName = "$uuid.${if (ext.isNotEmpty()) ext else "bin"}.enc"

      val client = okhttp3.OkHttpClient.Builder()
        .connectTimeout(30, java.util.concurrent.TimeUnit.SECONDS)
        .writeTimeout(120, java.util.concurrent.TimeUnit.SECONDS)
        .readTimeout(120, java.util.concurrent.TimeUnit.SECONDS)
        .build()

      val request = okhttp3.Request.Builder()
        .url("https://api.jaison.pl/api/attachments/upload")
        .post(payloadBytes.toRequestBody("application/octet-stream".toMediaType()))
        .header("x-file-name", encFileName)
        .build()

      runOnUiThread {
        Toast.makeText(context, "Szyfrowanie i wysyłanie załącznika...", Toast.LENGTH_SHORT).show()
      }

      val response = client.newCall(request).execute()
      if (response.isSuccessful) {
        val respBody = response.body?.string() ?: ""
        val respObj = JSONObject(respBody)
        val fileUrl = respObj.getString("url")

        // Construct JSON attachment metadata
        val attachmentMeta = JSONObject().apply {
          put("type", "attachment")
          put("url", "https://api.jaison.pl$fileUrl")
          put("name", originalFileName)
          put("size", originalBytes.size)
          put("aesKey", Base64.encodeToString(aesKey.encoded, Base64.NO_WRAP))
        }

        // Send Curve25519 E2EE message
        val contact = dbHelper?.listContacts()?.find { it["id"] == contactId }
        val pubKeyB64 = contact?.get("public_key") ?: ""
        if (pubKeyB64.isNotEmpty() && myPrivateKey != null) {
          val recipientPubKey = CryptoHelper.decodePublicKey(pubKeyB64)
          val sharedAesKey = CryptoHelper.deriveSharedKey(myPrivateKey!!, recipientPubKey)
          val encryptedMetadata = CryptoHelper.encrypt(attachmentMeta.toString(), sharedAesKey)

          val wsMessage = JSONObject().apply {
            put("type", "chat_message")
            put("senderId", myUserId)
            put("recipientId", contactId)
            put("payload", JSONObject().apply {
              put("data", encryptedMetadata)
              put("publicKey", CryptoHelper.encodePublicKey(myPublicKey!!))
            })
          }

          wsClient.send(wsMessage.toString())

          // Save locally in database
          dbHelper?.saveMessage(UUID.randomUUID().toString(), contactId, myUserId, attachmentMeta.toString(), false)
          
          runOnUiThread {
            messageListeners.toList().forEach { it.invoke() }
          }
        }
      } else {
        runOnUiThread {
          Toast.makeText(context, "Błąd przesyłania załącznika", Toast.LENGTH_SHORT).show()
        }
      }
    } catch (e: Exception) {
      e.printStackTrace()
      runOnUiThread {
        Toast.makeText(context, "Błąd szyfrowania/wysyłania: ${e.localizedMessage}", Toast.LENGTH_SHORT).show()
      }
    }
  }

  private fun downloadAndOpenAttachment(attachmentJson: String, context: android.content.Context) {
    try {
      val obj = JSONObject(attachmentJson)
      val fileUrl = obj.getString("url")
      val fileName = obj.getString("name")
      val aesKeyB64 = obj.getString("aesKey")

      val client = okhttp3.OkHttpClient()
      val request = okhttp3.Request.Builder().url(fileUrl).build()
      
      Toast.makeText(context, "Pobieranie i odszyfrowywanie pliku...", Toast.LENGTH_SHORT).show()

      client.newCall(request).enqueue(object : okhttp3.Callback {
        override fun onFailure(call: okhttp3.Call, e: java.io.IOException) {
          runOnUiThread {
            Toast.makeText(context, "Błąd pobierania pliku: ${e.localizedMessage}", Toast.LENGTH_SHORT).show()
          }
        }

        override fun onResponse(call: okhttp3.Call, response: okhttp3.Response) {
          if (!response.isSuccessful) {
            runOnUiThread {
              Toast.makeText(context, "Błąd serwera przy pobieraniu pliku", Toast.LENGTH_SHORT).show()
            }
            return
          }

          try {
            val encryptedPayload = response.body?.bytes() ?: return
            
            // Extract IV (12 bytes) and encrypted content
            val iv = ByteArray(12)
            val encryptedBytes = ByteArray(encryptedPayload.size - 12)
            System.arraycopy(encryptedPayload, 0, iv, 0, 12)
            System.arraycopy(encryptedPayload, 12, encryptedBytes, 0, encryptedBytes.size)

            // Reconstruct AES Key
            val decodedKey = Base64.decode(aesKeyB64, Base64.NO_WRAP)
            val aesKey = javax.crypto.spec.SecretKeySpec(decodedKey, "AES")

            // Decrypt with AES-GCM
            val cipher = javax.crypto.Cipher.getInstance("AES/GCM/NoPadding")
            cipher.init(javax.crypto.Cipher.DECRYPT_MODE, aesKey, javax.crypto.spec.GCMParameterSpec(128, iv))
            val decryptedBytes = cipher.doFinal(encryptedBytes)

            // Save decrypted file to Cache directory
            val cacheDir = context.externalCacheDir ?: context.cacheDir
            val outputFile = java.io.File(cacheDir, fileName)
            outputFile.writeBytes(decryptedBytes)

            // Open the file using FileProvider
            val authority = "${context.packageName}.fileprovider"
            val fileUri = androidx.core.content.FileProvider.getUriForFile(context, authority, outputFile)

            val mimeType = context.contentResolver.getType(fileUri) ?: when (outputFile.extension.lowercase()) {
              "pdf" -> "application/pdf"
              "mp4" -> "video/mp4"
              "png" -> "image/png"
              "jpg", "jpeg" -> "image/jpeg"
              "docx" -> "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
              else -> "*/*"
            }

            val intent = android.content.Intent(android.content.Intent.ACTION_VIEW).apply {
              setDataAndType(fileUri, mimeType)
              addFlags(android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION)
              addFlags(android.content.Intent.FLAG_ACTIVITY_NEW_TASK)
            }
            context.startActivity(intent)
          } catch (e: Exception) {
            e.printStackTrace()
            runOnUiThread {
              Toast.makeText(context, "Błąd dekodowania pliku: ${e.localizedMessage}", Toast.LENGTH_SHORT).show()
            }
          }
        }
      })
    } catch (e: Exception) {
      e.printStackTrace()
      Toast.makeText(context, "Błąd: ${e.localizedMessage}", Toast.LENGTH_SHORT).show()
    }
  }

  private fun getFileName(uri: android.net.Uri, context: android.content.Context): String? {
    var result: String? = null
    if (uri.scheme == "content") {
      val cursor = context.contentResolver.query(uri, null, null, null, null)
      try {
        if (cursor != null && cursor.moveToFirst()) {
          val index = cursor.getColumnIndex(android.provider.OpenableColumns.DISPLAY_NAME)
          if (index != -1) {
            result = cursor.getString(index)
          }
        }
      } finally {
        cursor?.close()
      }
    }
    if (result == null) {
      result = uri.path
      val cut = result?.lastIndexOf('/') ?: -1
      if (cut != -1) {
        result = result?.substring(cut + 1)
      }
    }
    return result
  }

  @Composable
  fun SettingsScreen(dbHelper: DatabaseHelper, myUserId: String) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val myPubKeyB64 = dbHelper.getSetting("my_public_key") ?: ""
    var customNvidiaKey by remember { mutableStateOf(dbHelper.getSetting("custom_nvidia_key") ?: "") }
    var customGeminiKey by remember { mutableStateOf(dbHelper.getSetting("custom_gemini_key") ?: "") }

    Column(
      modifier = Modifier
        .fillMaxSize()
        .padding(16.dp)
        .verticalScroll(rememberScrollState()),
      verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
      Text(
        text = "Twój Profil",
        color = MaterialTheme.colorScheme.onBackground,
        fontSize = 18.sp,
        fontWeight = FontWeight.Bold
      )
      
      OutlinedTextField(
        value = myUserId,
        onValueChange = {},
        readOnly = true,
        label = { Text("Mój Identyfikator (User ID)") },
        trailingIcon = {
          IconButton(onClick = {
            val clipboard = context.getSystemService(android.content.Context.CLIPBOARD_SERVICE) as android.content.ClipboardManager
            val clip = android.content.ClipData.newPlainText("User ID", myUserId)
            clipboard.setPrimaryClip(clip)
            Toast.makeText(context, "Skopiowano ID!", Toast.LENGTH_SHORT).show()
          }) {
            Icon(imageVector = Icons.Filled.Share, contentDescription = "Copy")
          }
        },
        modifier = Modifier.fillMaxWidth()
      )

      OutlinedTextField(
        value = myPubKeyB64,
        onValueChange = {},
        readOnly = true,
        label = { Text("Mój Klucz Publiczny") },
        trailingIcon = {
          IconButton(onClick = {
            val clipboard = context.getSystemService(android.content.Context.CLIPBOARD_SERVICE) as android.content.ClipboardManager
            val clip = android.content.ClipData.newPlainText("Public Key", myPubKeyB64)
            clipboard.setPrimaryClip(clip)
            Toast.makeText(context, "Skopiowano klucz publiczny!", Toast.LENGTH_SHORT).show()
          }) {
            Icon(imageVector = Icons.Filled.Share, contentDescription = "Copy")
          }
        },
        modifier = Modifier.fillMaxWidth()
      )

      Box(
        modifier = Modifier
          .fillMaxWidth()
          .height(1.dp)
          .background(MaterialTheme.colorScheme.outlineVariant)
      )

      Text(
        text = "Prywatne Klucze API (Opcjonalne)",
        color = MaterialTheme.colorScheme.onBackground,
        fontSize = 18.sp,
        fontWeight = FontWeight.Bold
      )
      Text(
        text = "Podaj własne klucze, aby telefon wysyłał zapytania bezpośrednio do dostawcy chmury AI.",
        fontSize = 12.sp,
        color = MaterialTheme.colorScheme.secondary
      )

      OutlinedTextField(
        value = customNvidiaKey,
        onValueChange = { customNvidiaKey = it },
        label = { Text("Klucz API NVIDIA") },
        visualTransformation = PasswordVisualTransformation(),
        modifier = Modifier.fillMaxWidth()
      )

      OutlinedTextField(
        value = customGeminiKey,
        onValueChange = { customGeminiKey = it },
        label = { Text("Klucz API Google (Gemini)") },
        visualTransformation = PasswordVisualTransformation(),
        modifier = Modifier.fillMaxWidth()
      )

      Button(
        onClick = {
          dbHelper.saveSetting("custom_nvidia_key", customNvidiaKey)
          dbHelper.saveSetting("custom_gemini_key", customGeminiKey)
          Toast.makeText(context, "Ustawienia zapisane pomyślnie!", Toast.LENGTH_SHORT).show()
        },
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(12.dp)
      ) {
        Text("Zapisz Klucze API")
      }

      Spacer(modifier = Modifier.height(8.dp))

      // --- KARTA E-BOOKA "PRYWATNA TWIERDZA" ---
      var ebookDownloaded by remember { mutableStateOf(dbHelper.getSetting("ebook_downloaded") == "true") }
      var ebookEmail by remember { mutableStateOf("") }
      var isDownloadingEbook by remember { mutableStateOf(false) }
      val isEbookEmailValid = android.util.Patterns.EMAIL_ADDRESS.matcher(ebookEmail).matches()

      Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(
          containerColor = Color.Transparent
        )
      ) {
        Box(
          modifier = Modifier
            .background(
              brush = Brush.linearGradient(
                colors = listOf(Color(0xFF00796B), Color(0xFF004D40))
              )
            )
            .padding(16.dp)
        ) {
          Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
              Box(
                modifier = Modifier
                  .size(40.dp)
                  .background(Color.White.copy(alpha = 0.2f), CircleShape),
                contentAlignment = Alignment.Center
              ) {
                Text("📚", fontSize = 20.sp)
              }
              Spacer(modifier = Modifier.width(12.dp))
              Column {
                Text(
                  text = "Odbierz darmowy E-book! 📚",
                  fontWeight = FontWeight.ExtraBold,
                  fontSize = 18.sp,
                  color = Color.White
                )
                Text(
                  text = "E-book „Prywatna Twierdza” — Bezpieczeństwo i Asysta AI",
                  fontSize = 11.sp,
                  color = Color.White.copy(alpha = 0.8f)
                )
              }
            }

            Text(
              text = "Dowiedz się, jak krok po kroku zabezpieczyć swoje urządzenia, szyfrować komunikację i chronić swoją prywatność przy użyciu lokalnych i chmurowych modeli sztucznej inteligencji. Praktyczny przewodnik napisany specjalnie dla przedsiębiorców dbających o swoje cyfrowe aktywa.",
              fontSize = 12.sp,
              lineHeight = 16.sp,
              color = Color.White.copy(alpha = 0.9f)
            )

            if (ebookDownloaded) {
              Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(8.dp),
                colors = CardDefaults.cardColors(containerColor = Color(0xFF4CAF50).copy(alpha = 0.2f))
              ) {
                Row(
                  modifier = Modifier.padding(12.dp).fillMaxWidth(),
                  horizontalArrangement = Arrangement.Center,
                  verticalAlignment = Alignment.CenterVertically
                ) {
                  Text("🎯 ", fontSize = 16.sp)
                  Text(
                    text = "Dziękujemy za pobranie poradnika!",
                    color = Color(0xFF81C784),
                    fontWeight = FontWeight.Bold,
                    fontSize = 12.sp
                  )
                }
              }
              
              Button(
                onClick = {
                  try {
                    val intent = android.content.Intent(android.content.Intent.ACTION_VIEW, android.net.Uri.parse("https://app.jaison.pl/assets/ebook_prywatna_twierdza.pdf"))
                    context.startActivity(intent)
                  } catch (e: Exception) {
                    Toast.makeText(context, "Nie można otworzyć linku", Toast.LENGTH_SHORT).show()
                  }
                },
                modifier = Modifier.fillMaxWidth(),
                colors = ButtonDefaults.buttonColors(containerColor = Color.White),
                shape = RoundedCornerShape(10.dp)
              ) {
                Text(
                  text = "Otwórz poradnik ponownie 📖",
                  color = Color(0xFF004D40),
                  fontWeight = FontWeight.Bold,
                  fontSize = 12.sp
                )
              }
            } else {
              OutlinedTextField(
                value = ebookEmail,
                onValueChange = { ebookEmail = it },
                label = { Text("Twój adres e-mail", color = Color.White.copy(alpha = 0.7f)) },
                singleLine = true,
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email),
                colors = OutlinedTextFieldDefaults.colors(
                  focusedTextColor = Color.White,
                  unfocusedTextColor = Color.White,
                  focusedBorderColor = Color.White,
                  unfocusedBorderColor = Color.White.copy(alpha = 0.5f),
                  focusedLabelColor = Color.White,
                  unfocusedLabelColor = Color.White.copy(alpha = 0.7f),
                  cursorColor = Color.White
                ),
                modifier = Modifier.fillMaxWidth()
              )

              Spacer(modifier = Modifier.height(4.dp))
              
              val ebookAnnotatedString = androidx.compose.ui.text.buildAnnotatedString {
                append("Zapisując się, akceptujesz ")
                pushStringAnnotation(tag = "URL", annotation = "https://app.jaison.pl/polityka-prywatnosci.html")
                withStyle(style = androidx.compose.ui.text.SpanStyle(
                  color = Color(0xFF80CBC4),
                  textDecoration = androidx.compose.ui.text.style.TextDecoration.Underline,
                  fontWeight = FontWeight.Bold
                )) {
                  append("Politykę Prywatności")
                }
                pop()
                append(". Dane są przetwarzane zgodnie z RODO.")
              }
              
              androidx.compose.foundation.text.ClickableText(
                text = ebookAnnotatedString,
                style = androidx.compose.ui.text.TextStyle(color = Color.White.copy(alpha = 0.7f), fontSize = 10.sp),
                onClick = { offset ->
                  ebookAnnotatedString.getStringAnnotations(tag = "URL", start = offset, end = offset)
                    .firstOrNull()?.let { annotation ->
                      try {
                        val intent = android.content.Intent(android.content.Intent.ACTION_VIEW, android.net.Uri.parse(annotation.item))
                        context.startActivity(intent)
                      } catch (e: Exception) {
                        Toast.makeText(context, "Nie można otworzyć linku", Toast.LENGTH_SHORT).show()
                      }
                    }
                },
                modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp)
              )
              
              Spacer(modifier = Modifier.height(4.dp))

              if (isDownloadingEbook) {
                Box(modifier = Modifier.fillMaxWidth(), contentAlignment = Alignment.Center) {
                  CircularProgressIndicator(color = Color.White)
                }
              } else {
                Button(
                  onClick = {
                    if (!isEbookEmailValid) {
                      Toast.makeText(context, "Proszę wpisać poprawny adres e-mail", Toast.LENGTH_SHORT).show()
                      return@Button
                    }
                    isDownloadingEbook = true
                    scope.launch(Dispatchers.IO) {
                      try {
                        val payload = org.json.JSONObject().apply {
                          put("userId", myUserId)
                          put("email", ebookEmail.trim())
                          put("action", "download_ebook")
                        }
                        val client = okhttp3.OkHttpClient.Builder()
                          .connectTimeout(15, java.util.concurrent.TimeUnit.SECONDS)
                          .readTimeout(15, java.util.concurrent.TimeUnit.SECONDS)
                          .build()
                        val request = okhttp3.Request.Builder()
                          .url("https://api.jaison.pl/api/ebook")
                          .post(payload.toString().toRequestBody("application/json".toMediaType()))
                          .build()
                        
                        client.newCall(request).execute().use { response ->
                          withContext(Dispatchers.Main) {
                            isDownloadingEbook = false
                            dbHelper.saveSetting("ebook_downloaded", "true")
                            ebookDownloaded = true
                            Toast.makeText(context, "📥 Rozpoczynanie pobierania E-booka...", Toast.LENGTH_LONG).show()
                            try {
                              val intent = android.content.Intent(android.content.Intent.ACTION_VIEW, android.net.Uri.parse("https://app.jaison.pl/assets/ebook_prywatna_twierdza.pdf"))
                              context.startActivity(intent)
                            } catch (e: Exception) {
                              Toast.makeText(context, "Nie można otworzyć linku pobierania", Toast.LENGTH_SHORT).show()
                            }
                          }
                        }
                      } catch (e: Exception) {
                        withContext(Dispatchers.Main) {
                          isDownloadingEbook = false
                          // Awaryjnie zapisujemy lokalnie i otwieramy link, aby użytkownik nie napotkał tarcia
                          dbHelper.saveSetting("ebook_downloaded", "true")
                          ebookDownloaded = true
                          Toast.makeText(context, "📥 Pobieranie E-booka (tryb awaryjny)...", Toast.LENGTH_LONG).show()
                          try {
                            val intent = android.content.Intent(android.content.Intent.ACTION_VIEW, android.net.Uri.parse("https://app.jaison.pl/assets/ebook_prywatna_twierdza.pdf"))
                            context.startActivity(intent)
                          } catch (ex: Exception) {
                            Toast.makeText(context, "Nie można otworzyć linku pobierania", Toast.LENGTH_SHORT).show()
                          }
                        }
                      }
                    }
                  },
                  modifier = Modifier.fillMaxWidth(),
                  colors = ButtonDefaults.buttonColors(containerColor = Color.White),
                  shape = RoundedCornerShape(10.dp)
                ) {
                  Text(
                    text = "Odbierz darmowy E-book 📥",
                    color = Color(0xFF004D40),
                    fontWeight = FontWeight.Bold,
                    fontSize = 12.sp
                  )
                }
              }
            }
          }
        }
      }

      Spacer(modifier = Modifier.height(8.dp))

      // --- KARTA DONACJI (BEZPIECZNA / ZASZYTA NA STAŁE) ---
      Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(
          containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.4f)
        )
      ) {
        Column(
          modifier = Modifier.padding(16.dp),
          verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
          Row(verticalAlignment = Alignment.CenterVertically) {
            Box(
              modifier = Modifier
                .size(40.dp)
                .background(Color(0xFFFFD54F), CircleShape),
              contentAlignment = Alignment.Center
            ) {
              Text("☕", fontSize = 20.sp)
            }
            Spacer(modifier = Modifier.width(12.dp))
            Column {
              Text(
                text = "Wesprzyj Projekt J(AI)SON",
                fontWeight = FontWeight.Bold,
                fontSize = 16.sp,
                color = MaterialTheme.colorScheme.onSurface
              )
              Text(
                text = "Pomóż nam rozwijać bezpieczną i wolną komunikację",
                fontSize = 11.sp,
                color = MaterialTheme.colorScheme.onSurfaceVariant
              )
            }
          }

          Text(
            text = "Projekt J(AI)SON jest w pełni darmowy i wolny od reklam. Jeśli asystent i komunikator pomagają Ci w codziennej organizacji, rozważ postawienie wirtualnej kawy. Każde wsparcie zasila rozwój infrastruktury i bezpiecznych, lokalnych modeli AI.",
            fontSize = 12.sp,
            lineHeight = 16.sp,
            color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.8f)
          )

          Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
          ) {
            Button(
              onClick = {
                try {
                  val intent = android.content.Intent(android.content.Intent.ACTION_VIEW, android.net.Uri.parse("https://buycoffee.to/jaison"))
                  context.startActivity(intent)
                } catch (e: Exception) {
                  Toast.makeText(context, "Nie można otworzyć przeglądarki", Toast.LENGTH_SHORT).show()
                }
              },
              modifier = Modifier.weight(1f),
              colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFFFDD00)),
              shape = RoundedCornerShape(8.dp),
              contentPadding = PaddingValues(vertical = 8.dp)
            ) {
              Text("Buy Me A Coffee ☕", color = Color.Black, fontWeight = FontWeight.Bold, fontSize = 11.sp)
            }

            Button(
              onClick = {
                try {
                  val intent = android.content.Intent(android.content.Intent.ACTION_VIEW, android.net.Uri.parse("https://buycoffee.to/jaison"))
                  context.startActivity(intent)
                } catch (e: Exception) {
                  Toast.makeText(context, "Nie można otworzyć przeglądarki", Toast.LENGTH_SHORT).show()
                }
              },
              modifier = Modifier.weight(1f),
              colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF4CAF50)),
              shape = RoundedCornerShape(8.dp),
              contentPadding = PaddingValues(vertical = 8.dp)
            ) {
              Text("BuyCoffee.to (BLIK) ⚡", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 11.sp)
            }
          }
        }
      }

      Spacer(modifier = Modifier.height(8.dp))

      // --- KARTA JASON PRO WAITLIST ---
      var waitlistJoined by remember { mutableStateOf(dbHelper.getSetting("waitlist_joined") == "true") }
      var waitlistEmail by remember { mutableStateOf("") }
      var isJoiningWaitlist by remember { mutableStateOf(false) }
      val isWaitlistEmailValid = android.util.Patterns.EMAIL_ADDRESS.matcher(waitlistEmail).matches()

      Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = Color.Transparent)
      ) {
        Box(
          modifier = Modifier
            .background(
              brush = Brush.linearGradient(
                colors = listOf(Color(0xFF3F51B5), Color(0xFF9C27B0))
              )
            )
            .padding(16.dp)
        ) {
          Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
              Box(
                modifier = Modifier
                  .size(40.dp)
                  .background(Color.White.copy(alpha = 0.2f), CircleShape),
                contentAlignment = Alignment.Center
              ) {
                Text("🚀", fontSize = 20.sp)
              }
              Spacer(modifier = Modifier.width(12.dp))
              Column {
                Text(
                  text = "Nadchodzi JaSon Pro! ⚡",
                  fontWeight = FontWeight.ExtraBold,
                  fontSize = 18.sp,
                  color = Color.White
                )
                Text(
                  text = "Twój osobisty cyfrowy zarząd w kieszeni",
                  fontSize = 11.sp,
                  color = Color.White.copy(alpha = 0.8f)
                )
              }
            }

            Text(
              text = "Przenieś swoją produktywność i ochronę energii na wyższy poziom dzięki zaawansowanym asystentom zintegrowanym w jednym bezpiecznym miejscu:",
              fontSize = 12.sp,
              lineHeight = 16.sp,
              color = Color.White.copy(alpha = 0.9f)
            )

            Column(
              verticalArrangement = Arrangement.spacedBy(6.dp),
              modifier = Modifier.padding(start = 4.dp, end = 4.dp)
            ) {
              Row(verticalAlignment = Alignment.Top) {
                Text("👥 ", fontSize = 12.sp)
                Column {
                  Text("Ghost AI", fontWeight = FontWeight.Bold, fontSize = 12.sp, color = Color.White)
                  Text("Twój cyfrowy klon. Pisze dokładnie tak jak Ty i uczy się Twojego stylu od pierwszej rozmowy.", fontSize = 11.sp, color = Color.White.copy(alpha = 0.8f))
                }
              }
              Row(verticalAlignment = Alignment.Top) {
                Text("🌱 ", fontSize = 12.sp)
                Column {
                  Text("Mentor AI", fontWeight = FontWeight.Bold, fontSize = 12.sp, color = Color.White)
                  Text("Doradca osobisty dbający o nawyki, poziom energii i chroniący przed przebodźcowaniem.", fontSize = 11.sp, color = Color.White.copy(alpha = 0.8f))
                }
              }
              Row(verticalAlignment = Alignment.Top) {
                Text("⚙️ ", fontSize = 12.sp)
                Column {
                  Text("CO AI (Orkiestrator)", fontWeight = FontWeight.Bold, fontSize = 12.sp, color = Color.White)
                  Text("Twój dyrektor operacyjny. Planuje zadania i odpala asynchroniczne automatyzacje.", fontSize = 11.sp, color = Color.White.copy(alpha = 0.8f))
                }
              }
              Row(verticalAlignment = Alignment.Top) {
                Text("⚖️ ", fontSize = 12.sp)
                Column {
                  Text("Dział Prawno-Podatkowy AI", fontWeight = FontWeight.Bold, fontSize = 12.sp, color = Color.White)
                  Text("Natychmiastowe wsparcie w analizie przepisów, RODO i optymalizacji kosztów.", fontSize = 11.sp, color = Color.White.copy(alpha = 0.8f))
                }
              }
              Row(verticalAlignment = Alignment.Top) {
                Text("🧠 ", fontSize = 12.sp)
                Column {
                  Text("Neuro-profilowanie", fontWeight = FontWeight.Bold, fontSize = 12.sp, color = Color.White)
                  Text("Wywiad Discovery (6 sekcji) dostosowujący styl i tempo asysty do Twojej osobowości lub ADHD.", fontSize = 11.sp, color = Color.White.copy(alpha = 0.8f))
                }
              }
            }

            Spacer(modifier = Modifier.height(4.dp))

            if (waitlistJoined) {
              Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(8.dp),
                colors = CardDefaults.cardColors(containerColor = Color(0xFF4CAF50).copy(alpha = 0.2f))
              ) {
                Row(
                  modifier = Modifier.padding(12.dp).fillMaxWidth(),
                  horizontalArrangement = Arrangement.Center,
                  verticalAlignment = Alignment.CenterVertically
                ) {
                  Text("🎯 ", fontSize = 16.sp)
                  Text(
                    text = "Jesteś na liście oczekujących JaSon Pro!",
                    color = Color(0xFF81C784),
                    fontWeight = FontWeight.Bold,
                    fontSize = 12.sp
                  )
                }
              }
            } else {
              OutlinedTextField(
                value = waitlistEmail,
                onValueChange = { waitlistEmail = it },
                label = { Text("Wpisz swój e-mail", color = Color.White.copy(alpha = 0.7f)) },
                singleLine = true,
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email),
                colors = OutlinedTextFieldDefaults.colors(
                  focusedTextColor = Color.White,
                  unfocusedTextColor = Color.White,
                  focusedBorderColor = Color.White,
                  unfocusedBorderColor = Color.White.copy(alpha = 0.5f),
                  focusedLabelColor = Color.White,
                  unfocusedLabelColor = Color.White.copy(alpha = 0.7f),
                  cursorColor = Color.White
                ),
                modifier = Modifier.fillMaxWidth()
              )

              Spacer(modifier = Modifier.height(4.dp))
              
              val waitlistAnnotatedString = androidx.compose.ui.text.buildAnnotatedString {
                append("Zapisując się, akceptujesz ")
                pushStringAnnotation(tag = "URL", annotation = "https://app.jaison.pl/polityka-prywatnosci.html")
                withStyle(style = androidx.compose.ui.text.SpanStyle(
                  color = Color(0xFF80CBC4),
                  textDecoration = androidx.compose.ui.text.style.TextDecoration.Underline,
                  fontWeight = FontWeight.Bold
                )) {
                  append("Politykę Prywatności")
                }
                pop()
                append(". Dane są przetwarzane zgodnie z RODO.")
              }
              
              androidx.compose.foundation.text.ClickableText(
                text = waitlistAnnotatedString,
                style = androidx.compose.ui.text.TextStyle(color = Color.White.copy(alpha = 0.7f), fontSize = 10.sp),
                onClick = { offset ->
                  waitlistAnnotatedString.getStringAnnotations(tag = "URL", start = offset, end = offset)
                    .firstOrNull()?.let { annotation ->
                      try {
                        val intent = android.content.Intent(android.content.Intent.ACTION_VIEW, android.net.Uri.parse(annotation.item))
                        context.startActivity(intent)
                      } catch (e: Exception) {
                        Toast.makeText(context, "Nie można otworzyć linku", Toast.LENGTH_SHORT).show()
                      }
                    }
                },
                modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp)
              )
              
              Spacer(modifier = Modifier.height(4.dp))

              if (isJoiningWaitlist) {
                Box(modifier = Modifier.fillMaxWidth(), contentAlignment = Alignment.Center) {
                  CircularProgressIndicator(color = Color.White)
                }
              } else {
                Button(
                  onClick = {
                    if (!isWaitlistEmailValid) {
                      Toast.makeText(context, "Proszę wpisać poprawny adres e-mail", Toast.LENGTH_SHORT).show()
                      return@Button
                    }
                    isJoiningWaitlist = true
                    scope.launch(Dispatchers.IO) {
                      try {
                        val payload = org.json.JSONObject().apply {
                          put("userId", myUserId)
                          put("email", waitlistEmail.trim())
                          put("action", "join_waitlist")
                        }
                        val client = okhttp3.OkHttpClient.Builder()
                          .connectTimeout(15, java.util.concurrent.TimeUnit.SECONDS)
                          .readTimeout(15, java.util.concurrent.TimeUnit.SECONDS)
                          .build()
                        val request = okhttp3.Request.Builder()
                          .url("https://api.jaison.pl/api/waitlist")
                          .post(payload.toString().toRequestBody("application/json".toMediaType()))
                          .build()
                        
                        client.newCall(request).execute().use { response ->
                          withContext(Dispatchers.Main) {
                            isJoiningWaitlist = false
                            dbHelper.saveSetting("waitlist_joined", "true")
                            waitlistJoined = true
                            Toast.makeText(context, "🎯 Gratulacje! Zostałeś zapisany na listę oczekujących JaSon Pro!", Toast.LENGTH_LONG).show()
                          }
                        }
                      } catch (e: Exception) {
                        withContext(Dispatchers.Main) {
                          isJoiningWaitlist = false
                          // Awaryjnie zapisujemy lokalnie, żeby użytkownik nie czuł "tarcia" przy problemach z siecią
                          dbHelper.saveSetting("waitlist_joined", "true")
                          waitlistJoined = true
                          Toast.makeText(context, "Zapisano lokalnie! Poinformujemy Cię o premierze. 🚀", Toast.LENGTH_LONG).show()
                        }
                      }
                    }
                  },
                  modifier = Modifier.fillMaxWidth(),
                  colors = ButtonDefaults.buttonColors(containerColor = Color.White),
                  shape = RoundedCornerShape(10.dp)
                ) {
                  Text(
                    text = "Zapisz się na listę oczekujących 🚀",
                    color = Color(0xFF6200EE),
                    fontWeight = FontWeight.ExtraBold
                  )
                }
              }
            }
          }
        }
      }
    }
  }
  @Composable
  fun CallScreen(
    peerName: String,
    status: String,
    isSpeakerOn: Boolean,
    onToggleSpeaker: () -> Unit,
    onAnswer: (() -> Unit)? = null,
    onHangup: () -> Unit
  ) {
    Column(
      modifier = Modifier
        .fillMaxSize()
        .background(MaterialTheme.colorScheme.background)
        .padding(24.dp),
      horizontalAlignment = Alignment.CenterHorizontally,
      verticalArrangement = Arrangement.SpaceBetween
    ) {
      Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = Modifier.padding(top = 64.dp)
      ) {
        Box(
          modifier = Modifier
            .size(100.dp)
            .background(MaterialTheme.colorScheme.primaryContainer, CircleShape),
          contentAlignment = Alignment.Center
        ) {
          Icon(
            imageVector = Icons.Filled.AccountCircle,
            contentDescription = "User Avatar",
            modifier = Modifier.size(64.dp),
            tint = MaterialTheme.colorScheme.onPrimaryContainer
          )
        }
        Spacer(modifier = Modifier.height(16.dp))
        Text(text = peerName, fontWeight = FontWeight.Bold, fontSize = 24.sp, color = MaterialTheme.colorScheme.onBackground)
        Spacer(modifier = Modifier.height(8.dp))
        Text(text = status, color = MaterialTheme.colorScheme.secondary, fontSize = 16.sp)
      }

      if (status == "Incoming call..." && onAnswer != null) {
        Row(
          modifier = Modifier
            .padding(bottom = 64.dp)
            .fillMaxWidth(),
          horizontalArrangement = Arrangement.SpaceEvenly
        ) {
          // Accept Button
          Button(
            onClick = onAnswer,
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF4CAF50)),
            shape = CircleShape,
            modifier = Modifier.size(64.dp)
          ) {
            Icon(
              imageVector = Icons.Filled.Phone,
              contentDescription = "Answer Call",
              tint = Color.White,
              modifier = Modifier.size(32.dp)
            )
          }

          // Decline Button
          Button(
            onClick = onHangup,
            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error),
            shape = CircleShape,
            modifier = Modifier.size(64.dp)
          ) {
            Icon(
              imageVector = Icons.Filled.Phone,
              contentDescription = "Decline Call",
              tint = Color.White,
              modifier = Modifier.size(32.dp).rotate(135f)
            )
          }
        }
      } else {
        Row(
          modifier = Modifier
            .padding(bottom = 64.dp)
            .fillMaxWidth(),
          horizontalArrangement = Arrangement.SpaceEvenly
        ) {
          // Speaker Button
          Button(
            onClick = onToggleSpeaker,
            colors = ButtonDefaults.buttonColors(containerColor = if (isSpeakerOn) Color(0xFF4CAF50) else Color.DarkGray),
            shape = CircleShape,
            modifier = Modifier.size(64.dp),
            contentPadding = PaddingValues(0.dp)
          ) {
            Icon(
              imageVector = if (isSpeakerOn) VolumeUpIcon else VolumeOffIcon,
              contentDescription = "Toggle Speakerphone",
              tint = Color.White,
              modifier = Modifier.size(32.dp)
            )
          }

          // Decline / Hangup Button
          Button(
            onClick = onHangup,
            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error),
            shape = CircleShape,
            modifier = Modifier.size(64.dp)
          ) {
            Icon(
              imageVector = Icons.Filled.Phone,
              contentDescription = "End Call",
              tint = Color.White,
              modifier = Modifier.size(32.dp).rotate(135f)
            )
          }
        }
      }
    }
  }

  // --- Screen State definitions ---
  sealed class Screen {
    object Unlock : Screen()
    data class SetupProfile(val pin: String) : Screen()
    object Home : Screen()
    object Chat : Screen()
    object Call : Screen()
  }

  // --- Theme ---
  @Composable
  fun HermesTheme(content: @Composable () -> Unit) {
    val darkColorScheme = darkColorScheme(
      primary = Color(0xFF82B1FF),
      onPrimary = Color(0xFF002F6C),
      primaryContainer = Color(0xFF1E2A3A),
      onPrimaryContainer = Color(0xFF82B1FF),
      secondary = Color(0xFFB0BEC5),
      onSecondary = Color(0xFF263238),
      background = Color(0xFF121212),
      onBackground = Color(0xFFE0E0E0),
      surface = Color(0xFF1E1E1E),
      onSurface = Color(0xFFE0E0E0),
      surfaceVariant = Color(0xFF2D2D2D),
      onSurfaceVariant = Color(0xFFE0E0E0),
      error = Color(0xFFE57373)
    )

    val defaultTypography = Typography(
      titleLarge = androidx.compose.ui.text.TextStyle(
        fontWeight = FontWeight.ExtraBold,
        fontSize = 22.sp,
        lineHeight = 28.sp,
        letterSpacing = 0.5.sp
      ),
      titleMedium = androidx.compose.ui.text.TextStyle(
        fontWeight = FontWeight.Bold,
        fontSize = 18.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.25.sp
      ),
      bodyLarge = androidx.compose.ui.text.TextStyle(
        fontWeight = FontWeight.Normal,
        fontSize = 15.sp,
        lineHeight = 22.sp,
        letterSpacing = 0.25.sp
      ),
      bodyMedium = androidx.compose.ui.text.TextStyle(
        fontWeight = FontWeight.Normal,
        fontSize = 13.sp,
        lineHeight = 18.sp,
        letterSpacing = 0.2.sp
      ),
      labelMedium = androidx.compose.ui.text.TextStyle(
        fontWeight = FontWeight.Medium,
        fontSize = 12.sp,
        lineHeight = 16.sp,
        letterSpacing = 0.5.sp
      )
    )

    MaterialTheme(
      colorScheme = darkColorScheme,
      typography = defaultTypography,
      content = content
    )
  }
}

private var _attachmentIcon: ImageVector? = null

val AttachmentIcon: ImageVector
  get() {
    if (_attachmentIcon != null) {
      return _attachmentIcon!!
    }
    _attachmentIcon = ImageVector.Builder(
      name = "Attachment",
      defaultWidth = 24.dp,
      defaultHeight = 24.dp,
      viewportWidth = 24f,
      viewportHeight = 24f
    ).path(
      fill = SolidColor(Color.White),
      pathFillType = PathFillType.NonZero
    ) {
      moveTo(16.5f, 6.0f)
      verticalLineToRelative(11.5f)
      curveToRelative(0.0f, 2.21f, -1.79f, 4.0f, -4.0f, 4.0f)
      reflectiveCurveToRelative(-4.0f, -1.79f, -4.0f, -4.0f)
      verticalLineTo(5.0f)
      curveToRelative(0.0f, -3.31f, 2.69f, -6.0f, 6.0f, -6.0f)
      reflectiveCurveToRelative(6.0f, 2.69f, 6.0f, 6.0f)
      verticalLineToRelative(11.5f)
      curveToRelative(0.0f, 1.38f, -1.12f, 2.5f, -2.5f, 2.5f)
      reflectiveCurveToRelative(-2.5f, -1.12f, -2.5f, -2.5f)
      verticalLineTo(6.0f)
      horizontalLineTo(13.0f)
      verticalLineToRelative(10.5f)
      curveToRelative(0.0f, 2.48f, 2.02f, 4.5f, 4.5f, 4.5f)
      reflectiveCurveToRelative(4.5f, -2.02f, 4.5f, -4.5f)
      verticalLineTo(5.0f)
      curveToRelative(0.0f, -4.42f, -3.58f, -8.0f, -8.0f, -8.0f)
      reflectiveCurveToRelative(-8.0f, 3.58f, -8.0f, 8.0f)
      verticalLineToRelative(12.5f)
      curveToRelative(0.0f, 1.1f, 0.9f, 2.0f, 2.0f, 2.0f)
      reflectiveCurveToRelative(2.0f, -0.9f, 2.0f, -2.0f)
      verticalLineTo(6.0f)
      horizontalLineToRelative(1.5f)
      close()
    }.build()
    return _attachmentIcon!!
  }

private var _volumeUpIcon: ImageVector? = null

val VolumeUpIcon: ImageVector
  get() {
    if (_volumeUpIcon != null) {
      return _volumeUpIcon!!
    }
    _volumeUpIcon = ImageVector.Builder(
      name = "VolumeUp",
      defaultWidth = 24.dp,
      defaultHeight = 24.dp,
      viewportWidth = 24f,
      viewportHeight = 24f
    ).path(
      fill = SolidColor(Color.White),
      pathFillType = PathFillType.NonZero
    ) {
      moveTo(3f, 9f)
      verticalLineToRelative(6f)
      horizontalLineToRelative(4f)
      lineTo(12f, 20f)
      verticalLineTo(4f)
      lineTo(7f, 9f)
      horizontalLineTo(3f)
      close()
      
      moveTo(14.5f, 12f)
      curveToRelative(0f, -1.77f, -1.02f, -3.29f, -2.5f, -4.03f)
      verticalLineToRelative(8.05f)
      curveToRelative(1.48f, -0.73f, 2.5f, -2.25f, 2.5f, -4.02f)
      close()
      
      moveTo(14f, 3.23f)
      verticalLineToRelative(2.06f)
      curveToRelative(2.89f, 0.86f, 5f, 3.54f, 5f, 6.71f)
      reflectiveCurveToRelative(-2.11f, 5.85f, -5f, 6.71f)
      verticalLineToRelative(2.06f)
      curveToRelative(4.01f, -0.91f, 7f, -4.49f, 7f, -8.77f)
      reflectiveCurveToRelative(-2.99f, -7.86f, -7f, -8.77f)
      close()
    }.build()
    return _volumeUpIcon!!
  }

private var _volumeOffIcon: ImageVector? = null

val VolumeOffIcon: ImageVector
  get() {
    if (_volumeOffIcon != null) {
      return _volumeOffIcon!!
    }
    _volumeOffIcon = ImageVector.Builder(
      name = "VolumeOff",
      defaultWidth = 24.dp,
      defaultHeight = 24.dp,
      viewportWidth = 24f,
      viewportHeight = 24f
    ).path(
      fill = SolidColor(Color.White),
      pathFillType = PathFillType.NonZero
    ) {
      moveTo(16.5f, 12f)
      curveToRelative(0f, -1.77f, -1.02f, -3.29f, -2.5f, -4.03f)
      verticalLineToRelative(2.21f)
      lineToRelative(2.45f, 2.45f)
      curveToRelative(0.03f, -0.21f, 0.05f, -0.42f, 0.05f, -0.63f)
      close()
      
      moveTo(19f, 12f)
      curveToRelative(0f, 0.94f, -0.2f, 1.82f, -0.54f, 2.64f)
      lineToRelative(1.51f, 1.51f)
      curveTo(20.63f, 14.91f, 21f, 13.5f, 21f, 12f)
      curveToRelative(0f, -4.28f, -2.99f, -7.86f, -7f, -8.77f)
      verticalLineToRelative(2.06f)
      curveToRelative(2.89f, 0.86f, 5f, 3.54f, 5f, 6.71f)
      close()
      
      moveTo(4.27f, 3f)
      lineTo(3f, 4.27f)
      lineTo(7.73f, 9f)
      horizontalLineTo(3f)
      verticalLineToRelative(6f)
      horizontalLineToRelative(4f)
      lineTo(12f, 20f)
      verticalLineToRelative(-6.73f)
      lineToRelative(4.25f, 4.25f)
      curveToRelative(-0.67f, 0.52f, -1.42f, 0.93f, -2.25f, 1.18f)
      verticalLineToRelative(2.06f)
      curveToRelative(1.38f, -0.31f, 2.63f, -0.95f, 3.69f, -1.81f)
      lineTo(19.73f, 21f)
      lineTo(21f, 19.73f)
      lineToRelative(-9f, -9f)
      lineTo(4.27f, 3f)
      close()
      
      moveTo(12f, 4f)
      lineToRelative(-2.09f, 2.09f)
      lineTo(12f, 8.18f)
      verticalLineTo(4f)
      close()
    }.build()
    return _volumeOffIcon!!
  }
