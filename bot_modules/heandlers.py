from bot_modules.create_bot import dp
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.types import Message, ContentType
from bot_modules.keyboards import keyboard_start_game, keyboard_start_search, ReplyKeyboardRemove
from aiogram import F
import random as r
from bot_modules.classes import Player, Game, game_list
from bot_modules.save_data import list_users, save_users
# player1 = []
# player2 = []

queue = []  

def is_player_in_game(player_id: int):
    for game in game_list:
        if game.player1.chat_id == player_id or game.player2.chat_id == player_id:
            return True
    return False

def sort_raitings(item):
    return item[1]["raiting"]


random = [0,1]
@dp.message(CommandStart())
async def start(message: Message):
    if not is_player_in_game(message.chat.id):
        await message.answer("👋 Привіт,для того щоб почати гру,натисни на кнопку", reply_markup=keyboard_start_search)
@dp.message(F.content_type.is_(ContentType.TEXT))
async def text(message:Message):
    global queue

    if message.text == "🔎 Почати пошук суперника" and not is_player_in_game(message.chat.id):
        if str(message.from_user.id) not in list_users.keys():
            list_users[message.from_user.id] = {
                'wins': 0,
                'loses': 0,
                'ties': 0,
                'raiting': 1000
            }
            save_users()
        if queue == []:
            await message.answer("🔍 Вас додано в чергу, шукаємо суперника", reply_markup=ReplyKeyboardRemove())
            queue.append(message.chat.id)
        elif message.chat.id not in queue:
            hod = r.choice(random)
            await message.answer("🔍 Вас додано в чергу, шукаємо суперника", reply_markup=ReplyKeyboardRemove())
            player1 = queue[0]
            queue = []
            if hod == 0:
                player1_obj = Player(player1,None,"O")
                player2_obj = Player(message.chat.id, None, "X")
            else:
                player1_obj = Player(player1,None,"X")
                player2_obj = Player(message.chat.id, None,"O")
            
            game = Game(player1_obj, player2_obj)
            game_list.append(game)
            player1_info = list_users[str(player1_obj.chat_id)]
            player2_info = list_users[str(player2_obj.chat_id)]

            player1_count_games = player1_info['wins'] + player1_info['loses'] + player1_info['ties']
            player2_count_games = player2_info['wins'] + player2_info['loses'] + player2_info['ties']
            player1_info_text = [
                f"Рейтинг: {player1_info['raiting']}\n",
                f"Кілкість ігор: {player1_count_games}",
                f"Кількість перемог: {player1_info['wins']}",
                f"Кількість поразок: {player1_info['loses']}",
                f"Кількість нічиїх: {player1_info['ties']}",
            ]

            player2_info_text = [
            f"Рейтинг: {player2_info['raiting']}\n", 
            f"Кілкість ігор: {player2_count_games}",
            f"Кількість перемог: {player2_info['wins']}",
            f"Кількість поразок: {player2_info['loses']}",
            f"Кількість нічиїх: {player2_info['ties']}",
            ]
            player1_info_text = '\n'.join(player1_info_text)
            player2_info_text = '\n'.join(player2_info_text)

            if hod == 0:
                sent_message_player1 = await message.bot.send_message(player1, text=f"👾Гру розпочато, ваш опонент: {player2_obj.create_link()} (Bи граєте за нулик0️⃣)\n\n{player2_info_text}", 
                                                                      reply_markup=keyboard_start_game, parse_mode = ParseMode.HTML)
                sent_message_player2 =  await message.answer(f"🃏Гру розпочато, ваш опонент:{player1_obj.create_link()} (Bи граєте за хрестик✖)\n\n{player1_info_text}", 
                                                             reply_markup=keyboard_start_game, parse_mode = ParseMode.HTML)
            else:
                sent_message_player1 = await message.bot.send_message(player1, text=f"🃏Гру розпочато, ваш опонент: {player2_obj.create_link()} (Bи граєте за хрестик✖)\n\n{player2_info_text}", 
                                                                      reply_markup=keyboard_start_game, parse_mode = ParseMode.HTML)
                sent_message_player2 = await message.answer(f"👾Гру розпочато, ваш опонент: {player1_obj.create_link()} (Bи граєте за нулик0️⃣)\n\n{player1_info_text}", 
                                                            reply_markup=keyboard_start_game, parse_mode = ParseMode.HTML)
            player1_obj.message_id = sent_message_player1.message_id
            player2_obj.message_id = sent_message_player2.message_id
        
            
            print(game_list)
            
        else:
            await message.answer("Спробуйте пізніше", reply_markup=ReplyKeyboardRemove)
    if message.text == '🏆 Показати топ 3 гравця':
        new_dict = sorted(list(list_users.items()), key=sort_raitings,reverse=True)
        message_text = ['🏆 Топ 3 гравця:\n']
        rainting_place = 1
        rainting_emoji = {
            1: "🥇",
            2: "🥈",
            3: "🥉"
        }
        for i in new_dict[:3]:
            try:
                chat_with_user = await message.bot.get_chat(i[0])
                link = f'{rainting_emoji[rainting_place]} <a href="tg://user?id={i[0]}">{chat_with_user.first_name}</a>'
                message_text.append(f'{link}')
            except:
                pass
            rainting_place += 1
        await message.answer('\n\n'.join(message_text),parse_mode = ParseMode.HTML)