# RemoteResolution — Suporte Remoto

Ferramenta para analistas de suporte que atendem via AnyDesk, RustDesk ou TeamViewer.
Ela ajusta a resolucao da maquina do cliente e permite restaurar ao final do atendimento.

## Gerar o .exe

Na raiz do repositorio:

```powershell
.\GerarRelease.ps1
```

Saida:

- `release\RemoteResolution.exe`
- `release\RemoteResolution-<versao>.exe`

Build rapido:

```powershell
.\scripts\build.ps1
```

## Estrutura (limpa)

```text
remote-resolution/
├── GerarRelease.ps1
├── README.md
├── requirements.txt
├── .gitignore
├── scripts/
│   ├── release.ps1
│   └── build.ps1
└── src/
    ├── resolucao_cliente.py
    ├── ajuste_resolucao.py
    ├── win_display.py
    └── driver_info.py
```

## Uso

Executavel (recomendado): envie `RemoteResolution.exe` ao cliente.

Script (desenvolvimento):

```powershell
py -3 src\resolucao_cliente.py
```

## Requisitos

- Cliente: Windows 7/10/11 (somente o .exe)
- Desenvolvimento/build: Windows + `py -3`

## Observacoes

- Altera a resolucao no cliente (monitor principal)
- Modos nao suportados ficam desativados
- Leitura de driver via PowerShell (CIM/WMI)

---

Desenvolvido por **Thomaz Arthur**  
🔗 https://www.linkedin.com/in/thomaz-arthur-a2a95b145/
