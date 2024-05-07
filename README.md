# Сервис для сбора денег (донатов) на разные нужды

### RESTful API, который позволяет:
1. Создать пользователя и групповой сбор
2. Задонатить на групповой сбор
3. Просмотреть существующие сборы и донаты

При создании сбора и доната на почту приходит письмо об успехе.

## Запуск проекта:
1. Клонировать репозиторий
    ```
    git@github.com:Smitona/Collect_donations.git
    ```
2. Перейти в директорию проекта и создать env. файл с переменные по примеру env_example:
    ```
    cd Collect_donations/
    ```
3. Перейти в папку с файлом docker-compose и запустить проект:
   ```
   docker-compose up -d
   ```
4. Скопировать статику бекенда:
   ```
   docker compose exec backend python manage.py collectstatic
   ```
   ***Для Windows вторая команда в PowerShell***
   ```
   docker compose exec backend cp -r /static/. /backend_static/static/
   ```
5. Импортировать тестовые данные в БД:
   ```
   docker compose exec python manage.py import_data
   ```

Документацию можно будет открыть по ссылке [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/api/v1/swagger/)

---
### Стек ⚡
<img src="https://img.shields.io/badge/Python-black?style=for-the-badge&logo=Python&logoColor=DodgerBlue"/> <img src="https://img.shields.io/badge/Django-black?style=for-the-badge&logo=Django&logoColor=darkturquoise"/> <img src="https://img.shields.io/badge/postgresql-black?style=for-the-badge&logo=postgresql&logoColor=Cyan"/> <img src="https://img.shields.io/badge/Celery-black?style=for-the-badge&logo=Celery&logoColor=darkturquoise"/> <img src="https://img.shields.io/badge/redis-black?style=for-the-badge&logo=redis&logoColor=white/">
