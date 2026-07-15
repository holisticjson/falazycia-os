import re

with open('/etc/nginx/sites-available/os.holisticjson.pl', 'r') as f:
    c = f.read()

c = re.sub(r'(location /api/ \{.*?proxy_set_header Host )\$host;', r'\g<1>127.0.0.1;', c, flags=re.DOTALL)
# Also fix the legacy /hermes-api/ if it exists
c = re.sub(r'(location /hermes-api/ \{.*?proxy_set_header Host )\$host;', r'\g<1>127.0.0.1;', c, flags=re.DOTALL)

with open('/etc/nginx/sites-available/os.holisticjson.pl', 'w') as f:
    f.write(c)
