import telebot
from telebot.types import *
from telebot import custom_filters
from pymongo import MongoClient 

client = MongoClient("mongodb+srv://really651:gSPMW6u9WuStXIwD@cluster0.pxc2foz.mongodb.net/?retryWrites=true&w=majority")

db = client["FastPostMakerBot"]
collection = db["promo"]


bot = telebot.TeleBot("6062326465:AAHezYHb8bs_X4q3UCXgb0ZMTxAdRlxseRc", parse_mode="html")

owner = [1365625365]

keyboards = ReplyKeyboardMarkup(resize_keyboard = True)
keyboards.add("📝CREATE POST", "📃HOW TO USE")
keyboards.add("📢PROJECT CHANNEL")


def user_exists(user_id):
	user = collection.find_one({"user_id": user_id})
	if user:
		return True
	else:
		bot.send_message(user_id, "👋Hello! This Bot Helps You To Create Promotions With A Simple Steps!\nSelect An Option Below:", reply_markup = keyboards)
		return collection.insert_one({"user_id": user_id, "is_admin": False, "is_banned": False, "is_premium": False})

@bot.chat_join_request_handler(func=lambda message: True)
def join_request(message):  
    user_id = message.from_user.id 
    user = collection.find_one({"user_id": user_id})
    if user:    	
    	bot.approve_chat_join_request(message.chat.id, message.from_user.id)
    	bot.send_message(message.from_user.id, "👋Hello! This Bot Helps You To Create Promotions With A Simple Steps!\nSelect An Option Below:", reply_markup = keyboards)
    else:
    	bot.approve_chat_join_request(message.chat.id, message.from_user.id)
    	collection.insert_one({"user_id": user_id, "is_admin": False, "is_banned": False, "is_premium": False})
    	bot.send_message(message.from_user.id, "👋Hello! This Bot Helps You To Create Promotions With A Simple Steps!\nSelect An Option Below:", reply_markup = keyboards)

def is_admin(user_id):
	user = collection.find_one({"user_id": user_id})
	if user["is_admin"] == True:
		return True
		
def is_banned(user_id):
	user = collection.find_one({"user_id": user_id})
	if user:
		if user["is_banned"] == True:
			return True

def is_premium(user_id):
	user = collection.find_one({"user_id": user_id})
	if user:
		if user["is_premium"] == True:
			return True
			
channelbtn = InlineKeyboardMarkup()
ch = InlineKeyboardButton(text ="✅JOIN CHANNEL", url="t.me/mt_projectz")
channelbtn.add(ch)


keyboard = ReplyKeyboardMarkup(resize_keyboard = True, row_width=3, input_field_placeholder="Admin Menu")
keyboard.add("🔎Search User🔍", "⛔Ban User⛔", "🤓Unban User🤓", "📢Broadcast📢", "👮‍♂️Add Admin👮‍♂️", "✖️Delete Admin✖️", "👨‍✈️Admin(s)👨‍✈️", "📊Statstics📊", "🎁Set Premium🎁", "🎈Remove Premium🎈")
keyboard.add("⏪Back")

@bot.message_handler(commands =["admin"])
def admin_panel(message):	
	admin = is_admin(message.chat.id)
	if message.from_user.id in owner or admin is True:		
		bot.send_message(message.chat.id, "😎Welcome to ADMIN PANEL:)\nChoose an option below:)", reply_markup = keyboard)
	
def check_sub(message):	
	a =  bot.get_chat_member("@mt_projectz", message.from_user.id)
	if a.status == "left":
		return False
	else:
		return True

get_link = "get_link"

canc = ReplyKeyboardMarkup(resize_keyboard = True)
canc.add("❌Cancel")

@bot.message_handler(commands =["link251"])
def get_links(message):
	check = check_sub(message)
	banned = is_banned(message.from_user.id)
	if check== False:
	   return bot.send_message(message.chat.id, "⚠️Before using this bot, You need to be a member of My Updates Channel⚠️", reply_markup = sub)
	else:
		if banned is True:
			return bot.send_message(message.chat.id, "⚠️You Have Been Banned:(")
		else:
			bot.set_state(message.from_user.id, get_link, message.chat.id)
			bot.send_message(message.chat.id, "Incredible, Now send me your post from @share251bot then i\'ll give you, your own link!", reply_markup = canc)

@bot.message_handler(content_types =["photo"], state=get_link)
def handle_getLink(message):	
	try:
		for i in message.reply_markup.keyboard:
		  		for x in i:
		  			bot.send_message(message.chat.id, f"Here is your own link: \n\n<code>{x.url}</code>", disable_web_page_preview=True)
		  			bot.delete_state(message.from_user.id, message.chat.id) 
		  			bot.send_message(message.chat.id, f"👋Hey {message.from_user.first_name}! \n\nThis bot can help you to make promotion/post simply:", reply_markup = keyboards)
	except:
		bot.send_message(message.chat.id, "It seems that you have not sent me correct info! Try Again!", reply_markup = canc)

@bot.message_handler(func = lambda message: True, state=get_link)
def handle_getLinks(message):
	if message.text =="❌Cancel":
		bot.delete_state(message.from_user.id, message.chat.id) 
		bot.send_message(message.chat.id, f"👋Hey {message.from_user.first_name}! \n\nThis bot can help you to make promotion/post simply:", reply_markup = keyboards)
	else:
		bot.send_message(message.chat.id, "Please send me your post from @share251bot!")
	
link = "link"
caption = "caption"
text = "text"

linkphoto = "linkphoto"
photo = "photo"
captionphoto = "captionphoto"
textphoto = "textphoto"


help = """
This helps you to make promotion with Normal buttons and Login Buttons(@Share251bot) on this telegram. And its super easy and Time saver bot! So You can make your promotions easily with this bot!
"""
project = """
This bot is developed by @MT_Projectz
Join and Get Updates of This Bot!
"""
typebtn = ReplyKeyboardMarkup(resize_keyboard = True)
typebtn.add("NORMAL BUTTON", "📲LOGIN BUTTON")
typebtn.add("🔙Back")

channel = InlineKeyboardMarkup()
ch1 = InlineKeyboardButton(text ="📢PROJECTS CHANNEL", url="t.me/mt_projectz")
channel.add(ch1)

sub = InlineKeyboardMarkup()
k = InlineKeyboardButton(text ="☑️ Join My Updates", url="t.me/mt_projectz")
sub.add(k)

@bot.message_handler(commands =["start"])
def start(message):
	user_id = message.from_user.id 
	users = user_exists(user_id)
	banned = is_banned(user_id)
	check = check_sub(message)
	if users is True:
		if banned is True:			
			bot.send_message(message.chat.id, "⚠️You Have Been Banned:(")
		else:
			if check == False:
				bot.send_message(message.chat.id, "⚠️Before using this bot, You need to be a member of My Updates Channel⚠️", reply_markup = sub)
			else:
				bot.send_message(message.chat.id, f"👋Hey {message.from_user.first_name}! \n\nThis bot can help you to make promotion/post simply:", reply_markup = keyboards)			

	
cancel = ReplyKeyboardMarkup(resize_keyboard = True)
cancel.add("❌Cancel")

@bot.message_handler(func = lambda message: True, state=link)
def handle_link(message):
	if message.text.startswith("https://") or message.text.startswith("https://"):
		with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
			data['link'] = message.text
			bot.set_state(message.from_user.id, caption, message.chat.id)
			return bot.send_message(message.chat.id, "Great! Send me your caption for your promotion:", reply_markup = cancel)
	if message.text =="❌Cancel":
		bot.delete_state(message.from_user.id, message.chat.id)
		return bot.send_message(message.chat.id, "Choose the type of button:", reply_markup = typebtn)
	else:
		bot.send_message(message.chat.id, "Invalid link! Please provide valid link\nNB: Make sure it starts with <i>https</i>:")

@bot.message_handler(func = lambda message: True, state=caption)
def handle_caption(message):
	if message.text =="❌Cancel":
		bot.delete_state(message.from_user.id, message.chat.id)
		return bot.send_message(message.chat.id, "Choose the type of button:", reply_markup = typebtn)
	else:
		with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
			data['caption'] = message.text 
			bot.set_state(message.from_user.id, text, message.chat.id)
			bot.send_message(message.chat.id, "Finally, Send me your Text for your buttons! for eg: <code>Join, Share</code>", parse_mode="html", reply_markup = cancel)

@bot.message_handler(func = lambda message: True, state=text)
def handle_text(message):
	if message.text == "❌Cancel":
		bot.delete_state(message.from_user.id, message.chat.id)
		bot.send_message(message.chat.id, "Choose the type of button:", reply_markup = typebtn)
	else:
		with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
			link1 = data['link']
			caption1 = data['caption']
			button_texts = message.text.split(",")
			buttons = [InlineKeyboardButton(text = text.strip(), url=link1.strip()) for text in button_texts]
			key = InlineKeyboardMarkup(row_width=1)
			key.add(*buttons)
			bot.send_message(chat_id=message.chat.id, text=caption1, reply_markup=key)
			bot.send_message(message.chat.id, f"👋Hey {message.from_user.first_name}! \n\nThis bot can help you to make promotion/post simply:", reply_markup = keyboards)
		bot.delete_state(message.from_user.id, message.chat.id)

@bot.message_handler(func = lambda message: True, state=linkphoto)
def handle_linkphoto(message):	
	if message.text.startswith("https://") or message.text.startswith("https://"):
		with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
			data['link'] = message.text
			bot.set_state(message.from_user.id, photo, message.chat.id)
			return bot.send_message(message.chat.id, "Great! Send me your photo for your promotion:", reply_markup = cancel)
	if message.text =="❌Cancel":
		bot.delete_state(message.from_user.id, message.chat.id)
		return bot.send_message(message.chat.id, "Choose the type of button:", reply_markup = typebtn)
	else:
		bot.send_message(message.chat.id, "Invalid link! Please provide valid link\nNB: Make sure it starts with <i>https</i>:")

@bot.message_handler(content_types =["photo"], state=photo)
def handle_photo(message):
	cap = ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
	cap.add("⏩NEVER MIND", "❌Cancel")
	for i in message.photo:
		with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
			data['photo'] = i.file_id
			bot.set_state(message.from_user.id, captionphoto, message.chat.id)
			return bot.send_message(message.chat.id, "Now, Send me the photo caption(optional):", reply_markup=cap)

@bot.message_handler(func = lambda message: True, state=photo)
def handle_phototext(message):	
	if message.text =="❌Cancel":
		bot.delete_state(message.from_user.id, message.chat.id)
		return bot.send_message(message.chat.id, "Choose the type of button:", reply_markup = typebtn)
	else:
		return bot.send_message(message.chat.id, "Please Send your photo for your promotion:", reply_markup = cancel)

@bot.message_handler(func = lambda message: True, state=captionphoto)
def handle_captionphoto(message):
	if message.text =="❌Cancel":
		bot.delete_state(message.from_user.id, message.chat.id)
		return bot.send_message(message.chat.id, "Choose the type of button:", reply_markup = typebtn)
	if message.text =="⏩NEVER MIND":
		with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
			data['caption'] = "None"
			bot.set_state(message.from_user.id, textphoto, message.chat.id)
			bot.send_message(message.chat.id, "Finally, Send me your Text for your buttons! for eg: <code>Join, Share</code>", parse_mode="html", reply_markup = cancel)
	else:
		with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
			data['caption'] = message.text 
			bot.set_state(message.from_user.id, textphoto, message.chat.id)
			bot.send_message(message.chat.id, "Finally, Send me your Text for your buttons! for eg: <code>Join, Share</code>", parse_mode="html", reply_markup = cancel)

@bot.message_handler(func = lambda message: True, state=textphoto)
def handle_ftext(message):
	with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
		link2 = data['link']
		photo2 = data['photo']
		caption2 = data['caption']
		if caption2 == "None".strip():
			button_texts = message.text.split(",")
			buttons = [InlineKeyboardButton(text = text.strip(), url=link2.strip()) for text in button_texts]
			key = InlineKeyboardMarkup(row_width=1)
			key.add(*buttons)
			bot.send_photo(message.chat.id, photo2, reply_markup = key)
		else:
			button_texts = message.text.split(",")
			buttons = [InlineKeyboardButton(text = text.strip(), url=link2.strip()) for text in button_texts]
			key = InlineKeyboardMarkup(row_width=1)
			key.add(*buttons)
			bot.send_photo(message.chat.id, photo2, caption = caption2, reply_markup = key)			
			bot.send_message(message.chat.id, f"👋Hey {message.from_user.first_name}! \n\nThis bot can help you to make promotion/post simply:", reply_markup = keyboards)
	bot.delete_state(message.from_user.id, message.chat.id)

loginmenu = ReplyKeyboardMarkup(resize_keyboard = True)
loginmenu.add("🗞TEXT", "📸PHOTO")
loginmenu.add("◀️Back")

llink = "llink"
ltext = "ltext"
lbtn = "lbtn"
	
@bot.message_handler(func = lambda message: True, state=llink)
def handle_ltext(message):
	if message.text.startswith("https://") or message.text.startswith("https://"):
		with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
			data['llink'] = message.text
			bot.set_state(message.from_user.id, ltext, message.chat.id)
			return bot.send_message(message.chat.id, "Great! Send me your text for your promotion:", reply_markup = cancel)
	if message.text =="❌Cancel":
		bot.delete_state(message.from_user.id, message.chat.id)
		return bot.send_message(message.chat.id, "Choose the type of button:", reply_markup = typebtn)
	else:
		bot.send_message(message.chat.id, "Invalid link! Please provide valid link:")
	
@bot.message_handler(func = lambda message: True, state=ltext)
def handle_lcaption(message):
	if message.text =="❌Cancel":
		bot.delete_state(message.from_user.id, message.chat.id)
		return bot.send_message(message.chat.id, "Choose the type of button:", reply_markup = typebtn)
	else:
		with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
			data['ltext'] = message.text 
			bot.set_state(message.from_user.id, lbtn, message.chat.id)
			bot.send_message(message.chat.id, "Finally, Send me your Text for your buttons! for eg: <code>Join, Share</code>", parse_mode="html", reply_markup = cancel)

@bot.message_handler(func = lambda message: True, state=lbtn)
def handle_lltext(message):
	if message.text == "❌Cancel":
		bot.delete_state(message.from_user.id, message.chat.id)
		bot.send_message(message.chat.id, "Choose the type of button:", reply_markup = typebtn)
	else:
		with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
			link1 = data['llink']
			caption1 = data['ltext']		
			button_texts = message.text.split(",")
			buttons = [InlineKeyboardButton(text = text, login_url=LoginUrl(link1, bot_username="@share251bot")) for text in button_texts]
			key = InlineKeyboardMarkup(row_width=1)
			key.add(*buttons)
			bot.send_message(chat_id=message.chat.id, text=caption1, reply_markup=key)
			bot.send_message(message.chat.id, f"👋Hey {message.from_user.first_name}! \n\nThis bot can help you to make promotion/post simply:", reply_markup = keyboard)
		bot.delete_state(message.from_user.id, message.chat.id)

lplink = "lplink"
lphoto = "lphoto"
lcaption = "lcaption"
lpbtn = "lpbtn"

@bot.message_handler(func = lambda message: True, state=lplink)
def handle_lplinkphoto(message):	
	if message.text.startswith("https://") or message.text.startswith("https://"):
		with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
			data['lplink'] = message.text
			bot.set_state(message.from_user.id, lphoto, message.chat.id)
			return bot.send_message(message.chat.id, "Great! Send me your photo for your promotion:", reply_markup = cancel)
	if message.text =="❌Cancel":
		bot.delete_state(message.from_user.id, message.chat.id)
		return bot.send_message(message.chat.id, "Choose the type of button:", reply_markup = typebtn)
	else:
		bot.send_message(message.chat.id, "Invalid link! Please provide valid link:")

@bot.message_handler(content_types =["photo"], state=lphoto)
def handle_lphoto(message):
	cap = ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
	cap.add("⏩NEVER MIND", "❌Cancel")
	for i in message.photo:
		with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
			data['lphoto'] = i.file_id
			bot.set_state(message.from_user.id, lcaption, message.chat.id)
			return bot.send_message(message.chat.id, "Now, Send me the photo caption(optional):", reply_markup=cap)

@bot.message_handler(func = lambda message: True, state=lphoto)
def handle_lphototext(message):	
	if message.text =="❌Cancel":
		bot.delete_state(message.from_user.id, message.chat.id)
		return bot.send_message(message.chat.id, "Choose the type of button:", reply_markup = typebtn)
	else:
		return bot.send_message(message.chat.id, "Please Send your photo for your promotion:", reply_markup = cancel)

@bot.message_handler(func = lambda message: True, state=lcaption)
def handle_lpcaptionphoto(message):
	if message.text =="❌Cancel":
		bot.delete_state(message.from_user.id, message.chat.id)
		return bot.send_message(message.chat.id, "Choose the type of button:", reply_markup = typebtn)
	if message.text =="⏩NEVER MIND":
		with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
			data['lcaption'] = "None"
			bot.set_state(message.from_user.id, lpbtn, message.chat.id)
			bot.send_message(message.chat.id, "Finally, Send me your Text for your buttons! for eg: <code>Join, Share</code>", parse_mode="html", reply_markup = cancel)
	else:
		with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
			data['lcaption'] = message.text 
			bot.set_state(message.from_user.id, lpbtn, message.chat.id)
			bot.send_message(message.chat.id, "Finally, Send me your Text for your buttons! for eg: <code>Join, Share</code>", parse_mode="html", reply_markup = cancel)

@bot.message_handler(func = lambda message: True, state=lpbtn)
def handle_lptextbtn(message):
	if message.text =="❌Cancel":
		bot.delete_state(message.from_user.id, message.chat.id)
		return bot.send_message(message.chat.id, "Choose the type of button:", reply_markup = typebtn) 
	else:
		pass
	with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
		link4 = data['lplink']
		photo2 = data['lphoto']
		caption2 = data['lcaption']
		if caption2 == "None".strip():
			button_texts = message.text.split(",")
			buttons = [InlineKeyboardButton(text = text, login_url=LoginUrl(link4, bot_username="@share251bot")) for text in button_texts]
			key = InlineKeyboardMarkup(row_width=1)
			key.add(*buttons)
			bot.send_photo(message.chat.id, photo2, reply_markup = key)
			bot.send_message(message.chat.id, f"👋Hey {message.from_user.first_name}! \n\nThis bot can help you to make promotion/post simply:", reply_markup = keyboard)
		else:
			button_texts = message.text.split(",")
			buttons = [InlineKeyboardButton(text = text, login_url=LoginUrl(link4, bot_username="@share251bot")) for text in button_texts]
			key = InlineKeyboardMarkup(row_width=1)
			key.add(*buttons)
			bot.send_photo(message.chat.id, photo2, caption = caption2, reply_markup = key)			
			bot.send_message(message.chat.id, f"👋Hey {message.from_user.first_name}! \n\nThis bot can help you to make promotion/post simply:", reply_markup = keyboards)
	bot.delete_state(message.from_user.id, message.chat.id)

searchuser = "searchuser"

@bot.message_handler(func = lambda message: True, state=searchuser)
def search_user(message):
	cancel = ReplyKeyboardMarkup(resize_keyboard = True)
	cancel.add("❌Cancel")
	if message.text =="❌Cancel":
		bot.delete_state(message.from_user.id, message.chat.id)
		bot.send_message(message.chat.id, "❌Cancelled", reply_markup=keyboard)
	else:		
		try:
			id = int(message.text)
			user = collection.find_one({"user_id": id})
			if user:
				bot.delete_state(message.from_user.id, message.chat.id)
				is_admins = user["is_admin"]
				is_premiumm = user["is_premium"]
				is_bannedd = user["is_banned"]
				bot.send_message(message.chat.id, f"User Found:)\n\nIs Admin: {is_admins}\nIs Banned: {is_bannedd}\nIs Premium: {is_premiumm}", reply_markup = keyboard)
			else:
				bot.send_message(message.chat.id, "No User Found!(404)", reply_markup = cancel) 
		except Exception as e:
			bot.delete_state(message.from_user.id, message.chat.id)
			bot.send_message(message.chat.id, f"⚠️ERROR: {e}", reply_markup = keyboard)

cancel = ReplyKeyboardMarkup(resize_keyboard = True)
cancel.add("❌Cancel")

@bot.message_handler(func = lambda message: True, state="banuser")
def ban_user(message):	
	if message.text =="❌Cancel":
		bot.delete_state(message.from_user.id, message.chat.id)
		bot.send_message(message.chat.id, "❌Cancelled", reply_markup=keyboard)
	else:
		try:
			user = collection.find_one({"user_id": int(message.text)})
			if not user:
				return bot.send_message(message.chat.id, "This User Doesnot Exist In DataBase!", reply_markup = cancel)
			else:
				pass
			id = int(message.text)
			banned = is_banned(id)
			if banned is True:
				bot.send_message(message.chat.id, "This User is Already Banned:(", reply_markup = cancel)
			else:
				collection.update_one({"user_id": id}, {"$set" : {"is_banned": True, "is_admin": False, "is_premium": False}})
				bot.delete_state(message.from_user.id, message.chat.id)
				bot.send_message(message.chat.id, "This User Has Successfully Been Banned:(", reply_markup = keyboard)
		except Exception as e:
			bot.delete_state(message.from_user.id, message.chat.id)
			bot.send_message(message.chat.id, f"⚠️ERROR: {e}", reply_markup = keyboard)

@bot.message_handler(func = lambda message: True, state="unbanuser")
def unban_user(message):	
	if message.text =="❌Cancel":
		bot.delete_state(message.from_user.id, message.chat.id)
		bot.send_message(message.chat.id, "❌Cancelled", reply_markup=keyboard)
	else:
		try:
			id = int(message.text)
			banned = is_banned(id)
			if banned is not True:
				bot.send_message(message.chat.id, "This User is Already UNBanned:(", reply_markup = cancel)
			else:
				collection.update_one({"user_id": id}, {"$set" : {"is_banned": False, "is_admin": False, "is_premium": False}})
				bot.delete_state(message.from_user.id, message.chat.id)
				bot.send_message(message.chat.id, "This User Has Successfully Been UNBanned:(", reply_markup = keyboard)
		except Exception as e:
			bot.delete_state(message.from_user.id, message.chat.id)
			bot.send_message(message.chat.id, f"⚠️ERROR: {e}", reply_markup = keyboard)

@bot.message_handler(func = lambda message: True, state="sendwithphoto")
def send_withPhotoT(message):
	if message.text =="❌Cancel":
		bot.delete_state(message.from_user.id, message.chat.id)
		bot.send_message(message.chat.id, "❌Cancelled", reply_markup=keyboard)
	else:
		bot.send_message(message.chat.id, "Dumb! Send A Photo:)", reply_markup=keyboard)
	
check = ReplyKeyboardMarkup(resize_keyboard = True)
check.add("✅YEAH", "❌NOPE")

@bot.message_handler(content_types =["photo"], state="sendwithphoto")
def send_withPhoto(message):	
	try:
		if message.caption is None:
			with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
				for i in message.photo:
					pass	
				data['photo'] = i.file_id
				data['caption'] = "None"
				bot.set_state(message.from_user.id, "checkphoto")
				bot.send_message(message.chat.id, "Are you sure to send the message:)", reply_markup = check)
		else:
			with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
				for i in message.photo:
					pass	
				data['photo'] = i.file_id
				data['caption'] = message.caption 
				bot.set_state(message.from_user.id, "checkphoto")
				bot.send_message(message.chat.id, "Are you sure to send the message:)", reply_markup = check)
	except Exception as e:
		bot.delete_state(message.from_user.id, message.chat.id)
		bot.send_message(message.chat.id, f"⚠️ERROR: {e}", reply_markup = keyboard)
	
@bot.message_handler(func = lambda message: True, state="sendtext")
def send_text(message):
	if message.text =="❌Cancel":
		bot.delete_state(message.from_user.id, message.chat.id)
		bot.send_message(message.chat.id, "❌Cancelled", reply_markup=keyboard)
	else:
		with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
			data['text'] = message.text
			bot.set_state(message.from_user.id, "checktxt", message.chat.id)
			bot.send_message(message.chat.id, "Are you sure to broadcast:)", reply_markup = check)

@bot.message_handler(func = lambda message: True, state="checktxt")
def check_txt(message):
	if message.text =="✅YEAH":
		with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
			users = collection.find({})
			for i in users:
				a = i["user_id"]
				bot.send_message(a, data['text'], reply_markup = channelbtn)
			bot.send_message(message.chat.id, "Successfully Broadcasted!")
			bot.send_message(message.chat.id, "MAIN MENU", reply_markup = keyboard)
		bot.delete_state(message.from_user.id, message.chat.id)
	if message.text =="❌NOPE":
		bot.delete_state(message.from_user.id, message.chat.id)
		bot.send_message(message.chat.id, "❌Cancelled", reply_markup=keyboard)

@bot.message_handler(func = lambda message: True, state="checkphoto")
def send_photo_only(message):
	if message.text =="✅YEAH":
		with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
			if data['caption'] == "None":
				users = collection.find({})
				for i in users:
					a = i["user_id"]
					bot.send_photo(a, data['photo'], reply_markup = channelbtn)
				bot.send_message(message.chat.id, "Successfully Broadcasted!")
				bot.send_message(message.chat.id, "MAIN MENU", reply_markup = keyboard)
			else:
				users = collection.find({})
				for i in users:
					a = i["user_id"]
					bot.send_photo(a, data['photo'], caption = data['caption'], reply_markup = channelbtn)
				bot.send_message(message.chat.id, "Successfully Broadcasted!")
				bot.send_message(message.chat.id, "MAIN MENU", reply_markup = keyboard)
		bot.delete_state(message.from_user.id, message.chat.id)
	if message.text =="❌NOPE":
		bot.delete_state(message.from_user.id, message.chat.id)
		bot.send_message(message.chat.id, "❌Cancelled", reply_markup=keyboard)

@bot.message_handler(func = lambda message: True, state="adadmin")
def add_admin(message):
	user = user_exists(message.chat.id)
	if message.text =="❌Cancel":
		bot.delete_state(message.from_user.id, message.chat.id)
		return bot.send_message(message.chat.id, "❌Cancelled", reply_markup=keyboard)
	else:
		pass
	if user:
		try:
			id = int(message.text)
			collection.update_one({"user_id": id}, {"$set": {"is_admin": True, "is_banned": False, "is_premium": True}})
			bot.delete_state(message.from_user.id, message.chat.id)
			bot.send_message(message.chat.id, "Successfully Promoted✅", reply_markup = keyboard)
			bot.send_message(id, "You Have Successfully Been Admin!", reply_markup = keyboard)
		except Exception as e:
			bot.delete_state(message.from_user.id, message.chat.id)
			bot.send_message(message.chat.id, f"⚠️ERROR: {e}", reply_markup = keyboard)

@bot.message_handler(func = lambda message: True, state="deleteadmin")
def delete_admin(message):
	user = user_exists(message.chat.id)
	if message.text =="❌Cancel":
		bot.delete_state(message.from_user.id, message.chat.id)
		return bot.send_message(message.chat.id, "❌Cancelled", reply_markup=keyboard)
	else:
		pass
	if user:
		try:
			id = int(message.text)
			collection.update_one({"user_id": id}, {"$set": {"is_admin": False, "is_banned": False, "is_premium": False}})
			bot.delete_state(message.from_user.id, message.chat.id)
			bot.send_message(message.chat.id, "Successfully demoted✅", reply_markup = keyboard)			
		except Exception as e:
			bot.delete_state(message.from_user.id, message.chat.id)
			bot.send_message(message.chat.id, f"⚠️ERROR: {e}", reply_markup = keyboard)

@bot.message_handler(func = lambda message: True, state="setpremium")
def set_premium(message):
	user = user_exists(message.chat.id)
	if message.text =="❌Cancel":
		bot.delete_state(message.from_user.id, message.chat.id)
		return bot.send_message(message.chat.id, "❌Cancelled", reply_markup=keyboard)
	else:
		pass
	if user:
		try:
			id = int(message.text)
			collection.update_one({"user_id": id}, {"$set":  {"is_premium": True}})
			bot.delete_state(message.from_user.id, message.chat.id)
			bot.send_message(message.chat.id, "This user has been premium user✅", reply_markup = keyboard)
			bot.send_message(id, "You Have Successfully Got Your Premium Account🎁", reply_markup = keyboards)
		except Exception as e:
			bot.delete_state(message.from_user.id, message.chat.id)
			bot.send_message(message.chat.id, f"⚠️ERROR: {e}", reply_markup = keyboard)

@bot.message_handler(func = lambda message: True, state="demotepremium")
def demote_premium(message):
	user = user_exists(message.chat.id)
	if message.text =="❌Cancel":
		bot.delete_state(message.from_user.id, message.chat.id)
		return bot.send_message(message.chat.id, "❌Cancelled", reply_markup=keyboard)
	else:
		pass
	if user:
		try:
			id = int(message.text)
			collection.update_one({"user_id": id}, {"$set":  {"is_premium": False}})
			bot.delete_state(message.from_user.id, message.chat.id)
			bot.send_message(message.chat.id, "This user has been Free user✅", reply_markup = keyboard)
			bot.send_message(id, "You Have Successfully Lost Your Premium Account😒", reply_markup = keyboards)
		except Exception as e:
			bot.delete_state(message.from_user.id, message.chat.id)
			bot.send_message(message.chat.id, f"⚠️ERROR: {e}", reply_markup = keyboard)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    check = check_sub(message)
    banned = is_banned(message.from_user.id)
    user = user_exists(message.chat.id)
    admin = is_admin(message.chat.id)
    if message.from_user.id in owner or admin is True:
    	if message.text =="🔎Search User🔍":
    		bot.set_state(message.from_user.id, searchuser, message.chat.id)
    		return bot.send_message(message.chat.id, "Cool, Send me USER_ID:)", reply_markup = cancel)
    	if message.text =="⛔Ban User⛔":
    		bot.set_state(message.from_user.id, "banuser", message.chat.id)
    		return bot.send_message(message.chat.id, "Cool, Send me USER_ID:)", reply_markup = cancel)
    	if message.text =="🤓Unban User🤓":
    		bot.set_state(message.from_user.id, "unbanuser", message.chat.id)
    		return bot.send_message(message.chat.id, "Cool, Send me USER_ID:)", reply_markup = cancel)
    	if message.text == "📢Broadcast📢":
    		choosebtn = ReplyKeyboardMarkup(resize_keyboard = True)
    		choosebtn.add("✨TEXT", "🏄‍♂️PHOTO")
    		choosebtn.add("❌Cancel")
    		return bot.send_message(message.chat.id, "Choose the type of Broadast:)\nWith Photo or Text:)", reply_markup = choosebtn)
    	if message.text == "⏪Back":
    		bot.delete_state(message.from_user.id, message.chat.id)
    		return bot.send_message(message.chat.id, "MAIN MENU", reply_markup = keyboards)
    	if message.text =="🏄‍♂️PHOTO":
    		bot.set_state(message.from_user.id, "sendwithphoto", message.chat.id)
    		return bot.send_message(message.chat.id, "Great! Send me a Photo with its Caption(caption is optional):)", reply_markup = cancel)
    	if message.text =="✨TEXT":
    		bot.set_state(message.from_user.id, "sendtext", message.chat.id)
    		return bot.send_message(message.chat.id, "Great! Send me a Text:)", reply_markup = cancel)
    	if message.text =="🎁Set Premium🎁":
    		bot.set_state(message.from_user.id, "setpremium", message.chat.id)
    		return bot.send_message(message.chat.id, "Cool, Send me USER_ID:)", reply_markup = cancel)
    	if message.text =="🎈Remove Premium🎈":
    		bot.set_state(message.from_user.id, "demotepremium", message.chat.id)
    		return bot.send_message(message.chat.id, "Cool, Send me USER_ID:)", reply_markup = cancel)
    	if message.text =="📊Statstics📊":
    		users = list(collection.find())
    		count = len(users)
    		return bot.send_message(message.chat.id, "Total Users : {}".format(count))
    	if message.text =="👨‍✈️Admin(s)👨‍✈️":
    		return bot.send_message(message.chat.id, "This feature is under maintenance!")
    	if message.text =="👮‍♂️Add Admin👮‍♂️":
    		if message.chat.id in owner:
    			bot.set_state(message.from_user.id, "adadmin", message.chat.id)
    			return bot.send_message(message.chat.id, "Wonderful, Send me USER_ID:)", reply_markup = cancel)
    		elif admin is True:
    			return bot.send_message(message.chat.id, "⚠️Only The Bot Owner Can Manage Admins:)")
    	if message.text =="✖️Delete Admin✖️":
    		if message.chat.id in owner:
    			bot.set_state(message.from_user.id, "deleteadmin", message.chat.id)
    			return bot.send_message(message.chat.id, "Wonderful, Send me USER_ID:)", reply_markup = cancel)
    		elif admin is True:
    			return bot.send_message(message.chat.id, "⚠️Only The Bot Owner Can Manage Admins:)")
    if user is True:
    	if check == False:
    		return bot.send_message(message.chat.id, "⚠️Before using this bot, You need to be a member of My Updates Channel⚠️", reply_markup = sub)
    	else:
    		if banned is True:
    			return bot.send_message(message.chat.id, "⚠️You Have Been Banned:(")
    		else:
    			pass  
    options = ReplyKeyboardMarkup(resize_keyboard = True, row_width=2)
    options.add("📄TEXT", "📷PHOTO")
    options.add("◀️Back")
    premium = is_premium(message.chat.id)
    if message.text =="🗞TEXT":
    	if premium is True:
    		bot.set_state(message.from_user.id, llink, message.chat.id)
    		return bot.send_message(message.chat.id, "Well, Send me the link of your promotion\nNB: for @share251bot users only!\nDon\'t have a link for @Share251bot? then click ❌Cancel and Send me /link251 😎:", reply_markup = cancel)
    	else:
    		return bot.send_message(message.chat.id, "🎁This feature is only available for premium users🎁\n💼UPGRADE NOW: @Lencho24")
    if message.text =="📸PHOTO":
    	if premium is True:
    		bot.set_state(message.from_user.id, lplink, message.chat.id)
    		return bot.send_message(message.chat.id, "Well, Send me the link of your promotion\nNB: for @share251bot users only!\nDon\'t have a link for @Share251bot? then click ❌Cancel and Send me /link251 😎:", reply_markup = cancel)
    	else:
    		return bot.send_message(message.chat.id, "🎁This feature is only available for premium users🎁\n💼UPGRADE NOW: @Lencho24")
    if message.text =="📝CREATE POST":
    	return bot.send_message(message.chat.id, "Choose the type of button:", reply_markup = typebtn)
    if message.text =="NORMAL BUTTON":
    	return bot.send_message(message.chat.id, "Choose the type of promotion you wanna make:", reply_markup = options)
    if message.text =="📄TEXT":
    	bot.set_state(message.from_user.id, link, message.chat.id)
    	return bot.send_message(message.chat.id, "Well, Send me the link of your promotion:", reply_markup = cancel)
    if message.text =="📷PHOTO":
    	bot.set_state(message.from_user.id, linkphoto, message.chat.id)
    	return bot.send_message(message.chat.id, "Well, Send me the link of your promotion:", reply_markup = cancel)
    if message.text =="🔙Back":
    	return bot.send_message(message.chat.id, f"👋Hey {message.from_user.first_name}! \n\nThis bot can help you to make promotion/post simply:", reply_markup = keyboards)
    if message.text =="◀️Back":
    	return bot.send_message(message.chat.id, "Choose the type of button:", reply_markup = typebtn)
    if message.text =="📲LOGIN BUTTON":
    	return bot.send_message(message.chat.id, "Choose the type of button\nNB: for @share251bot users only!:", reply_markup = loginmenu)
    
    if message.text =="📃HOW TO USE":
    	return bot.send_message(message.chat.id, help)
    if message.text =="📢PROJECT CHANNEL":
    	return bot.send_message(message.chat.id, project)   
    

bot.add_custom_filter(custom_filters.StateFilter(bot))

print("Successful")
bot.infinity_polling()                                               
