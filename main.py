import discord 
from discord.ext import commands
import requests
from host import host

TOKEN = " " # BOT TOKEN HERE

client = commands.Bot(command_prefix = ',')

BASE_URL = "https://data.nba.net"
ALL_JSON = "/prod/v1/today.json"

data = requests.get(BASE_URL + ALL_JSON).json()
links = data['links']
scoreboard = links['scoreboard']

def get_links():
    data = requests.get(BASE_URL + ALL_JSON).json()
    links = data['links']
    return links

scoreboard = get_links()['currentScoreboard']
games = requests.get(BASE_URL + scoreboard).json()['games']

for game in games:
    home_team = game['hTeam']
    away_team = game['vTeam']
    clock = game['clock']
    period = game['period']

@client.event
async def on_ready():
    print('Logged in.')

@client.command(aliases = ['latency'])
async def _latency(ctx):
    await ctx.send(f'{round(client.latency * 1000)} ms')

@client.command(aliases = ['stats'])
async def _stats(ctx):
    embed = discord.Embed(
        title = "NBA Live Game Stats",
        description = f"{home_team['triCode']}: {home_team['score']} - {away_team['triCode']}: {away_team['score']}\nPeriod: {period['current']} - Clock: {clock}",
        color = discord.Color.red()
    )
    await ctx.send(embed=embed)

host()
client.run(TOKEN)
