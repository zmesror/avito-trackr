import mysql.connector
import sys
import matplotlib.pyplot as plt


class Price:
    def __init__(self, mydb):
        """
        Initialize the Price class by establishing a MySQL database connection.

        :raises: SystemExit with an error message if a MySQL connection error occurs.
        """
        try:
            self.mydb = mydb
            self.mycursor = self.mydb.cursor()
        except mysql.connector.Error as err:
            sys.exit("MySQL Error: {}".format(err))

    def mean(self, city=None):
        """
        Calculate the average price per m2 for a given city or all cities.

        :param city: The city for which to calculate the average price. If None, calculate
            the overall average for all cities.
        :type city: str or None
        :return: The average price per square meter.
        :rtype: tuple
        """
        sql = "SELECT AVG(price / habitable_size) FROM property "
        if city:
            sql += f"WHERE city='{city}';"
        else:
            sql += ";"

        self.mycursor.execute(sql)
        return self.mycursor.fetchone()

    def mean_city(self):
        """
        Calculate the average price per m2 for each city.

        :return: A list of tuples, where each tuple contains the city name and its average
            price
        :rtype: list
        """
        sql = "SELECT city, AVG(price / habitable_size) AS average_price_per_m2 FROM property GROUP BY city;"
        self.mycursor.execute(sql)
        return self.mycursor.fetchall()


def main():
    mydb = mysql.connector.connect(
        host="localhost", user="root", password="", database="avito_trackr"
    )
    price = Price(mydb)
    print("Average price per m2:", f"{price.mean()[0]:.2f}")
    print("Average price by city:")
    data = price.mean_city()
    for city, average in data:
        print(city, f"{average:.2f}", sep=", ")
    
    # Create data visualization
    cities, averages = zip(*data)
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

    plt.figure(figsize=(10, 6))
    bars = plt.bar(cities, averages, color=colors[:len(cities)])
    plt.xlabel("City")
    plt.ylabel("Average Price")
    plt.title("The average price per m2 of an apartment in Morocco.")
    plt.xticks(rotation=45)

    for i, bar in enumerate(bars):
        bar.set_label(f'{cities[i]} ({averages[i]:.2f})')

    plt.legend()
    plt.tight_layout()
    plt.savefig("averages.png")


if __name__ == "__main__":
    main()
