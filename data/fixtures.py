import mysql.connector

# Configuration for the test database
test_db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
}

# Sample data for fixtures
fixtures = [
    {
        "url": "https://example.ma/1",
        "ad_title": "Appartement au Centre de Casablanca",
        "description": "Appartement moderne avec vue imprenable.",
        "price": 750000.00,
        "address": "Avenue Mohammed V",
        "city": "Casablanca",
        "category": "Immobilier",
        "is_new_building": 1,
        "phone": "0123456789",
        "published_date": "2023-10-30 14:30:00",
        "seller_name": "Mohammed Ali",
        "habitable_size": 120,
        "total_surface": 150,
    },
    {
        "url": "https://example.ma/2",
        "ad_title": "Villa à Marrakech",
        "description": "Belle villa avec piscine près de la Palmeraie.",
        "price": 1500000.00,
        "address": "Palmeraie, Marrakech",
        "city": "Marrakech",
        "category": "Immobilier",
        "is_new_building": 0,
        "phone": "0987654321",
        "published_date": "2023-10-29 10:00:00",
        "seller_name": "Fatima Ahmed",
        "habitable_size": 250,
        "total_surface": 500,
    },
]


def create_test_database():
    try:
        # Connect to the MySQL server
        conn = mysql.connector.connect(**test_db_config)
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS test_avito")
        cursor.execute("USE test_avito")

        # Create the 'property' table
        cursor.execute(
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

        # Insert fixture data into the table
        for fixture in fixtures:
            cursor.execute(
                """
                INSERT INTO property (url, ad_title, description, price, address, city, category, is_new_building, phone, published_date, seller_name, habitable_size, total_surface)
                VALUES (%(url)s, %(ad_title)s, %(description)s, %(price)s, %(address)s, %(city)s, %(category)s, %(is_new_building)s, %(phone)s, %(published_date)s, %(seller_name)s, %(habitable_size)s, %(total_surface)s)
                """,
                fixture,
            )

        conn.commit()
        conn.close()
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")


if __name__ == "__main__":
    create_test_database()
