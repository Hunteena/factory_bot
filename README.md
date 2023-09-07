# Django REST API для отправки сообщений боту Telegram
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
