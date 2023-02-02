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
        DATE = input('>>> ')
        assert len(DATE) == 10 and DATE[:4].isdigit() and DATE[4] == '-' \
            and DATE[5:7].isdigit() and DATE[7] == '-' and DATE[8:10].isdigit()
    except AssertionError:
        print('Please enter a date in the correct format.')
        return prompt_date()

    return DATE


def parse_xml_for_rates():
    """Pull and parse XML data from the Treasury Dept. website. This
    function may break if the XML URL or file structure changes.
    """
    url = ['https://home.treasury.gov/resource-center/data-chart-center/',
           'interest-rates/pages/xml?data=daily_treasury_yield_curve&',
           'field_tdr_date_value_month=']
    DATE = '2023-02-01'# prompt_date()
    year, month = DATE.split('-')[0:2]
    url.append(year)
    url.append(month)
    url = ''.join(url)
    print('Connecting to treasury.gov...')

    with urllib.request.urlopen(url) as page:
        tree = ET.parse(page)
    root = tree.getroot()

    # The XML tages in the tree variable are all prepended by a URL.
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        for content in entry.find('{http://www.w3.org/2005/Atom}content'):
            if content[0].text[:10] == DATE:
                rates = []
                for ind, child in enumerate(content):
                    if ind > 0:
                        rates.append(float(child.text))
                # Remove repeated 30-year rate (due to XML format)
                rates.pop()
                return rates, DATE


def plot_rates(rates_and_date: tuple):
    """Generate a plot of the selected day's interest rates."""
    rates, DATE = rates_and_date
    x_values = (1 / 12, 1 / 6, 1 / 4, 1 / 3, 1 / 2, 1, 2, 3, 5, 7, 10, 20, 30)
    plt.xlabel('Duration (years)')
    plt.ylabel('Annualized Interest Rate (%)')
    title = ''.join(['U.S. Treasuries Yield Curve ', '(', DATE, ')'])
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
        print(f'\nNo rates found for {DATE}. Are you sure it was a'
               'trading day?')


plot_rates(parse_xml_for_rates())
