import discord 
import random
import os
from discord.ext import commands, tasks
from itertools import cycle
client = commands.Bot(command_prefix = '!') #created an instance of a bot and set it to a client variable 
status = cycle(['Alive', 'Dead']) 

#players = {}

@client.event
async def on_ready(): #made an event 
    change_status.start()
    print("bot is ready")

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'): #looping through the cogs directory and checks if the file is a python file
        client.load_extension(f'cogs.{filename[:-3]}')

@client.command()
async def ping(ctx): 
    await ctx.send(f'pong! {round(client.latency * 1000)}ms') #when the command is run, the bot will say pong

@client.command()
@commands.has_permissions(manage_messages=True)
async def kick(ctx, member : discord.Member, *, reason = None): 
    await member.kick(reason = reason)

@client.command()
@commands.has_permissions(manage_messages=True)
async def ban(ctx, member : discord.Member, *, reason = None): 
    await member.ban(reason = reason)
    await ctx.send(f'banned {member.mention}')

@client.command(aliases = ['8ball'])
async def _8ball(ctx, *, question):
    responses = ["As I see it, yes.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
             "Don’t count on it.", "It is certain.", "It is decidedly so.", "Most likely.", "My reply is no.", "My sources say no.",
             "Outlook not so good.", "Outlook good.", "Reply hazy, try again.", "Signs point to yes.", "Very doubtful.", "Without a doubt.",
             "Yes.", "Yes, definitely.", "You may rely on it."]
    await ctx.send(f'Question: {question}\nAnswe: {random.choice(responses)}') #print the question and the response picks a random answer


@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans() #method of guild that goes through all the banned users and generates a list of them in a banned entry 
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if(user.name, user.discriminator) == (member_name, member_discriminator): #taking the name and discriminator of the user by making a tuple 
            await ctx.guild.unban(user)
            await ctx.send(f"unbanned {user.mention}")
            return 
@tasks.loop(seconds = 10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('invalid command used')

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int): #the default value 5 will be used when the amount is not specified 
    await ctx.channel.purge(limit=amount) #taking the context and accessing the channel, determining how many messages are going to be purged
    
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('please specify an amount of messages to delete')

client.run('OTI3Mzg4NTM0NDQzMjE2OTI2.YdJf4A.HSO3SMAqobthvGF0CmlGIVD3jTY') #running the bot using it's token 
