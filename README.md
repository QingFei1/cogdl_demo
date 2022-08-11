# cogdl_demo
```
1.需要提供entities.tsv和relation.tsv，实体和关系对应索引的文件
2.需要提供使用transe模型训练好的embedding.npy文件
3.在test_score.py中替换文件路径，运行kg_app.py即可
```
```
由于demo使用的数据集中一些实体加了额外标签，故对输入的实体使用url来匹配数据集实体，
使用自己的数据，可在kg_app中删去url和判断逻辑，使用test_score.rank预测尾实体和test_score.smi预测相似实体，
```


## Requirements
```
python
flask
faiss
```




