# RemoteResolution — Suporte Remoto

Ferramenta desenvolvida para analistas de suporte que realizam atendimentos remotos via **AnyDesk**, **RustDesk** e **TeamViewer**.

Permite adaptar a resolução da máquina do cliente à tela do analista durante a sessão, facilitando a leitura e melhorando o desempenho no atendimento.

---

## Funcionalidades

- Lista todas as resoluções suportadas pelo hardware do cliente
- Botões de acesso rápido com as resoluções mais comuns do analista
- Testa a compatibilidade da resolução com o driver antes de aplicar
- Detecta e informa problemas com drivers de vídeo
- Ao fechar, pergunta se deseja restaurar a resolução original
- Não requer instalação — basta executar o `.exe`

---

## Estrutura do projeto

| Arquivo | Função |
|--------|--------|
| `resolucao_cliente.py` | Aplicativo principal (interface e fluxo) |
| `win_display.py` | Chamadas Win32 (`EnumDisplaySettings`, `ChangeDisplaySettings`) |
| `driver_info.py` | Dados do adaptador via PowerShell (`Get-CimInstance` / `Get-WmiObject`) |
| `ajuste_resolucao.py` | Entrada opcional; executa o mesmo programa que `resolucao_cliente.py` |
| `app_assets.py` | Localização do PNG em modo script e dentro do `.exe` (PyInstaller) |
| `img/remote-resolution-icon-Photoroom.png` | Ícone da janela, assinatura visual no rodapé e base para `img/app.ico` no build |
| `release.ps1` | Build de **release**: limpa artefatos, gera `.exe` e copia para `release/` (arquivo pronto para o cliente) |
| `build.ps1` | Build **rápido** (gera só `dist/RemoteResolution.exe`, sem limpar nem copiar) |

---

## Como usar?

### Opção 1 — Executável (recomendado)

1. Transfira o arquivo `RemoteResolution.exe` para a máquina do cliente via ferramenta remota
2. Execute o arquivo — nenhuma instalação necessária
3. Escolha uma resolução e clique em **✔ Aplicar Selecionada**
4. Ao finalizar o atendimento, clique em **↺ Restaurar Original**

### Opção 2 — Script Python

Requer Python 3.x instalado na máquina do cliente.

No Windows, se `python` não estiver no PATH, use o launcher **`py -3`** (como no exemplo abaixo).

```powershell
py -3 resolucao_cliente.py
```

O arquivo `ajuste_resolucao.py` faz a mesma coisa (compatibilidade com atalhos ou scripts antigos):

```powershell
py -3 ajuste_resolucao.py
```

---

## Transferência do arquivo via ferramenta remota

| Ferramenta | Como transferir |
|---|---|
| **AnyDesk** | Menu superior → ícone de pasta (File Transfer) |
| **TeamViewer** | Menu `File & Extras` → `Open File Transfer` |
| **RustDesk** | Ícone de pasta na barra de ferramentas |

---

## Personalização

Para alterar as resoluções de atalho rápido, você pode:

- editar a lista padrão `MINHAS_RESOLUCOES`
- criar/ajustar perfis em `PERFIS_RESOLUCAO` (ex.: Notebook, Full HD, QHD/4K)

No início do arquivo `resolucao_cliente.py`:

```python
MINHAS_RESOLUCOES = [
    (1366, 768),
    (1280, 720),
    (1920, 1080),
    (1600, 900),
    (1440, 900),
    (1280, 800),
]

PERFIS_RESOLUCAO = {
    "Padrão (recomendado)": MINHAS_RESOLUCOES,
    "Notebook/HD": [...],
    "Full HD / 16:10": [...],
    "QHD / 4K / Ultrawide": [...],
}
```

Após editar, gere novamente o `.exe`. Na pasta do projeto:

1. Instale as dependências de build (na sua máquina de desenvolvimento, uma vez):

   ```powershell
   py -3 -m pip install -r requirements.txt
   ```

2. **Release para o cliente (recomendado)** — ícone embutido no `.exe`, build limpo e cópia versionada:

   ```powershell
   .\release.ps1
   ```

   Saída:

   - `release\RemoteResolution.exe` — última build (nome fixo, fácil de anexar)
   - `release\RemoteResolution-<versão>.exe` — mesma build com versão lida de `VERSAO` em `resolucao_cliente.py`

   **Distribua só um desses arquivos** para o cliente (AnyDesk, pasta compartilhada, etc.). Não é necessário instalar Python nem Pillow na máquina do cliente.

   Parâmetro opcional (se as dependências já estiverem instaladas):

   ```powershell
   .\release.ps1 -SkipInstall
   ```

3. **Build rápido** (só gera `dist\RemoteResolution.exe`, sem limpar nem pasta `release/`):

   ```powershell
   .\build.ps1
   ```

   Ou, manualmente (PowerShell — em `--add-data` use `origem;destino`):

   ```powershell
   py -3 make_ico.py
   py -3 -m PyInstaller --onefile --windowed --name "RemoteResolution" --icon img/app.ico --add-data "img/remote-resolution-icon-Photoroom.png;img" --add-data "img/app.ico;img" resolucao_cliente.py
   ```

Coloque o PNG em `img/remote-resolution-icon-Photoroom.png` (ou ajuste o nome em `app_assets.py`, em `--add-data` e em `make_ico.py`). O `release.ps1` e o `build.ps1` chamam `make_ico.py`, que gera `img/app.ico` antes do PyInstaller.

A pasta `release/` está no `.gitignore` (binários grandes). Remova essa entrada do `.gitignore` se quiser versionar os `.exe` no Git.

---

## Requisitos

- Sistema operacional: **Windows** (7, 10 ou 11)
- Para rodar o `.exe`: nenhum requisito adicional
- Para rodar o `.py`: Python 3.x com `tkinter` (já incluso na instalação padrão)

---

## Observações

- A ferramenta altera a resolução **na máquina do cliente**, não na do analista
- O ajuste vale em geral para o **monitor principal** do Windows
- Resoluções não suportadas pelo driver do cliente aparecem desativadas automaticamente
- Caso o driver de vídeo esteja ausente ou corrompido, a ferramenta exibe um aviso ao iniciar
- Informações de driver usam **PowerShell** (CIM, com fallback para WMI), sem depender do `wmic` (em desuso)

---

## Testes sugeridos antes de distribuir uma nova versão

- Windows 10 e 11: abrir o app, aplicar uma resolução da lista e restaurar
- Máquina com um e com dois monitores (confirmar que o comportamento no principal é o esperado)
- Conta sem privilégios de administrador
- Botão **Driver de vídeo** retorna texto ou mensagem amigável se o PowerShell estiver bloqueado

**Versão atual do código:** 1.1.1 (constante `VERSAO` em `resolucao_cliente.py`).

---

Desenvolvido por **Thomaz Arthur**

Estudante de Análise e Desenvolvimento de Sistemas

🔗: https://www.linkedin.com/in/thomaz-arthur-a2a95b145/
