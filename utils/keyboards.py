from telebot.types import ReplyKeyboardMarkup

def get_main_keyboard():
    """Get main user keyboard"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📝CREATE POST", "📃HOW TO USE")
    return keyboard


def get_cancel_keyboard():
    """Get cancel keyboard"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("❌Cancel")
    return keyboard


def get_type_button_keyboard():
    """Get button type selection keyboard"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("NORMAL BUTTON", "📲LOGIN BUTTON")
    keyboard.add("🔙Back")
    return keyboard


def get_login_menu_keyboard():
    """Get login button menu keyboard"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("🗞TEXT", "📸PHOTO")
    keyboard.add("◀️Back")
    return keyboard


def get_options_keyboard():
    """Get post options keyboard"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add("📄TEXT", "📷PHOTO")
    keyboard.add("◀️Back")
    return keyboard


def get_caption_keyboard():
    """Get caption keyboard with skip option"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add("⏩NEVER MIND", "❌Cancel")
    return keyboard


def get_check_keyboard():
    """Get confirmation keyboard"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("✅YEAH", "❌NOPE")
    return keyboard
