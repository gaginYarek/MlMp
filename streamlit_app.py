import streamlit as st 
import requests
from requests.exceptions import ConnectionError

ip_api = "5.159.103.200"
port_api = "5000"

# Заголовок приложения
st.title("Классификация линзы в пакет Мастера продаж")

# Ввод данных
st.write("Введите данные линзы:")

# Выпадающее меню для выбора OHE
Degr0_8 = st.selectbox("Degr.0,8", [0, 1])
Degr1_5 = st.selectbox("Degr.1,5", [0, 1])
Brend_TOKAI = st.selectbox("Бренд.TOKAI", [0, 1])
Brend_ESSILOR = st.selectbox("Бренд.ESSILOR", [0, 1])
Brend_KEFF_PREMIUM_by_RODENSTOCK = st.selectbox("Бренд.KEFF PREMIUM by RODENSTOCK", [0, 1])
Brend_NIKON = st.selectbox("Бренд.NIKON", [0, 1])
Brend_KEFF_WL = st.selectbox("Бренд.KEFF WL", [0, 1])
Vertex_v_probnoi_oprave_0 = st.selectbox("Вертекс в пробной оправе.0", [0, 1])
Dizain_linzy_Prochee = st.selectbox("Дизайн линзы.Прочее", [0, 1])
Individualnost_Standartnye = st.selectbox("Индивидуальность.Стандартные", [0, 1])
Individualnost_Optimizirovannye = st.selectbox("Индивидуальность.Оптимизированные", [0, 1])
Individualnost_Individualnye = st.selectbox("Индивидуальность.Индивидуальные", [0, 1])
Isklucheniya_METS_Net = st.selectbox("Исключения METS.Нет", [0, 1])
Isklucheniya_METS_Da = st.selectbox("Исключения METS.Да", [0, 1])
Material_linzy_OL_Polimer = st.selectbox("Материал линзы ОЛ.Полимер", [0, 1])
Material_linzy_OL_Steklo = st.selectbox("Материал линзы ОЛ.Стекло", [0, 1])
Material_linzy_OL_Polikarbons = st.selectbox("Материал линзы ОЛ.Поликарбонат", [0, 1])
Minimalnyi_koridor_progressii_0 = st.selectbox("Минимальный коридор прогрессии.0", [0, 1])
Polozhenie_opticheskogo_tsentra_Po_glazu = st.selectbox("Положение оптического центра.По глазу", [0, 1])
Polozhenie_opticheskogo_tsentra_Po_veku = st.selectbox("Положение оптического центра.По веку", [0, 1])
Prizma_OL_Net = st.selectbox("Приза ОЛ.Нет", [0, 1])
Svetoproppuskaniye_Polarizatsionnye = st.selectbox("Светопропускание.Поляризационные", [0, 1])
Tip_linzy_Ofisnyi_progressiv = st.selectbox("Тип линзы.Офисный прогрессив", [0, 1])
Tip_linzy_Polnyi_progressiv = st.selectbox("Тип линзы.Полный прогрессив", [0, 1])


# Текстовое поле для ввода индекса преломления с проверкой на число
Indeks_prelomleniya = st.text_input("Индекс преломления", value=1.5)
#if not Indeks_prelomleniya.isinstance():
#    st.error("Please enter a valid number for Fare.")

# Кнопка для отправки запроса
if st.button("Предсказание"):
        # Подготовка данных для отправки
        data = {
            'Degr0_8': int(Degr0_8),
            'Degr1_5': int(),
            'Brend_TOKAI': int(),
            'Brend_ESSILOR': int(),
            'Brend_KEFF_PREMIUM_by_RODENSTOCK': int(),
            'Brend_NIKON': int(),
            'Бренд.KEFF WL': int(),
            'Brend_KEFF_WL': int(),
            'Vertex_v_probnoi_oprave_0': int(),
            'Dizain_linzy_Prochee': int(),
            'Individualnost_Standartnye': int(),
            'Individualnost_Optimizirovannye': int(),
            'Individualnost_Individualnye': int(),
            'Isklucheniya_METS_Net': int(),
            'Isklucheniya_METS_Da': int(),
            'Material_linzy_OL_Polimer': int(),
            'Material_linzy_OL_Steklo': int(),
            'Material_linzy_OL_Polikarbons': int(),
            'Minimalnyi_koridor_progressii_0': int(),
            'Polozhenie_opticheskogo_tsentra_Po_glazu': int(),
            'Polozhenie_opticheskogo_tsentra_Po_veku': int(),
            'Prizma_OL_Net': int(),
            'Svetoproppuskaniye_Polarizatsionnye': int(),
            'Tip_linzy_Ofisnyi_progressiv': int(),
            'Tip_linzy_Polnyi_progressiv': int(),
            'Indeks_prelomleniya': float()
        }

        try:
            # Отправка запроса к Flask API
            response = requests.post(f"http://{ip_api}:{port_api}/predict_model", json=data)

            # Проверка статуса ответа
            if response.status_code == 200:
                prediction = response.json()["prediction"]
                st.success(f"Prediction: {prediction}")
            else:
                st.error(f"Request failed with status code {response.status_code}")
        except ConnectionError as e:
            st.error(f"Failed to connect to the server")