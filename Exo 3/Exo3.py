import json, csv
from re import findall as fa
from codecs import open
from os import listdir
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk import word_tokenize
from nltk.tag import StanfordPOSTagger
from nltk.tokenize import RegexpTokenizer

def stopWordsList(fichierStopTxt):

    fileStop = open(fichierStopTxt, "r", 'utf-8')
    fileStopForRE = fileStop.read()
    fileStop.close()
    listStopWords = fa("([a-z]+)", fileStopForRE)

    return listStopWords

def createDicoClasse():

    constructClasse={}

    list_neg = listdir("../Book/neg_Bk")
    list_pos = listdir("../Book/pos_Bk")

    number_files_neg = len(list_neg)
    number_files_pos = len(list_pos)

    for i in range(0,number_files_neg):
        try :
            questions = open("../Book/neg_Bk/" +list_neg[i], "r", 'utf-8')
            questionsread = questions.read()
            questions.close()

            constructClasse[str(i)] = {
                'Class': 'Negatif',
                'Text': questionsread,
                'nbStdelete': 0
            }
        except UnicodeDecodeError:

            pass

    for j in range(1,number_files_pos):
        try:
            questions = open("../Book/pos_Bk/" + list_pos[j], "r", 'utf-8')
            questionsread = questions.read()
            questions.close()

            constructClasse[str(i+j)] = {
                'Class': 'Positif',
                'Text': questionsread,
                'nbStdelete': 0
            }
        except UnicodeDecodeError:
            pass

    return constructClasse

def lowercaseConvert():

    dico = createDicoClasse()

    for key in dico:

        try:
            dico[key]["Text"]=dico[key]["Text"].lower()

        except KeyError:
            pass


    return dico

def stopWords():

    dico=lowercaseConvert()

    stop_words = set(stopwords.words("english"))

    for key in dico:

        words = dico[key]["Text"].split()
        a = ""

        for r in words:
            if not r in stop_words:
                a = a + str(" "+r)

        dico[key]["Text"] = a

    return dico

def deletePunc():

    dico=stopWords()

    tokenizer = RegexpTokenizer('\w+')

    for key in dico:

        arrayTokenWP = tokenizer.tokenize(dico[key]["Text"])
        a = ""

        for r in arrayTokenWP:

                a = a + str(" "+r)

        dico[key]["Text"] = a

    return dico

def stemmingDico():

    dico=deletePunc()
    ps = PorterStemmer()

    for key in dico:

        sentence = dico[key]["Text"]
        tokens=word_tokenize(sentence)
        a=""
        for words in tokens:
            a= a+" "+ps.stem(words)
            # print(a)
        dico[key]["Text"]=a

    return dico

jar = '../stanford-postagger-full-2017-06-09/stanford-postagger.jar'
model = '../stanford-postagger-full-2017-06-09/models/english-left3words-distsim.tagger'

def correctStringPosttag(tocorrect, listTag,ps):

    text = ps.tag(word_tokenize(tocorrect))
    print(text)
    result=""

    for (word,tag) in text:

        if not(tag in listTag):
            result=result +" "+word

    return result

ps=["CC","CD","DT","EX","FW","IN","JJ","JJR","JJS","LS","MD","NN","NNS","NNP","NNPS","PDT","POS","PRP","RB","RBR","RBS","RP","SYM","TO","UH","VB","VBD","VBG","VBN","VBP","VBZ","WDT","WP","WRB","PRP$","WP$"]
listeToRemove=["CC","CD","DT","EX","FW","IN","LS","MD","PDT","POS","PRP","RP","SYM","TO","UH","WDT","WP","WRB","PRP$","WP$"]

def writeDico(dico):

    with open('../dico.json', 'w',"utf-8") as outfile:
        json.dump(dico, outfile)

def postDico(listTag):
    ps= StanfordPOSTagger(model, jar)
    dico=stemmingDico()
    i=0
    for key in dico:
        dico[key]["Text"] = correctStringPosttag(dico[key]["Text"], listTag, ps)
        print(i)
        i=i+1
    return dico

def createliste(i,dico):

    classe = ["Classe"]
    text = ["Texte"]

    for key in dico:

        classe = classe + [dico[key]["Class"]]
        text = text + [dico[key]["Text"]]

def createCsv(classe,text):

    csv_out = open('forClassification.csv', 'w')
    mywriter = csv.writer(csv_out, delimiter=',', lineterminator='\r\n')
    rows = zip(classe, text)
    mywriter.writerows(rows)
    csv_out.close()

