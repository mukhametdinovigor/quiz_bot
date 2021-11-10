# Чат боты с викториной для Telegram и VK

Бот отправляет вопросы, можно либо ответить на вопрос, либо сдаться и получить правильный ответ.

Пообщаться с ботом можно:

- в Телеграм [@Tg_Quiz_Mif_Bot](https://t.me/Tg_Quiz_Mif_Bot)
- Вконтакте в группе [QuizBot](https://vk.com/public208694766) кликнуть на `Написать сообщение`

Также пример работы ботов можно посмотреть на гифке

- Бот для Telegram

![бот для Telegram](examples/examination_tg.gif)

- Бот для VK

![бот для VK](examples/examination_vk.gif)



## Как запустить

Скачайте код:
```sh
git clone https://github.com/mukhametdinovigor/quiz_bot.git
```

Перейдите в каталог проекта:
```sh
cd quiz_bot
```

[Установите Python](https://www.python.org/), если этого ещё не сделали.

Проверьте, что `python` установлен и корректно настроен. Запустите его в командной строке:
```sh
python --version
```

В каталоге проекта создайте виртуальное окружение:
```sh
python -m venv venv
```
Активируйте его. На разных операционных системах это делается разными командами:
- Windows: `.\venv\Scripts\activate`
- MacOS/Linux: `source venv/bin/activate`


Установите зависимости в виртуальное окружение:
```sh
pip install -r requirements.txt
```

У вас должен быть [зарегистрированный бот в Telegram](https://telegram.me/BotFather)

## Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` в корне проекта
и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступны переменные:
- `TG_TOKEN` — токен рабочего бота в телеграм.
- `VK_TOKEN` — токен Вконтакте
- `REDIS_PASSWORD` — пароль к базе данных Redis
- `REDIS_ENDPOINT` - адрес базы данных Redis
- `REDIS_PORT` - порт  
- `BUG_REPORTING_BOT_TOKEN` - токен бота в телеграм, куда будут отправлятся сообщения об ошибках
- `CHAT_ID` - ваш chat_id в телеграм


Запустите ботов:

- Телеграм

```sh
python tg_bot.py
```

- Вконтакте, для запуска бота напишите - `Привет`

```sh
python vk_bot.py
```

## Цели проекта

Код написан в учебных целях на курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
