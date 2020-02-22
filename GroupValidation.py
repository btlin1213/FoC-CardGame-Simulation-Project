def factorial(num):
    '''take an integer input and return its factorial'''
    # base case
    if num == 0:
        return 1
    # recursion step
    else:
        return num * factorial(num - 1)

def count_ace(given_ace, values):
    '''take list of aces and values, return if the given aces match required'''
    i = 1
    n_lst = []
    # append the difference between each adjacent pair of values to n_lst
    # number of ace required between each pair = difference - 1
    # check if given aces match the number of ace required
    while i in range(1, len(values)):
        n_lst.append(values[i] - values[i - 1] - 1)
        i += 1
    return given_ace == sum(n_lst)

def colour_check(sort_colours, values, i):
    '''check if colours alternate as required'''
    # go through each value in values
    while i in range(1, len(values)):
        # if difference between two values is even then must be same colour
        if (values[i] - values[i - 1]) % 2 == 0 and \
            sort_colours[i] == sort_colours[i - 1]:
            i += 1
            return colour_check(sort_colours, values, i)
        # if difference between two values is odd, must be different colours
        elif (values[i] - values[i - 1]) % 2 == 1 and \
            sort_colours[i] != sort_colours[i - 1]:
            i += 1
            return colour_check(sort_colours, values, i)
        else:
            return False
    return True
    

def ace_colour(total_cards, ace_colours, sort_colours):
    '''determine if ace colours match the required number of each'''
    total_colours = ace_colours + sort_colours
    # if card total is even, number of black match number of red 
    if total_cards % 2 == 0:
        return total_colours.count('B') == total_colours.count('R')
    # if card total is odd, number of first colour is 
    # number of second colour plus one
    elif total_cards % 2 == 1:
        return total_colours.count('B') == total_colours.count('R') + 1 or \
                total_colours.count('R') == total_colours.count('B') + 1

        
value_dct = {}
colour_dct = {}
def comp10001go_score_group(cards):
    '''score the given list of cards'''
    
    # number and colour of aces
    ace_colours = []
    for card in cards:
        if card[0] == 'A':
            ace_colours.append(card[1])
    
    # str_values = unsorted, with JQKA 
    str_values = [card[0] for card in cards]
    
    # colours = unsorted, same order as str_values
    colours = [card[1] for card in cards]
    
    # convert colour from club, heart etc. to black(B) or red(R)
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
            return 'N-kind'
    
    # preparation for run calculations
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
    
    # sort_colours match the order of values list 
    sort_colours = []
    for value, colour in lst:
        sort_colours.append(colour)
        
    # create variable for total number of cards 
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
                    return 'run'
                else:
                    return False
                        
            # no ace in run 
            else:
                if count_ace(len(ace_colours), values) and \
                    colour_check(sort_colours, values, 1):
                    return 'run'
                else:
                    return False
    
    # singleton
    elif len(cards) == 1:
        return 'singleton'
    
    else:
        return False

def comp10001go_valid_groups(groups):
    '''validate the given list of cards'''
    ans = []
    # if group is empty, return True
    if not groups:
        return True
    
    # if group is not empty, test if singleton/run/N-kind
    else:
        for group in groups:
            ans.append(comp10001go_score_group(group) in ['singleton', 
                                                      'run', 'N-kind'])
    return all(ans)