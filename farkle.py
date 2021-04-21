#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 17:02:12 2020

@author: pete
"""

import random
#from PIL import Image

#OBJECTS
"""
#to be used at a later date
one = Image.open("one.png")
two = Image.open("two.png")
three = Image.open("three.png")
four = Image.open("four.png")
five = Image.open("five.png")
six = Image.open("six.png")
"""

def image(list):
    #list = the dice rolls, in list form
    for each in list:
        if each == 1:
            one.show()
        if each == 2:
            two.show()
        if each == 3:
            three.show()
        if each == 4:
            four.show()
        if each == 5:
            five.show()
        if each == 6:
            six.show()

class Die(object):
    @classmethod        #This means i dont have to make an instance of the class to use roll. Essentially a normal function.
    def roll(self):
        return random.choice((1,2,3,4,5,6))
    
class Player(object):
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.turns = 0
        self.everHitFiveHundred = False
    def getName(self):
        return self.name
    def addScore(self, score):
        self.score += score
    def getScore(self):
        return self.score
    def addTurn(self):
        self.turns += 1
    def getTurns(self):
        return self.turns
    def updateEverHitFiveHundred(self, yes):
        if yes == True:
            self.everHitFiveHundred = True
    def getEverHitFiveHundred(self):
        return self.everHitFiveHundred
            

#HELPER FUNCTIONS - ROLL and SCORING

def rollThisManyDice(num_of_dice):
    result = []
    for eachDie in range(num_of_dice):
        result.append(Die.roll())
    return result

def makeitadictionary(result):
    count = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
    for each in result:
            count[each] += 1
    return count
        
def calculateScore(result):
    score = 0
    count = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0} #Spots on dice: How many of each
    try:
        for each in result:
            count[each] += 1
    except:
        return int(score)  #try/except is to return 0 if no dice.
    for key in count:     #could do count.keys() but it's redundant
        if count[key] == 6:
            score += 3000
            count[key] = 0
        elif count[key] == 5:
            score += 2500
            count[key] = 0
        elif count[key] == 4:
            score += 1000
            count[key] = 0
            for anotherPair in count:
                if count[anotherPair] == 2:
                    score = 1500
                    count[anotherPair] = 0
        elif count[key] == 3:
            if key == 1:
                score += 300
            score += key*100
            count[key] = 0
            for anotherTriple in count:
                if count[anotherTriple] == 3:
                    score = 2500
                    count[anotherTriple] = 0
        elif count[key] == 2:
            for secondPair in count:
                if secondPair > key and count[secondPair] == 2:
                    for thirdPair in count:
                        if thirdPair > secondPair and count[thirdPair] == 2:
                            score += 1500
                            count[key] = 0
                            count[secondPair] = 0
                            count[thirdPair] = 0 
                            break        #Need to check on this. Trying to score three triples.
            if key == 1 and count[key] == 2:
                score += 200
                count[key] = 0
            elif key == 5 and count[key] == 2:
                score += 100
                count[key] = 0
        elif count[key] == 1:
            if key == 1:
                score += 100
                count[key] = 0
            elif key == 5:
                score += 50
                count[key] = 0
    return int(score)
    
def turn(playerlist):
    highScore = 0
    while highScore < 10000:
        for each in playerlist:
            print("It is ", each.getName(), "'s turn.")
            diceLeft = 6
            farkle = False
            tempScore = 0
            while diceLeft > 0:
                while farkle == False:
                    x = input("Are you ready to roll? Type r to roll or e to end turn.")
                    if x == "r":
                        #roll dice
                        y = rollThisManyDice(diceLeft)
                        #turn dice roll from a list to a dictionary, as a helper object
                        tempDict = makeitadictionary(y)
                        #check for farkle
                        if calculateScore(y) == 0:
                            print("You rolled", makeitadictionary(y))
                            print("You farkled! End of turn. Bad luck!")
                            print("You scored: 0 this round.")
                            print("Your cumulative score is: ",each.getScore())
                            each.addTurn()
                            diceLeft = 0
                            farkle = True
                        else:
                            #display the roll
                            print("You rolled", makeitadictionary(y))
                            #find out which dice to keep
                            tempResult = []
                            #check to see if chosen dice are in the dictionary (enough dice?), then add to the tempResult list
                            while True:
                                z = input("Which dice would you like to keep? (Ex. If you want three fives 555). If none, end turn('e')): ")
                                try:
                                    for chosen in z:
                                        if tempDict[int(chosen)] > 0: #if a legitimate choice
                                            tempResult.append(int(chosen))
                                            tempDict[int(chosen)] -= 1
                                        else:
                                            raise ValueError
                                    break #to exit the while loop
                                except:
                                    print("Please try again")
                            #calculate each roll's score
                            tempScore = tempScore + calculateScore(tempResult)
                            print("Your score so far is: ",tempScore)
                            #reduce the dice in the hand to be rolled again
                            diceLeft -= len(tempResult)  
                            #check to see if all 6 dice scored
                            if calculateScore(tempResult) > 0 and diceLeft == 0:
                                print("You successfully rolled all 6 die! You get to roll again.")
                                diceLeft = 6
                        break
                    if x == "e":
                        each.addScore(tempScore)
                        each.addTurn()
                        if each.getScore() > highScore:
                            highScore = each.getScore()
                            if highScore > 10000:
                                print("End of turn")
                                print("You scored: ",tempScore," this round.")
                                print("Your cumulative score is: ",each.getScore())
                                print("You've crossed 10,000! One last turn for everyone else.")
                                break
                        print("End of turn")
                        print("You scored: ",tempScore," this round.")
                        print("Your cumulative score is: ",each.getScore())
                        print("You have had", each.getTurns(), "turns.")
                        diceLeft = 0
                        farkle = True


#COMPUTER OPPONENT AI -- TBD
                        
#HELPER FUNCTION to choose dice to keep
"""
def keep(choice, roll):
    for each in choice:
        if roll
 """      

#THE GAME

def farkle():
    introduction()      #Just making it easier to read, breaking it into segment functions
    playerlist = []     #I should make each player in the list a Player class object, so i can assign scores and names to that object
    topscore = 0
    x = int(input("How many humans players will be playing? "))
    for each in range(x):
        name = input("What is human player %i's name? " % int(each+1))     #string formatting with %!
        playerlist.append(Player(name))
    turn(playerlist)
                    
                
    #last round:
    #everyone but the player with the topscopre, plays another hand.
    
def introduction():
    print("Welcome to Farkle!")
    print("Let's begin.")
    
def getplayerinfo():
    eplayerlist = []     #I should make each player in the list a Player class object, so i can assign scores and names to that object
    x = int(input("How many Players will be playing? "))
    
def basics():
    playerlist = ["Person"]
    score = 0
    return playerlist

        
"""
I may need some while loops instead of if statements, to keep asking until dice

Objects: Players, Dice
Introdution()
Round() cycle through the people until score > 10,000
    Turn() continues while # dice > 0... 

[Turn should look somethingl like this...]
Handscore = 0
Dice = 6
You have [Dice] dice remaining in your hand:
You may Roll (r) or End turn (e),
while Dice > 0:
If End turn, then: "Your score was Handscore, well done!" / break  (while or If....)
    Player.addScore(Handscore)
If Roll, print[1,2,3,4,5,6] x = rollThisManyDice(Dice) -- maybe i need to put this into a Dict
y = Which dice do you want to keep? The first, second, third, etc? ie 235   str(input())
Dice = Dice - len(y)    #so as to reduce the number of dice... and keep the while Dice loop running
handtoscore = []
for each in y:
    handtoscore.append(x[each])
calculateScore(handtoscore)
if len(handtoscore) == 0:
    print("FARKLE!")
    Handscore = 0
If player.getscore() is > topscore, topscore = player.getscore()

"""
"""
a = Player("Peter")
a.addScore(100)
print(a.getName(), a.getScore())
"""