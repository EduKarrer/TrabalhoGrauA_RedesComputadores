import socket
import threading

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

def handle_client(client_socket):
    try:
        client_socket.sendall("---------------------------------------------------".encode())
        client_socket.sendall("\033[31m""Bem-vindo ao sistema de votação de Filmes/Séries!\n""\033[0m".encode())
        client_socket.sendall("---------------------------------------------------".encode())

        while True:
            options_message = "\nOpções disponíveis para votar:\n\n"
            for key, value in movies_series_votes.items(): 
                options_message += f"{key} - {value['nome']}\n" 
            options_message += "\nEscolha uma opção de filme para votar:\n"
            options_message += "\n=========================================\n"
            options_message += "Digite 0 para sair\nDigite 7 para ver o resultado da votação\n"
            options_message += "=========================================\n"
            client_socket.sendall(options_message.encode())

            vote = client_socket.recv(1024).decode().strip()
            if not vote:
                print("Cliente desconectado.")
                break  

            if vote.isdigit():
                vote = int(vote)
                if vote == 0:
                    print("Cliente solicitou desconexão.")
                    client_socket.sendall("Conexão encerrada. Obrigado por participar!\n".encode())
                    break  
                elif vote == 7:
                    result_message = "\n""\033[30;47m" "Resultado da votação atual: ""\033[0m" "\n"
                    result_message += "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                    with lock:
                        for key, value in movies_series_votes.items():
                            result_message += f"{value['nome']}: {value['votos']} votos\n"
                    client_socket.sendall(result_message.encode())
                elif vote in movies_series_votes:
                    with lock:
                        movies_series_votes[vote]['votos'] += 1
                    client_socket.sendall(f"Obrigado por votar no filme {movies_series_votes[vote]['nome']}!\n".encode())
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
    server.bind(("127.0.0.1", 5555)) 
    server.listen(5)  
    print("Servidor iniciado. Aguardando conexões...")

    while True:
        client_socket, addr = server.accept()
        print(f"Cliente conectado: {addr}")
        # Cria uma nova thread para lidar com cada cliente
        threading.Thread(target=handle_client, args=(client_socket,)).start() 

start_server()