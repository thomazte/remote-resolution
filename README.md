# Ajuste de Resolução — Suporte Remoto

Ferramenta desenvolvida para analistas de suporte que realizam atendimentos remotos via **AnyDesk**, **RustDesk** e **TeamViewer**.

Permite adaptar a resolução da máquina do cliente à tela do analista durante a sessão, facilitando a leitura e melhorando o desempenho no atendimento.

---

## Funcionalidades

- Lista todas as resoluções suportadas pelo hardware do cliente
- Botões de acesso rápido com as resoluções mais comuns do analista
- Testa a compatibilidade da resolução com o driver antes de aplicar
- Detecta e informa problemas com drivers de vídeo
- Restaura automaticamente a resolução original ao fechar
- Não requer instalação — basta executar o `.exe`

---

## Como usar?

### Opção 1 — Executável (recomendado)

1. Transfira o arquivo `AjusteResolucao.exe` para a máquina do cliente via ferramenta remota
2. Execute o arquivo — nenhuma instalação necessária
3. Escolha uma resolução e clique em **✔ Aplicar Selecionada**
4. Ao finalizar o atendimento, clique em **↺ Restaurar Original**

### Opção 2 — Script Python

Requer Python 3.x instalado na máquina do cliente.

```bash
python resolucao_cliente.py
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

Para alterar as resoluções de atalho rápido, edite a lista no início do arquivo `resolucao_cliente.py`:

```python
MINHAS_RESOLUCOES = [
    (1366, 768),
    (1280, 720),
    (1920, 1080),
    (1600, 900),
    (1440, 900),
    (1280, 800),
]
```

Após editar, gere novamente o `.exe` com:

```bash
python -m PyInstaller --onefile --windowed --name "AjusteResolucao" resolucao_cliente.py
```

O executável será gerado na pasta `dist/`.

---

## Requisitos

- Sistema operacional: **Windows** (7, 10 ou 11)
- Para rodar o `.exe`: nenhum requisito adicional
- Para rodar o `.py`: Python 3.x com `tkinter` (já incluso na instalação padrão)

---

## Observações

- A ferramenta altera a resolução **na máquina do cliente**, não na do analista
- Resoluções não suportadas pelo driver do cliente aparecem desativadas automaticamente
- Caso o driver de vídeo esteja ausente ou corrompido, a ferramenta exibe um aviso ao iniciar

---

Desenvolvido por **Thomaz Arthur**
Estudante de Análise e Desenvolvimento de Sistemas

🔗: https://www.linkedin.com/in/thomaz-arthur-a2a95b145/
