from itertools import combinations
from collections import defaultdict

def factorial(num):
    if num == 0:
        return 1
    else:
        return num * factorial(num - 1)

def count_ace(given_ace, values):
    i = 1
    n_lst = []
    while i in range(1, len(values)):
        n_lst.append(values[i] - values[i - 1] - 1)
        i += 1
    return given_ace == sum(n_lst)

def colour_check(sort_colours, values, i):
    while i in range(1, len(values)):
        if (values[i] - values[i - 1]) % 2 == 0 and \
            sort_colours[i] == sort_colours[i - 1]:
            i += 1
            return colour_check(sort_colours, values, i)
        elif (values[i] - values[i - 1]) % 2 == 1 and \
            sort_colours[i] != sort_colours[i - 1]:
            i += 1
            return colour_check(sort_colours, values, i)
        else:
            return False
    return True
    

def ace_colour(total_cards, ace_colours, sort_colours):
    total_colours = ace_colours + sort_colours
    if total_cards % 2 == 0:
        return total_colours.count('B') == total_colours.count('R')
    elif total_cards % 2 == 1:
        return total_colours.count('B') == total_colours.count('R') + 1 or \
                total_colours.count('R') == total_colours.count('B') + 1

        
value_dct = {}
colour_dct = {}
def comp10001go_score_group(cards):
    # number and colour of aces
    ace_colours = []
    for card in cards:
        if card[0] == 'A':
            ace_colours.append(card[1])
    # str_values = unsorted, with JQKA 
    str_values = [card[0] for card in cards]
    # colours = unsorted, same order as str_values
    colours = [card[1] for card in cards]
    # convert colour
    colour_dct['C'] = 'B'
    colour_dct['S'] = 'B'
    colour_dct['H'] = 'R'
    colour_dct['D'] = 'R'
    for i in range(len(colours)):
        colours[i] = colour_dct[colours[i]]
    for i in range(len(ace_colours)):
        ace_colours[i] = colour_dct[ace_colours[i]]
    # convert 0JQK to 10, 11, 12, 13, everything else in str_values is string 
    value_dct['0'] = 10
    value_dct['J'] = 11
    value_dct['Q'] = 12
    value_dct['K'] = 13
    for i in range(len(str_values)):
        if str_values[i] in value_dct.keys():
            str_values[i] = value_dct[str_values[i]]
    # separate values list for singletons
    sin_values = []
    for value in str_values:
        if value != 'A':
            sin_values.append(int(value))
    # N-of-a-kind

    if 4 >= len(cards) >= 2 and all(elem == str_values[0] for elem in
                                    str_values) and 'A' not in str_values:
            return int(str_values[0]) * factorial(len(cards))
    # remove ace
    str_values2 = dict(zip(str_values, colours))
    if 'A' in str_values2:
        str_values2.pop('A')
    colours = [colour for value, colour in str_values2.items()]
    str_values = [value for value, colour in str_values2.items()]
    if str_values:
        values = sorted([int(string) for string in str_values])
    lst = sorted([(int(value), colour) for (value, 
                                            colour) in str_values2.items()])
    sort_colours = []
    for value, colour in lst:
        sort_colours.append(colour)
    total_cards = len(str_values) + len(ace_colours)

    # run
    if len(sin_values) == len(set(sin_values)) and \
        len(cards) >= 3 and \
        str_values.count('A') <= len(str_values) - 2:
            # at least 1 ace in run
            if ace_colours:
                if count_ace(len(ace_colours), values) and \
                    colour_check(sort_colours, values, 1) and \
                    ace_colour(total_cards, ace_colours, sort_colours):
                    return sum(range(values[0], values[len(values) - 1] + 1))
                else:
                    return sum([value * -1 for value in sin_values]) + \
                        (len(ace_colours) * -20)
            # no ace in run 
            else:
                if count_ace(len(ace_colours), values) and \
                    colour_check(sort_colours, values, 1):
                    return sum(range(values[0], values[len(values) - 1] + 1))
                else:
                    return sum([value * -1 for value in sin_values]) + \
                        (len(ace_colours) * -20)

    # singleton
    else:
        return sum([value * -1 for value in sin_values]) + \
                (len(ace_colours) * -20)


def best_combo(cards):
    combscore = defaultdict(int)
    # combscore = {[comb]: score, [comb]:score}
    # (comb, score) in combscore, return max(comb)
    # take out that comb, repeat process for the remaining 
    for group_size in range(1, len(cards)):
        for comb_tup in combinations(cards, group_size):
            comb = [', '.join(x) for x in [comb_tup]]
            combscore[comb[0]] = comp10001go_score_group(comb)
    lst = sorted([(score, [comb]) for (comb, score) in combscore.items()], 
                 reverse=True)
    print(combscore)
    print(lst)

    
'''def comp10001go_best_partitions(cards):
    ans = []
    if 0 <= len(cards) <= 1:
        ans.append(cards[0])
        return ans
    else:
        ans.append(best_combo(cards))
        cards == [card for card in cards if card not in best_combo(cards)]
        return comp10001go_best_partitions(cards)'''