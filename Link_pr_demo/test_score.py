import torch
from torch import nn
import numpy as np
import operator
import faiss
entity2id={}
relation2id={}
entity_dict = {}
relation_dict = {}


def TransE(head, relation):
    score =head + relation 
    return score
def dataloader(entity_file, relation_file):
    file1 = "/cogdl_demo/data/entity2id.txt"
    file2 = "/cogdl_demo/data/relation2id.txt"
    with open(file1, encoding='utf-8') as fin:      
        for line in fin:
            eid, entity = line.strip().split('\t')
            entity2id[entity] = int(eid)

    with open(file2, encoding='utf-8') as fin:       
        for line in fin:
            rid, relation = line.strip().split('\t')
            relation2id[relation] = int(rid)

    entity_embedding=np.load(entity_file)
    for i,value in enumerate (entity_embedding):
        entity_dict[i] = value  

    relation_embedding=np.load(relation_file)
    for i, value in enumerate(relation_embedding):
        relation_dict[i] = value 
    return entity_dict, relation_dict,entity_embedding,relation_embedding  
entity_dict, relation_dict,entity_embedding,relation_embedding = \
    dataloader("/cogdl_demo/Link_pr_demo/data/entity_embedding.npy","/cogdl_demo/Link_pr_demo/data/relation_embedding.npy"
                )
rank_head={}
id2entity = dict([val, key] for key, val in entity2id.items())
id2relation = dict([val, key] for key, val in relation2id.items())
key=True
def rank(input_en,input_re):
    h=entity2id[input_en]
    r=relation2id[input_re]
    head = torch.tensor(entity_dict[h])
    relation = torch.tensor(relation_dict[r])
    feature = TransE(head, relation).reshape(1,-1).numpy()
    index = faiss.IndexFlatIP(1000) #1000为embedding_size
    index.add(np.ascontiguousarray(entity_embedding))
    distance, match_idx = index.search(feature, 10)
    pre=[]
    for line in match_idx:
        for i in line:
            pr=id2entity[int(i)]
            pre.append(pr)
    #print("预测",pre)
    return(pre)


def smi(input_en):

    h=entity2id[input_en]
    head = torch.tensor(entity_dict[h]).reshape(1,-1).numpy()
    index = faiss.IndexFlatIP(1000)
    index.add(np.ascontiguousarray(entity_embedding))
    distance, match_idx = index.search(head, 10)
    pre=[]
    for line in match_idx:
        for i in line:
            pr=id2entity[int(i)]
            pre.append(pr)
    #print("预测",pre)
    return(pre)

