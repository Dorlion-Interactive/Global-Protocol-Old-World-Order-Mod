@echo off
setlocal EnableDelayedExpansion

set MOD_ID=globalprotocol.old_world_order
set TARGET=%LOCALAPPDATA%\NewWorldOrder\Mods\%MOD_ID%
set SCRIPT_DIR=%~dp0
set BUILD_VARIANT=as
set SKIP_BUILD=0

:: -- Parse flags ---------------------------------------------------------------
:parse_args
if "%~1"=="" goto done_args
if /I "%~1"=="/dotnet"     set BUILD_VARIANT=dotnet & shift & goto parse_args
if /I "%~1"=="/as"         set BUILD_VARIANT=as    & shift & goto parse_args
if /I "%~1"=="/skip-build" set SKIP_BUILD=1        & shift & goto parse_args
echo WARNING: Unknown flag "%~1" ignored.
shift & goto parse_args
:done_args

echo ============================================================
echo  Global Protocol: Old World Order  ^|  Build + Installer
echo ============================================================
echo.
echo  Variant  : %BUILD_VARIANT%  (use /dotnet or /as to switch)
echo  Target   : %TARGET%
echo  Skip bld : %SKIP_BUILD%
echo.

:: =============================================================
::  PHASE 1 - BUILD
:: =============================================================

if "%SKIP_BUILD%"=="1" (
    echo [BUILD] Skipping build -- /skip-build flag set.
    goto install
)

if "%BUILD_VARIANT%"=="as" goto build_as
if "%BUILD_VARIANT%"=="dotnet" goto build_dotnet

:build_as
echo [BUILD] Variant: AssemblyScript (core WASM)
echo.

:: Check Node.js
where node >nul 2>&1
if errorlevel 1 (
    echo ERROR: node.exe not found on PATH.
    echo.
    echo   Install Node.js from https://nodejs.org  ^(LTS version recommended^)
    echo   Then re-run this installer.
    echo.
    if exist "%SCRIPT_DIR%Content\mod.wasm" (
        echo   Found a pre-built Content\mod.wasm -- continuing with that.
        goto install
    )
    pause & exit /b 1
)
for /f "tokens=*" %%v in ('node --version 2^>nul') do set NODE_VER=%%v
echo   node %NODE_VER% found.

:: Install node_modules if missing
if not exist "%SCRIPT_DIR%Content\wasm-as\node_modules\" (
    echo   node_modules not found -- running npm install...
    pushd "%SCRIPT_DIR%Content\wasm-as"
    call npm install --prefer-offline
    if errorlevel 1 (
        echo ERROR: npm install failed.
        popd & pause & exit /b 1
    )
    popd
    echo   npm install complete.
) else (
    echo   node_modules present, skipping npm install.
)

:: Build
echo   Building mod.ts -^> Content\mod.wasm ...
pushd "%SCRIPT_DIR%Content\wasm-as"
call npx asc mod.ts --target release -o ..\mod.wasm --runtime stub --use abort= --exportRuntime
if errorlevel 1 (
    echo ERROR: AssemblyScript build failed.
    popd & pause & exit /b 1
)
popd
goto verify_wasm

:build_dotnet
echo [BUILD] Variant: .NET WASI (component-model WASM)
echo.

:: Check dotnet
where dotnet >nul 2>&1
if errorlevel 1 (
    echo ERROR: dotnet.exe not found on PATH.
    echo.
    echo   Install .NET 10 SDK from https://dotnet.microsoft.com/download
    echo   Then re-run this installer.
    echo.
    if exist "%SCRIPT_DIR%Content\mod.wasm" (
        echo   Found a pre-built Content\mod.wasm -- continuing with that.
        goto install
    )
    pause & exit /b 1
)
for /f "tokens=*" %%v in ('dotnet --version 2^>nul') do set DOTNET_VER=%%v
echo   dotnet %DOTNET_VER% found.

:: Check wasi-experimental workload
dotnet workload list 2>nul | find /I "wasi-experimental" >nul
if errorlevel 1 (
    echo.
    echo   WARNING: wasi-experimental workload is not installed.
    echo   This is required to compile .NET to WASM.
    echo.
    set /P INSTALL_WASI=  Install it now? (dotnet workload install wasi-experimental) [Y/N]: 
    if /I "!INSTALL_WASI!"=="Y" (
        echo   Installing wasi-experimental workload...
        dotnet workload install wasi-experimental
        if errorlevel 1 (
            echo ERROR: Workload install failed.
            pause & exit /b 1
        )
        echo   Workload installed.
    ) else (
        if exist "%SCRIPT_DIR%Content\mod.wasm" (
            echo   Found a pre-built Content\mod.wasm -- continuing with that.
            goto install
        )
        echo   No pre-built mod.wasm found. Cannot continue.
        pause & exit /b 1
    )
)

:: Build -- CopyWasmToContent target in .csproj auto-copies dotnet.wasm -> Content/mod.wasm
echo   Publishing .NET WASI project...
dotnet publish "%SCRIPT_DIR%Content\wasm-dotnet\OldWorldOrder.csproj" -c Release
if errorlevel 1 (
    echo ERROR: dotnet publish failed.
    pause & exit /b 1
)
goto verify_wasm

:verify_wasm
echo.
if not exist "%SCRIPT_DIR%Content\mod.wasm" (
    echo ERROR: Build completed but Content\mod.wasm was not produced.
    echo        Check the build output above for details.
    pause & exit /b 1
)

:: Report file size
for %%F in ("%SCRIPT_DIR%Content\mod.wasm") do set WASM_SIZE=%%~zF
set /a WASM_KB=%WASM_SIZE% / 1024
echo [BUILD] Content\mod.wasm produced: %WASM_KB% KB (%WASM_SIZE% bytes)

:: Detect binary kind by peeking at bytes 4-7 via certutil hex dump
certutil -encodehex -f "%SCRIPT_DIR%Content\mod.wasm" "%TEMP%\owo_wasm_peek.hex" 4 >nul 2>&1
if exist "%TEMP%\owo_wasm_peek.hex" (
    set /p HEXLINE=<"%TEMP%\owo_wasm_peek.hex"
    del "%TEMP%\owo_wasm_peek.hex" >nul 2>&1
    echo !HEXLINE! | findstr /I "0a000100" >nul 2>&1
    if not errorlevel 1 (
        echo [BUILD] Binary kind  : component-model  (mod.json enableComponentRuntime=true set)
    ) else (
        echo [BUILD] Binary kind  : core WASM  (standard wasm3 runtime, no extra engine flags needed)
    )
)
echo.

:: =============================================================
::  PHASE 1b - VALIDATE SCENARIO FRAGMENTS
:: =============================================================
:validate
echo [VALIDATE] Checking scenario\*.json shape before deploy...
powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%dev\validate_scenario.ps1" -ScenarioDir "%SCRIPT_DIR%scenario"
if errorlevel 1 (
    echo.
    echo ERROR: Scenario validation failed. Aborting install to prevent broken deploy.
    echo        Fix the issues above, then re-run install.bat.
    pause
    exit /b 1
)
echo.

:: =============================================================
::  PHASE 2 - INSTALL
:: =============================================================
:install
echo [INSTALL] Deploying to mod folder...

if not exist "%TARGET%" (
    echo   Creating mod folder...
    mkdir "%TARGET%"
)

echo   Copying root mod files...
copy /Y "%SCRIPT_DIR%mod.json"      "%TARGET%\mod.json"      >nul
copy /Y "%SCRIPT_DIR%logo.png"      "%TARGET%\logo.png"      >nul
copy /Y "%SCRIPT_DIR%thumbnail.png" "%TARGET%\thumbnail.png" >nul

echo   Copying scenario\...
robocopy "%SCRIPT_DIR%scenario"   "%TARGET%\scenario"   /E /NFL /NDL /NJH /NJS /R:1 /W:1
if %ERRORLEVEL% GTR 7 ( echo ERROR: robocopy failed on scenario\ & pause & exit /b 1 )

echo   Copying overrides\...
robocopy "%SCRIPT_DIR%overrides"  "%TARGET%\overrides"  /E /NFL /NDL /NJH /NJS /R:1 /W:1
if %ERRORLEVEL% GTR 7 ( echo ERROR: robocopy failed on overrides\ & pause & exit /b 1 )

echo   Copying flags\...
robocopy "%SCRIPT_DIR%flags"      "%TARGET%\flags"      /E /NFL /NDL /NJH /NJS /R:1 /W:1
if %ERRORLEVEL% GTR 7 ( echo ERROR: robocopy failed on flags\ & pause & exit /b 1 )

echo   Copying Content\ (runtime assets only, no source files)...
robocopy "%SCRIPT_DIR%Content" "%TARGET%\Content" /E /NFL /NDL /NJH /NJS /R:1 /W:1 /XD wasm-as wasm-dotnet mod-csharp /XF *.ts *.cs *.csproj *.c *.h *.a *.rsp
if %ERRORLEVEL% GTR 7 ( echo ERROR: robocopy failed on Content\ & pause & exit /b 1 )

:: =============================================================
::  PHASE 3 - SUMMARY
:: =============================================================
echo.
echo ============================================================
echo  DONE
echo ============================================================
if exist "%TARGET%\Content\mod.wasm" (
    for %%F in ("%TARGET%\Content\mod.wasm") do set INST_SIZE=%%~zF
    set /a INST_KB=!INST_SIZE! / 1024
    echo  mod.wasm  !INST_KB! KB  installed  [variant: %BUILD_VARIANT%]
) else (
    echo  No mod.wasm  -- scenario and UI assets installed only.
    echo  Run install.bat again without /skip-build to compile WASM.
)
echo  Installed to: %TARGET%
echo ============================================================
echo.
echo  Next steps:
echo   1. Start Global Protocol
echo   2. Open Mods screen ^> enable "Old World Order"
echo   3. Start the 1450 scenario
echo   4. The crown toolbar button should appear in the HUD
echo   5. On dev builds: check Unity console for
echo        OWO: welcome popup shown on first tick
echo.
pause
endlocal
