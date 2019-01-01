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
showValue = args["show"]>0
showCrib = args["show"]>=2
showEnemyHand = args["show"]==3

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
 
# Define a list of player positions and seed the isHeroDealer
position = ['Pone', 'Dealer']
isHeroDealer = True

def printHand(handName, hand, showValue=True, addCut=False):
  global cut
 
  if addCut and cut.size == 1:
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
 
  if addCut and hand.size == 5:
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
    # TODO: Score the Table
    action = 'Played {0} {1}'
    print(action.format(cardTerm, '\n'))
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
printHand('%s\'s hand' % heroPosition, heroHand, showValue)

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
printHand('%s\'s hand' % heroPosition, heroHand, showValue, True)
if showEnemyHand:
  printHand('%s\'s hand' % enemyPosition, enemyHand, showValue, True)
if showCrib:
  printHand('Crib', crib, showValue)
 
isHeroTurn = not(isHeroDealer)
go = 0
 
# Play for points
while sumHandValue(table) < 31 and go < 2 and (heroHand.size > 0 or enemyHand.size > 0):
  newCount = sumHandValue(table)
  countTemplate = '{0}\'s turn. The Count is {1}'
  cardPlayed = False
 
  if isHeroTurn:
    while not cardPlayed:
      if table.size > 0:
        printHand(countTemplate.format(heroPosition, str(sumHandValue(table))), table, False)
      else:
        print('%s\'s turn.' % heroPosition)
      printHand('%s\'s hand' % heroPosition, heroHand, showValue=False)
      cardIndex = int(input('Enter the card to play or 0 for "Go": ')) - 1
      if cardIndex == -1:
        go += 1
        print('Go: %s\n' % go)
        continue
      cardTerm = heroHand[cardIndex].abbrev
      cardPlayed = playCard(cardTerm, heroHand, table)
    table.add(heroHand.get(cardTerm))
  else:
    # TODO: Implement enemy card selection
    cardIndex = 0
    while not cardPlayed and cardIndex + 1 != enemyHand.size:
      if table.size > 0:
        printHand(countTemplate.format(enemyPosition, str(sumHandValue(table))), table, False)
      else: 
        print('%s\'s turn.' % enemyPosition)
      if showEnemyHand:
        printHand('%s\'s hand' % enemyPosition, enemyHand, showValue)
      
      # Pick a card from the enemy deck
      cardTerm = enemyHand[cardIndex].abbrev
      cardPlayed = playCard(cardTerm, enemyHand, table)
      if not cardPlayed:
        cardIndex += 1
        if cardIndex == enemyHand.size:
          go += 1
          print('Go: %s\n' % go)
    table.add(enemyHand.get(cardTerm))
  isHeroTurn = not isHeroTurn
  # TODO: Fix go condition testing for enemy turn
  if go == 2:
    print('Start next count.')
    table.empty(return_cards=False)
    go = 0

