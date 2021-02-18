from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Defaults

from botcommands import start, closest_rounds, get_user_info, get_contest_standings, get_last_round

API_KEY = "1697589398:AAGGFcUCdXGrqBq0Yux9UOTWLnoWdkaSvAI"


def main():
    updater = Updater(API_KEY, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    dispatcher.add_handler(CommandHandler("closest_rounds", closest_rounds))

    dispatcher.add_handler(CommandHandler("user", get_user_info))

    dispatcher.add_handler(CommandHandler("contest_results", get_contest_standings))

    dispatcher.add_handler(CommandHandler("last_contest", get_last_round))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
