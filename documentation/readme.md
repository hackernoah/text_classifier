# Progetto di ricerca CANP (AI su GRC)

## Contenuti

### **Datasets**

#### LDC

Il file excel `LDC.xlsx` contiene 7688 eventi di perdita provenienti da 6 banche diverse. Il file contiene 2 fogli:
- **LDC:** contiene tutti gli eventi di perdita
- **EType:** contiene la tabella di equivalenza fra le diverse tassonomie specifiche delle società, e la tassonomia GOLD generale per tutte. 

##### Foglio LDC
E' composto da 8 colonne il cui significato è il seguente (in ordine crescente delle colonne)
-  **Società**: la banca a cui appartiene l'evento di perdita.
-  **Description**: La descrizione in linguaggio naturale dell'evento di perdita.
-  **ETX**: L'event type del livello X, appartenente alla tassonomia specifica della società, con cui è stato categorizzato l'evento di perdita.
-  **Gold_ETX**: L'event type di livello X, appartenente alla tassonomia GOLD, a cui l'even type in ETX corrisponde nella tabella di equivalenza fra le tassonomie (se esiste una corrispondenza). 

##### Foglio EType
Contiene 7 colonne, 1 per ogni banca e 1 per la tassonomia GOLD. 
Ogni colonna di ogni banca contiene tutti gli event type riconducibili alla tassonomia GOLD, quelli non riconducibili sono stati omessi. 

#### WORDNET
La cartella wordnet contiene tutti i file db di wordnet utilizzati dal wordnet manager e altri due file che servono al corretto funzionamento di quest'ultimo. I contenuti di questa cartella vengono descritti in dettaglio nella documentazione di wordnet manager. 

### **Moduli**
Il progetto, composto da vari moduli Python, è molto semplice. C'è una cartella `models`  al cui interno sono presenti singoli moduli che implementano i classificatori e il preprocessamento del testo, ovvero moduli che elaborano il dataset. In data odierna (17/09/2019), sono presenti:
- `naivebayes.py`: una classe che implementa un classificatore bayesiano uilizzando nltk.
- `svm.py`: contiene una classe che implementa una support vector machine utilizzando scikit-learn.
- `textcleaner.py`: una serie di metodi basilari che puliscono il linguaggio naturale. 
- `random_classifier.py`: un classificatore casuale che può anche prendere in considerazione la distribuzione d. 

Nella cartella principale, oltre al dataset, sono presenti anche:
- `main.py`: modulo principale in cui si combina l'utilizzo di tutti gli altri moduli e unico modulo da chiamare nella console di python. 
- `dataset_manager.py` modulo contenente i metodi per tradurre il dataset in strutture dati di python.  
- `*.pkl`: file contenente il classificatore già trainato. In qualsiasi momento si può caricare in memoria principale e usare per classificare.
- `web_api.py`: file contenente l'implementazione dell'API. 
- `prova_dotnet.py`: script che carica il classificatore salvato in memoria e classifica una descrizione, eseguibile da programma C#.
- `wnmanager.py`: script che apre l'interfaccia grafica del wordnet manager. Serve per poter creare l'eseguibile con pyinstaller.

### **Web API**
E' stata creata un API a cui potersi interfacciare per utilizzare il classificatore.
Per attivarla occorre aprire una shell, attivare l'ambiente virtuale, ed eseguire i seguenti comandi:
- `$env:FLASK_APP = "web_api.py"`
- `$env:FLASK_ENV = "development"`
- `flask run`

Si attiverà web server all'indirizzo http://127.0.0.1:5000/ a cui si potranno inviare le richieste. 

## Configurazione ambiente di lavoro

- installare python 3.7.*
- creare la cartella del progetto
- eseguire la pull da remoto
- aprire una shell e posizionarsi all'interno della cartella
- (SOLO LA PRIMA VOLTA) eseguire il comando "python -m venv v_env_etc" per creare l'ambiente virtuale 
- sempre dalla shell eseguire "v_env_etc\Scripts\activate.ps1" per attivare l'ambiente su di essa
- (SOLO LA PRIMA VOLTA) eseguire il comando "pip install -r requirements.txt" per installare tutte le dipendenze necessarie
- eseguire il comando "python -m idlelib.idle" per aprire l'IDLE su cui far girare il main
- eseguire "deactivate" per uscire dall'ambiente virtuale sulla shell
... Altro

## Distribuzione pacchetto
Per la distribuzione si è scelto pyinstaller. In teoria basterebbe un solo comando per creare il pacchetto di distribuzione, ma per motivi ignoti, se si vuole far aprire l'applicazione col click del mouse e senza che si apra la console, bisogna mettere insieme 2 distribuzioni.

Quindi da terminale, attivare l'ambiente virtuale come descritto nel capitolo sopra. Successivamente:
- eseguire il comando `pyinstaller wnmanager.py`
- eseguire il comando `pyinstaller --onefile wnmanager.py`
  
Il primo comando creerà 2 cartelle `build` e `dist`. All'interno di dist avrete una cartella `wnmanager` (risultato del primo comando) e un file `wnmanager.exe` (risultato del secondo). 
Per completare la distribuzione bisogna ancora:
- entrare nella cartella `wnmanager` descritta sopra ed eliminare l'omonimo .exe
- copiare la cartella `wordnet` all'interno della cartella `dist`

A questo punto nella cartella dist si hanno la cartella `wnmanager`, la cartella `wordnet` e l'eseguibile `wnmanager.exe`. Comprimere i files e inviarli all'utente, il quale potrà estrarre il pacchetto dove vuole e iniziare subito ad utilizzare Wordnet Manager clickando sull'eseguibile. 

