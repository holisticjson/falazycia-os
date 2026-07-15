const http = require('http');
const sqlite3 = require('sqlite3');
const path = require('path');

const payload = JSON.stringify({
    name: 'Jan Kowalski Test',
    contact: 'jan.kowalski.test@example.com',
    rodo_consent: true
});

const options = {
    hostname: 'localhost',
    port: 8080,
    path: '/api/lead',
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Content-Length': payload.length
    }
};

const req = http.request(options, (res) => {
    let body = '';
    res.on('data', chunk => body += chunk);
    res.on('end', () => {
        console.log(`STATUS: ${res.statusCode}`);
        console.log(`BODY: ${body}`);

        // Verify SQLite database
        setTimeout(() => {
            console.log('\n--- Checking SQLite database contents ---');
            const dbPath = path.resolve(__dirname, 'hermes.db');
            console.log(`Opening database at: ${dbPath}`);
            const db = new sqlite3.Database(dbPath, (err) => {
                if (err) {
                    console.error('Failed to open DB:', err);
                    return;
                }
                
                db.all('SELECT * FROM leads', [], (err, rows) => {
                    if (err) {
                        console.error('Error querying leads:', err);
                    } else {
                        console.log('Leads in database:');
                        console.log(rows);
                    }

                    db.all('SELECT * FROM mail_queue', [], (err, mailRows) => {
                        if (err) {
                            console.error('Error querying mail_queue:', err);
                        } else {
                            console.log('\nMail Queue in database:');
                            mailRows.forEach(row => {
                                console.log({
                                    id: row.id,
                                    to_email: row.to_email,
                                    to_name: row.to_name,
                                    subject: row.subject,
                                    status: row.status,
                                    attempts: row.attempts,
                                    last_error: row.last_error ? row.last_error.substring(0, 80) + '...' : null
                                });
                            });
                        }
                        db.close();
                    });
                });
            });
        }, 1500);
    });
});

req.on('error', (e) => {
    console.error(`problem with request: ${e.message}`);
});

req.write(payload);
req.end();
