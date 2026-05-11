# RemoteResolution

Ferramenta desktop para **suporte remoto** (AnyDesk, RustDesk, TeamViewer, etc.): permite ao analista orientar o ajuste da **resolução de ecrã** na máquina do cliente e **restaurar** a resolução original no fim do atendimento.

---

## Funcionalidades

- Lista de resoluções suportadas pelo driver do cliente (monitor principal).
- Perfis de atalhos e aplicação rápida de resoluções comuns.
- Restauração explícita para a resolução capturada ao abrir a aplicação.
- Informação de driver de vídeo (CIM/WMI via PowerShell).
- Interface com barra de título integrada (sem depender da barra nativa do Windows para os controlos principais).

---

## Requisitos

| Contexto | Requisito |
|----------|-----------|
| **Cliente** (só executável) | Windows 10 ou 11 (x64). Não é necessário Python. |
| **Build / desenvolvimento** | Windows, [Python 3](https://www.python.org/downloads/) com o launcher `py` disponível no PATH. |

---

## Desenvolvimento (código-fonte)

Na raiz do repositório:

```powershell
py -3 -m pip install -r requirements.txt
py -3 src\resolucao_cliente.py
```

Ponto de entrada alternativo (compatibilidade):

```powershell
py -3 src\ajuste_resolucao.py
```

---

## Build e distribuição

### Release completa (recomendado)

Gera o executável com **PyInstaller**, limpa artefactos anteriores e copia o resultado para `release\`, incluindo um ficheiro com sufixo de versão (lido de `VERSAO` em `src\resolucao_cliente.py`).

```powershell
.\GerarRelease.ps1
```

Instala dependências a partir de `requirements.txt`. Para repetir o build sem reinstalar pacotes:

```powershell
.\GerarRelease.ps1 -SkipInstall
```

**Saídas esperadas**

| Ficheiro | Descrição |
|----------|-----------|
| `dist\RemoteResolution.exe` | Binário gerado pelo PyInstaller. |
| `release\RemoteResolution.exe` | Cópia “última” para distribuição imediata. |
| `release\RemoteResolution-<versão>.exe` | Cópia versionada (arquivo e histórico local). |

> **Nota:** A pasta `release\` não é versionada no Git (ver `.gitignore`). Os `.exe` são **artefactos locais**; cada máquina de desenvolvimento gera os seus com `GerarRelease.ps1`. Se `RemoteResolution.exe` estiver em execução, feche a aplicação antes de voltar a correr o script para evitar falha ao substituir o ficheiro.

### Build rápido (apenas `dist\`)

```powershell
.\scripts\build.ps1
```

Útil para validar o executável sem copiar para `release\`.

---

## Estrutura do repositório

```text
remote-resolution/
├── GerarRelease.ps1      # Atalho na raiz → chama scripts/release.ps1
├── README.md
├── requirements.txt      # PyInstaller (ambiente de build)
├── .gitignore
├── scripts/
│   ├── release.ps1       # Build completo + cópia para release/
│   └── build.ps1         # Build rápido → dist/
└── src/
    ├── resolucao_cliente.py   # Aplicação principal (GUI)
    ├── ajuste_resolucao.py    # Entrada legada → delega na principal
    ├── win_display.py         # Alteração de resolução (Win32)
    └── driver_info.py         # Informação do adaptador (PowerShell)
```

Pastas **`build\`**, **`dist\`** e **`release\`** (e o ficheiro **`RemoteResolution.spec`**) são **geradas pelo PyInstaller** ou pelo script de release: não fazem parte do controlo de versões e podem ser apagadas em qualquer momento; voltam a ser criadas ao correr os scripts de build.

---

## Limitações e boas práticas

- Altera a resolução do **monitor principal**; combinações exóticas ou drivers limitados podem restringir modos disponíveis.
- Ao fechar com resolução alterada, a aplicação pergunta se deseja restaurar a original.
- Distribua o `.exe` de acordo com a política da sua organização (canal seguro, assinatura futura, etc.).

---

## Autor

**Thomaz Arthur** — [LinkedIn](https://www.linkedin.com/in/thomaz-arthur-a2a95b145/)
