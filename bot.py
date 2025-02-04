from users import User_data
from dotenv import load_dotenv
import os

import pickle
import sys
import signal
import discord
import math
from discord import Embed
from discord.ext import commands
import asyncio
import humanfriendly
import random
from datetime import datetime,timedelta

load_dotenv()
Money_DATA_FILE = "UserMoney.pkl"
intents = discord.Intents.default()
intents.message_content = True  
bot = commands.Bot(command_prefix='.', intents=intents)

admin_ids = os.getenv("ADMIN_IDS", "").split(",")
Channel_ids = os.getenv("CHANNEL_IDS", "").split(",")
Approved = [int(id.strip()) for id in admin_ids if id.strip().isdigit()]
Channels = [int(id.strip()) for id in Channel_ids if id.strip().isdigit()]
def save_data(signal, frame):
    print("Ctrl+C detected, saving data...")
    with open(Money_DATA_FILE, 'wb') as f:
        pickle.dump(User, f)
    print("Data saved!")
    sys.exit(0)
 
def Bot_save():
    global User
    del User
    User = {}
    with open(Money_DATA_FILE, 'wb') as f:
        pickle.dump(User, f)

signal.signal(signal.SIGINT, save_data)

def load_data():
    try:
        with open(Money_DATA_FILE, 'rb') as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return {}

User = load_data()

def Check(User_id):
    if User_id not in User:
        User[User_id] = User_data(User_id)
    if User[User_id].Stars < 0 and User[User_id].Stars_in_bank + User[User_id].Stars >= 0: 
        User[User_id].Stars_in_bank += User[User_id].Stars
        User[User_id].Stars = 0
    elif User[User_id].Stars_in_bank < 0 and User[User_id].Stars_in_bank + User[User_id].Stars >= 0: 
        User[User_id].Stars += User[User_id].Stars_in_bank
        User[User_id].Stars_in_bank = 0
    return 

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

bot.remove_command("help")
@bot.command()
async def beg(ctx):
    if ctx.channel.id not in Channels:
        return
    User_id = ctx.author.id
    Check(User_id)
    Ob_user = User[User_id]

    current_datetime = datetime.now()

    time_dif = abs(current_datetime - Ob_user.last_beg)
    if time_dif < timedelta(minutes=10):
        await ctx.reply(f"Please wait {abs(10-math.ceil(time_dif.total_seconds()/60)+1)} minute(s) to beg again.")
        return
    Ob_user.last_beg = current_datetime
    Money_earned = random.randint(1,30)
    embed = Embed(
        title="YOU BEGGED!",
        description="", 
        color=0x00FF00             
        )
    embed.add_field(
        name = "", 
        value= f"You begged and got {Money_earned} ✨.",
        inline = False,
    )
    if random.random() <= 0.1:
        Sentences = ["Someone Kicked your cup over and stole a few stars, OH WAIT YOU ARE POOR YOU DON'T HAVE STARS.","Someone Screamed 'ew' and kicked you in the stomach","People felt disgusted by your torn clothes and farted in your face.","Someone posted you on social media and everyone stayed away from you."]
        embed = Embed(
            title="YOU FAILED IN BEGGING, LOSER!",
            description=f"{Sentences[random.randint(0,len(Sentences))]}", 
            color=0x8B0000             
            )
    else:
        User[User_id].Stars += Money_earned
    embed.set_thumbnail(url ="")
    await ctx.reply(embed=embed)
    
@bot.command()
async def remove(ctx,User_id):
    if ctx.author.id not in Approved:
        return
    try:
        User_id = int(User_id)
    except:
        User_id = int(User_id[2:-1])
    
    Check(User_id)
    del User[User_id]
    await ctx.reply(f"Deletion Successfull, Deleted <@{User_id}> from the data base")

@bot.command()
async def help(ctx):
    if ctx.channel.id not in Channels:
        return
    User_id = ctx.author.id
    Check(User_id)
    embed = Embed(
        title="Help.",
        color=0x800020 
    )
    embed.add_field(
        name= "```balance```",
        value ="- Shows the amount of stars in your wallet and bank.", 
        inline= False
    )
    embed.add_field(
        name = "```Beg```",
        value="- Beg like a peasent to gain some money",
        inline = False
    )
    embed.add_field(
        name= "```gamble```",
        value =f"- Randomly decides your chances of winning. If you win, you get 70% of your money in profit, but if you lose, you lose 100% of it.",
        inline= False
    )
    embed.add_field(
        name = "```coinflip```",
        value="- A fair coinflip, If you win, you get 50% more money, else you lose 50%",
        inline = False
    )
    embed.add_field(
        name = "```work```",
        value="- Do a small job and gain some money to get by.",
        inline = False
    )
    embed.add_field(
        name = "```pay```",
        value="- Transfer money from your wallet to someone else's wallet.",
        inline = False
    )
    embed.add_field(
        name = "```deposite```",
        value="- Transfer money from your wallet to your bank.",
        inline = False
    )
    embed.add_field(
        name = "```withdraw```",
        value="- Transfer money from your bank to your wallet.",
        inline = False
    )
    embed.add_field(
        name = "```Basics.```",
        value = "- .rob, .heist, the basics.",
        inline = False 
    )
    embed.set_image(url = "https://png.pngtree.com/thumb_back/fh260/background/20230408/pngtree-robot-white-cute-robot-blue-light-background-image_2199825.jpg")
    await ctx.reply(embed=embed)
@bot.command()
async def bal_other(ctx,User_Id : str):
    if ctx.channel.id not in Channels:
        return
    User_id = User_Id[2:-1]
    Check(User_id)
    embed = Embed(
        title="Balance",
        color=0xffd700 
    )
    embed.add_field(
        name="💰 Wallet", 
        value=f"`{User[User_id].Stars} ✨`", 
        inline=True
    )
    embed.add_field(
        name=":shield: Bank", 
        value=f"`{User[User_id].Stars_in_bank} ✨`", 
        inline=True
    )

    embed.set_thumbnail(url="https://png.pngtree.com/element_our/png/20181114/bank-icon-png_239804.jpg") 
    await ctx.reply(embed=embed)

@bot.command(aliases = ["bal","bala","balan","balanc"])
async def balance(ctx,Id = None):
    if ctx.channel.id not in Channels:
        return
    User_id = ctx.author.id
    
    if Id != None:
        try:
            User_id = int(Id)
        except:
            User_id = int(Id[2:-1])
    Check(User_id)
    embed = Embed(
        title="Balance",
        color=0xffd700 
    )
    embed.add_field(
        name="💰 Wallet", 
        value=f"`{math.floor(User[User_id].Stars)} ✨`", 
        inline=True
    )
    embed.add_field(
        name=":shield: Bank", 
        value=f"`{math.floor(User[User_id].Stars_in_bank)} ✨`", 
        inline=True
    )

    embed.set_thumbnail(url="https://png.pngtree.com/element_our/png/20181114/bank-icon-png_239804.jpg") 
    await ctx.reply(embed=embed)
@bot.command(aliases = ["res_all","resall","resetall","rac"])
async def reset_all(ctx):
    if ctx.author.id not in Approved:
        return
    Bot_save()

    await ctx.reply("Resetted All")



    
@bot.command()
async def heist(ctx,User_Id = None):
    if ctx.channel.id not in Channels:
        return
    
    User_id = ctx.author.id
    try:
        User_Id = int(User_Id)
    except:
        User_Id = int(User_Id[2:-1])
    
    Check(User_id)
    Check(User_Id)
    if User_Id == None:
        await ctx.reply("Tell me the person whose bank you wanna rob!")
        return
    if User_Id == User_id:
        await ctx.reply("Robbing yourself? BRUH!")
        return
    
    Ob_user = User[User_id]

    current_datetime = datetime.now()

    time_dif = abs(current_datetime - Ob_user.last_heist)
    if time_dif < timedelta(minutes=30):
        await ctx.reply(f"Please wait {abs(30-math.ceil(time_dif.total_seconds()/60))} minute(s) to heist someone's bank again.")
        return
    if User[User_id].Stars_in_bank <= 499:
        await ctx.reply("Bro, you need atleast 500 stars in your bank to rob someone else's bank.")
        return 
    Rob_Success = random.random()
    if User[User_Id].Stars_in_bank <= 499:
        await ctx.reply("Bro, they are already pretty poor, why are you even mugging them?")
        return

    Ob_user.last_heist = current_datetime
    while Rob_Success < 0.4 or Rob_Success > 0.6:
        Rob_Success = random.random()
    embed = None
    if random.random() < Rob_Success:
        Money_ = math.ceil(User[User_Id].Stars_in_bank * random.random())
        User[User_Id].Stars_in_bank -= Money_
        User[User_id].Stars_in_bank += Money_
        embed = Embed(
        title="Heist Successfull",
        color=0x008000 
        )
        embed = embed.add_field(
            name = "",
            value = f"Stole {Money_} ✨ from <@{User_Id}>.",
            inline= True 
        )
    else:
        Money_ = math.ceil(User[User_id].Stars_in_bank * random.random())
        if User[User_id].Stars_in_bank-Money_ < 0:
            User[User_Id].Stawrs_in_bank += User[User_id].Stars_in_bank
            User[User_id].Stars_in_bank = 0
        else: 
            User[User_Id].Stars_in_bank += Money_
            User[User_id].Stars_in_bank -= Money_
        embed = Embed(
        title="Heist Failed",
        color=0xFF0000 
        )
        
        embed = embed.add_field(
            name = "",
            value = f"Paid {Money_} ✨ to <@{User_Id}> as an apology.",
            inline= True 
        )
    
        embed.set_thumbnail(url="https://img.freepik.com/premium-vector/bank-robbery-icon-vector-image-can-be-used-banking_120816-82290.jpg?w=826")

    await ctx.reply(embed=embed)
@bot.command(aliases = ["Rob","ROb","ROB","Steal","steal"])
async def rob(ctx,User_Id = None):
    if ctx.channel.id not in Channels:
        return
    
    User_id = ctx.author.id
    try:
        User_Id = int(User_Id)
    except:
        User_Id = int(User_Id[2:-1])
    
    Check(User_id)
    Check(User_Id)
    if User_Id == None:
        await ctx.reply("Tell me the person you wanna rob!")
        return
    if User_Id == User_id:
        await ctx.reply("Robbing yourself? BRUH!")
        return
    
    Ob_user = User[User_id]

    current_datetime = datetime.now()

    time_dif = abs(current_datetime - Ob_user.last_rob)
    if time_dif < timedelta(minutes=10):
        await ctx.reply(f"Please wait {abs(10-math.ceil(time_dif.total_seconds()/60)+1)} minute(s) to rob someone again.")
        return
    if User[User_id].Stars <= 49:
        await ctx.reply("Bro, you need atleast 50 stars to rob someone else.")
        return 
    Rob_Success = random.random()
    if User[User_Id].Stars <= 50:
        await ctx.reply("Bro, they are already pretty poor, why are you even mugging them?")
        return

    Ob_user.last_rob = current_datetime
    while Rob_Success < 0.4 or Rob_Success > 0.6:
        Rob_Success = random.random()
    embed = None
    if random.random() < Rob_Success:
        Money_ = math.floor(User[User_Id].Stars * random.random())
        User[User_Id].Stars -= Money_
        User[User_id].Stars += Money_
        embed = Embed(
        title="Robbery Successfull",
        color=0x008000 
        )
        embed = embed.add_field(
            name = "",
            value = f"Stole {Money_} ✨ from <@{User_Id}>.",
            inline= True 
        )
        await ctx.reply(embed=embed)
    else:
        Money_ = math.floor(User[User_id].Stars * random.random())
    
        User[User_Id].Stars += Money_
        User[User_id].Stars -= Money_
        embed = Embed(
        title="Robbery Failed",
        color=0xFF0000 
        )
        embed = embed.add_field(
            name = "",
            value = f"Paid {Money_} ✨ to <@{User_Id}> as an apology.",
            inline= True 
        )
        await ctx.reply(embed=embed)

@bot.command(aliases = ["create"])
async def creator(ctx):
    if ctx.channel.id not in Channels:
        return
    User_id = ctx.author.id
    Check(User_id)
    await ctx.reply(f"<@830768330612408330> is my creator.")

@bot.command(aliases=["gam","gamb","gambl"])
async def gamble(ctx,Money_ = None):
    if ctx.channel.id not in Channels:
        return
    User_id = ctx.author.id
    Check(User_id)
    if Money_ == None:
        await ctx.reply("Specify how many stars do you want to gamble.")
        return
    if Money_.lower() == "half":
        Money_ = str(math.floor(User[User_id].Stars * (50/100)))
    elif Money_.lower() == "all" or Money_.lower() == "full":
        Money_ = str(User[User_id].Stars * (100/100))
    elif Money_[-1] == "%" and Money_[:-1].isdigit():
        Money_ = str(math.floor((int(Money_[:-1])/100) *  User[User_id].Stars))
    try: 
        Money_ = humanfriendly.parse_size(Money_)
    except:
        await ctx.reply("Please send a positive number, not characters or empty space(s).")
        return
    Money_ = math.floor(Money_)
    if User[User_id].Stars-Money_ < 0:
        await ctx.reply("You don't have enough stars!")
        return
    User[User_id].Stars -= Money_
    
    message = await ctx.reply("`Your chances of winning are ???`")
    await asyncio.sleep(0.1)
    x = 0
    while x < 10:
        x += 1
        await asyncio.sleep(0.5)
        await message.edit(content =  f"`Your chances of winning are {math.ceil(random.random()*100)}%`") 
    Win_prob = 0
    while Win_prob < 0.3 or Win_prob > 0.8:
        Win_prob = random.random()
    await message.edit(content = f"`Your chances of winning are {math.ceil(Win_prob*100)}%`")
    embed = Embed(
            title = "YOU LOST.",
            description=f"- {Money_*(100/100)} ✨",
            color = 0xFF0000
            )
    if random.random() <= Win_prob:
        embed = Embed(
        title="YOU WON!",
        description=f"+ {round(Money_*(70/100))} ✨", 
        color=0x00FF00             
        )
        User[User_id].Stars += math.floor(Money_*(70/100))
    else:
        User[User_id].Stars -= Money_
    User[User_id].Stars += Money_
    await ctx.reply(embed=embed)


@bot.command(aliases = ["coinflip","coin","coinf","coinfl","coinfli"])
async def cf(ctx,Money_ = None):
    if ctx.channel.id not in Channels:
        return

    User_id = ctx.author.id

    Check(User_id)
    if Money_ == None:
        await ctx.reply("Specify how many stars do you want bet on this coinflip?")
        return
    if Money_.lower() == "half":
        Money_ = str(User[User_id].Stars * (50/100))
    elif Money_.lower() == "all" or Money_.lower() == "full":
        Money_ = str(User[User_id].Stars * (100/100))
    elif Money_[-1] == "%" and Money_[:-1].isdigit():
        Money_ = str(math.floor((int(Money_[:-1])/100) *  User[User_id].Stars))
    try: 
        Money_ = humanfriendly.parse_size(Money_)
    except:
        await ctx.reply("Please send a positive number, not characters or empty space(s).")
        return
    

    if User[User_id].Stars-Money_ < 0:
        await ctx.reply("You don't have enough stars!")  
        return
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    Ls = [discord.utils.get(ctx.guild.emojis, name="CoinFlipTails"),discord.utils.get(ctx.guild.emojis, name="CoinFlipHeads")]

    await ctx.reply("Heads or Tails? (H/T)")

    try:
        msg = await bot.wait_for("message", check=check, timeout=30.0)
        if msg.content.upper() != "T" and msg.content.upper() != "H":
            await ctx.reply("Wrong Choice!")
            return
        Win = False
        Prob = random.random()
        User[User_id].Stars -= Money_
        if Prob <= 0.5:
            if msg.content.upper() == "T":
                Win = True
        else:
            if msg.content.upper() == "H":
                Win = True
        message = await ctx.reply(Ls[0])
        for i in range(1,10):
            await message.edit(content = f"{Ls[i%2]}")

        if Prob <= 0.5:
            await message.edit(content =Ls[0])
        else:
            await message.edit(content =Ls[1])
        
        embed = Embed(
        title="YOU WON!",
        description=f"+ {Money_*(50/100)} ✨", 
        color=0x00FF00             
        )

        if Win == False:

            embed = Embed(
                title = "YOU LOST.",
                description=f"- {Money_*(50/100)} ✨",
                color = 0xFF0000
                )
            User[User_id].Stars -= Money_*(50/100)
        
        else:
            User[User_id].Stars += Money_*(50/100)
        User[User_id].Stars += Money_
        
        await message.edit(embed=embed)
        
    except asyncio.TimeoutError:
        await ctx.reply("You took too long to respond!")

@bot.command(aliases=["wo","wor","earn"])
async def work(ctx):
    if ctx.channel.id not in Channels:
        return
    User_id = ctx.author.id
    Check(User_id)
    Ob_user = User[User_id]

    current_datetime = datetime.now()

    time_dif = abs(current_datetime - Ob_user.last_work)
    if time_dif < timedelta(minutes=10):
        await ctx.reply(f"Please wait {abs(10-math.ceil(time_dif.total_seconds()/60)+1)} minute(s) to work again.")
        return
    Ob_user.last_work = current_datetime
    Money_earned = random.randint(1,100)
    embed = Embed(
        title="YOU WORKED!",
        description="", 
        color=0x00FF00             
        )
    embed.add_field(
        name = "", 
        value= f"You earned {Money_earned} ✨.",
        inline = False,
    )
    User[User_id].Stars += Money_earned
    embed.set_thumbnail(url ="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQNWx5o6MTW4Xalq_oQIvmaHxISeep2adwFA&s")
    await ctx.reply(embed=embed)

@bot.command()
async def reset(ctx,Id = None):
    if ctx.channel.id not in Channels:
        return
    if ctx.author.id not in Approved:
        ctx.reply("Only the creator can run this command!")
        return
    User_id = ctx.author.id
    if Id != None:
        try:
            User_id = int(Id)
        except:
            User_id = int(Id[2:-1])
    Check(User_id)
    Ob_user = User[User_id]
    Ob_user.reset()
    await ctx.reply("Reset successfull")
@bot.command(aliases = ["lb","le","lea","lead","leade","leader","leaderb","leaderbo","leaderboa","leaderboar"])
async def leaderboard(ctx):
    if ctx.channel.id not in Channels:
        return
    embed = Embed(
        title = "Leader Board",
        description="The Top ten people",
        color = 0x900C3F 
    )

    People = []
    if len(User) <= 0 :
        await ctx.reply("I have no information on any user, Run a command to register your self.")
        return
    for Key,obj in User.items():
        People.append([Key,obj.Stars+obj.Stars_in_bank])

    People.sort(key = lambda x : x[1], reverse= True)
    for _ in People:
        embed.add_field(
            name = "",
            inline =  False,
            value = f"- <@{_[0]}> -> {round(_[1])} ✨"
        )
    embed.set_thumbnail(url= "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT9s9CEY9ZxsRA1wA4Y-09VSWInk7_5sGhIcQ&s")
    await ctx.reply(embed=embed)
    return
@bot.command(aliases = ["give","trans","transfer"])
async def pay(ctx,User_Id = None,Money_ = None):
    if ctx.channel.id not in Channels:
        return
    if User_Id == None:
        await ctx.reply("Bro, Please specify who should I pay to?")
        return
    if Money_ == None:
        await ctx.reply("Bro, How much should I pay them?")
        return
    User_id = ctx.author.id
    try:
        User_Id = int(User_Id)
    except:
        User_Id = int(User_Id[2:-1])
    Check(User_id)
    Check(User_Id)
    if User_Id == User_id:
        await ctx.reply("What are you gonna acheive by paying yourself?")
        return
    if Money_.lower() == "half":
        Money_ = str(round(User[User_id].Stars * 0.5))
    elif Money_.lower() == "all" or Money_.lower() == "full":
        Money_ = str(User[User_id].Stars)
    try: 
        Money_ = humanfriendly.parse_size(Money_)
    except:
        await ctx.reply("Please send a positive number, not characters or empty space(s).")
        return
    if Money_ == 0:
        embed = Embed(
            title="Seriously 0 ✨?",
            description= "Disappointment 😞",
            color=0xFF0000  
        )
        await ctx.reply(embed=embed)
        return
    if Money_ > User[User_id].Stars:
        embed = Embed(
        title="Transfer Failed!",
        description="You don't have enough stars in your wallet!", 
        color=0xFF0000             
        )
        await ctx.reply(embed=embed)
        return
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    await ctx.reply(f"Are you sure about transfering {Money_} ✨ to <@{User_Id}>? (Yes/No)")
    try:
        responses = ["YES","NO","N","YE","Y"]
        msg = await bot.wait_for("message", check=check, timeout=30.0)
        if msg.content.upper() not in responses:
            await ctx.reply("Wrong Choice!")
            return

    except asyncio.TimeoutError:
        await ctx.reply("You didn't respond quickly enough.")
        return
    Tax = 25/1000
    User[User_id].Stars -= Money_
    User[User_Id].Stars += Money_ - (Money_ * Tax)
    User[1307599260346220546] += (Money_ * Tax)
    embed = Embed(
        title="Transfer Successfull!",
        description=f"You transfered  {Money_ - (Money_ * Tax)} ✨ to <@{User_Id}>.", 
        color=0x00FF00             
        )
    embed.add_field(
        name="TAX",
        value="A 2.5% Tax has been applied to your transfer.",
        inline=False
    )
    await ctx.reply(embed=embed)
@bot.command(aliases=["Add","Add_","Add_M","Add_Mo"])
async def Add_Mon(ctx,Money_ = None,Id = None,B = None):
    if ctx.channel.id not in Channels:
        return
    User_id = ctx.author.id
    if User_id not in Approved:
        await ctx.reply("You are not approved to run this command!!!")
        return
    if Money_ == None:
        await ctx.reply("Please specify the amount of money you want to add.")
        return
    if Id != None:
        try:
            User_id = int(Id)
        except:
            User_id = int(Id[2:-1])
    Check(User_id)
    try: 
        Money_ = humanfriendly.parse_size(Money_)
    except:
        await ctx.reply("Please send a positive number, not characters or empty space(s).")
        return
    wal = "wallet"
    if B == None:
        User[User_id].Stars += Money_
    else:
        wal = "bank"
        User[User_id].Stars_in_bank += Money_
    await ctx.reply(f"Added {Money_} ✨ to <@{User_id}>'s {wal}.")
@bot.command(aliases=["with","wi","withd","withdr","withdra","get"])
async def withdraw(ctx,Money_ = None):
    if ctx.channel.id not in Channels:
        return
    User_id = ctx.author.id
    Check(User_id)
    if Money_ == None:
        await ctx.reply("Please enter the amount of money you wanna withdraw")
    if Money_.lower() == "half":
        Money_ = str(User[User_id].Stars_in_bank * (50/100))
    elif Money_.lower() == "all" or Money_.lower() == "full":
        Money_ = str(User[User_id].Stars_in_bank)
    elif Money_[-1] == "%" and Money_[:-1].isdigit():
        Percent = int(Money_[:-1])/100

        Money_ = str( math.floor(Percent *  User[User_id].Stars ))    
    try:
        Money_ = humanfriendly.parse_size(Money_)
    except:
        await ctx.reply("Please send a positive number, not characters or empty space(s).")
        return
    if User[User_id].Stars_in_bank-Money_ < 0:
        await ctx.reply("You are withdrawing more stars then you have in your bank!")
        return
    embed = Embed(
        title="Withdrawn!",
        description=f"{Money_} ✨", 
        color=0x355E3B
    )
    
    embed.add_field(
        name="💰 Wallet", 
        value=f"{math.floor(User[User_id].Stars+Money_)} ✨", 
        inline=True
    )
    embed.add_field(
        name=":shield: Bank", 
        value=f"{math.floor(User[User_id].Stars_in_bank-Money_)} ✨", 
        inline=True
    )
    User[User_id].Stars += Money_
    User[User_id].Stars_in_bank -= Money_ 
    embed.set_thumbnail(url="https://png.pngtree.com/element_our/png/20181114/bank-icon-png_239804.jpg") 
    await ctx.reply(embed=embed)

@bot.command(aliases=["dep","depo","depos","deposi","deposit","put"])
async def deposite(ctx,Money_:str = None):
    if ctx.channel.id not in Channels:
        return
    User_id = ctx.author.id
    Check(User_id)
    if Money_ == None:
        await ctx.reply("Please enter the amount of money you wanna deposite")
    if Money_.lower() == "half":
        Money_ = str(User[User_id].Stars * (50/100))
    elif Money_.lower() == "all" or Money_.lower() == "full":
        Money_ = str(User[User_id].Stars * (100/100))
    elif Money_[-1] == "%" and Money_[:-1].isdigit():
        Percent = int(Money_[:-1])/100

        Money_ = str( math.floor(Percent *  User[User_id].Stars ))

    try: 
        Money_ = humanfriendly.parse_size(Money_)
    except:
        await ctx.reply("Please send a positive number, not characters or empty space(s).")
        return
    
    if User[User_id].Stars-Money_ < 0:
        await ctx.reply("You are depositing more stars then you have in your wallet!")
        return 

    embed = Embed(
        title="Deposited!",
        description=f"{Money_} ✨", 
        color=0xffd700  
    )
    
    embed.add_field(
        name="💰 Wallet", 
        value=f"{math.floor(User[User_id].Stars-Money_)} ✨", 
        inline=True
    )
    embed.add_field(
        name=":shield: Bank", 
        value=f"{math.floor(User[User_id].Stars_in_bank+Money_)} ✨", 
        inline=True
    )
    
    User[User_id].Stars -= Money_
    User[User_id].Stars_in_bank += Money_ 

    embed.set_thumbnail(url="https://png.pngtree.com/element_our/png/20181114/bank-icon-png_239804.jpg") 
    
    await ctx.reply(embed=embed)
    



TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)



    
