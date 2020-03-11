# Documentazione Wordnet manager

##  Wordnet
Una api che permette di gestire WordNet da linea di comando. Il core di WordNet è in lingua inglese e distribuito su vari file chiamati dbfiles. I più importanti di questi sono:
- data.noun
- data.verb
- data.adv
- data.adj
- index.noun
- index.verb
- index.adv
- index.adj

I file `index.pos` contengono la lista delle parole del relativo *pos*. I file  `data.pos` contengono invece tutti i synset del relativo *pos*.  

Le estensioni delle varie lingue consistono in un file unico della forma `wb-data-lan.tab` dove *lan* è un codice a 3 lettere che indica la lingua. Nel nostro caso useremo solo l'italiano il cui codice è `ita`. Questo file è una lista di parole in cui per ogni parola c'è un collegamento a un synset del core di WordNet. 

Nella cartella `wordnet` ci sono altri 2 file non correlati col wordnet originale:
- `sense_disambiguation.json`: un dizionario di (parole - numero) che indica qual'è l'indice del senso corretto della lista di sensi collegati con essa. Se alla parola viene assegnato l'indice -1 allora il tagger la ignorerà. 
- `wordnet_additions.py`: uno storico di tutte le aggiunte eseguite. Basta importarlo da console con un wordnet originale per eseguire tutte le aggiunte.
  
### Data.*pos*

Ogni riga di questo file contiene un synset. Ogni synset ha il seguente formato:

13444578 22 n 01 ablactation 0 001 @ 13461236 n 0000 | the cessation of lactation  

Partendo da sinistra:
- **13444578**: l'*offset*, un numero decimale a 8 cifre 0-filled che rappresenta il byte offset rispetto all'inizio del file fino a questo synset. 
- **22**: il *lex_filenum*, il numero del lexicographic file da cui è stato letto questo synset.
- **n**: *ss_type*, il tipo di synset:
    -	n NOUN
    -	v VERB
    -	a ADJECTIVE
    -	s ADJECTIVE SATELLITE
    -	r ADVERB
- **01**: *w_cnt*, numero esadecimale di due cifre che indica il numero di parole che contiene il synset. 
- **ablactation**: *word*, la parola
- **0**:  *lex_id*, una cifra esadecimale che quando unita al lemma identifica 
  univocamente il senso all’interno del lexicographic file. Questo numero inizia con 0 e aumenta man mano che si aggiungono sensi con la stessa parola nello stesso file. Lo 0 è omesso nei lexicographic files. 

La coppia [*word* *lex_id*] si ripete per ogni parola del synset.

- **001**: *p_cnt*, numero a tre cifre 0-filled che indica quanti puntatori ci sono da questo synset ad altri. 
- **pointers**: uno o più puntatori a un altro synset, i puntatori hanno la forma seguente:
    -	**@**: *pointer_symbol*, il simbolo che indica che tipo di relazione con l’altro synset.
    -	**13461236**: *synset_offset* l’offset dell’altro synset nel file inidicato da pos.
    -	**n**: *pos*
    -	**0000**: *source/target*. Serve per distinguere puntatori semantici da puntatori sintattici. Un campo da 4 byte contenente 2 numeri esadecimali da 2 cifre. Le prime due cifre indicano la parola nel synset corrente (source), le ultime due indicano la parola nel synset puntato (target). Se è 0000 vuol dire che il puntatore è semantico. Noi aggiungeremo solo puntatori semantici  

Solo per i synset in `data.verb`, dopo i puntatori c'è una lista di *frames*, i quali hanno il seguente formato:
- **f_cnt**: numero decimale a due cifre 0-filled che indica il numero di frames. 
- **[f_num w_num]**: *f_num* è un numero decimale a due cifre  che indica il frame e *w_num* è un numero esadecimale a due cifre che indica la parola a cui si applica il frame. 

 Dopo la ‘|’ inizia il *gloss*, ovvero la definizione e qualche esempio, se presenti, separati da “;”. 

### Index.*pos*

Ogni linea di questo file contiene un lemma, ovvero la forma scritta di una parola. Ogni linea è nel seguente formato:

ablactation n 2 1 @ 2 0 13444578 00199119  

Partendo da sinistra:
- **ablactation**: il *lemma*, in lowercase. Nel ci siano più parole, le si uniscono con un underscore "_". 
- **n**: il *pos*.
- **2**: il *synset_cnt*, un contatore che indica in quanti synset è presente il lemma. 
- **1**: il *p_cnt*, il numero di diversi puntatori che ha il lemma in tutti i synset che lo contengono. 
- **@**:  una lista di diversi puntatori, lunga p_cnt, che ha il lemma in tutti i synset che lo contengono.
- **2**: *sense_cnt*, il numero di sensi legati al lemma. Uguale a synset_cnt (1 synset=1 senso), è stato lasciato per ragioni di compatibilità 
- **13444578** e **00199119** : *synset_offset*, il byte offset nel relativo file data.pos corrispondente al synset che contiene il lemma. Tanti quanto synset_cnt. 

### File di estensione di una lingua

Ogni linea contiene una parola e il riferimento a un synset. Ogni elemento della linea è separato da un *tab*. 

00198270-n	ita:lemma	divezzamento

- **00198270**: l’offset del synset a cui la parola è collegato rispetto all’inizo del relativo file data.pos.
- **n**: pos
- **ita**: lingua
- **lemma**: tipo di entità aggiunta. Nel 99% dei casi è un lemma ma può anche essere un esempio (exe) o definizione (def). 
- **divezzamento**: la parola

## Struttura

`wnmanager` è un modulo python che contiene altri 3 moduli distinti. 

### Modulo: Manager
E' il modulo che contiene il manager di wordnet. Ha il compito di caricare in memoria tutto wordnet, eseguire le operazioni su di esso, fornire i dati ad altri moduli, e scrivere su file tutte le modifiche eseguite. 
Il file più importante è `manager.py` che contiene la classe `WordnetManager`

#### WordnetManager
Questa è la classe tramite da caricare per gestire WordNet e le estensioni in altre lingue. Prende come parametri il path della cartella dentro cui ci sono i dbfiles e il path del file della lingua di cui si vuole usare l'estensione. Di default questi parametri indicano la cartella `wordnet` all'interno del progetto, nella quale c'è anche il file di estensione dell'italiano. 

I metodi principali di questa classe sono i seguenti:
- `open()`
- `add_word(word, pos, offset, lang='eng')`
- `add_synset(ss_type, words, pointers = [], gloss = '', frames = [])`

### Inizializzazione

Per inizializzare la classe, eseguire i seguenti passaggi:
- aprire il terminale di python. Guardare il file `readme.md` per le istruzioni sull'attivazione del virtual environment e l'avvio del terminale. 
- importare il modulo:
  - `from wordnet_manager import *`
- inizializzare la classe e assegnarla a una variabile:
  - `wm = WordnetManager()`
- caricare tutti i dati in ram:
  - `wm.open()` 

La funzione `open()` legge tutti i dbfiles nella cartella e li carica in appositi dizionari, accessibili da terminale. Le informazioni di ogni synset e lemma vengono immagazzinate in apposite clasi. Anche tutte le parole del file di estensione della lingua vengono caricate. Le classi utilizzate per immagazzinare le varie entry sono:
- DataEntry: per i synset
- IndexEntry: per i lemmi
- LangEntry: per i lemmi del file di estensione

### Aggiunta di una parola (da conosole)

Il metodo add_word è incaricato di aggiungere una parola a WordNet. Per farlo bisogna indicare:
- `word` (str): la parola 
- `pos` (str): il pos della parola
- `offset` (int): l'offset del synset al quale collegare  la parola. Non ha senso aggiungere una parola ma non collegarla a nessun synset.

Con questi 3 parametri, WordnetManager esegue i seguenti passaggi:
- crea un nuovo IndexEntry. Se la parola esiste già, aggiunge l'offset alla sua lista di offsets. 
- aggiunge la parola al synset
- ricalcola tutti gli offset dei synset con lo stesso pos
- modifica tutte le reference agli offset ricalcolati
- riscrive sui file tutte le modifiche apportate

Se viene anche definito il parametro `lang`, allora creerà solo una nuova LangEntry con riferimento all'offset e pos specificato. 

### Aggiunta di un synset (da console)

Il metodo add_synset è incaricato di aggiungere un nuovo synset. Per farlo bisogna indicare:
- `ss_type`: il tipo di synset. All'interno della class esiste un dizionario che lo convertirà nel pos corretto.
- `words`: una lista di parole da aggiungere al synset, ce ne deve essere almeno una in quanto un synset non può essere vuoto. 
- `pointers`: eventuali puntatori ad altri synset 
- `gloss`: eventuali definizioni ed esempi separati da ';'
- `frames`: eventuali frames, nel caso ss_type == v

Successivamente il metodo eseguirà i seguenti passaggi:
- crea una nuova DataEntry senza parole e con i pointers, frames e gloss indicati.
- Per ogni pointer presente, aggiungerà un pointer opposto al synset indicato, aggiornando anche i pointers delle IndexEntry relative alle parole contenute nel synset
- Per ogni parola indicata, richiamerà il metodo add_words
- Ricalcola gli offset di tutti synset per via dei pointers aggiunti
- Riscrive i cambiamenti su file

### Modulo: app

E' modulo contiene un interfaccia grafica per il modulo manager. Permette di svolgere tutte le operazioni di WordnetManager da interfaccia grafica. Genera un log. 

### Script: tagger.py

E' l'implementazione di un tagger che utilizza WordnetManager per ottenere i sensi per ogni lemma. Permette di taggare un testo sostituendo per ogni parola il nome del suo senso.  

## Glossario
- **synset**: un insieme di parole caratterizzate dallo stesso significato 
- **lemma**: la forma scritta di una parola
- **pos**: part of speech. Un "codice" che indica se una parola è un nome, aggettivo, verbio o avverbio. 
- **lexicographic files**: i file di origine di wordnet. Sono file, con una sintassi indipendente, scritti a mano dai linguisti, in cui vengono definiti i sensi e le parole. L'api di wordnet ha un comando chiamato *grind* che converte questi file nei dbfiles descritti. 
- **frames**: I frame sono delle frasi generiche già costruite in cui si possono inserire i verbi per creare degli esempi. I frame sono specificati in un file fra i *lexicographic files*. 