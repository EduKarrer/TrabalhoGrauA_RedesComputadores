import socket
import threading

# Dicionário para armazenar as opções de filmes com suas respectivas contagens de votos
movies_series_votes = {
    1: {"nome": "Harry Potter", "votos": 0},
    2: {"nome": "Madagascar", "votos": 0},
    3: {"nome": "Senhor dos Anéis", "votos": 0},
    4: {"nome": "Breaking Bad", "votos": 0},
    5: {"nome": "Stranger Things", "votos": 0},
    6: {"nome": "Game of Thrones", "votos": 0}
}

# Bloqueio para evitar condições de corrida ao atualizar os votos
lock = threading.Lock()

# Função para lidar com os clientes
def handle_client(client_socket):
    try:
        # Envia a mensagem de boas-vindas
        client_socket.sendall("---------------------------------------------------".encode())
        client_socket.sendall("Bem-vindo ao sistema de votação de Filmes/Séries!\n".encode())
        client_socket.sendall("---------------------------------------------------".encode())

        while True:
            # Envia as opções de votação para o cliente
            options_message = "\nOpções disponíveis para votar:\n"
            for key, value in movies_series_votes.items():
                options_message += f"{key} - {value['nome']}\n"
            options_message += "7 - Ver resultado\n\n"
            options_message += "Escolha uma opção de filme para votar:\n"
            client_socket.sendall(options_message.encode())

            # Recebe a escolha do cliente
            vote = client_socket.recv(1024).decode().strip()
            if not vote:
                print("Cliente desconectado.")
                break  # Sai do loop se o cliente desconectar

            # Verifica se a entrada é um número válido
            if vote.isdigit():
                vote = int(vote)

                if vote == 7:
                    # Envia o resultado da votação para o cliente
                    result_message = "\nResultado da votação atual:\n"
                    with lock:
                        for key, value in movies_series_votes.items():
                            result_message += f"{value['nome']}: {value['votos']} votos\n"
                    client_socket.sendall(result_message.encode())
                elif vote in movies_series_votes:
                    # Se o voto for válido, atualiza a contagem de votos
                    with lock:
                        movies_series_votes[vote]['votos'] += 1
                    client_socket.sendall(f"Obrigado por votar em {movies_series_votes[vote]['nome']}!\n".encode())
                else:
                    client_socket.sendall("Opção inválida! Tente novamente.\n".encode())
            else:
                client_socket.sendall("Opção inválida! Digite um número válido.\n".encode())
    except Exception as e:
        print(f"Ocorreu um erro com o cliente: {e}")
    finally:
        client_socket.close()
        print("Conexão com o cliente encerrada.")

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
