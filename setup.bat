@echo off
REM ============================================================
REM  Uma Auto - first-time setup.
REM  Double-click this once. It installs the app and creates an
REM  "Uma Auto" shortcut in this folder. Use that shortcut from
REM  then on: it opens the app with no console window.
REM ============================================================
cd /d "%~dp0"

python --version >nul 2>&1
if errorlevel 1 (
  echo.
  echo [!] Python is not installed or not on PATH.
  echo     Install Python 3.10+ from https://www.python.org/downloads/
  echo     with "Add python.exe to PATH" checked, then run again.
  echo.
  pause
  exit /b 1
)

if not exist ".venv\Scripts\pythonw.exe" (
  echo Installing Uma Auto, this takes about a minute...
  echo.
  python -m venv .venv
  call ".venv\Scripts\activate.bat"
  python -m pip install --upgrade pip
  pip install -e ".[gui]"
  if errorlevel 1 (
    echo.
    echo [!] Installation failed. Check the messages above.
    pause
    exit /b 1
  )
)

echo Creating the "Uma Auto" shortcut in this folder...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$w=New-Object -ComObject WScript.Shell; $s=$w.CreateShortcut('%CD%\Uma Auto.lnk'); $s.TargetPath='%CD%\.venv\Scripts\pythonw.exe'; $s.Arguments='-m umauto.gui'; $s.WorkingDirectory='%CD%'; $s.IconLocation='%CD%\img\uma_auto.ico,0'; $s.Save()"

echo.
echo Done! Double-click the "Uma Auto" shortcut in this folder to launch the app.
echo (Opening it now...)
start "" ".venv\Scripts\pythonw.exe" -m umauto.gui
exit /b 0
