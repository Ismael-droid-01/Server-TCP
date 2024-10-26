import socket
import sys

SERVER_IP = '192.168.122.173' # Direccion IP del servidor
SERVER_PORT = 1234  # Puerto en el que el servidor esta escuchando
BUFFER_SIZE = 4096  # Tamano del buffer para la transferencia

def main():
    # Crear el socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conectar al servidor
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
    except Exception as e:
        print(f"Error al conectar al servidor {e}")
        sys.exit(1)

    # Obtener el nombre del archivo desde la linea de comandos
    if len(sys.argv) != 2:
        print("Uso: python3 cliente.py <nombre_del_archivo>")
        sys.exit(1)

    file_name = sys.argv[1]

    # Enviar el nombre del archivo al servidor
    client_socket.send(file_name.encode())

    # Recibir el contenido del archivo
    with open('recibido_' + file_name, 'wb') as f:
        while True:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break
            f.write(data)

    print(f"Archivo recibido: recibido_{file_name}")

    # Cerrar el socket
    client_socket.close()

if __name__ == "__main__":
    main()
