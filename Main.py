import random
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
    def basicAttack(self,vihollinen):
        vihollinen - random.randint(self.attackMin, self.attackMax)

    #Ui
    sprite = ["      _,.",
              "    ,` -.)",
              "   ( _/-\\\\-._",
              "  /,|`--._,-^|            ,",
              "  \_| |`-._/||          ,'|",
              "    |  `-, / |         /  /",
              "    |     || |        /  /",
              "     `r-._||/   __   /  /",
              " __,-<_     )`-/  `./  /",
              "'  \   `---'   \   /  /",
              "    |           |./  /",
              "    /           //  /",
              "\_/' \         |/  /",
              " |    |   _,^-'/  /",
              " |    , ``  (\/  /_",
              "  \,.->._    \X-=/^",
              "  (  /   `-._//^`",
              "   `Y-.____(__}",
              "    |     {__)",
              "          ()"]

#Viholliset
class Goblini:

    #stats:
    maxHp = 20
    hp = 20
    hyokkaysArvoMin = 5
    hyokkausArvoMax = 10

#Esineet:
def healingPotion(player):
    player + 10

def greaterHealingPotion(player):
    player + 25

def spPotion(player):
    player + 10

def greaterSpPotion(player):
    player + 25

ritari = Ritari
for x in ritari.sprite:
    print(x)
