import os
import asyncio
import discord
from discord.ext import commands
from keys import tourist_token

print("discord.py version:", discord.__version__)
intents = discord.Intents.all()
bot = commands.Bot(command_prefix = "%", intents = intents)


def get_act():
    pen = open("status.txt", 'r', encoding="UTF-8")
    game = pen.readline()
    pen.close()
    return game


@bot.event
async def on_ready():
    slash = await bot.tree.sync()
    print(f"目前登入身份 --> {bot.user}")
    print(f"載入 {len(slash)} 個斜線指令")
    game = get_act()
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(game))
    print(f"正在玩 {game}")


# @bot.command()
# async def load(ctx, extension):
#     print("loaddd")
#     await bot.load_extension(f"cogs.{extension}")
#     await ctx.send(f"Loaded {extension} done.")
#
#
# @bot.command()
# async def unload(ctx, extension):
#     await bot.unload_extension(f"cogs.{extension}")
#     await ctx.send(f"UnLoaded {extension} done.")
#
#
# @bot.command()
# async def reload(ctx, extension):
#     await bot.reload_extension(f"cogs.{extension}")
#     await ctx.send(f"ReLoaded {extension} done.")


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with bot:
        await load_extensions()
        await bot.start(tourist_token)


if __name__ == "__main__":
    asyncio.run(main())