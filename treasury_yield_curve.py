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
        print('For which trading day do you want to view the yield curve?',
              'Response format must be YYYY-MM-DD.')
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
    print('Connecting to treasury.gov...')

    content_start_index = 0
    # Treasury changed XML structure on Oct. 19, 2022.
    IS_OLD_XML_FORMAT = int(year) <= 2022 and int(month) <= 10 \
                        and int(day) <= 18
    if IS_OLD_XML_FORMAT:
        content_start_index = 1

    with urllib.request.urlopen(url) as page:
        tree = ET.parse(page)
    root = tree.getroot()

    # The XML tages in the tree variable are all prepended by a URL.
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
    rates, date = rates_and_date
    year, month, day = date.split('-')
    x_values = (1 / 12, 1 / 6, 1 / 4, 1 / 3, 1 / 2, 1, 2, 3, 5, 7, 10, 20, 30)
    # Treasury added a new data point on Oct. 19, 2022, the 4 month bill.
    if int(year) <= 2022 and int(month) <= 10 and int(day) <= 18:
        x_values = (1 / 12, 1 / 6, 1 / 4, 1 / 2, 1, 2, 3, 5, 7, 10, 20, 30)

    plt.xlabel('Duration (years)')
    plt.ylabel('Annualized Interest Rate (%)')
    title = ''.join(['U.S. Treasuries Yield Curve ', '(', date, ')'])
    plt.title(title)

    # A few more labelled tick marks on the y-axis looks nicer.
    # Increase amount of y-axis ticks while maintaining proportional spacing.
    # Decimal values of ticks are multiples of 1 / SCALE_FACTOR.
    try:
        DIFF_1M_30YR = abs(rates[-1] - rates[0])
        if DIFF_1M_30YR > 5:
            SCALE_FACTOR = 2
        else:
            SCALE_FACTOR = 4
        yticks_start = int(rates[0]) * SCALE_FACTOR
        yticks_end = SCALE_FACTOR * int(rates[-1]) + SCALE_FACTOR
        yticks = range(yticks_start, yticks_end, 1)
        yticks = [i / SCALE_FACTOR for i in yticks]
        if len(yticks) > 11:
            yticks_copy = yticks.copy()
            yticks = []
            for ind, num in enumerate(yticks_copy):
                if ind > 0 and ind % 2 != 0:
                    yticks.append(num)

        plt.yticks(yticks, yticks)

        plt.plot(x_values, rates, marker='o')
        plt.show()
    except (IndexError, ValueError):
        print(f'\nNo rates found for {date}. Are you sure it was a'
               'trading day?')


plot_rates(parse_xml_for_rates())
