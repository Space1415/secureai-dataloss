@echo off
echo Setting up SecureAI manually...
echo.

echo Step 1: Creating virtual environment with Python 3.12...
py -3.12 -m venv pdfmcp
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

echo Step 2: Activating virtual environment...
call pdfmcp\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

echo Step 3: Upgrading pip...
python -m pip install --upgrade pip

echo Step 4: Installing SecureAI...
python -m pip install git+https://github.com/postralai/masquerade@main
if errorlevel 1 (
    echo Error: Failed to install SecureAI
    pause
    exit /b 1
)

echo Step 5: Creating .env file...
if not exist .env (
    echo TINFOIL_API_KEY=your_api_key_here > .env
    echo Created .env file - please edit it and add your Tinfoil API key
)

echo Step 6: Creating test directory...
if not exist test_files mkdir test_files

echo.
echo Setup completed successfully!
echo.
echo Next steps:
echo 1. Edit .env file and add your Tinfoil API key
echo 2. Activate virtual environment: pdfmcp\Scripts\activate.bat
echo 3. Test installation: python demo_secureai.py
echo.
pause 