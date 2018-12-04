import pydealer

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

def printHand(handName, hand):
  handTemplate = '{0} (value: {1})'
  score = scoreHand(hand)
  print()
  print(handTemplate.format(handName, str(score)))
  print('-' * len(handTemplate.format(handName, str(score))))
  print(hand)

def scoreHand(hand):
  return 19

heroHand = deck.deal(6)
enemyHand = deck.deal(6)
crib = pydealer.Stack()
heroHand.sort()
enemyHand.sort()

position = ['Pone', 'Dealer']
isDealer = True
heroPosition = position[int(isDealer)]
enemyPosition = position[int(not(isDealer))]

print('You are the %s' % heroPosition)
printHand('%s\'s hand' % heroPosition, heroHand)

chuck = input('Name the cards to throw in the crib. (separate them with a comma) \n').split(',', 1)

for card in chuck:
  crib.add(heroHand.get(card.strip())) 

crib.sort()

printHand('%s\'s hand' % heroPosition, heroHand)

printHand('Crib', crib)

printHand('%s\'s hand' % enemyPosition, enemyHand)

