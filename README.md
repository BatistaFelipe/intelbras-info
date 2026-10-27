# Intelbras Info

Ferramenta para buscar informações e gerenciar dispositivos (interfones) Intelbras via API, disponível em duas formas:

- **GUI** (`intelbras_info_gui.exe`) — interface gráfica em Tkinter para uso interativo no Windows.
- **CLI** (`intelbras_info.exe`) — linha de comando para scripts e automações.

## Funcionalidades

- Busca de informações gerais do sistema.
- Consulta de configurações SIP.
- Sincronização e leitura de data/hora do dispositivo.
- Reinicialização remota (Reboot).

## Estrutura do projeto

O código segue uma separação MVC:

| Arquivo | Camada | Responsabilidade |
| --- | --- | --- |
| `model.py` | Model | `Credentials` + funções HTTP contra o dispositivo Intelbras |
| `gui_view.py` | View (GUI) | Widgets Tkinter, estilos, formatação de saída; sem lógica |
| `gui_controller.py` | Controller (GUI) | Validação, threads, orquestra model ↔ view |
| `gui_app.py` | Entry point | Cria `tk.Tk`, instancia view + controller |
| `cli_controller.py` | Controller (CLI) | `argparse` + orquestração |
| `cli_app.py` | Entry point | Chama `cli_controller.run()` |

## Configuração

### Instalar pré-requisitos

1. Python3:

   > [Using Python on Unix platforms](https://docs.python.org/3/using/unix.html)
   >
   > [Using Python on Windows](https://docs.python.org/3/using/windows.html)
   >
   > [Installing Python Modules](https://docs.python.org/3/installing/index.html)

2. Abra o terminal dentro da pasta do projeto e execute o comando abaixo para instalar as bibliotecas necessárias:

   ```bash
   python3 -m pip install -r requirements.txt
   ```

### Criar o arquivo `.env` (somente CLI)

A GUI pede as credenciais no próprio formulário e **não** depende do `.env`. A CLI carrega as credenciais de variáveis de ambiente via [`python-dotenv`](https://pypi.org/project/python-dotenv/). Copie `.env.example` para `.env` (no mesmo diretório do script em dev, ou ao lado do `.exe` após instalado) e preencha:

```bash
INTELBRAS_USER=admin
INTELBRAS_PASSWORD=sua-senha
```

Alternativamente, defina `INTELBRAS_USER` e `INTELBRAS_PASSWORD` diretamente no ambiente — o `.env` é só um atalho.

## Build

Ambos os builds possuem arquivos `.spec` versionados no repositório — o uso dos specs é o caminho recomendado para builds reprodutíveis. O spec da GUI já embute o ícone (`assets/icon.ico`) no executável.

### GUI (janela, sem console)

```bash
pyinstaller gui_app.spec
```

Equivalente manual:

```bash
pyinstaller --onefile --windowed --collect-all requests --name intelbras_info_gui gui_app.py
```

### CLI

```bash
pyinstaller cli_app.spec
```

Equivalente manual:

```bash
pyinstaller --onefile --collect-all requests --name intelbras_info cli_app.py
```

### Instalação

Organize os arquivos da seguinte forma:

```text
├── intelbras-info/
│   ├── intelbras_info.exe
│   └── intelbras_info_gui.exe
├── Install.bat
└── install.ps1
```

Após organizar os arquivos rode o script `Install.bat`. O instalador:

- Copia a pasta para `C:\Program Files\intelbras-info`.
- Adiciona o diretório ao `PATH` do sistema (acesso à CLI por qualquer terminal).
- Cria atalhos **Intelbras Info** no Desktop e no Menu Iniciar apontando para a GUI.

## Uso — GUI

Abra pelo atalho no Desktop ou pelo Menu Iniciar e preencha:

- **IP/DDNS**: endereço do dispositivo (ex: `192.168.1.100` ou `meu-dominio.ddns.com`).
- **Porta**: porta HTTP do dispositivo (`1-65535`).
- **Usuário** e **Senha**: credenciais de acesso.

Botões:

- **BUSCAR** — busca em sequência: informações do sistema, configurações SIP e data/hora atual, exibindo o resultado na área central.
- **SINCRONIZAR DATA E HORA** — envia o horário atual do computador para o dispositivo.
- **REBOOT** — reinicia o dispositivo (pede confirmação).

## Uso — CLI

### Sintaxe Básica

Executar com **Python** direto do código fonte:

```bash
python3 cli_app.py -H [HOST:PORTA] [OPÇÕES]
```

Executar após a instalação com o `Install.bat`:

```bash
intelbras_info -H [HOST:PORTA] [OPÇÕES]
```

### Comandos Disponíveis

| Opção                | Descrição                                                         |
| -------------------- | ----------------------------------------------------------------- |
| `-H, --host`         | **Obrigatório:** Endereço do interfone (ex: `192.168.1.100:8085`) |
| `-i, --info`         | Exibe informações gerais do sistema                               |
| `-s, --sip-info`     | Exibe as configurações de SIP                                     |
| `-d, --get-datetime` | Retorna a data e hora atual do dispositivo                        |
| `-D, --set-datetime` | Ajusta a data e hora do dispositivo para o horário atual          |
| `-r, --reboot`       | Reinicia o dispositivo remotamente                                |
| `-h, --help`         | Mostra a mensagem de ajuda                                        |
