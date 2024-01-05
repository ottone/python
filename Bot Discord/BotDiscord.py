

# https://discord.com/api/oauth2/authorize?client_id=1191883947416768632&permissions=2048&scope=bot

from requests import get
import discord
from discord.ext.tasks import loop


intents = discord.Intents.default()
bot = discord.Client(intents=intents)
intents.message_content = True


CHANNEL_ID = 1191882886752764038
TOKEN = "MTE5MTg4Mzk0NzQxNjc2ODYzMg.GyRoF3.F4qrAETYsSEoERY90WFemFI2Yap2TAFHv_ZDXs"
FILENAME = 'prezzo_target.txt'


def get_prezzo_target():
    with open(FILENAME) as f:
        prezzo_target = int(f.read())
    return prezzo_target

def set_prezzo_target(nuovo_prezzo_target):
    with open(FILENAME, 'w') as f:
        f.write(nuovo_prezzo_target)

@bot.event
async def on_ready():
    invia_quotazione.start()

@loop(seconds=1)
async def invia_quotazione():
    response = get("https://api.kucoin.com/api/v1/market/stats?symbol=BTC-EUR")
    prezzo_attuale = float(response.json()['data']['buy'])
    canale = bot.get_channel(CHANNEL_ID)
    testo = f'Il prezzo attuale per 1 BTC è pari a {prezzo_attuale} euro'
    if prezzo_attuale < get_prezzo_target():
        await canale.send(testo)
        await canale.send("E' arrivata l'ora di comprare 🤑🤑🤑")

@bot.event
async def on_message(message):
    autore = message.author 
    testo = message.content
    canale = message.channel
    if autore == bot.user:
        return
    if message.content.startswith('!prezzo'):
        nuovo_prezzo_target = testo.split()[1]
        await canale.send(f'Nuovo prezzo {nuovo_prezzo_target}!')
        set_prezzo_target(nuovo_prezzo_target)
        return
    await canale.send(f'Ciao {autore.name}  😊')
    await canale.send(f'Ti avviso quando 1 BTC costa meno di {get_prezzo_target()}!')
    await canale.send(f'Per modificare il prezzo target usa il comando `!prezzo <nuovo prezzo target>`')



bot.run(TOKEN)