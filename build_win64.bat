@echo off
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed on this machine.
    echo Python is required to build the executable.
    echo.
    choice /C YN /M "Would you like to open the Python download page"
    if errorlevel 2 (
        echo.
        echo Please install Python from https://www.python.org/downloads/ and re-run this script.
        pause
        exit /b 1
    )
    start https://www.python.org/downloads/
    echo.
    echo After installing Python, close this window and re-run this script.
    echo IMPORTANT: Check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

echo Installing dependencies...
python -m pip install pyinstaller sqlalchemy openpyxl PyQt5 PyQtWebEngine qtpy bottle proxy_tools python-docx fpdf2 PyMuPDF
python -m pip install pywebview --no-deps
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo Building executable...
python -m PyInstaller --clean --distpath build\win64 --workpath build\tmp job_tracker.spec
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Build failed.
    pause
    exit /b 1
)

echo Cleaning up build temp files...
rmdir /s /q build\tmp

echo.
echo Done! Executable is at: build\win64\JobTracker.exe
echo.
choice /C YN /M "Uninstall build dependencies"
if errorlevel 2 goto :done
echo.
echo Uninstalling dependencies...
python -m pip uninstall -y pyinstaller pywebview sqlalchemy openpyxl PyQt5 PyQtWebEngine qtpy pyinstaller-hooks-contrib bottle proxy_tools packaging PyQt5-sip PyQt5-Qt5 PyQtWebEngine-Qt5 python-docx fpdf2 PyMuPDF lxml Pillow fonttools defusedxml

:done
pause
