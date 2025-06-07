
import json
import time
import os
from typing import Dict, List, Optional, Any, Iterable
from urllib.parse import urlencode

import scrapy
from scrapy import Request
from scrapy.http import Response

class AlkotekaDetailSpider(scrapy.Spider):
    name = "alkoparser_spider"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'FEED_FORMAT': 'json',
        'FEED_URI': 'result.json',
        'DOWNLOAD_DELAY': 0.5,
        'ROBOTSTXT_OBEY': False,
    }
    CITY_UUID = "4a70f9e0-46ae-11e7-83ff-00155d026416"
    BASE_API_URL = "https://alkoteka.com/web-api/v1/product"
    ITEMS_PER_PAGE = 20

    def start_requests(self) -> Iterable[Request]:
        urls_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "urls.txt")
        if not os.path.exists(urls_path):
            self.logger.error(f"Файл с ссылками не найден: {urls_path}")
            return
        with open(urls_path, encoding="utf-8") as f:
            for line in f:
                category_url = line.strip()
                if not category_url:
                    continue
                yield self._create_category_request(category_url)


    def _create_category_request(self, category_url: str) -> Request:
        category_slug = category_url.split("/")[-1]
        api_url = self._build_list_api_url(category_slug, page=1)
        return Request(
            url=api_url,
            callback=self.parse_product_list,
            meta={"category_slug": category_slug, "page": 1}
        )


    def _build_list_api_url(self, category_slug: str, page: int = 1) -> str:
        params = {
            "city_uuid": self.CITY_UUID,
            "page": page,
            "per_page": self.ITEMS_PER_PAGE,
            "root_category_slug": category_slug,
        }
        return f"{self.BASE_API_URL}?{urlencode(params)}"


    def _build_detail_api_url(self, slug: str) -> str:
        return f"{self.BASE_API_URL}/{slug}?city_uuid={self.CITY_UUID}"


    def parse_product_list(self, response: Response) -> Iterable[Request]:
        data = json.loads(response.text)
        products = data.get("results", [])
        for product in products:
            if slug := product.get("slug"):
                yield self._create_product_request(slug, product.get("product_url"))
        if data.get("meta", {}).get("has_more_pages"):
            yield self._create_pagination_request(response)


    def _create_product_request(self, slug: str, product_url: str) -> Request:
        return Request(
            url=self._build_detail_api_url(slug),
            callback=self.parse_product_detail,
            meta={"product_url": product_url}
        )


    def _create_pagination_request(self, response: Response) -> Request:
        next_page = response.meta["page"] + 1
        next_api_url = self._build_list_api_url(
            category_slug=response.meta["category_slug"],
            page=next_page,
        )
        return Request(
            url=next_api_url,
            callback=self.parse_product_list,
            meta={"category_slug": response.meta["category_slug"], "page": next_page}
        )


    def parse_product_detail(self, response: Response) -> Dict[str, Any]:
        product = json.loads(response.text)["results"]

        return {
            "timestamp": int(time.time()),
            "RPC": product.get("uuid", ""),
            "url": response.meta["product_url"],
            "title": self._build_title(product),
            "marketing_tags": self._get_marketing_tags(product),
            "brand": self._get_brand(product),
            "section": self._get_section(product),
            "price_data": self._get_price_data(product),
            "stock": self._get_stock_data(product),
            "assets": self._get_assets_data(product),
            "metadata": self._get_metadata(product),
            "variants": 1,
        }


    def _build_title(self, product: Dict[str, Any]) -> str:
        name = product.get("name", "")
        filter_labels = product.get("filter_labels", [])
        for label in filter_labels:
            if title := label.get("title"):
                name += f", {title}"
        return name


    def _get_marketing_tags(self, product: Dict[str, Any]) -> List[str]:
        tags = []
        if product.get("new"):
            tags.append("Новинка")
        if product.get("gift_package"):
            tags.append("Подарочная упаковка")
        return tags


    def _get_brand(self, product: Dict[str, Any]) -> str:
        for block in product.get("description_blocks", []):
            if block.get("code") == "brend":
                if values := block.get("values"):
                    if brand_name := values[0].get("name"):
                        return brand_name
        return ""


    def _get_section(self, product: Dict[str, Any]) -> List[str]:
        parent_name = ""
        category_name = ""
        if category := product.get("category"):
            category_name = category.get("name", "")
            if parent := category.get("parent"):
                parent_name = parent.get("name", "")
        return [parent_name, category_name]


    def _get_price_data(self, product: Dict[str, Any]) -> Dict[str, Any]:
        original_price = product.get("prev_price")
        current_price = product.get("price")
        if original_price is None and current_price is None:
            return {"current": None, "original": None, "sale_tag": ""}
        if original_price is None:
            return {"current": float(current_price), "original": float(current_price), "sale_tag": ""}
        if current_price is None:
            return {"current": float(original_price), "original": float(original_price), "sale_tag": ""}
        has_discount = original_price != current_price
        sale_tag = ""
        if has_discount and current_price != 0:
            try:
                discount = int((1 - original_price / current_price) * 100)
                sale_tag = f"Скидка {discount}%"
            except Exception:
                sale_tag = ""
        return {
            "current": float(current_price) if has_discount else float(original_price),
            "original": float(original_price),
            "sale_tag": sale_tag
        }


    def _get_stock_data(self, product: Dict[str, Any]) -> Dict[str, Any]:
        quantity = int(product.get("quantity_total", 0))
        return {
            "in_stock": quantity > 0,
            "count": quantity
        }


    def _get_assets_data(self, product: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "main_image": product.get("image_url", ""),
            "set_images": [""],
            "view360": [""],
            "video": [""]
        }


    def _get_metadata(self, product: Dict[str, Any]) -> Dict[str, Any]:
        metadata = {}
        if text_blocks := product.get("text_blocks"):
            if text_blocks and len(text_blocks) > 0:
                metadata["__description"] = text_blocks[0].get("content", "")
        else:
            metadata["__description"] = ""
        if article := product.get("vendor_code"):
            metadata["article"] = article
        for label in product.get("filter_labels", []):
            metadata[label["filter"]] = label["title"]
        return metadata
