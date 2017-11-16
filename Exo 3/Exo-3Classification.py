import Exo3, pandas, json
from sklearn.naive_bayes import MultinomialNB as mod
from sklearn.ensemble import RandomForestClassifier as mod2
from sklearn.feature_extraction.text import CountVectorizer

def choiceClassifier(i):

    if(i==1):
        classifier=mod
    else:
        classifier=mod2

    return classifier

def constructModel(i,cc,j):

    classifieur=choiceClassifier(2)

    df_train= pandas.read_csv('forClassification.csv')
    final=pandas.DataFrame(data=df_train)

    vecteurClasseTrain=final["Classe"][:cc]
    vecteurQuestion=final["Texte"][:cc]

    classifier=classifieur()

    targetsClasse=vecteurClasseTrain.values

    vecteurClasseTest=final["Classe"][cc:].values

    count_vectorizer = CountVectorizer()
    counts = count_vectorizer.fit_transform(vecteurQuestion.values)

    classifier.fit(counts, targetsClasse)
    examples = final["Texte"][cc:len(final)]

    example_counts = count_vectorizer.transform(examples)
    predictions = classifier.predict(example_counts)

    if (i==1):
        return predictions
    elif(i==2):
        return vecteurClasseTest
    elif(i==3):
        return examples

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

            result+=1

    return result

def falsePositive(classe,tailletraining,j):

    data = construcTableRP(constructModel(1,tailletraining,j),constructModel(2,tailletraining,j))
    result=0
    for i in range(0,len(data)):

        if ((classe == data[str(i)]["class"]) & (data[str(i)]["bool"]==False)) :
            result+=1

    return result

def trueNegative(classeOption,tailletraining,j):

    data = constructModel(2,tailletraining,j)
    data.sort()
    result=0

    for classe in data:

        if(classe!=classeOption):

            result+=1

    return result

def falseNegative(classeOption,tailletraining,j):

    data = constructModel(2,tailletraining,j)
    data.sort()
    result=0

    for classe in data:

        if(classe==classeOption):

            result+=1

    return result

def precision(classe,trainingSize,j):

    return truePositive(classe,trainingSize,j)/(truePositive(classe,trainingSize,j)+falsePositive(classe,trainingSize,j))

def recall(classe,trainingSize,j):

    return truePositive(classe,trainingSize,j)/(falseNegative(classe,trainingSize,j))


with open('dicoClass.json') as json_data:
    dico = json.load(json_data)

Exo3.createliste(1,dico)


print(falsePositive("Positif",1500,1))
print(falsePositive("Negatif",1500,1))

print(falseNegative("Positif",1500,1))
print(falseNegative("Negatif",1500,1))

print(precision("Positif",1500,1))
print(precision("Negatif",1500,1))

print(recall("Positif",1500,1))
print(recall("Negatif",1500,1))




