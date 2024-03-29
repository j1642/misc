#!/usr/bin/env python3

"""
Displays the U.S. Treasury securities yield curve (interest rate vs.
bond duration) on a given trading day.
"""

# Note: https://docs.python.org/3/library/xml.html#xml-vulnerabilities

import urllib.request
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt


def prompt_date():
    """Ask user for a date. The input date must be a trading day (when
    stock exchanges are open), not during a weekend or holiday.
    """
    try:
        print('For which trading day do you want to view the yield curve?'
              ' (YYYY-MM-DD)')
        date = input('>>> ')
        assert len(date) == 10 and date[:4].isdigit() and date[4] == '-' \
            and date[5:7].isdigit() and date[7] == '-' and date[8:10].isdigit()
    except AssertionError:
        print('Please enter a date in the correct format.')
        return prompt_date()

    return date


def parse_xml_for_rates():
    """Pull and parse XML data from the Treasury Dept. website. This
    function may break if the XML URL or file structure changes.
    """
    url = ['https://home.treasury.gov/resource-center/data-chart-center/',
           'interest-rates/pages/xml?data=daily_treasury_yield_curve&',
           'field_tdr_date_value_month=']
    date = prompt_date()
    year, month, day = date.split('-')
    url.append(year)
    url.append(month)
    url = ''.join(url)

    content_start_index = 0
    # Treasury changed XML structure on Oct. 19, 2022.
    IS_OLD_XML_FORMAT = int(year) <= 2022 and int(month) <= 10 \
                        and int(day) <= 18
    if IS_OLD_XML_FORMAT:
        content_start_index = 1

    print('Connecting to treasury.gov...')
    with urllib.request.urlopen(url) as page:
        print('Reading XML...')
        tree = ET.parse(page)
    root = tree.getroot()

    # The XML tags in the tree variable are all prepended by a URL.
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        for content in entry.find('{http://www.w3.org/2005/Atom}content'):
            if content[content_start_index].text[:10] == date:
                rates = []
                for ind, child in enumerate(content):
                    if ind > content_start_index:
                        rates.append(float(child.text))
                # Remove repeated 30-year rate (due to XML format)
                rates.pop()
                return rates, date


def plot_rates(rates_and_date: tuple):
    """Generate a plot of the selected day's interest rates."""
    try:
        rates, date = rates_and_date
    except TypeError:
        print('Are you sure that was a trading day? If so, this tool is '
            'not configured to read Treasury data from before 2019, '
            'roughly.')
        return
    year, month, day = date.split('-')
    x_values = (1 / 12, 1 / 6, 1 / 4, 1 / 3, 1 / 2, 1, 2, 3, 5, 7, 10, 20, 30)
    # Treasury added a new data point on Oct. 19, 2022, the 4 month bill.
    if int(year) <= 2022 and int(month) <= 10 and int(day) <= 18:
        x_values = (1 / 12, 1 / 6, 1 / 4, 1 / 2, 1, 2, 3, 5, 7, 10, 20, 30)

    plt.xlabel('Duration (years)')
    plt.ylabel('Annualized Interest Rate (%)')
    title = ''.join(['U.S. Treasuries Yield Curve ', '(', date, ')'])
    plt.title(title)

    try:
        plt.plot(x_values, rates, marker='o')
        plt.show()
    except (IndexError, ValueError):
        print('This tool is not configured to read Treasury data from '
            'before 2019, roughly.')
        return


plot_rates(parse_xml_for_rates())
