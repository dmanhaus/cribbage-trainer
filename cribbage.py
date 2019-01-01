import pydealer
import itertools
from cribbageHand import CribbageHand
import argparse

ap = argparse.ArgumentParser(description='Play cribbage against, or learn how to play from a self-learning opponent.', formatter_class=argparse.RawTextHelpFormatter)
ap.add_argument('-sh'
              , '--show'
              , required=False
              , help='level of detail to show during play\n ' 
                  + '0 = Show only the player cards & the count\n ' 
                  + '1 = Show the player hand score before and after discard\n '
                  + '2 = Show the crib after discard\n ' 
                  + '3 = Show everything, including the enemy hand after discard and during play'
              , type=int
              , default=0)
ap.add_argument('-a'
              , '--autoplay'
              , required=False
              , help='Computer plays against itself [n] times'
              , type=int
              , default=0)
ap.add_argument('-s'
              , '--strategy'
              , required=False
              , help='Specifies the strategy used by the enemy in standard play, and the hero in autoplay mode (comma-separated).')
                                                         
args = vars(ap.parse_args())
print(args)
show_value = args["show"]>0
show_crib = args["show"]>=2
show_enemy_hand = args["show"]==3

# Define a cribbage rank dictionary
 
cribbage_ranks = {
  "values": {
    "King":  10,
    "Queen": 10,
    "Jack": 10,
    "10": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "Ace": 1
  }
}

# Define a cribbage board
cribbage_board = {
  "hero": {
    "peg" : [0,0]
  },
  "enemy": {
    "peg" : [0,0]
  }
}

deck = pydealer.Deck(ranks=cribbage_ranks)
deck.shuffle()
cut = pydealer.Stack()
 
# Define a list of player positions and seed the is_hero_dealer
position = ['Pone', 'Dealer']
is_hero_dealer = True

def print_hand(hand_name, hand, show_value=True, add_cut=False):
  global cut
 
  if add_cut and cut.size == 1:
    cut_term = cut[0].abbrev
    hand.add(cut.get(cut_term))
 
  score_hand = CribbageHand(cards=hand)
  hand_template = '{0} value: {1}'
  cards = ' '.join([card.abbrev.rjust(3) for card in hand])
 
  if show_value:
    if score_hand.size < 6:
      score_flush = score_hand.score_flush()
    else:
      score_flush = 0
 
    printed_score = hand_template.format(hand_name, str(score_hand.score()))
    score_template = '15\'s: {0} Pairs: {1} Runs: {2} Flush: {3} Knobs: {4}'
    printed_count = score_template.format(str(score_hand.score_fifteens()),
                                          str(score_hand.score_pairs()),
                                          str(score_hand.score_runs()),
                                          str(score_flush),
                                          str(score_hand.score_knobs()))
  else:
    printed_score = hand_name
 
  index_string = ' 1  '
  for i in range(2,hand.size+1):
    index_string = index_string + ' %s  ' % str(i)
 
  if add_cut and hand.size == 5:
    index_string = index_string.replace('5', 'Cut')
    cut.add(hand.get(cut_term))
 
  print(printed_score + '\n')
  print(index_string)
  print('-' * len(index_string))
  print(cards)
  print('-' * len(index_string))
  if show_value:
    print(printed_count + '\n')
 
def sum_hand_value(hand):
  hand = CribbageHand(cards = hand)
  count = 0
  for card in hand:
    count = count + card.count_value
  return count
 
def play_card(card_term, hand, table):
  table.add(hand.get(card_term))
  if sum_hand_value(table) > 31:
    print('That card is too big to play. Try again.')
    hand.add(table.get(card_term))
    hand.sort(cribbage_ranks)
    return False
  else:
    # TODO: Score the Table
    action = 'Played {0} {1}'
    print(action.format(card_term, '\n'))
    return True
 
# Deal out the player hands, sort them and initialize an empty crib, cut and board
hero_hand = cards=deck.deal(6)
enemy_hand = cards=deck.deal(6)
hero_hand.sort(cribbage_ranks)
enemy_hand.sort(cribbage_ranks)
crib = pydealer.Stack()
table = cards=pydealer.Stack()

hero_position = position[int(is_hero_dealer)]
enemy_position = position[int(not(is_hero_dealer))]

# Hero discards into the crib
print('You are the %s' % hero_position + '\n')
print_hand('%s\'s hand' % hero_position, hero_hand, show_value)

chuck = input('\nWhich cards do you want to discard to the crib?.\n(Enter two numbers from 1-6 above the cards in the list, separated with a space.)\n').split()
chuck = [int(i)-1 for i in chuck]
 
crib.add(hero_hand.get_list(chuck))
 
# Enemy discards into the crib
enemy_hand.shuffle()             # shuffle the hand so the discard is random
crib.add(enemy_hand.deal(2))
enemy_hand.sort(cribbage_ranks)  # sort the hand so it displays correctly
 
hero_score_term = ' '.join([card.abbrev.rjust(3) for card in hero_hand])
enemy_score_term = ' '.join([card.abbrev.rjust(3) for card in enemy_hand])
 
# Cut for deal
cut = deck.deal(1)
print('Dealer cuts a ' + str(cut[0]) + '\n')
print_hand('%s\'s hand' % hero_position, hero_hand, show_value, True)
if show_enemy_hand:
  print_hand('%s\'s hand' % enemy_position, enemy_hand, show_value, True)
if show_crib:
  print_hand('Crib', crib, show_value)
 
is_hero_turn = not(is_hero_dealer)
go = 0
 
# Play for points
while sum_hand_value(table) < 31 and go < 2 and (hero_hand.size > 0 or enemy_hand.size > 0):
  new_count = sum_hand_value(table)
  count_template = '{0}\'s turn. The Count is {1}'
  card_played = False
 
  if is_hero_turn:
    while not card_played:
      if table.size > 0:
        print_hand(count_template.format(hero_position, str(sum_hand_value(table))), table, False)
      else:
        print('%s\'s turn.' % hero_position)
      print_hand('%s\'s hand' % hero_position, hero_hand, show_value=False)
      card_index = int(input('Enter the card to play or 0 for "Go": ')) - 1
      if card_index == -1:
        go += 1
        print('Go: %s\n' % go)
        continue
      card_term = hero_hand[card_index].abbrev
      card_played = play_card(card_term, hero_hand, table)
    table.add(hero_hand.get(card_term))
  else:
    # TODO: Implement enemy card selection
    card_index = 0
    while not card_played and card_index + 1 != enemy_hand.size:
      if table.size > 0:
        print_hand(count_template.format(enemy_position, str(sum_hand_value(table))), table, False)
      else: 
        print('%s\'s turn.' % enemy_position)
      if show_enemy_hand:
        print_hand('%s\'s hand' % enemy_position, enemy_hand, show_value)
      
      # Pick a card from the enemy deck
      card_term = enemy_hand[card_index].abbrev
      card_played = play_card(card_term, enemy_hand, table)
      if not card_played:
        card_index += 1
        if card_index == enemy_hand.size:
          go += 1
          print('Go: %s\n' % go)
    table.add(enemy_hand.get(card_term))
  is_hero_turn = not is_hero_turn
  # TODO: Fix go condition testing for enemy turn
  if go == 2:
    print('Start next count.')
    table.empty(return_cards=False)
    go = 0

