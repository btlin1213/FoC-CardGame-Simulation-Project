# THIS IS A SAMPLE SOLUTION PROVIDED TO US BY THE TEACHING STAFF 

from math import factorial


# index of value of a card
VALUE = 0

# index of suit of a card
SUIT = 1

# value of Ace
ACE = 'A'

# dictionary of scores of individual cards
card_score = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '0': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    ACE: 20,
    }
    
# suits which are red
RED_SUITS = 'HD'

# suits which are black
BLACK_SUITS = 'SC'

# card colours
RED = 1
BLACK = 2

# minimum no. of cards in an n-of-a-kind set
MIN_CARDS_NKIND = 2

# minimum no. of non-Ace cards in a run
MIN_NONACE_RUN = 2

# minimum no. cards in a run
MIN_RUN = 3



def is_ace(card):
    """Boolean evaluation of whether `card` is an Ace"""
    return card[VALUE] == ACE


def get_score(card):
    """return the score of `card`, based on its value"""
    return card_score[card[VALUE]]


def get_colour(card):
    """Return the colour of `card` (`RED` or `BLACK`)"""
    if card[SUIT] in RED_SUITS:
        return RED
    else:
        return BLACK


def comp10001go_score_group(cards):
    """Validate/score a group of cards (order unimportant), supplied as a 
    list of cards (each a string); return the positive score of the group if 
    valid, and negative score otherwise. Note, assumes that all cards are 
    valid, and unique."""

    # construct sorted list of values of cards (ignore suit for now)
    values = sorted([get_score(card) for card in cards])

    # CASE 1: N-of-a-kind if all cards of same value, at least
    # `MIN_CARDS_NKIND` cards in total, and not Aces
    if (len(set(values)) == 1 and len(cards) >= MIN_CARDS_NKIND
        and not is_ace(cards[0])):
        return factorial(len(cards)) * card_score[cards[0][VALUE]]

    # construct sorted list of non-Ace cards
    nonace_cards = sorted([card for card in cards if not is_ace(card)],
                          key=lambda x: get_score(x))

    # construct list of Ace cards
    ace_cards = list(set(cards) - set(nonace_cards))

    # run must have at least `MIN_NONACE_RUN` non-Ace cards in it
    if len(nonace_cards) >= MIN_NONACE_RUN:

        is_run = True
        prev_val = prev_colour = None
        score = 0

        # iterate through cards to make sure they form a run
        for card in nonace_cards:

            # CASE 1: for the first card in `nonace_cards`, nothing to
            # check for
            if prev_val is None:
                score = prev_val = get_score(card)
                prev_colour = get_colour(card)

            # CASE 2: adjacent to previous card in value
            elif get_score(card) - prev_val == 1:

                # CASE 2.1: alternating colour, meaning continuation of run
                if get_colour(card) != prev_colour:
                    prev_val = get_score(card)
                    prev_colour = get_colour(card)
                    score += prev_val
                # CASE 2.2: not alternating colour, meaning invalid run
                else:
                    is_run = False
                    break

            # CASE 3: repeat value, meaning no possibility of valid run
            elif get_score(card) == prev_val:
                is_run = False
                break

            # CASE 4: gap in values, in which case check to see if can be
            # filled with Ace(s)
            else:
                gap = get_score(card) - prev_val - 1
                
                gap_filled = False
                # continue until gap filled
                while is_run and gap and len(ace_cards) >= gap:

                    gap_filled = False
                
                    # search for an Ace of appropriate colour, and remove
                    # from list of Aces if found (note that it doesn't matter
                    # which Ace is used if multiple Aces of same colour)
                    for i, ace in enumerate(ace_cards):
                        if get_colour(ace) != prev_colour:
                            ace_cards.pop(i)
                            prev_val += 1
                            prev_colour = get_colour(ace)
                            score += prev_val
                            gap -= 1
                            gap_filled = True
                            break

                    if not gap_filled:
                        is_run = False

                if is_run and gap_filled and get_colour(card) != prev_colour:
                    prev_val = get_score(card)
                    prev_colour = get_colour(card)
                    score += prev_val
                else:
                    is_run = False

        if is_run and len(cards) >= MIN_RUN and not ace_cards:
            return score

    return -sum(values)
            

def comp10001go_valid_groups(groups):
    for cards in groups:
        if not cards or (len(cards) > 1
                         and comp10001go_score_group(cards) < 0):
            return False
    return True


def comp10001go_score_groups(groups):
    score = 0
    for group in groups:
        score += comp10001go_score_group(group)
    return score


def comp10001go_randplay(discard_history, player_no, hand):

    from random import shuffle

    shuffle(hand)

    # for first turn, select lowest card
    return hand[0]


    
def comp10001go_partition(cards):

    # BASE CASE 1: no cards, so no grouping to make
    if len(cards) == 0:
        return []

    # BASE CASE 2: single card, so make a singleton group
    if len(cards) == 1:
        return [[cards]]

    # RECURSIVE CASE
    out = []
    first = cards[0]
    for sub_partition in comp10001go_partition(cards[1:]):

        # insert `first` in each of the subpartition's groups
        for n, subpart in enumerate(sub_partition):
            out.append(sub_partition[:n] + [[first] + subpart] + sub_partition[n+1:])

        # put `first` in its own subpart 
        out.append([[first]] + sub_partition)
    return out


def comp10001go_best_partitions(cards):

    # generate and score all valid card groups from `cards`
    valid_groups = [(part, comp10001go_score_groups(part)) for part in comp10001go_partition(cards) 
                    if comp10001go_valid_groups(part)]

    if valid_groups:
        first_group, best_score = valid_groups[0]
        best_groups = [first_group]
        for group, score in valid_groups[1:]:
            if score > best_score:
                best_groups = [group]
                best_score = score
            elif score == best_score:
                best_groups.append(group)
        return best_groups