from elasticsearch import Elasticsearch
import requests, os, json, glob, codecs, re
os.chdir("indexpays/")
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


def listjson():

    listfile = glob.glob("*.json")
    return listfile

# print(listjson())

def constructindex():

    # by default we connect to localhost:9200
    es.indices.create(index='indexpays', ignore=400)
    file=listjson()
    file.sort()
    # print(file)

    i = 0

    for keys in file:

        paysinfo=json.load(open(keys,encoding="utf-8"))
        # print(keys)
        es.index(index='pays', doc_type='paysdef', id=i, body=paysinfo)
        # print("ok")
        i+=1

def queryelastic(query):

    # if(question==1):
    result={
            "query": {
                "more_like_this": {
                    "fields":  ["Background"],
                    "like": query,
                    "analyzer":"stop",
                    "min_term_freq": 1,
                    "max_query_terms": 12
                }
            }
        }

    #
    # elif(question==2):
    #     result= {
    #         "query": {
    #             "more_like_this": {
    #                 "fields": ["Geography-note"],
    #                 "like": query,
    #                 "min_term_freq": 1,
    #                 "max_query_terms": 12
    #             }
    #         }
    #     }
    #
    # elif(question==3):
    #     result = {
    #         "query": {
    #             "more_like_this": {
    #                 "fields":  ["Economy-overview"],
    #                 "like": query,
    #                 "min_term_freq": 0,
    #                 "max_doc_freq": 5
    #             }
    #         }
    #     }

    return result

def result_txt():

    # file = open("../testfile.json", "w")
    # file.write(str(es.search(index="pays", doc_type="paysdef", body=question3)))
    # file.close()

    requetes = open("../liste_requetes.txt", "r")
    liste_requetes=requetes.read()
    requetes.close()

    quest = re.findall("(Q[0-9]+)[\W]([\w ]*[a-z])",liste_requetes)

    for i in range(0,len(quest)):
        # file = open("../testfile.json", "w")
        data = json.dumps(es.search(index="pays",doc_type="paysdef",body=queryelastic(quest[i][1])))
        j = json.loads(data)
        print(j)
        # file.write(data)
        # file.close()
        print(len(j["hits"]["hits"]))
        # print(j["hits"]["hits"][0]["_source"]["name"])

    # file = open("../resultfile.txt", "w")
    # file.write("Q1 "+j["hits"]["hits"][0]["_source"]["name"])
    # file.close()

    # result.close()

# result_txt()

print(es.search(index="pays",doc_type="paysdef",body=queryelastic("neighbours of Canada")))
