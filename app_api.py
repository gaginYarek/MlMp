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
curl -X POST http://127.0.0.1:5000/predict_model -H "Content-Type: application/json" -d "{\"Pclass\": 3, \"Age\": 22.0, \"Fare\": 7.2500}"
'''

from fastapi import FastAPI, Request, HTTPException
import pickle
import pandas as pd
from pydantic import BaseModel

app = FastAPI()

# Загрузка модели из файла pickle
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

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

       'Бренд.KEFF PREMIUM by RODENSTOCK', 'Бренд.NIKON', 'Бренд.KEFF WL',
       'Вертекс в пробной оправе.0', 'Дизайн линзы.Прочее',
       'Индивидуальность.Стандартные', 'Индивидуальность.Оптимизированные',
       'Индивидуальность.Индивидуальные', 'Исключения METS.Нет',
       'Исключения METS.Да', 'Материал линзы ОЛ.Полимер',
       'Материал линзы ОЛ.Стекло', 'Материал линзы ОЛ.Поликарбонат',
       'Минимальный коридор прогрессии.0',
       'Положение оптического центра.По глазу',
       'Положение оптического центра.По веку', 'Призма ОЛ.Нет',
       'Светопропускание.Поляризационные', 'Тип линзы.Офисный прогрессив',
       'Тип линзы.Полный прогрессив', 'Индекс преломления'
    IndecsPrelom: float
    Age: float
    Fare: float

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
        'Pclass': [input_data.Pclass],
        'Age': [input_data.Age],
        'Fare': [input_data.Fare]
    })

    # Предсказание
    predictions = model.predict(new_data)

    # Преобразование результата в человеко-читаемый формат
    result = "Survived" if predictions[0] == 1 else "Not Survived"

    return {"prediction": result}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
