from telebot import types
import utils


categories = [
    {'name': 'Презентации', 'folder_name': 'presentations'},
    {'name': 'Инфографика', 'folder_name': 'infographics'},
    {'name': 'Соцсети', 'folder_name': 'social_networks'},
    {'name': 'Таплинк', 'folder_name': 'taplink'},
    {'name': 'Иной дизайн', 'folder_name': 'others'}
]


def categories_keyboard():
    return utils.split_list([
            types.InlineKeyboardButton(
                text=item['name'],
                callback_data=item['folder_name']
            )
        for item in categories
    ])


def infographics_keyboard(): 
    return utils.split_list([
        types.InlineKeyboardButton(
            text='Для WB, карусель',
            callback_data='wb'
        ),
        types.InlineKeyboardButton(
            text='Для WB, обложка',
            callback_data='wbc'
        ),
        types.InlineKeyboardButton(
            text='Для озона',
            callback_data='ozon'
        )
    ])


def presentations_keyboard(): 
    return utils.split_list([
        types.InlineKeyboardButton(
            text='Полезное меню',
            callback_data='menu'
        ),
        types.InlineKeyboardButton(
            text='Промышленные краски',
            callback_data='colors'
        )
    ])


def sn_keyboard(): 
    return utils.split_list([
        types.InlineKeyboardButton(
            text='Магазин в Инсте',
            callback_data='in'
        ),
        types.InlineKeyboardButton(
            text='Сторис в Инсте',
            callback_data='in_s'
        ),
        types.InlineKeyboardButton(
            text='Сообщество VK',
            callback_data='vk'
        )
    ])


def back_to_menu_keyboard():
    return [[
        types.InlineKeyboardButton(
            text='Посмотреть ещё работы',
            callback_data='to_menu'
        )
    ]]


def order_keyboard(): 
    return [[
        types.InlineKeyboardButton(
            text='Заказать работу',
            callback_data='order'
        )
    ]]
