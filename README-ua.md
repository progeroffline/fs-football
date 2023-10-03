# FlashScore Football Library

## Зміст

- [Мови](#мови)
- [Огляд](#огляд)
- [Особливості](#особливості)
- [Встановлення](#встановлення)
- [Використання](#використання)
- [Автор](#автор)

### Мови

- [🇺🇸 Англійська](README.md)
- [🇺🇦 Українська](README_UA.md)

### Огляд

Ця бібліотека Python дозволяє вам легко отримувати дані про футбольні матчі з веб-сайту FlashScore (flashscore.com). Вона розроблена для асинхронної роботи, забезпечуючи швидке та ефективне отримання даних. У деяких частинах бібліотеки використовується бібліотека `grequests` для покращення продуктивності.

### Особливості

- Асинхронне отримання даних: Бібліотека використовує асинхронний підхід Python з використанням фреймворку `asyncio` для здійснення асинхронних HTTP-запитів, що дозволяє отримувати дані з FlashScore ефективно.

- Історичні дані матчів: Можливість доступу до історичних даних про минулі футбольні матчі, включаючи результати матчів, статистику команд та бомбардирів.

### Встановлення

```shell
git clone ...
cd ...
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### Використання

Ось простий приклад використання бібліотеки для отримання історичних даних матчів:

```python
from flashscore import FlashscoreApi

api = FlashscoreApi()
countries = api.get_countries()

for country in countries:
    leagues = country.get_leagues()

    for league in leagues:
        season = league.get_season()

        current_season = season[0]
        for match in current_season.get_matches():
            print(match)
            match.load_content()
            print(match)
```

Ось простий приклад використання бібліотеки для отримання даних про сьогоднішні матчі:

```python
from flashscore import FlashscoreApi

api = FlashscoreApi()
today_matches = api.get_today_matches()

for i, match in enumerate today_matches:
    match.load_content()
```

### Автор

- GitHub: [progeroffline](https://github.com/progeroffline)

Якщо у вас виникнуть питання або проблеми, будь ласка, не соромтеся відкривати питання на GitHub.

Щасливого парсингу! 🚀📈
