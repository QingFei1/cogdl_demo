# cogdl_demo
```
1.需要提供entity2id.txt和relation2id.txt，实体和关系对应索引的文件
2.需要提供使用transe模型训练好的embedding.npy文件
3.在test_score.py中替换文件路径，运行kg_app.py即可
```
```
使用test_score.rank预测尾实体和test_score.smi预测相似实体
```


## Requirements
```
python
flask
faiss
```




