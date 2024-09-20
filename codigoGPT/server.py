import socket
import threading

# Dicionário para armazenar as opções de filmes e séries com suas respectivas contagens de votos
movies_series_votes = {
    "Filme 1": 0,
    "Filme 2": 0,
    "Filme 3": 0,
    "Série 1": 0,
    "Série 2": 0,
    "Série 3": 0
}

# Bloqueio para evitar condições de corrida ao atualizar os votos
lock = threading.Lock()

# Função para lidar com os clientes
def handle_client(client_socket):
    client_socket.sendall("Bem-vindo ao sistema de votação de Filmes/Séries!\n".encode())
    
    # Envia as opções de votação para o cliente
    options_message = "Opções disponíveis para votar:\n"
    for key in movies_series_votes:
        options_message += f"- {key}\n"
    options_message += "Digite o nome do filme/série para votar ou 'resultado' para ver o placar atual.\n"
    client_socket.sendall(options_message.encode())
    
    while True:
        # Recebe a escolha do cliente
        vote = client_socket.recv(1024).decode().strip()
        
        if vote.lower() == 'resultado':
            # Envia o resultado da votação para o cliente
            result_message = "\nResultado da votação atual:\n"
            with lock:
                for item, votes in movies_series_votes.items():
                    result_message += f"{item}: {votes} votos\n"
            client_socket.sendall(result_message.encode())
        elif vote in movies_series_votes:
            # Se o voto for válido, atualiza a contagem de votos
            with lock:
                movies_series_votes[vote] += 1
            client_socket.sendall(f"Obrigado por votar em {vote}!\n".encode())
        else:
            # Se a escolha não for válida, envia uma mensagem de erro
            client_socket.sendall("Opção inválida! Tente novamente.\n".encode())

# Função principal do servidor
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 5555))  # Escuta no localhost, porta 5555
    server.listen(5)  # Permite até 5 conexões simultâneas
    print("Servidor iniciado. Aguardando conexões...")

    while True:
        client_socket, addr = server.accept()
        print(f"Cliente conectado: {addr}")
        # Cria uma nova thread para lidar com cada cliente
        threading.Thread(target=handle_client, args=(client_socket,)).start()

start_server()
