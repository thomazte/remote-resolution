# Build rápido: gera dist/RemoteResolution.exe (Windows).
# Para pacote pronto para enviar ao cliente (pasta release/, build limpo), use: .\release.ps1
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

py -3 -m pip install -r requirements.txt

$pngRel = "img\remote-resolution-icon-Photoroom.png"
if (-not (Test-Path $pngRel)) {
    Write-Host "Aviso: $pngRel não encontrado — ícone da janela e rodapé não aparecerão no app empacotado." -ForegroundColor Yellow
}

py -3 make_ico.py

$pyArgs = @(
    "-m", "PyInstaller",
    "--onefile",
    "--windowed",
    "--name", "RemoteResolution",
    "resolucao_cliente.py"
)
if (Test-Path $pngRel) {
    $pyArgs = @("--add-data", "${pngRel};img") + $pyArgs
}
if (Test-Path "img\app.ico") {
    $pyArgs = @("--add-data", "img\app.ico;img") + $pyArgs
    $pyArgs = @("--icon", "img\app.ico") + $pyArgs
}
py -3 @pyArgs

Write-Host "Concluído: dist\RemoteResolution.exe" -ForegroundColor Green
