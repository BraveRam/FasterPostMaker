import telebot
from telebot import custom_filters
from telebot.types import ReplyKeyboardMarkup

from utils.config import BOT_TOKEN, OWNER_ID
from utils.user_manager import user_exists, is_admin, is_banned, is_premium
from utils.database import db
from utils.keyboards import (
    get_main_keyboard, get_cancel_keyboard, get_type_button_keyboard,
    get_login_menu_keyboard, get_options_keyboard
)
from handlers.admin import setup_admin_handlers
from handlers.broadcast import setup_broadcast_handlers
from handlers.posts import setup_post_handlers
import utils.constants as const


# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="MARKDOWN")


# Setup handlers
admin_keyboard, cancel_keyboard = setup_admin_handlers(bot)
setup_broadcast_handlers(bot)
setup_post_handlers(bot)


@bot.message_handler(commands=["start"])
def start(message):
    """Handle /start command"""
    user_id = message.from_user.id
    users = user_exists(bot, user_id)
    banned = is_banned(user_id)
    
    if users is True:
        if banned is True:
            bot.send_message(message.chat.id, const.BANNED_MESSAGE)
        else:
            bot.send_message(
                message.chat.id,
                const.WELCOME_MESSAGE,
                reply_markup=get_main_keyboard()
            )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Main message handler"""
    banned = is_banned(message.from_user.id)
    user = user_exists(bot, message.chat.id)
    admin = is_admin(message.chat.id)
    
    # Admin commands
    if message.from_user.id == OWNER_ID or admin is True:
        if message.text == "🔎Search User🔍":
            bot.set_state(message.from_user.id, "searchuser", message.chat.id)
            return bot.send_message(message.chat.id, const.SEND_USER_ID, reply_markup=get_cancel_keyboard())
        
        if message.text == "⛔Ban User⛔":
            bot.set_state(message.from_user.id, "banuser", message.chat.id)
            return bot.send_message(message.chat.id, const.SEND_USER_ID, reply_markup=get_cancel_keyboard())
        
        if message.text == "🤓Unban User🤓":
            bot.set_state(message.from_user.id, "unbanuser", message.chat.id)
            return bot.send_message(message.chat.id, const.SEND_USER_ID, reply_markup=get_cancel_keyboard())
        
        if message.text == "📢Broadcast📢":
            choosebtn = ReplyKeyboardMarkup(resize_keyboard=True)
            choosebtn.add("✨TEXT", "🏄‍♂️PHOTO")
            choosebtn.add("❌Cancel")
            return bot.send_message(
                message.chat.id,
                const.CHOOSE_BROADCAST_TYPE,
                reply_markup=choosebtn
            )
        
        if message.text == "⏪Back":
            bot.delete_state(message.from_user.id, message.chat.id)
            return bot.send_message(message.chat.id, const.MAIN_MENU_MESSAGE, reply_markup=get_main_keyboard())
        
        if message.text == "🏄‍♂️PHOTO":
            bot.set_state(message.from_user.id, "sendwithphoto", message.chat.id)
            return bot.send_message(
                message.chat.id,
                const.SEND_BROADCAST_PHOTO,
                reply_markup=get_cancel_keyboard()
            )
        
        if message.text == "✨TEXT":
            bot.set_state(message.from_user.id, "sendtext", message.chat.id)
            return bot.send_message(message.chat.id, const.SEND_BROADCAST_TEXT, reply_markup=get_cancel_keyboard())
        
        if message.text == "🎁Set Premium🎁":
            bot.set_state(message.from_user.id, "setpremium", message.chat.id)
            return bot.send_message(message.chat.id, const.SEND_USER_ID, reply_markup=get_cancel_keyboard())
        
        if message.text == "🎈Remove Premium🎈":
            bot.set_state(message.from_user.id, "demotepremium", message.chat.id)
            return bot.send_message(message.chat.id, const.SEND_USER_ID, reply_markup=get_cancel_keyboard())
        
        if message.text == "📊Statstics📊":
            users = db.get_all_users()
            count = len(users)
            return bot.send_message(message.chat.id, const.TOTAL_USERS_TEMPLATE.format(count=count))
        
        if message.text == "👨‍✈️Admin(s)👨‍✈️":
            return bot.send_message(message.chat.id, const.FEATURE_MAINTENANCE)
        
        if message.text == "👮‍♂️Add Admin👮‍♂️":
            if message.chat.id == OWNER_ID:
                bot.set_state(message.from_user.id, "adadmin", message.chat.id)
                return bot.send_message(message.chat.id, const.SEND_USER_ID_ADMIN, reply_markup=get_cancel_keyboard())
            elif admin is True:
                return bot.send_message(message.chat.id, const.ADMIN_ONLY_MESSAGE)
        
        if message.text == "✖️Delete Admin✖️":
            if message.chat.id == OWNER_ID:
                bot.set_state(message.from_user.id, "deleteadmin", message.chat.id)
                return bot.send_message(message.chat.id, const.SEND_USER_ID_ADMIN, reply_markup=get_cancel_keyboard())
            elif admin is True:
                return bot.send_message(message.chat.id, const.ADMIN_ONLY_MESSAGE)
    
    # Regular user commands
    if user is True:
        if banned is True:
            return bot.send_message(message.chat.id, const.BANNED_MESSAGE)
    
    premium = is_premium(message.chat.id)
    
    # Login button handlers (premium feature)
    if message.text == "🗞TEXT":
        if premium is True:
            bot.set_state(message.from_user.id, "llink", message.chat.id)
            return bot.send_message(
                message.chat.id,
                const.LINK_PROMPT_SHARE251,
                reply_markup=get_cancel_keyboard()
            )
        else:
            return bot.send_message(message.chat.id, const.PREMIUM_ONLY_MESSAGE)
    
    if message.text == "📸PHOTO":
        if premium is True:
            bot.set_state(message.from_user.id, "lplink", message.chat.id)
            return bot.send_message(
                message.chat.id,
                const.LINK_PROMPT_SHARE251,
                reply_markup=get_cancel_keyboard()
            )
        else:
            return bot.send_message(message.chat.id, const.PREMIUM_ONLY_MESSAGE)
    
    # Main menu options
    if message.text == "📝CREATE POST":
        return bot.send_message(message.chat.id, const.CHOOSE_BUTTON_TYPE, reply_markup=get_type_button_keyboard())
    
    if message.text == "NORMAL BUTTON":
        return bot.send_message(
            message.chat.id,
            const.CHOOSE_POST_TYPE,
            reply_markup=get_options_keyboard()
        )
    
    if message.text == "📄TEXT":
        bot.set_state(message.from_user.id, "link", message.chat.id)
        return bot.send_message(message.chat.id, const.LINK_PROMPT, reply_markup=get_cancel_keyboard())
    
    if message.text == "📷PHOTO":
        bot.set_state(message.from_user.id, "linkphoto", message.chat.id)
        return bot.send_message(message.chat.id, const.LINK_PROMPT, reply_markup=get_cancel_keyboard())
    
    if message.text == "🔙Back":
        return bot.send_message(
            message.chat.id,
            const.WELCOME_MESSAGE,
            reply_markup=get_main_keyboard()
        )
    
    if message.text == "◀️Back":
        return bot.send_message(message.chat.id, const.CHOOSE_BUTTON_TYPE, reply_markup=get_type_button_keyboard())
    
    if message.text == "📲LOGIN BUTTON":
        return bot.send_message(
            message.chat.id,
            const.CHOOSE_LOGIN_BUTTON_TYPE,
            reply_markup=get_login_menu_keyboard()
        )
    
    if message.text == "📃HOW TO USE":
        return bot.send_message(message.chat.id, const.HELP_MESSAGE)


# Add custom filters
bot.add_custom_filter(custom_filters.StateFilter(bot))


if __name__ == "__main__":
    print("The bot has started running....")
    bot.infinity_polling()
