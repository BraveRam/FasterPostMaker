from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, LoginUrl
from utils.keyboards import (
    get_cancel_keyboard, get_caption_keyboard, get_main_keyboard,
    get_type_button_keyboard
)
from utils.config import SHARE251_BOT
import utils.constants as const


def setup_post_handlers(bot):
    """Setup all post creation handlers"""
    
    # NORMAL BUTTON HANDLERS - TEXT POST
    @bot.message_handler(func=lambda message: True, state="link")
    def handle_link(message):
        """Handle link input for normal text post"""
        if message.text.startswith("https://"):
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['link'] = message.text
                bot.set_state(message.from_user.id, "caption", message.chat.id)
                return bot.send_message(
                    message.chat.id,
                    const.CAPTION_PROMPT,
                    reply_markup=get_cancel_keyboard()
                )
        if message.text == "❌Cancel":
            bot.delete_state(message.from_user.id, message.chat.id)
            return bot.send_message(message.chat.id, const.CHOOSE_BUTTON_TYPE, reply_markup=get_type_button_keyboard())
        else:
            bot.send_message(message.chat.id, const.INVALID_LINK)
    
    @bot.message_handler(func=lambda message: True, state="caption")
    def handle_caption(message):
        """Handle caption input for normal text post"""
        if message.text == "❌Cancel":
            bot.delete_state(message.from_user.id, message.chat.id)
            return bot.send_message(message.chat.id, const.CHOOSE_BUTTON_TYPE, reply_markup=get_type_button_keyboard())
        else:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['caption'] = message.text
                bot.set_state(message.from_user.id, "text", message.chat.id)
                bot.send_message(
                    message.chat.id,
                    const.BUTTON_TEXT_PROMPT,
                    reply_markup=get_cancel_keyboard()
                )
    
    @bot.message_handler(func=lambda message: True, state="text")
    def handle_text(message):
        """Handle button text input and create normal text post"""
        if message.text == "❌Cancel":
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id, const.CHOOSE_BUTTON_TYPE, reply_markup=get_type_button_keyboard())
        else:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                link1 = data['link']
                caption1 = data['caption']
                button_texts = message.text.split(",")
                buttons = [InlineKeyboardButton(text=text.strip(), url=link1.strip()) for text in button_texts]
                key = InlineKeyboardMarkup(row_width=1)
                key.add(*buttons)
                bot.send_message(chat_id=message.chat.id, text=caption1, reply_markup=key)
                bot.send_message(
                    message.chat.id,
                    f"{const.WELCOME_MESSAGE}",
                    reply_markup=get_main_keyboard()
                )
            bot.delete_state(message.from_user.id, message.chat.id)
    
    # NORMAL BUTTON HANDLERS - PHOTO POST
    @bot.message_handler(func=lambda message: True, state="linkphoto")
    def handle_linkphoto(message):
        """Handle link input for normal photo post"""
        if message.text.startswith("https://"):
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['link'] = message.text
                bot.set_state(message.from_user.id, "photo", message.chat.id)
                return bot.send_message(
                    message.chat.id,
                    const.PHOTO_PROMPT,
                    reply_markup=get_cancel_keyboard()
                )
        if message.text == "❌Cancel":
            bot.delete_state(message.from_user.id, message.chat.id)
            return bot.send_message(message.chat.id, const.CHOOSE_BUTTON_TYPE, reply_markup=get_type_button_keyboard())
        else:
            bot.send_message(message.chat.id, const.INVALID_LINK)
    
    @bot.message_handler(content_types=["photo"], state="photo")
    def handle_photo(message):
        """Handle photo input for normal photo post"""
        for i in message.photo:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['photo'] = i.file_id
                bot.set_state(message.from_user.id, "captionphoto", message.chat.id)
                return bot.send_message(
                    message.chat.id,
                    const.PHOTO_CAPTION_PROMPT,
                    reply_markup=get_caption_keyboard()
                )
    
    @bot.message_handler(func=lambda message: True, state="photo")
    def handle_phototext(message):
        """Handle text when expecting photo"""
        if message.text == "❌Cancel":
            bot.delete_state(message.from_user.id, message.chat.id)
            return bot.send_message(message.chat.id, const.CHOOSE_BUTTON_TYPE, reply_markup=get_type_button_keyboard())
        else:
            return bot.send_message(message.chat.id, const.PHOTO_SEND_PROMPT, reply_markup=get_cancel_keyboard())
    
    @bot.message_handler(func=lambda message: True, state="captionphoto")
    def handle_captionphoto(message):
        """Handle photo caption input"""
        if message.text == "❌Cancel":
            bot.delete_state(message.from_user.id, message.chat.id)
            return bot.send_message(message.chat.id, const.CHOOSE_BUTTON_TYPE, reply_markup=get_type_button_keyboard())
        if message.text == "⏩NEVER MIND":
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['caption'] = "None"
                bot.set_state(message.from_user.id, "textphoto", message.chat.id)
                bot.send_message(
                    message.chat.id,
                    const.BUTTON_TEXT_PROMPT,
                    reply_markup=get_cancel_keyboard()
                )
        else:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['caption'] = message.text
                bot.set_state(message.from_user.id, "textphoto", message.chat.id)
                bot.send_message(
                    message.chat.id,
                    const.BUTTON_TEXT_PROMPT,
                    reply_markup=get_cancel_keyboard()
                )
    
    @bot.message_handler(func=lambda message: True, state="textphoto")
    def handle_ftext(message):
        """Handle button text and create normal photo post"""
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            link2 = data['link']
            photo2 = data['photo']
            caption2 = data['caption']
            if caption2 == "None".strip():
                button_texts = message.text.split(",")
                buttons = [InlineKeyboardButton(text=text.strip(), url=link2.strip()) for text in button_texts]
                key = InlineKeyboardMarkup(row_width=1)
                key.add(*buttons)
                bot.send_photo(message.chat.id, photo2, reply_markup=key)
            else:
                button_texts = message.text.split(",")
                buttons = [InlineKeyboardButton(text=text.strip(), url=link2.strip()) for text in button_texts]
                key = InlineKeyboardMarkup(row_width=1)
                key.add(*buttons)
                bot.send_photo(message.chat.id, photo2, caption=caption2, reply_markup=key)
                bot.send_message(
                    message.chat.id,
                    const.WELCOME_MESSAGE,
                    reply_markup=get_main_keyboard()
                )
        bot.delete_state(message.from_user.id, message.chat.id)
    
    # LOGIN BUTTON HANDLERS - TEXT POST
    @bot.message_handler(func=lambda message: True, state="llink")
    def handle_ltext(message):
        """Handle link input for login text post"""
        if message.text.startswith("https://"):
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['llink'] = message.text
                bot.set_state(message.from_user.id, "ltext", message.chat.id)
                return bot.send_message(
                    message.chat.id,
                    const.TEXT_PROMPT,
                    reply_markup=get_cancel_keyboard()
                )
        if message.text == "❌Cancel":
            bot.delete_state(message.from_user.id, message.chat.id)
            return bot.send_message(message.chat.id, const.CHOOSE_BUTTON_TYPE, reply_markup=get_type_button_keyboard())
        else:
            bot.send_message(message.chat.id, const.INVALID_LINK_SIMPLE)
    
    @bot.message_handler(func=lambda message: True, state="ltext")
    def handle_lcaption(message):
        """Handle text input for login text post"""
        if message.text == "❌Cancel":
            bot.delete_state(message.from_user.id, message.chat.id)
            return bot.send_message(message.chat.id, const.CHOOSE_BUTTON_TYPE, reply_markup=get_type_button_keyboard())
        else:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['ltext'] = message.text
                bot.set_state(message.from_user.id, "lbtn", message.chat.id)
                bot.send_message(
                    message.chat.id,
                    const.BUTTON_TEXT_PROMPT,
                    reply_markup=get_cancel_keyboard()
                )
    
    @bot.message_handler(func=lambda message: True, state="lbtn")
    def handle_lltext(message):
        """Handle button text and create login text post"""
        if message.text == "❌Cancel":
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id, const.CHOOSE_BUTTON_TYPE, reply_markup=get_type_button_keyboard())
        else:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                link1 = data['llink']
                caption1 = data['ltext']
                button_texts = message.text.split(",")
                buttons = [
                    InlineKeyboardButton(text=text, login_url=LoginUrl(link1, bot_username=SHARE251_BOT))
                    for text in button_texts
                ]
                key = InlineKeyboardMarkup(row_width=1)
                key.add(*buttons)
                bot.send_message(chat_id=message.chat.id, text=caption1, reply_markup=key)
                bot.send_message(
                    message.chat.id,
                    const.WELCOME_MESSAGE,
                    reply_markup=get_main_keyboard()
                )
            bot.delete_state(message.from_user.id, message.chat.id)
    
    # LOGIN BUTTON HANDLERS - PHOTO POST
    
    @bot.message_handler(func=lambda message: True, state="lplink")
    def handle_lplinkphoto(message):
        """Handle link input for login photo post"""
        if message.text.startswith("https://"):
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['lplink'] = message.text
                bot.set_state(message.from_user.id, "lphoto", message.chat.id)
                return bot.send_message(
                    message.chat.id,
                    const.PHOTO_PROMPT,
                    reply_markup=get_cancel_keyboard()
                )
        if message.text == "❌Cancel":
            bot.delete_state(message.from_user.id, message.chat.id)
            return bot.send_message(message.chat.id, const.CHOOSE_BUTTON_TYPE, reply_markup=get_type_button_keyboard())
        else:
            bot.send_message(message.chat.id, const.INVALID_LINK_SIMPLE)
    
    @bot.message_handler(content_types=["photo"], state="lphoto")
    def handle_lphoto(message):
        """Handle photo input for login photo post"""
        for i in message.photo:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['lphoto'] = i.file_id
                bot.set_state(message.from_user.id, "lcaption", message.chat.id)
                return bot.send_message(
                    message.chat.id,
                    const.PHOTO_CAPTION_PROMPT,
                    reply_markup=get_caption_keyboard()
                )
    
    @bot.message_handler(func=lambda message: True, state="lphoto")
    def handle_lphototext(message):
        """Handle text when expecting photo"""
        if message.text == "❌Cancel":
            bot.delete_state(message.from_user.id, message.chat.id)
            return bot.send_message(message.chat.id, const.CHOOSE_BUTTON_TYPE, reply_markup=get_type_button_keyboard())
        else:
            return bot.send_message(message.chat.id, const.PHOTO_SEND_PROMPT, reply_markup=get_cancel_keyboard())
    
    @bot.message_handler(func=lambda message: True, state="lcaption")
    def handle_lpcaptionphoto(message):
        """Handle photo caption for login photo post"""
        if message.text == "❌Cancel":
            bot.delete_state(message.from_user.id, message.chat.id)
            return bot.send_message(message.chat.id, const.CHOOSE_BUTTON_TYPE, reply_markup=get_type_button_keyboard())
        if message.text == "⏩NEVER MIND":
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['lcaption'] = "None"
                bot.set_state(message.from_user.id, "lpbtn", message.chat.id)
                bot.send_message(
                    message.chat.id,
                    const.BUTTON_TEXT_PROMPT,
                    reply_markup=get_cancel_keyboard()
                )
        else:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['lcaption'] = message.text
                bot.set_state(message.from_user.id, "lpbtn", message.chat.id)
                bot.send_message(
                    message.chat.id,
                    const.BUTTON_TEXT_PROMPT,
                    reply_markup=get_cancel_keyboard()
                )
    
    @bot.message_handler(func=lambda message: True, state="lpbtn")
    def handle_lptextbtn(message):
        """Handle button text and create login photo post"""
        if message.text == "❌Cancel":
            bot.delete_state(message.from_user.id, message.chat.id)
            return bot.send_message(message.chat.id, const.CHOOSE_BUTTON_TYPE, reply_markup=get_type_button_keyboard())
        else:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                link4 = data['lplink']
                photo2 = data['lphoto']
                caption2 = data['lcaption']
                if caption2 == "None".strip():
                    button_texts = message.text.split(",")
                    buttons = [
                        InlineKeyboardButton(text=text, login_url=LoginUrl(link4, bot_username=SHARE251_BOT))
                        for text in button_texts
                    ]
                    key = InlineKeyboardMarkup(row_width=1)
                    key.add(*buttons)
                    bot.send_photo(message.chat.id, photo2, reply_markup=key)
                    bot.send_message(
                        message.chat.id,
                        const.WELCOME_MESSAGE,
                        reply_markup=get_main_keyboard()
                    )
                else:
                    button_texts = message.text.split(",")
                    buttons = [
                        InlineKeyboardButton(text=text, login_url=LoginUrl(link4, bot_username=SHARE251_BOT))
                        for text in button_texts
                    ]
                    key = InlineKeyboardMarkup(row_width=1)
                    key.add(*buttons)
                    bot.send_photo(message.chat.id, photo2, caption=caption2, reply_markup=key)
                    bot.send_message(
                        message.chat.id,
                        const.WELCOME_MESSAGE,
                        reply_markup=get_main_keyboard()
                    )
            bot.delete_state(message.from_user.id, message.chat.id)
    
    # GET LINK FROM SHARE251 BOT
    
    @bot.message_handler(commands=["link251"])
    def get_links(message):
        """Command to get share251bot link"""
        from utils.user_manager import is_banned
        
        banned = is_banned(message.from_user.id)
        if banned is True:
            return bot.send_message(message.chat.id, const.BANNED_MESSAGE)
        else:
            bot.set_state(message.from_user.id, "get_link", message.chat.id)
            bot.send_message(
                message.chat.id,
                const.SHARE251_PROMPT,
                reply_markup=get_cancel_keyboard()
            )
    
    @bot.message_handler(content_types=["photo"], state="get_link")
    def handle_getLink(message):
        """Extract link from share251bot post"""
        try:
            for i in message.reply_markup.keyboard:
                for x in i:
                    bot.send_message(
                        message.chat.id,
                        const.SHARE251_LINK_TEMPLATE.format(link=x.url),
                        disable_web_page_preview=True
                    )
                    bot.delete_state(message.from_user.id, message.chat.id)
                    bot.send_message(
                        message.chat.id,
                        const.WELCOME_MESSAGE,
                        reply_markup=get_main_keyboard()
                    )
        except:
            bot.send_message(
                message.chat.id,
                const.SHARE251_INVALID,
                reply_markup=get_cancel_keyboard()
            )
    
    @bot.message_handler(func=lambda message: True, state="get_link")
    def handle_getLinks(message):
        """Handle other messages in get_link state"""
        if message.text == "❌Cancel":
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.send_message(
                message.chat.id,
                const.WELCOME_MESSAGE,
                reply_markup=get_main_keyboard()
            )
        else:
            bot.send_message(message.chat.id, const.SHARE251_RETRY)