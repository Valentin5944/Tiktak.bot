from aiogram.types import CallbackQuery,Message 
from bot_modules.keyboards import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from bot_modules.save_data import save_users,list_users


game_list = []

win_shema = [
    [0,1,2],
    [3,4,5],
    [6,7,8],
    [0,3,6],
    [1,4,7],
    [2,5,8],
    [0,4,8],
    [2,4,6]
]

class Player:
    def __init__(self, chat_id: int, message_id: int, shape: int, username : str = ''):
        self.chat_id = chat_id
        self.message_id = message_id
        self.shape = shape
        self.username = username
    def create_link(self):
        return f'<a href="tg://user?id={self.chat_id}">опонент</a>'


class Game:
    def __init__(self, player1:Player, player2:Player):
        self.player1 = player1
        self.player2 = player2
        self.save_steps_list = [0,0,0,0,0,0,0,0,0]
        self.game_end = False
        self.success_step = False
        

    async def step(self, callback: CallbackQuery):
        start_count_empty_cells = self.save_steps_list.count(0)
        if self.save_steps_list[int(callback.data)] == 0:
            # print(callback.message.from_user)

            if callback.message.chat.id == self.player1.chat_id and callback.message.message_id == self.player1.message_id :
                if self.player1.username == "":
                    self.player1.username = callback.from_user.first_name
                    
                if self.player1.shape == 'X':
                    if self.save_steps_list.count(1) == self.save_steps_list.count(2):
                        self.save_steps_list[int(callback.data)] = 1
                else:
                    if self.save_steps_list.count(1) > self.save_steps_list.count(2):
                        self.save_steps_list[int(callback.data)] = 2
            elif callback.message.chat.id == self.player2.chat_id and callback.message.message_id == self.player2.message_id:
                if self.player2.username == "":
                    self.player2.username = callback.from_user.first_name
                if self.player2.shape == 'X':
                    if self.save_steps_list.count(1) == self.save_steps_list.count(2):
                        self.save_steps_list[int(callback.data)] = 1
                else:
                    if self.save_steps_list.count(1) > self.save_steps_list.count(2):
                        self.save_steps_list[int(callback.data)] = 2
            print(start_count_empty_cells > self.save_steps_list.count(0))
            if start_count_empty_cells > self.save_steps_list.count(0):
                self.success_step = True
            await self.check_win(callback)
        await asyncio.sleep(0.1)

    async def check_win(self, callback: CallbackQuery):
        for shema in win_shema: 
            if self.save_steps_list[shema[0]] == self.save_steps_list[shema[1]] and self.save_steps_list[shema[1]] == self.save_steps_list[shema[2]]:
                print(123)
                if self.save_steps_list[shema[0]] != 0:
                    print(321)
                    if self.save_steps_list[shema[0]] == 1:
                        print(444)
                        print("win cross")
                        if self.player1.shape == 'X':
                            list_users[str(self.player1.chat_id)]["wins"] += 1
                            list_users[str(self.player1.chat_id)]["raiting"] += 50
                            list_users[str(self.player2.chat_id)]["loses"] -= 1
                            list_users[str(self.player2.chat_id)]["raiting"] -= 50
                            await callback.message.bot.send_message(self.player1.chat_id, f'🥇 Ви перемогли!')
                            await callback.message.bot.send_message(self.player2.chat_id , f"Виграв {self.player1.username}")
                        else:
                            list_users[str(self.player2.chat_id)]["wins"] += 1
                            list_users[str(self.player2.chat_id)]["raiting"] += 50
                            list_users[str(self.player1.chat_id)]["loses"] -= 1
                            list_users[str(self.player1.chat_id)]["raiting"] -= 50

                            await callback.message.bot.send_message(self.player2.chat_id, f'🥇 Ви перемогли!')
                            await callback.message.bot.send_message(self.player1.chat_id, f'Виграв {self.player2.username}')

                    elif self.save_steps_list[shema[0]] == 2:
                        print("win zero")
                        if self.player1.shape == 'O':
                            list_users[str(self.player1.chat_id)]["wins"] += 1
                            list_users[str(self.player1.chat_id)]["raiting"] += 50
                            list_users[str(self.player2.chat_id)]["loses"] += 1
                            list_users[str(self.player2.chat_id)]["raiting"] -= 50
                            save_users()
                            await callback.message.bot.send_message(self.player1.chat_id, f'🥇 Ви перемогли!')
                            await callback.message.bot.send_message(self.player2.chat_id , f"Виграв {self.player1.username}")
                        else:
                            list_users[str(self.player2.chat_id)]["wins"] += 1
                            list_users[str(self.player2.chat_id)]["raiting"] += 50
                            list_users[str(self.player1.chat_id)]["loses"] += 1
                            list_users[str(self.player1.chat_id)]["raiting"] -= 50
                            save_users()
                            await callback.message.bot.send_message(self.player2.chat_id, f'🥇 Ви перемогли!')
                            await callback.message.bot.send_message(self.player1.chat_id, f'Виграв {self.player2.username}')
                    self.game_end = True
                    game_list.remove(self)
        if self.game_end == False:
            if self.save_steps_list.count(0) == 0:
                self.game_end = True
                list_users[str(self.player2.chat_id)]["ties"] += 1
                list_users[str(self.player1.chat_id)]["ties"] += 1
                save_users()
                await callback.message.bot.send_message(self.player1.chat_id,'🤝 Гра завершилися нічією')
                await callback.message.bot.send_message(self.player2.chat_id,'🤝 Гра завершилися нічією')
                game_list.remove(self)
        await self.update_keyboard(callback)
                        
    async def update_keyboard(self, callback:CallbackQuery):
        button_list = []
        
        if self.game_end:
            for i in range(9):
                if self.save_steps_list[i] == 0:
                    empty_button = InlineKeyboardButton(text = ' ', callback_data = f'end')
                elif self.save_steps_list[i] == 1:
                    empty_button = InlineKeyboardButton(text = 'X', callback_data = f'end')
                elif self.save_steps_list[i] == 2:
                    empty_button = InlineKeyboardButton(text = 'O', callback_data = f'end')
                button_list.append(empty_button)
        else:
            for i in range(9):
                if self.save_steps_list[i] == 0:
                    empty_button = InlineKeyboardButton(text = ' ', callback_data = f'{i}')
                elif self.save_steps_list[i] == 1:
                    empty_button = InlineKeyboardButton(text = 'X', callback_data = f'{i}')
                elif self.save_steps_list[i] == 2:
                    empty_button = InlineKeyboardButton(text = 'O', callback_data = f'{i}')
                button_list.append(empty_button)

        update_keyboard = InlineKeyboardMarkup(
        inline_keyboard =  [
                                [button_list[0],button_list[1],button_list[2]],
                                [button_list[3],button_list[4],button_list[5]],
                                [button_list[6],button_list[7],button_list[8]],
                                [InlineKeyboardButton(text = "Вихід 🏳", callback_data = "exit"  )]
                                ])
        if self.success_step:
            await callback.message.bot.edit_message_reply_markup(chat_id=self.player1.chat_id, message_id=self.player1.message_id,reply_markup=update_keyboard)
            await callback.message.bot.edit_message_reply_markup(chat_id=self.player2.chat_id, message_id=self.player2.message_id,reply_markup=update_keyboard)
        else:
            await callback.answer('‼️ Дочекайтесь вашого ходу')
        self.success_step = False