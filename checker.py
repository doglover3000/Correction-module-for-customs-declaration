import joblib

def check_declaration(df):
    issues = []
    for idx, row in df.iterrows():
        row_issues = []
        # словарь соответствий
        country_to_currency = {
            'Китай': 'CNY',
            'Индия': 'INR',
            'Турция': 'TRY',
            'ОАЭ': 'AED',
            'Саудовская Аравия': 'SAR',
            'Египет': 'EGP',
            'Бразилия': 'BRL',
            'ЮАР': 'ZAR',
            'Иран': 'IRR',
            'Аргентина': 'ARS',
            'Мексика': 'MXN',
            'Индонезия': 'IDR',
            'Пакистан': 'PKR',
            'Таиланд': 'THB',
            'Вьетнам': 'VND',
            'Казахстан': 'KZT',
            'Узбекистан': 'UZS',
            'Киргизия': 'KGS',
            'Азербайджан': 'AZN',
            'Армения': 'AMD',
            'Сербия': 'RSD',
            'Венесуэла': 'VES',
            'Куба': 'CUP',
            'Беларусь': 'BYN',
            'Сирия': 'SYP',
            'Никарагуа': 'NIO',
            'Бангладеш': 'BDT',
            'Мьянма': 'MMK',
            'Эфиопия': 'ETB',
            'Алжир': 'DZD'
        }

        # 1. Проверка валюты
        expected_currency = country_to_currency.get(row["country"])
        if expected_currency and row["currency"] != expected_currency:
            row_issues.append(
                f"для страны '{row['country']}' ожидается валюта '{expected_currency}', но указана '{row['currency']}'")

        # 2. Проверка полей
        tnved = str(row["tnved"])
        if len(tnved) != 10:
            row_issues.append(
                f"недействительный код ТН ВЭД {row["tnved"]}"
            )

        # 3. Проверка кода ТНВЭД с помощью модели
        model = joblib.load("ml-model/tnved_model.pkl")
        try:
            x_text = [row["name"]]
            predicted_code = model.predict(x_text)[0]
            declared_code = str(row["tnved"])[:10]  # сравниваем по 10 знакам
            if str(predicted_code) != declared_code:
                row_issues.append(
                    f"модель предсказывает ТНВЭД {predicted_code}, указано {declared_code}"
                )
        except Exception as e:
            row_issues.append(f"Ошибка при предсказании ТНВЭД: {e}")

        if row_issues:
            issues.append({"Номер товара": idx, "Товар": row["name"], "Ошибка": row_issues})

    return issues
