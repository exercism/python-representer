from math import hypot, ceil

YACHT = 'yacht'
ONES, TWOS, THREES, FOURS, FIVES, SIXES = 1, 2, 3, 4, 5, 6
FULL_HOUSE = 'full_house'
FOUR_OF_A_KIND = 'four_of_a_kind'
LITTLE_STRAIGHT = 'little'
BIG_STRAIGHT = 'big'
CHOICE = 'choice'


def yacht_score(dice, category):
    dice, roll = sorted(dice), sorted(set(dice))

    match (category, roll):
        case ('full_house', _) | ('choice', _):
            three_match = any(dice.count(item) == 3 for item in roll)
            return sum(dice) if three_match or category == 'choice' else 0

        case ('big', [2, 3, 4, 5, 6]) | ('little', [1, 2, 3, 4, 5]):
            return 30

        case ('four_of_a_kind', _):
            four_match = dice[0] == dice[3] or dice[1] == dice[4]
            return 4 * dice[1] if four_match else 0

        case ('yacht', _) if len(roll) == 1:
            return 50

        case _:
            return sum(item for item in dice if item == category)

def dart_score(x, y):
    match ceil(hypot(x, y)):
        case 0 | 1: return 10
        case 2 | 3 | 4 | 5: return 5
        case 6 | 7 | 8 | 9 | 10: return 1
        case _: return 0
