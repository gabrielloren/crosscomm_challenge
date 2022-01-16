import aiohttp, asyncio
from time import sleep
from urllib.error import URLError, HTTPError


crossCommUrl = "http://challenge.dienekes.com.br/api/numbers?page=" # URL da requisição
headers = {'User-Agent': 'API', 'content-type': 'application/json'} # Cabeçalho da requisição

numbers = []            # Lista de numeros adquiridos
listEmpty = False       # Flag de fim da lista

async def get_api_data(session, url):
    global numbers
    global listEmpty
    global headers
    success = False     # Flag requisição exitosa
    errSequence = 0     # Sequencia de erros
    errLimit = 20       # Limite de erros consecutivos
    while not success:
        try: 
            async with session.get(url, headers=headers, timeout=20) as response:
                data = await response.json()
                print(url, "Status:", response.status, "Array:", len(numbers))
                if response.status == 200:
                    if len(data["numbers"]) > 0:
                        numbers += data["numbers"]
                    else:
                        listEmpty = True    # Se o argumento veio vazio, sinaliza o final da lista
                    success = True
        except HTTPError as e:
            # Apresenta codigo de erro HTTP
            print("Codigo de erro HTTP: ", e.code, "- Tentando novamente...")
            errSequence += 1
            if errSequence == errLimit:
                raise Exception("Limite de tentativas excedida. Verifique sua conexão ou tente novamente mais tarde.")
        except URLError as e:
            # Apresenta codigo de erro de URL
            print("Erro de URL: ", e.reason, "- Tentando novamente...")
            errSequence += 1
            if errSequence == errLimit:
                raise Exception("Limite de tentativas excedida. Verifique sua conexão ou tente novamente mais tarde.")
        except KeyError:
            #Processa o erro caso a chave 'numbers' não esteja presente (faz uma nova requisição)
            print("Erro, chave não encontrada - Tentando novamente...")
            errSequence += 1
            if errSequence == errLimit:
                raise Exception("Limite de tentativas excedida. Verifique sua conexão ou tente novamente mais tarde.")
        except asyncio.TimeoutError:
            #Processa exception de timeout da requisição
            print("Erro, timeout - Tentando novamente...")
            errSequence += 1
            if errSequence == errLimit:
                raise Exception("Limite de tentativas excedida. Verifique sua conexão ou tente novamente mais tarde.")
        else:
            errSequence = 0


async def Make_request():
    global numbers
    global listEmpty
    global crossCommUrl
    listIndex = 0       #Index de requisição da página
    interval = 100       #Intervalo de requisições simultâneas
    
    connector = aiohttp.TCPConnector(limit=50)  # Cria connector e limita o número de conexões simultâneas
    async with aiohttp.ClientSession(connector=connector) as session: #Cria sessão http para as requisições assíncronas
        while not listEmpty:
            
            tasks = []
            for page in range(1,interval):
                try:
                    #Cria chamada para a função de requisição e acrescenta à lista de tarefas
                    tasks.append(asyncio.ensure_future(get_api_data(session,crossCommUrl+str(page+listIndex))))
                except Exception:
                    print("ERRO na criação das tasks de request")
                    break
            # Aguarda a execução dos requests simultâneos para prosseguir
            await asyncio.gather(*tasks)
            # Incrementa index das páginas
            listIndex += interval-1
        

# Rotina para ordenação crescente dos números
def qsort(list):
    if not list:  # Caso o elemento seja nulo, retorna uma lista vazia
        return []
    else:   # Percorrer todos os elementos da lista
        pivot = list[0] # Cria um pivot com o elemento zero da posição atual
        less = [x for x in list     if x <  pivot]
        more = [x for x in list[1:] if x >= pivot]
        return qsort(less) + [pivot] + qsort(more)

    
def extract():
    global numbers
    asyncio.run(Make_request()) # Inicia carregamento assíncrono dos números
    print("Iniciando ordenação dos numeros coletados...")
    numbers = qsort(numbers) # Realiza a ordenação (transform) dos números coletados
    print("Ordenação dos números concluída!")
    return numbers # Retorna os números ordenados

