# AlphaBot_n_Flask


## Funzione Login
Questa funzione preleva i valori dai campi "Username" e "Passsword" e controlla se c'è un'associazione nel DataBase, se l'esito è positivo ci renderizza alla funzione "Control" e alla corrispettiva pagina.

## Funzione Control:
Gestisce se i tasti con i movimenti vengono premuti o se viene inserita una sequenza. 
Se viene inserita una sequenza viene chiamata la funzione "Runcommand".

## Funzione Runcommand:
Si esegue una query sul DataBase ricercando la sequenza richiesta. Una volta ottenuta divide la sequenza e chiama la funzione per ogni movimento base dicendo anche la durata in secondi.

## Funzione dbAccess
Connette il database e avvia il cursore, ed esegue la query che inserisce nella tabella accesses il nome dell'utente che ha effettuate l'accesso e la data nel quale il tutto è avventuo.

## Funzione dbActions
Connette il database e avvia il cursore, ed esegue la query che inserisce nella tabella actions il nome dell'utente che ha eseguito un'azione e la data nel quale il tutto è avventuo.

## Funzione check_password
Controlla che la password inserita sia presente nel database.

## Funzione validate
Connette il database e avvia il cursore, ed esegue la query che seleziona tutta la tabella user per poi ricercare utente e password inseriti.
