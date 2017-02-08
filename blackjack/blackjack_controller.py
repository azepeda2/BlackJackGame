
import cgi
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from appengine_utilities import sessions

import deckOfCards
import model

# main page appears on load
class MainPage(webapp.RequestHandler):
  def get(self):
      user=users.get_current_user()
      Messages=db.GqlQuery('Select * from MessageTable')
      session = sessions.Session()
      dealerText=''
      deck=deckOfCards.Deck()
      hand=[deckOfCards.Deck.pickACard(deck),deckOfCards.Deck.pickACard(deck)]          
      i=0
      handTotalA=0
      while i < (len(hand)):
        handTotalA=handTotalA+hand[i].value
        i=i+1
      i=0
      handTotal11=0
      while i < (len(hand)):
        if hand[i].face=='A':
          handTotal11=handTotal11+11
        else:
          handTotal11=handTotal11+hand[i].value
        i=i+1
      if handTotal11 < 22:
        handTotal=handTotal11
      else:
        handTotal=handTotalA
      aiHand=[deckOfCards.Deck.pickACard(deck),deckOfCards.Deck.pickACard(deck)]
      session['aiHand']=aiHand
      session['deck']=deck
      session['hand']=hand
      session['wins']=0
      session['losses']=0
      session['win']=0
      session['loss']=0
      logouturl=users.create_logout_url('/')
      template_values={'wins':session['wins'],'losses':session['losses'],'Messages':Messages,'logouturl':logouturl,'deck':session['deck'],'hand':session['hand'],'handTotal':handTotal}
      # render the page using the template engine
      path = os.path.join(os.path.dirname(__file__),'index.html')
      self.response.out.write(template.render(path,template_values))


class HitMeHandler(webapp.RequestHandler):
  def get(self):
    user=users.get_current_user()
    session=sessions.Session()
    hand=session['hand']
    deck=session['deck']
    loss=session['loss']
    win=session['win']
    loss=0
    win=0
    Messages=db.GqlQuery('Select * from MessageTable')
    
    hand.append(deckOfCards.Deck.pickACard(deck))
    gameStatus=''
    i=0
    handTotalA=0
    while i < (len(hand)):
      handTotalA=handTotalA+hand[i].value
      i=i+1
    i=0
    handTotal11=0
    while i < (len(hand)):
      if hand[i].face=='A':
        handTotal11=handTotal11+11
      else:
        handTotal11=handTotal11+hand[i].value
      i=i+1
    if handTotal11 < 22:
      handTotal=handTotal11
    else:
      handTotal=handTotalA
    
    if handTotal==21:
      gameStatus='Congratulations you are a winner! You are ready for the casinos! If you would like to play again click new game above'
      win=1
    elif handTotal>21:
      gameStatus='Oh no! You passed 21! You Lose! Try again by clicking new game above!'
      loss=1
    session['deck']=deck
    session['hand']=hand
    session['loss']=loss
    session['win']=win
    logouturl=users.create_logout_url('/')
    # set up the template_values with the list of people returned.
    template_values= {'wins':session['wins'],'losses':session['losses'],'Messages':Messages,'logouturl':logouturl,'deck':session['deck'],'hand':session['hand'],'gameStatus':gameStatus,'handTotal':handTotal}
    # render the page using the template engine
    path = os.path.join(os.path.dirname(__file__),'index.html')
    self.response.out.write(template.render(path,template_values))

class HoldHandler(webapp.RequestHandler):
    def get(self):
      user=users.get_current_user()
      session= sessions.Session()
      aiHand=session['aiHand']
      hand=session['hand']
      deck=session['deck']
      Messages=db.GqlQuery('Select * from MessageTable')
      loss=session['loss']
      win=session['win']
      gameStatus=''
      i=0
      handTotalA=0
      while i < (len(hand)):
        handTotalA=handTotalA+hand[i].value
        i=i+1
      i=0
      handTotal11=0
      while i < (len(hand)):
        if hand[i].face=='A':
          handTotal11=handTotal11+11
        else:
          handTotal11=handTotal11+hand[i].value
        i=i+1
      if handTotal11 < 22:
        handTotal=handTotal11
      else:
        handTotal=handTotalA
      i=0
      aiTotal=0
      while i < (len(aiHand)):
        aiTotal=aiTotal+aiHand[i].value
        i=i+1
      if handTotal<21 or handTotal==21:
        while aiTotal<17 and aiTotal!=21:
          aiHand.append(deckOfCards.Deck.pickACard(deck))
          i=0
          aiTotal=0
          while i < (len(aiHand)):
            aiTotal=aiTotal+aiHand[i].value
            i=i+1
      
      #history=db.GqlQuery('Select * from ScoreHistory where user= :1', user)
      #score=history.get(userHistory)
      if handTotal==21 and aiTotal!=21:
        gameStatus='Congratulations you are a winner! You are ready for the casinos! If you would like to play again click new game above'
        win=1
      elif handTotal>21:
        gameStatus='Oh no! You passed 21! You Lose! Try again by clicking new game above!'
        loss=1
      elif handTotal==21 and aiTotal==21:
        gameStatus='Oh no! You and the dealer both have 21! What are the odds? New game? click above.'
        loss=1
      elif handTotal< aiTotal and aiTotal<22:
        gameStatus='Looks like the dealer has won! Time to watch the movie 21 and try again!'
        loss=1
      elif aiTotal< handTotal and handTotal<22:
        gameStatus='We have a winner! Looks like you took my advice and watched the movie 21! Would you like to play again? Click new game above!'
        win=1
      elif handTotal<22 and aiTotal>21:
        gameStatus='We have a winner! Looks like you took my advice and watched the movie 21! Would you like to play again? Click new game above!'
        win=1
      aiTotal='Dealers Total: '+ str(aiTotal)
      dealerText='Dealers Hand:'
      session['deck']=deck
      session['loss']=loss
      session['win']=win
      #userScore=model.ScoreHistory()
      #userScoreHistory=query.get()
      #userScore.wins=0
      #userScore.losses=0
      #userScore.user=user
      #userScore.put()
      #userHistory=db.GqlQuery('Select * from ScoreHistory where user= :1', user)
      logouturl=users.create_logout_url('/')
      template_values= {'wins':session['wins'],'losses':session['losses'],'Messages':Messages,'logouturl':logouturl,'deck':session['deck'],'hand':session['hand'],'gameStatus':gameStatus,'handTotal':handTotal, 'aiTotal':aiTotal,'dealerText':dealerText,'aiHand':aiHand}
      # render the page using the template engine
      path = os.path.join(os.path.dirname(__file__),'index.html')
      self.response.out.write(template.render(path,template_values))

class SubmitMessageHandler(webapp.RequestHandler):
 def get(self):
      session=sessions.Session()
      user= users.get_current_user()
      status=self.request.get('statusText')
      hand=session['hand']
      losses=session['losses']
      wins=session['wins']
      Messages=db.GqlQuery('Select * from MessageTable')
      gameStatus=''
      i=0
      handTotalA=0
      while i < (len(hand)):
        handTotalA=handTotalA+hand[i].value
        i=i+1
      i=0
      handTotal11=0
      while i < (len(hand)):
        if hand[i].face=='A':
          handTotal11=handTotal11+11
        else:
          handTotal11=handTotal11+hand[i].value
        i=i+1
      if handTotal11 < 22:
        handTotal=handTotal11
      else:
        handTotal=handTotalA
      Message=model.MessageTable()
      Message.statusMessage=status
      Message.user=user
      Message.put()
      Messages=db.GqlQuery('Select * from MessageTable')
      logouturl=users.create_logout_url('/')
      template_values={'handTotal':handTotal,'hand':session['hand'],'wins':session['wins'],'losses':session['losses'],'Messages':Messages,'logouturl':logouturl}
      # render the page using the template engine
      path = os.path.join(os.path.dirname(__file__),'index.html')
      self.response.out.write(template.render(path,template_values))


class NewGameHandler(webapp.RequestHandler):
    def get(self):
      user=users.get_current_user()
      session = sessions.Session()
      losses=session['losses']
      wins=session['wins']
      loss=session['loss']
      win=session['win']
      dealerText=''
      deck=deckOfCards.Deck()
      hand=[deckOfCards.Deck.pickACard(deck),deckOfCards.Deck.pickACard(deck)]
      aiHand=[deckOfCards.Deck.pickACard(deck),deckOfCards.Deck.pickACard(deck)]
      gameStatus=''
      i=0
      handTotalA=0
      while i < (len(hand)):
        handTotalA=handTotalA+hand[i].value
        i=i+1
      i=0
      handTotal11=0
      while i < (len(hand)):
        if hand[i].face=='A':
          handTotal11=handTotal11+11
        else:
          handTotal11=handTotal11+hand[i].value
        i=i+1
      if handTotal11 < 22:
        handTotal=handTotal11
      else:
        handTotal=handTotalA
      session['aiHand']=aiHand
      session['deck']=deck
      session['hand']=hand
      session['losses']=losses+loss
      session['wins']=wins+win
      session['loss']=0
      session['win']=0
      Messages=db.GqlQuery('Select * from MessageTable')
      logouturl=users.create_logout_url('/')
      template_values={'wins':session['wins'],'losses':session['losses'],'Messages':Messages,'logouturl':logouturl,'deck':session['deck'],'hand':session['hand'],'handTotal':handTotal}
      # render the page using the template engine
      path = os.path.join(os.path.dirname(__file__),'index.html')
      self.response.out.write(template.render(path,template_values))


# create this global variable that represents the application and specifies which class
# should handle each page in the site
application = webapp.WSGIApplication(
					# MainPage handles the home load
                                     [('/', MainPage),
					# when user clicks on add button, we call on_add action
					# check out index.html to see where on_add gets submitted
                                       ('/newgame',NewGameHandler),
                                      ('/Hit_Me', HitMeHandler),
                                     ('/Hold', HoldHandler),
                                      ('/submit_message', SubmitMessageHandler)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
