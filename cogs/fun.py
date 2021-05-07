from utils.constant_strings import EIGHT_BALL_DICT, GAY_DICT, HEART_LIST, PUSSY_DICT, SHIP_DICT, KISS_GIF_ARRAY
import discord, random
from discord.ext import commands
from discord import Embed
from datetime import datetime
from utils.clusters import CLUSTER_DICK, CLUSTER_GAY, CLUSTER_PUSSY, CLUSTER_SHIP

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def kiss(self, ctx, member: discord.Member = None):
        if member is None:
            return

        embed = discord.Embed(
            description=f"{ctx.message.author.mention} Kissed {member.mention}, How Sweet :heart:", 
            color=0xc81f9f,
            ).set_image(url=f"{random.choice(KISS_GIF_ARRAY)}"
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=["diceroll"])
    async def rolldice(self, ctx):
        """Roll some die"""

        embed= discord.Embed(
            description=f"You rolled a {random.randint(1, 6)}!", 
            timestamp=datetime.now()
            ).set_author(name=f"Dice Roll", 
            icon_url=f"https://www.freeiconspng.com/thumbs/dice-png/dice-png-transparent-images--png-all-4.png"
        )
        await ctx.send(embed=embed)


    @commands.command(aliases=["flipcoin", "fiftyfifty", "5050"])
    async def coinflip(self, ctx):
        """Flip a coin"""
        choices = ["heads", "tails"]

        embed= discord.Embed(
            description=(f"{random.choice(choices).capitalize()}!"), 
            timestamp=datetime.now()
            ).set_author(name=f"Coin Flip", 
            icon_url=f"https://www.pngarts.com/files/3/Silver-Coin-Transparent-Background-PNG.png"
        )
        await ctx.send(embed=embed)



    @commands.command()
    async def gayav(self, ctx, member : discord.Member = None):
        if member is None:
            member = ctx.author

        url = f'https://some-random-api.ml/canvas/gay?avatar={member.avatar_url}'
        if url.endswith(".webp?size=1024"):
            url = url[:-len(".webp?size=1024")]

        elif url.endswith(".gif?size=1024"):
            url = url[:-len(".gif?size=1024")]

        await ctx.send(embed=Embed(
            title=f"Gay Avatar for {member.display_name}", 
            timestamp=datetime.now(), url=url
        ).set_image(url=url))

    @commands.command(aliases=["simp"])
    async def ship(self, ctx, member : discord.Member = None, member2 : discord.Member = None):
        if member is None or member2 is None:
            return

        members = [member.id, member2.id]
        members.sort()

        _find_user = CLUSTER_SHIP.find_one({"member_one" : members[0], "member_two": members[1]})

        if _find_user is None:
            shipnumber = random.randint(0,100)
            new_ship = ({"member_one" : members[0], "member_two": members[1], "rating": shipnumber})
            CLUSTER_SHIP.insert(new_ship)

            _find_user = CLUSTER_SHIP.find_one({"member_one" : members[0], "member_two": members[1]})

        shipnumber = _find_user["rating"]
        
        if 0 <= shipnumber <= 10: 
            choice = random.choice(SHIP_DICT["SHIP_REALLY_LOW"])
            status = f"Really low! {choice}"

        elif 10 < shipnumber <= 20:
            choice = random.choice(SHIP_DICT["SHIP_LOW"])
            status = f"Low! {choice}"
            
        elif 20 < shipnumber <= 30:
            choice = random.choice(SHIP_DICT["SHIP_POOR"])
            status = f"Poor! {choice}"

        elif 30 < shipnumber <= 40:
            choice = random.choice(SHIP_DICT["SHIP_FAIR"])
            status = f"Fair! {choice}"

        elif 40 < shipnumber <= 60:
            choice = random.choice(SHIP_DICT["SHIP_MODERATE"])
            status = f"Moderate! {choice}"

        elif 60 < shipnumber <= 70:
            choice = random.choice(SHIP_DICT["SHIP_GOOD"])
            status = f"Good! {choice}"

        elif 70 < shipnumber <= 80:
            choice = random.choice(SHIP_DICT["SHIP_GREAT"])
            status = f"Great! {choice}"

        elif 80 < shipnumber <= 90:
            choice = random.choice(SHIP_DICT["SHIP_OVERAVERAGE"])
            status = f"Over Average! {choice}"
        elif 90 < shipnumber <= 100:
            choice = random.choice(SHIP_DICT["SHIP_TRUELOVE"])
            status = f"True Love! {choice}"

        if shipnumber <= 33:
            colour = 0xE80303

        elif 33 < shipnumber < 66:
            colour = 0xff6600

        else:
            colour = 0x3be801

        embed = (discord.Embed(
            color=colour,
            title="Simp rate for:",
            description=f"**{member}** and **{member2}** {random.choice(HEART_LIST)}")
            ).add_field(name="Results:", value=f"{shipnumber}%", inline=True
            ).add_field(name="Status:", value=(status), inline=False
            ).set_author(name="Shipping", icon_url="http://moziru.com/images/kopel-clipart-heart-6.png")

        await ctx.send(embed=embed)
    
    @commands.command(aliases=['8ball'])
    async def eightball(self, ctx, *, _ballInput):
        """extra generic just the way you like it"""
        choice = random.randint(1,3)
        if choice == 1:
            prediction = random.choice(EIGHT_BALL_DICT["EIGHT_BALL_AFFIRMATIVE"])
            colour=0x3be801

        elif choice == 2:
            prediction = random.choice(EIGHT_BALL_DICT["EIGHT_BALL_UNSURE"])
            colour=0xff6600
        elif choice == 3:
            prediction = random.choice(EIGHT_BALL_DICT["EIGHTEIGHT_BALL_NEGATIVE"])
            colour=0xE80303
        
            
        embed = discord.Embed(
            title=f"Question: {_ballInput}", 
            description=f"{prediction} :8ball:",
            colour=colour
            ).set_author(name='Magic 8 ball', icon_url='https://www.horoscope.com/images-US/games/game-magic-8-ball-no-text.png'
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=['gay-scanner', 'gayscanner', 'gay'])
    async def gay_scanner(self, ctx, member : discord.Member=None):
        if member == None:
            member = ctx.author

        _find_user = CLUSTER_GAY.find_one({"id" : member.id})

        if _find_user is None:
            gayness = random.randint(0,100)
            new_gay_client = ({"id": member.id, "gay_rating": gayness})
            CLUSTER_GAY.insert(new_gay_client)
            _find_user = CLUSTER_GAY.find_one({"id" : member.id})

        gayness = _find_user["gay_rating"]
        
        if gayness <= 10:
            gayStatus = random.choice(GAY_DICT["GAY_1"])
            colour = 0xFFFFFF

        elif 10 < gayness < 33:
            gayStatus = random.choice(GAY_DICT["GAY_2"])
            colour = 0xFFC0CB

        elif 33 < gayness < 66:
            gayStatus = random.choice(GAY_DICT["GAY_3"])
            colour = 0xFF69B4

        else:
            gayStatus = random.choice(GAY_DICT["GAY_4"])
            colour = 0xFF00FF

        embed = discord.Embed(
            description=f"Gayness for **{member }**", 
            color=colour
            ).add_field(name="Gayness:", value=f"{gayness}% gay"
            ).add_field(name="Comment:", value=f"{gayStatus} :kiss_mm:"
            ).set_author(name="Gay-Scanner™", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/ICA_flag.svg/2000px-ICA_flag.svg.png"
        )

        await ctx.send(embed=embed)

    @commands.command(aliases=['pussy'])
    async def pussy_size(self, ctx, member : discord.Member=None):
        if member == None:
            member = ctx.author


        _find_user = CLUSTER_PUSSY.find_one({"id" : member.id})

        if _find_user is None:
            size = random.randint(0,100)
            new_pussy = ({"id": member.id, "pussy_size": size})
            CLUSTER_PUSSY.insert(new_pussy)
            _find_user = CLUSTER_PUSSY.find_one({"id" : member.id})

        size = _find_user["pussy_size"]

        colour = 0xFFFFFF
        if size <= 20:
            status = random.choice(PUSSY_DICT["PUSSY_SIZE_SMALL"])
        elif 20 < size < 50:
            status = random.choice(PUSSY_DICT["PUSSY_SIZE_MEDIUM"])
            colour = 0xFFC0CB

        elif 50 < size < 66:
            status = random.choice(PUSSY_DICT["PUSSY_SIZE_SMALL"])
            colour = 0xFF69B4
        else:
            status = random.choice(PUSSY_DICT["PUSSY_SIZE_BUCKET"])
            colour = 0xFF00FF

        embed = discord.Embed(
            description=f"Pussy Size for **{member }**", 
            color=colour
            ).add_field(name="Pussy Size:", value=f"{status}"
            ).set_author(name="Pussy-Scanner™", icon_url="https://assets.stickpng.com/images/580b585b2edbce24c47b2792.png"
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def dick(self, ctx, member : discord.Member=None):
        if member == None:
            member = ctx.author

        _find_user = CLUSTER_DICK.find_one({"id" : member.id})

        if _find_user is None:
            dick_size = f"8{'='*random.randint(1,12)}3"
            new_dick_size = ({"id": member.id, "dick_size": dick_size})
            CLUSTER_DICK.insert(new_dick_size)
            _find_user = CLUSTER_DICK.find_one({"id" : member.id})

        dick_size = _find_user["dick_size"]
        gayColor = 0xFFFFFF

        emb = discord.Embed(description=f"Dick size for **{member }**", color=gayColor)
        emb.add_field(name="Dick Size:", value=f"{dick_size}\n{len(dick_size)-1} Inches")
        emb.set_author(name="Dick-Detector™", icon_url="https://static.thenounproject.com/png/113312-200.png")
        await ctx.send(embed=emb)

def setup(client):
    client.add_cog(Fun(client))