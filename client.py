import socket

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 5555))  # Conecta-se ao servidor no localhost, porta 5555

    try:
        while True:
            # Recebe a mensagem do servidor (pode ser opções ou resultado)
            server_message = client.recv(4096).decode()
            if not server_message:
                print("Conexão fechada pelo servidor.")
                break  # Sai do loop se o servidor fechar a conexão
            print(server_message)

            # Verifica se o servidor está solicitando uma entrada
            if "Escolha uma opção de filme para votar:" in server_message:
                vote = input()
                client.sendall(vote.encode())
            else:
                # Se a mensagem não solicitar entrada, continuamos recebendo
                continue
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        client.close()
        print("Conexão encerrada.")

start_client()
