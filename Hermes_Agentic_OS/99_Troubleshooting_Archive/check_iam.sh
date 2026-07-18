#!/bin/bash
echo "=== SA KEY INFO ==="
python3 -c "
import json
with open('/home/holisticjson/gcp-sa-key.json') as f:
    d = json.load(f)
print('SA project_id :', d.get('project_id', '?'))
print('SA client_email:', d.get('client_email', '?'))
print('SA type        :', d.get('type', '?'))
"

echo ""
echo "=== VM DEFAULT PROJECT (gcloud) ==="
gcloud config get-value project 2>/dev/null || echo "brak"

echo ""
echo "=== ROLE SA w projekcie holistic-broker ==="
SA_EMAIL=$(python3 -c "import json; d=json.load(open('/home/holisticjson/gcp-sa-key.json')); print(d.get('client_email',''))")
echo "SA: $SA_EMAIL"
gcloud projects get-iam-policy holistic-broker \
    --flatten="bindings[].members" \
    --filter="bindings.members:$SA_EMAIL" \
    --format="table(bindings.role)" 2>/dev/null || echo "[brak dostępu do listy ról]"

echo ""
echo "=== ROLE SA w projekcie holistic-dashboard-dev ==="
gcloud projects get-iam-policy holistic-dashboard-dev \
    --flatten="bindings[].members" \
    --filter="bindings.members:$SA_EMAIL" \
    --format="table(bindings.role)" 2>/dev/null || echo "[brak dostępu do listy ról]"
