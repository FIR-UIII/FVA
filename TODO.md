1. Добавить образ докер контейнера для более удобного и быстрого запуска
    docker build -t fva_app -f Dockerfile_fva .
    docker build -t fva_postgres_db -f Dockerfile_postgres .

    TEST:
    docker create network fva_net
    docker run -d --name fva_postgres_db -p 5432:5432 --network=fva_net fva_postgres_db
    docker run -d --name fva_app -p 8888:8888 --network=fva_net fva_app

    VIA 
    docker-compose up

2. Добавить правила nuclei / semgrep для поиска и анализа уязвимостей
3. Добавить уязвимости:
-
-
-
4. Cделать заглушки в случае невалидных логина или пароля или необходиомсти аутентификации
5. csrf добавить подключение к БД psql
6. перенести в env основные конфигурационные настройки