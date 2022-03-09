# AlphaBot_n_Flask


## Funzione Login
Questa funzione prende i valori dai campi "Username" e "Passsword" e controlla se c'è un'associazione nel DataBase, se l'esito è positivo ci renderizza alla funzione "Control".

## Funzione Control:
Gestisce se i tasti con i movimenti vengono premuti o se viene inserito una sequenza. 
Se viene inserito una sequenza viene chiamata la funzione "Runcommand".

## Funzione Runcommand:
Si esegue una query sul DataBase ricercando la sequenza richiesta. Una volta ottenuta dividere la sequenza e chiamare la funzione per ogni movimento base dicendo anche la durata in secondi.
