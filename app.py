from threading import Thread, Event
from flask import *
from load import extract
import json
from time import sleep

port = 8080             # Porta de execução do serviço de load 

sort_numbers = []       # Lista que armazenará os numeros ordenados
sort_flag = False       # Flag de sinalização da ordenação dos números
event = Event()

def start_extract():            # Define função de inicialização da extração
    global sort_flag
    global sort_numbers
    global port
    sort_numbers = extract()    # Solicita a extração dos numeros através da API
    sort_flag = True            # Sinaliza o final da extração e ordenação
    print("Carregamento de dados concluído. Acesse http://localhost:"+str(port))
        

def start_server():             # Define função de inicialização do webserver
    global sort_flag
    global sort_numbers
    app = Flask(__name__)       # Cria instância do webserver em Flask
    app.config["DEBUG"] = False # Desativa o modo depuração
    app.secret_key = 'Cross Commerce API'   # Chave aleatória de segurança

    @app.route('/', methods=["GET"])    # Define diretório raiz e método das requisições
    def index():
        if not sort_flag:               # Verifica se os numeros já foram recebidos e ordenados
            js = [{"status" : "loading", "numbers" : "[]"}] 
            return Response(json.dumps(js),  mimetype='application/json') # Se não, retorna status "loading"
        else:
            js = [{"status": "done", "numbers" : sort_numbers}]
            return Response(json.dumps(js),  mimetype='application/json') # Se sim, retorna status "done" + sequência de números
    
    from waitress import serve  # Usa o serve da waitress para iniciar o Flask
    while True:
        serve(app, host="0.0.0.0", port=port) # Inicia host na porta especificada


p1 = Thread(target=start_extract)   # Define a função como Thread p1
p1.daemon = True
p2 = Thread(target=start_server)    # Define a função como Thread p2
p2.daemon = True

if __name__ == "__main__":          # Inicializa Threads simultaneamente
    p2.start()
    p1.start()

while True:
    sleep(1)
