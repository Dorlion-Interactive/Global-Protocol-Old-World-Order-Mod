@echo off
setlocal EnableDelayedExpansion

set "SCRIPT_DIR=%~dp0"
set "MOD_ID=globalprotocol.old_world_order"
set "APP_ID=4500270"
set "CONTENT_FOLDER=%LOCALAPPDATA%\NewWorldOrder\Mods\%MOD_ID%"
set "PREVIEW_FILE=%SCRIPT_DIR%thumbnail.png"
set "TITLE=Global Protocol: Old World Order"
set "DESCRIPTION=A historical total conversion mod for Global Protocol set in 1450 AD."
set "VDF_FILE=%TEMP%\%MOD_ID%_workshop.vdf"
set "PUBLISHEDFILEID="

echo =======================================================
echo Global Protocol: Old World Order - WORKSHOP PUBLISHER
echo =======================================================
echo.
echo This uploads the installed mod folder to Steam Workshop.
echo SteamCMD will ask for your password and Steam Guard code.
echo Your password is not stored by this script.
echo.
echo Expected staged content:
echo   %CONTENT_FOLDER%
echo.
echo Run install.bat first if you want the latest build uploaded.
echo.

if not exist "%CONTENT_FOLDER%\mod.json" (
    echo ERROR: Staged mod folder not found.
    echo        Run install.bat first to build and deploy the mod locally.
    echo.
    pause
    exit /b 1
)

if not exist "%PREVIEW_FILE%" (
    echo ERROR: Preview image not found: %PREVIEW_FILE%
    echo.
    pause
    exit /b 1
)

where steamcmd >nul 2>&1
if errorlevel 1 (
    echo ERROR: steamcmd.exe not found on PATH.
    echo        Install SteamCMD or add it to PATH, then re-run this script.
    echo.
    pause
    exit /b 1
)

for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "$json = Get-Content '%SCRIPT_DIR%mod.json' -Raw | ConvertFrom-Json; if ($json.workshopItemId) { $json.workshopItemId }"`) do (
    set "PUBLISHEDFILEID=%%A"
)
set "PUBLISHEDFILEID=!PUBLISHEDFILEID: =!"

echo AppID:            %APP_ID%
if defined PUBLISHEDFILEID (
    echo Workshop item id: !PUBLISHEDFILEID!
) else (
    echo Workshop item id: none saved yet ^(first upload will create a new item^)
)
echo.

set /p "USERNAME=Enter your Steam username: "
if "%USERNAME%"=="" (
    echo.
    echo Cancelled: Steam username is required.
    echo.
    pause
    exit /b 1
)

set /p "VISIBILITY=Visibility [0=public, 1=friends-only, 2=hidden] [2]: "
if "%VISIBILITY%"=="" set "VISIBILITY=2"
set /p "CHANGENOTE=Change note (optional): "

echo.
echo Generating Workshop upload config...
(
    echo "workshopitem"
    echo {
    echo     "appid" "%APP_ID%"
    if defined PUBLISHEDFILEID echo     "publishedfileid" "%PUBLISHEDFILEID%"
    echo     "contentfolder" "%CONTENT_FOLDER%"
    echo     "previewfile" "%PREVIEW_FILE%"
    echo     "visibility" "%VISIBILITY%"
    echo     "title" "%TITLE%"
    echo     "description" "%DESCRIPTION%"
    if defined CHANGENOTE echo     "changenote" "%CHANGENOTE%"
    echo }
) > "%VDF_FILE%"

echo.
echo Starting SteamCMD...
steamcmd +login %USERNAME% +workshop_build_item "%VDF_FILE%" +quit
set "STEAMCMD_EXIT=%ERRORLEVEL%"

echo.
if not "%STEAMCMD_EXIT%"=="0" (
    echo Workshop upload failed with exit code %STEAMCMD_EXIT%.
    echo Check the SteamCMD output above for details.
) else (
    echo Workshop upload completed.
    if defined PUBLISHEDFILEID (
        echo Item id: !PUBLISHEDFILEID!
    ) else (
        echo A new Workshop item was created. Save the returned item id into mod.json as workshopItemId.
    )
)
echo.
pause
endlocal
