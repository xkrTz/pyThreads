import os
import random
import time
from concurrent.futures import ThreadPoolExecutor

# Caminhos para os named pipes de números
fifo_num_in = '/tmp/fifo_num_in'   # Pipe para requisições de números
fifo_num_out = '/tmp/fifo_num_out' # Pipe para respostas de números

# Caminhos para os named pipes de strings
fifo_str_in = '/tmp/fifo_str_in'   # Pipe para requisições de strings
fifo_str_out = '/tmp/fifo_str_out' # Pipe para respostas de strings

# Função que processa uma requisição de número
def process_number_request():
    with open(fifo_num_in, 'rb') as pipe_num:
        request = pipe_num.read(1024).decode().strip()  # Ler a requisição do cliente
        if request == "Quero um número":  # Filtrar a requisição válida
            print(f"\n[Servidor] Requisição recebida: {request}")
            response = str(random.randint(0, 100)).encode()  # Gerar a resposta aleatória
            print(f"[Servidor] Respondendo com número: {response.decode()}")

            # Responder ao cliente
            with open(fifo_num_out, 'wb') as write_pipe:
                write_pipe.write(response)

# Função que processa uma requisição de string
def process_string_request():
    with open(fifo_str_in, 'rb') as pipe_str:
        request = pipe_str.read(1024).decode().strip()  # Ler a requisição do cliente
        if request == "Quero uma string":  # Filtrar a requisição válida
            print(f"\n[Servidor] Requisição recebida: {request}")
            response = random.choice(["Olá", "Mundo", "Teste", "Servidor"]).encode()  # Resposta aleatória
            print(f"[Servidor] Respondendo com string: {response.decode()}")

            # Responder ao cliente
            with open(fifo_str_out, 'wb') as write_pipe:
                write_pipe.write(response)

# Função para iniciar o servidor com pool de threads
def start_server():
    # Criando os named pipes para números e strings
    if not os.path.exists(fifo_num_in):
        os.mkfifo(fifo_num_in)
    if not os.path.exists(fifo_num_out):
        os.mkfifo(fifo_num_out)
    if not os.path.exists(fifo_str_in):
        os.mkfifo(fifo_str_in)
    if not os.path.exists(fifo_str_out):
        os.mkfifo(fifo_str_out)

    print("\n[Servidor] Servidor iniciado e aguardando requisições...")

    # Criando a pool de threads com até 4 threads simultâneas
    with ThreadPoolExecutor(max_workers=4) as executor:
        while True:
            # Escuta as requisições e delega para a pool de threads
            executor.submit(process_number_request)
            executor.submit(process_string_request)
            time.sleep(1)

if __name__ == "__main__":
    start_server()
