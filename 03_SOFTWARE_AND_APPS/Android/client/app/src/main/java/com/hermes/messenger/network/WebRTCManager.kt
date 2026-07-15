package com.hermes.messenger.network

import android.content.Context
import android.util.Log
import org.json.JSONObject
import org.webrtc.*
import java.util.ArrayList

class WebRTCManager(
  private val context: Context,
  private val onSignalingMessage: (JSONObject) -> Unit,
  private val onCallStateChanged: (String) -> Unit
) {

  companion object {
    private const val TAG = "WebRTCManager"
  }

  private var peerConnectionFactory: PeerConnectionFactory? = null
  private var peerConnection: PeerConnection? = null
  private var localAudioSource: AudioSource? = null
  private var localAudioTrack: AudioTrack? = null
  private val pendingIceCandidates = mutableListOf<IceCandidate>()

  init {
    initializePeerConnectionFactory()
  }

  private fun initializePeerConnectionFactory() {
    org.webrtc.ContextUtils.initialize(context)
    val options = PeerConnectionFactory.InitializationOptions.builder(context)
      .setEnableInternalTracer(true)
      .createInitializationOptions()
    PeerConnectionFactory.initialize(options)

    val audioDeviceModule = org.webrtc.audio.JavaAudioDeviceModule.builder(context)
      .setUseHardwareAcousticEchoCanceler(org.webrtc.audio.JavaAudioDeviceModule.isBuiltInAcousticEchoCancelerSupported())
      .setUseHardwareNoiseSuppressor(org.webrtc.audio.JavaAudioDeviceModule.isBuiltInNoiseSuppressorSupported())
      .setAudioRecordErrorCallback(object : org.webrtc.audio.JavaAudioDeviceModule.AudioRecordErrorCallback {
          override fun onWebRtcAudioRecordInitError(errorMessage: String?) {
              Log.e(TAG, "AudioRecord init error: $errorMessage")
          }
          override fun onWebRtcAudioRecordStartError(errorCode: org.webrtc.audio.JavaAudioDeviceModule.AudioRecordStartErrorCode?, errorMessage: String?) {
              Log.e(TAG, "AudioRecord start error: $errorMessage")
          }
          override fun onWebRtcAudioRecordError(errorMessage: String?) {
              Log.e(TAG, "AudioRecord error: $errorMessage")
          }
      })
      .setAudioTrackErrorCallback(object : org.webrtc.audio.JavaAudioDeviceModule.AudioTrackErrorCallback {
          override fun onWebRtcAudioTrackInitError(errorMessage: String?) {
              Log.e(TAG, "AudioTrack init error: $errorMessage")
          }
          override fun onWebRtcAudioTrackStartError(errorCode: org.webrtc.audio.JavaAudioDeviceModule.AudioTrackStartErrorCode?, errorMessage: String?) {
              Log.e(TAG, "AudioTrack start error: $errorMessage")
          }
          override fun onWebRtcAudioTrackError(errorMessage: String?) {
              Log.e(TAG, "AudioTrack error: $errorMessage")
          }
      })
      .createAudioDeviceModule()

    peerConnectionFactory = PeerConnectionFactory.builder()
      .setOptions(PeerConnectionFactory.Options())
      .setAudioDeviceModule(audioDeviceModule)
      .createPeerConnectionFactory()

    audioDeviceModule.release() // Releasing the module after the factory takes ownership
    Log.d(TAG, "PeerConnectionFactory initialized successfully with JavaAudioDeviceModule")
  }

  fun startCall(recipientId: String) {
    Log.d(TAG, "Starting call to recipient: $recipientId")
    createPeerConnection(recipientId)

    val constraints = MediaConstraints().apply {
      mandatory.add(MediaConstraints.KeyValuePair("OfferToReceiveAudio", "true"))
      mandatory.add(MediaConstraints.KeyValuePair("OfferToReceiveVideo", "false"))
    }

    peerConnection?.createOffer(object : SdpObserver {
      override fun onCreateSuccess(sdp: SessionDescription) {
        Log.d(TAG, "Offer SDP created successfully")
        peerConnection?.setLocalDescription(object : SdpObserver {
          override fun onCreateSuccess(desc: SessionDescription?) {}
          override fun onSetSuccess() {
            Log.d(TAG, "Local Description set successfully for Offer")
            // Send Offer signaling message
            val signal = JSONObject().apply {
              put("type", "offer")
              put("sdp", sdp.description)
            }
            onSignalingMessage(signal)
          }
          override fun onCreateFailure(error: String?) {}
          override fun onSetFailure(error: String?) {
            Log.e(TAG, "Failed to set local description for Offer: $error")
          }
        }, sdp)
      }

      override fun onSetSuccess() {}
      override fun onCreateFailure(error: String?) {
        Log.e(TAG, "Failed to create WebRTC Offer: $error")
      }
      override fun onSetFailure(error: String?) {}
    }, constraints)
  }

  fun handleIncomingOffer(offerDescription: String, recipientId: String) {
    Log.d(TAG, "Handling incoming WebRTC Offer from: $recipientId")
    createPeerConnection(recipientId)

    val sessionDesc = SessionDescription(SessionDescription.Type.OFFER, offerDescription)
    peerConnection?.setRemoteDescription(object : SdpObserver {
      override fun onCreateSuccess(desc: SessionDescription?) {}
      override fun onSetSuccess() {
        Log.d(TAG, "Remote Description (Offer) set successfully")
        drainPendingIceCandidates()
        createAnswer()
      }
      override fun onCreateFailure(error: String?) {}
      override fun onSetFailure(error: String?) {
        Log.e(TAG, "Failed to set Remote Description (Offer): $error")
      }
    }, sessionDesc)
  }

  fun handleIncomingAnswer(answerDescription: String) {
    Log.d(TAG, "Handling incoming WebRTC Answer")
    val sessionDesc = SessionDescription(SessionDescription.Type.ANSWER, answerDescription)
    peerConnection?.setRemoteDescription(object : SdpObserver {
      override fun onCreateSuccess(desc: SessionDescription?) {}
      override fun onSetSuccess() {
        Log.d(TAG, "Remote Description (Answer) set successfully. WebRTC Connected.")
        drainPendingIceCandidates()
        onCallStateChanged("Connected")
      }
      override fun onCreateFailure(error: String?) {}
      override fun onSetFailure(error: String?) {
        Log.e(TAG, "Failed to set Remote Description (Answer): $error")
      }
    }, sessionDesc)
  }

  fun handleIncomingIceCandidate(sdpMid: String, sdpMLineIndex: Int, sdp: String) {
    Log.d(TAG, "Handling incoming ICE candidate")
    val candidate = IceCandidate(sdpMid, sdpMLineIndex, sdp)
    if (peerConnection?.remoteDescription != null) {
      peerConnection?.addIceCandidate(candidate)
    } else {
      pendingIceCandidates.add(candidate)
    }
  }

  private fun drainPendingIceCandidates() {
    val candidatesToDrain = pendingIceCandidates.toList()
    pendingIceCandidates.clear()
    for (candidate in candidatesToDrain) {
      peerConnection?.addIceCandidate(candidate)
    }
  }

  private fun createAnswer() {
    val constraints = MediaConstraints().apply {
      mandatory.add(MediaConstraints.KeyValuePair("OfferToReceiveAudio", "true"))
      mandatory.add(MediaConstraints.KeyValuePair("OfferToReceiveVideo", "false"))
    }

    peerConnection?.createAnswer(object : SdpObserver {
      override fun onCreateSuccess(sdp: SessionDescription) {
        Log.d(TAG, "Answer SDP created successfully")
        peerConnection?.setLocalDescription(object : SdpObserver {
          override fun onCreateSuccess(desc: SessionDescription?) {}
          override fun onSetSuccess() {
            Log.d(TAG, "Local Description set successfully for Answer")
            // Send Answer signaling message
            val signal = JSONObject().apply {
              put("type", "answer")
              put("sdp", sdp.description)
            }
            onSignalingMessage(signal)
          }
          override fun onCreateFailure(error: String?) {}
          override fun onSetFailure(error: String?) {
            Log.e(TAG, "Failed to set local description for Answer: $error")
          }
        }, sdp)
      }

      override fun onSetSuccess() {}
      override fun onCreateFailure(error: String?) {
        Log.e(TAG, "Failed to create WebRTC Answer: $error")
      }
      override fun onSetFailure(error: String?) {}
    }, constraints)
  }

  private fun createPeerConnection(recipientId: String) {
    val iceServers = ArrayList<PeerConnection.IceServer>()
    iceServers.add(PeerConnection.IceServer.builder("stun:stun.l.google.com:19302").createIceServer())
    iceServers.add(PeerConnection.IceServer.builder("turn:openrelay.metered.ca:80")
      .setUsername("openrelayproject")
      .setPassword("openrelayproject")
      .createIceServer())
    iceServers.add(PeerConnection.IceServer.builder("turn:openrelay.metered.ca:443")
      .setUsername("openrelayproject")
      .setPassword("openrelayproject")
      .createIceServer())
    val rtcConfig = PeerConnection.RTCConfiguration(iceServers).apply {
      sdpSemantics = PeerConnection.SdpSemantics.UNIFIED_PLAN
    }

    peerConnection = peerConnectionFactory?.createPeerConnection(rtcConfig, object : PeerConnection.Observer {
      override fun onSignalingChange(state: PeerConnection.SignalingState?) {}
      
      override fun onIceConnectionChange(state: PeerConnection.IceConnectionState?) {
        Log.d(TAG, "IceConnectionState changed to: $state")
        when (state) {
          PeerConnection.IceConnectionState.CONNECTED -> onCallStateChanged("Connected")
          PeerConnection.IceConnectionState.DISCONNECTED,
          PeerConnection.IceConnectionState.FAILED -> onCallStateChanged("Disconnected")
          else -> {}
        }
      }

      override fun onConnectionChange(state: PeerConnection.PeerConnectionState?) {
        Log.d(TAG, "onConnectionChange: $state")
        if (state == PeerConnection.PeerConnectionState.CONNECTED) {
          onCallStateChanged("Connected")
        } else if (state == PeerConnection.PeerConnectionState.DISCONNECTED ||
                   state == PeerConnection.PeerConnectionState.FAILED) {
          onCallStateChanged("Disconnected")
        }
      }

      override fun onIceConnectionReceivingChange(receiving: Boolean) {}
      override fun onIceGatheringChange(state: PeerConnection.IceGatheringState?) {}

      override fun onIceCandidate(candidate: IceCandidate) {
        Log.d(TAG, "New local ICE candidate gathered")
        // Send ICE candidate signaling message
        val signal = JSONObject().apply {
          put("type", "candidate")
          put("sdp", candidate.sdp)
          put("sdpMid", candidate.sdpMid)
          put("sdpMLineIndex", candidate.sdpMLineIndex)
        }
        onSignalingMessage(signal)
      }

      override fun onIceCandidatesRemoved(candidates: Array<out IceCandidate>?) {}
      override fun onAddStream(stream: MediaStream?) {}
      override fun onRemoveStream(stream: MediaStream?) {}
      
      override fun onDataChannel(channel: DataChannel?) {}
      override fun onRenegotiationNeeded() {}

      override fun onAddTrack(receiver: RtpReceiver?, mediaStreams: Array<out MediaStream>?) {
        Log.d(TAG, "Remote track added")
        if (receiver?.track()?.kind() == "audio") {
          Log.d(TAG, "Audio stream received from peer")
        }
      }

      override fun onTrack(transceiver: RtpTransceiver?) {
        Log.d(TAG, "onTrack: ${transceiver?.mid}")
      }

      override fun onRemoveTrack(receiver: RtpReceiver?) {
        Log.d(TAG, "onRemoveTrack: ${receiver?.id()}")
      }

      override fun onSelectedCandidatePairChanged(event: CandidatePairChangeEvent?) {
        Log.d(TAG, "onSelectedCandidatePairChanged: $event")
      }
    })

    // Capture and add local audio track with try-catch block to prevent crashes due to mic permissions or hardware initialization errors
    try {
      val audioConstraints = MediaConstraints()
      localAudioSource = peerConnectionFactory?.createAudioSource(audioConstraints)
      localAudioTrack = peerConnectionFactory?.createAudioTrack("local_audio_track_id", localAudioSource)
      localAudioTrack?.let { track ->
        peerConnection?.addTrack(track, listOf("local_media_stream_id"))
        Log.d(TAG, "Local audio track added to PeerConnection")
      } ?: Log.e(TAG, "Failed to create local audio track, localAudioTrack is null")
    } catch (e: Exception) {
      Log.e(TAG, "Error capturing local audio: ${e.localizedMessage}")
    }
  }

  fun endCall() {
    Log.d(TAG, "Ending call and releasing WebRTC resources")
    pendingIceCandidates.clear()
    peerConnection?.close()
    peerConnection = null
    localAudioTrack?.setEnabled(false)
    localAudioTrack?.dispose()
    localAudioTrack = null
    localAudioSource?.dispose()
    localAudioSource = null
    onCallStateChanged("Disconnected")
  }
}
