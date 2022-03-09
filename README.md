# AlphaBot_n_Flask


## Funzione Login
Questa funzione prende i valori dai campi "Username" e "Passsword" e controlla se c'è un'associazione nel DataBase, se l'esito è positivo ci renderizza alla funzione "Control".

## Funzione Control:
Gestisce se i tasti con i movimenti vengono premuti o se viene inserito una sequenza. 
Se viene inserito una sequenza viene chiamata la funzione "Runcommand".

## Funzione Runcommand:
Si esegue una query sul DataBase ricercando la sequenza richiesta. Una volta ottenuta dividere la sequenza e chiamare la funzione per ogni movimento base dicendo anche la durata in secondi.

## Funzione dbAccess
Connette il database e avvia il cursore, ed esegue la query che inserisce nel database la data di adesso

## Funzione dbActions
Connette il database e avvia il cursore, ed esegue la query che inserisce nella tabella actions l'utente, l'azione e la data di adesso

## Funzione check_password
Controlla che la password inserita sia corretta

## Funzione validate

Connette il database e avvia il cursore, ed esegue la query che seleziona tutto dalla tabella user poi cicla tutte le password per cercarne una che corrisponda
