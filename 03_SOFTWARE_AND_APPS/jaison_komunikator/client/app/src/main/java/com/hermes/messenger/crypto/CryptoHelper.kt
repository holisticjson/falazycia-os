package com.hermes.messenger.crypto

import android.util.Base64
import java.security.KeyFactory
import java.security.KeyPair
import java.security.KeyPairGenerator
import java.security.PrivateKey
import java.security.PublicKey
import java.security.SecureRandom
import java.security.spec.X509EncodedKeySpec
import javax.crypto.Cipher
import javax.crypto.KeyAgreement
import javax.crypto.spec.GCMParameterSpec
import javax.crypto.spec.SecretKeySpec
import java.security.MessageDigest

object CryptoHelper {

  private const val ALGORITHM_EC = "EC"
  private const val ALGORITHM_ECDH = "ECDH"
  private const val ALGORITHM_AES_GCM = "AES/GCM/NoPadding"
  private const val TAG_LENGTH_BIT = 128
  private const val IV_LENGTH_BYTE = 12

  /**
   * Generates a standard Elliptic Curve keypair for E2EE key exchange (supported on all Android versions)
   */
  fun generateKeyPair(): KeyPair {
    val kpg = KeyPairGenerator.getInstance(ALGORITHM_EC)
    kpg.initialize(256)
    return kpg.generateKeyPair()
  }

  /**
   * Encodes a public key to Base64 string for sharing over the signaling server
   */
  fun encodePublicKey(publicKey: PublicKey): String {
    return Base64.encodeToString(publicKey.encoded, Base64.NO_WRAP)
  }

  /**
   * Decodes a Base64 string back into a PublicKey
   */
  fun decodePublicKey(base64Str: String): PublicKey {
    val keyBytes = Base64.decode(base64Str, Base64.NO_WRAP)
    val keyFactory = KeyFactory.getInstance(ALGORITHM_EC)
    return keyFactory.generatePublic(X509EncodedKeySpec(keyBytes))
  }

  /**
   * Derives a 256-bit AES symmetric key from my Private Key and their Public Key using ECDH
   */
  fun deriveSharedKey(myPrivateKey: PrivateKey, theirPublicKey: PublicKey): SecretKeySpec {
    val keyAgreement = KeyAgreement.getInstance(ALGORITHM_ECDH)
    keyAgreement.init(myPrivateKey)
    keyAgreement.doPhase(theirPublicKey, true)
    val sharedSecret = keyAgreement.generateSecret()
    
    // Hash the shared secret with SHA-256 to derive a stable 256-bit AES key
    val digest = MessageDigest.getInstance("SHA-256")
    val aesKeyBytes = digest.digest(sharedSecret)
    return SecretKeySpec(aesKeyBytes, "AES")
  }

  /**
   * Encrypts plaintext using AES-256-GCM. Returns a base64 encoded payload: "IV_Base64:Ciphertext_Base64"
   */
  fun encrypt(plainText: String, secretKey: SecretKeySpec): String {
    val cipher = Cipher.getInstance(ALGORITHM_AES_GCM)
    val iv = ByteArray(IV_LENGTH_BYTE)
    SecureRandom().nextBytes(iv)
    val spec = GCMParameterSpec(TAG_LENGTH_BIT, iv)
    cipher.init(Cipher.ENCRYPT_MODE, secretKey, spec)
    
    val cipherTextBytes = cipher.doFinal(plainText.toByteArray(Charsets.UTF_8))
    
    val ivBase64 = Base64.encodeToString(iv, Base64.NO_WRAP)
    val cipherTextBase64 = Base64.encodeToString(cipherTextBytes, Base64.NO_WRAP)
    return "$ivBase64:$cipherTextBase64"
  }

  /**
   * Decrypts an encrypted payload formatted as "IV_Base64:Ciphertext_Base64" using AES-256-GCM
   */
  fun decrypt(encryptedPayload: String, secretKey: SecretKeySpec): String {
    val parts = encryptedPayload.split(":")
    if (parts.size != 2) {
      throw IllegalArgumentException("Invalid encrypted payload format")
    }
    
    val iv = Base64.decode(parts[0], Base64.NO_WRAP)
    val cipherTextBytes = Base64.decode(parts[1], Base64.NO_WRAP)
    
    val cipher = Cipher.getInstance(ALGORITHM_AES_GCM)
    val spec = GCMParameterSpec(TAG_LENGTH_BIT, iv)
    cipher.init(Cipher.DECRYPT_MODE, secretKey, spec)
    
    val decryptedBytes = cipher.doFinal(cipherTextBytes)
    return String(decryptedBytes, Charsets.UTF_8)
  }
}
