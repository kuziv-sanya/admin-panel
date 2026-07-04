import discord
from discord.ext import commands
import json
import os
from dotenv import load_dotenv

# =====================
# TOKEN
# =====================

load_dotenv()
TOKEN = os.getenv("TOKEN")

# =====================
# INTENTS
# =====================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =====================
# DATA
# =====================

if os.path.exists("warns.json"):
    with open("warns.json", "r") as f:
        warns = json.load(f)
else:
    warns = {}

def save_warns():
    with open("warns.json", "w") as f:
        json.dump(warns, f, indent=4)

# =====================
# READY
# =====================

@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Game(name="Moderation System")
    )
    print(f"Bot {bot.user} is online")

# =====================
# WARN
# =====================

@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason="без причины"):

    user_id = str(member.id)

    if user_id not in warns:
        warns[user_id] = 0

    warns[user_id] += 1
    save_warns()

    try:
        await member.send(
            f"⚠️ Вам выдан варн\n"
            f"Причина: {reason}\n"
            f"Всего варнов: {warns[user_id]}"
        )
    except:
        pass

    await ctx.send(f"⚠️ {member.mention} получил варн ({warns[user_id]})")

# =====================
# UNWARN
# =====================

@bot.command()
@commands.has_permissions(manage_messages=True)
async def unwarn(ctx, member: discord.Member, *, reason="не указана"):

    user_id = str(member.id)

    if user_id not in warns or warns[user_id] == 0:
        await ctx.send("У пользователя нет варнов")
        return

    warns[user_id] -= 1
    save_warns()

    await ctx.send(f"✅ У {member.mention} снят варн. Осталось: {warns[user_id]}")

# =====================
# WARS CHECK
# =====================

@bot.command()
async def warnings(ctx, member: discord.Member = None):

    member = member or ctx.author
    user_id = str(member.id)

    await ctx.send(f"⚠️ Варнов у {member.mention}: {warns.get(user_id, 0)}")

# =====================
# KICK
# =====================

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="не указана"):

    try:
        await member.kick(reason=reason)
        await ctx.send(f"👢 {member.mention} кикнут. Причина: {reason}")
    except discord.Forbidden:
        await ctx.send("❌ У меня нет прав на кик")

# =====================
# BAN
# =====================

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="не указана"):

    try:
        await member.ban(reason=reason)
        await ctx.send(f"🔨 {member.mention} забанен. Причина: {reason}")
    except discord.Forbidden:
        await ctx.send("❌ У меня нет прав на бан")

# =====================
# UNBAN
# =====================

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):

    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user)

    await ctx.send(f"✅ Пользователь разбанен")

# =====================
# CLEAR
# =====================

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):

    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 Удалено {amount} сообщений", delete_after=3)

# =====================
# RUN BOT
# =====================

bot.run(TOKEN)

    )

    embed.add_field(
        name="Ролей",
        value=len(guild.roles)
    )

    embed.add_field(
        name="Создан",
        value=guild.created_at.strftime("%d.%m.%Y")
    )

    await ctx.send(embed=embed)
