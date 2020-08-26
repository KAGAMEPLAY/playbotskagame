import discord
from discord import utils
from discord.ext import commands
from discord.ext.commands import Bot
from discord import Activity, ActivityType
from discord import Guild
import config

Bot = commands.Bot(command_prefix="-")

@Bot.event
async def on_ready():
    print('Бот сервера включен!')
    memberCount = len(set(Bot.get_all_members()))
    await Bot.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = f"за {memberCount} пользователями!"))

@Bot.command()
async def say(ctx,arg):    
	await ctx.send(arg)

@Bot.command()
async def userinfo(ctx,member:discord.Member):
    await ctx.message.delete()

    if not member in ctx.guild.members:
       return await ctx.send(f'{ctx.author.mention}, нет такого пользователя!')
    
    if member.bot == True:
        return await ctx.send(f'{ctx.author.mention}, у девочки(бота) нет имени 🤖')
    status = {
        "val": "",
    }
    if str(member.status) == 'online':
        status['val'] = '🟩 В сети'
    if str(member.status) == 'idle':
        status['val'] = '🟨 Спит'
    if str(member.status) == 'dnd':
        status['val'] = '🟥 Не беспокоить'
    if str(member.status) == 'offline':
        status['val'] = '⬛ Не в сети'
    
    roles = ''
    for role in member.roles:
        if str(role.name) != '@everyone':
            roles += f'<@&{role.id}> | '

    emb = discord.Embed(title='Профиль',color=0xff0000)
    emb.set_thumbnail(url=member.avatar_url)
    emb.add_field(name='Имя: ',value=f'<@{member.id}>', inline=False)
    emb.add_field(name='ID: ',value=member.id, inline=False)
    emb.add_field(name='Аккаунт создан: ',value=member.created_at.strftime("%d.%m.%Y | %H:%M:%S"), inline=False)
    emb.add_field(name='Присоединился: ',value=member.joined_at.strftime("%d.%m.%Y | %H:%M:%S"), inline=False)
    emb.add_field(name='Статус: ',value=status['val'], inline=False)
    emb.add_field(name='Роль: ',value=roles, inline=False)
    emb.set_footer(text=f"Отправитель: {ctx.message.author}",icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed = emb)

@Bot.event
async def on_member_join(member):
    try:
        channel = Bot.get_channel(406098834586992650)     
        role = member.guild.get_role(408268005928075266)
        await member.add_roles(role)
        await channel.send(f"<@{member.id}> Добро пожаловать на сервер!")
    except Exception as e:
        print(e)

@Bot.event
async def on_member_remove(member):
    channel = Bot.get_channel(406098834586992650)
    await channel.send(f"<@{member.id}> Покинул нас!")

@Bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    guild_age = (ctx.message.created_at - guild.created_at).days
    created_at = f"{guild.created_at.strftime('%d.%m.%Y в %H:%M')}. Это {guild_age} дней назад!"
    totalmembers = ctx.guild.members
    channels = ctx.guild.channels
    textchannels = ctx.guild.text_channels
    voicechannels = ctx.guild.voice_channels
    roletotal = ctx.guild.roles
    
    role = discord.utils.get(ctx.guild.roles,id = 285731552061685760)
    embedserverinfo = discord.Embed(
    title=ctx.guild.name,color =role.color)
    embedserverinfo.set_thumbnail(url=ctx.guild.icon_url)
    embedserverinfo.add_field(name="Айди сервера:", value=guild.id, inline=True)
    embedserverinfo.add_field(name="Создатель сервера:", value=guild.owner.mention, inline=True)
    embedserverinfo.add_field(name="Количество участников:", value=f'{len(totalmembers)}', inline=False)
    embedserverinfo.add_field(name="В сети:", value=len({m.id for m in guild.members if m.status is not discord.Status.offline}))
    embedserverinfo.add_field(name="Каналы:", value=f'{len(channels)} [{len(textchannels)} Текстовых | {len(voicechannels)} Голосовых] ', inline=False)
    embedserverinfo.add_field(name="Количество ролей", value=f'{len(roletotal)}', inline=False)
    embedserverinfo.add_field(name="Регион сервера", value=guild.region, inline=False)
    embedserverinfo.add_field(name="Сервер был создан:", value=created_at, inline=False)
    embedserverinfo.set_footer(text='Создатель бота - KAGAME')
    await ctx.send(embed = embedserverinfo)

@Bot.command()
async def embrole(ctx):
    e = discord.Embed(title=f'Роли дискорд канала {ctx.guild.name}', color=0xfbc531)
    e.add_field(name ='Список ролей которую можна получить:', value = "<:4sB:747574700401754133> - <@&329334829009338391>\n<:pod:747601216120291328> - <@&317604087375986688>\n<:rust:747601336907989083> - <@&288624844734726144>\n<:minecraft:747601368373788713> - <@&326408629316091906>\n<:dota:747601424766205963> - <@&293708733119201281>\n<:gta:747607289804095488> - <@&290224043691474944>\n<:cs:747607260368470047> - <@&288678369862877184>\n<:wot:747607219348176959> - <@&401025074259427338>\n<:rpg:747601269945925690> - <@&747523060902395955>\n<:pubg:747607172153868308> - <@&747592278142353580>\n<:fortnite:747607097318965288> - <@&747592368584130662>\n<:gust:747601301872967760> - <@&408268005928075266>\n**Это даст Вам возможность получать уведомления о новостях!**")
    e.set_image(url='https://resources.bastionbot.org/og/42a7fd2efc8a0ff6b6eb97f601ee8b73.jpg')
    e.set_footer(text='Эмоджи снизу могут не отображаться из-за ошибки дискорд.\nВ таком случае перезагрузите дискорд сочетанием клавиш CTRL+R')
    await ctx.send(embed=e)
 
import discord
from discord import utils
import config

@Bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == config.POST_ID:
        channel = Bot.get_channel(payload.channel_id)   # получаем объект канала
        message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
        member = utils.get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию
 
        try:
            emoji = str(payload.emoji) # эмоджик который выбрал юзер
            role = utils.get(message.guild.roles, id=config.ROLES[emoji]) # объект выбранной роли (если есть)
            
            if(len([i for i in member.roles if i.id not in config.EXCROLES]) <= config.MAX_ROLES_PER_USER):
                await member.add_roles(role)
                print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))
            else:
                await message.remove_reaction(payload.emoji, member)
                print('[ERROR] Too many roles for user {0.display_name}'.format(member))
            
        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))

@Bot.event
async def on_raw_reaction_remove(payload):
    channel = Bot.get_channel(payload.channel_id) # получаем объект канала
    message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
    member = utils.get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию
 
    try:
        emoji = str(payload.emoji) # эмоджик который выбрал юзер
        role = utils.get(message.guild.roles, id=config.ROLES[emoji]) # объект выбранной роли (если есть)
 
        await member.remove_roles(role)
        print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))
 
    except KeyError as e:
        print('[ERROR] KeyError, no role found for ' + emoji)
    except Exception as e:
        print(repr(e))
 
# RUN
#Bot = MyClient()
Bot.run(config.TOKEN)











