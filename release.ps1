# Build de release: gera dist/RemoteResolution.exe e copia para release/ (pronto para enviar ao cliente).
# Uso: .\release.ps1
param(
    [switch]$SkipInstall
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$src = Get-Content -Raw -Path "resolucao_cliente.py"
if ($src -notmatch 'VERSAO\s*=\s*"([^"]+)"') {
    Write-Host "Erro: não achei VERSAO em resolucao_cliente.py" -ForegroundColor Red
    exit 1
}
$ver = $Matches[1]
Write-Host "Versão detectada: $ver" -ForegroundColor Cyan

if (-not $SkipInstall) {
    py -3 -m pip install -r requirements.txt
}

$pngRel = "img\remote-resolution-icon-Photoroom.png"
if (-not (Test-Path $pngRel)) {
    Write-Host "Aviso: $pngRel não encontrado — ícone PNG/rodapé podem faltar no pacote." -ForegroundColor Yellow
}

py -3 make_ico.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "Erro: make_ico.py falhou (Pillow instalado? py -3 -m pip install -r requirements.txt)" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path "img\app.ico")) {
    Write-Host "Erro: img\app.ico não existe após make_ico.py" -ForegroundColor Red
    exit 1
}

Write-Host "Limpando artefatos anteriores (RemoteResolution)..." -ForegroundColor Cyan
Remove-Item -Recurse -Force "build\RemoteResolution" -ErrorAction SilentlyContinue
Remove-Item -Force "dist\RemoteResolution.exe" -ErrorAction SilentlyContinue
Remove-Item -Force "RemoteResolution.spec" -ErrorAction SilentlyContinue

$pyArgs = @(
    "-m", "PyInstaller",
    "--onefile",
    "--windowed",
    "--noconfirm",
    "--name", "RemoteResolution",
    "resolucao_cliente.py"
)
if (Test-Path $pngRel) {
    $pyArgs = @("--add-data", "${pngRel};img") + $pyArgs
}
$pyArgs = @("--add-data", "img\app.ico;img") + $pyArgs
$pyArgs = @("--icon", "img\app.ico") + $pyArgs

py -3 @pyArgs
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

New-Item -ItemType Directory -Force "release" | Out-Null
$outVersioned = "release\RemoteResolution-$ver.exe"
$outLatest = "release\RemoteResolution.exe"
Copy-Item -Force "dist\RemoteResolution.exe" $outVersioned
Copy-Item -Force "dist\RemoteResolution.exe" $outLatest

Write-Host ""
Write-Host "Release pronta." -ForegroundColor Green
Write-Host "  -> $outVersioned"
Write-Host "  -> $outLatest"
Write-Host ""
Write-Host "Distribua apenas o .exe ao cliente (AnyDesk / pasta / e-mail conforme política)." -ForegroundColor Gray
