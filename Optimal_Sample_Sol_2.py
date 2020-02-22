# THIS IS A SAMPLE SOLUTION PROVIDED TO US BY THE TEACHING STAFF 

import itertools
import math

SUIT_TO_COLOUR = dict(zip('HDCS', 'RRBB'))
VALUE_STRING_TO_VALUE = dict(zip('A234567890JQK', range(1, 14)))
VALUE_TO_VALUE_STRING = {v: k for k, v in VALUE_STRING_TO_VALUE.items()}


class Card:
  def __init__(self, card_string):
    if isinstance(card_string, Card):
      card_string = str(card_string)
    elif isinstance(card_string, tuple):
      card_string = VALUE_TO_VALUE_STRING[card_string[0]] + card_string[1]
    self.value_str = card_string[0]
    self.value = VALUE_STRING_TO_VALUE[self.value_str]
    self.suit = card_string[1]
    self.colour = SUIT_TO_COLOUR[self.suit]
    self.inv_colour = 'R' if self.colour == 'B' else 'B'
    self.orphan_value = -20 if self.is_ace() else -self.value

  def __hash__(self):
    return hash(str(self))

  def __eq__(self, other):
    return self.value_str == other.value_str and self.suit == other.suit

  def __repr__(self):
    return f'Card(\'{self.value_str}{self.suit}\')'

  def __str__(self):
    return f'{self.value_str}{self.suit}'

  def is_ace(self):
    return self.value_str == 'A'

  def is_black(self):
    return self.colour == 'B'

  def is_king(self):
    return self.value_str == 'K'

  def is_red(self):
    return self.colour == 'R'


def construct_n_of_a_kind(cards):
  # Early bail if we don't have enough cards.
  if len(cards) < 2:
    return None

  # Ensure that all of the cards have the same value and are not an Ace.
  value = None
  for card in cards:
    if card.is_ace():
      return None
    elif value is None:
      value = card.value
    elif card.value != value:
      return None

  # Return the cards as is.
  return list(cards)


def construct_run(cards):
  # Early bail if we don't have enough cards.
  if len(cards) < 3:
    return None

  # Partition the cards into Aces and non-Aces.
  non_aces = []
  aces_by_colour = {'B': [], 'R': []}
  for card in cards:
    if card.is_ace():
      aces_by_colour[card.colour].append(card)
    else:
      non_aces.append(card)

  # Ensure we have enough non-Aces.
  if len(non_aces) < 2:
    return None

  # Sort the non-Aces by value.
  non_aces.sort(key=lambda card: card.value, reverse=True)

  # Attempt to construct a valid run from the avaialble cards.
  prev = non_aces.pop()
  run = [prev]
  while non_aces:
    top = non_aces[-1]

    # Check for a normal valid transition.
    if prev.value + 1 == top.value and prev.colour == top.inv_colour:
      run.append(non_aces.pop())  # Consume the current card in the run.
      prev = top
    else:
      # Check if we can do an Ace insertion.
      aces = aces_by_colour[prev.inv_colour]
      if aces and not prev.is_king():  # Can't go higher than a King for Ace insertion.
        ace = aces.pop()  # Consume the next ace.
        run.append(ace)
        prev = Card((prev.value + 1, ace.suit))
      else:
        # We did not find a valid transition.
        return None

  # If we have any aces left over, we do not have a valid run.
  if aces_by_colour['B'] or aces_by_colour['R']:
    return None

  return run


def score_n_of_a_kind(cards):
  return cards[0].value * math.factorial(len(cards))


def score_orphans(cards):
  return sum(map(lambda card: card.orphan_value, cards))


def score_run(cards):
  return sum(range(cards[0].value, cards[-1].value + 1))


def score_group(cards):
  if len(cards) == 1:
    return score_orphans(cards)

  grouped_cards = construct_n_of_a_kind(cards)
  if grouped_cards is not None:
    return score_n_of_a_kind(grouped_cards)

  grouped_cards = construct_run(cards)
  if grouped_cards is not None:
    return score_run(grouped_cards)

  assert False, 'Should not be possible'


def is_valid_group(cards):
  if len(cards) == 1:
    return True
  elif construct_n_of_a_kind(cards) is not None:
    return True
  elif construct_run(cards) is not None:
    return True
  else:
    return False


def _generate_partitions(cards, groups):
  if len(cards) == 0:
    yield frozenset(groups)
    return

  for k in range(1, len(cards) + 1):
    for combination in map(frozenset, itertools.combinations(cards, k)):
      if not is_valid_group(combination):
        continue
      remaining_cards = cards - combination
      groups.append(combination)
      yield from _generate_partitions(remaining_cards, groups)
      groups.pop()


def generate_partitions(cards):
  seen = set()
  for partition in _generate_partitions(frozenset(cards), []):
    if partition in seen:
      continue
    seen.add(partition)
    yield list(map(list, partition))


def comp10001go_best_partitions(card_strings):
  cards = set(map(Card, card_strings))

  max_score = float('-inf')
  max_partitions = []
  for partition in generate_partitions(cards):
    score = sum(map(score_group, partition))
    if score > max_score:
      max_score = score
      max_partitions = [partition]
    elif score == max_score:
      max_partitions.append(partition)

  return [[list(map(str, cards)) for cards in partition] for partition in max_partitions]