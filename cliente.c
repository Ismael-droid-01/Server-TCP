#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <unistd.h>

#define SERVER_PORT 1234 /* arbitrario, pero el cliente y el servidor deben coincidir */
#define BUF_SIZE 4096 /* tamaño de bloque para transferencia */

void fatal(char *string)
{
printf("%s\n", string);
exit(1);
}

int main(int argc, char **argv)
{
int c, s, bytes;
char buf[BUF_SIZE];         /* búfer para el archivo entrante */
struct hostent *h;          /* información sobre el servidor */
struct sockaddr_in channel; /* contiene la dirección IP */

if (argc != 3) fatal("Usage: client server-name file-name");
h = gethostbyname(argv[1]); /* busca la dirección IP del host */
if (!h) fatal("gethostbyname failed");

s = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);
if (s < 0) fatal("socket");

memset(&channel, 0, sizeof(channel));
channel.sin_family= AF_INET;
memcpy(&channel.sin_addr.s_addr, h->h_addr, h->h_length);
channel.sin_port= htons(SERVER_PORT);
c = connect(s, (struct sockaddr *) &channel, sizeof(channel));
if (c < 0) fatal("connect failed");

/* Se ha establecido la conexión. Se envía el nombre del archivo incluyendo el byte 0 al final. */
write(s, argv[2], strlen(argv[2])+1);
/* Obtiene el archivo y lo escribe en la salida estándar. */
while (1) {
bytes = read(s, buf, BUF_SIZE); /* lee del socket */
if (bytes <= 0) exit(0); /* verifica el final del archivo */
write(1, buf, bytes); /* escribe en la salida estándar */
}
}
