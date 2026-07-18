package com.hermes.messenger.network

import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response
import okhttp3.WebSocket
import okhttp3.WebSocketListener
import java.util.concurrent.TimeUnit

class WebSocketClient {

  enum class State {
    DISCONNECTED,
    CONNECTING,
    CONNECTED
  }

  private val client = OkHttpClient.Builder()
    .readTimeout(0, TimeUnit.MILLISECONDS) // Keeps connection alive
    .pingInterval(15, TimeUnit.SECONDS) // Automatically sends pings to keep Nginx from dropping idle connections
    .build()

  private var webSocket: WebSocket? = null
  
  @Volatile
  private var connectionState = State.DISCONNECTED

  val state: State
    get() = connectionState

  interface Listener {
    fun onConnected()
    fun onDisconnected()
    fun onMessageReceived(text: String)
    fun onError(t: Throwable)
  }

  fun connect(url: String, listener: Listener) {
    synchronized(this) {
      if (connectionState != State.DISCONNECTED) {
        return
      }
      connectionState = State.CONNECTING
    }

    // Cancel any existing websocket to ensure no duplicate connections
    try {
      webSocket?.cancel()
    } catch (e: Exception) {
      // Ignore
    }
    webSocket = null

    val request = Request.Builder()
      .url(url)
      .build()

    webSocket = client.newWebSocket(request, object : WebSocketListener() {
      override fun onOpen(webSocket: WebSocket, response: Response) {
        synchronized(this@WebSocketClient) {
          connectionState = State.CONNECTED
        }
        listener.onConnected()
      }

      override fun onMessage(webSocket: WebSocket, text: String) {
        listener.onMessageReceived(text)
      }

      override fun onClosing(webSocket: WebSocket, code: Int, reason: String) {
        webSocket.close(1000, null)
      }

      override fun onClosed(webSocket: WebSocket, code: Int, reason: String) {
        synchronized(this@WebSocketClient) {
          connectionState = State.DISCONNECTED
        }
        listener.onDisconnected()
      }

      override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
        synchronized(this@WebSocketClient) {
          connectionState = State.DISCONNECTED
        }
        listener.onError(t)
      }
    })
  }

  fun send(messageJson: String): Boolean {
    return webSocket?.send(messageJson) ?: false
  }

  fun disconnect() {
    try {
      webSocket?.close(1000, "Goodbye")
    } catch (e: Exception) {
      try {
        webSocket?.cancel()
      } catch (ex: Exception) {}
    }
    synchronized(this) {
      connectionState = State.DISCONNECTED
    }
  }
}

