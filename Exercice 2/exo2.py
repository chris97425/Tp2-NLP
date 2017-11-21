import  re, codecs, csv


def createListe():
    result=[]
    questions = codecs.open("questions.txt", "r", 'utf-8')
    questionsRead = questions.read()
    questions.close()
    listeCl = re.findall("([QLDPT][A-Z]+[NLY]) .*", questionsRead)
    listequestion = re.findall(" (.*)", questionsRead)
    listeClass = ["Classe"]+listeCl
    listeQuery = ["Question"]+listequestion
    result.append(listeClass)
    result.append(listeQuery)

    return result

def constructCsv():

    csv_out = open('mycsv.csv', 'w')
    mywriter = csv.writer(csv_out,delimiter=',',lineterminator='\r\n')
    rows = zip(createListe()[0],createListe()[1])
    mywriter.writerows(rows)
    csv_out.close()

