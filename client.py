import socket

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 5555))  

    try:
        while True:
            server_message = client.recv(4096).decode()
            if not server_message:
                print("Conexão fechada pelo servidor.")
                break 
            print(server_message)

            if "Escolha uma opção de filme para votar" in server_message:
                vote = input()

                if vote == '0':
                    client.sendall(vote.encode())
                    print("Desconectando do servidor...")
                    break  
                else:
                    client.sendall(vote.encode())
            else:
                continue
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        client.close()
        print("Conexão encerrada.")

start_client()