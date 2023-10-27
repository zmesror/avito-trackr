# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime


class AvitoscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Convert published_date to datetime
        date = adapter["published_date"]
        adapter["published_date"] = self._to_datetime(date)

        return item

    def _to_datetime(self, datetime_str):
        return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ")


import mysql.connector
from mysql.connector import errorcode
import sys


class SaveToMySQLPipeline:
    """
    A pipeline for saving scraped property data to a MySQL database.
    """

    def __init__(self):
        try:
            self.cnx = mysql.connector.connect(
                host="localhost", user="root", password=""
            )

            self.cursor = self.cnx.cursor()

            # Ensure the database exists or create it
            self.create_database()
            self.cursor.execute("USE avito_trackr")

            self.create_property_table()
        except mysql.connector.Error as err:
            sys.exit("MySQL Error: {}".format(err))

    def create_database(self):
        """
        Create avito_trackr database if it doesn't exist.
        """
        try:
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS avito_trackr")
        except mysql.connector.Error as err:
            sys.exit("MySQL Error: {}".format(err))

    def create_property_table(self):
        """
        Create the 'property' table with the necessary columns.
        """
        try:
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS property (
                id INT NOT NULL AUTO_INCREMENT,
                url VARCHAR(255) NOT NULL,
                ad_title TEXT NOT NULL,
                description TEXT,
                price DECIMAL(10, 2),
                address TEXT,
                city VARCHAR(255),
                category VARCHAR(255) NOT NULL,
                is_new_building TINYINT(1),
                phone VARCHAR(10),
                published_date DATETIME NOT NULL,
                seller_name VARCHAR(255) NOT NULL,
                habitable_size INT,
                total_surface INT,
                PRIMARY KEY (id),
                UNIQUE (url),
                INDEX idx_category (category),
                INDEX idx_published_date (published_date)
                )   
                """
            )
        except mysql.connector.Error as err:
            sys.exit("MySQL Error: {}".format(err))

    def process_item(self, item, spider):
        """
        Process an PropertyItem by inserting it into the 'property' table.

        :param item: The scraped property data.
        :type item: PropertyItem
        :param spider: The spider object.
        """
        try:
            sql = """
                INSERT INTO property (
                    url,
                    ad_title,
                    description,
                    price,
                    address,
                    city,
                    category,
                    is_new_building,
                    phone,
                    published_date,
                    seller_name,
                    habitable_size,
                    total_surface
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )"""

            values = (
                item["url"],
                item["ad_title"],
                item["description"],
                item["price"],
                item["address"],
                item["city"],
                item["category"],
                item["is_new_building"],
                item["phone"],
                item["published_date"],
                item["seller_name"],
                item["habitable_size"],
                item["total_surface"],
            )

            self.cursor.execute(sql, values)
            self.cnx.commit()
        except mysql.connector.Error as err:
            print("MySQL Error: {}".format(err))

        return item

    def close_spider(self, spider):
        """
        Close the cursor and the database connection when the spider is closed.

        :param spider: The spider object.
        """
        self.cursor.close()
        self.cnx.close()
