from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import sqlite3

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from config import TOKEN
import text_or_question as text
import keaboard as kb
import time
import datetime
import asyncio

from db_admin import DateBase

from sqlit import reg_user,obnova_members_status,count_member_in_status,info_members,send_status_no_rassilka,cheack_status

datebase = DateBase('users.db')

bot = Bot(token=TOKEN)
db = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

class st_reg(StatesGroup):
    st_name = State()
    st_fname = State()
    step_q = State()
    step_regbutton = State()

user_list1 = []
user_list2 = []
user_list3 = []
user_list4 = []
user_list5 = []
user_list6 = []
user_list7 = []
user_list8 = []


class Form(StatesGroup):
    info_text = State()
    user_delete = State()

ADMIN_ID_1 = 494588959 #Cаня
ADMIN_ID_2 = 44520977 #Коля
ADMIN_ID_3 = 678623761 #Бекир
ADMIN_ID_4 = 941730379 #Джейсон
ADMIN_ID_5 = 807911349 #Байзат
ADMIN_ID_6 = 1045832338 #Коля 2 (НИКОЛА_ОДНОУС)

ADMIN = [ADMIN_ID_1,ADMIN_ID_2,ADMIN_ID_3,ADMIN_ID_4,ADMIN_ID_5,ADMIN_ID_6]

user_1 = '@nikolanext' #ДЛЯ ТЕХ, КТО ПЛАТНЫЙ (1)
user02349 = '@NikolaOdnous' #ДЛЯ ТЕХ, КТО НЕ (1)

@db.message_handler(commands=['start'])
async def greetings(message: types.Message):

    user_id = message.chat.id
    reg_user(user_id,0) #Записываем в базу человека со статусом 0

    m = await message.answer_photo(text.hi_photo_id, caption=text.hi_text, reply_markup=kb.the_first_go_button)

    go_new = 'Г'
    for i in range(1,14):
        go_new+='о'
        await bot.edit_message_caption(chat_id=user_id,message_id=m.message_id,caption=text.hi_text.format(go_new),reply_markup=kb.the_first_go_button)
        await asyncio.sleep(0.43)



@db.message_handler(commands=['admin'])
async def vienw_adminka(message: types.Message):
    if message.chat.id in ADMIN:
        button1 = KeyboardButton('📊Статистика всех пользователей')

        button2 = KeyboardButton('💿База данных')
        button3 = KeyboardButton('🔫Удаление челов')

        button4 = KeyboardButton('🆓Рассылка бесплатникам')
        button5 = KeyboardButton('💰Рассылка платникам')

        markup3 = ReplyKeyboardMarkup(resize_keyboard=True)
        markup3 = markup3.add(button1)
        markup3 = markup3.add(button2,button3)
        markup3 = markup3.add(button4,button5)

        await bot.send_message(chat_id=message.chat.id,text='Открыта админка 🔘',reply_markup=markup3)





@db.message_handler(state=Form.user_delete,content_types=['video','voice','photo','video_note','file','document','text'])
async def delete_user(message: types.Message, state: FSMContext):
    try:
        user_id = message.forward_from.id
        send_status_no_rassilka(user_id)
    except Exception as e:
        print(e)

    markup = types.InlineKeyboardMarkup()
    bat_otmena12 = types.InlineKeyboardButton(text='Выйти из режима удаления',callback_data='exit_del')
    markup.add(bat_otmena12)

    await message.answer('Пользователь удалён 🩸',reply_markup=markup)



@db.message_handler(state=Form.info_text, content_types=['text', 'photo', 'video_note', 'video', 'voice'])
async def send_mailing_text(message: types.Message, state: FSMContext):
    if message.text == 'отмена':
        await state.finish()
        await message.answer('Отменено')
    if message.text or message.photo or message.video:
        for user_id in datebase.mailing_user_id():
            if message.text and message.photo:
                await bot.send_photo(user_id[1], message.photo[2].file_id, caption=message.text)
            elif message.text and message.video:
                await bot.send_video(user_id[1], message.video.file_id, caption=message.text)
            elif message.photo:
                await bot.send_photo(user_id[1], message.photo[2].file_id)
            elif message.video:
                await bot.send_video(user_id[1], message.video.file_id)
            elif message.text:
                await bot.send_message(user_id[1], message.text)
    elif message.video_note:
        for user_id in datebase.mailing_user_id():
            await bot.send_video_note(user_id[1], message.video_note.file_id)
    elif message.voice:
        for user_id in datebase.mailing_user_id():
            await bot.send_voice(user_id[1], message.voice.file_id)
    await message.answer('Рассылка произведена.')
    await message.answer(f'Рассылку получили {datebase.count_string2()} из {datebase.count_string()}')
    await state.finish()


@db.callback_query_handler(lambda call: True, state = '*')
async def answer_push_inline_button(call, state: FSMContext):
    global user_list1
    user_id = call.message.chat.id # ЮЗЕР ЧЕЛА
    status = (cheack_status(user_id))[0]
    if status == 1:
        username_contact = user_1
    else:
        username_contact = user02349

    if call.data == 'go_button':
        await state.finish()
        await bot.send_message(chat_id=call.message.chat.id,text='Отменено. Включен обычный режим✅')
    if call.data == 'go_button':
        await call.message.answer_video_note(text.video_note_id, reply_markup=kb.pass_the_five_question)
    elif call.data == 'five_question':
        await call.message.answer_animation(text.the_first_question_gif_id, caption=text.the_first_question_text,
                                            reply_markup=kb.first_question_buttons)
    elif call.data == 'first_question':
        await call.message.delete()
        await call.message.answer_animation(text.the_second_question_gif_id, caption=text.the_second_question_text,
                                            reply_markup=kb.second_question_buttons)
    elif call.data == 'second_question':
        await call.message.delete()
        await call.message.answer_animation(text.the_third_question_gif_id, caption=text.the_third_question_text,
                                            reply_markup=kb.third_question_buttons)
    elif call.data == 'third_question':
        await call.message.delete()
        await call.message.answer_animation(text.the_fourth_question_gif_id, caption=text.the_fourth_question_text,
                                            reply_markup=kb.fourth_question_buttons)


    elif call.data[:15] == 'fourth_question':
        if call.data == 'fourth_question1': # Человек из рекламы инст
            obnova_members_status(call.message.chat.id, 1)
        if call.data == 'fourth_question2': # Человек из ТикТока
            obnova_members_status(call.message.chat.id, 2)
        if call.data == 'fourth_question3': # Человек из Рилса
            obnova_members_status(call.message.chat.id, 3)
        if call.data == 'fourth_question4': # Другое
            obnova_members_status(call.message.chat.id, 4)

        await call.message.delete()
        await call.message.answer_animation(text.the_five_question_gif_id, caption=text.the_five_question_text,
                                            reply_markup=kb.five_question_buttons)




    elif call.data == 'five_questions':
        await call.message.delete()
        await call.message.answer('🕺🏻А вот и обещанный бонус 🕺🏻')
        await call.message.answer_document(text.bonus_dock_file_id)
        await call.message.answer_photo(text.finished_text_file_id, caption=text.finished_text, reply_markup=kb.finished_text_button)

    elif call.data == 'go_2':
        await call.message.answer_video('BAACAgIAAxkBAAMmYV1W4yEZI3tZMuEFt7TzpRXmTtMAAskPAALV8iFKl-Icg7tg87IhBA')
        # await call.message.answer('Первое видео')
        await asyncio.sleep(78)#60
        await call.message.answer(text='Жмякай кнопку пока не убежала👇', reply_markup=kb.further_button)

    elif call.data == 'further':
        await call.message.answer_video('BAACAgIAAxkBAAMoYV1XarMS_OoOn_Vwr3oJ9liOtPkAAogVAALalClKikrq4brnf-0hBA')
        # await call.message.answer('Второе видео')
        await asyncio.sleep(136)#136
        await call.message.answer(text='Жмякай кнопку пока не убежала👇', reply_markup=kb.futher2_button)

    elif call.data == 'further2':
        await call.message.answer_video(f'BAACAgIAAxkBAAMqYV1XrtFkA-VnlCNrx2scKWuU6pUAAp0TAAKBgcBKIdx8Ive5nrYhBA')
        # await call.message.answer('Третье видео')
        await asyncio.sleep(205)#205
        await call.message.answer(text.last_text.format(username_contact))
        user_id = call.message.chat.id
        username = call.message.from_user.username

        # Если рассылка человек не состоит ни в одной из группе, то добалвяем его в первую
        if (user_id not in user_list1) and (user_id not in user_list2) and (user_id not in user_list3) and (user_id not in user_list4) and (user_id not in user_list5) and (user_id not in user_list6) and (user_id not in user_list7) and (user_id not in user_list8):
            #ЕСЛИ ЧЕЛА НЕТУ НИ В ОДНОЙ ИЗ ГРУПП ДЛЯ ПРОГРЕВА, ТО:
            user_list1.append(user_id)
            try:
                datebase.records_of_mailing_users(username, user_id)
            except Exception as e:
                print(e)



@db.message_handler(content_types=['text', 'photo', 'video_note', 'animation', 'document', 'video','file'])
async def all_message(message: types.Message, state: FSMContext):
    # try:
    #     print(message.video.file_id)
    # except:
    #     pass
    #
    # try:
    #     print(message.photo[2].file_id)
    # except:
    #     pass
    #
    # try:
    #     print(message.video_note.file_id)
    # except:
    #     pass
    #
    # try:
    #     print(message.animation.file_id)
    # except:
    #     pass
    #
    # try:
    #     print(message.document.file_id)
    # except:
    #     pass
    #
    if message.chat.id in ADMIN:


        if message.text == '📊Статистика всех пользователей':
            all = info_members()# Всего пользователей
            s1 = count_member_in_status(1)
            s2 = count_member_in_status(2)
            s3 = count_member_in_status(3)
            s4 = count_member_in_status(4)

            s0 = count_member_in_status(0) #Еще не выбрпали ответ


            await bot.send_message(chat_id=message.chat.id,text=f"""<b>👥Всего пользователей: {all}</b>

1️⃣Пользователей из инсты: {s1}
2️⃣Пользователей из ТикТока : {s2}
3️⃣Пользователей из Рилса: {s3}
4️⃣Пользователей из «Другого»: {s4}

🟡Еще не выбрали ответ: {s0}""",parse_mode='html')

        if message.text == '💿База данных':
            await message.answer_document(open("server.db", "rb"))

        if message.text == '🔫Удаление челов':
            await message.answer('👺Включен режим удаление челов \n'
                                 '🔙Для выхода, напиши "отмена"')
            await Form.user_delete.set()

        if message.text == '🆓Рассылка бесплатникам': #Рассылка по группе 2,3,4,0
            murkap = types.InlineKeyboardMarkup()
            bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
            murkap.add(bat0)
            await bot.send_message(message.chat.id, 'Перешли мне уже готовый пост и я разошлю его всем юзерам',
                                   reply_markup=murkap)
            await st_reg.step_q.set()

            await state.update_data(type_rassilki = 2340) # ТИП расслыки по 2,3,4,0 группе

        if message.text == '💰Рассылка платникам': #Рассылка по группе 1
            murkap = types.InlineKeyboardMarkup()
            bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
            murkap.add(bat0)
            await bot.send_message(message.chat.id, 'Перешли мне уже готовый пост и я разошлю его всем юзерам',
                                   reply_markup=murkap)
            await st_reg.step_q.set()

            await state.update_data(type_rassilki=1) # ТИП расслыки по первой группе




#ПРОГРЕВ
async def send_to_a_certain_hour():
    while True:


        offset = datetime.timezone(datetime.timedelta(hours=3))
        now_time = datetime.datetime.now(offset)

        if now_time.hour == 16:
            for user7 in user_list7:
                status = (cheack_status(user7))[0]
                if status == 1:
                    username_contact = user_1
                else:
                    username_contact = user02349
                if status != 9:
                    await bot.send_message(user7, text=text.dayly_text7.format(username_contact))
                    user_list7.remove(user7)
                    user_list8.append(user7)

            for user6 in user_list6:
                status = (cheack_status(user6))[0]
                if status == 1:
                    username_contact = user_1
                else:
                    username_contact = user02349
                if status != 9:
                    await bot.send_photo(user6, photo=text.dayly_photo_id6, caption=text.dayly_text6.format(username_contact))
                    user_list7.append(user6)
                    user_list6.remove(user6)

            for user5 in user_list5:
                status = (cheack_status(user5))[0]
                if status == 1:
                    username_contact = user_1
                else:
                    username_contact = user02349

                if status != 9:
                    await bot.send_photo(user5, photo=text.dayly_photo_id5, caption=text.dayly_text5.format(username_contact))
                    user_list6.append(user5)
                    user_list5.remove(user5)

            for user4 in user_list4:
                status = (cheack_status(user4))[0]
                if status == 1:
                    username_contact = user_1
                else:
                    username_contact = user02349
                if status != 9:
                    await bot.send_photo(user4, photo=text.dayly_photo_id4, caption=text.dayly_text4.format(username_contact))
                    user_list5.append(user4)
                    user_list4.remove(user4)

            for user3 in user_list3:
                status = (cheack_status(user3))[0]
                if status == 1:
                    username_contact = user_1
                else:
                    username_contact = user02349
                if status != 9:
                    await bot.send_photo(user3, photo=text.dayly_photo_id3, caption=text.dayly_text3.format(username_contact))
                    user_list4.append(user3)
                    user_list3.remove(user3)

            for user2 in user_list2:
                status = (cheack_status(user2))[0]
                if status == 1:
                    username_contact = user_1
                else:
                    username_contact = user02349
                if status != 9:
                    await bot.send_message(user2, text=text.dayly_text2.format(username_contact))
                    user_list3.append(user2)
                    user_list2.remove(user2)

            for user1 in user_list1:
                status = (cheack_status(user1))[0]
                if status == 1:
                    username_contact = user_1
                else:
                    username_contact = user02349
                if status != 9:
                    await bot.send_photo(user1, photo=text.dayly_photo_id1, caption=text.dayly_text1.format(username_contact))
                    user_list2.append(user1)
                    user_list1.remove(user1)


        await asyncio.sleep(3600)


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()



@db.callback_query_handler(text='otemena',state='*')
async def otmena_12(call: types.callback_query, state: FSMContext):
    await bot.send_message(call.message.chat.id, 'Отменено')
    await state.finish()
    try:
        await bot.delete_message(call.message.chat.id,message_id=call.message.message_id)
    except: pass



@db.message_handler(state=st_reg.step_q,content_types=['text','photo','video','video_note','animation','voice','sticker']) # Предосмотр поста
async def redarkt_post(message: types.Message, state: FSMContext):
    await st_reg.st_name.set()
    murkap = types.InlineKeyboardMarkup()
    bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    bat1 = types.InlineKeyboardButton(text='РАЗОСЛАТЬ', callback_data='send_ras')
    bat2 = types.InlineKeyboardButton(text='Добавить кнопки', callback_data='add_but')
    murkap.add(bat1)
    murkap.add(bat2)
    murkap.add(bat0)

    await message.copy_to(chat_id=message.chat.id)
    q = message
    await state.update_data(q=q)

    await bot.send_message(chat_id=message.chat.id,text='Пост сейчас выглядит так 👆',reply_markup=murkap)



# НАСТРОЙКА КНОПОК
@db.callback_query_handler(text='add_but',state=st_reg.st_name) # Добавление кнопок
async def addbutton(call: types.callback_query, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    await bot.send_message(call.message.chat.id,text='Отправляй мне кнопки по принципу Controller Bot\n\n'
                                                     'Пока можно добавить только одну кнопку')
    await st_reg.step_regbutton.set()


@db.message_handler(state=st_reg.step_regbutton,content_types=['text']) # Текст кнопок в неформате
async def redarkt_button(message: types.Message, state: FSMContext):
    arr2 = message.text.split('-')

    k = -1  # Убираем пробелы из кнопок
    for i in arr2:
        k+=1
        if i[0] == ' ':
            if i[-1] == ' ':
                arr2[k] = (i[1:-1])
            else:
                arr2[k] = (i[1:])

        else:
            if i[-1] == ' ':

                arr2[0] = (i[:-1])
            else:
                pass

    # arr2 - Массив с данными


    try:
        murkap = types.InlineKeyboardMarkup() #Клавиатура с кнопками
        bat = types.InlineKeyboardButton(text= arr2[0], url=arr2[1])
        murkap.add(bat)

        data = await state.get_data()
        mess = data['q']  # ID сообщения для рассылки

        await bot.copy_message(chat_id=message.chat.id, from_chat_id=message.chat.id,message_id=mess.message_id,reply_markup=murkap)

        await state.update_data(text_but =arr2[0]) # Обновление Сета
        await state.update_data(url_but=arr2[1])  # Обновление Сета

        murkap2 = types.InlineKeyboardMarkup() # Клавиатура - меню
        bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
        bat1 = types.InlineKeyboardButton(text='РАЗОСЛАТЬ', callback_data='send_ras')
        murkap2.add(bat1)
        murkap2.add(bat0)

        await bot.send_message(chat_id=message.chat.id,text='Теперь твой пост выглядит так☝',reply_markup=murkap2)


    except:
        await bot.send_message(chat_id=message.chat.id,text='Ошибка. Отменено')
        await state.finish()


# КОНЕЦ НАСТРОЙКИ КНОПОК


@db.callback_query_handler(text='send_ras',state="*") # Рассылка
async def fname_step(call: types.callback_query, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)

    data = await state.get_data()
    mess = data['q'] # Сообщения для рассылки

    type_rass = data['type_rassilki']
    murkap = types.InlineKeyboardMarkup()  # Клавиатура с кнопками

    try: #Пытаемся добавить кнопки. Если их нету оставляем клаву пустой
        text_but = data['text_but']
        url_but = data['url_but']
        bat = types.InlineKeyboardButton(text=text_but, url=url_but)
        murkap.add(bat)
    except: pass


    db = sqlite3.connect('server.db')
    sql = db.cursor()
    await state.finish()
    if type_rass == 1:
        users = sql.execute(f"SELECT id FROM user_time WHERE status_active = 1").fetchall()
    else:
        users = sql.execute(f"SELECT id FROM user_time WHERE status_active = 0 or status_active = 2 or status_active = 3 or status_active =4").fetchall()

    bad = 0
    good = 0
    await bot.send_message(call.message.chat.id, f"<b>Всего пользователей: <code>{len(users)}</code></b>\n\n<b>Расслыка начата!</b>",
                           parse_mode="html")
    for i in users:
        await asyncio.sleep(1)
        try:
            await mess.copy_to(i[0],reply_markup=murkap)
            good += 1
        except:
            bad += 1

    await bot.send_message(
        call.message.chat.id,
        "<u>Рассылка окончена\n\n</u>"
        f"<b>Всего пользователей:</b> <code>{len(users)}</code>\n"
        f"<b>Отправлено:</b> <code>{good}</code>\n"
        f"<b>Не удалось отправить:</b> <code>{bad}</code>",
        parse_mode="html"
    )
#########################################################



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(send_to_a_certain_hour())
    executor.start_polling(db, on_shutdown=shutdown,skip_updates=True)
