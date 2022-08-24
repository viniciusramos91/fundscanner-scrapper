from tabulate import tabulate
from bs4 import BeautifulSoup
import requests
import locale

# Set the locale to Brazilian Portuguese, encoded in UTF-8
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def handle_percentage(percentage_str: str):
    """
    Converts percentage from string to float
    :param percentage_str: Percentage in string
    :return: Percentage in float representation
    """
    return locale.atof(percentage_str.split('%')[0])


def handle_decimal(decimal_str: str):
    """
    Converts decimal from string to float
    :param decimal_str: Decimal in string
    :return: Decimal in float representation
    """
    return locale.atof(decimal_str)


if __name__ == '__main__':
    response = requests.get(
        'https://fundamentus.com.br/fii_resultado.php',
        headers={'User-Agent': 'Mozilla/5.0'})

    soup = BeautifulSoup(response.text, 'html.parser')

    table_rows = soup.find(id='tabelaResultado').find('tbody').find_all('tr')

    result_table = []

    for table_line in table_rows:
        line_data = table_line.find_all('td')

        ticker = line_data[0].text
        sector = line_data[1].text
        current_price = handle_decimal(line_data[2].text)
        dividend_yield = handle_percentage(line_data[4].text)
        total_value = handle_decimal(line_data[6].text)
        vacancy = handle_percentage(line_data[12].text)
        property_quantity = int(line_data[8].text)

        result_table.append([
            ticker,
            sector,
            locale.currency(current_price),
            f'{locale.str(dividend_yield)} %',
            locale.currency(total_value),
            f'{locale.str(vacancy)} %',
            property_quantity
        ])

    table_header = [
        "TICKER", "SECTOR", "CURRENT PRICE", "DIVIDEND YIELD", "TOTAL VALUE",
        "VACANCY", "PROPERTY QUANTITY"]

    print(tabulate(result_table, headers=table_header, showindex='always', tablefmt='fancy_grid'))
