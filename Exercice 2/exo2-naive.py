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
        exo2.constructcsv()

construccsv()

#Construction du modèle prédictive en fonction du choiceClassifier() et prédiction sur un certain nombre de ligne résévées au test
def constructModel(i,cc,j):

    classifieur=choiceClassifier(j)

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
    # print(count_vectorizer.get_feature_names())

    classifier.fit(counts, targetsClasse)

    examples = vecteurQuestion[cc:389]
    example_counts = count_vectorizer.transform(examples)
    predictions = classifier.predict(example_counts)

    if (i==1):
        return predictions
    elif(i==2):
        return vecteurClasseTest
    elif(i==3):
        return examples

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


def truePositive(classe,tailletraining,j):

    data = construcTableRP(constructModel(1,tailletraining,j),constructModel(2,tailletraining,j))
    result=0
    for i in range(0,len(data)):

        if ((classe == data[str(i)]["class"]) & (data[str(i)]["bool"])) :
            # print(data[str(i)]["class"])

            result+=1


    return result

# print(truePositive("DEFINITION",300))

def falsePositive(classe,tailletraining,j):

    data = construcTableRP(constructModel(1,tailletraining,j),constructModel(2,tailletraining,j))
    # print(data)
    result=0
    for i in range(0,len(data)):

        if ((classe == data[str(i)]["class"]) & (data[str(i)]["bool"]==False)) :
            result+=1

    return result

def trueNegative(classeOption,tailletraining,j):

    data = constructModel(2,tailletraining,j)
    data.sort()
    result=0

    print(data)
    for classe in data:

        if(classe!=classeOption):
            result+=1
    return result

# print(trueNegative("DEFINITION",300,1))

def falseNegative(classeOption,tailletraining,j):

    data = constructModel(2,tailletraining,j)
    data.sort()
    result=0

    print(data)
    for classe in data:

        if(classe==classeOption):
            result+=1
    return result
# print(falseNegative("DEFINITION",300,1))

def precision(classe,trainingSize,j):
    return truePositive(classe,trainingSize,j)/(truePositive(classe,trainingSize,j)+falsePositive(classe,trainingSize,j))
print(precision("DEFINITION",300,2))

def recall(classe,trainingSize,j):
    return truePositive(classe,trainingSize,j)/(falseNegative(classe,trainingSize,j))
# print(recall("DEFINITION",300))







