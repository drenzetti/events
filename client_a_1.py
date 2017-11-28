import requests

BASE_URL = 'http://localhost:5000/events/'

MAIN_TEXT = """-----------------------------------------
 Digita:
 - 1 per inserire un evento
 - 2 per visualizzare tutti gli eventi
 - 3 per modificare un evento
 - 4 per eliminare un evento
"""

def display():
    print(requests.get(BASE_URL).json())

def insert():
    title = input('Inserisci il titolo (Invio per tornare al menu principale): ')
    if not title.strip():
        return

    desc = input('Inserisci la descrizione (Invio per tornare al menu principale): ')
    if not desc.strip():
        return

    date = input('Inserisci la data in formato ISO (Invio per tornare al menu principale): ')
    if not date.strip():
        return

    resp = requests.post(BASE_URL, data={
        'title': title,
        'desc': desc,
        'date': date
    })

    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError:
        print('Inserimento fallito!')
    else:
        print('Inserimento effettuato con successo!')

def update():
    id = input('Inserisci l\'id dell\'evento da modificare (Invio per tornare al menu principale): ')
    if not id.strip():
        return

    title = input('Inserisci il nuovo titolo (Invio per tornare al menu principale): ')
    if not title.strip():
        return

    desc = input('Inserisci la nuova descrizione (Invio per tornare al menu principale): ')
    if not desc.strip():
        return

    date = input('Inserisci la nuova data in formato ISO (Invio per tornare al menu principale): ')
    if not date.strip():
        return

    resp = requests.put(BASE_URL + id, data={
        'title': title,
        'description': desc,
        'date': date
    })

    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError:
        print('Modifica fallita!')
    else:
        print('Modifica effettuata con successo!')

def delete():
    id = input('Inserisci l\'id dell\'evento da eliminare (Invio per tornare al menu principale): ')
    if not id.strip():
        return

    resp = requests.delete(BASE_URL + id)

    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError:
        print('Cancellazione fallita!')
    else:
        print('Cancellazione effettuata con successo!')

def main():
    commands = {
        '1': insert,
        '2': display,
        '3': update,
        '4': delete
    }

    while True:
        print(MAIN_TEXT)
        cmd = input('Comando (Invio per terminare): ')
        if not cmd:
            return
        elif cmd in commands:
            commands[cmd]()
        else:
            print('Comando sconosciuto!')


if __name__ == '__main__':
    main()
