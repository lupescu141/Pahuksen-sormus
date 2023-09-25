import random
import tkinter
from tkinter import *
import keyboard
from PIL import Image, ImageTk





#Pelaajan tiedot:
playerName = 'player'

#Hahmot
class Ritari:

    #Stats:
    maxHp = 100
    hp = 100
    maxSp = 20
    sp = 20
    attackMin = 4
    attackMax = 10
    inventory = []

    #Taidot
    def basicAttack(self, vihollinen):
        damage = random.randint(self.attackMin, self.attackMax)
        vihollinen.hp -= damage


#Enemies
class Goblini:

    #stats:
    name = "Goblin"
    maxHp = 20
    hp = 20




#Items:
def healingPotion(player):
    player + 10

def greaterHealingPotion(player):
    player + 25

def spPotion(player):
    player + 10

def greaterSpPotion(player):
    player + 25

ritari = Ritari


#Combat funktion
def fight(player, enemy):
    currentEnemy = enemy()
    while True:

        print(f"    {playerName}                        {currentEnemy.name}  \n"
              f"----------------            ----------------\n"
              f"  HP: {player.hp} / {player.maxHp}               HP: {currentEnemy.hp} / {currentEnemy.maxHp}   \n"
              f"  SP: {player.sp} / {player.maxSp}               ----------------\n"
              f"----------------")
        print("  (1) Aatack     ")
        print(" --------------- ")
        userInput = input()
        if userInput == "1":
            player.basicAttack(player, currentEnemy)

        if player.hp <= 0:
            print("GAME OVER")
            break
        elif currentEnemy.hp <= 0:
            print("VICTORY")
            break


fight(ritari,Goblini)
fight(ritari,Goblini)





