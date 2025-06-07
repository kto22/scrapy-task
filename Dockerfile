FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scrapy_task/ /app/scrapy_task/
COPY scrapy.cfg /app/

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /app/scrapy_task/ /app/scrapy_task/
COPY --from=builder /app/scrapy.cfg /app/

RUN mkdir -p /app/data

ENV PYTHONPATH=/app
ENV PATH="/usr/local/bin:${PATH}"

CMD ["python", "-m", "scrapy", "crawl", "alkoparser_spider"] 