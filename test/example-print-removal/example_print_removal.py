"""Functions for tracking poker hands and assorted card tasks.

Python list documentation: https://docs.python.org/3/tutorial/datastructures.html
"""


def get_rounds(number):
    """

     :param number: int - current round number.
     :return: list - current round and the two that follow.
    """
    print([int( number ), int( number ) + 1, int( number ) + 2])

    return [int( number ), int( number ) + 1, int( number ) + 2]


def concatenate_rounds(rounds_1, rounds_2):
    """

    :param rounds_1: list - first rounds played.
    :param rounds_2: list - second set of rounds played.
    :return: list - all rounds played.
    """
    print(rounds_1 + rounds_2)

    return rounds_1 + rounds_2


def list_contains_round(rounds, number):
    """

    :param rounds: list - rounds played.
    :param number: int - round number.
    :return:  bool - was the round played?
    """

    if(number in rounds):
        print(number)
        return True
    else:
        print(rounds)
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
    import statistics

    print((hand[0] + hand[-1]) / 2)

    mediana = avg == statistics.median(hand)

    print(hand[0] + hand[-1])

    if (mediana == True or skrajne == True):
        print(mediana)
        return True
    else:
        return False

def average_even_is_average_odd(hand):
    """

    :param hand: list - cards in hand.
    :return: bool - are even and odd averages equal?
    """

    list_odd = (list(range(1, len(hand), 2)))
    list_even = (list( range( 0, len( hand ), 2 ) ))

    print([list_odd,list_even])

    count_odd = len(hand[0:len(hand):2])
    avg_odd = (sum(hand[0:len(hand):2])) / count_odd
    count_even = len( hand[1:len( hand ):2] )
    avg_even = (sum( hand[1:len( hand ):2] )) / count_even

    print(avg_odd, count_odd)

    return avg_odd == avg_even


def maybe_double_last(hand):
    """

    :param hand: list - cards in hand.
    :return: list - hand with Jacks (if present) value doubled.
    """

    if(hand[-1] == 11):
        print(hand)
        return [hand [0], hand [1], hand[-1] * 2]
    else:
        print("Nothing found!", hand)
        return hand

