import pytest
import mysql.connector
from price import Price

# Initialize the Price class with test database connection
@pytest.fixture(scope="module")
def price_instance():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="test_avito"
        )
        yield Price(mydb)
        mydb.close()
    except mysql.connector.Error as err:
        pytest.fail(f"MySQL Error: {err}")

def test_mean_with_city(price_instance):
    result = price_instance.mean_all("Casablanca")
    assert result == (6250.00,)

def test_mean_without_city(price_instance):
    result = price_instance.mean_all()
    assert result == (6125.00,)

def test_mean_city(price_instance):
    result = price_instance.mean_city()
    expected_result = [("Casablanca", 6250.00), ("Marrakech", 6000.00)]
    assert result == expected_result

if __name__ == "__main__":
    pytest.main()
