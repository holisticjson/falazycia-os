# Skrypt wdrożeniowy (Deployment Script) - Hermes OS
# Autor: Antigravity
# Cel: Automatyczne wypychanie konfiguracji i UI na maszynę Google Cloud

$ZONE = "us-central1-a"
$INSTANCE = "hermes-os"
$USER = "holisticjson"

Write-Host "[1/3] Przesyłanie nowej konfiguracji omijającej limity (hermes_server_config.yaml)..." -ForegroundColor Cyan
gcloud compute scp "..\..\..\.gemini\antigravity\brain\5318ebb3-6fa9-4b29-ac85-2a6b3a2dd4b2\hermes_server_config.yaml" ${USER}@${INSTANCE}:/home/${USER}/config.yaml --zone $ZONE --quiet

Write-Host "[2/3] Przesyłanie nowego interfejsu (folder ui/)..." -ForegroundColor Cyan
gcloud compute scp --recurse ".\ui" ${USER}@${INSTANCE}:/home/${USER}/ui_new --zone $ZONE --quiet

Write-Host "[3/3] Aplikowanie zmian i restart rdzenia Hermes na serwerze GCP..." -ForegroundColor Cyan
$REMOTE_COMMAND = @"
sudo cp /home/$USER/config.yaml /home/$USER/.hermes/config.yaml
sudo rm -rf /home/$USER/.hermes/ui
sudo mv /home/$USER/ui_new /home/$USER/.hermes/ui
sudo systemctl restart hermes-agent || (cd /home/$USER/hermes-agent && pkill -f hermes_cli.main)
echo 'Wdrożenie pomyślne! Hermes Agent zrestartowany.'
"@

gcloud compute ssh ${USER}@${INSTANCE} --zone $ZONE --quiet --command $REMOTE_COMMAND

Write-Host "DEPLOJ ZAKOŃCZONY SUKCESEM 🚀" -ForegroundColor Green
