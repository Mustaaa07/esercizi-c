SERVER
# Importiamo le librerie necessarie
import socket      # Per la comunicazione client-server
import json        # Per inviare/ricevere dati in formato JSON
# Indirizzo IP del server
HOST = '127.0.0.1'
# Porta di comunicazione
PORT = 5000
# Dizionario contenente i prodotti del negozio
prodotti = {
    "Mouse": {"prezzo": 25, "quantita": 10},
    "Tastiera": {"prezzo": 45, "quantita": 5},
    "Monitor": {"prezzo": 150, "quantita": 3}
}
# Soglia minima per ottenere lo sconto
SOGLIA_SCONTO = 100
# Percentuale di sconto (10%)
SCONTO = 0.10
# Creazione del socket TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Collega il server all'indirizzo e porta scelti
server.bind((HOST, PORT))
# Il server resta in ascolto delle connessioni
server.listen()
print(f"Server avviato su {HOST}:{PORT}")
# Ciclo infinito: il server resta sempre acceso
while True:
    # Accetta una connessione dal client
    conn, addr = server.accept()
    print(f"Client collegato: {addr}")
    # Invia il catalogo prodotti al client
    conn.send(json.dumps(prodotti).encode())
    # Riceve l'ordine del client
    dati = conn.recv(4096).decode()
    # Converte il JSON ricevuto in dizionario Python
    ordine = json.loads(dati)
    # Variabile per il totale dell'ordine
    totale = 0
    # Lista che conterrà il dettaglio dell'ordine
    dettaglio = []
    # Analizza ogni prodotto ordinato
    for nome, quantita in ordine.items():
        # Controlla se il prodotto esiste
        if nome in prodotti:
            # Quantità disponibile in magazzino
            disponibile = prodotti[nome]["quantita"]

            # Controlla se il magazzino ha abbastanza pezzi
            if quantita <= disponibile:
                # Prezzo del prodotto
                prezzo = prodotti[nome]["prezzo"]
                # Calcolo subtotale
                subtotale = prezzo * quantita
                # Aggiorna il totale
                totale += subtotale
                # Aggiorna lo stock del magazzino
                prodotti[nome]["quantita"] -= quantita
                # Aggiunge una riga al dettaglio ordine
                dettaglio.append(
                    f"{nome} x{quantita} = {subtotale}€"
                )
            else:
                # Messaggio se il prodotto non è disponibile
                dettaglio.append(
                    f"{nome}: quantità non disponibile"
                )
    # Variabile per lo sconto applicato
    sconto_applicato = 0
    # Controlla se il totale supera la soglia
    if totale > SOGLIA_SCONTO:
        # Calcola lo sconto
        sconto_applicato = totale * SCONTO
        # Sottrae lo sconto dal totale
        totale -= sconto_applicato
    # Dizionario risposta da inviare al client
    risposta = {
        "dettaglio": dettaglio,
        "sconto": sconto_applicato,
        "totale": totale,
        "stock_aggiornato": prodotti
    }
    # Invia la risposta al client
    conn.send(json.dumps(risposta).encode())
    # Chiude la connessione con il client
    conn.close()

CLIENT
# Importiamo le librerie necessarie
import socket
import json
# Indirizzo del server
HOST = '127.0.0.1'
# Porta del server
PORT = 5000
# Creazione del socket client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connessione al server
client.connect((HOST, PORT))
# Riceve il catalogo prodotti dal server
catalogo = json.loads(client.recv(4096).decode())
print("=== CATALOGO PRODOTTI ===")
# Mostra i prodotti disponibili
for nome, info in catalogo.items():
    print(
        f"{nome} - "
        f"{info['prezzo']}€ - "
        f"Disponibili: {info['quantita']}"
    )
# Dizionario che conterrà l'ordine del cliente
ordine = {}
# Inserimento prodotti
while True:
    # Chiede il nome del prodotto
    prodotto = input(
        "\nInserisci prodotto (fine per terminare): "
    )
    # Esce dal ciclo
    if prodotto.lower() == "fine":
        break
    # Controlla se il prodotto esiste
    if prodotto not in catalogo:
        print("Prodotto inesistente")
        continue
    # Chiede la quantità
    quantita = int(input("Quantità: "))
    # Salva il prodotto nell'ordine
    ordine[prodotto] = quantita
# Invia l'ordine al server
client.send(json.dumps(ordine).encode())
# Riceve il risultato dell'ordine
risposta = json.loads(client.recv(4096).decode())
print("\n=== DETTAGLIO ORDINE ===")
# Mostra il dettaglio dei prodotti acquistati
for riga in risposta["dettaglio"]:
    print(riga)
# Mostra lo sconto applicato
print(f"\nSconto applicato: {risposta['sconto']}€")
# Mostra il totale finale
print(f"Totale finale: {risposta['totale']}€")
print("\n=== STOCK AGGIORNATO ===")
# Mostra il nuovo stock disponibile
for nome, info in risposta["stock_aggiornato"].items():
    print(f"{nome}: {info['quantita']} disponibili")
# Chiude la connessione
client.close()
