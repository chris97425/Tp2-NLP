import exo2, pandas, glob

from sklearn.naive_bayes import MultinomialNB as mod
from sklearn.ensemble import RandomForestClassifier as mod2
from sklearn.feature_extraction.text import CountVectorizer

#Choix du classifieurn i=1 NaivesBayes sinon RandomForest
#################################Partie 0
def choiceClassifier(i):

    if(i==1):
        classifier=mod
    else:
        classifier=mod2

    return classifier

#################################Partie 1
#Construction du fichier csv s'il n'est pas encore présent dans le répértoire
def construCsv():

    a = glob.glob("*.csv")
    if (len(a)==0):
        exo2.constructCsv()


#################################Partie 2
#Construction du modèle prédictive en fonction du choiceClassifier() et prédiction sur un certain nombre de ligne résévées au test
def constructModel(cc,j):

    classifieur=choiceClassifier(j)
    result=[]
    # Transformation de mon document csv en dataframe grâce à panda
    df_train= pandas.read_csv('mycsv.csv')
    final=pandas.DataFrame(data=df_train)
    #Y sera mon vecteur de classe et x le vecteur de question associé
    vecteurClasseTrain=final["Classe"][:cc]
    # print(vecteurClasseTrain)
    vecteurQuestion=final["Question"]
    classifier=classifieur()
    targetsClasse=vecteurClasseTrain[:cc].values
    vecteurClasseTest=final["Classe"][cc:].values
    # print(final["Classe"][cc:])
    count_vectorizer = CountVectorizer()
    counts = count_vectorizer.fit_transform(vecteurQuestion[:cc].values)
    classifier.fit(counts, targetsClasse)

    examples = vecteurQuestion[cc:]
    example_counts = count_vectorizer.transform(examples)
    predictions = classifier.predict(example_counts)

    result.append(predictions)
    result.append(vecteurClasseTest)
    result.append(examples)
    result.append(j)

    return result

#################################Partie 3

#Ici on construit un dictionnaire qui nous stock les différence entre les vraies prédictions et les fausses pour chaque classe
def construcTableRP(predictions,trueclass):

    result = {}

    for i in range(0,len(predictions)):

        if(predictions[i]==trueclass[i]):

            result[str(i)]=({
                "class":predictions[i],
                "bool": True
            })

        else:
            result[str(i)]=({
                "class": predictions[i],
                "bool": False
            })

    return result
#################################Partie 4

def truePositive(classe,tableRP):

    data = tableRP
    result=0
    for i in range(0,len(data)):

        if ((classe == data[str(i)]["class"]) & (data[str(i)]["bool"])) :
            result+=1
    return result

def falsePositive(classe,tableRP):

    data = tableRP
    result=0
    for i in range(0,len(data)):

        if ((classe == data[str(i)]["class"]) & (data[str(i)]["bool"]==False)) :
            result+=1

    return result

def trueNegative(classeOption,Model):

    data = Model[1]
    data.sort()
    result=0
    for classe in data:

        if(classe!=classeOption):
            result+=1
    return result

def falseNegative(classeOption,Model):

    data = Model[1]
    data.sort()
    result=0
    for classe in data:

        if(classe==classeOption):
            result+=1
    return result

def precision(classe,Model,tableRP):
    return truePositive(classe,tableRP)/(truePositive(classe,tableRP)+falsePositive(classe,tableRP))

def recall(classe,Model,tableRP):
    return truePositive(classe,tableRP)/(falseNegative(classe,Model))
#################################Partie 5

def general(Model, tableRP,classe):

    if(Model[3]==1):
        cl="Naives Bayes"
    else:
        cl="Random Forest"

    print("Pour la classe ",classe," et un modèle ",cl," la précision est de:")
    print(precision(classe,Model,tableRP))
    print("Pour un rappel de:")
    print(recall(classe,Model,tableRP))

def result(list,model,tableRP):

    if (model[3]==1):
        print("Pour Naives Bayes:")
    else:
        print("Pour Random Forest")

    for key in list:

        general(model,tableRP,key)
    print("-------------------")

construCsv()
Model1=constructModel(15, 1)
Model2=constructModel(15, 2)
tableRp1=construcTableRP(Model1[0],Model1[1])
tableRp2=construcTableRP(Model2[0],Model2[1])
liste=["DEFINITION","QUANTITY","LOCATION","TEMPORAL","PERSON"]
result(liste,Model1,tableRp1)
result(liste,Model2,tableRp2)







