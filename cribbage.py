import pydealer
import itertools
from cribbageHand import CribbageHand
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-e', '--enemy', required=False, help='Show the enemy hand during play')
ap.add_argument('-c', '--crib', required=False, help='Show the crib during play')
ap.add_argument('-a', '--autoplay', required=False, help='Computer plays against itself')
ap.add_argument('-s', '--strategy', required=False, help='Specifies the strategy used by the enemy. ' +
                                                         'In autoplay mode, add a comma and specify the strategy used by the hero')
args = vars(ap.parse_args())
print(args)

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

deck = pydealer.Deck(ranks=cribbage_ranks)
deck.shuffle()
cut = pydealer.Stack()
 
# Define a list of player positions and seed the isHeroDealer
position = ['Pone', 'Dealer']
isHeroDealer = True

def printHand(handName, hand, showValue=True):
  global cut
 
  if cut.size == 1 and showValue:
    cutTerm = cut[0].abbrev
    hand.add(cut.get(cutTerm))
 
  scoreHand = CribbageHand(cards=hand)
  handTemplate = '{0} value: {1}'
  cards = ' '.join([card.abbrev.rjust(3) for card in hand])
 
  if showValue:
    if scoreHand.size < 6:
      scoreFlush = scoreHand.score_flush()
    else:
      scoreFlush = 0
 
    printedScore = handTemplate.format(handName, str(scoreHand.score()))
    scoreTemplate = '15\'s: {0} Pairs: {1} Runs: {2} Flush: {3} Knobs: {4}'
    printedCount = scoreTemplate.format(str(scoreHand.score_fifteens()),
                                        str(scoreHand.score_pairs()),
                                        str(scoreHand.score_runs()),
                                        str(scoreFlush),
                                        str(scoreHand.score_knobs()))
  else:
    printedScore = handName
 
  indexString = ' 1  '
  for i in range(2,hand.size+1):
    indexString = indexString + ' %s  ' % str(i)
 
  if hand.size == 5:
    indexString = indexString.replace('5', 'Cut')
    cut.add(hand.get(cutTerm))
 
  print(printedScore + '\n')
  print(indexString)
  print('-' * len(indexString))
  print(cards)
  print('-' * len(indexString))
  if showValue:
    print(printedCount + '\n')
 
def sumHandValue(hand):
  hand = CribbageHand(cards = hand)
  count = 0
  for card in hand:
    count = count + card.count_value
  return count
 
def playCard(cardTerm, hand, table):
  table.add(hand.get(cardTerm))
  if sumHandValue(table) > 31:
    print('That card is too big to play. Try again.')
    hand.add(table.get(cardTerm))
    hand.sort(cribbage_ranks)
    return False
  else:
    action = 'Played {0} {1}'
    print(action.format(cardTerm, ''))
    return True
 
# Deal out the player hands, sort them and initialize an empty crib, cut and board
heroHand = cards=deck.deal(6)
enemyHand = cards=deck.deal(6)
heroHand.sort(cribbage_ranks)
enemyHand.sort(cribbage_ranks)
crib = pydealer.Stack()
table = cards=pydealer.Stack()

heroPosition = position[int(isHeroDealer)]
enemyPosition = position[int(not(isHeroDealer))]

# Hero discards into the crib
print('You are the %s' % heroPosition + '\n')
printHand('%s\'s hand' % heroPosition, heroHand, False)

chuck = input('\nWhich cards do you want to discard to the crib?.\n(Enter two numbers from 1-6 above the cards in the list, separated with a space.)\n').split()
chuck = [int(i)-1 for i in chuck]
 
crib.add(heroHand.get_list(chuck))
 
# Enemy discards into the crib
enemyHand.shuffle()             # shuffle the hand so the discard is random
crib.add(enemyHand.deal(2))
enemyHand.sort(cribbage_ranks)  # sort the hand so it displays correctly
 
heroScoreTerm = ' '.join([card.abbrev.rjust(3) for card in heroHand])
enemyScoreTerm = ' '.join([card.abbrev.rjust(3) for card in enemyHand])
 
# Cut for deal
cut = deck.deal(1)
print('Dealer cuts a ' + str(cut[0]) + '\n')
printHand('%s\'s hand' % heroPosition, heroHand)
printHand('%s\'s hand' % enemyPosition, enemyHand)
printHand('Crib', crib)
 
isHeroTurn = not(isHeroDealer)
go = 0
 
# Play for points
while sumHandValue(table) < 31 and (heroHand.size > 0 or enemyHand.size > 0):
  newCount = sumHandValue(table)
  countTemplate = '{0}\'s turn. The count is {1}.\n'
  cardPlayed = False
 
  if isHeroTurn:
    while not cardPlayed:
      print(countTemplate.format(heroPosition, str(sumHandValue(table))))
      printHand('%s\'s hand' % heroPosition, heroHand, showValue=False)
      cardIndex = int(input('Enter the card to play or 0 for "Go": ')) - 1
      if cardIndex == -1:
        go += 1
        continue
      cardTerm = heroHand[cardIndex].abbrev
      cardPlayed = playCard(cardTerm, heroHand, table)
    table.add(heroHand.get(cardTerm))
  else:
    # TODO: Implement enemy card selection
    cardIndex = 0
    while not cardPlayed and cardIndex + 1 != enemyHand.size:
      print(countTemplate.format(enemyPosition, str(sumHandValue(table))))
      printHand('%s\'s hand' % enemyPosition, enemyHand, showValue=False)
      # Pick a card from the enemy deck
      cardTerm = enemyHand[cardIndex].abbrev
      cardPlayed = playCard(cardTerm, enemyHand, table)
      if not cardPlayed:
        cardIndex += 1
        if cardIndex == enemyHand.size:
          go += 1
    table.add(enemyHand.get(cardTerm))
  isHeroTurn = not isHeroTurn
  # TODO: Fix go condition testing for enemy turn
  if go == 2:
    table.empty(return_cards=False)