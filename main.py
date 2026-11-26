import discord
import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv("token.env")
bot = discord.Bot(intents=discord.Intents.all())
token = os.getenv("TOKEN")
banlog = {}

# Command Part

@bot.slash_command(name ="presentation", description="Present who I am and what's my purpose")
async def presentation(ctx):
    embed = discord.Embed(title="This is my own presentation 🎤!", color=discord.Color.orange())
    embed.add_field(name="Who am I", value="I'm a simple ring, and a new discord bot made with ❤️") 
    embed.add_field(name="My purpose", value="To be fair with you, the goal of this bot is only improving my python. I found it very fun to make and really increase my skill, thank u HackClub! 🤖")
    embed.add_field(name="Who made it", value="My creator is a 15 (almost 16) y/o teenager in France, after switching language every 2 weeks: he found peace in python by learning complex notion with easy syntax!")
    embed.set_footer(text="If you are reading that, I hope you will pass a great day")
    await ctx.respond(embed=embed)

@bot.slash_command(name="ban_log", description="shows the log of banned people")
async def ban_log(ctx):
    await ctx.respond(banlog)


moderation = bot.create_group("moderation", "All commands to moderate your server")
@moderation.command(name="ban", description="Ban a member, THIS ACTION IS IMPORTANT")
@discord.option("member", discord.Member, description="The person who will be banned", required=True)
@discord.option("reason", str, description="Explain why you want to ban this user", default="No reason given")
@discord.default_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, reason: str):
    await ctx.respond(f"🔍 I'm trying to ban *{member}* with this id: `{member.id}`...")
    await member.ban(reason=reason)
    await ctx.respond(f"✅ All good, **{member}** is banned by *{ctx.author.name}*, because: {reason}")
    banlog[member.id] = {
        "name": str(member),
        "reason": reason,
        "moderator": str(ctx.author),
    }


@moderation.command(name="unban", description="Unban a member")
@discord.option("member_id", str, description="The id of the account that need to be UNBAN", required=True,)
@discord.option("reason", str, description="Why you want to UNBAN?", default="No reason given")
@discord.default_permissions(ban_members=True) 
async def unban(ctx, member_id: str, reason: str):
    try: 
        user = discord.Object(id=int(member_id))
        await ctx.respond("🔍 Searching the user to unban...")
        await ctx.guild.unban(user, reason=reason)
        await ctx.respond(f"✅ All good, <@{member_id}> is unban by *{ctx.author.name}*, because: {reason}")
    except ValueError:
        await ctx.respond("❌ This is not a valid ID, it must only contain numbers. You can find the id with /ban_log")
    except discord.NotFound:
        await ctx.respond("❌ This user is not banned.")

@moderation.command(name="kick", description="kick the member out of the server")
@discord.option("member", discord.Member, description="id of the member you want to kick", required=True)
@discord.option("reason", str, description="why you want to kick him?", default="No reason given")
@discord.default_permissions(kick_members=True)  
async def kick(ctx, member: discord.Member, reason: str):
    await ctx.respond(f"🔍 I'm trying to kick <@{member.id}>...")
    await member.kick(reason=reason)
    await ctx.respond(f"✅ All good, **{member}** has been kicked out by *{ctx.author.name}* because: *{reason}*")

@moderation.command(name="mute", description="mute someone in the chat")
@discord.option("member", discord.Member, description="choose the member you want to mute", required=True)
@discord.option("time", int, description="what will be the duration of the mute (IN MINUTES)", required=True)
@discord.option("reason", str, description="why do you want to mute this member", default="No reason given")
@discord.default_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, time: int, reason: str):
    await ctx.respond(f"🔍 I'm trying to mute <@{member.id}>...")
    await member.timeout_for(timedelta(minutes=time), reason=reason)
    await ctx.respond(f"✅ All good, <@{member.id}> has been muted by *{ctx.author.name}*, because: *{reason}*")

@moderation.command(name="unmute", description="unmute someone in the chat")
@discord.option("member", discord.Member, description="choose the number you want to unmute", required=True)
@discord.option("reason", str, description="why do you want to unmute this member", default="No reason given")
@discord.default_permissions(moderate_members=True)
async def unmute(ctx, member: discord.Member, reason: str):
    await ctx.respond(f"🔍 I'm trying to unmute <@{member.id}>...")
    await member.remove_timeout()
    await ctx.respond(f"✅ All good, <@{member.id}> has been unmuted by *{ctx.author.name}*, because: *{reason}*")

@moderation.command(name="delete", description="delete x number of messages the actual channel")
@discord.option("number", int, description="how many messages you want to delete")
@discord.default_permissions(manage_messages=True)
async def delete(ctx, number: int):
    await ctx.respond(f"🔍 I'm trying to clear this channel of {number} messages...")
    await ctx.channel.purge(limit=number+1)
    await ctx.respond(f"✅ All good, {number} messages has been deleted here <@{ctx.author.id}>", ephemeral=True)

info = bot.create_group("info", "All commands about finding info on everything")
@info.command(name="avatar", description="See the avatar of someone")
@discord.option("member", discord.Member, description="choose who you want to see the avatar, by default: YOU", required=False)
async def avatar(ctx, member: discord.Member):
    member = member or ctx.author
    embed = discord.Embed(color=member.color)
    embed.set_image(url=member.display_avatar.url)
    await ctx.respond(embed=embed)

@info.command(name="pong", description="Check the ping of the bot")
async def pong(ctx):
    ping = round(bot.latency * 1000)
    await ctx.respond(f"🧰 The ping is **{ping} ms**")

@info.command(name="server", description="Display some infos about the server you're in")
@discord.guild_only()
async def server(ctx):
    guild = ctx.guild
    bots = 0
    for i in guild.members:
        if i.bot == True:
            bots += 1
    humans = guild.member_count - bots
    embed = discord.Embed(title=f"Information about **{guild.name}** ", description=guild.description, color=discord.Color.blurple())
    owner: str
    if guild.owner:
        owner = guild.owner
    else:
        owner="Unknown"
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Created on", value=f"<t:{int(guild.created_at.timestamp())}:D>", inline=True) #I just learn that <t...:D> shows the date and time in the user own language format
    embed.add_field(name="ID", value=f"`{guild.id}`", inline=True)
    embed.add_field(name="Members", value=f"👨🏻‍🌾 Humans: {humans}, 🤖 Bots: {bots}")
    embed.add_field(name="Channels", value=f"💬 {len(guild.text_channels)} texts channel\n🔊 {len(guild.voice_channels)} voices channel", inline=True)

    if guild.icon :
        embed.set_thumbnail(url=guild.icon.url)
    await ctx.respond(embed=embed)

@info.command(name="user", description="Display some infos about a member")
@discord.option("member", discord.Member, description="Choose the source of the infos, by default YOU", required=False)
@discord.guild_only()
async def user(ctx, member: discord.Member):
    member = member or ctx.author
    roles = [role.mention for role in member.roles if role != ctx.guild.default_role]
    bot: str
    if member.bot:
        bot = "🤖 yes !"
    
    else:
        bot = "❌ No !"

    embed = discord.Embed(title=f"Infos about {member.display_name}", color=member.color)
    embed.add_field(name="ID", value=f"The value is {member.id}", inline=True)
    embed.add_field(name="Bot?", value=bot, inline=True)
    embed.add_field(name="Created", value=f"<t:{int(member.created_at.timestamp())}:D>", inline=False)
    embed.add_field(name="Join", value=f"<t:{int(member.joined_at.timestamp())}:D>", inline=True)
    embed.add_field(name="Highest role", value=member.top_role.mention, inline=True)
    embed.add_field(name=f"Roles ({len(roles)})", value=" ".join(roles)[:1024] if roles else "No roles", inline=False) #1024 is the maximum characters in an embed (thanks the doc haha)


    if member.timed_out:
        embed.add_field(name="Muted until...", value=f"<t:{int(member.communication_disabled_until.timestamp())}:R>", inline=False)
    embed.set_thumbnail(url=member.display_avatar.url)
    await ctx.respond(embed=embed)

class Vue(discord.ui.View):
    @discord.ui.button(label="Open a ticket", style=discord.ButtonStyle.orange, emoji="🧰")
    async def ticket(self, button, interaction):
        await 


# Event Part
#@bot.event

#async def on_member_join(member):
#    welcomeRoom = member.guild.system_channel
#    embed = discord.Embed(title="A plane just land 🛩️", description="You saw that, an embed !", color=discord.Color.blurple())
#    embed.add_field(value=f"Welcome here {member.mention}, here is some information about your invitation:...")
#    used = invite
#    embed.add_field(name="You come from", value=f"https://discord.gg/"+{discord.used.code}, inline=True)
#    embed.add_field(name="Link made by", value=f"{discord.used(inviter)}, thank you!", inline=True)
#    embed.add_field(name="That have ", value=f"{discord.used(uses)} invites on this server!", inline=True)
#
#   embed.set_thumbnail(url=member.display_avatar.url)
#    await welcomeRoom.send(embed=embed)

@bot.event
async def on_ready():
    ping = round(bot.latency * 1000)
    channel = bot.get_channel(1573272525234774126)
    await channel.send(f"I'm __*ready*__ and __*online*__ with a latence of **{ping} ms** ")

greetings = {"hi", "hii", "hai", "haii", "hello", "helloo", "hey", "heyy"}
how_are_you = {"how are you", "how are u", "how r u", "how u", "how r you"}
n_words = {"crap", "bloody", "arse", "ass", "shit", "bitch", "bastard", "piss", "bollocks", "fuck", "motherfucker", "cunt", "cock", "dick"}

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower().strip(" !?.,")
    if content in greetings:
        await message.reply(f"Hi {message.author.mention} 👋")
    elif content in how_are_you:
        await message.reply("I'm doing great, thanks for asking! And you?")
    elif content in n_words:
        await message.delete()
        await message.author.send("it seems like you sad a word that you shouldn't said, it's ok for this time but if you continue a moderator will punish you...")
        await message.reply("This is really bad what you are doing, please stop")




# The best part, RUNNING THE BOT !!!
bot.run(token)