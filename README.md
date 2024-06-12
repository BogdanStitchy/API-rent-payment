![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-D82C20?style=for-the-badge&logo=redis&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-336791?style=for-the-badge)

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-003545?style=for-the-badge&logo=sqlalchemy)
![Pydantic](https://img.shields.io/badge/Pydantic-2D3748?style=for-the-badge&logo=pydantic)
![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery)
![Flower](https://img.shields.io/badge/Flower-306998?style=for-the-badge&logo=flower)

# API-rent-payment

## Оглавление

- [Описание](#описание)
- [Стек технологий](#стек-технологий)
- [Установка](#установка)
- [Конфигурация приложения](#конфигурация-приложения)
- [Структура базы данных](#структура-базы-данных)

## Описание

Система расчёта квартплаты для квартир в домах. Проект включает в себя модели данных «Дом», «Квартира», «Счётчик воды», «Тариф», а также функции и API для расчёта квартплаты, управления данными и выполнения расчётов в фоновом режиме с помощью Celery.

## Стек технологий

- **FastAPI**: для создания и управления RESTful API.
- **SQLAlchemy**: для ORM (Object-Relational Mapping) и взаимодействия с базой данных.
- **PostgreSQL**: в качестве базы данных.
- **Celery**: для выполнения задач в фоновом режиме.
- **Redis**: в качестве брокера и бэкенда для Celery.
- **Flower**: для мониторинга статуса Celery задач (http://localhost:5555/tasks).

## Установка
1. Клонируйте репозиторий:

```plaintext
   git clone https://github.com/BogdanStitchy/API-rent-payment.git
```

2. Перейдите в директорию проекта:

```plaintext
   cd API-rent-payment
```

3. Создайте файл для переменных окружения

  ```bash
echo > app\config\.env
  ```

После чего заполните данный файл любым удобным для вас способом в соответствии с
разделом [конфигурация](#конфигурация-приложения)

4. Для запуска FastAPI можно использовать веб-сервер uvicorn. Команда для запуска:

```bash
uvicorn app.main:app --reload
```  

Необходимо запускать команду, находясь в корневой директории проекта.

5. После чего нужно вручную запустить все сопутствующие инструменты:

* Celery

Для запуска Celery используется команда:

```bash
celery --app=app.tasks.celery:celery worker -l INFO -P solo
```

Обратите внимание, что `-P solo` используется только на Windows, так как у Celery есть проблемы с работой на Windows.

* Flower

Для запуска Flower используется команда

```bash
celery --app=app.tasks.celery:celery flower
``` 

После выполнения всех трех команд, приложение будет доступно по адресу **http://localhost:8000**
Flower будет доступно по адресу **http://localhost:5555**

## Конфигурация приложения

Расположение конфигурационного файла приложения: *app/config/.env*. Данный файл отвечает за конфигурацию fastAPI
приложения.
Содержимое файла *app/config/.env* следующее:

  ```dotenv
MODE=
LOG_LEVEL=
LOGIN_DB=
PASSWORD_DB=
NAME_DB=
HOST=
DB_PORT=
HASH_FUNCTION=
DIALECT_DB=
DRIVER_DB=
HOST_REDIS=

  
  ```

Файл заполняется без кавычек. В конце обязательно должна быть пустая строка.

* MODE - режим работы приложения. Доступны следующие варианты: "DEV", "TEST", "PROD"
* LOG_LEVEL - уровень логирования приложения по умолчанию
* LOGIN_DB - логин для базы данных
* PASSWORD_DB - пароль для базы данных
* NAME_DB - имя используемой базы данных
* HOST - хост на котором расположена используемая базы данных
* DB_PORT - порт для подключения на хосте для базы данных
* HASH_FUNCTION - используемая хеш функция для хеширования паролей
* DIALECT_DB - используемая СУБД. Для выбора возможных вариантов
  ознакомьтесь с [документацией](https://docs.sqlalchemy.org/en/20/core/engines.html)
* DRIVER_DB - драйвер для СУБД. Для выбора возможных вариантов
  ознакомьтесь с [документацией](https://docs.sqlalchemy.org/en/20/core/engines.html)
* HOST_REDIS - хост расположения redis

## Структура базы данных
Структура базы данных представлена на фото ниже:
![image](https://github.com/BogdanStitchy/API-rent-payment/assets/83240866/5e51587e-54a0-455d-85f6-ee29b44dd168)
