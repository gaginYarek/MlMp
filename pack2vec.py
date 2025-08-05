import pandas
import json
import itertools

df = pandas.read_excel('СборДанныхBI_20250520_145108.XLSX', usecols=['Узел', 'Пакет', 'УзелУИД', 'РодительУИД', 'СвойствоУИД', 'ГруппаУИД'])
print(df.head())

edges = {uid: list() for uid in df['УзелУИД'].unique()}
edges['root'] = list()

packs = {uid: pack for uid, pack in zip(df['УзелУИД'], df['Пакет'])}
groups = {uid: group for uid, group in zip(df['УзелУИД'], df['ГруппаУИД'])}
values = {uid: value for uid, value in zip(df['УзелУИД'], df['Узел'])}

for parent, node in zip(df['РодительУИД'], df['УзелУИД']):
    edges[parent if parent == parent else 'root'].append(node)
    
def dfs(uid: str, path: list[tuple[str, str]], result: list[tuple[str, list[tuple[str, str]]]]):
    children = edges[uid]
    if len(children) == 0:
        result.append((packs[uid], path.copy()))
    else:
        for child in children:
            path.append((groups[child], values[child]))
            dfs(child, path, result)
            path.pop()

result = []
dfs('root', [], result)

group_uids = {uid: i for uid, i in zip(df['ГруппаУИД'].unique(), itertools.count(start=0))}
vec_result = []
for package in result:
    vec = [''] * len(group_uids)
    for group, value in package[1]:
        vec[group_uids.get(group)] = value

    vec_result.append({'package': package[0], 'properties': vec})

with open('human_package_paths.json', 'w', encoding='utf_8') as file:
    json.dump(vec_result, file, ensure_ascii=False, indent=4)

with open('human_group_uids_mapping.json', 'w', encoding='utf_8') as file:
    json.dump(group_uids, file, ensure_ascii=False, indent=4)
