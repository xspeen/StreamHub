# StreamHub Installer - PowerShell (Windows 11 / PowerShell 5.1+)
# Usage: irm https://raw.githubusercontent.com/xspeen/StreamHub/main/install.ps1 | iex

$ErrorActionPreference = "Stop"
$Version = "2.0.2"
$Raw = "https://raw.githubusercontent.com/xspeen/StreamHub/main"
$InstallDir = Join-Path $env:USERPROFILE ".streamhub"

# Colors
function Write-Color($Text, $Color = "White") {
    Write-Host $Text -ForegroundColor $Color
}

Write-Host ""
Write-Host "  ============================================" -ForegroundColor Cyan
Write-Host "         StreamHub Installer v$Version" -ForegroundColor Cyan
Write-Host "  ============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Installing to $InstallDir" -ForegroundColor Gray
Write-Host ""

# Check Python
$PY = $null
foreach ($cmd in @("python", "python3")) {
    try {
        $ver = & $cmd --version 2>&1 | Select-String -Pattern '\d+\.\d+'
        if ($ver -match '(\d+)\.(\d+)') {
            $major = [int]$Matches[1]
            $minor = [int]$Matches[2]
            if ($major -ge 3 -and $minor -ge 7) {
                $PY = $cmd
                break
            }
        }
    } catch { }
}

if (-not $PY) {
    Write-Color "  [ERROR] Python 3.7+ is required but not found." "Red"
    Write-Color "  Install it from https://python.org or your package manager," "White"
    Write-Color "  then run this installer again." "White"
    exit 1
}

# Create directories
Write-Host "  [1/5] Creating directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $InstallDir "bin") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $InstallDir "src") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $InstallDir "web") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $InstallDir "data") | Out-Null

# Download files
$files = @(
    @{ Remote = "bin/streamhub"; Local = "bin/streamhub" },
    @{ Remote = "src/core.sh"; Local = "src/core.sh" },
    @{ Remote = "src/server.py"; Local = "src/server.py" },
    @{ Remote = "src/scanner.py"; Local = "src/scanner.py" },
    @{ Remote = "src/db.py"; Local = "src/db.py" },
    @{ Remote = "web/index.html"; Local = "web/index.html" }
)

$total = $files.Count
for ($i = 0; $i -lt $total; $i++) {
    $f = $files[$i]
    $pct = [math]::Round(($i + 1) / $total * 100)
    Write-Host "`r  [$pct%] Downloading $($f.Remote)..." -ForegroundColor Yellow -NoNewline
    
    $url = "$Raw/$($f.Remote)"
    $dest = Join-Path $InstallDir $f.Local
    
    try {
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        $wc = New-Object System.Net.WebClient
        $wc.DownloadFile($url, $dest)
    } catch {
        Write-Host ""
        Write-Color "  [ERROR] Failed to download $($f.Remote)." "Red"
        exit 1
    }
}
Write-Host ""

# Create PowerShell wrapper
Write-Host "  Configuring launcher..." -ForegroundColor Yellow
$wrapper = @"
`$streamhubPath = "$InstallDir\bin\streamhub"
if (Test-Path `$streamhubPath) {
    & bash `$streamhubPath @args
} else {
    Write-Host "StreamHub not found. Run the installer again." -ForegroundColor Red
}
"@
$wrapper | Set-Content -Path (Join-Path $InstallDir "streamhub.ps1") -Encoding UTF8

# Create batch wrapper
$batchWrapper = @"
@echo off
"%InstallDir%\bin\streamhub" %*
"@
$batchWrapper | Set-Content -Path (Join-Path $InstallDir "streamhub.bat") -Encoding ASCII

# Add to PATH
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$InstallDir*") {
    [Environment]::SetEnvironmentVariable("Path", "$userPath;$InstallDir", "User")
    $env:Path = "$env:Path;$InstallDir"
    Write-Host "  PATH updated." -ForegroundColor Green
} else {
    Write-Host "  PATH already configured." -ForegroundColor Green
}

Write-Host ""
Write-Host "  ============================================" -ForegroundColor Blue
Write-Host "         INSTALLATION COMPLETE" -ForegroundColor Blue
Write-Host "  ============================================" -ForegroundColor Blue
Write-Host ""
Write-Host "  Type 'streamhub' in your terminal to launch." -ForegroundColor White
Write-Host ""
