from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

#start
create_or_connect = ReplyKeyboardMarkup(
	keyboard=[
		[
			KeyboardButton(text="Створити групу")
		],
		[
			KeyboardButton(text="Підключитись до групи")
		]
	],
	resize_keyboard=True,
	one_time_keyboard=True
)

add_subjects = ReplyKeyboardMarkup(
	keyboard=[
		[
			KeyboardButton(text="Додати предмети")
		],
	],

	resize_keyboard=True,
	one_time_keyboard=True
)

ready_kb = ReplyKeyboardMarkup(
	keyboard=[
		[
			KeyboardButton(text="Готово")
		]
	],
	resize_keyboard=True,
	one_time_keyboard=True
)

#main menu
main_menu_or_add_subjects = ReplyKeyboardMarkup(
	keyboard=[
		[
			KeyboardButton(text="Додати предмети")
		],
		[
			KeyboardButton(text="Головне меню")
		]
	],

	resize_keyboard=True,
	one_time_keyboard=True
)

main_menu_ = ReplyKeyboardMarkup(
	keyboard=[
		[
			KeyboardButton(text="Головне меню"),
		]
	],
	resize_keyboard=True,
	one_time_keyboard=True
)

main_menu_action_button = ReplyKeyboardMarkup(
	keyboard=[
		[
			KeyboardButton(text="Додати домашнє"),
			KeyboardButton(text="Отримати домашнє")
		],
		[
			KeyboardButton(text="Отримати код групи"),
			KeyboardButton(text="Змінити групу")
		]

	],
	resize_keyboard=True,
	one_time_keyboard=True
)