import Exo3, pandas, glob

from sklearn.naive_bayes import MultinomialNB as mod
from sklearn.ensemble import RandomForestClassifier as mod2
import json

from sklearn.feature_extraction.text import CountVectorizer

with open('2.json') as json_data:
    d = json.load(json_data)
Exo3.createliste(1,d)

def constructModel(i,cc,j):

    classifieur=mod

    # Transformation de mon document csv en dataframe grâce à panda
    df_train= pandas.read_csv('forClassification.csv')
    final=pandas.DataFrame(data=df_train)
    # print(final)

    #Y sera mon vecteur de classe et x le vecteur de question associé
    vecteurClasseTrain=final["Classe"][:cc]
    vecteurQuestion=final["Texte"][:cc]



    classifier=classifieur()

    targetsClasse=vecteurClasseTrain.values
    #
    vecteurClasseTest=final["Classe"][cc:].values

    # print(vecteurClasseTest)
    # print(vecteurClasseTrain)
    #
    count_vectorizer = CountVectorizer()
    counts = count_vectorizer.fit_transform(vecteurQuestion.values)
    # # print(count_vectorizer.get_feature_names())
    #
    classifier.fit(counts, targetsClasse)
    #
    examples = final["Texte"][cc:len(final)]
    # print(final["Classe"][cc:len(final)])

    example_counts = count_vectorizer.transform(examples)
    predictions = classifier.predict(example_counts)

    if (i==1):
        return predictions
    elif(i==2):
        return vecteurClasseTest
    elif(i==3):
        return examples

# print(constructModel(1,1500,1))

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

# print(construcTableRP(constructModel(1,1500,1),constructModel(2,1500,1)))


def truePositive(classe,tailletraining,j):

    data = construcTableRP(constructModel(1,tailletraining,j),constructModel(2,tailletraining,j))
    result=0
    for i in range(0,len(data)):

        if ((classe == data[str(i)]["class"]) & (data[str(i)]["bool"])) :
            # print(data[str(i)]["class"])

            result+=1


    return result

print(truePositive("Positif",1500,1))
print(truePositive("Negatif",1500,1))



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
# print(precision("DEFINITION",300,2))

def recall(classe,trainingSize,j):
    return truePositive(classe,trainingSize,j)/(falseNegative(classe,trainingSize,j))
# print(recall("DEFINITION",300))



