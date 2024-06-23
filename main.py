from bot_modules.create_bot import dp, bot
import asyncio
async def main():
    print('\n')
    await dp.start_polling(bot)
asyncio.run(main())

