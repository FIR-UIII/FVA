1. Добавить образ докер контейнера для более удобного и быстрого запуска
    docker build -t fva_app -f Dockerfile_fva .
    docker build -t fva_postgres_db -f Dockerfile_postgres .

    TEST:
    docker run -d --name fva_postgres_db -p 5432:5432 fva_postgres_db
    docker run -d --name fva_app -p 8888:8888 --link fva_postgres_db:fva_postgres_db fva_app

2. Добавить правила nuclei / semgrep для поиска и анализа уязвимостей
3. Добавить уязвимости:
-
-
-
4. Cделать заглушки в случае невалидных логина или пароля или необходиомсти аутентификации
5. csrf добавить подключение к БД psql
6. перенести в env основные конфигурационные настройки