import pandas as pd
import json
import demjson3
from tqdm import tqdm
import csv

fileinput = pd.read_csv('../database/data/PROPER_v1.csv')
taskfile = pd.DataFrame(columns = ['A蛋白ID','A基因名称','A基因ID','A对应转录ENST','A对应蛋白ENSP','B蛋白ID','B基因名称','B基因ID','B对应转录ENST','B对应蛋白ENSP','来源物种','细胞类型L1','细胞类型L2','作用方向','数据来源','数据来源版本'
                                       ,'数据来源对应疾病','数据来源对应组织','可靠水平','质控状态','相互作用对象','相互作用类型','数据来源相互作用类型描述','相互作用权重','相互作用置信度','备注'])
for u in tqdm(range(len(fileinput))):
    i=u
    taskfile.loc[i, 'A基因名称'] = fileinput.loc[i, 'Gene1']
    taskfile.loc[i, 'B基因名称'] = fileinput.loc[i, 'Gene2']
    taskfile.loc[i, '细胞类型L1'] = fileinput.loc[i, 'Cell line specificity']
    taskfile.loc[i, '数据来源'] = 'proper'
    taskfile.loc[i, '质控状态'] = fileinput.loc[i, 'Potential background contamination']
    taskfile.loc[i, '相互作用对象'] = 'PPI'
    obj = {'Odds ratio':fileinput.loc[i, 'Odds ratio'],'BH-corrected p-value':fileinput.loc[i, 'BH-corrected p-value']}
    obj_json = demjson3.encode(obj)
    taskfile.loc[i, '备注'] = obj_json
##再次统一处理json的格式
bz = taskfile['备注']
bz_json = bz.to_json(orient='records', force_ascii=False)
bz_json = json.loads(bz_json)
taskfile['备注'] = bz_json
## nan转化为None
df = taskfile.where((taskfile.notna()),None)
##储存不要index，去掉可能的引号
df.to_csv('../project/proper/proper_formed.tsv',sep = '\t',index = False, quoting=csv.QUOTE_NONE, quotechar="",  escapechar="\\")