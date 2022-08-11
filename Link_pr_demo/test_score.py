import codecs
import json

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
    file1 = "data_qy_8_90/entities.tsv"
    file2 = "data_qy_8_90/relations.tsv"
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
    dataloader("data_qy_8_90/kg_qy_8_9000000_TransE_entity.npy","data_qy_8_90/kg_qy_8_9000000_TransE_relation.npy"
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
    index = faiss.IndexFlatIP(300)
    index.add(np.ascontiguousarray(entity_embedding))
    distance, match_idx = index.search(feature, 10)
    pre=[]
    for line in match_idx:
        for i in line:
            pr=id2entity[int(i)]
            pre.append(pr)
    return(pre)


def smi(input_en):

    h=entity2id[input_en]
    head = torch.tensor(entity_dict[h]).reshape(1,-1).numpy()
    index = faiss.IndexFlatIP(300)
    index.add(np.ascontiguousarray(entity_embedding))
    distance, match_idx = index.search(head, 10)
    pre=[]
    for line in match_idx:
        for i in line:
            pr=id2entity[int(i)]
            pre.append(pr)
    return(pre)

