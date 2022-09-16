#! /bin/bash
while true
do
checkglmapi=$(ps -ef | grep "uvicorn plm_app:app --port 9546" | grep -v "grep") # 查找reloader process
checksenapi=$(ps -ef | grep "uvicorn sentsim_api:app --port 9504" | grep -v "grep") # 查找reloader process
if [ "$checkglmapi" ] 
then
    echo "glmapi进程已存在"
    glmapipid=$(echo ${checkglmapi} | cut -d ' ' -f 2)
    echo ${glmapipid}
    searchglm=$(ps -ef | grep ${glmapipid} | grep -v "grep")
    checkglm=$(echo ${searchglm} | grep "/home/tsq/miniconda3/envs/xdai/bin/python -c from multiprocessing") #查找glm server process
    if [ "$checkglm" ] # 经常出现的问题是reloader process仍然运行但是glm server停止，因此需要检查两次
    then
        echo "glm存在"
    else
        echo "glm不存在"
        # kill -9 ${glmapipid} # 先杀掉reloader process再重启，不然uvicorn会出现address already in use错误
        source /home/tsq/miniconda3/bin/activate xdai
        # date # 显示问题日期
        # glmlogdate=$(echo $(date) | cut -d ' ' -f 3)
        # cd /home/tsq/user/lcy/XDAI
        # CUDA_VISIBLE_DEVICES=4 nohup bash tools/deploy_plm.sh > glm_server_${glmlogdate}.log &
fi
else
    echo "glmapi进程不存在"
    source /home/tsq/miniconda3/bin/activate xdai
    # date # 显示问题日期
    # glmlogdate=$(echo $(date) | cut -d ' ' -f 3)
    # cd /home/tsq/user/lcy/XDAI
    # CUDA_VISIBLE_DEVICES=4 nohup bash tools/deploy_plm.sh > glm_server_${glmlogdate}.log &
fi
if [ "$checksenapi" ]
then
    echo "sentsimapi进程已存在"
    senapipid=$(echo ${checksenapi} | cut -d ' ' -f 2)
    echo ${senapipid}
    searchsen=$(ps -ef | grep ${senapipid} | grep -v "grep")
    checksen=$(echo ${searchsen} | grep "/home/tsq/miniconda3/envs/xdai/bin/python -c from multiprocessing")
    if [ "checksen" ]
    then
        echo "sen存在"
    else
        echo "sen不存在"
        # kill -9 ${senapipid} # 先杀掉reloader process再重启，不然uvicorn会出现address already in use错误
        source /home/tsq/miniconda3/bin/activate xdai
        # date # 显示问题日期
        # senlogdate-$(echo $(date) | cut -d ' ' -f 3)
        # cd /home/tsq/user/lcy/XDAI
        # nohup bash tools/deploy_sentsim.sh > similarity_server_${senlogdate}.log &
    fi
else
    echo "sentsimapi进程不存在"
    source /home/tsq/miniconda3/bin/activate xdai
    # date # 显示问题日期
    # senlogdate-$(echo $(date) | cut -d ' ' -f 3)
    # cd /home/tsq/user/lcy/XDAI
    # nohup bash tools/deploy_sentsim.sh > similarity_server_${senlogdate}.log &
fi
sleep 10
done
