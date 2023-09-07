# Django REST API для отправки сообщений боту Telegram

## Схема работы:
1. Пользователь регистрируется в системе. При регистрации указывает логин, пароль и имя.
2. Пользователь находит бота в Telegram и начинает чат с ним.
3. В личном кабинете генерирует токен и привязывает к своему чату этот токен, отправив его боту.
4. Пользователь отправляет на API своё сообщение. В этот момент бот сразу дублирует его в Telegram.
   Пользователь получает только свои сообщения.
   
## Локальный запуск проекта

Клонировать репозиторий
```shell
git clone https://github.com/Hunteena/factory_bot
```
Перейти в директорию [factorybot](factorybot)
```shell
cd factorybot
```
Создать файл _.env_, аналогичный файлу [.env.example](factorybot/.env.example). 
([Инструкция](https://core.telegram.org/bots/features#creating-a-new-bot), как получить токен telegram-бота)

Запустить сервер
```shell
docker-compose up --build
```
После успешнего запуска сервера доступна документация Swagger:  
http://localhost:8000/api/schema/swagger-ui/
