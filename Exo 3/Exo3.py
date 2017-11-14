from re import findall as fa
from codecs import open
from os import listdir
import json
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk import word_tokenize
from nltk.tag import StanfordPOSTagger
from nltk.tokenize import RegexpTokenizer
import csv


import nltk

import string
# nltk.download('HunposTagger')
# newpath = r'../neg+pos'
# if not path.exists(newpath):
#     makedirs(newpath)

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

# def creationDicoTxt(dico):
#
#     list_dir = listdir("../")
#
#     if not ("../dico.json" in list_dir):
#
#         with open('../dico.json', 'w', "utf-8") as outfile:
#             json.dump(str(dico), outfile)
#         # txt_out = open('../dico.json', 'w','utf-8')
#         # txt_out.write()
#         # txt_out.close()
#
# # creationDicoTxt(createDicoClasse())

def lowercaseConvert():
    dico = createDicoClasse()

    for key in dico:

        try:
            dico[key]["Text"]=dico[key]["Text"].lower()

        except KeyError:
            pass


    return dico

# print(lowercaseConvert())

def stopWords():

    dico=lowercaseConvert()

    # print(getcwd(),listdir(getcwd()))

    stop_words = set(stopwords.words("english"))

    for key in dico:

        words = dico[key]["Text"].split()
        a = ""

        for r in words:
            if not r in stop_words:
                a = a + str(" "+r)

        dico[key]["Text"] = a

    return dico

# print(stopWords()["100"]["Text"])

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
# print(stemmingDico())
# print(getcwd())
jar = '../stanford-postagger-full-2017-06-09/stanford-postagger.jar'
model = '../stanford-postagger-full-2017-06-09/models/english-left3words-distsim.tagger'
# print(stemmingDico())
# ps = StanfordPOSTagger(model, jar)


def correctStringPosttag(tocorrect, listTag,ps):

    # ps=nltk.tag.
    text = ps.tag(word_tokenize(tocorrect))
    print(text)
    # print(text)
    result=""

    for (word,tag) in text:

        if not(tag in listTag):
            result=result +" "+word

    return result

ps=["CC","CD","DT","EX","FW","IN","JJ","JJR","JJS","LS","MD","NN","NNS","NNP","NNPS","PDT","POS","PRP","RB","RBR","RBS","RP","SYM","TO","UH","VB","VBD","VBG","VBN","VBP","VBZ","WDT","WP","WRB","PRP$","WP$"]
listeToRemove=["CC","CD","DT","EX","FW","IN","LS","MD","PDT","POS","PRP","RP","SYM","TO","UH","WDT","WP","WRB","PRP$","WP$"]
# a=correctStringPosttag("Whether you're planning to read through Crowley's Book of Thoth for the first time, or if you think you know every little thing Crowley was getting at with it, this book is going to be equally useless to you. Several of Crowley's diagrams from the Book of Thoth are reprinted in this book much more clearly, but sadly that's the only good thing about this book. The book is filled with a lot of fluff. Duquette tells many useless anecdotes of Crowley's and Harris' lives, and constantly excuses and defends Crowley's character against those who would consider him a devil worshiper. Duquette explains in the book that he initially thought that when he first found Crowley's works, so perhaps its some sort of atonement. But the argument really has no place in a book like this where the reader has already come to terms with Crowley's character.Through out the Book of Thoth Crowley constantly alludes to and makes references to other works and various myths and systems. Having a reference book that explained all of these things would be an invaluable aid. Unfortunately Duquette doesn't do this. His background information is base and scarce. He does spend some time explaining about Thelema and Kabbalah, but as one would expect from a chapter long explanation of subjects like this, Duquette doesn't give nearly enough information to understand Crowley's works, and what he does give is easy enough to find elsewhere.As for offering anything knew or shedding some understanding on Crowley's work, Duquette outright fails. At times it seems as if Duquette doesn't even understand Crowley or the Book of Thoth and the associated tarot deck. I don't think the man even understands tarot in general (and Duquette's own tarot deck is evidence of this too). At his best, Duquette only manages to rephrase what Crowley had to say in the book of Thoth. Typically though a lot of what Crowley was getting at is complete lost in Duquette's work, a lot of it no doubt because Duquette never really understood Crowley at anything but a very base level.Reading through the Book of Thoth, there are a few ways in which Duquette could have made his book better. Crowley's phonetic translation of the I Ching doesn't follow the current standard, and sometimes the differences are confusing, especially if the reader is not already familiar with the I Ching. A key showing Crowley's translation and the standard translation would've been helpful. Likewise Crowley rarely wrote on astrology, despite astrology being alluded to many times through the Book of Thoth, and what he did write is hard to find. A chapter explaining Crowley's views on astrology would've been great. If that wasn't possible, then a list of books on astrology that were similar to what Crowley was working with would have been helpful. However Duquette's solution is to just tell the reader to go find some books on astrology to read.Duquette's book isn't useful as a reference to Crowley's work. Duquette doesn't seem to understand Crowley most of the time, and fails to adequatley explain Crowley's ideas. Besides some new-agey nonsense, like assigning celebrities to the court cards based on their birthdays, Duquette doesn't offer any new ideas or insights into Crowley's work. Except for a few nice diagrams (which are common enough and easy to find), there isn't anything worthwhile contained in this book. At least not anything you won't get out of reading Crowley's Book of Thoth",["VB","NN"])
# print(a)
def writeDico(dico):

    with open('../dico.json', 'w',"utf-8") as outfile:
        json.dump(dico, outfile)

def postDico(listTag):
    ps= StanfordPOSTagger(model, jar)

    dico=stemmingDico()
    i=0
    for key in dico:

        dico[key]["Text"]=correctStringPosttag(dico[key]["Text"],listTag,ps)
        print(i)
        i=i+1
    return dico


# print(d["1"])
#     # for key in d:
#     #     print(key)
# print(sorted(d))
# print(d["1"]["Class"])
#
# def posnegClassJson(dico):
#
#     pos = open("../pos.json", "w", "utf-8")
#     neg = open("../neg.json", "w", "utf-8")
#     a={}
#     b={}
#     i=0
#     j=0
#     for key in dico:
#
#         if (dico[key]["Class"]=="Positif"):
#             a[i]={"Text":dico[key]["Text"]}
#             i+=1
#
#         elif (dico[key]["Class"]=="Negatif"):
#             b[j] = {"Text": dico[key]["Text"]}
#             j+=1
#
#     with open('../pos.json', 'w', "utf-8") as outfile:
#         json.dump(a, outfile)
#     with open('../neg.json', 'w', "utf-8") as outfile:
#         json.dump(b, outfile)
#
#     pos.close()
#     neg.close()
#
# posnegClassJson(d)

def createliste(i,dico):




    classe = ["Classe"]
    text = ["Texte"]


    for key in dico:

        classe = classe + [dico[key]["Class"]]
        text = text + [dico[key]["Text"]]

    csv_out = open('forClassification.csv', 'w')
    mywriter = csv.writer(csv_out, delimiter=',', lineterminator='\r\n')
    rows = zip(classe, text)
    mywriter.writerows(rows)
    csv_out.close()

