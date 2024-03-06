"""Functions for tracking poker hands and assorted card tasks.

Python list documentation: https://docs.python.org/3/tutorial/datastructures.html
"""
import statistics

def get_rounds(number):
    """

     :param number: int - current round number.
     :return: list - current round and the two that follow.
    """

    return [int( number ), int( number ) + 1, int( number ) + 2]


def concatenate_rounds(rounds_1, rounds_2):
    """

    :param rounds_1: list - first rounds played.
    :param rounds_2: list - second set of rounds played.
    :return: list - all rounds played.
    """

    return rounds_1 + rounds_2


def list_contains_round(rounds, number):
    """

    :param rounds: list - rounds played.
    :param number: int - round number.
    :return:  bool - was the round played?
    """

    if(number in rounds):
        return True
    else:
        return False

def card_average(hand):
    """

    :param hand: list - cards in hand.
    :return:  float - average value of the cards in the hand.
    """

    return round(sum(hand)/len(hand), 1)


def approx_average_is_average(hand):
    """

    :param hand: list - cards in hand.
    :return: bool - if approximate average equals to the `true average`.
    """

    avg = (sum(hand) / len(hand))
    skrajne = avg == (hand[0] + hand[-1]) / 2
    mediana = avg == statistics.median(hand)

    if (mediana == True or skrajne == True):
        return True
    else:
        return False

def average_even_is_average_odd(hand):
    """

    :param hand: list - cards in hand.
    :return: bool - are even and odd averages equal?
    """
    count_odd = len(hand[0:len(hand):2])
    avg_odd = (sum(hand[0:len(hand):2])) / count_odd
    count_even = len( hand[1:len( hand ):2] )
    avg_even = (sum( hand[1:len( hand ):2] )) / count_even

    return avg_odd == avg_even


def maybe_double_last(hand):
    """

    :param hand: list - cards in hand.
    :return: list - hand with Jacks (if present) value doubled.
    """

    if(hand[-1] == 11):
        return [hand [0], hand [1], hand[-1] * 2]
    else:
        return hand


if __name__ == '__main__':
    # print(add_prefix_un(input("Enter number: ")))
    print( f"list of rounds: {get_rounds(7)}" )
    print( f"list 1 and 2: {concatenate_rounds([27, 28, 29], [35, 36])}" )
    print( f"Is round played?: {list_contains_round([27, 28, 21], 28)}" )
    print( f"Average on hand: {card_average([0, 1, 5])}" )
    print( f"Aprox Average on hand: {approx_average_is_average([1, 2, 3, 5, 9])}" )
    print( f"Is odd == even: {average_even_is_average_odd([1, 2, 3, 4])}" )
    print( f"Hand after mayby double: {maybe_double_last([1, 2, 11])}" )
