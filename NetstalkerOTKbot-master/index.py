import telebot
from telebot import types
import json
from users import manager, prototype
import codecs

bot = telebot.TeleBot('1289437496:AAGKvUDEGudYBRSh1WfjGwuNn0F3GmMdfkM')

_languages_to_load = ["ru", "en", "ua"]

languages = {}
for lang in _languages_to_load:
    with codecs.open("./language/"+lang+".json", "r", "utf-8") as f:
        languages[lang] = json.loads(f.read())

UserManager = manager.UserManager()

def checkRegistration(chat_id):
    user = UserManager.searchUser(chat_id)
    if user == False:
        bot.send_message(chat_id, "You aren't registered, please do it with this command /start", reply_markup=types.ReplyKeyboardRemove())
        return False
    else:
        return user

def markupMenu(lang):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
    markup.row('ℹ️ '+languages[lang]["what_is"], "❔ "+languages[lang]["test"])
    markup.add('🏳️‍🌈 '+languages[lang]["devgays"], "💎 "+languages[lang]["sbutton_name"])
    markup.add('♻️ '+languages[lang]["hello"])
    return markup

def testMenu(lang):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    markup.row('✅ '+languages[lang]["test_btn_yes"])
    markup.add('❌ '+languages[lang]["test_btn_no"])
    return markup

def presentationMarkup(lang):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    markup.row('➡️ '+languages[lang]["Continue"])
    return markup
    
def resolveContentType(content, chat_id, bot, lang):
    if"https://" in content:
        bot.send_photo(chat_id, content, reply_markup=presentationMarkup(lang))
    else:
        bot.send_message(chat_id, content, reply_markup=presentationMarkup(lang))

def infoMenu(lang):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    markup.row('➡️ '+languages[lang]["Continue"])
    markup.row('💀 '+languages[lang]["DW"])
    return markup

@bot.message_handler(commands=['start'])
@bot.message_handler(regexp='♻️.*')
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    markup.row('🇷🇺 Русский')
    markup.add('🇺🇸 English')
    markup.add('🇺a Украинский')
    bot.send_message(message.chat.id, 'Choose your language', reply_markup=markup)

@bot.message_handler(regexp='🇷🇺.*')
@bot.message_handler(regexp='🇺🇸.*')
def choose_language_ru(message):
    if "🇷🇺" in message.text:
        language = "ru"
    else:
        language = "en"
    else
        language = "ua"

    user = UserManager.searchUser(message.chat.id)
    if user == False:
        newUser = prototype.User(language, message.chat.id)
        UserManager.insertUser(newUser)
    else:
        user.language = language

    bot.send_message(message.chat.id, languages[language]["donechose"], reply_markup=markupMenu(language))

@bot.message_handler(regexp='🏳️‍🌈.*')
def about_developers(message):
    user = checkRegistration(message.chat.id)
    if user == False:
        return
    bot.send_message(message.chat.id, languages[user.language]["devGAYs2"])

@bot.message_handler(regexp='❔.*')
def tests_start(message):
    user = checkRegistration(message.chat.id)
    if user == False:
        return

    user.curTest = 1
    user.points = 0
    bot.send_message(message.chat.id, languages[user.language]["test_question_1"], reply_markup=testMenu(user.language))

@bot.message_handler(regexp='✅.*')
@bot.message_handler(regexp='❌.*')
def test_answer(message):
    user = checkRegistration(message.chat.id)
    if user == False:
        return

    if("✅" in message.text):
        user.points += 1
    user.curTest += 1
    if user.curTest > 10:
        bot.send_message(message.chat.id, languages[user.language]["result"]+": "+str(user.points * 10)+"%", reply_markup=markupMenu(user.language))
        return
    
    bot.send_message(message.chat.id, languages[user.language]["test_question_"+str(user.curTest)], reply_markup=testMenu(user.language))

@bot.message_handler(regexp='💎.*')
def sButton(message):
    user = checkRegistration(message.chat.id)
    if user == False:
        return

    bot.send_message(message.chat.id, languages[user.language]["sbutton"])


@bot.message_handler(regexp='ℹ️.*')
def presentation_start(message):
    user = checkRegistration(message.chat.id)
    if user == False:
        return

    user.page = 1
    resolveContentType(languages[user.language]["netis1"], message.chat.id, bot, user.language)

@bot.message_handler(regexp='➡️.*')
def presentation_next(message):
    user = checkRegistration(message.chat.id)
    if user == False:
        return

    user.page += 1
    key = "netis"+str(user.page)
    if(key in languages[user.language]):
        if(user.page == 4):
            bot.send_message(message.chat.id, languages[user.language][key], reply_markup=infoMenu(user.language))
            return
        resolveContentType(languages[user.language][key], message.chat.id, bot, user.language)
    else:
        bot.send_message(message.chat.id, "The end!", reply_markup=markupMenu(user.language))

@bot.message_handler(regexp='💀.*')
def about_DW_next(message):
    user = checkRegistration(message.chat.id)
    if user == False:
        return
    bot.send_message(message.chat.id, languages[user.language]["WhatIsDeepWeb"], reply_markup=presentationMarkup(user.language))
    bot.send_message(message.chat.id, languages[user.language]["WhatIsDarkNet"], reply_markup=presentationMarkup(user.language))

bot.polling()