"""
Author: Furkan Karakutuk.
Mail: furkan@hypeistanbul.com

Created for Hype Google Trends Tool.

Description:
This little script gets data from Google Trends and returns pandas series table.
"""

from pytrends.request import TrendReq

import random
import string


def get_trends(kw_list: list, s_date, e_date):
    """
    Gets trends from Google Trends and returnds pandas series table.
    :param kw_list: list, keyword list.
    :param s_date: date, start_date.
    :parma e_date: date, end_date.
    """
    try:
        pytrends = TrendReq(hl='tr_TR', tz=360)

        if kw_list[-1] == '':
            kw_list.pop(-1)

        if s_date is None or s_date == "" or e_date is None or e_date == "":
            pytrends.build_payload(kw_list, cat=0, timeframe='all', geo='TR')
        else:
            pytrends.build_payload(kw_list, cat=0, timeframe='''{s_date} {e_date}'''.format(s_date=str(s_date), e_date=str(e_date)), geo='TR')

        trends_data = pytrends.interest_by_region(resolution='CITY')
        trends_data.to_csv('trends_data.csv')
        # json_data = trends_data.to_json(orient="columns", force_ascii=False)

    except Exception as e:
        raise e
    return trends_data


def generate_key(length):
    """
    Generates secret key.
    :param length: int, secret key length.
    """
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
