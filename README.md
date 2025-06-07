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

Пример вывода:
{"timestamp": 1749301552, "RPC": "19107788-ed8a-11e8-80f6-00155d2fc707", "url": "https://alkoteka.com/product/sidr-medovukha-1/puare-grushevyy-sidr-polusladkiy_39012", "title": "Пуаре Грушевый сидр полусладкий, 0.33 Л, Сидр, медовуха, Россия, Скидка", "marketing_tags": [], "brand": "Медоварус", "section": ["Слабоалкогольные напитки", "Сидр, медовуха"], "price_data": {"current": 115.0, "original": 135.0, "sale_tag": "Скидка -17%"}, "stock": {"in_stock": true, "count": 545}, "assets": {"main_image": "https://web.alkoteka.com/storage/product/63/e8/39012_image.png", "set_images": [""], "view360": [""], "video": [""]}, "metadata": {"__description": "В аромате - тона груши дюшес и спелого яблока. Вкус дополняеться тонами меда. Послевкусие среднее.", "article": 39012, "obem": "0.33 Л", "categories": "Сидр, медовуха", "strana": "Россия", "tovary-so-skidkoi": "Скидка"}, "variants": 1},
{"timestamp": 1749301553, "RPC": "19107784-ed8a-11e8-80f6-00155d2fc707", "url": "https://alkoteka.com/product/sidr-medovukha-1/medovyy-napitok-khmelnoy-med-tradicionnyy_39020", "title": "Медовый напиток Хмельной мёд Традиционный, 0.33 Л, Сидр, медовуха, Россия, Скидка", "marketing_tags": [], "brand": "Медоварус", "section": ["Слабоалкогольные напитки", "Сидр, медовуха"], "price_data": {"current": 115.0, "original": 135.0, "sale_tag": "Скидка -17%"}, "stock": {"in_stock": true, "count": 597}, "assets": {"main_image": "https://web.alkoteka.com/storage/product/bc/f2/39020_image.png", "set_images": [""], "view360": [""], "video": [""]}, "metadata": {"__description": "В аромате - тона меда и пряностей. Вкус дополняеться тонами миндаля, фруктов. Послевкусие средней продолжителььности.", "article": 39020, "obem": "0.33 Л", "categories": "Сидр, медовуха", "strana": "Россия", "tovary-so-skidkoi": "Скидка"}, "variants": 1},
{"timestamp": 1749301553, "RPC": "19107778-ed8a-11e8-80f6-00155d2fc707", "url": "https://alkoteka.com/product/sidr-medovukha-1/medovyy-napitok-khmelnoy-med-vishnevyy-krik_39010", "title": "Медовый напиток Хмельной мёд Вишнёвый Крик, 0.33 Л, Сидр, медовуха, Россия, Скидка", "marketing_tags": [], "brand": "Медоварус", "section": ["Слабоалкогольные напитки", "Сидр, медовуха"], "price_data": {"current": 125.0, "original": 145.0, "sale_tag": "Скидка -15%"}, "stock": {"in_stock": true, "count": 569}, "assets": {"main_image": "https://web.alkoteka.com/storage/product/20/27/39010_image.png", "set_images": [""], "view360": [""], "video": [""]}, "metadata": {"__description": "Вишневый ламбик, сваренный в европейских традициях XIX века, производится из сока спелой вишни «Шампань», крик обладает насыщенным слегка терпким вкусом. Оригинальность напитку придает долгое послевкусие с приятной кислинкой и легким миндальным оттенком. Является продуктом естественного брожения.", "article": 39010, "obem": "0.33 Л", "categories": "Сидр, медовуха", "strana": "Россия", "tovary-so-skidkoi": "Скидка"}, "variants": 1},
