## Установка и запуск

### Через .venv

1. Клонируйте репозиторий:
```bash
git clone https://github.com/kto22/scrapy-task.git
cd scrapy-task
```

2. Создайте и активируйте виртуальное окружение:
```bash
python3 -m venv .venv
source .venv/bin/activate  # для Linux/Mac
# или
.venv\Scripts\activate  # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Запустите парсер:
```bash
python -m scrapy crawl alkoparser_spider -O result.json
```

### Через Docker

1. Клонируйте репозиторий:
```bash
git clone https://github.com/kto22/scrapy-task.git
cd scrapy-task
```

2. Создайте директорию для результатов:
```bash
mkdir -p data
```

3. Соберите Docker образ:
```bash
docker build -t scrapy-task .
```

4. Запустите контейнер:
```bash
docker run -v $(pwd)/data:/app/data scrapy-task
```

После завершения работы контейнера результаты парсинга будут доступны в директории `data/result.json` на вашем компьютере. Файл создается автоматически т.к. директория `data` монтирована в контейнер
