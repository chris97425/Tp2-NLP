import  re, codecs, os, csv


def createliste(i):

    questions = codecs.open("questions.txt", "r", 'utf-8')
    questionsread = questions.read()
    questions.close()

    listecl = re.findall("([QLDPT][A-Z]+[NLY]) .*", questionsread)
    listequestion = re.findall(" (.*)", questionsread)

    listeclass = ["Classe"]+listecl
    listefea = ["Question"]+listequestion

    if(i=="bim"):

        return listeclass

    if(i=="bam"):

        return listefea

def constructcsv():

    csv_out = open('mycsv.csv', 'w')
    mywriter = csv.writer(csv_out,delimiter=',',lineterminator='\r\n')
    rows = zip(createliste("bim"),createliste("bam"))
    mywriter.writerows(rows)
    csv_out.close()

