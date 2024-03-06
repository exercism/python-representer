import logging
#import logging.config
from collections import defaultdict, Counter

YACHT = lambda d: 50 if len(set(d)) == 1 else 0
ONES = lambda d: sum(x for x in d if x == 1)
TWOS = lambda d: sum(x for x in d if x == 2)
THREES = lambda d: sum(x for x in d if x == 3)
FOURS = lambda d: sum(x for x in d if x == 4)
FIVES = lambda d: sum(x for x in d if x == 5)
SIXES = lambda d: sum(x for x in d if x == 6)
FULL_HOUSE = lambda d: sum(d) if len(set(d)) == 2 and any(d.count(x) == 3 for x in set(d)) else 0
FOUR_OF_A_KIND = lambda d: sum(x * 4 for x in set(d) if d.count(x) > 3)
LITTLE_STRAIGHT = lambda d: 30 if sum(d) == 15 and len(set(d)) == 5 else 0
BIG_STRAIGHT = lambda d: 30 if sum(d) == 20 and len(set(d)) == 5 else 0
CHOICE = lambda d: sum(d)

def score(dice, category):
    if any(not 0 < x < 7 for x in dice):
        raise ValueError("Invalid dice {}".format(dice))
    return category(dice)


def tally(tournament_results):
    '''
    Generate a list of formatted report strings for tournament results.

     >>> test = (tally(["Courageous Californians;Devastating Donkeys;win",\
                        "Allegoric Alaskans;Blithering Badgers;win",\
                        "Devastating Donkeys;Allegoric Alaskans;loss",\
                        "Courageous Californians;Blithering Badgers;win",\
                        "Blithering Badgers;Devastating Donkeys;draw",\
                        "Allegoric Alaskans;Courageous Californians;draw"]))
     >>> print(type(test))
     <class 'list'>
     >>> print(test[0])
     Team                           | MP |  W |  D |  L |  P
     >>> print(test[1])
     Allegoric Alaskans             |  3 |  2 |  1 |  0 |  7
     >>> print(test[2])
     Courageous Californians        |  3 |  2 |  1 |  0 |  7
     >>> print(test[3])
     Blithering Badgers             |  3 |  0 |  1 |  2 |  1
     >>> print(test[4])
     Devastating Donkeys            |  3 |  0 |  1 |  2 |  1
    '''

    try:
        results = (row.split(';') for row in tournament_results)
        tournament_stats = compile_statistics(results)

    except AttributeError:
        logger.exception(f'There is a problem with the tournament results string: ')
        raise

    except IndexError:
        logger.exception(f'Compiling team statistics failed: ')
        raise

    return make_report(tournament_stats)


def compile_statistics(results):
    '''
    Create a stats dictionary with results by team name.
    Return a dictionary with Counter()s as values.
    '''

    team_stats = defaultdict(Counter)
    opposite = {'win': 'loss', 'loss': 'win', 'draw': 'draw'}

    for home, away, outcome in results:
            team_stats[home].update([outcome])
            team_stats[away].update([opposite[outcome]])

    return team_stats


def make_report(team_stats):
    '''
    Format & return a report string for printing.
    If there are no team_stats, return only a header.
    '''

    report_format = '{:<30} | {:4>} |  {:4>} |  {:4>} |  {:4>} | {:>2}'

    header  = [('Team', 'MP', 'W', 'D', 'L', 'P')]
    content = ((team, ' ' + str(sum(team_stats[team].values())),
                      team_stats[team]["win"],
                      team_stats[team]["draw"],
                      team_stats[team]["loss"],
                      team_stats[team]["win"] * 3 + team_stats[team]["draw"])
                      for team in team_stats.keys())

    #descending by total points & **ascending** by team if there is a tie.
    report_order = header + sorted(content, key=lambda x: (-(x[5]), x))

    return "\n".join(report_format.format(*team) for team in report_order).split('\n')