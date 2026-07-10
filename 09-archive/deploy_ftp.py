import os
import ftplib

FTP_HOST = "kurczakujasia.pl"
FTP_USER = "deploy@kurczakujasia.pl"
FTP_PASS = "Kosmos!!@@1234"
REMOTE_DIR = "public_html"
LOCAL_DIR = "kurczakujasia_html"

def upload_directory(ftp, local_dir, remote_dir):
    try:
        ftp.cwd(remote_dir)
    except ftplib.error_perm:
        ftp.mkd(remote_dir)
        ftp.cwd(remote_dir)

    for item in os.listdir(local_dir):
        local_path = os.path.join(local_dir, item)
        if os.path.isfile(local_path):
            print(f"Uploading {local_path} to {remote_dir}/{item}")
            with open(local_path, "rb") as f:
                ftp.storbinary(f"STOR {item}", f)
        elif os.path.isdir(local_path):
            print(f"Entering directory {item}")
            upload_directory(ftp, local_path, item)
            ftp.cwd("..") # go back up

def deploy():
    print(f"Connecting to {FTP_HOST}...")
    ftp = ftplib.FTP(FTP_HOST)
    ftp.login(user=FTP_USER, passwd=FTP_PASS)
    ftp.set_pasv(True)
    
    ftp.cwd(REMOTE_DIR)
    
    # Disable WordPress by renaming its core files
    print("Disabling WordPress files (index.php, .htaccess) if present...")
    files = ftp.nlst()
    
    if "index.php" in files:
        try:
            ftp.rename("index.php", "wp-index-backup.php")
            print("Renamed index.php -> wp-index-backup.php")
        except Exception as e:
            print(f"Could not rename index.php: {e}")
            
    if ".htaccess" in files:
        try:
            ftp.rename(".htaccess", ".htaccess-backup")
            print("Renamed .htaccess -> .htaccess-backup")
        except Exception as e:
            print(f"Could not rename .htaccess: {e}")
            
    # Go back to root before upload_directory because upload_directory uses relative paths and changes dirs
    ftp.cwd("/")
    
    print("Uploading static HTML site to Hostido...")
    upload_directory(ftp, LOCAL_DIR, REMOTE_DIR)
    
    ftp.quit()
    print("Deployment complete! The static site is now live.")

if __name__ == "__main__":
    deploy()
