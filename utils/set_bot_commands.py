from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустити бота"),
            types.BotCommand("help", "Показати команди"),
            types.BotCommand("main_menu", "Головне меню"),
            types.BotCommand("add_subjects", 'Додати предемети'),
            types.BotCommand("chose_subject", "Вибрати предмет"),
            types.BotCommand("test", "test command"),
            types.BotCommand('add_subjects', "Додати домашнє завдання")
        ]
    )
