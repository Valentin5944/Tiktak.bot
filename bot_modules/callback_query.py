from aiogram.types import CallbackQuery,Message 
from bot_modules.create_bot import dp
from bot_modules.keyboards import InlineKeyboardMarkup, InlineKeyboardButton
# from bot_modules.heandlers import player1, player2
from bot_modules.heandlers import game_list
from bot_modules.save_data import save_users,list_users

@dp.callback_query()
async def choise(callback: CallbackQuery):             
    current_game = None
    if callback.data != 'end' and callback.data != 'exit':
        current_game = False
        for game in game_list:
            if callback.message.chat.id == game.player1.chat_id or callback.message.chat.id == game.player2.chat_id:
                current_game = game
                break
        if current_game:
            await current_game.step(callback)
    elif callback.data == "exit":
        for game in game_list:
            if callback.message.chat.id == game.player1.chat_id or callback.message.chat.id == game.player2.chat_id:
                current_game = game
                break
        if current_game:
            list_users[str(current_game.player1.chat_id)]['ties'] += 1
            list_users[str(current_game.player2.chat_id)]['ties'] += 1
            list_users[str(current_game.player1.chat_id)]['raiting'] -= 10
            list_users[str(current_game.player2.chat_id)]['raiting'] -= 10
            save_users()
            if callback.from_user.id ==  current_game.player1.chat_id:
                await callback.message.bot.send_message(current_game.player1.chat_id,'Ты с позором убежал')
                await callback.message.bot.send_message(current_game.player2.chat_id,'Ваш соперник с позором убежал')
            elif callback.from_user.id == current_game.player2.chat_id:
                await callback.message.bot.send_message(current_game.player1.chat_id,'Ваш соперник с позором убежал')
                await callback.message.bot.send_message(current_game.player2.chat_id,'Ты с позором убежал')
            game_list.remove(current_game)

            