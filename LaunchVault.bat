@echo off@echo off

title 7K Vault Launchertitle Secure Vault Launcher

cd /d "%~dp0"cd /d "%~dp0"



echo.echo.

echo ================================================echo ================================================

echo          Launching 7K Vault...echo          Launching Secure Vault...

echo          Your Media, Your Privacyecho ================================================

echo ================================================echo.

echo.

REM Check if Python is installed

REM Check if Python is installedpython --version >nul 2>&1

python --version >nul 2>&1if errorlevel 1 (

if errorlevel 1 (    echo ERROR: Python is not installed or not in PATH!

    echo ERROR: Python is not installed or not in PATH!    echo.

    echo.    echo Please install Python from: https://www.python.org/downloads/

    echo Please install Python from: https://www.python.org/downloads/    echo.

    echo Make sure to check "Add Python to PATH" during installation    pause

    echo.    exit /b 1

    pause)

    exit /b 1

)REM Check if dependencies are installed

python -c "import customtkinter" >nul 2>&1

REM Check if dependencies are installedif errorlevel 1 (

python -c "import customtkinter" >nul 2>&1    echo Installing dependencies...

if errorlevel 1 (    pip install -r requirements.txt

    echo Installing dependencies (first time only)...    echo.

    pip install -r requirements.txt)

    if errorlevel 1 (

        echo.REM Launch the app

        echo ERROR: Failed to install dependenciespythonw vault_app.py

        echo Please run: pip install -r requirements.txt

        echo.if errorlevel 1 (

        pause    echo.

        exit /b 1    echo ERROR: Failed to launch Secure Vault

    )    echo.

    echo.    pause

    echo Dependencies installed successfully!)

    echo.
)

REM Launch the app
echo Starting 7K Vault...
pythonw vault_app.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to launch 7K Vault
    echo.
    echo Try running: python vault_app.py
    echo to see detailed error messages
    echo.
    pause
)
