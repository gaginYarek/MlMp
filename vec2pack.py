import pandas
import json


class Vec2Pack:
    def __init__(self, tree_file: str):
        df = pandas.read_excel(tree_file, usecols=['Узел', 'Пакет', 'УзелУИД', 'РодительУИД', 'СвойствоУИД', 'ГруппаУИД'])
        # print(df.head())

        self._edges = {uid: list() for uid in df['УзелУИД'].unique()}
        self._edges['root'] = list()

        self._packs = {uid: pack for uid, pack in zip(df['УзелУИД'], df['Пакет'])}
        self._groups = {uid: group for uid, group in zip(df['УзелУИД'], df['ГруппаУИД'])}
        self._values = {uid: value for uid, value in zip(df['УзелУИД'], df['Узел'])}

        for parent, node in zip(df['РодительУИД'], df['УзелУИД']):
            self._edges[parent if parent == parent else 'root'].append(node)

    def get_package(self, feature_values: dict[str, dict[str, float]]) -> str:
        uid = 'root'
        while len(self._edges[uid]) > 0:
            children = {self._values[child]: child for child in self._edges[uid]}
            group_uid = self._groups[self._edges[uid][0]]
            sorted = [(prob, value) for value, prob in feature_values[group_uid].items() if value in children.keys()]
            sorted.sort(reverse=True)
            uid = children[sorted[0][1]]

        return self._packs[uid]


if __name__ == '__main__':
    vec2pack = Vec2Pack('СборДанныхBI_20250520_145108.XLSX')

    with open('predicted_values_by_group.json', encoding='utf_8') as file:
        predicted_results_vec_dejsoned = json.load(file)

    result = []
    for pack_vec in predicted_results_vec_dejsoned:
        result.append(vec2pack.get_package(pack_vec))

    with open('selected_packages.json', 'w', encoding='utf_8') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)
