# Intelbras Info CLI

Ferramenta de linha de comando para buscar informações e gerenciar dispositivos (interfones) Intelbras via API.

## Funcionalidades

- Busca de informações gerais do sistema.
- Consulta de configurações SIP.
- Sincronização e leitura de data/hora do dispositivo.
- Reinicialização remota (Reboot).

## Configuração

### Instalar pré-requisitos

1. Python3:

   > [Using Python on Unix platforms](https://docs.python.org/3/using/unix.html)
   >
   > [Using Python on Windows](https://docs.python.org/3/using/windows.html)
   >
   > [Installing Python Modules](https://docs.python.org/3/installing/index.html)

2. Abra o terminal dentro da pasta do projeto e execute o comando abaixo para instalar as bibliotecas necessárias:

   ```
   python3 -m pip install -r requirements.txt
   ```

### Criar o arquivo de configuração

Crie um arquivo com o nome `config.py` no mesmo diretório do projeto com as variáveis USER e PASSWORD no seguinte formato:

```
USER="USUÁRIO_DE_ACESSO"
PASSWORD="SENHA_DE_ACESSO"
```

## Execução

### Sintaxe Básica

```bash
python3 intelbras_info.py -H [HOST:PORTA] [OPÇÕES]
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
