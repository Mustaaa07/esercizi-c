//SERVER
import socket  # modulo per usare le socket di rete

# Indirizzo IP del server
# 0.0.0.0 = accetta connessioni da qualsiasi interfaccia di rete
HOST = '0.0.0.0'

# Porta su cui il server ascolta
PORT = 5000

# Crea una socket TCP/IP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Collega la socket all'indirizzo e porta scelti
server.bind((HOST, PORT))

# Mette il server in ascolto di connessioni
server.listen()

print(f"Server in ascolto su {HOST}:{PORT}")

# Aspetta che un client si connetta
# accept() restituisce:
# - conn = connessione col client
# - addr = indirizzo del client
conn, addr = server.accept()

print(f"Connesso da {addr}")

# Ciclo infinito per ricevere messaggi
while True:

    # Riceve fino a 1024 byte
    data = conn.recv(1024)

    # Se non arriva nulla, il client si è disconnesso
    if not data:
        break

    # Converte i byte ricevuti in stringa
    messaggio = data.decode()

    print("Client:", messaggio)

    # Crea una risposta
    risposta = f"Hai scritto: {messaggio}"

    # Invia la risposta al client
    conn.send(risposta.encode())

# Chiude la connessione col client
conn.close()

# Chiude il server
server.close()


//CLIENT
import socket  # modulo per le socket

# IP del server
# 127.0.0.1 = localhost (stesso PC)
HOST = '127.0.0.1'

# Porta del server
PORT = 5000

# Crea una socket TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Si connette al server
client.connect((HOST, PORT))

# Ciclo per inviare messaggi
while True:

    # Chiede un messaggio all'utente
    messaggio = input("Scrivi: ")

    # Se l'utente scrive exit termina il programma
    if messaggio.lower() == "exit":
        break

    # Converte la stringa in byte e la invia
    client.send(messaggio.encode())

    # Riceve la risposta del server
    risposta = client.recv(1024).decode()

    print("Server:", risposta)

# Chiude la connessione
client.close()
