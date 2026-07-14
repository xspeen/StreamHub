@echo off
setlocal enabledelayedexpansion
:: StreamHub Installer - Windows (CMD)
:: Usage: curl -sSL https://raw.githubusercontent.com/xspeen/StreamHub/main/install.bat -o install.bat && install.bat

set "VERSION=3.2.7"
set "REPO=https://github.com/xspeen/StreamHub"
set "RAW=https://raw.githubusercontent.com/xspeen/StreamHub/main"
set "INSTALL_DIR=%USERPROFILE%\.streamhub"

echo.
echo   ============================================
echo          StreamHub Installer v%VERSION%
echo   ============================================
echo.
echo   Installing to %INSTALL_DIR%
echo.

:: Check Python
set "PY="
where python >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set "PYVER=%%v"
    set "PY=python"
) else (
    where python3 >nul 2>&1
    if %errorlevel% equ 0 (
        set "PY=python3"
    )
)

if "%PY%"=="" (
    echo   [ERROR] Python 3 is required but not found.
    echo   Install it from https://python.org or your package manager,
    echo   then run this installer again.
    echo.
    pause
    exit /b 1
)

:: Check curl
where curl >nul 2>&1
if %errorlevel% neq 0 (
    echo   [ERROR] curl is required but not found.
    echo   Install it from https://curl.se or enable it in Windows Features.
    echo.
    pause
    exit /b 1
)

:: Create directories
echo   [1/6] Creating directories...
mkdir "%INSTALL_DIR%" 2>nul
mkdir "%INSTALL_DIR%\bin" 2>nul
mkdir "%INSTALL_DIR%\src" 2>nul
mkdir "%INSTALL_DIR%\web" 2>nul
mkdir "%INSTALL_DIR%\data" 2>nul

:: Download files
echo   [1/6] Downloading version info...
curl -sSL --retry 3 -o "%INSTALL_DIR%\VERSION" "%RAW%/VERSION" 2>nul

echo   [2/6] Downloading core modules...
curl -sSL --retry 3 -o "%INSTALL_DIR%\bin\streamhub" "%RAW%/bin/streamhub" 2>nul
if %errorlevel% neq 0 goto :dl_error

echo   [3/6] Downloading server components...
curl -sSL --retry 3 -o "%INSTALL_DIR%\src\core.sh" "%RAW%/src/core.sh" 2>nul
curl -sSL --retry 3 -o "%INSTALL_DIR%\src\server.py" "%RAW%/src/server.py" 2>nul
curl -sSL --retry 3 -o "%INSTALL_DIR%\src\scanner.py" "%RAW%/src/scanner.py" 2>nul
curl -sSL --retry 3 -o "%INSTALL_DIR%\src\db.py" "%RAW%/src/db.py" 2>nul

echo   [4/6] Downloading web interface...
curl -sSL --retry 3 -o "%INSTALL_DIR%\web\index.html" "%RAW%/web/index.html" 2>nul
if %errorlevel% neq 0 goto :dl_error

:: Create wrapper batch file
echo   [5/6] Configuring launcher...
:: Find bash (Git Bash or WSL)
set "BASH="
if exist "C:\Program Files\Git\bin\bash.exe" (
    set "BASH=C:\Program Files\Git\bin\bash.exe"
) else if exist "C:\Program Files (x86)\Git\bin\bash.exe" (
    set "BASH=C:\Program Files (x86)\Git\bin\bash.exe"
) else if exist "%LOCALAPPDATA%\Programs\Git\bin\bash.exe" (
    set "BASH=%LOCALAPPDATA%\Programs\Git\bin\bash.exe"
) else (
    where bash >nul 2>&1
    if %errorlevel% equ 0 (
        set "BASH=bash"
    )
)

if "%BASH%"=="" (
    echo   [WARNING] Git Bash not found. Trying Python launcher...
    :: Create a Python-based launcher as fallback
    (
        echo @echo off
        echo setlocal
        echo python "%INSTALL_DIR%\src\server.py" --port 5000 --data "%INSTALL_DIR%\data" --web "%INSTALL_DIR%\web"
    ) > "%INSTALL_DIR%\streamhub.bat"
) else (
    (
        echo @echo off
        echo setlocal
        echo "%BASH%" "%INSTALL_DIR%\bin\streamhub" %%*
    ) > "%INSTALL_DIR%\streamhub.bat"
)

:: Also copy to bin directory
copy "%INSTALL_DIR%\streamhub.bat" "%INSTALL_DIR%\bin\streamhub.bat" >nul 2>&1

:: Add to user PATH
for /f "tokens=2*" %%A in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "CURPATH=%%B"
echo !CURPATH! | findstr /I /C:"%INSTALL_DIR%" >nul 2>&1
if %errorlevel% neq 0 (
    if defined CURPATH (
        reg add "HKCU\Environment" /v Path /t REG_EXPAND_SZ /d "!CURPATH!;%INSTALL_DIR%" /f >nul 2>&1
    ) else (
        reg add "HKCU\Environment" /v Path /t REG_EXPAND_SZ /d "%INSTALL_DIR%" /f >nul 2>&1
    )
    echo   [6/6] PATH updated. You may need to restart your terminal.
) else (
    echo   [6/6] PATH already configured.
)

:: Also create in a location already in PATH
copy "%INSTALL_DIR%\streamhub.bat" "%INSTALL_DIR%\bin\streamhub.bat" >nul 2>&1

echo.
echo   ============================================
echo          INSTALLATION COMPLETE
echo   ============================================
echo.
echo   _____  _                            _   _       _
echo  ^| ___ ^|^| ^|_ _ __ ___  __ _ _ __ ___ ^| ^| ^| ^|_   _^| ^|__
echo  ^| ___ ^|^| __^| '__/ _ \\/ _` ^| '_ ` _ \\\\^| ^|_^| ^| ^| ^| ^| '_ \
echo  ^| ___ ^|^| ^|_^| ^| ^|  __/ (_^| ^| ^| ^| ^| ^| ^|  _  ^| ^|_^| ^| ^|_) ^|
echo  ^|_____/ ^|\\__^|_^|  \\___|\\__,_^|_^| ^|_^| ^|_^|_^|_^|_\\__,_^|_.__/
echo.
echo   Type 'streamhub' in your terminal to launch.
echo.
pause
exit /b 0

:dl_error
echo.
echo   [ERROR] Download failed. Check your internet connection.
echo.
pause
exit /b 1
