import time
from telebot.types import ReplyKeyboardMarkup
from utils.database import db
from utils.keyboards import get_cancel_keyboard, get_check_keyboard
import utils.constants as const


def setup_broadcast_handlers(bot):
    """Setup all broadcast handlers"""
    
    @bot.message_handler(func=lambda message: True, state="sendwithphoto")
    def send_with_photo_text(message):
        """Handle text messages when expecting photo"""
        if message.text == "❌Cancel":
            from handlers.admin import setup_admin_handlers
            keyboard, _ = setup_admin_handlers(bot)
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id, const.CANCELLED_MESSAGE, reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, const.SEND_PHOTO_PROMPT, reply_markup=get_cancel_keyboard())
    
    @bot.message_handler(content_types=["photo"], state="sendwithphoto")
    def send_with_photo(message):
        """Handle photo broadcast preparation"""
        try:
            if message.caption is None:
                with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                    for i in message.photo:
                        pass
                    data['photo'] = i.file_id
                    data['caption'] = "None"
                    bot.set_state(message.from_user.id, "checkphoto")
                    bot.send_message(message.chat.id, const.BROADCAST_CONFIRM, reply_markup=get_check_keyboard())
            else:
                with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                    for i in message.photo:
                        pass
                    data['photo'] = i.file_id
                    data['caption'] = message.caption
                    bot.set_state(message.from_user.id, "checkphoto")
                    bot.send_message(message.chat.id, const.BROADCAST_CONFIRM, reply_markup=get_check_keyboard())
        except Exception as e:
            from handlers.admin import setup_admin_handlers
            keyboard, _ = setup_admin_handlers(bot)
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id, const.ERROR_TEMPLATE.format(error=e), reply_markup=keyboard)
    
    @bot.message_handler(func=lambda message: True, state="sendtext")
    def send_text(message):
        """Handle text broadcast preparation"""
        if message.text == "❌Cancel":
            from handlers.admin import setup_admin_handlers
            keyboard, _ = setup_admin_handlers(bot)
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id, const.CANCELLED_MESSAGE, reply_markup=keyboard)
        else:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['text'] = message.text
                bot.set_state(message.from_user.id, "checktxt", message.chat.id)
                bot.send_message(message.chat.id, const.BROADCAST_TEXT_CONFIRM, reply_markup=get_check_keyboard())
    
    @bot.message_handler(func=lambda message: True, state="checktxt")
    def check_txt(message):
        """Confirm and send text broadcast"""
        if message.text == "✅YEAH":
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                users = db.get_all_users()
                
                # Send progress notification
                bot.send_message(
                    message.chat.id,
                    f"📤 Broadcasting to {len(users)} users...\nThis may take a few moments."
                )
                
                # Broadcast with rate limiting
                success_count = 0
                failed_count = 0
                
                for user in users:
                    try:
                        bot.send_message(user["user_id"], data['text'])
                        success_count += 1
                        time.sleep(0.04)
                    except Exception as e:
                        failed_count += 1
                        continue
                
                from handlers.admin import setup_admin_handlers
                keyboard, _ = setup_admin_handlers(bot)
                
                report = f"✅ **Broadcast Complete**\n\n"
                report += f"✓ Successfully sent: {success_count}\n"
                if failed_count > 0:
                    report += f"✗ Failed: {failed_count}"
                
                bot.send_message(message.chat.id, report)
                bot.send_message(message.chat.id, const.MAIN_MENU_MESSAGE, reply_markup=keyboard)
            bot.delete_state(message.from_user.id, message.chat.id)
        
        if message.text == "❌NOPE":
            from handlers.admin import setup_admin_handlers
            keyboard, _ = setup_admin_handlers(bot)
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id, const.CANCELLED_MESSAGE, reply_markup=keyboard)
    
    @bot.message_handler(func=lambda message: True, state="checkphoto")
    def send_photo_only(message):
        """Confirm and send photo broadcast"""
        if message.text == "✅YEAH":
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                users = db.get_all_users()
                
                bot.send_message(
                    message.chat.id,
                    f"📤 Broadcasting to {len(users)} users...\nThis may take a few moments."
                )
                
                success_count = 0
                failed_count = 0
                
                if data['caption'] == "None":
                    for user in users:
                        try:
                            bot.send_photo(user["user_id"], data['photo'])
                            success_count += 1
                            time.sleep(0.04)
                        except Exception as e:
                            failed_count += 1
                            continue
                else:
                    for user in users:
                        try:
                            bot.send_photo(user["user_id"], data['photo'], caption=data['caption'])
                            success_count += 1
                            time.sleep(0.04)
                        except Exception as e:
                            failed_count += 1
                            continue
                
                from handlers.admin import setup_admin_handlers
                keyboard, _ = setup_admin_handlers(bot)
                
                report = f"✅ **Broadcast Complete**\n\n"
                report += f"✓ Successfully sent: {success_count}\n"
                if failed_count > 0:
                    report += f"✗ Failed: {failed_count}"
                
                bot.send_message(message.chat.id, report)
                bot.send_message(message.chat.id, const.MAIN_MENU_MESSAGE, reply_markup=keyboard)
            bot.delete_state(message.from_user.id, message.chat.id)
        
        if message.text == "❌NOPE":
            from handlers.admin import setup_admin_handlers
            keyboard, _ = setup_admin_handlers(bot)
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id, const.CANCELLED_MESSAGE, reply_markup=keyboard)
