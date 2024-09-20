import socket

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 5555))  # Conecta-se ao servidor no localhost, porta 5555

    # Recebe a mensagem inicial do servidor
    while True:
        server_message = client.recv(1024).decode()
        print(server_message)
        
        # Envia o voto ou comando "resultado" ao servidor
        vote = input("Digite sua escolha: ")
        client.sendall(vote.encode())

start_client()
