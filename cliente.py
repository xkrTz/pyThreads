import os
import time

# Caminhos para os named pipes de números
fifo_num_in = '/tmp/fifo_num_in'   # Pipe para requisições de números
fifo_num_out = '/tmp/fifo_num_out' # Pipe para respostas de números

# Caminhos para os named pipes de strings
fifo_str_in = '/tmp/fifo_str_in'   # Pipe para requisições de strings
fifo_str_out = '/tmp/fifo_str_out' # Pipe para respostas de strings

# Cliente que solicita um número
def client_number_request():
    with open(fifo_num_in, 'wb') as pipe_num:
        request = "Quero um número"
        print(f"[Cliente] Enviando requisição: {request}")
        pipe_num.write(request.encode())  # Enviar a requisição
    
    with open(fifo_num_out, 'rb') as pipe_num:
        response = pipe_num.read(1024).decode()  # Leitura da resposta
        print(f"[Cliente] Resposta recebida: {response}")

# Cliente que solicita uma string
def client_string_request():
    with open(fifo_str_in, 'wb') as pipe_str:
        request = "Quero uma string"
        print(f"[Cliente] Enviando requisição: {request}")
        pipe_str.write(request.encode())  # Enviar a requisição
    
    with open(fifo_str_out, 'rb') as pipe_str:
        response = pipe_str.read(1024).decode()  # Leitura da resposta
        print(f"[Cliente] Resposta recebida: {response}")

if __name__ == "__main__":
    client_number_request()
    time.sleep(1)
    client_string_request()
