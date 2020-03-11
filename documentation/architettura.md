# Sistema di classificazione automatica

Questo sistema ha lo scopo di poter creare e mantenere un modulo di intelligenza artificiale, chiamato classificatore, capace di riconoscere un descrittivo e assegnargli un elemento di tassonomia. Più in specifico, è stato progettato per attribuire la giusta risk category a un loss event, data la sua descrizione. Tuttavia attraverso questo sistema è possibile creare un classificatore per qualsiasi tassonomia e qualsiasi tipo di descrittivo. 

Per andare a descrivere le sue funzionalità è necessario precisare che il sistema si suddividerà in 2 parti distinte:
- la prima è il plug-in vero e proprio, ovvero l'estensione di GRC a cui ci aggiungerà funzionalità specifiche per l'utilizzo del classificatore. 
- la seconda è un ambiente di back-end dove un consulente avrà la possibilità di gestire, creare e mantenere il classificatore. 

## Ambiente di back-end

L'ambiente di back-end avrà le funzionalità necessarie per la creazione e manutenzione del classificatore. 

Prima di procedere è necessario descrivere brevemente il funzionamento del classificatore. Un testo prima di essere passato ad un classificatore deve essere preprocessato attraverso un dizionario, le parole trovate nel dizionario verranno tenute mentre le altre saranno scartate.

Il dizionario utilizzato in questo compito ha una lista di termini raggruppati per concetti. Una parola può far parte di più concetti (omonimi) e parole diverse possono far parte dello stesso concetto (sinonimi). 

Si possono distinguere due compiti principali da svolgere nell'ambiente di back-end:
- Uno sarà quello di estendere questo dizionario con termini specifici della società per cui sta lavorando. 
- L'altro sarà quello di creare e monitorare le performance del classificatore, anche a fronte di nuovi dati.

Le funzionalità chiave di questo ambiente sono quindi:

- Per il dizionario:
  - Aggiunta di una parola al dizionario, indicando il concetto a cui la si vuole collegare.
  - Aggiunta di un concetto al dizionario, nel caso non ce ne sia uno che soddisfi il consulente.
    - ogni concetto ha una breve descrizione per poterli identificare
  - Provare il dizionario con le nuove aggiunte inserendo un descrittivo e processandolo. 
- Per il classificatore
  - Testare le performance del modello del classificatore con nuovi dati e/o con nuove aggiunte al dizionario
  - Creare un classificatore con il dizionario e dati forniti dall'applicativo e salvarlo in memoria.

Al termine delle attività di consulenza, sarà possibile aggiornare l'estensione di GRC spostando dei file specifici dall'ambiente di back-end a quello del plug-in.


## Estensione GRC (plug-in)

L'estensione di GRC riguardante il classificatore di testo si concretizzerà in 2 funzionalità:
- Censire un oggetto utilizzando il classificatore per trovare il giusto elemento di tassonomia.
  - Ad esempio durante il censimento della sezione "attribuzione" di un loss event nel campo di "risk category". 
- Creare un export specifico di un tipo di oggetto e una tassonomia, da poter passare poi alla consulenza per creare il classificatore.
  - Ad esempio nella pagina di indice dei loss event sarà possibile creare un export selezionando la tassonomia su cui si vuole allenare il classificatore, creando un file excel con un formato apposito. 


