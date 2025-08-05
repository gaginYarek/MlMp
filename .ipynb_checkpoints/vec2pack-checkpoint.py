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

with open('predicted_values_by_group.json', encoding='utf_8') as file:
    predicted_results_vec_dejsoned = json.load(file)

result = []

for pack_vec in predicted_results_vec_dejsoned:
    uid = 'root'
    while len(edges[uid]) > 0:
        children = {values[child]: child for child in edges[uid]}
        group_uid = groups[edges[uid][0]]
        sorted = [(prob, value) for value, prob in pack_vec[group_uid].items() if value in children.keys()]
        sorted.sort(reverse=True)
        uid = children[sorted[0][1]]

    result.append(packs[uid])
        
with open('selected_packages.json', 'w', encoding='utf_8') as file:
    json.dump(result, file, ensure_ascii=False, indent=4)
