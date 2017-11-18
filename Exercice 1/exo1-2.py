from elasticsearch import Elasticsearch
import requests, os, json, glob, codecs, re
import numpy as np

os.chdir("indexpays/")

#connexion au serveur Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


#retourne une liste de tous les fichier json dans le fichier "indexpays"
def listjson():

    listfile = glob.glob("*.json")
    return listfile


def constructindex():

    es.indices.create(index='indexpays', ignore=400)
    file=listjson()
    file.sort()
    i = 0
    for keys in file:

        paysinfo=json.load(open(keys,encoding="utf-8"))
        es.index(index='pays', doc_type='paysdef', id=i, body=paysinfo)
        i+=1

def queryelastic(query):

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

def resultPrediction():

    requetes = open("../liste_requetes.txt", "r")
    liste_requetes=requetes.read()
    requetes.close()
    quest = re.findall("(Q[0-9]+)[\W]([\w ]*[a-z])",liste_requetes)
    listprediction=""
    for i in range(0,len(quest)):

        data = json.dumps(es.search(index="pays",doc_type="paysdef",body=queryelastic(quest[i][1])))
        # print(data)
        j = json.loads(data)
        for g in range(0,len(j["hits"]["hits"])):

            listprediction=listprediction+str(quest[i][0]+" "+j["hits"]["hits"][g]["_source"]["name"]+"\n")
    # print(listprediction)
    return listprediction
resultPrediction()
def writeJugementsPrediction(listeOfPrediction):

    file=open("../jugementsPrediction.txt","w")
    file.write(listeOfPrediction)
    file.close()

def listOfJugements(txtjugements):

    jugements = open("../"+txtjugements)
    jugementsRE = jugements.read()
    jugements.close()

    reGex = re.findall("(Q[0-9]+) ([A-Z][\w ,()'-]*)",jugementsRE)

    return reGex

def appendTab(tab,precision):
    tab.append(precision)

def moyTab(tab):
    result=0
    for i in range(0,len(tab)):
        result+=tab[i]
    try:
        moyenne = result/len(tab)
    except ZeroDivisionError:
        moyenne=0
    return moyenne

def averagePrecision(txtjugements,txtjugementsPrediction):

    tableAverage=[]
    resultMoyPrediction=[]
    jugements = listOfJugements(txtjugements)
    jugementsPrediction = listOfJugements(txtjugementsPrediction)
    nbPast=0
    nominateur=0
    indexQestions="Q1"

    for i in range(0,len(jugementsPrediction)):

        if(indexQestions!=jugementsPrediction[i][0]):
            appendTab(resultMoyPrediction,moyTab(tableAverage))
            tableAverage = []
            nominateur,nbPast,resultPrediction=0,0,0
            indexQestions=jugementsPrediction[i][0]

        if(jugementsPrediction[i] in jugements):
            nominateur += 1
            nbPast += 1
            resultPrediction=nominateur/nbPast
            appendTab(tableAverage,resultPrediction)
        else:
            nbPast+=1
            resultPrediction = nominateur / nbPast

    return resultMoyPrediction
print(averagePrecision("jugements.txt","jugementsPrediction.txt"))

def MAP(averagePrecision):

    return moyTab(averagePrecision)

print(MAP(averagePrecision("jugements.txt","jugementsPrediction.txt")))
