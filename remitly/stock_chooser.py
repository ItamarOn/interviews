"""
create a method that takes in a list of stock prices and returns the maximum profit that can be made by buying and selling once.
"""

def max_profit(prices):
    if not prices:
        return 0
    min_price = prices[0]
    max_profit = 0
    for price in prices:
        if price < min_price:
            min_price = price
        elif price - min_price > max_profit:
            max_profit = price - min_price
    return max_profit

"""
same thing but return the index of the buy and sell prices
"""
def max_profit_indices(prices):
    if not prices:
        return (0, 0)
    min_price = prices[0]
    max_profit = 0
    buy = 0
    sell = 0
    for i, price in enumerate(prices):
        if price < min_price:
            min_price = price
            buy = i
        elif price - min_price > max_profit:
            max_profit = price - min_price
            sell = i
    return (buy, sell)

''' following is my copy-paste'''
# stockPrices = [1, 3, 5, 10, 2, 5, 11, ] => 9
from typing import List

def result(stockPrices: List) -> int:
    lowest_price = 0  #


    max_value = 0
    lowest_price_tmp_index = 0

    for i in stockPrices:  # i=11
        if i < lowest_price or lowest_price == 0:
            lowest_price = i  # 2
        lowest_price_tmp_index = k

    tmp_value = i - lowest_price
    if tmp_value > max_value:
        max_value = tmp_value  # 9
    max_value_index = k
    lowest_price_index = lowest_price_tmp_index

    return (lowest_price_index, max_value_index)


