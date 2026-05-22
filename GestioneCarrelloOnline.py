SERVER
# Importa il modulo socket
# Serve per la comunicazione in rete
import socket

# Importa threading
# Serve per gestire più client contemporaneamente
import threading

# Indirizzo IP del server
# 0.0.0.0 = accetta connessioni da tutti
HOST = '0.0.0.0'

# Porta del server
PORT = 5000

# Dizionario prodotti
# Formato:
# nome : [prezzo, quantità]
prodotti = {
    "mouse": [25, 10],
    "tastiera": [45, 5],
    "monitor": [150, 3]
}

# Funzione che gestisce un client
def gestisci_client(conn, addr):

    # Stampa il client collegato
    print(f"Client connesso: {addr}")

    # Stringa che conterrà il catalogo
    catalogo = ""

    # Scorre tutti i prodotti
    for nome, info in prodotti.items():

        # Prezzo del prodotto
        prezzo = info[0]

        # Quantità disponibile
        quantita = info[1]

        # Aggiunge il prodotto al catalogo
        catalogo += (
            f"{nome} - "
            f"{prezzo}€ - "
            f"disponibili: {quantita}\n"
        )

    # Invia il catalogo al client
    conn.send(catalogo.encode())

    # Riceve i dati dal client
    dati = conn.recv(1024).decode()

    # Divide il messaggio usando la virgola
    # esempio:
    # mouse,2
    parti = dati.split(",")

    # Nome prodotto
    nome = parti[0]

    # Quantità richiesta
    quantita = int(parti[1])

    # Controlla se il prodotto esiste
    if nome in prodotti:

        # Prezzo prodotto
        prezzo = prodotti[nome][0]

        # Quantità disponibile
        disponibili = prodotti[nome][1]

        # Controlla disponibilità
        if quantita <= disponibili:

            # Calcola il totale
            totale = prezzo * quantita

            # Applica sconto del 10%
            # se il totale supera 100€
            if totale > 100:

                totale = totale - (totale * 0.10)

            # Aggiorna il magazzino
            prodotti[nome][1] -= quantita

            # Messaggio finale
            risposta = (
                f"Ordine confermato\n"
                f"Prodotto: {nome}\n"
                f"Quantità: {quantita}\n"
                f"Totale: {totale}€"
            )

        else:
            # Se non ci sono abbastanza prodotti
            risposta = "Quantità non disponibile"

    else:
        # Se il prodotto non esiste
        risposta = "Prodotto inesistente"

    # Invia la risposta al client
    conn.send(risposta.encode())

    # Chiude la connessione col client
    conn.close()


# Creazione socket TCP
server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

# Collega server a IP e porta
server.bind((HOST, PORT))

# Mette il server in ascolto
server.listen()

print(f"Server avviato su {HOST}:{PORT}")

# Ciclo infinito
while True:

    # Accetta una connessione
    conn, addr = server.accept()

    # Crea un thread per il client
    thread = threading.Thread(

        # Funzione da eseguire
        target=gestisci_client,

        # Parametri della funzione
        args=(conn, addr)
    )

    # Avvia il thread
    thread.start()
CLIENT
# Importa socket
# Serve per comunicare col server
import socket

# IP del server
# 127.0.0.1 = stesso computer
HOST = '127.0.0.1'

# Porta del server
PORT = 5000

# Crea socket TCP
client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

# Connessione al server
client.connect((HOST, PORT))

# Riceve il catalogo dal server
catalogo = client.recv(1024).decode()

print("=== CATALOGO ===")

# Stampa catalogo
print(catalogo)

# Chiede il prodotto
prodotto = input("Prodotto: ")

# Chiede quantità
quantita = input("Quantità: ")

# Crea messaggio
# esempio:
# mouse,2
messaggio = prodotto + "," + quantita

# Invia messaggio al server
client.send(messaggio.encode())

# Riceve risposta server
risposta = client.recv(1024).decode()

print("\n=== RISPOSTA SERVER ===")

# Stampa risposta
print(risposta)

# Chiude connessione
client.close()
