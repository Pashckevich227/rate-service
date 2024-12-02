# Api для подсчета стоимости страховки

## Технологии использованные в проекте:
* FastApi
* PostgreSQL 
* SQLalchemy
* Alembic
* Docker-compose
* Kafka
____
## Установка
1. Склонировать проект к себе: `https://github.com/Pashckevich227/rate-service.git`
2. Зайти в папку `rate-service`, выполнить `docker-compose up -d`
* Проверить, не запустился ли бекенд раньше Kafka `docker logs rate-service-backend-1`. Если в сообщении лога присутсивует ошибка `NoBrokersAvaible`, то снова выполнить `docker restart rate-service-backend-1`
## Применить миграции к базе данных
1. Зайти на контейнер бекенда `docker exec -ti rate-service-backend-1 bash`
2. Выполнить миграцию `alembic upgrade head`
![image](https://github.com/user-attachments/assets/fba64d62-df25-48ea-aa55-cd53c2c6bdf3)
3. Зайти на контейнер postgres и добавить данные о цене страховки 
`docker exec -it postgres_database psql -U root -h database -d postgres` 
Пароль `root`

Добавить данные: `INSERT INTO price (id, price) VALUES (1, 100), (2, 50), (3, 200);`

В ответ должны получить <b>INSERT 0 3</b>

4. В swagger `http://localhost:8080/docs` выполнить POST запрос на добавление новых данных о страховке
   
![image](https://github.com/user-attachments/assets/68c7eca5-e3b3-4b72-9f40-3b464c67fb13)

Формат ответа при успехе
![image](https://github.com/user-attachments/assets/389d9233-b5bf-4939-b7b4-b94a71151af0)

Добавленные данные можно посмотреть в контейнере базы через `SELECT * FROM rate;` и `SELECT * FROM price;`

![image](https://github.com/user-attachments/assets/4a5d632d-6830-4281-a72a-4fcd53c05d58)

![image](https://github.com/user-attachments/assets/a5c24572-054a-47fe-a371-6b7f29c656fd)


## Теперь необходимо связать цену страховки со страховкой по ключу
Для этого необходимо отправить PATCH запрос на изменение данных о страховке. Следуя описанию запроса, добавим связь для категории `Other` равную `price_id=2` для первой записи из таблицы rate

![image](https://github.com/user-attachments/assets/5c401b30-8dd2-46d8-a0b4-8c53341af4ae)

Теперь, когда страховка имеет цену и тариф, сможем рассчитать ее стоимость, выполнив GET запрос 
![image](https://github.com/user-attachments/assets/50618a6a-d52b-48c3-9b42-1658d5c41216)

P.s Добавлен функционал добавления записей из файлов (принимается формат JSON внутри файла). Для примера можно воспользоваться приложенным файлом `data.json`

![image](https://github.com/user-attachments/assets/98134eac-c2f5-4f58-af40-93e212867050)

Также добавлено логирование через Kafka батч. Для просмотра совершенных действий:
1. Зайти на контейнер Kafka `docker exec -ti kafka bash`
2. `kafka-console-consumer --bootstrap-server kafka:29092 --topic test.events --from-beginning`

<img width="1512" alt="Снимок экрана 2024-12-02 в 21 26 34" src="https://github.com/user-attachments/assets/1b835b9d-00c3-48ed-ad91-82242df13341">
   

