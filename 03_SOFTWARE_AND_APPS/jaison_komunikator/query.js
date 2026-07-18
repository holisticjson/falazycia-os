const sqlite3 = require('/app/node_modules/sqlite3'); const db = new sqlite3.Database('/hermes.db'); db.all('SELECT id, username FROM users', function(err, rows) { console.log(rows); });
