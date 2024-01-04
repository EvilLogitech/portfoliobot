#!/usr/bin/python
from telebot import types, TeleBot
import os
from dotenv import load_dotenv
from db_utils import get_file_id, add_file_id
import utils
import keyboards
import time


load_dotenv()
admin_id = os.environ.get('admin_id', '')
owner_id = os.environ.get('owner_id', '')
token = os.environ.get('token')
bot = TeleBot(token)

text_messages = {
    'error_no_files': 'Простите, что-то пошло не так. '\
        'Попробуйте позже, когда всё восстановится',
    'greetings': 'Здраствуйте, {}, я бот-помощник Марии, графического дизайнера.\n'\
        'Вы можете заказать создание оформления социальных сетей, '\
        'таплинк, инфографику для маркетплейсов, презентации.',
    'no_command': 'Простите, я не знаю такой команды.\nЧто вы хотите посмотреть?',
    'start_question': 'Что вас интересует?',
    'no_new_images': 'Нет новых изображений',
    'new_images': 'Были добавлены следующие id:\n',
    'wb': 'Заглавные карточки товара для Wildberries',
    'wbc': 'Карусель карточки товара для Wildberries',
    'ozon': 'Карусель карточки товара для Ozon',
    'menu': 'Меню рациона здорового питания',
    'colors': 'Каталог промышленных красок',
    'in': 'Магазин одежды в Инсте',
    'in_s': 'Оформление сторис в Инсте',
    'vk': 'Оформление сообществ в VK',
    'taplink': 'Оформление таплинк',
    'others': 'Прочие работы для ознакомления со стилем',
    'order': 'Чтобы сделать заказ напишите сюда! (https://t.me/Marija_design)'
}


prices = {
    'infographics': 'Cоздание карточек товаров для Wildberries, Яндекс, Ozon,'\
        ' Авито - 400 рублей за слайд при наличии ТЗ, + индивидуальная скидка'\
        ' за объём до 25%\n',
    'presentations': 'Оформление гайдов, презентаций. Основная программа -'\
        'Figma, также работаю также в Power Point, если вы захотите потом'\
        'редактировать самостоятельно.\nОт 400 рублей за слайд + скидка за'\
        ' объём\n',
    'social_networks': 'Оформление ленты Нельзяграм (а также сторис,'\
        'обложка актуального):\n1 пост, а также сторис, аватарка,'\
        'обложка актуального 400 рублей слайд + скидка за объем\n\n'\
        'Оформление сообщества ВКонтакте - пакет мини 3500 рублей '\
        '(2 обложки десктопная и мобильная, 4 услуги и 4 виджета, +'\
        ' аватарка)\n',
    'taplink': 'Оформление Таплинк - от 2000 рублей за блок с версткой, '\
        'тариф таплинк оплачивается отдельно\n',
    'all': '\nВозможна работа без ТЗ, тогда стоимость больше. '\
        'Также при наличии необходимости можно сделать редизайн, '\
        'минимальные изменения в дизайне за меньшую цену при наличии объёма'\
        ', обсуждается индивидуально.',
}


folders = {
    'wb': 'infographics',
    'wbc': 'infographics',
    'ozon': 'infographics',
    'menu': 'presentations',
    'colors': 'presentations',
    'in': 'social_networks',
    'in_s': 'social_networks',
    'vk': 'social_networks',
    'taplink': '',
    'others': ''    
}


keyboards = {
    'categories': keyboards.categories_keyboard(),
    'infographics': keyboards.infographics_keyboard(),
    'presentations': keyboards.presentations_keyboard(),
    'social_networks': keyboards.sn_keyboard(),
    'back_to_menu': keyboards.back_to_menu_keyboard(),
    'order_kb': keyboards.order_keyboard()
}


def send_picture_first_time(filename, chat_id):
    file_id = ''
    try:
        with open(filename, 'rb') as f:
            file_id = f.read()
    except IOError:
        bot.send_message(chat_id, text_messages['error_no_files'])
    if not file_id:
        bot.send_message(chat_id, text_messages['error_no_files'])
        return
    msg = bot.send_photo(chat_id, photo=file_id)
    add_file_id(filename.name, msg.photo[-1].file_id)
    return msg


def send_pictures(filenames, chat_id):
    files_to_send = [get_file_id(filename.name) for filename in filenames]
    if len(files_to_send) > 1:
        files_to_send = [types.InputMediaPhoto(filename) for filename in files_to_send][:10]
        msg = bot.send_media_group(chat_id, media=files_to_send)
        return msg
    elif len(files_to_send) == 1:
        msg = bot.send_photo(chat_id, photo=files_to_send[0])
    else:
        msg = bot.send_message(chat_id, text_messages['error_no_files'])


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    chat_id = message.chat.id
    username = message.from_user.first_name
    greetings_text = text_messages.get('greetings').format(username)
    greetings_img = utils.get_pictures_filenames('')[0]
    filename = greetings_img.name
    file_id = get_file_id(filename)
    if not file_id:
        send_picture_first_time(greetings_img, chat_id)
    else:
        send_pictures([greetings_img], chat_id)
    bot.send_message(chat_id=chat_id, text=greetings_text)
    bot.send_message(
        chat_id=chat_id,
        text='Что вас интересует?',
        reply_markup=types.InlineKeyboardMarkup(keyboards['categories'])
    )


@bot.message_handler(commands=['rebuild'])
def collect_all_file_ids(message):
    chat_id = message.chat.id
    user_id = str(message.from_user.id)
    if str(user_id) == admin_id:
        new_images = []
        images = utils.get_all_pictures()
        for image in images:
            file_id = get_file_id(image.name)
            if not file_id:
                send_picture_first_time(image, chat_id)
                new_images.append(image.name)
        if not new_images:
            response = text_messages['no_new_images']
        else:
            response = text_messages['new_images'] + '\n'.join(new_images)
        bot.send_message(
            chat_id=chat_id,
            text=response
        )
    else:
        bot.send_message(
            chat_id=chat_id,
            text=text_messages['no_command'],
            reply_markup=types.InlineKeyboardMarkup(keyboards['categories'])
        )


@bot.message_handler(commands=['stat'])
def collect_all_file_ids(message):
    user_id = str(message.from_user.id)
    chat_id = message.chat.id
    if user_id == admin_id or owner_id:
        pass


@bot.callback_query_handler(func=lambda call: True)
def categories_callback(call):
    callback_data = call.data
    chat_id = call.message.chat.id
    match callback_data:
        case kb if kb in keyboards.keys():
            bot.send_message(
                chat_id,
                text='Примеры моих работ:',
                reply_markup=types.InlineKeyboardMarkup(keyboards[kb])
            )
        case folder if folder in folders.keys():
            folder_name = folders[callback_data]
            keyboard = keyboards.get(folder_name, [])
            extended_path = os.path.join(folder_name, callback_data)
            pictures = utils.get_pictures_filenames(extended_path)
            price = prices.get(folder_name, '')
            if folder == 'taplink':
                price = prices['taplink']
            price += prices['all']
            send_pictures(pictures, chat_id)
            time.sleep(0.25)
            bot.send_message(
                chat_id,
                text=price,
                reply_markup=types.InlineKeyboardMarkup(
                    keyboard + keyboards['back_to_menu'] + keyboards['order_kb']
                )
            )
        case 'to_menu':
            bot.send_message(
                chat_id=chat_id,
                text=text_messages['start_question'],
                reply_markup=types.InlineKeyboardMarkup(keyboards['categories'])
            )
        case 'order':
            bot.send_message(
                chat_id=chat_id,
                text=text_messages['order'],
                reply_markup=types.InlineKeyboardMarkup(keyboards['back_to_menu']))
        case _:
            bot.send_message(chat_id, text=text_messages['error_no_files'])


@bot.message_handler(content_types=['text'])
def process_messages(message):
    chat_id = message.chat.id
    print(f'MIVKOSH: {str(message.from_user)}')
    bot.send_message(
            chat_id=chat_id,
            text=text_messages['no_command'],
            reply_markup=types.InlineKeyboardMarkup(keyboards['categories'])
        )


def start():
    bot.infinity_polling()


if __name__ == '__main__':
    start()
