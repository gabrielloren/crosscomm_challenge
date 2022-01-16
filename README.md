# Cross Commerce Challenge
ETL API Challenge for Cross Commerce

Este script foi desenvolvido como desafio para a vaga de Desenvolvedor Elixir Pleno, na startup Cross Commerce.


Esta API foi criada com o Python versão **3.10.1**, caso sua versão seja anterior, favor atualizar antes de prosseguir, caso contrário poderão surgir BUGs.


O repositório deve ser clonado e iniciado o virtual environment pelo PowerShell ou teminal, navegando até a pasta clonada e executando os comandos:
```
# Linux
sudo apt-get install python3-venv    # Se necessário
python3 -m venv .venv
source .venv/bin/activate

# macOS
python3 -m venv .venv
source .venv/bin/activate

# Windows
py -3 -m venv .venv
.venv\scripts\activate
```

Após entrar no virtual environment, executar o script com o comando:
```
python app.py
```

O serviço de **load** é executado no *localhost* inicialmente na porta 8080. Caso exista necessidade de modificação, o mesmo pode ser alterado no arquivo [*app.py*](/app.py), através do parâmetro:
```
port = 8080
```

A requequisição deve ser feita no formato **GET** na URL padrão:
```
http://localhost:8080 ou http://127.0.0.1:8080
```

A resposta da requisição é recebida no formato JSON, possui dois parâmetros: **status** e **numbers**.

**status** apresenta a resposta *loading* enquanto está processando os dados e *done* quando os dados já estão processados.

**numbers** apresenta uma lista de números ordenados de maneira crescente, coletados anteriormente através da API fornecida.
