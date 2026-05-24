# Quick setup: install Temurin 17, set JAVA_HOME, install compatible PySpark.
# Run: powershell -ExecutionPolicy Bypass -File .\install_java_and_pyspark.ps1

$ProgressPreference = 'SilentlyContinue'  # suppress progress bar for faster download

$javaVersion = "17.0.19_10"
$javaFolder = "C:\Tools\temurin-17"
$javaZip = "$env:TEMP\temurin-17.zip"
$javaUrl = "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.19%2B10/OpenJDK17U-jdk_x64_windows_hotspot_17.0.19_10.zip"

Write-Host "Installing Java 17 (Temurin)..."

# Download
if (-not (Test-Path $javaFolder)) {
    Write-Host "Downloading Temurin 17 from GitHub..."
    try {
        [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
        Invoke-WebRequest -Uri $javaUrl -OutFile $javaZip -ErrorAction Stop
        Write-Host "Download complete. Extracting..."
        Expand-Archive -Path $javaZip -DestinationPath "$javaFolder" -Force
        Write-Host "Java 17 extracted to $javaFolder"
    } catch {
        Write-Host "ERROR: Failed to download/extract Java 17: $_"
        exit 1
    }
} else {
    Write-Host "Java 17 already exists at $javaFolder"
}

# Find the actual JDK folder (Temurin extracts to a subfolder)
$jdkRoot = Get-ChildItem -Path $javaFolder -Directory | Select-Object -First 1
if ($jdkRoot) {
    $javaHome = $jdkRoot.FullName
} else {
    $javaHome = $javaFolder
}

Write-Host "Setting JAVA_HOME to $javaHome"
$env:JAVA_HOME = $javaHome
[Environment]::SetEnvironmentVariable("JAVA_HOME", $javaHome, "User")

# Update PATH for current session
$env:Path = "$javaHome\bin;$env:Path"

# Verify Java
Write-Host "Verifying Java installation..."
& java -version

Write-Host "Installing PySpark compatible with Python 3.14 and Java 17..."
& python -m pip install --upgrade "pyspark>=4.1,<4.2"

Write-Host "`n=== SUCCESS ==="
Write-Host "Java 17 installed at: $javaHome"
Write-Host "JAVA_HOME set to: $env:JAVA_HOME"
Write-Host "PySpark installed in the 4.1.x line"
Write-Host "You may need to restart your PowerShell for changes to take full effect."
