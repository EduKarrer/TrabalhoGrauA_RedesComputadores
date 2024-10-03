import socket

def inicia_cliente():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 5555)) 

    try:
        while True:
            mensagem_servidor = client.recv(4096).decode()
            if not mensagem_servidor:
                print("Conexão fechada pelo servidor.")
                break  
            print(mensagem_servidor)

            if "Escolha uma opção de filme para votar" in mensagem_servidor:
                voto = input()

                if voto == '0':
                    client.sendall(voto.encode())
                    print("Desconectando do servidor...")
                    break  
                else:
                    client.sendall(voto.encode())
            else:
                continue
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        client.close()
        print("Conexão encerrada.")

inicia_cliente()