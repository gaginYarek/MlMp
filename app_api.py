'''
Давайте создадим простое API с тремя ручками: одна для предсказания выживания (/predict), 
другая для получения количества сделанных запросов (/stats), и третья для проверки работы API (/health).

Шаг 1: Установка необходимых библиотек
Убедитесь, что у вас установлены необходимые библиотеки:
pip install fastapi uvicorn pydantic scikit-learn pandas

Шаг 2: Создание app_api.py
Шаг 3: Запустите ваше приложение: python app_api.py
Шаг 4: Тестирование API
Теперь вы можете протестировать ваше API с помощью curl или любого другого инструмента для отправки HTTP-запросов.

Проверка работы API (/health)
curl -X GET http://127.0.0.1:5000/health
curl -X GET http://127.0.0.1:5000/stats
curl -X POST http://127.0.0.1:5000/predict_model -H "Content-Type: application/json" -d "{\"Degr0_8\": 0, \"Degr1_5\": 0, \"Brend_TOKAI\": 0, \"Brend_ESSILOR\": 0, \"Brend_KEFF_PREMIUM_by_RODENSTOCK\": 0, \"Brend_NIKON\": 0, \"Brend_KEFF_WL\": 0, \"Vertex_v_probnoi_oprave_0\": 0, \"Dizain_linzy_Prochee\": 0, \"Individualnost_Standartnye\": 0, \"Individualnost_Optimizirovannye\": 0, \"Individualnost_Individualnye\": 0, \"Isklucheniya_METS_Net\": 0, \"Isklucheniya_METS_Da\": 0, \"Material_linzy_OL_Polimer\": 0, \"Material_linzy_OL_Steklo\": 0, \"Material_linzy_OL_Polikarbons\": 0, \"Minimalnyi_koridor_progressii_0\": 0, \"Polozhenie_opticheskogo_tsentra_Po_glazu\": 0, \"Polozhenie_opticheskogo_tsentra_Po_veku\": 0, \"Prizma_OL_Net\": 0, \"Svetoproppuskaniye_Polarizatsionnye\": 1, \"Tip_linzy_Ofisnyi_progressiv\": 0, \"Tip_linzy_Polnyi_progressiv\": 0, \"Indeks_prelomleniya\": 1.5}"
'''

from fastapi import FastAPI, Request, HTTPException
import pickle
import pandas as pd
from pydantic import BaseModel
from vec2pack import *

app = FastAPI()

# Загрузка модели из файла pickle
with open('model.pkl', 'rb') as f:
    loadModels = pickle.load(f)

# Счетчик запросов
request_count = 0

# Модель для валидации входных данных
class PredictionInput(BaseModel):

    Degr0_8: int 
    Degr1_5: int
    Brend_TOKAI: int
    Brend_ESSILOR: int
    Brend_KEFF_PREMIUM_by_RODENSTOCK: int
    Brend_NIKON: int
    Brend_KEFF_WL: int
    Vertex_v_probnoi_oprave_0: int
    Dizain_linzy_Prochee: int
    Individualnost_Standartnye: int
    Individualnost_Optimizirovannye: int
    Individualnost_Individualnye: int
    Isklucheniya_METS_Net: int
    Isklucheniya_METS_Da: int
    Material_linzy_OL_Polimer: int
    Material_linzy_OL_Steklo: int
    Material_linzy_OL_Polikarbons: int
    Minimalnyi_koridor_progressii_0: int
    Polozhenie_opticheskogo_tsentra_Po_glazu: int
    Polozhenie_opticheskogo_tsentra_Po_veku: int
    Prizma_OL_Net: int
    Svetoproppuskaniye_Polarizatsionnye: int
    Tip_linzy_Ofisnyi_progressiv: int
    Tip_linzy_Polnyi_progressiv: int
    Indeks_prelomleniya: float

vec2pack = Vec2Pack('СборДанныхBI_20250520_145108.XLSX')

@app.get("/stats")
def stats():
    return {"request_count": request_count}

@app.get("/health")
def health():
    return {"status": "OK"}

@app.post("/predict_model")
def predict_model(input_data: PredictionInput):
    global request_count
    request_count += 1

    # Создание DataFrame из данных
    new_data = pd.DataFrame({

        'Degr.0,8': [input_data.Degr0_8],
        'Degr.1,5': [input_data.Degr1_5],
        'Бренд.TOKAI': [input_data.Brend_TOKAI],
        'Бренд.ESSILOR': [input_data.Brend_ESSILOR],
        'Бренд.KEFF PREMIUM by RODENSTOCK': [input_data.Brend_KEFF_PREMIUM_by_RODENSTOCK],
        'Бренд.NIKON': [input_data.Brend_NIKON],
        'Бренд.KEFF WL': [input_data.Brend_KEFF_WL],
        'Вертекс в пробной оправе.0': [input_data.Vertex_v_probnoi_oprave_0],
        'Дизайн линзы.Прочее': [input_data.Dizain_linzy_Prochee],
        'Индивидуальность.Стандартные': [input_data.Individualnost_Standartnye],
        'Индивидуальность.Оптимизированные': [input_data.Individualnost_Optimizirovannye],
        'Индивидуальность.Индивидуальные': [input_data.Individualnost_Individualnye],
        'Исключения METS.Нет': [input_data.Isklucheniya_METS_Net],
        'Исключения METS.Да': [input_data.Isklucheniya_METS_Da],
        'Материал линзы ОЛ.Полимер': [input_data.Material_linzy_OL_Polimer],
        'Материал линзы ОЛ.Стекло': [input_data.Material_linzy_OL_Steklo],
        'Материал линзы ОЛ.Поликарбонат': [input_data.Material_linzy_OL_Polikarbons],
        'Минимальный коридор прогрессии.0': [input_data.Minimalnyi_koridor_progressii_0],
        'Положение оптического центра.По глазу': [input_data.Polozhenie_opticheskogo_tsentra_Po_glazu],
        'Положение оптического центра.По веку': [input_data.Polozhenie_opticheskogo_tsentra_Po_veku],
        'Призма ОЛ.Нет': [input_data.Prizma_OL_Net],
        'Светопропускание.Поляризационные': [input_data.Svetoproppuskaniye_Polarizatsionnye],
        'Тип линзы.Офисный прогрессив': [input_data.Tip_linzy_Ofisnyi_progressiv],
        'Тип линзы.Полный прогрессив': [input_data.Tip_linzy_Polnyi_progressiv],
        'Индекс преломления': [input_data.Indeks_prelomleniya]

    })

    lenses = new_data
    predicted_results_vec = []

    for index, _ in lenses.iterrows():
        predicted_values_by_group = {}
        for column, model in loadModels.items():
            if model == None:
                predicted_values_by_group[column] = {}
                continue

            predicted_values_by_group[column] = {value: prob for prob, value in zip(model.predict_proba(lenses.iloc[[index]])[0], model.classes_)}

        predicted_results_vec.append(predicted_values_by_group)
        

    predicted_results_pack = []

    for pack_vec in predicted_results_vec:
        predicted_results_pack.append(vec2pack.get_package(pack_vec))

    # Преобразование результата в человеко-читаемый формат
    result = predicted_results_pack[0]

    return {"prediction": result}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)