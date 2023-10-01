import keyboard

esinelista = ["eliksiiri","taito eliksiiri"]
inventaario = [1,2,1]

def tulosta_inventaario():

    numero = 1
    for x in inventaario:
        print(f"{numero}. {esinelista[x - 1]}")
        numero += 1


def käytä_esine():

    tulosta_inventaario()

    while True:
        if keyboard.is_pressed("1"):
            inventaario.pop(0)
            break

        if keyboard.is_pressed("2"):
            inventaario.pop(1)
            break

        if keyboard.is_pressed("3"):
            inventaario.pop(2)
            break


käytä_esine()
print("käytön jälkeen:")
tulosta_inventaario()
