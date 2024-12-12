"""MADE BY ANANS1K"""

import disnake
import aiosqlite

from disnake.ext import commands

intents = disnake.Intents.all()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

def get_db():
    return aiosqlite.connect('punishment.db')

async def create_db():
    async with aiosqlite.connect('punishment.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS warnings (
                user_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                warnings_count INTEGER DEFAULT 0
            )
        ''')
        await db.commit()

async def add_warning(user_id: int, username: str):
    async with get_db() as db:
        async with db.execute("SELECT * FROM warnings WHERE user_id = ?", (user_id,)) as cursor:
            user = await cursor.fetchone()
        
        if user:
            await db.execute("UPDATE warnings SET warnings_count = warnings_count + 1 WHERE user_id = ?", (user_id,))
        else:
            await db.execute("INSERT INTO warnings (user_id, username, warnings_count) VALUES (?, ?, ?)", (user_id, username, 1))
        
        await db.commit()


async def get_warnings(user_id: int):
    async with get_db() as db:
        async with db.execute("SELECT warnings_count FROM warnings WHERE user_id = ?", (user_id,)) as cursor:
            user = await cursor.fetchone()
            if user:
                return user[0]
            else:
                return 0


async def reset_warnings(user_id: int):
    async with get_db() as db:
        await db.execute("UPDATE warnings SET warnings_count = 0 WHERE user_id = ?", (user_id,))
        await db.commit()


@bot.event
async def on_ready():
    print(f"The bot started as {bot.user}")
    await create_db()


@bot.command()
async def warn(ctx):
    member = ctx.author
    warnings_count = await get_warnings(member.id)
    embed = disnake.Embed(
        title='Варны',
        description=f'У тебе есть {warnings_count} варнов',
        color=disnake.Color.from_rgb(255,255,255)
    )
    await ctx.send(embed=embed)
    

@bot.slash_command(description='Выдать предупреждение пользователю')
@commands.has_permissions(moderate_members=True)
async def warn(ctx, member: disnake.Member, *, reason: str = "Не указано"):
    await add_warning(member.id, member.name)
    await ctx.send(f"{member.mention} получил предупреждение. Причина: {reason}")

@warn.error
async def warn_error(interaction, error):
    if isinstance(error, disnake.ext.commands.MissingRole):     
        embed = disnake.Embed(
            description=f'\n{interaction.author.mention}\n ** У вас нет прав для использования этой команды. ** \n >>> Если вы хотите получить эти права, попробуйте оставить заявку в наборе персонала.',
            color=disnake.Color.from_rgb(0, 0, 0)
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    elif isinstance(error, disnake.ext.commands.BadArgument):
        embed = disnake.Embed(
            description=f'\n{interaction.author.mention}\n ** Ошибка! ** \n >>> Пожалуйста, убедитесь, что вы ввели корректные значения для времени и причины.',
            color=disnake.Color.from_rgb(0, 0, 0)
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    elif isinstance(error, disnake.ext.commands.MissingPermissions):
        embed = disnake.Embed(
            description=f'\n{interaction.author.mention}\n ** У вас нет прав для использования этой команды. ** \n >>> Если вы хотите получить эти права, попробуйте оставить заявку в наборе персонала.',
            color=disnake.Color.from_rgb(0, 0, 0)
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    


@bot.slash_command(description='Посмотреть предупреждение пользователя')
async def warnings(ctx, member: disnake.Member):
    warnings_count = await get_warnings(member.id)
    await ctx.send(f"{member.mention} имеет {warnings_count} предупреждений.")


@bot.slash_command(description='Снять все предупреждение пользователя')
@commands.has_permissions(moderate_members=True)
async def clear_warnings(ctx, member: disnake.Member):
    await reset_warnings(member.id)
    await ctx.send(f"Все предупреждения для {member.mention} были сброшены.")
@clear_warnings.error
async def clear_warnings_error(interaction, error):
    if isinstance(error, disnake.ext.commands.MissingRole):     
        embed = disnake.Embed(
            description=f'\n{interaction.author.mention}\n ** У вас нет прав для использования этой команды. ** \n >>> Если вы хотите получить эти права, попробуйте оставить заявку в наборе персонала.',
            color=disnake.Color.from_rgb(0, 0, 0)
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    elif isinstance(error, disnake.ext.commands.BadArgument):
        embed = disnake.Embed(
            description=f'\n{interaction.author.mention}\n ** Ошибка! ** \n >>> Пожалуйста, убедитесь, что вы ввели корректные значения для времени и причины.',
            color=disnake.Color.from_rgb(0, 0, 0)
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    elif isinstance(error, disnake.ext.commands.MissingPermissions):
        embed = disnake.Embed(
            description=f'\n{interaction.author.mention}\n ** У вас нет прав для использования этой команды. ** \n >>> Если вы хотите получить эти права, попробуйте оставить заявку в наборе персонала.',
            color=disnake.Color.from_rgb(0, 0, 0)
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

bot.run("токен сюда вставь")