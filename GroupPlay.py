def comp10001go_play(discard_history, player_no, hand):
    '''choose a card from hand to play for each of the 10 turns'''
    # always return first card in hand
    return hand[0]



def comp10001go_group(discard_history, player_no):
    '''group the discards into groups for scoring'''
    # return a list of history cards played by this player
    return [[lst[player_no]] for lst in discard_history]