import scrapy
import json
from urllib.parse import unquote
from typing import Dict, Union

from avitoscraper.items import PropertyItem
from helpers import get_last_url, save


class PropertyspiderSpider(scrapy.Spider):
    name = "propertyspider"
    allowed_domains = ["www.avito.ma"]
    start_urls = ["https://www.avito.ma/fr/maroc/appartements-%C3%A0_vendre"]

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1
    }

    def __init__(self):
        self.parsed = unquote(get_last_url())
        self.is_last_ad_url_saved = False

    def parse(self, response: scrapy.http.Response):
        """
        Parse the main response and process property listings.

        :param response: The response object containing web page data.
        :type response: scrapy.http.Response
        :return: Follows links to property pages.
        :rtype: scrapy.http.Request or scrapy.item
        """
        properties = response.css("a.sc-1jge648-0")

        if not self.is_last_ad_url_saved:
            save(properties[0].css("a").attrib["href"])
            self.is_last_ad_url_saved = True

        for property in properties:
            url = property.css("a").attrib["href"]
            url = unquote(url)
            if url == self.parsed:
                return

            yield response.follow(url, callback=self.parse_property_page)

        if href := self.get_next_page_url(response):
            yield response.follow(href, callback=self.parse)

    def parse_property_page(self, response: scrapy.http.Response):
        """
        Parse a property page and extract details.

        :param response: The response object for a property page.
        :type response: scrapy.http.Response
        :return: Yields property details.
        :rtype: Scrapy item
        """
        json_data = response.css("#__NEXT_DATA__::text").get()
        try:
            data = json.loads(json_data)

            ad_info = data["props"]["pageProps"]["componentProps"]["adInfo"]["ad"]
            property_item = PropertyItem()

            property_item["url"] = response.url
            property_item["ad_title"] = ad_info["subject"]
            property_item["description"] = ad_info["description"]
            property_item["price"] = ad_info["price"].get("value", None)
            property_item["address"] = ad_info["location"]["address"]
            property_item["city"] = ad_info["location"]["city"]["name"]
            property_item["category"] = ad_info["category"]["name"]
            property_item["is_new_building"] = ad_info["isImmoneuf"]
            property_item["phone"] = ad_info["phone"]
            property_item["published_date"] = ad_info["listTime"]
            property_item["seller_name"] = ad_info["seller"]["name"]
            property_item["habitable_size"] = self.total_surface(
                ad_info, "primary", "habitable_size"
            )
            property_item["total_surface"] = self.total_surface(
                ad_info, "secondary", "size"
            )

            yield property_item
        except (ValueError, KeyError):
            self.logger.error(f"Failed to parse data for URL: {response.url}")

    def total_surface(self, data: Dict, key: str, value: Union[str, int]) -> int:
        """
        Extract surface value from property data based on a given key and value.

        :param data: A dictionary containing property information.
        :type data: dict
        :param key: The key to identify the category of the surface (e.g., 'primary', 'secondary').
        :type key: str
        :param value: The value associated with the key, indicating the specific surface to extract.
        :type value: str
        :return: The extracted surface value matching the provided key and value, or an empty string if not found.
        :rtype: int
        """
        for param in data.get("params", {}).get(key, []):
            try:
                if param.get("key") == value:
                    return int(param.get("value", ""))
            except KeyError:
                pass
        return 0

    def get_next_page_url(self, response: scrapy.http.Response) -> Union[str, None]:
        """
        Extract the URL of the next page for pagination from a Scrapy response.

        :param response: The response object containing web page data.
        :type response: scrapy.http.Response
        :return: The URL of the next page for pagination, or None if not found.
        :rtype: str or None
        """
        last_a = response.css(
            "div.sc-116g21e-1 a:not(.activePage):last-child::attr(href)"
        ).get()
        return last_a
