# Elaborato back-end 2024

# Full Website E-commerce Store di abbigliamento con Django.

## Tecnologie utilizzate

Framework back-end: Django
Front-end: HTML, CSS , JS, JQuery, Bootstrap e AJAX

## Idea

Il sito prevede due tipi di utenti: il cliente e il venditore. Quest'ultimo è anche l'amministatore del suo stesso sito.
Quindi le schermate e funzionalità (cliente e admin) sono sviluppate ad hoc per i rispettivi ruoli che ricoprono.

Il pannello di admin è stato modificato per consentire al venditore di esercitare il suo ruolo, avendo anche dei poteri da superuser.
Se un admin (venditore) non può fare certe azioni, verrà bloccato dal pannello di admin.

Il sito è sviluppato con 3 applicazioni: order, store e accounts. Order si occupa della gestione del carrelo. Store si occupa della gestione dei prodotti e di come visualizzarli, soprattuto dal lato client. Accounts si occupa della gestione degli utenti e di tutte le azioni ad esso collegate.

Tutti i valori sensibili NON sono trasmessi in chiaro, ma tramite variabili ambientali.

Il sito è pensato per utenti registrati al sito, che hanno più benefici riguardanti la gestione degli ordini o degli indirizzi per una maggiore comodità. Inoltre è pensato anche per utenti ospiti che non possiedono (e non intendono averlo) un account.



## Modelli

Il database è Postgresql offerto da Railway. I file statici (CSS,JS e media) sono salvati su un web server Amazon AWS, ma per backup sono tenuti anche nella repository remota.

I modelli sono riempiti con prodotti di fantasia basati su aziende reali utilizzati solamente a scopo didattico senza alcun fine economico. Le immagini sono generate con AI.

### Store

I modelli dell'app Store sono:

- Category: per la categoria del prodotto
- Color: per il colore del prodotto
- Size: per la taglia del prodotto
- Image: per l'immagine del prodotto
- Product: per il prodotto (modello), senza considerare la taglia o il colore
- ProductVariant: rappresenta la variante del prodotto, ovvero quella usata nello shop. Una variante è compresa anche di campi come "color" e "size" perché degli articoli posso avere diverse varianti di colore e/o di taglia. Infatti l'attrivuto "variant" serve per precisarlo.
- Brand: per la marca del prodotto

Tutti quesit modelli sono sollegati tra loro tramite chiavi esterne. Il modello principale su cui vengono fatte le query è ProductVariant. Gli altri sono di supporto per facilitare la gestione del database.

### Order

I modelli dell'app Order sono:

- Cart: per il carrelo. Ogni utente può avere solamente un carrello.
- CartItem: rappresenta un elemento del carrelo, infatti ha un ProductVariant come chiave esterna ed un attributo "quantity" per indicare la quantità aggiunta al carrello della SOLITA variante.
- Order: per l'ordine. I dati di un ordine vengono salvati come testo per non avere dipendenze da altri modelli (soprattutto in caso di eliminazione). Ogni utente può avere più ordini.
- OrderItem: per un elemento dell'ordine. Stesso concetto di CartItem ma per l'ordine.

### Accounts

I modelli dell'app Accounts sono:

- CustomUser: è un'estenzione del modello utente integrato di Django
- Address: rappresenta un indirizzo. Perché gli utenti possono salvare degli indirizzi nel proprio account così da fare un checkout molto rapido, selezionando uno di quelli salvati.

## Organizzazione Store

La home del sito mostra gli ultimi 6 arrivi nella sollezione, può mostrare anche stessi prodotti ma di colore diverso.

In alto a sinistra si trovano i generi sulla quale è possibile cliccare per iniziare la navigazione. Altrimenti è possibile utilizzare la barra di ricerca, che fa una ricerca tu tutti i parametri testuali relativi ad prodotto.

In alto a destra si trovano i pulsanti di accesso/registrazione e il carrello.

### Navigazione

Dopo aver cliccato su un genere, si apre lo store dalla quale è possible selezionare un'ulteriore categoria, oppure filtrare i risultati (anche combinandoli)

I risultati mostrati nelle categorie Man e Woman mostrano anche prodotti Unisex. Vengono mostrati solamente i prodotti disponibili (in stock)

Una volta scelto un prodotto è possible visualizzare i suoi dettagli scegliendo taglia e/o colore (se permesso). Vengono mostrati (e aggiornati) tutti i colori e taglie disopnibili per un determinato prodotto in tempo reale, grazie ad AJAX, permettendo di non ricaricare la pagina.

Le taglie non disponibili (ma esistenti) vengano oscurate. La dipendenza di scelta è pensata per scegliere prima il colore e poi la taglia (non viceversa).

Una volta scelte le opzioni è possibile aggiunere un prodotto al carrello, che tramite AJAX ci informa istanzaneamente della risposta del server attraverso un messaggio (di successo o di errore).



### Carrello

Il carrello, uno per utente, viene aggiornato in tempo reale ad ogni aggiunta/rimozione di un prodotto.

Anche gli utenti non registrati hanno un carrello, ma se perdono la sessione perderanno anche il carrello. Ma se intendono registrarsi (con il carrello pieno) prima del pagamento, il carrello da utente ospite sarà trasferito al loro nuovo account.


### Forms e checkout

Ogni tipo di form è provvisto di una validazione preliminare lato client e una lato server, per garantire una migliore esperienza utente. Nei form di registrazione (o modifica mail/username), i campi di email e username vengono validati con il server per vedere se ci sono altri cmapi uguali a quello. Questo perché email e password devono essere unici. La verifica "interattiva" viene fatta tramite AJAX.

Il pagamento non è provvisto di un sistema bancario, quindi basterà selezionare il metodo di pagamento ed verrà considerato come "eseguito con successo" in ogni caso. Viene verificato solamente che sia selezionato. I dati di pagamento non vengono chiesti perché si presume che vengano inseriti su ipotetici servizi di terzi.

ATTENZIONE: quando si effettua un ordine inserire una mail reale perché viene inviata una mail di conferma contentente il riepilogo

Quindi se l'oridne viene effettuato come ospite, non vi è alcuna verifica dell'esistenza sul database perché gli ordini ospiti posso avere anche la stessa mail e l'email associata all'ordine è quella inserita in fase di checkout.
Invece se si effettua un ordine con un account usando un indirizzo salvato, la mail associata all'ordine è quella associata all'account.

In tutti i form vi è una verifica (sia client-side, sia server-side) riguardante i caratteri utilizzati per un determinato campo. Ad esempio la password deve avere almeno 8 caratteri con almeno una lettera maiuscola, minuscola e un numero (ad accezione dell'admin).

Tutti i campi tranne username, password ed email non hanno validazioni particolari. Viene controllato solamente che venganon inseriti (se obbligatori).


## Admin

L'admin, ovvero il venditore (in questo caso), ha accesso all'aggiunta, modifica e rimozione di prodotti e modelli ad esso collegati (come taglie, categorie ecc...)

Inoltre può vedere gli ordini effettuati (da tutti gli utenti, ospiti e non) con una vista panoramica in modo tale da poter evadere più ordini possibile. Quando un ordine cambia stato, il venditore può modificare lo stato di un ordine in modo tale che possa essere visto anche dal cliente.

In aggiunta, ha accesso (più limitato) anche ai modelli di Address e User, in modo da garantire la sicurezza dei clienti. Però ha anche dei poteri da admin, infatti può modificare anche qualche campo "manualmente", ad esempio se viene chiesto da un cliente tramite un ipotetico servizio clienti.


Il pannello di controllo admin è accessibile dal seguente link -> https://elaborato-backend.onrender.com/admin/

## Sicurezza

Gli id di prodotti o indirizzi vengono crittografati tramite hash se vengono mostrati nell'url. Ovviamente nessun dato sensibile viene passato in chiaro.

Le chaivi per le impostazioni di Django e variabili che mettonon a rischio la sicurezza non sono mai visibili in chiaro.

Nella schermata di log-in è possibile spuntare "Remember me" per allungare di molto la sessione.


## Credenziali di prova
Qui ci sono alcune credenziali di tutte le tipologie di utenti. Le credenziali sottostanti sono rilasciate (in chiaro) per facilitare la revisione.
Il cliente ha già dei dati caricati al suo interno.

Admin ->

username: admin
password: admin

Utente (cliente) di prova ->

username: mariorossi1
password: Ciaociao1



Developed by Alberto Pizzi

