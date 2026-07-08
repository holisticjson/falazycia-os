import os
import subprocess
import sys

def run_command(cmd, cwd=None):
    print(f"Executing: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"❌ Error: {result.stderr}")
        return False
    print(result.stdout)
    return True

def deploy():
    # Set console encoding to UTF-8 on Windows to prevent UnicodeEncodeError
    if sys.platform.startswith('win'):
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
        
    print("🚀 Starting deployment of holisticjson.pl to Google Cloud Run...")
    
    # Step 1: Build the Vite project
    vite_dir = os.path.join(os.getcwd(), "04_website", "site")
    print(f"📦 Step 1: Building Vite production package in {vite_dir}...")
    if not run_command("npm run build", cwd=vite_dir):
        print("❌ Failed to build Vite project.")
        sys.exit(1)
        
    # Step 2: Check if gcloud CLI is available
    print("🔍 Step 2: Checking Google Cloud SDK (gcloud CLI)...")
    if not run_command("gcloud --version"):
        print("❌ gcloud CLI not found. Please install Google Cloud SDK first.")
        sys.exit(1)
        
    # Step 3: Trigger Cloud Build (builds image in Artifact Registry on GCP)
    print("☁️ Step 3: Triggering Cloud Build (submitting code to GCP)...")
    project_id = "holistic-broker" # Default GCP project from .env
    
    if os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("GCP_PROJECT_BROKER="):
                    project_id = line.strip().split("GCP_PROJECT_BROKER=", 1)[1].strip('"').strip("'")
                    break
    
    print(f"Targeting GCP Project: {project_id}")
    run_command(f"gcloud config set project {project_id}")
    
    # We will submit the build
    image_name = f"gcr.io/{project_id}/holisticjson-site:latest"
    build_cmd = f"gcloud builds submit --tag {image_name} ."
    if not run_command(build_cmd, cwd=vite_dir):
        print("❌ Failed to build image on Google Cloud Build.")
        sys.exit(1)
        
    # Step 4: Deploy the built image to Google Cloud Run
    print("🚀 Step 4: Deploying container to Google Cloud Run...")
    deploy_cmd = (
        f"gcloud run deploy holisticjson-website "
        f"--image {image_name} "
        f"--platform managed "
        f"--region europe-west1 "
        f"--port 80 "
        f"--allow-unauthenticated"
    )
    if not run_command(deploy_cmd, cwd=vite_dir):
        print("❌ Failed to deploy to Cloud Run.")
        sys.exit(1)
        
    print("\n🎉 Deployment completed successfully!")
    print("👉 Strona jest teraz dostępna na Cloud Run.")
    print("💡 Aby podpiąć domenę, wejdź w Google Cloud Console -> Cloud Run -> Manage Custom Domains.")

if __name__ == "__main__":
    deploy()
