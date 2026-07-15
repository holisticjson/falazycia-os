# Automated Build & Deploy Script for Jason Messenger
# This script builds the signed Android APK, timestamps it, updates the landing page links/instructions,
# and deploys both the APK and landing page to the VPS server.

$ErrorActionPreference = "Stop"

# 1. Define Variables and Config
$javaHome = "C:\Program Files\Android\Android Studio\jbr"
$vpsHost = "HermesGCP"
$vpsWebDir = "/home/tomas_yq1b9su/hermes-server/web"

# Add Java to path for this session
$env:JAVA_HOME = $javaHome
$env:PATH = "$javaHome\bin;" + $env:PATH

# 2. Extract Version Info from build.gradle
Write-Host "--- Extracting Version Info ---" -ForegroundColor Cyan
if (!(Test-Path "client/app/build.gradle")) {
    throw "Could not find client/app/build.gradle!"
}
$buildGradle = Get-Content "client/app/build.gradle" -Raw
$versionCode = [regex]::Match($buildGradle, 'versionCode\s+(\d+)').Groups[1].Value
$versionName = [regex]::Match($buildGradle, 'versionName\s+"([^"]+)"').Groups[1].Value

if (!$versionCode -or !$versionName) {
    throw "Failed to parse versionCode or versionName from build.gradle!"
}

$timestamp = Get-Date -Format "yyyyMMdd-HHmm"
$apkName = "Jason-App-Release-v$versionName-$timestamp.apk"
Write-Host "Parsed Version: v$versionName (Build $versionCode)" -ForegroundColor Green
Write-Host "Target APK Name: $apkName" -ForegroundColor Green

# 3. Build Signed Release APK
Write-Host "`n--- Building Signed Release APK ---" -ForegroundColor Cyan
Push-Location client
try {
    .\gradlew.bat assembleRelease
} finally {
    Pop-Location
}

$localApkSource = "client/app/build/outputs/apk/release/app-release.apk"
if (!(Test-Path $localApkSource)) {
    throw "Gradle build succeeded but could not find output APK at $localApkSource!"
}

# 4. Copy to Local Web folder
Write-Host "`n--- Copying APK to local web directory ---" -ForegroundColor Cyan
$localWebDir = "web"
$localApkDest = Join-Path $localWebDir $apkName

# Remove old dynamic APKs from local web folder to prevent clutter
Get-ChildItem -Path $localWebDir -Filter "Jason-App-Release-*.apk" | Remove-Item -Force -ErrorAction SilentlyContinue

# Copy newly built APK
Copy-Item -Path $localApkSource -Destination $localApkDest -Force
Write-Host "Copied APK to $localApkDest" -ForegroundColor Green

# 5. Update web/index.html and web/dziekuje-za-zapis.html with the new APK name
Write-Host "`n--- Updating HTML files with new APK name ---" -ForegroundColor Cyan
$filesToUpdate = @("index.html", "dziekuje-za-zapis.html")

foreach ($file in $filesToUpdate) {
    $filePath = Join-Path $localWebDir $file
    if (Test-Path $filePath) {
        $htmlContent = Get-Content -Path $filePath -Raw
        
        # Replace download link: <a href="..." class="download-btn" download>
        $patternLink = 'href="(app-release\.apk|Jason-App-Release-[^"]+\.apk)"'
        $htmlContent = [regex]::Replace($htmlContent, $patternLink, "href=`"$apkName`"")
        
        # Replace code instruction: <code>app-release.apk</code> or <code>Jason-App-Release-*.apk</code>
        $patternCode = '<code>(app-release\.apk|Jason-App-Release-[^<]+\.apk)</code>'
        $htmlContent = [regex]::Replace($htmlContent, $patternCode, "<code>$apkName</code>")
        
        Set-Content -Path $filePath -Value $htmlContent -NoNewline
        Write-Host "Updated $file download references to $apkName" -ForegroundColor Green
    }
}

# 6. Deploy to VPS
Write-Host "`n--- Deploying to VPS ($vpsHost) ---" -ForegroundColor Cyan

# A. Upload index.html, APK, and all web asset files to remote /tmp/ using scp
Write-Host "Uploading all web files and brand logo assets to /tmp on server..." -ForegroundColor Yellow

Get-ChildItem -Path $localWebDir -File | Where-Object { $_.Name -notmatch "app-release.apk" -and ($_.Name -eq $apkName -or $_.Name -notlike "Jason-App-Release-*.apk") } | ForEach-Object {
    Write-Host "Uploading: $($_.Name)" -ForegroundColor DarkGray
    scp $_.FullName "${vpsHost}:/tmp/$($_.Name)"
}

# B. Move files to production directory and fix ownership using sudo ssh
Write-Host "Moving files to production web directory and setting permissions..." -ForegroundColor Yellow

# Remove old dynamic APKs on server to keep disk clean
ssh $vpsHost "sudo rm -f $vpsWebDir/Jason-App-Release-*.apk"

# Move all uploaded files from /tmp to the production directory, then fix ownership
ssh $vpsHost "sudo find /tmp -maxdepth 1 -type f \( -name '*.html' -o -name '*.png' -o -name '*.jpg' -o -name '*.jpeg' -o -name '*.gif' -o -name '*.mp4' -o -name '*.pdf' -o -name '*.apk' -o -name '*.css' -o -name '*.js' \) -exec mv {} $vpsWebDir/ \; 2>/dev/null || true"
ssh $vpsHost "sudo chown -R tomas_yq1b9su:tomas_yq1b9su $vpsWebDir"



Write-Host "`n🚀 DEPLOYMENT COMPLETED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "Web Landing Page and Signed APK have been published." -ForegroundColor Green
Write-Host "Live Download Link: https://app.jaison.pl/$apkName" -ForegroundColor Yellow
