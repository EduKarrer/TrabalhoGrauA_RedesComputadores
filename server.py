import socket
import threading

votos_filmes_series = {
    1: {"nome": "Harry Potter", "votos": 0},
    2: {"nome": "Madagascar", "votos": 0},
    3: {"nome": "Senhor dos Anéis", "votos": 0},
    4: {"nome": "Breaking Bad", "votos": 0},
    5: {"nome": "Stranger Things", "votos": 0},
    6: {"nome": "Game of Thrones", "votos": 0}
}

lock = threading.Lock()

def gerencia_cliente(client_socket):
    try:
        client_socket.sendall("---------------------------------------------------".encode())
        client_socket.sendall("\033[31m""Bem-vindo ao sistema de votação de Filmes/Séries!\n""\033[0m".encode())
        client_socket.sendall("---------------------------------------------------".encode())

        while True:
            mensagem_opcoes = "\nOpções disponíveis para votar:\n\n"
            for i, value in votos_filmes_series.items(): 
                mensagem_opcoes += f"{i} - {value['nome']}\n" 
            mensagem_opcoes += "\nEscolha uma opção de filme para votar:\n"
            mensagem_opcoes += "\n=========================================\n"
            mensagem_opcoes += "Digite 0 para sair\nDigite 7 para ver o resultado da votação\n"
            mensagem_opcoes += "=========================================\n"
            client_socket.sendall(mensagem_opcoes.encode())

            voto = client_socket.recv(1024).decode().strip()
            if not voto:
                print("Cliente desconectado.")
                break  

            if voto.isdigit():
                voto = int(voto)
                if voto == 0:
                    print("Cliente solicitou desconexão.")
                    client_socket.sendall("Conexão encerrada. Obrigado por participar!\n".encode())
                    break  

                elif voto == 7:
                    mensagem_resultado = "\n""\033[30;47m" "Resultado da votação atual: ""\033[0m" "\n"
                    mensagem_resultado += "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                    with lock:
                        for i, value in votos_filmes_series.items():
                            mensagem_resultado += f"{value['nome']}: {value['votos']} votos\n"
                    client_socket.sendall(mensagem_resultado.encode())
                elif voto in votos_filmes_series:
                    with lock:
                        votos_filmes_series[voto]['votos'] += 1
                    client_socket.sendall(f"Obrigado por votar no filme {votos_filmes_series[voto]['nome']}!\n".encode())
                else:
                    client_socket.sendall("Opção inválida! Tente novamente.\n".encode())
            else:
                client_socket.sendall("Opção inválida! Digite um número válido.\n".encode())
    except Exception as e:
        print(f"Ocorreu um erro com o cliente: {e}")
    finally:
        client_socket.close()
        print("Conexão com o cliente encerrada.")

def inicia_servidor(): 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 5555)) 
    server.listen(5) 
    print("Servidor iniciado. Aguardando conexões...")

    while True:
        client_socket, addr = server.accept()
        print(f"Cliente conectado: {addr}")
        threading.Thread(target=gerencia_cliente, args=(client_socket,)).start() 

inicia_servidor()