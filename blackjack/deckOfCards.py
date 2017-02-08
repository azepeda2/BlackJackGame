import random

class Card:
        def __init__(self,suit,value,face,image):
                self.suit=suit
                self.value=value
                self.face=face
                self.image=image


class Deck:
        def __init__(self):
                self.listOfCards=[]
                faces=['A','2','3','4','5','6','7','8','9','10','J','Q','K']
                values=[1,2,3,4,5,6,7,8,9,10,10,10,10]
                i=0
                while i<13:
                        c = Card("Spades",values[i],faces[i],'/images/s'+str(i+1)+'.gif')
                        self.listOfCards.append(c)
                        i=i+1
                i=0
                while i<13:
                        c = Card("Hearts",values[i],faces[i],'/images/h'+str(i+1)+'.gif')
                        self.listOfCards.append(c)
                        i=i+1
                i=0
                while i<13:
                        c = Card("Clubs",values[i],faces[i],'/images/c'+str(i+1)+'.gif')
                        self.listOfCards.append(c)
                        i=i+1
                i=0
                while i<13:
                        c = Card("Diamonds",values[i],faces[i],'/images/d'+str(i+1)+'.gif')
                        self.listOfCards.append(c)
                        i=i+1
                        
        def pickACard(self):
                num=random.randint(0,len(self.listOfCards)-1)
                card=self.listOfCards[num]
                self.listOfCards.remove(card)
                return card
# main

#deck = Deck()
#i=0
#while i<len (deck.listOfCards):
#        card= deck.pickACard()
#        print card.suit, card.face, card.image

#while i < (len(deck.listOfCards)-1):
       # print deck.listOfCards[i].suit,deck.listOfCards[i].value,deck.listOfCards[i].face
        #i=i+1
