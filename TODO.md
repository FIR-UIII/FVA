1. Добавить образ докер контейнера для более удобного и быстрого запуска
    docker build -t FVA_app -f Dockerfile_fva .
    docker build -t FVA_postgres_db -f Dockerfile_postgres .

    TEST:
    docker run -d --name FVA_postgres_db -p 5432:5432 FVA_postgres_db
    docker run -d --name FVA_app -p 80:80 --link FVA_postgres_db:FVA_postgres_db FVA_app

2. Добавить правила nuclei / semgrep для поиска и анализа уязвимостей
3. Добавить уязвимости:
-
-
-
