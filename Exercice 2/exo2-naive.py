import exo2, pandas, glob

from sklearn.naive_bayes import MultinomialNB as mod
from sklearn.ensemble import RandomForestClassifier as mod2
from sklearn.feature_extraction.text import CountVectorizer

#Choix du classifieurn i=1 NaivesBayes sinon RandomForest
def choiceClassifier(i):

    if(i==1):
        classifier=mod
    else:
        classifier=mod2

    return classifier

#Construction du fichier csv s'il n'est pas encore présent dans le répértoire
def construccsv():

    a = glob.glob("*.csv")
    if (len(a)==0):
        exo2.constructCsv()

construccsv()

#Construction du modèle prédictive en fonction du choiceClassifier() et prédiction sur un certain nombre de ligne résévées au test
def constructModel(cc,j):

    classifieur=choiceClassifier(j)
    result=[]
    # Transformation de mon document csv en dataframe grâce à panda
    df_train= pandas.read_csv('mycsv.csv')
    final=pandas.DataFrame(data=df_train)
    #Y sera mon vecteur de classe et x le vecteur de question associé
    vecteurClasseTrain=final["Classe"][:cc]
    vecteurQuestion=final["Question"]
    classifier=classifieur()
    targetsClasse=vecteurClasseTrain[:cc].values
    vecteurClasseTest=final["Classe"][cc:389].values
    count_vectorizer = CountVectorizer()
    counts = count_vectorizer.fit_transform(vecteurQuestion[:cc].values)
    classifier.fit(counts, targetsClasse)

    examples = vecteurQuestion[cc:389]
    example_counts = count_vectorizer.transform(examples)
    predictions = classifier.predict(example_counts)

    result.append(predictions)
    result.append(vecteurClasseTest)
    result.append(examples)
    result.append(j)

    return result

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
def truePositive(classe,Model,tableRP):

    data = tableRP
    result=0
    for i in range(0,len(data)):

        if ((classe == data[str(i)]["class"]) & (data[str(i)]["bool"])) :
            result+=1
    return result

def falsePositive(classe,Model,tableRP):

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
    return truePositive(classe,Model,tableRP)/(truePositive(classe,Model,tableRP)+falsePositive(classe,Model,tableRP))

def recall(classe,Model,tableRP):
    return truePositive(classe,Model,tableRP)/(falseNegative(classe,Model))


def general(Model, tableRP,classe):

    if(Model[3]==1):
        cl="Naives Bayes"
    else:
        cl="Random Forest"

    print("Pour la classe ",classe," et un modèle ",cl," la précision est de:")
    print(precision(classe,Model,tableRP))
    print("Pour un rappel de:")
    print(recall(classe,Model,tableRP))


Model1=constructModel(100, 1)
Model2=constructModel(250, 2)
tableRp1=construcTableRP(Model1[0],Model1[1])
tableRp2=construcTableRP(Model2[0],Model2[1])
liste=["DEFINITION","QUANTITY","LOCATION","TEMPORAL","PERSON"]
def result(list,model,tableRP):

    if (model[3]==1):
        print("Pour Naives Bayes:")
    else:
        print("Pour Random Forest")

    for key in list:

        general(model,tableRP,key)
    print("-------------------")


result(liste,Model1,tableRp1)
result(liste,Model2,tableRp2)







