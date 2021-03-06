#!/usr/bin/env python3
try:
    import discord
    from discord.ext import commands
except:
    print("You need to install the discord.py api")
    sys.exit(-1)
import re
import config
from pymongo import MongoClient

client = MongoClient()

#our db
db = client.isabelle
#our collection
codes = db.switch

#3ds_codes = db.3ds
#wiiu_codes = db.wiiu

bot = commands.Bot(command_prefix="~")
botAuth = config.token



@bot.event
async def on_ready():
    print('Logged in as: '+ bot.user.name)
    print ('ID: ' +bot.user.id)
    print('Friend code database: '+str(db))
    print('There are '+str(codes.find({}).count())+' friend codes in the database')
    print('------')
    await bot.change_presence(game=discord.Game(name='Type ~help'))




@bot.command(pass_context=True,description='Register your FC with Isabelle.\n Use !register SW-5208-7719-6394 with your corresponding FC, it has to be in SW-XXXX-XXXX-XXXX format or else it isnt accepted')
async def register(ctx):
        this_id = ctx.message.author.id
        this_fc = ctx.message.content.split('~register ',1)[-1]
        myDict = {}
        myDict[this_id]=this_fc

        '''if '3ds' in ctx.message.content:
            codes = db.3ds
        elif 'wiiu' in ctx.message.content:
            codes = db.wiiu
        else:
            codes = db.switch
            '''
       
        if re.search('[S][W]\W\d\d\d\d\W\d\d\d\d\W\d\d\d\d',this_fc):
            
            if codes.find({'discordId':this_id}).count() > 0:         
                codes.remove({'discordId':this_id,})
                codes.insert({'discordId':this_id, 'FC':this_fc})   
                return await bot.say(ctx.message.author.mention+', your friend code has been updated, thanks!')
                  
            else:
                codes.insert({'discordId':this_id, 'FC':this_fc})
                return await bot.say(ctx.message.author.mention+' you have been added!')
        else:
            return await bot.say('Sorry! I only accept friend codes!')



@bot.command(description='Sends the switch friend code for specific user ')
async def fc(user:discord.Member):
    if codes.find_one({"discordId" : user.id}):
        cur = codes.find({"discordId":user.id},{"_id":0,"FC":1 })
        for doc in cur:
            qResult = doc.values()
            ourFC = list(qResult)[0]
            return await bot.say('Their FC is '+str(ourFC))
    else:
        return await bot.say('You aren\'t in the database! Please look at `!help register`')




try:
    bot.run(botAuth)
except:
    print('[@] ERROR')
    sys.exit(-1)
