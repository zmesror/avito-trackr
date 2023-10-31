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

    def mean_all(self, city=None):
        """
        Calculate the average price per m2 for a given city or all cities.

        :param city: The city for which to calculate the average price. If None, calculate
            the overall average for all cities.
        :type city: str or None
        :return: The average price per square meter.
        :rtype: tuple
        """
        sql = "SELECT AVG(price / habitable_size) FROM property WHERE price IS NOT NULL AND habitable_size IS NOT NULL"
        if city:
            sql += f"AND city='{city}';"
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
        sql = """SELECT city, AVG(price / habitable_size) AS average_price_per_m2
            FROM property
            WHERE price IS NOT NULL AND habitable_size IS NOT NULL
            GROUP BY city;"""
        self.mycursor.execute(sql)
        return self.mycursor.fetchall()

    def mean(self, interval=1):
        """
        Calculate the average price per m2 for properties over time.

        :param interval: The time interval in years to consider for calculating the average prices.
        :type interval: int, optional
        :return: A list of tuples, where each tuple contains the year, month, and the average price per m2.
        :rtype: list[(int, int, float)]
        """
        sql = """SELECT YEAR(published_date) AS year, MONTH(published_date) AS month, 
        AVG(price) AS average_price FROM property 
        WHERE published_date >= DATE_SUB(NOW(), INTERVAL 1 YEAR) AND price IS NOT NULL
        GROUP BY YEAR(published_date), MONTH(published_date) 
        ORDER BY year DESC, month DESC;"""
        self.mycursor.execute(sql)
        return self.mycursor.fetchall()

    def plot_bar(self, x, y):
        """
        Plot average prices as bar charts for different cities.

        :param x: List of city names.
        :type x: list[str]
        :param y: List of average prices corresponding to each city.
        :type y: list[float]
        :return: None
        :rtype: None
        """
        colors = ["b", "g", "r", "c", "m", "y", "k"]

        plt.figure(figsize=(10, 6))
        bars = plt.bar(x, y, color=colors[: len(x)])
        plt.xlabel("City")
        plt.ylabel("Average Price")
        plt.title("The average price per m2 of an apartment in Morocco.")
        plt.xticks(rotation=45)

        for i, bar in enumerate(bars):
            bar.set_label(f"{x[i]} ({y[i]:.2f})")

        plt.legend()
        plt.tight_layout()
        plt.savefig("averages.png")

    def plot_mean_evolution(self, data):
        """
        Plot the average prices over time.

        :return: None
        :rtype: None
        """
        if not data:
            print("No data to plot.")
            return

        years = []
        months = []
        prices = []

        for row in data:
            year, month, average_price = row
            years.append(year)
            months.append(month)
            prices.append(average_price)

        # Create a single continuous date variable for the x-axis
        dates = [f"{y}-{m:02d}" for y, m in zip(years, months)]

        plt.figure(figsize=(10, 6))
        plt.plot(dates, prices, marker="o", linestyle="-")
        plt.xlabel("Date")
        plt.ylabel("Average Price")
        plt.title("Average Price Evolution Over Time")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()

        plt.savefig("plot.png")


def main():
    mydb = mysql.connector.connect(
        host="localhost", user="root", password="", database="avito_trackr"
    )
    price = Price(mydb)
    print("Average price per m2:", f"{price.mean_all()[0]:.2f}")
    print("Average price by city:")
    data1 = price.mean_city()
    for city, average in data1:
        print(city, f"{average:.2f}", sep=", ")

    data2 = price.mean()
    print("Average price per m2 for last year:")
    for row in data2:
        print(row)

    # Create data visualization
    cities, averages = zip(*data1)
    price.plot_bar(cities, averages)
    price.plot_mean_evolution(data2)


if __name__ == "__main__":
    main()
