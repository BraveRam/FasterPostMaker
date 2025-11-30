from utils.database import db
from utils.constants import WELCOME_MESSAGE


def user_exists(bot, user_id):
    user = db.get_user(user_id)
    if user:
        return True
    else:
        bot.send_message(user_id, WELCOME_MESSAGE)
        return db.create_user(user_id)


def is_admin(user_id):
    user = db.get_user(user_id)
    if user and user.get("is_admin") == True:
        return True
    return None


def is_banned(user_id):
    user = db.get_user(user_id)
    if user and user.get("is_banned") == True:
        return True
    return None


def is_premium(user_id):
    user = db.get_user(user_id)
    if user and user.get("is_premium") == True:
        return True
    return None
