import http from 'http';
import { WebSocketServer } from 'ws';
import dotenv from 'dotenv';
import fs from 'fs';
import path from 'path';
import { initDb, saveLead, enqueueEmail, getPendingEmails, markEmailSent, markEmailFailed } from './db';
import { handleConnection } from './signaling';
import { proxyChatStream } from './ai';
import nodemailer from 'nodemailer';

// Load environment variables
dotenv.config();

const PORT = parseInt(process.env.PORT || '8080', 10);

function startCleanupTask() {
  const uploadsDir = path.resolve(__dirname, '../web/uploads');
  const cleanup = () => {
    if (!fs.existsSync(uploadsDir)) return;
    
    fs.readdir(uploadsDir, (err, files) => {
      if (err) {
        console.error('Failed to read uploads directory for cleanup:', err);
        return;
      }
      
      const now = Date.now();
      const expirationMs = 30 * 24 * 60 * 60 * 1000; // 30 days
      
      for (const file of files) {
        const filePath = path.join(uploadsDir, file);
        fs.stat(filePath, (statErr, stats) => {
          if (statErr) return;
          if (stats.isFile() && (now - stats.mtimeMs > expirationMs)) {
            fs.unlink(filePath, (unlinkErr) => {
              if (unlinkErr) {
                console.error(`Failed to delete expired file: ${file}`, unlinkErr);
              } else {
                console.log(`Deleted expired attachment file: ${file}`);
              }
            });
          }
        });
      }
    });
  };

  // Run cleanup on startup and then every 24 hours
  cleanup();
  setInterval(cleanup, 24 * 60 * 60 * 1000);
}

function startMailQueueProcessor() {
  const processQueue = async () => {
    let pending;
    try {
      pending = await getPendingEmails();
    } catch (err) {
      console.error('Failed to query mail queue from DB:', err);
      return;
    }

    if (pending.length === 0) return;

    console.log(`Found ${pending.length} pending emails in the queue. Processing...`);

    const smtpHost = process.env.SMTP_HOST;
    const smtpPort = parseInt(process.env.SMTP_PORT || '587', 10);
    const smtpSecure = process.env.SMTP_SECURE === 'true';
    const smtpUser = process.env.SMTP_USER;
    const smtpPass = process.env.SMTP_PASS;
    const smtpFromEmail = process.env.SMTP_FROM_EMAIL || 'info@jaison.pl';
    const smtpFromName = process.env.SMTP_FROM_NAME || 'Tomasz | J(a)son Messenger';

    if (!smtpHost || !smtpUser || !smtpPass) {
      for (const mail of pending) {
        console.warn(`SMTP is not configured. Unable to send email to ${mail.to_email}. Incrementing attempt count.`);
        try {
          await markEmailFailed(mail.id, 'SMTP environment variables are not configured in .env (SMTP_HOST, SMTP_USER, SMTP_PASS).', mail.attempts + 1);
        } catch (dbErr) {
          console.error('Failed to update email status in DB:', dbErr);
        }
      }
      return;
    }

    const transporter = nodemailer.createTransport({
      host: smtpHost,
      port: smtpPort,
      secure: smtpSecure,
      auth: {
        user: smtpUser,
        pass: smtpPass
      }
    });

    for (const mail of pending) {
      try {
        console.log(`Sending email to ${mail.to_email} (Attempt ${mail.attempts + 1})...`);
        await transporter.sendMail({
          from: `"${smtpFromName}" <${smtpFromEmail}>`,
          to: `"${mail.to_name}" <${mail.to_email}>`,
          subject: mail.subject,
          html: mail.body_html
        });

        await markEmailSent(mail.id);
        console.log(`Email to ${mail.to_email} sent successfully and marked as sent.`);
      } catch (err: any) {
        console.error(`Failed to send email to ${mail.to_email}:`, err);
        const errMsg = err.message || String(err);
        await markEmailFailed(mail.id, errMsg, mail.attempts + 1);
      }
    }
  };

  // Run queue processor immediately and every 30 seconds
  processQueue();
  setInterval(processQueue, 30000);
}

async function startServer() {
  // Start 30-day cleanup task
  startCleanupTask();

  // Initialize database
  await initDb();

  // Start background SMTP queue processor
  startMailQueueProcessor();

  // Create HTTP Server
  const server = http.createServer(async (req, res) => {
    // Enable CORS for API requests
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

    if (req.method === 'OPTIONS') {
      res.writeHead(204);
      res.end();
      return;
    }

    const url = new URL(req.url || '', `http://${req.headers.host}`);

    // Redirect legacy PDF ebook requests to the beautiful interactive HTML ebook
    if (url.pathname.includes('ebook_prywatna_twierdza.pdf')) {
      res.writeHead(302, { 'Location': '/ebook_prywatna_twierdza.html' });
      res.end();
      return;
    }

    // Serve static files from the 'web' folder if they exist
    const webDir = path.resolve(__dirname, '../web');
    const requestedPath = url.pathname === '/' ? '/index.html' : url.pathname;
    const filePath = path.join(webDir, requestedPath);

    // Guard against directory traversal attacks
    if (filePath.startsWith(webDir) && fs.existsSync(filePath) && !fs.statSync(filePath).isDirectory()) {
      const ext = path.extname(filePath).toLowerCase();
      let contentType = 'application/octet-stream';
      if (ext === '.html') contentType = 'text/html';
      else if (ext === '.css') contentType = 'text/css';
      else if (ext === '.js') contentType = 'text/javascript';
      else if (ext === '.png') contentType = 'image/png';
      else if (ext === '.jpg' || ext === '.jpeg') contentType = 'image/jpeg';
      else if (ext === '.apk') contentType = 'application/vnd.android.package-archive';
      else if (ext === '.pdf') contentType = 'application/pdf';
      else if (ext === '.mp4') contentType = 'video/mp4';
      else if (ext === '.docx') contentType = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document';
      
      res.writeHead(200, { 'Content-Type': contentType });
      fs.createReadStream(filePath).pipe(res);
      return;
    }

    // Health check route
    if (url.pathname === '/health' && req.method === 'GET') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ status: 'ok', name: 'J(a)son Messenger Server' }));
      return;
    }

    // Lead capturing route (Saves leads and enqueues HTML welcome mail)
    if (url.pathname === '/api/lead' && req.method === 'POST') {
      let body = '';
      req.on('data', chunk => {
        body += chunk.toString();
      });

      req.on('end', async () => {
        try {
          const parsed = JSON.parse(body);
          // Handle both 'name' and 'first_name', and 'contact' and 'email' for seamless front-end support
          const firstName = parsed.name || parsed.first_name;
          const email = parsed.contact || parsed.email;
          const rodoConsent = parsed.rodo_consent !== undefined ? (parsed.rodo_consent ? 1 : 0) : 1; // Default to 1 if from main signup form
          const messenger = parsed.messenger;
          const phoneModel = parsed.phone_model || parsed.phoneModel;
          const additionalInfo = parsed.additional_info || parsed.additionalInfo || parsed.message;

          if (!firstName || !email) {
            res.writeHead(400, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Imię i adres e-mail są wymagane.' }));
            return;
          }

          // 1. Save lead to DB
          await saveLead(firstName, email, rodoConsent, messenger, phoneModel, additionalInfo);
          console.log(`Zapisano nowego leada: ${firstName} (${email})`);

          // 2. Draft welcome email with beautiful obsidian and glowing cyan layout
          const subject = '📚 Twój darmowy Poradnik: Bezpieczny Telefon (Prywatna Twierdza)';
          const bodyHtml = `
            <div style="font-family: 'Segoe UI', Arial, sans-serif; background-color: #080b11; color: #f1f3f5; padding: 40px 20px; min-height: 100vh;">
              <div style="max-width: 600px; margin: 0 auto; background-color: rgba(13, 20, 30, 0.95); border: 1px solid rgba(0, 240, 255, 0.25); border-radius: 20px; padding: 40px; box-shadow: 0 10px 30px rgba(0, 240, 255, 0.15);">
                
                <div style="text-align: center; margin-bottom: 30px;">
                  <h1 style="color: #ffffff; font-size: 28px; margin-bottom: 5px; font-weight: 700; letter-spacing: -0.5px;">J(a)son</h1>
                  <p style="color: #00f0ff; font-size: 14px; text-transform: uppercase; letter-spacing: 2px; margin-top: 0; font-weight: 600;">Prywatność i Kontrola AI</p>
                </div>

                <h2 style="color: #ffffff; font-size: 22px; margin-bottom: 20px; border-bottom: 1px solid rgba(0, 240, 255, 0.1); padding-bottom: 10px;">Cześć ${firstName}!</h2>
                
                <p style="font-size: 16px; line-height: 1.6; margin-bottom: 24px; color: #f1f3f5;">
                  Cieszę się, że dołączasz do społeczności osób dbających o swoją prywatność i skupienie uwagi. Zgodnie z obietnicą, przesyłam Ci darmowy przewodnik, który krok po kroku pomoże Ci przekształcić telefon w bezpieczną twierdzę.
                </p>

                <div style="background-color: rgba(255, 255, 255, 0.02); border-left: 4px solid #00f0ff; padding: 20px; border-radius: 8px; margin: 30px 0;">
                  <h4 style="color: #ffffff; margin-top: 0; margin-bottom: 8px; font-size: 16px;">🎁 Twój pakiet powitalny:</h4>
                  <ul style="margin: 0; padding-left: 20px; font-size: 14.5px; line-height: 1.6; color: #90a4ae;">
                    <li style="margin-bottom: 10px;">
                      <strong style="color: #ffffff;">Darmowy E-book:</strong> "Prywatna Twierdza: Jak zabezpieczyć i odciążyć Androida w 15 minut" (PDF w załączniku / do pobrania bezpośrednio na stronie).
                    </li>
                    <li style="margin-bottom: 10px;">
                      <strong style="color: #ffffff;">Komunikator J(a)son (APK):</strong> Bezpieczna, w pełni szyfrowana aplikacja ze wsparciem lokalnej bazy SQLCipher i prywatnym asystentem AI.
                    </li>
                  </ul>
                </div>

                <div style="text-align: center; margin: 35px 0;">
                  <a href="https://app.jaison.pl/ebook_prywatna_twierdza.html" style="display: inline-block; padding: 16px 36px; background-color: #00f0ff; color: #001f24; font-size: 16px; font-weight: 700; text-decoration: none; border-radius: 12px; box-shadow: 0 4px 15px rgba(0, 240, 255, 0.3);">
                    Czytaj E-book Online & Pobierz APK
                  </a>
                </div>

                <p style="font-size: 15px; line-height: 1.6; margin-bottom: 24px; color: #f1f3f5;">
                  P.S. Jeśli chcesz porozmawiać na żywo o audycie odciążania (debloatingu) Twojego telefonu lub masz problem z instalacją, napisz bezpośrednio do mnie na e-mail: <a href="mailto:hello@jaison.pl" style="color: #00f0ff; text-decoration: underline;">hello@jaison.pl</a>.
                </p>

                <hr style="border: none; border-top: 1px solid rgba(255, 255, 255, 0.05); margin: 30px 0;">

                <div style="font-size: 12px; color: #90a4ae; text-align: center; line-height: 1.5;">
                  Wiadomość została wysłana automatycznie przez platformę J(a)son.<br>
                  Tomasz Duda (Jaison) • © 2026<br>
                  Możesz wypisać się z newslettera w każdej chwili, pisząc krótki e-mail na adres hello@jaison.pl.
                </div>

              </div>
            </div>
          `;

          await enqueueEmail(email, firstName, subject, bodyHtml);
          console.log(`Zakolejkowano mail powitalny dla: ${email}`);

          // 3. Forward to n8n Webhook if configured
          const n8nWebhookUrl = process.env.N8N_WEBHOOK_URL;
          if (n8nWebhookUrl) {
            try {
              const webhookPayload = {
                firstName,
                email,
                rodoConsent,
                messenger: messenger || null,
                phoneModel: phoneModel || null,
                additionalInfo: additionalInfo || null,
                source: parsed.source || 'J(AI)Son Landing Page',
                timestamp: new Date().toISOString()
              };

              fetch(n8nWebhookUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(webhookPayload)
              }).then(res => {
                console.log(`Przekazano lead do n8n webhook (Status: ${res.status})`);
              }).catch(err => {
                console.error('Błąd asynchronicznego wysyłania do n8n webhook:', err);
              });
            } catch (webhookErr) {
              console.error('Błąd podczas próby wysłania do n8n:', webhookErr);
            }
          }

          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ status: 'ok', message: 'Lead saved and welcome email enqueued.' }));
        } catch (err: any) {
          console.error('Błąd przy zapisywaniu leada:', err);
          res.writeHead(500, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: 'Wystąpił błąd serwera. Spróbuj ponownie później.' }));
        }
      });
      return;
    }

    // File upload route
    if (url.pathname === '/api/attachments/upload' && req.method === 'POST') {
      const fileNameHeader = req.headers['x-file-name'];
      if (!fileNameHeader || typeof fileNameHeader !== 'string') {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Missing x-file-name header.' }));
        return;
      }

      // Sanitize file name to prevent directory traversal
      const fileName = path.basename(fileNameHeader);
      const uploadsDir = path.resolve(__dirname, '../web/uploads');
      if (!fs.existsSync(uploadsDir)) {
        fs.mkdirSync(uploadsDir, { recursive: true });
      }

      const uploadPath = path.join(uploadsDir, fileName);
      const fileStream = fs.createWriteStream(uploadPath);

      req.pipe(fileStream);

      req.on('end', () => {
        const fileUrl = `/uploads/${fileName}`;
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ url: fileUrl }));
      });

      req.on('error', (err) => {
        console.error('Upload stream error:', err);
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Upload failed' }));
      });
      return;
    }

    // NVIDIA LLM proxy route
    if (url.pathname === '/api/chat' && req.method === 'POST') {
      let body = '';
      req.on('data', chunk => {
        body += chunk.toString();
      });

      req.on('end', async () => {
        try {
          const { messages, model } = JSON.parse(body);
          if (!messages || !Array.isArray(messages)) {
            res.writeHead(400, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Invalid payload: messages must be an array.' }));
            return;
          }
          await proxyChatStream(messages, model, res);
        } catch (err: any) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: 'Malformed JSON body.' }));
        }
      });
      return;
    }

    // Default 404 route
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Not found' }));
  });

  // Create WebSocket Server
  const wss = new WebSocketServer({ server });

  wss.on('connection', (ws) => {
    console.log('New WebSocket connection established.');
    handleConnection(ws);
  });

  server.listen(PORT, '0.0.0.0', () => {
    console.log(`J(a)son Messenger Server is listening on port ${PORT}`);
  });
}

startServer().catch(err => {
  console.error('Failed to start server:', err);
  process.exit(1);
});
