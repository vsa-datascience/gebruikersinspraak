# Classificatie van parlementaire vragen

## Scraper
''scraper_parlement.py'' \

De Scraper itereert over de verschillenda pagina's van de website van parlementaire vragen (https://www.vlaamsparlement.be/nl/parlementaire-documenten). Op elke pagina identificeert de scaper of de link het document met parlementaire vragen een webpagina, pdf,of word document is. 

Afhankelijk van het document wordt de juiste functie uitgevoerd om de inhoud van he document er uit te halen en in .txt file te plaatsen onde de /documents folder.


## Identificeren van vragen
''retrieve_questions.py'' \

Voor elk van de gescrapete documenten in /documents folder, gaat de vragen er uit gehaald worden. Aangezien de vragen niet altijd met regex te identficeren valt of weinig informatie opzich bevatten, wordt hiervoor GPT 3.5 model gebruikt. De vragen worden als .csv file geplaatst in de /questions folder. GPT 4 werd hier niet gebeurd aangezien voor het identficeren de 3.5 het goed presteerde en om de kosten te drukken.


## classficeren van vragen
''classify.py'' \

De laatste stap in de pipeline is het classificeren (statistic/non-statistic) van de geïdentificeerde vragen. Dit wordt aan de hand met GPT API uitgevoerd met de GPT 4 model en few shot prompting. In de prompt worden een aantal voorbeelden meegegven om context aan het GPT model te geven. Het eindresultaat is een .csv bestand met de vragen en nieuwe kolom 'label' dat de classificatie omvat.


