from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

button_list = []
for i in range(9):
    empty_button = InlineKeyboardButton(text = ' ', callback_data = f'{i}')
    button_list.append(empty_button)
    
keyboard_start_game = InlineKeyboardMarkup(
    inline_keyboard =  [
                             [button_list[0],button_list[1],button_list[2]],
                             [button_list[3],button_list[4],button_list[5]],
                             [button_list[6],button_list[7],button_list[8]],
                             [InlineKeyboardButton(text = "Вихід 🏳", callback_data = "exit"  )]
                             ])


button_start_search = KeyboardButton(text="🔎 Почати пошук суперника")
button_top = KeyboardButton(text='🏆 Показати топ 3 гравця')
keyboard_start_search = ReplyKeyboardMarkup(keyboard=[[button_start_search], [button_top]], resize_keyboard=True)
