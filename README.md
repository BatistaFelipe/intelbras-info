# Intelbras Info

Aplicação de terminal para verificar informações sobre dispositivos Intelbras via API.

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

Abra o terminal na pasta do projeto e execute o programa com o comando: 

```
python3 intelbrasInfo.py
```

-> Saída: `<IP:porta>:`

Digite o endereço do dispositivo usando o formato **IP:PORTA**, por exemplo:
- 192.168.2.104:8085
- meuexemplo.com.br:8086

### Menu 

Será exibido o menu conforme descrito abaixo. Digite apenas o número da opção desejada.

| Opção | Nome | Descrição |
|---|------|-----------|
| 1 | Informações gerais | Informações de modelo, serial, etc. |
| 2 | Informações sip | Informações sobre sip, usuário, porta, ip, etc. |
| 3 | Data e hora | Mostra a informação de data e hora do dispositivo. |
| 4 | Ajustar data e hora | Salva nova data e hora usando como base a do computador. |
| 5 | Reiniciar | Reiniciar o dispositivo. |
| 0 | Sair | Finalizar a aplicação. |