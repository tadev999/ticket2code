@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
if exist "%ProgramFiles%\PowerShell\7\pwsh.exe" (
  "%ProgramFiles%\PowerShell\7\pwsh.exe" -NoProfile -File "%SCRIPT_DIR%figma_export_svg.ps1" %*
  exit /b %ERRORLEVEL%
)
powershell -NoProfile -File "%SCRIPT_DIR%figma_export_svg.ps1" %*
exit /b %ERRORLEVEL%
