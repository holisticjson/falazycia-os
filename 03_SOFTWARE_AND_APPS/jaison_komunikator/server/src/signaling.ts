import WebSocket from 'ws';
import * as db from './db';

// Map of active connections: userId -> WebSocket
const activeConnections = new Map<string, WebSocket>();

interface Message {
  type: string;
  senderId?: string;
  recipientId?: string;
  payload: any;
}

export function handleConnection(ws: WebSocket) {
  let registeredUserId: string | null = null;

  ws.on('message', async (data: string) => {
    try {
      const msg: Message = JSON.parse(data);

      switch (msg.type) {
        case 'register':
          const { id, username, publicKey } = msg.payload;
          if (!id || !username || !publicKey) {
            ws.send(JSON.stringify({ type: 'error', payload: { message: 'Missing registration details' } }));
            return;
          }
          
          // Save user in database
          await db.registerUser(id, username, publicKey);
          
          // Register connection
          registeredUserId = id;
          activeConnections.set(id, ws);
          console.log(`User registered: ${username} (${id})`);

          ws.send(JSON.stringify({ type: 'registered', payload: { status: 'success' } }));

          // Push pending messages
          const pending = await db.popPendingMessages(id);
          for (const pendingMsg of pending) {
            ws.send(JSON.stringify({
              type: 'chat_message',
              senderId: pendingMsg.sender_id,
              recipientId: pendingMsg.recipient_id,
              payload: JSON.parse(pendingMsg.encrypted_payload)
            }));
          }
          break;

        case 'signaling':
          // Forward WebRTC signaling (offer, answer, candidate) to the recipient
          if (!msg.recipientId || !msg.senderId) return;
          const targetWs = activeConnections.get(msg.recipientId);
          if (targetWs && targetWs.readyState === WebSocket.OPEN) {
            targetWs.send(JSON.stringify({
              type: 'signaling',
              senderId: msg.senderId,
              payload: msg.payload
            }));
          } else {
            console.log(`Signaling failed: recipient ${msg.recipientId} is offline.`);
          }
          break;

        case 'chat_message':
          // Forward E2EE encrypted chat message
          if (!msg.recipientId || !msg.senderId || !msg.payload) return;
          const recipientWs = activeConnections.get(msg.recipientId);
          if (recipientWs && recipientWs.readyState === WebSocket.OPEN) {
            recipientWs.send(JSON.stringify({
              type: 'chat_message',
              senderId: msg.senderId,
              recipientId: msg.recipientId,
              payload: msg.payload
            }));
          } else {
            // Queue message in database since recipient is offline
            console.log(`Queueing message from ${msg.senderId} to offline recipient ${msg.recipientId}`);
            await db.queueMessage(
              Math.random().toString(36).substring(2),
              msg.recipientId,
              msg.senderId,
              JSON.stringify(msg.payload)
            );
          }
          break;

        case 'get_users':
          const users = await db.listUsers();
          ws.send(JSON.stringify({
            type: 'users_list',
            payload: users
          }));
          break;

        default:
          ws.send(JSON.stringify({ type: 'error', payload: { message: `Unknown message type: ${msg.type}` } }));
      }
    } catch (err: any) {
      console.error('Error handling WebSocket message:', err);
      ws.send(JSON.stringify({ type: 'error', payload: { message: err.message } }));
    }
  });

  ws.on('close', () => {
    if (registeredUserId) {
      activeConnections.delete(registeredUserId);
      console.log(`Connection closed for user: ${registeredUserId}`);
    }
  });

  ws.on('error', (err) => {
    console.error(`WebSocket error for user ${registeredUserId}:`, err);
  });
}
