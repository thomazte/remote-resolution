# Atalho na raiz: gera o .exe de release (pasta release/).
param([switch]$SkipInstall)

& "$PSScriptRoot\scripts\release.ps1" @PSBoundParameters
