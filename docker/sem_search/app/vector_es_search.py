import requests
import json
hostname = "mpgpu02.southcentralus.cloudapp.azure.com"
headers = {'Content-Type': 'application/json'}
def search_by_vec(vec, version="v1"):
    if version == "v1":
       url = "http://{}:9200/test_01/_search".format(hostname) 
    if version == "v2":
        url = "http://{}:9200/test_02/_search".format(hostname)
    d = {
        "_source" : ['sent', 'title', 'author'],
        "query": {
            "script_score": {
                "query": {
                    "match_all": {}
                },
                "script": {
                    "source": "cosineSimilarity(params.queryVector, doc['bert-chinese-emb'])",
                    "params": {
                    "queryVector": vec
                    }
                }
            }
        }
    }
    resp = requests.post(url, data=json.dumps(d),headers=headers)
    return resp

def get_vec4query(query, version="v1"):
    if version == "v1":
        url = "http://{}:8500/api/emb/v1".format(hostname) 
    if version == "v2":
        url = "http://{}:8500/api/emb/v2".format(hostname)
    resp = requests.post(url, json.dumps([query]), headers=headers)
    d = resp.json()
    assert len(d) == 1
    return d[0]


if __name__ == "__main__":
    vec = get_vec4query("山有木兮木有枝，心悦君兮君不知。")
    res = search_by_vec(vec)
    print(res)
