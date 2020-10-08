import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update
import requests
import json
import os

PORT = int(os.environ.get('PORT', 5000))
secrets = json.load(open("secrets.json"))
# api header and url
url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"

headers = {
    'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
    'x-rapidapi-key': secrets["API_KEY"]
}
# enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


TOKEN = secrets["TOKEN"]


def start(update: Update, context: CallbackContext):
    # print(update)
    # author=update.message.from_user.first_name
    # reply="hi! {} ".format(author)
    # bot.send_message(chat_id=update.message.chat_id,text=reply)
    # update.message.reply_text("hey")
    _help(update, context)


def _help(update: Update, context: CallbackContext):
    help_txt = "Wanna know what the slang word means? \n \n Use: '/' followed by the slang word \n Ex: /lol"
    update.message.reply_text(help_txt)


def echo_txt(update: Update, context: CallbackContext):
    # reply=update.message.text
    # bot.send_message(chat_id=update.message.chat_id,text=reply)
    logger.info(update)

    word = update.message.text.split('/')[1]
    querystring = {"term": word}
    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    json_res = json.loads(response.text)
    print(json_res['list'][0]['example'])
    definition = (json_res['list'][0]['definition'])
    example = (json_res['list'][0]['example'])
    word_data = "<b>What it means</b> \n"+definition+"\n\n<b>Example</b> \n"+example+"\n"

    update.message.reply_text(word_data,parse_mode='html')

# def error(bot,update):
#     logger.error("Error")


def main():
    updater = Updater(TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", _help))
    dp.add_handler(MessageHandler(Filters.text, echo_txt))
    # dp.add_error_handler(error)

    # updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook(
        'https://powerful-ravine-41494.herokuapp.com/' + TOKEN)
    logger.info("started polling")
    updater.idle()


if __name__ == "__main__":
    main()
