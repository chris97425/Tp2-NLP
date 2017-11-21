from elasticsearch import Elasticsearch
import  os, json, glob, re

##################################### Partie 0

os.chdir("indexpays/")
#Connexion au serveur Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


#retourne une liste de tous les fichier json dans le fichier "indexpays"
##################################### Partie 1
def listJson():

    listFile = glob.glob("*.json")
    return listFile

##################################### Partie 2
def constructIndex():

    es.indices.create(index='indexpays', ignore=400)
    file=listJson()
    file.sort()
    i = 0
    for keys in file:

        paysinfo=json.load(open(keys,encoding="utf-8"))
        es.index(index='indexpays', doc_type='paysDef', id=i, body=paysinfo)
        i+=1
##################################### Partie 3
constructIndex()
def queryElastic(query):

    result = {
            "query" : {
                        "match" : {
                                    "_all" :{
                                            "query":query,
                                            "operator":"or",
                                            "minimum_should_match": "79%"
                                            }
                                     }
                        }
            }

    return result

##################################### Partie 4
def resultPrediction():

    requetes = open("../liste_requetes.txt", "r")
    liste_requetes=requetes.read()
    requetes.close()
    quest = re.findall("(Q[0-9]+)[\W]([\w ]*[a-z])",liste_requetes)
    listprediction=""
    for i in range(0,len(quest)):

        data = json.dumps(es.search(index="indexpays",doc_type="paysDef",body=queryElastic(quest[i][1])))
        j = json.loads(data)
        for g in range(0,len(j["hits"]["hits"])):

            listprediction=listprediction+str(quest[i][0]+" "+j["hits"]["hits"][g]["_source"]["name"]+"\n")

    # print(listprediction)
    return listprediction

resultPrediction()

##################################### Partie 5
def writeJugementsPrediction(listeOfPrediction):

    file=open("../jugementsPrediction.txt","w")
    file.write(listeOfPrediction)
    file.close()


##################################### Partie 6
def listOfJugements(txtjugements):

    jugements = open("../"+txtjugements)
    jugementsRE = jugements.read()
    jugements.close()

    reGex = re.findall("(Q[0-9]+) ([A-Z][\w ,()'-]*)",jugementsRE)

    return reGex

##################################### Partie 7
def appendTab(tab,precision):
    tab.append(precision)

##################################### Partie 8
def moyTab(tab):
    result=0

    for i in range(0,len(tab)):
        result+=tab[i]
    try:
        moyenne = result/len(tab)
    except ZeroDivisionError:
        moyenne = 0

    return moyenne

##################################### Partie 9
def averagePrecision(txtjugements,txtjugementsPrediction):

    tableAverage=[]
    resultMoyPrediction=[]
    jugements = listOfJugements(txtjugements)
    jugementsPrediction = listOfJugements(txtjugementsPrediction)
    denominateur=0
    numerateur=0
    indexQestions="Q1"

    for i in range(0,len(jugementsPrediction)):

        if(indexQestions!=jugementsPrediction[i][0]):
            appendTab(resultMoyPrediction,moyTab(tableAverage))
            tableAverage = []
            numerateur,denominateur=0,0
            indexQestions=jugementsPrediction[i][0]

        if(jugementsPrediction[i] in jugements):
            numerateur+= 1
            denominateur += 1
            resultPrediction=numerateur/denominateur
            appendTab(tableAverage,resultPrediction)
        else:
            denominateur+=1

    return resultMoyPrediction

print(averagePrecision("jugements.txt","jugementsPrediction.txt"))
##################################### Partie 10

def MAP(averagePrecision):

    return moyTab(averagePrecision)

print("Le MAP vaut: ",MAP(averagePrecision("jugements.txt","jugementsPrediction.txt")))
