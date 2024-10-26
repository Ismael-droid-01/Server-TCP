import socket
import os

SERVER_PORT = 1234 # Puerto en el que el servidor escuchara
BUFFER_SIZE = 4096 # Tamano del buffer para la transferencia

def main():
    # Crear un socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Enlazar el socket al puerto
    server_socket.bind(('0.0.0.0', SERVER_PORT))

    # Escuchar conexiones entrantes
    server_socket.listen(3)
    print(f"Servidor escuchando en el puerto {SERVER_PORT}...")

    while True:
        # Aceptar una conexion
        client_socket, addr = server_socket.accept()
        print(f"Conexion aceptada de {addr}")

        # Leer el nombre del archivo solicitado
        file_name = client_socket.recv(BUFFER_SIZE).decode()
        print(f"Solicitando archivo: {file_name}")

        if os.path.isfile(file_name): # Verificar si el archivo existe
            with open(file_name, 'rb') as file:
                while True:
                    # Leer el archivo y enviar al cliente
                    data = file.read(BUFFER_SIZE)
                    if not data:
                        break
                    client_socket.send(data)
            print("Archivo enviado exitosamente")
        else:
            print("El archivo no existe")

        client_socket.close() # Cerrar la conexio con el cliente

if __name__ == "__main__":
    main()
