from cogdl import experiment
from cogdl.datasets.kg_data import KnowledgeGraphDataset
import os.path as osp

class Test_kgDatset(KnowledgeGraphDataset):
    def __init__(self, data_path="/cogdl_demo"):
        dataset = "data"
        path = osp.join(data_path, dataset)
        super((Test_kgDatset), self).__init__(path, dataset)
    def download(self):
        pass
    
dataset =Test_kgDatset()
experiment(dataset=dataset, model="transe",do_test=False,do_valid=False,epochs=2000,batch_size=1024,embedding_size=1000)
