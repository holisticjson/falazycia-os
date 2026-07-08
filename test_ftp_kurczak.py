import os
import ftplib

FTP_HOST = "kurczakujasia.pl"
FTP_USER = "deploy@kurczakujasia.pl"
FTP_PASS = "Kosmos!!@@1234"

try:
    print(f"Connecting to {FTP_HOST} as {FTP_USER}...")
    ftp = ftplib.FTP(FTP_HOST)
    ftp.login(user=FTP_USER, passwd=FTP_PASS)
    ftp.set_pasv(True)
    
    print("\n--- Root Directory Listing ---")
    files = []
    ftp.dir(files.append)
    for f in files:
        print(f)
        
    ftp.quit()
except Exception as e:
    print(f"Error: {e}")
