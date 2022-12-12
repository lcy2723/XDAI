# (初始化) Elastic Search

配置环境:

```
tar  -zxvf  elasticsearch-7.8.1-linux-x86_64.tar.gz
mv  elasticsearch-7.8.1   elasticsearch7.8
./bin/elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v7.8.1/elasticsearch-analysis-ik-7.8.1.zip
```

授权:

```
chown -R tsq:tsq  /data/tsq/elasticsearch7.8
```

在`/data/tsq/elasticsearch7.8/bin`**开启后台服务**

```
./elasticsearch -d
```

检查链接:

```
curl 'http://0.0.0.0:9200'
```

先预处理数据:

```
python -m database.elastic_search --task 'preprocess' --model 'MoocArticle' --max_ctx_window 128
```

处理出来1.6G，但是tags等标签没有加

再初始化Index,不断往里面存文章:

```
python -m database.elastic_search --task 'build_index' --model 'MoocArticle' --init
```

注意: **还没写加课程名字、检索查询的代码**

# (文档检索) Elastic Search

```
tmux a -t 130b
```

```
conda activate testretri
```

```
CUDA_VISIBLE_DEVICES=7 python fix_his_questions.py --data_dir '/data/tsq/xiaomu/qa' --test_file '问题答案标注.xlsx' --test_version bm25
```

