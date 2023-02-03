# LittleMu: Deploying an Online Virtual Teaching Assistant via Heterogeneous Sources Integration and Chain-of-Teach Prompts

## 1 Introduction

LittleMu is a virtual MOOC teaching assistant with minimum labeled trainding data. Empowered by a meta concept graph, tuning-free propting of large models and "Chain-of-Teach" or personalized emotional support prompts, LittleMu provides question answering service and emotional support services.

The features of LittleMu are as fellows:

* High-coverage Q&A: LittleMu integrates knowledge sources such as concept-centered MOOCCubeX, web search engine, platform FAQ, thereby supporting accurate Q&A for a wide range of questions.
* Instructional Complex Reasoning: We design delicate demonstrations named “Chain-of-Teach” prompts to exploit the emergent reasoning ability of large-scale pre-trained model, which enables LittleMu to handle complex uncollected questions.
* Easy-to-adapt Transferability: Empowered by a meta concept graph and tuning-free prompting of large models, LittleMu does not require further training stage to be applied to new courses.
* Diverse Educational Functions: Except for the necessary functions for dealing with above questions, we develop several other educational services such as personalized emotional supporting for further lifting the user experience in real-world MOOC scenarios.

## 2 Run the Code

Settings to be modified are in

```
config/conf.ini
```

#### 1. Set up PLM API

```bash
nohup bash tolls/deploy_plm.sh > glm_server.log &
```

#### 2. Set up mongoDB

#### 3. Knowledge Explore

```bash
python tools/knowledge/explore.py -t init -fdata/seed_concept.json
```

```bash
nohup python tools/knowledge/explore.oy -t update -fdata/seed_concept.json -i 1 > ke_server.log
```

#### 4. Set up Sentence similarity API

```bash
nohup bash tools/deploy_sentsim.sh > similarity_server.log &
```

#### 5. Set up LittleMu API

in api/

```bash
nohup uvicorn xiaomu_api:app --host [your host] --port [your port] --reload > xiaomu.log &
```


