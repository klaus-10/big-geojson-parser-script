# Istruzioni per l'importazione dei dati

Per file di grandi dimensionoi è necessario utilizzare la libreria JQ per la compressione e la standardizzazione del GeoJson. Nello specifico il comando riportato seleziona il campo "features" tipico dei file gejson e ci lavora su:

''' jq --compact-output ".features" input.geojson > output.geojson '''

l'output è un array di oggetti JSON.

A questo punto sarebbe stato bello utilizzare il seguente comando "mongoimport --db dbname -c collectionname --file "output.geojson" --jsonArray", ma il problema è che il file di input "output.geojson" ha dimensione 350MB. Dunque mongoimport è praticamente inutile...

[IDEA] L'idea è stata quella di leggere il file di input in riga, e successivamente fare la insert su database per ogni singolo oggetto letto.

[Problemi riscontrati]:

- tipologia di codifica di input "utf16" -> "utf-8"
- problemi con il tipo Decimal dovuto all'oggetto Bson e Json di python
- problemi con la libreria json causati dalla dimensione eccessiva delle singole righe degli oggetti dell'array

[SOLUZIONE]:

- convertire il file output3 con la codifica utf8 nel file --> output3_utf8 ("cml: iconv -f UTF-16 -t UTF-8 output3.geojson > output3_utf8.geojson")
- convertire in modo ricorsivo tutti gli elementi di tipo Decimal in Float presenti all'interno di un singolo oggetto
- cambiare la libreria di utilizzo json in "ijson", più adatta per la lettura di file json grandi
