import telebot
from telebot import types

from Fomo.telebot_fomo.Event import Event

from Fomo.telebot_fomo.search_event import event_string
import Fomo.telebot_fomo.db_functions as func
from Fomo.telebot_fomo.side_func import get_image_url


TOKEN = "831344999:AAHjyCtTfi95bEGpsBx2Yk1HK_dYh7nDv3c"
bot = telebot.TeleBot(TOKEN)

# Handle '/start' and '/help'
@bot.message_handler(commands=["help", "start"])
def send_welcome(msg):
    chat_id = msg.chat.id
    msg = bot.send_message(
        chat_id,
        """\
~~~~Welcome to FOMO bot~~~~
This bot can help you keep track of all your upcoming events.
Please input:
/search to begin search for events
""",
    )
    bot.message_handler(msg, handle_actions)


# Handles 'search'
@bot.message_handler(commands=['search'])
def search_command(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("Category", "Date", 'Venue')
    bot.send_message(chat_id, "What would you like to search by?", reply_markup=markup)


# Handles 'category'
@bot.message_handler(commands=['category'])
def category_search(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    categories = func.select_categories()
    for cat in categories:
        markup.add(cat)
    msg = bot.send_message(
        chat_id, "What category would you like to check?", reply_markup=markup
    )
    bot.register_next_step_handler(msg, retrieve_category)


# Handles 'date'
@bot.message_handler(commands=['date'])
def date_search(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("TODAY", "THIS WEEK", "THIS MONTH")
    msg = bot.send_message(chat_id, "What date would you like to check?", reply_markup=markup)
    bot.register_next_step_handler(msg, retrieve_date)


# Handles 'venue'
@bot.message_handler(commands=['venue'])
def venue_search(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    venues = func.select_venue()
    for ven in venues:
        markup.add(ven[0])
    msg = bot.send_message(chat_id, "What venue would you like to check?", reply_markup=markup)
    bot.register_next_step_handler(msg, retrieve_venue)


@bot.message_handler(commands=['doggo'])
def doggo(message):
    url = get_image_url()
    chat_id = message.chat.id
    bot.send_photo(chat_id=chat_id, photo=url)


# Handles all commands/messages that are invalid and commands that are typed as msg
@bot.message_handler(func=lambda msg: msg.text is not None)
def handle_actions(msg):
    chat_id = msg.chat.id
    message = msg.text
    if message == "search":
        search_command(msg)
    elif message == "Category" or message == 'category':
        category_search(msg)
    elif message == "Date" or message == 'date':
        date_search(msg)
    elif message == "Venue" or message == 'venue':
        venue_search(msg)
    else:
        bot.send_message(
            chat_id, "There is no such function. Please try again"
        )


def retrieve_category(message):
    chat_id = message.chat.id
    category = message.text
    lst_events = func.query_category(category)
    if lst_events is not None:
        event_details = "~~~~~ Events by " + category + " ~~~~~\n"
        for index, event in lst_events.iterrows():
            new_event = Event(event['title'])
            new_event.id = event['id']
            new_event.date = event['date']
            new_event.description = event['description']
            new_event.category = func.find_category(func.find_category_id(event['id']))
            new_event.venue = func.find_venue(event['venue_id'])
            event_details += event_string(new_event)
        msg = bot.send_message(chat_id, event_details)
        bot.register_next_step_handler(msg, retrieve_category)
    else:
        bot.send_message(chat_id, "Oops there are no events here.")


def retrieve_venue(message):
    chat_id = message.chat.id
    venue = message.text
    lst_events = func.query_venue(venue)
    if lst_events is not None:
        event_details = "~~~~~ Events by " + venue + " ~~~~~\n"
        for index, event in lst_events.iterrows():
            new_event = Event(event['title'])
            new_event.id = event['id']
            new_event.date = event['date']
            new_event.description = event['description']
            new_event.category = func.find_category(func.find_category_id(event['id']))
            new_event.venue = func.find_venue(event['venue_id'])
            event_details += event_string(new_event)
        msg = bot.send_message(chat_id, event_details)
        bot.register_next_step_handler(msg, retrieve_venue)
    else:
        bot.send_message(chat_id, "Oops there are no events here.")


def retrieve_date(message):
    chat_id = message.chat.id
    date = message.text
    lst_event = func.query_date(date)
    if lst_event is not None:
        event_details = "~~~~~ Events  " + date + " ~~~~~\n"
        for index, event in lst_event.iterrows():
            new_event = Event(event['title'])
            new_event.id = event['id']
            new_event.date = event['date']
            new_event.description = event['description']
            new_event.category = func.find_category(func.find_category_id(event['id']))
            new_event.venue = func.find_venue(event['venue_id'])
            event_details += event_string(new_event)
        msg = bot.send_message(chat_id, event_details)
        bot.register_next_step_handler(msg, retrieve_date)
    else:
        bot.send_message(chat_id, "Oops there are no events here.")

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will happen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=0)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.polling()


