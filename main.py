import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
import random

updateId = None
# enter your token here:
token = ''
alphabet = 'abcdefghijklmnopqrstuvwxyz '

def init_rotor():
    random.seed(27)
    rotor1 = list(alphabet)
    random.shuffle(rotor1)
    rotor1 = ''.join(rotor1)
    random.seed(28)
    rotor2 = list(alphabet)
    random.shuffle(rotor2)
    rotor2 = ''.join(rotor2)
    random.seed(29)
    rotor3 = list(alphabet)
    random.shuffle(rotor3)
    rotor3 = ''.join(rotor3)
    return rotor1, rotor2, rotor3

def rotate_rotors(rotorsState, r1, r2, r3):
    r1 = r1[1:] + r1[0]
    if rotorsState % 26:
        r2 = r2[1:] + r2[0]
    if rotorsState % (26*26):
        r3 = r3[1:] + r3[0]
    return r1, r2, r3
    
def reflector(c):
    elementIndex = alphabet.find(c)
    return alphabet[len(alphabet) - elementIndex - 1]

def enigma_one_character(c, r1, r2, r3):
    c1 = r1[alphabet.find(c)]
    c2 = r2[alphabet.find(c1)]
    c3 = r3[alphabet.find(c2)]
    reflected = reflector(c3)
    c3 = alphabet[r3.find(reflected)]
    c2 = alphabet[r2.find(c3)]
    c1 = alphabet[r1.find(c2)]
    return c1

def cipher(text, r1, r2, r3):
    rotorsState = 0
    cipher_text = ''
    for c in text:
        rotorsState += 1
        cipher_text += enigma_one_character(c, r1, r2, r3)
        r1, r2, r3 = rotate_rotors(rotorsState, r1, r2, r3)
    return cipher_text

def main():
    global updateId
    bot = telegram.Bot(token)
    try:
        updateId = bot.getUpdates()[0].update_id
    except IndexError:
        updateId = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            echo(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            updateId += 1

def echo(bot):
    global updateId
    for update in bot.getUpdates(offset=updateId, timeout=10):
        chatId = update.message.chat_id
        updateId = update.update_id + 1

        if update.message:
            r1, r2, r3 = init_rotor()
            incommingMessage = update.message.text
            m = cipher(incommingMessage, r1, r2, r3)
            bot.sendMessage(chat_id=chatId, text=m)

if __name__ == '__main__':
    main()
