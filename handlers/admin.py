from telebot.types import ReplyKeyboardMarkup
from utils.user_manager import is_admin, user_exists, is_banned
from utils.database import db
from utils.config import OWNER_ID
import utils.constants as const


def setup_admin_handlers(bot):
    """Setup all admin handlers"""
    
    # Admin keyboard
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, input_field_placeholder="Admin Menu")
    keyboard.add(
        "🔎Search User🔍", "⛔Ban User⛔", "🤓Unban User🤓",
        "📢Broadcast📢", "👮‍♂️Add Admin👮‍♂️", "✖️Delete Admin✖️",
        "👨‍✈️Admin(s)👨‍✈️", "📊Statstics📊", "🎁Set Premium🎁", "🎈Remove Premium🎈"
    )
    keyboard.add("⏪Back")
    
    cancel = ReplyKeyboardMarkup(resize_keyboard=True)
    cancel.add("❌Cancel")
    
    @bot.message_handler(commands=["admin"])
    def admin_panel(message):
        """Display admin panel"""
        admin = is_admin(message.chat.id)
        if message.from_user.id == OWNER_ID or admin is True:
            bot.send_message(
                message.chat.id,
                const.ADMIN_WELCOME,
                reply_markup=keyboard
            )
    
    # Search User Handler
    @bot.message_handler(func=lambda message: True, state="searchuser")
    def search_user(message):
        if message.text == "❌Cancel":
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id, const.CANCELLED_MESSAGE, reply_markup=keyboard)
        else:
            try:
                user_id = int(message.text)
                user = db.get_user(user_id)
                if user:
                    bot.delete_state(message.from_user.id, message.chat.id)
                    bot.send_message(
                        message.chat.id,
                        const.USER_FOUND_TEMPLATE.format(
                            is_admin=user['is_admin'],
                            is_banned=user['is_banned'],
                            is_premium=user['is_premium']
                        ),
                        reply_markup=keyboard
                    )
                else:
                    bot.send_message(message.chat.id, const.USER_NOT_FOUND, reply_markup=cancel)
            except Exception as e:
                bot.delete_state(message.from_user.id, message.chat.id)
                bot.send_message(message.chat.id, const.ERROR_TEMPLATE.format(error=e), reply_markup=keyboard)
    
    # Ban User Handler
    @bot.message_handler(func=lambda message: True, state="banuser")
    def ban_user(message):
        if message.text == "❌Cancel":
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id, const.CANCELLED_MESSAGE, reply_markup=keyboard)
        else:
            try:
                user_id = int(message.text)
                user = db.get_user(user_id)
                if not user:
                    return bot.send_message(message.chat.id, const.USER_NOT_IN_DB, reply_markup=cancel)
                
                if is_banned(user_id):
                    bot.send_message(message.chat.id, const.USER_ALREADY_BANNED, reply_markup=cancel)
                else:
                    db.update_user(user_id, {"is_banned": True, "is_admin": False, "is_premium": False})
                    bot.delete_state(message.from_user.id, message.chat.id)
                    bot.send_message(message.chat.id, const.USER_BANNED_SUCCESS, reply_markup=keyboard)
            except Exception as e:
                bot.delete_state(message.from_user.id, message.chat.id)
                bot.send_message(message.chat.id, const.ERROR_TEMPLATE.format(error=e), reply_markup=keyboard)
    
    # Unban User Handler
    @bot.message_handler(func=lambda message: True, state="unbanuser")
    def unban_user(message):
        if message.text == "❌Cancel":
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id, const.CANCELLED_MESSAGE, reply_markup=keyboard)
        else:
            try:
                user_id = int(message.text)
                if not is_banned(user_id):
                    bot.send_message(message.chat.id, const.USER_ALREADY_UNBANNED, reply_markup=cancel)
                else:
                    db.update_user(user_id, {"is_banned": False, "is_admin": False, "is_premium": False})
                    bot.delete_state(message.from_user.id, message.chat.id)
                    bot.send_message(message.chat.id, const.USER_UNBANNED_SUCCESS, reply_markup=keyboard)
            except Exception as e:
                bot.delete_state(message.from_user.id, message.chat.id)
                bot.send_message(message.chat.id, const.ERROR_TEMPLATE.format(error=e), reply_markup=keyboard)
    
    # Add Admin Handler
    @bot.message_handler(func=lambda message: True, state="adadmin")
    def add_admin(message):
        if message.text == "❌Cancel":
            bot.delete_state(message.from_user.id, message.chat.id)
            return bot.send_message(message.chat.id, const.CANCELLED_MESSAGE, reply_markup=keyboard)
        
        try:
            user_id = int(message.text)
            db.update_user(user_id, {"is_admin": True, "is_banned": False, "is_premium": True})
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id, const.USER_PROMOTED_ADMIN, reply_markup=keyboard)
            bot.send_message(user_id, const.USER_BECAME_ADMIN, reply_markup=keyboard)
        except Exception as e:
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id, const.ERROR_TEMPLATE.format(error=e), reply_markup=keyboard)
    
    # Delete Admin Handler
    @bot.message_handler(func=lambda message: True, state="deleteadmin")
    def delete_admin(message):
        if message.text == "❌Cancel":
            bot.delete_state(message.from_user.id, message.chat.id)
            return bot.send_message(message.chat.id, const.CANCELLED_MESSAGE, reply_markup=keyboard)
        
        try:
            user_id = int(message.text)
            db.update_user(user_id, {"is_admin": False, "is_banned": False, "is_premium": False})
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id, const.USER_DEMOTED_ADMIN, reply_markup=keyboard)
        except Exception as e:
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id, const.ERROR_TEMPLATE.format(error=e), reply_markup=keyboard)
    
    # Set Premium Handler
    @bot.message_handler(func=lambda message: True, state="setpremium")
    def set_premium(message):
        if message.text == "❌Cancel":
            bot.delete_state(message.from_user.id, message.chat.id)
            return bot.send_message(message.chat.id, const.CANCELLED_MESSAGE, reply_markup=keyboard)
        
        try:
            user_id = int(message.text)
            db.update_user(user_id, {"is_premium": True})
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id, const.USER_PREMIUM_GRANTED, reply_markup=keyboard)
            
            from keyboards import get_main_keyboard
            bot.send_message(user_id, const.USER_GOT_PREMIUM, reply_markup=get_main_keyboard())
        except Exception as e:
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id, const.ERROR_TEMPLATE.format(error=e), reply_markup=keyboard)
    
    # Remove Premium Handler
    @bot.message_handler(func=lambda message: True, state="demotepremium")
    def demote_premium(message):
        if message.text == "❌Cancel":
            bot.delete_state(message.from_user.id, message.chat.id)
            return bot.send_message(message.chat.id, const.CANCELLED_MESSAGE, reply_markup=keyboard)
        
        try:
            user_id = int(message.text)
            db.update_user(user_id, {"is_premium": False})
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id, const.USER_PREMIUM_REMOVED, reply_markup=keyboard)
            
            from keyboards import get_main_keyboard
            bot.send_message(user_id, const.USER_LOST_PREMIUM, reply_markup=get_main_keyboard())
        except Exception as e:
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id, const.ERROR_TEMPLATE.format(error=e), reply_markup=keyboard)
    
    return keyboard, cancel
