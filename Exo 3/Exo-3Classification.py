import Exo3, pandas, json
from sklearn.naive_bayes import MultinomialNB as mod
from sklearn.ensemble import RandomForestClassifier as mod2
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer


def choiceClassifier(i):
    if (i == 1):
        classifier = mod
    else:
        classifier = mod2

    return classifier


def constructModel( cc, frequencies):

    classifieur = choiceClassifier(2)
    result=[]
    df_train = pandas.read_csv('forClassification.csv')
    final = pandas.DataFrame(data=df_train)

    vecteurClasseTrain = final["Classe"][:cc]
    vecteurQuestion = final["Texte"][:cc]

    classifier = classifieur()

    targetsClasse = vecteurClasseTrain.values

    vecteurClasseTest = final["Classe"][cc:].values

    if not frequencies:
        count_vectorizer = CountVectorizer()
    else:
        count_vectorizer = TfidfVectorizer(min_df=10)  ## Retire tous ce qui a une frequence max de 10

    counts = count_vectorizer.fit_transform(vecteurQuestion.values)

    classifier.fit(counts, targetsClasse)
    examples = final["Texte"][cc:len(final)]

    example_counts = count_vectorizer.transform(examples)
    predictions = classifier.predict(example_counts)


    result.append(predictions)
    result.append(vecteurClasseTest)
    result.append(examples)

    return result

def construcTableRP(predictions, trueclass, Model):
    result = {}
    predictions=Model[0]
    trueclass=Model[1]
    for i in range(0, len(Model[0])):

        if (predictions[i] == trueclass[i]):

            result[str(i)] = ({
                "class": predictions[i],
                "bool": True
            })

        else:
            result[str(i)] = ({
                "class": predictions[i],
                "bool": False
            })

    return result



def truePositive(classe, Model):

    data = construcTableRP(Model[0],
                           Model[1],Model)
    result = 0
    for i in range(0, len(data)):

        if ((classe == data[str(i)]["class"]) & (data[str(i)]["bool"])):
            result += 1

    return result


def falsePositive(classe, Model):
    data = construcTableRP(Model[0],
                           Model[1], Model)
    result = 0
    for i in range(0, len(data)):

        if ((classe == data[str(i)]["class"]) & (data[str(i)]["bool"] == False)):
            result += 1

    return result


def trueNegative(classeOption,Model):
    data = Model[1]
    data.sort()
    result = 0

    for classe in data:

        if (classe != classeOption):
            result += 1

    return result


def falseNegative(classeOption, Model):
    data = Model[1]
    data.sort()
    result = 0

    for classe in data:

        if (classe == classeOption):
            result += 1

    return result


def precision(classe, Model):
    return truePositive(classe,Model) / (
    truePositive(classe, Model) + falsePositive(classe, Model))


def recall(classe, Model):
    return truePositive(classe, Model) / (falseNegative(classe, Model))

Model=constructModel(1500, False)

with open('dicoClass.json') as json_data:
    dico = json.load(json_data)

Exo3.createliste(dico)

print(precision("Positif",Model))
print(precision("Negatif", Model))

print("=========================")
Model=constructModel(1500, True)

print(precision("Positif", Model))
print(precision("Negatif", Model))



