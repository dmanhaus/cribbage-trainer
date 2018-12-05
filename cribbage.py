import pydealer
import itertools
from cribbageHand import CribbageHand

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
 
# Define a list of player positions and seed the isHeroDealer
position = ['Pone', 'Dealer']
isHeroDealer = True
 
def printHand(handName, hand):
  handTemplate = '{0} (value: {1})'
  scoringHand = CribbageHand(cards=hand)
  score = scoringHand.score()
  print()
  print(handTemplate.format(handName, str(score)))
  print('-' * len(handTemplate.format(handName, str(score))))
  print(hand)
 
# Deal out the player hands, sort them and initialize an empty crib, cut and board
heroHand = deck.deal(6)
enemyHand = deck.deal(6)
heroHand.sort()
enemyHand.sort()
crib = pydealer.Stack()
table = pydealer.Stack()

heroPosition = position[int(isHeroDealer)]
enemyPosition = position[int(not(isHeroDealer))]
 
# Hero discards into the crib
print('You are the %s' % heroPosition)
printHand('%s\'s hand' % heroPosition, heroHand)
 
chuck = input('\nName the cards to throw in the crib. (separate them with a comma) \n').split(',', 1)
 
for card in chuck:
  crib.add(heroHand.get(card.strip()))
 
printHand('%s\'s hand' % heroPosition, heroHand)
 
# Enemy discards into the crib
crib.add(enemyHand.deal(2))
 
printHand('%s\'s hand' % enemyPosition, enemyHand)
printHand('Crib', crib)
 
# Cut for deal
cut = deck.deal(1)
print('\nDealer cuts a ' + str(cut[0]))