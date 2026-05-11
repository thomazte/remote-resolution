# Quick build: dist/RemoteResolution.exe at repo root.
# Full release: .\GerarRelease.ps1 from repo root.
$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $RepoRoot

Write-Host "Limpando artefatos locais (build/dist/spec)..." -ForegroundColor Cyan
Remove-Item -Recurse -Force "build" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "dist" -ErrorAction SilentlyContinue
Remove-Item -Force "RemoteResolution.spec" -ErrorAction SilentlyContinue

py -3 -m pip install -r requirements.txt

$entry = "src\resolucao_cliente.py"
$pyArgs = @(
    "-m", "PyInstaller",
    "--onefile",
    "--windowed",
    "--name", "RemoteResolution"
)
$pyArgs += $entry

py -3 @pyArgs

Write-Host "Concluido: $RepoRoot\dist\RemoteResolution.exe" -ForegroundColor Green
