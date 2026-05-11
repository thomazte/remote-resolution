# Release build: creates dist/RemoteResolution.exe and copies to release/
# From repo root: .\scripts\release.ps1  or  .\GerarRelease.ps1
param(
    [switch]$SkipInstall
)

$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $RepoRoot

$verFile = Join-Path $RepoRoot "src\resolucao_cliente.py"
$src = Get-Content -Raw -Path $verFile
if ($src -notmatch 'VERSAO\s*=\s*"([^"]+)"') {
    Write-Host "Erro: VERSAO not found in src\resolucao_cliente.py" -ForegroundColor Red
    exit 1
}
$ver = $Matches[1]
Write-Host "Versao detectada: $ver" -ForegroundColor Cyan

if (-not $SkipInstall) {
    py -3 -m pip install -r requirements.txt
}

Write-Host "Limpando artefatos anteriores..." -ForegroundColor Cyan
Remove-Item -Recurse -Force "build\RemoteResolution" -ErrorAction SilentlyContinue
Remove-Item -Force "dist\RemoteResolution.exe" -ErrorAction SilentlyContinue
Remove-Item -Force "RemoteResolution.spec" -ErrorAction SilentlyContinue

$entry = "src\resolucao_cliente.py"
# Opcoes do PyInstaller: depois de "-m PyInstaller"; script .py sempre por ultimo.
$pyArgs = @(
    "-m", "PyInstaller",
    "--onefile",
    "--windowed",
    "--noconfirm",
    "--name", "RemoteResolution"
)
$pyArgs += $entry

py -3 @pyArgs
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

New-Item -ItemType Directory -Force "release" | Out-Null
$outVersioned = "release\RemoteResolution-$ver.exe"
$outLatest = "release\RemoteResolution.exe"
Copy-Item -Force "dist\RemoteResolution.exe" $outVersioned

$latestOk = $false
try {
    Copy-Item -Force "dist\RemoteResolution.exe" $outLatest -ErrorAction Stop
    $latestOk = $true
} catch {
    Write-Host ""
    Write-Host "AVISO: nao copiou para release\RemoteResolution.exe (arquivo em uso?)." -ForegroundColor Yellow
    Write-Host "Feche o RemoteResolution se estiver aberto e rode GerarRelease de novo, ou use:" -ForegroundColor Yellow
    Write-Host "  $RepoRoot\$outVersioned" -ForegroundColor Yellow
    Write-Host "Ou copie manualmente: dist\RemoteResolution.exe -> release\RemoteResolution.exe" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Release pronta." -ForegroundColor Green
Write-Host "  -> $RepoRoot\$outVersioned"
if ($latestOk) {
    Write-Host "  -> $RepoRoot\$outLatest"
}
Write-Host ""
Write-Host "Distribua apenas o .exe ao cliente (AnyDesk, pasta compartilhada ou e-mail, conforme politica da empresa)." -ForegroundColor Gray
