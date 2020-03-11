# Sperimentazione modelli

## Metodologia e terminologia

### Classificatori
- Naive Bayes: è un classificatore bayesiano, per ogni feature cerca di capire quale label sia la più probabile considerando le occorrenze di ogni istanza.
- Support vector machine: un classificatore che esegue regressione lineare. Mappa le istanze di training su un piano multidimensionale e cerca di trovare una funzione che separi gli iperpiani che rappresentano le classi considerate. 
  
### Tecninche di pre-processing

- treetagger: sostituisce le parole col loro lemma e toglie articoli e pronomi
- rimozione stopwords: rimozione di stopwords all'interno di `nltk.stopwords.words('italian')`
- sostituzione synsets: si sostituiscono le parole, dove possibile, con i relativi siynsets di wordnet

### Classificazione 

Gli oggetti classificati sono delle descrizioni scritte in linguaggio naturale che descrivono un evento di perdita. Il risultato della classificazione è un elemento di una tassonomia di categorie di rischio, la quale si dirama su 3 livelli. Si prende sempre in considerazione un livello alla volta.  

Fino al (2) è stato usato un metodo grossolano in cui esisteva un metodo che faceva girare il training del classificatore solo 1 volta (spezzando il dataset fra training set e test set) e mandava in output la validazione eseguita sul test set. Il metodo veniva fatto girare 5-10 volte per ottenere una media dei risultati. 
Dal (3) in poi questo metodo è stato sostituito con una "k-fold cross validation" che spezza il dataset in k parti e ne utilizza k-1 per il training e 1 per il test. Tutto ciò per k volte utilizzando ogni set almeno una volta per il test. Il metodo manda poi in output una lista di risultati su cui si può fare una media. 


### Risultati

- **Accuratezza**: semplice rapporto fra le istanze classificate correttamente e quelle non corrette. 
- **Precisione**: rapporto fra le istanze positive classificate correttamente come positive e quelle negative classificate erroneamente positive (true positive/true positive + false positive). Fa riferimento a una sola classe.
- **Macro precision**: La media non pesata della precisione di ogni classe
- **Recall**: rapporto fra le istanze positive classificate correttamente come positive e quelle positive classificate erroneamente negative (true positive/true positive + false negatives). Fa riferimento a una sola classe.
- **Macro recall**: La media non pesata del recall di ogni classe


## 1 Naive-Bayes di nltk

### Configurazione

- **Classificatore**: Naive-Bayes di nltk
- **Preprocessing**: treetagger e rimozione stopwords
- **Tecnologie**: NLTK, TreeTagger
- **dataset**: sparkasse, 1022 train records, 100 test records con duplicati
- **Modalità di test**: training e test eseguiti 5-10 volte, è stato poi creato il range col minimo e col massimo.
- **Risultati**: 85-95%, classifica TUTTE le istanze con la classe più rappresentata, sempre la G, quindi assolutamente inutile.

### Conclusioni

Il classificatore bayesiano non riesce a trovare le differenze fra una classe e un'altra, riesce soltanto a individuare la classe più rappresentata. 

## 2 Support vector machine di scikit-learn

- **Classificatore**: Support vector machine di scikit-learn
- **Preprocessing**: treetagger e rimozione stopwords
- **Tecnologie**: scikit-learn
- **dataset**: sparkasse con duplicati
  - senza preprocessing: 1494 train records, 500 test records 
  - con preprocessing: 872 train records, 250 test records 
- **Modalità di test**: training e test eseguiti 5-10 volte, è stato poi creato il range col minimo e col massimo.
- **tempo**: ogni giro impiega 20-30 secondi.
- **Risultati**: 
  - Livello 1: 94%-96%  sia con che senza preprocessing
    - Macro precision: 
      - 16%-25% con preprocessing
      - 96%-99% senza preprocessing (overfitting)
    - macro recall: 
      - 17%-25% con preprocessing
      - 73%-91% senza preprocessing (overfitting)
  - Livello 3: senza preprocessing 88%-91%, con 89%-93%
    - Macro precision:
      - 21%-28% con preprocessing
      - 45%-60% senza preprocessing
    - Macro recall: 
      - 16%-30% con preprocessing
      - 40%-52% senza preprocessing

### Conclusioni

La SVM riesce a distinguere con adeguata accuratezza le differenti classi. Rimane da svolgere un lavoro a monte sul preprocessamento del testo. 

## 3 Support vector machine di scikit-learn (data-set esteso)
- **Classificatore**: Support vector machine di scikit-learn
- **Preprocessing**: treetagger e rimozione stopwords
- **Tecnologie**: scikit-learn
- **dataset**: LDC finale con 7688 records
  - senza preprocessing: 
    - livello 1: 7688 train records, 1000 test records 
    - livello 3: 3236 train records, 700 test records
  - con preprocessing: 872 train records, 250 test records 
- **Modalità di test**: 9 fold cross validation, è stato aggiunto un più o meno 5
- **tempo**: ogni giro impiega 1 minuto.
- **Risultati**: 
  - Livello 1: 90% 
    - Macro precision: 
      - senza preprocessing. 80%-90%
      - con preprocessing: 50%-60%
    - Macro recall: 
      - senza preprocessing: 70%-80%
      - con preprocessing: 35%-45%
  - Livello 3: 77%-80%
    - Macro precision:
      - senza preprocessing: 30%-40%
      - con preprocessing: < 10%
    - Macro recall:
      - senza preprocessing: 30%-40%
      - con preprocessing: < 10%

### Conclusioni

Il dataset nuouvo ha introdotto più diversificazione nel linguaggio utilizzato nelle descrizioni, portando a leggero abbassamento dell'accuratezza. Si è scoperto un bug per il quale ilpreprocessamento eliminava quasi tutte le parole da quasi tutti i record e lasciava soltanto le preposizioni e gli articoli.

## 4 Support vector machine di scikit-learn (con nuovo preprocessamento)
- **Classificatore**: Support vector machine di scikit-learn
- **Preprocessing**: treetagger e rimozione stopwords (che funzionano correttamente)
- **Tecnologie**: scikit-learn
- **dataset**: LDC finale con 7688 records uguale con e senza preprocessing, 3236 al terzo livello
- **Modalità di test**: 9 fold cross validation fatto girare 2 volte
- **tempo**: ogni giro impiega 1 minuto.
- **Risultati**: 
  - Livello 1: 90% 
    - Macro precision: 90%
    - Macro recall: 76%
  - Livello 3: 79%
    - Macro precision:35%
    - Macro recall:35%

### conclusioni 
Con la correzione del bug del preprocessing ora i risultati nel caso del suo utilizzo sono simili a quelli nel caso non lo si usasse.

## 5 Support vector machine di scikit-learn (con i synsets di wordnet)
- **Classificatore**: Support vector machine di scikit-learn
- **Preprocessing**: treetagger e rimozione stopwords (che funzionano correttamente) e sostituzione synests
- **Tecnologie**: scikit-learn
- **dataset**: LDC finale con 7688 records uguale con e senza preprocessing, 3236 al terzo livello
- **Modalità di test**: 9 fold cross validation fatto girare 2 volte
- **tempo**: ogni giro impiega 2-3 minut1.
- **Risultati**: 
  - Livello 1: 
    - Accuratezza: 90% 
    - Macro precision: 90%
    - Macro recall: 76%
  - Livello 3: 
    - Accuratezza: 79%
    - Macro precision:36%
    - Macro recall:36%

## 6 Classificazione casuale
- **Classificatore**: random classifier
- **Preprocessing**: treetagger e rimozione stopwords (che funzionano correttamente) e sostituzione synests
- **Tecnologie**: 
- **dataset**: LDC finale con 7688 records uguale con e senza preprocessing, 3236 al terzo livello
- **Modalità di test**: 9 fold cross validation fatto girare 2 volte
- **tempo**: ogni giro impiega 2-3 minuti.
- **Risultati**: 
  - Livello 1: 
    - Accuratezza: 14%
    - Macro precision: 14%
    - Macro recall: 15%
  - Livello 1 sfruttando la distribuzione: 
    - Accuratezza: 37% 
    - Macro precision: 14%
    - Macro recall: 14%
  - Livello 3: 
    - Accuratezza: 1%
    - Macro precision:<1%
    - Macro recall:<1%

## 7 Support vector machine di scikit-learn (con i synsets di wordnet e parole aggiunte )
- **Classificatore**: Support vector machine di scikit-learn
- **Preprocessing**: sostituzione synests se trovato altrimenti solo originale, le parole sono quelle aggiunte in wordnet_additions.py
- **Tecnologie**: scikit-learn
- **dataset**: LDC finale con 7688 records , 3236 al terzo livello
- **Modalità di test**: 9 fold cross validation fatto girare 2 volte
- **tempo**: ogni giro impiega 2-3 minut1.
- **Risultati**: 
  - Livello 1: 
    - Accuratezza: 90% 
    - Macro precision: 89%
    - Macro recall: 75%
  - Livello 3: 
    - Accuratezza: 79%
    - Macro precision:38%
    - Macro recall:36%
  - **Considerazioni**: le parole aggiunte a wordnet non sono sufficienti per fare la differenza

## 8 Support vector machine di scikit-learn (con nuovo dataset pulito)
- **Classificatore**: Support vector machine di scikit-learn
- **Preprocessing**: sostituzione synests se trovato altrimenti solo originale, le parole sono quelle aggiunte in wordnet_additions.py
- **Tecnologie**: scikit-learn
- **dataset**: LDC con 5104 records, 1936 al terzo livello SENZA RIPETIZIONI
- **Modalità di test**: 9 fold cross validation fatto girare 2 volte
- **tempo**: ogni giro impiega 2-3 minut1.
- **Risultati**: 
  - Livello 1: 
    - Accuratezza: 86% 
    - Macro precision: 81%
    - Macro recall: 66%
  - Livello 3: 
    - Accuratezza: 67%
    - Macro precision:32%
    - Macro recall:32%
- **considerazioni**: L'assenza di ripetizioni nel dataset ha abbassato la performance perché non esistono più doppioni nel train set e nel test set, i quali, se presenti, vengono classificati a colpo sicuro. 
  
## 8 Support vector machine di scikit-learn (con aggiunte wordnet)
- **Classificatore**: Support vector machine di scikit-learn
- **Preprocessing**: sostituzione synests se trovato altrimenti solo originale, le parole sono quelle aggiunte in wordnet_additions.py: 93 parole aggiunte e 11 synset aggiunti
- **Tecnologie**: scikit-learn
- **dataset**: LDC con 5104 records, 1936 al terzo livello SENZA RIPETIZIONI
- **Modalità di test**: 9 fold cross validation fatto girare 2 volte
- **tempo**: ogni giro impiega 2-3 minut1.
- **Risultati**: 
  - **Tenendo** le parole non trovate da wordnet
    - con wordnet **originale**
      - Livello 1: 
        - Accuratezza: 86% 
        - Macro precision: 81%
        - Macro recall: 66%
      - Livello 3: 
        - Accuratezza: 67%
        - Macro precision:34%
        - Macro recall:31%
    - con **aggiunte** a wordnet
      - Livello 1: 
        - Accuratezza: 86% 
        - Macro precision: 81%
        - Macro recall: 66%
      - Livello 3: 
        - Accuratezza: 66%
        - Macro precision:32%
        - Macro recall:30%
  - **togliendo** le parole non trovate da wordnet
      - con wordnet **originale**
        - Livello 1: 
          - Accuratezza: 80% 
          - Macro precision: 67%
          - Macro recall: 55%
        - Livello 3: 
          - Accuratezza: 61%
          - Macro precision:28%
          - Macro recall:28%
      - con **aggiunte** a wordnet
        - Livello 1: 
          - Accuratezza: 81% 
          - Macro precision: 66%
          - Macro recall: 57%
        - Livello 3: 
          - Accuratezza: 61%
          - Macro precision:28%
          - Macro recall:28%
- **considerazioni**: La differenza fra il tenere le parole non trovate da wordnet e tenerle fa ancora un'enorme differenza in quanto si tolgono ancora troppe parole di significato. Quando si tolgono le parole c'è però un risultato interessante. Sul terzo livello non succede ancora niente, ma sul primo le prove svolte con il wordnet esteso hanno trovato un miglioramento rispetto al wordnet originale. 

### conclusioni 
Con la sostituzione dei synset non c'è molta differenza col semplice preprocessamento, questo è dovuto al fatto che la modalità di sostituzione ora prevista, non aggiunge una unificazione semantica dei termini simili. C'è però un leggero miglioramento sul terzo livello

## Considerazioni future
- bisogna gestire i casi in cui wordnet non trovi un synset
- bisogna creare un metodo per trovare il synset appropriato per ogni parola
- bisogna pulire ulteriormente il testo


