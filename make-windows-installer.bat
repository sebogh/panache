@echo off

for /f "tokens=1-2 delims= " %%a in ('bin\panache.exe --version 2^>^&1') do (
  @set VERSION=%%b
  goto :next
  )
:next
if "%VERSION%" == "" (
  echo Error: could not determine version number.
  exit /b 1
)
echo Detected version %VERSION%
echo Creating msi...

"C:\Program Files (x86)\WiX Toolset v3.11\bin\candle.exe" -dVERSION=%VERSION% panache.wxs
if %errorlevel% neq 0 exit /b %errorlevel%
"C:\Program Files (x86)\WiX Toolset v3.11\bin\light.exe" panache.wixobj -out panache-%VERSION%-windows.msi
if %errorlevel% neq 0 exit /b %errorlevel%
move panache-%VERSION%-windows.msi bin
