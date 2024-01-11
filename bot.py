"""import telebot
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
"""
import os
#from flask import Flask, request
from pymongo import MongoClient
import telebot
from telebot.types import *
from telebot import custom_filters
from OpsAi import Ai
import requests
import PyPDF2
import os
import tempfile, datetime, time, math 
from gtts import gTTS
#from googletrans import LANGCODES, Translator
from mtranslate import translate

languages = []#list(LANGCODES.items())
languages.append(("English","en"))
languages.append(("Oromic","om"))
languages.append(("Amharic","am"))
languages.append(("Tigrigna","ti"))
languages.append(("German","de"))
languages.append(("Hindi","hi"))
languages.append(("Arabic","ar"))
languages.append(("French","fr"))

TOKEN = "5714196179:AAHGENqd7-KmGchB-gf-lVylsMoV1hp5iSw"
bot = telebot.TeleBot(TOKEN, parse_mode="html")
#server = Flask(__name__)


channel = ["@mt_projectz"]

def check_sub(message):
    for i in channel:
        a = bot.get_chat_member(i, message.from_user.id)
        if a.status == "left":
            return False
    return True

users = []

admin = [1365625365, 1170583016, 6118912816]

buttons = ["🧑‍💻Ask Code🧑‍💻", "🤖Explain Code🤖", "🌀Generate Images🌀", "⚙️Image Settings⚙️", "🎧Text To Voice🎧", "📑Ask PDF📑", "📸Ask Photo📸", "🌍Language🌍"]

markup = InlineKeyboardMarkup()
ma = InlineKeyboardButton("🕹Join My Updates🕹", url="t.me/mt_projectz")
markup.add(ma)

back = ReplyKeyboardMarkup(resize_keyboard=True)
back.add("⏪Back")

client = MongoClient("mongodb+srv://really651:gSPMW6u9WuStXIwD@cluster0.pxc2foz.mongodb.net/?retryWrites=true&w=majority")

db = client["Products"]
collection = db["coll"]

def markups():
    btns = []
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    for btn in buttons:
        btns.append(KeyboardButton(btn))
    markup.add(*btns)
    markup.add("❤Donate💛")
    return markup

def ask_coder(message, text):
    bot.send_chat_action(message.chat.id, "typing")
    try:
        s = Ai(query = text)
        cd = s.code()
        return bot.send_message(message.chat.id, cd, parse_mode="MARKDOWN")
    except:
        bot.send_message(message.chat.id, "Ohh, Dear Programmer, Something went wrong!\nPlease Try Again Later:)")

testbtn = InlineKeyboardMarkup()
testbtn.add(InlineKeyboardButton("🎧Let me hear this text🎧", callback_data="voice"))

@bot.inline_handler(lambda query: True)
def inline_query(query):    
    result = InlineQueryResultArticle(
        id='1',
        title="Channel Membership Required!",
        description="Before using this bot, kindly Join Our Channel:)",
        input_message_content=InputTextMessageContent(f"⚠️{query.from_user.first_name} before using this bot, kindly Join Our Channel👇"),
        reply_markup=markup
    )

    if bot.get_chat_member("@mt_projectz", query.from_user.id).status == "left":
        return bot.answer_inline_query(query.id, [result],
                                       button=InlineQueryResultsButton(text="Click here to Join:)",
                                                                      start_parameter="start"),
                                       cache_time=1, is_personal=True)
    photo_urls = []
    response = requests.get(f"https://lexica.art/api/v1/search?q={query.query}")
    data = response.json()  
    for image in data["images"]:
        if image["nsfw"] is not True:        	
            photo_urls.append(image["src"])
            if len(photo_urls) == 10:
                break 
    results = []
    for i, src in enumerate(photo_urls):
        results.append(
            telebot.types.InlineQueryResultPhoto(
                id=str(i),
                photo_url=src,
                thumbnail_url=src
            )
        )       

    bot.answer_inline_query(query.id, results,
                            button=InlineQueryResultsButton(text="Generate Images:",
                                                            start_parameter="start"),
                            is_personal=True)

def render_chat(message, text, lang):
    try:
        s = Ai(query = text)
        cd = s.chat()
        res = translate(cd, lang)
        return bot.reply_to(message, res, parse_mode ="MARKDOWN", reply_markup=testbtn)
    except Exception as e:
        bot.send_message(message.chat.id, "Ohh, Something went wrong!\nPlease Try Again Later:)")

def render_chat_gt(message, text, lang):
    try:
        s = Ai(query = text)
        cd = s.chat()
        res = translate(cd, lang)
        return bot.reply_to(message, res, parse_mode ="MARKDOWN",reply_markup=testbtn)		
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Ohh, Something went wrong!\nPlease Try Again Later:)")

def ask_chat(message, text):
    #bot.send_message(-1001882951482, f"username: {message.from_user.username}\nfirst-name: {message.from_user.first_name}\nprompt: {text}")
    bot.send_chat_action(message.chat.id, "typing")
    user = collection.find_one({"user_id": message.from_user.id})
    lang = user["lang"]
    if lang == "om" or lang == "ti":
        data = translate(text, "en")
        return render_chat(message=message, text=data, lang=lang)
    else:
        data = translate(text, "en")
        return render_chat_gt(message=message, text=data, lang=lang)

def ex_coder(message, text):
    bot.send_chat_action(message.chat.id, "typing")
    try:
        s = Ai(query = text)
        cd = s.explain()
        return bot.send_message(message.chat.id, cd, parse_mode="MARKDOWN")
    except:
        bot.send_message(message.chat.id, "Ohh, Dear Programmer, Something went wrong!\nPlease Try Again Later:)")

def convert_pdf_to_text(pdf_path, message):
    pdf_file = open(pdf_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    text = ''
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()

    pdf_file.close()

    return ask_chat(message, text)


@bot.message_handler(commands = ["stats"])
def sats(message):
    users = list(collection.find())
    count = len(users)
    if message.chat.id in admin:
        bot.send_message(message.chat.id, f"Total Users: {count}")
    else:
        pass

cancelb = ReplyKeyboardMarkup(resize_keyboard=True)
cancelb.add("❌Cancel")

@bot.message_handler(func = lambda message: True, state="broadcast")
def cast_state(message):
    if message.text == "❌Cancel":
        bot.delete_state(message.from_user.id, message.chat.id)
        return welcome(message)
    else:
        bot.delete_state(message.from_user.id, message.chat.id)
        users = collection.find({})
        for i in users:
            user = i["user_id"]
            try:
                bot.send_message(user, message.text, parse_mode ="html")
            except:
                pass

@bot.message_handler(commands =["broadcast"])
def broadcast(message):
    if message.chat.id in admin:
        bot.set_state(message.from_user.id, "broadcast", message.chat.id)
        bot.send_message(message.chat.id, "📥Send me a message to be sent to users || ❌Cancel", reply_markup=cancelb)


def welcome(message):
    return bot.send_message(message.from_user.id, f"{message.from_user.first_name}, Hello and welcome to poweful ChatGPT Bot👋\n\n<b>This bot can help you to do so many things and it\'s completely free🌀</b>\n\n<i>✨Select an option below or Just Ask me questions directly👇</i>", reply_markup=markups())		

@bot.message_handler(commands=["start"], chat_types=["private"])
def start(message):
    user = collection.find_one({"user_id": message.from_user.id})
    state = bot.get_state(message.from_user.id, message.chat.id)
    if state:
        bot.delete_state(message.from_user.id, message.chat.id)
    else:
        pass
    if user:
        if not "is_gallery" or "lang" in user:
            collection.update_one({"user_id": message.from_user.id}, {"$set": {"is_gallery": False, "lang": "en"}})
            return welcome(message)
        #if bot.get_chat_member("@mt_projectz", message.from_user.id).status != "left":
            #bot.send_message(message.chat.id, f"{message.from_user.first_name}, Hello and welcome to poweful ChatGPT Bot👋\n\n<b>This bot can help you to do so many things and it\'s completely free🌀</b>\n\n<i>✨Select an option below or Just Ask me questions directly👇</i>", reply_markup=markups())
        else:
            #pass
            return welcome(message)
            #bot.send_message(message.chat.id, f"⚠️{message.from_user.first_name} before using this bot, kindly Join Our Channel👇", reply_markup=markup)
    else:
        collection.insert_one({"user_id": message.from_user.id, "is_premium": False, "is_gallery": False, "lang": "en"})
        return welcome(message)
        #if bot.get_chat_member("@mt_projectz", message.from_user.id).status != "left":
            #bot.send_message(message.chat.id, f"{message.from_user.first_name}, Hello and welcome to poweful ChatGPT Bot👋\n\n<b>This bot can help you to do so many things and it\'s completely free🌀</b>\n\n<i>✨Select an option below or Just Ask me questions directly👇</i>", reply_markup=markups())
        #else:
            #bot.send_message(message.chat.id, f"⚠️{message.from_user.first_name} before using this bot, kindly Join Our Channel👇", reply_markup=markup)

def answer_photo(message):
    b = bot.reply_to(message,"✨Reading what you sent....")
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)    
    api_key = 'K81164834388957'
    url = 'https://api.ocr.space/parse/image'
    payload = {
        'apikey': api_key,
        'language': 'eng',
        'isOverlayRequired': False
    }
    files = {
        'filename': ('image.jpg', downloaded_file, 'image/jpeg')
    }
    response = requests.post(url, data=payload, files=files)
    if response.status_code == 200:
        response_data = response.json()
        if response_data['IsErroredOnProcessing']:
            error_message = response_data['ErrorMessage']
            bot.send_message(message.chat.id, f'Error: {error_message}\nReport to @MT_ProjectzChat')
        else:
            extracted_text = response_data['ParsedResults'][0]['ParsedText']
            bot.delete_message(message.chat.id, b.id)
            ask_chat(message, extracted_text)
    else:
        bot.send_message(message.chat.id, 'Error: Report to @MT_ProjectzChat')

def answer_pdf(message):
    try:
        chat_id = message.chat.id

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        if message.document.file_name.endswith('.pdf'):          
            temp = tempfile.NamedTemporaryFile(delete=False)
            temp.write(downloaded_file)
            temp.close()          
            text = convert_pdf_to_text(temp.name, message)                   
            os.unlink(temp.name)
    except Exception as e:
        bot.reply_to(message, f'Oops, something went wrong. Error: {e}NB: Only PDF format is supported!')	

def generate_gallery(text):
    photos = []
    album = []
    response = requests.get(f"https://lexica.art/api/v1/search?q={text}")
    data = response.json() 
    for image in data["images"]:
         if image["nsfw"] is not True:
           photos.append(image)
           if len(photos) == 10:
            break
    for img in photos:
        album.append(InputMediaPhoto(img["gallery"]))  
    return album

def voice(text, chat_id):
    bot.send_chat_action(chat_id, "upload_voice")
    tts = gTTS(text=text, lang='en')
    tts.save('voice.mp3')  
    with open('voice.mp3', 'rb') as voice:
        bot.send_voice(chat_id, voice, reply_markup=markups(), caption="Generated by @ChatGPT_v4_Robot ")  
    os.remove('voice.mp3')

crypto = """
<b>❤Donate the developer to encourage for new features via Crypto:💚</b>

<b>Bitcoin</b>: <code>17mBRrYZQtFwfHDdDAe6HtGdAc8TmZMKQA</code>

<b>USDT(TRC20)</b>: <code>TV6FUqCKGUq7SE4K2S3X19uc8te1uLYU5T</code>

<b>Binance Coin</b>: <code>0x8cF185cBF72E40b1B5B6DFdFAb2E5CB19175b22a</code>

<b>Tron(TRX)</b>: <code>TV6FUqCKGUq7SE4K2S3X19uc8te1uLYU5T</code>

<i>🌍For others payment methods contact the admin - @BetterParrot:)</i>
"""

inline = InlineKeyboardMarkup()
inline.add(InlineKeyboardButton("📝Try Inline Search📝", switch_inline_query_current_chat="Goat"))

def generate_src(text):
    photos = []
    album = []
    response = requests.get(f"https://lexica.art/api/v1/search?q={text}")
    data = response.json() 
    for image in data["images"]:
         if image["nsfw"] is not True:
           photos.append(image)
           if len(photos) == 10:
            break
    for img in photos:
        album.append(InputMediaPhoto(img["src"]))  
    return album

def render_src(text, chat_id):
    bot.send_chat_action(chat_id, "upload_photo")
    data = {
        "user_id": chat_id,
        "time": time.time()}
    try:
        album = generate_src(text)
        bot.send_media_group(chat_id, album)
        users.append(data)
    except Exception as e:        
        bot.send_message(chat_id, "The image couldn't be generated.")

def render_gallery(text, chat_id):
    bot.send_chat_action(chat_id, "upload_photo")
    data = {
        "user_id": chat_id,
        "time": time.time()}
    try:
        album = generate_gallery(text)
        bot.send_media_group(chat_id, album)
        users.append(data)
    except Exception as e:        
        bot.send_message(chat_id, "The image couldn't be generated.")

@bot.message_handler(content_types=["text"], state="ask_code")
def ask_code_state(message):
    data = {
        "user_id": message.from_user.id,
        "time": time.time()
    }
    if message.text == "⏪Back":
        bot.delete_state(message.from_user.id, message.chat.id)
        return welcome(message)
    else:
        user_time = [usr for usr in users if usr["user_id"] == data["user_id"]]
        if user_time:
            if time.time() - user_time[0]["time"] >= 30:
                user_time[0]["time"] = time.time()
                bot.send_message(-1001882951482, f"username: {message.from_user.username}\nfirst-name: {message.from_user.first_name}\nprompt: {message.text}")
                return ask_coder(message, message.text)         
            else:
                limit = time.time() - user_time[0]["time"]
                time_limit = 30 - limit
                return bot.send_message(message.chat.id, f"Please wait {math.floor(time_limit)} seconds before asking another code.")
        else:
            users.append(data)
            return ask_coder(message, message.text)

@bot.message_handler(content_types=["text"], state="ex_code")
def ex_code_state(message):
    data = {
        "user_id": message.from_user.id,
        "time": time.time()
    }
    if message.text == "⏪Back":
        bot.delete_state(message.from_user.id, message.chat.id)
        return welcome(message)
    else:
        user_time = [usr for usr in users if usr["user_id"] == data["user_id"]]
        if user_time:
            if time.time() - user_time[0]["time"] >= 10:
                user_time[0]["time"] = time.time()
                #bot.send_message(-1001882951482, f"username: {message.from_user.username}\nfirst-name: {message.from_user.first_name}\nprompt: {message.text}")
                return ex_coder(message, message.text)         
            else:
                limit = time.time() - user_time[0]["time"]
                time_limit = 10 - limit
                return bot.send_message(message.chat.id, f"Please wait {math.floor(time_limit)} seconds before making another request.")
        else:
            users.append(data)
            return ex_coder(message, message.text)

@bot.message_handler(content_types =["document"], state="pdf")
def resp_pdf(message):
    if message.text == "⏪Back":
        bot.delete_state(message.from_user.id, message.chat.id)
        return welcome(message)
    else:
        bot.delete_state(message.from_user.id, message.chat.id)
        return answer_pdf(message)

@bot.message_handler(content_types =["text"], state="pdf")
def resp_pdf3(message):
    if message.text == "⏪Back":
        bot.delete_state(message.from_user.id, message.chat.id)
        return welcome(message)

@bot.message_handler(content_types =["text"], state="voice")
def resp_pdf4(message):
    if message.text == "⏪Back":
        bot.delete_state(message.from_user.id, message.chat.id)
        return welcome(message)
    else:
        bot.delete_state(message.from_user.id, message.chat.id)
        return voice(message.text, message.from_user.id)  

@bot.message_handler(content_types =["text"], state="photo")
def resp_pdf1(message):
    if message.text == "⏪Back":
        bot.delete_state(message.from_user.id, message.chat.id)
        return welcome(message)               

@bot.message_handler(content_types =["photo"], state="photo")
def resp_pdf2(message):
    if message.text == "⏪Back":
        bot.delete_state(message.from_user.id, message.chat.id)
        return welcome(message)
    else:
        bot.delete_state(message.from_user.id, message.chat.id)
        return answer_photo(message)

@bot.message_handler(content_types=["text"], state="generate_image")
def generate_img(message):
    data = {
        "user_id": message.from_user.id,
        "time": time.time()
    }
    if message.text == "⏪Back" or message.text == "/start":
        bot.delete_state(message.from_user.id, message.chat.id)
        return welcome(message)
    else:
        user = collection.find_one({"user_id": message.from_user.id})
        user_time = [usr for usr in users if usr["user_id"] == data["user_id"]]
        if user_time:
            if time.time() - user_time[0]["time"] >= 10:
                user_time[0]["time"] = time.time()
                if user["is_gallery"]:                 
                    return render_gallery(message.text, message.from_user.id)
                else:                
                    return render_src(message.text, message.from_user.id)
            else:
                limit = time.time() - user_time[0]["time"]
                time_limit = 10 - limit
                return bot.send_message(message.chat.id, f"Please wait {math.floor(time_limit)} seconds before asking another question.")
        else:
            users.append(data)
            if user["is_gallery"]:
               return render_gallery(message.text, message.from_user.id)
            else:
                return render_src(message.text, message.from_user.id)


img_type = InlineKeyboardMarkup(row_width=2)
i1 = InlineKeyboardButton("📸Single Images📸", callback_data="single")
i2 = InlineKeyboardButton("🗞Gallery Images🗞", callback_data="gallery")
i3 = InlineKeyboardButton("❌Cancel", callback_data="cancel")
img_type.add(i1, i2, i3)


@bot.message_handler(content_types =["text"], chat_types =["private"])
def resp(message):
    user = collection.find_one({"user_id": message.from_user.id})
    if not "lang" in user:
        return collection.update_one({"user_id": message.from_user.id}, {"$set": {"is_gallery": False, "lang": "en"}})
    else:
        pass
    #if bot.get_chat_member("@mt_projectz", message.from_user.id).status == "left":
        #return bot.send_message(message.chat.id, f"⚠️{message.from_user.first_name} before using this bot, kindly Join Our Channel: @Mt_Projectz")
    data = {
        "user_id": message.from_user.id,
        "time": time.time()
    }    
    if message.text == "🧑‍💻Ask Code🧑‍💻":
        bot.set_state(message.from_user.id, "ask_code", message.chat.id)
        return bot.send_message(message.chat.id, "What do you wanna me to code for you:", reply_markup=back)
    if message.text == "🌀Generate Images🌀":
        bot.set_state(message.from_user.id, "generate_image", message.chat.id)
        bot.send_message(message.chat.id, "What do you wanna me to Imagine:", reply_markup=back)
        return bot.send_message(message.chat.id, "<i>You can also use Inline mode</i>", reply_markup=inline)
    if message.text == "⚙️Image Settings⚙️":
        return bot.send_message(message.chat.id, "Choose Images format:", reply_markup = img_type)  
    if message.text == "🤖Explain Code🤖":
        bot.set_state(message.from_user.id, "ex_code", message.chat.id)
        return bot.send_message(message.chat.id, "Just send me a code, i\'ll explain as much as I can:", reply_markup=back)
    if message.text == "📑Ask PDF📑":
        bot.set_state(message.from_user.id, "pdf", message.chat.id)
        return bot.send_message(message.chat.id, "Just upload your PDF, i\'ll analyse it:", reply_markup=back)
    if message.text == "📸Ask Photo📸":
        bot.set_state(message.from_user.id, "photo", message.chat.id)
        return bot.send_message(message.chat.id, "Just send your photo, i\'ll analyse it:", reply_markup=back)
    if message.text == "🎧Text To Voice🎧":
        bot.set_state(message.from_user.id, "voice", message.chat.id)
        return bot.send_message(message.chat.id, "Just send your some text, i\'ll convert it to voice:", reply_markup=back)
    if message.text == "🌍Language🌍": 	
        buttons = []
        markup = InlineKeyboardMarkup(row_width=2)
        for btn in languages[:10]:
            buttons.append(InlineKeyboardButton(btn[0].title(), callback_data=btn[1]))
        markup.add(*buttons)
        markup.add(InlineKeyboardButton("🔙Go Back", callback_data="cancel"), InlineKeyboardButton("⏩", callback_data="page_2"))
        return bot.send_message(message.chat.id, "Choose your language🌍", reply_markup=markup)
    if message.text == "❤Donate💛":
        return bot.send_message(message.chat.id, crypto)
    if message.text == "⏪Back":
        return welcome(message)
    else:        
        user_time = [usr for usr in users if usr["user_id"] == data["user_id"]]
        if user_time:
           if time.time() - user_time[0]["time"] >= 10:
                user_time[0]["time"] = time.time()
                return ask_chat(message, message.text)
           else:
                limit = time.time() - user_time[0]["time"]
                time_limit = 10 - limit
                return bot.send_message(message.chat.id, f"Please wait {math.floor(time_limit)} seconds before asking another question.")
        else:
            users.append(data)
            return ask_chat(message, message.text)

@bot.callback_query_handler(func=lambda callback: callback.data.startswith("page_"))
def handle_callback_query(callback):  
    page = int(callback.data.split("_")[1])
    start_index = (page - 1) * 10
    end_index = start_index + 10
    page_items = languages[start_index:end_index]
    buttons = []
    markup = InlineKeyboardMarkup(row_width=2)
    for item in page_items:
        buttons.append(InlineKeyboardButton(item[0].title(), callback_data=item[1]))   
    if page > 1:        
        buttons.append(InlineKeyboardButton("⏪", callback_data=f"page_{page - 1}"))
    if end_index < len(languages):
        buttons.append(InlineKeyboardButton("⏩", callback_data=f"page_{page + 1}"))
    markup.add(*buttons)
    markup.add(InlineKeyboardButton("🔙Go Back", callback_data="cancel"))
    bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func = lambda callback: True)
def ans_callback(callback):
    donate = InlineKeyboardMarkup()
    donate.add(InlineKeyboardButton("❤Donate❤", callback_data="donate"))
    if callback.data == "single":
        collection.update_one({"user_id": callback.from_user.id}, {"$set": {"is_gallery": False}})
        return bot.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.message_id, text="📸The format of image is changed to Single Images📸")
    if callback.data == "gallery":
        collection.update_one({"user_id": callback.from_user.id}, {"$set": {"is_gallery": True}})
        return bot.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.message_id, text="📸The format of image is changed to Gallery Images📸")
    if callback.data == "cancel":
        return bot.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.message_id, text=f"❌Cancelled.")
    if callback.data == "donate":
        menu = InlineKeyboardMarkup()
        menu.add(InlineKeyboardButton("🔙Back to menu", callback_data="menu"))
        return bot.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.message_id, text=crypto, reply_markup=menu)
    if callback.data == "menu":
        bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=None)
        return welcome(callback)
    if callback.data == "voice":
        bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=None)
        return voice(callback.message.text, callback.message.chat.id)
    else:		
        collection.update_one({"user_id": callback.from_user.id}, {"$set": {"lang": callback.data}})
        return bot.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.message_id, text=f"Great, I\'ll answer your questions by this language🌍", reply_markup = donate)

bot.add_custom_filter(custom_filters.StateFilter(bot))

print("Successful")
bot.delete_webhook()
bot.infinity_polling()

"""@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://flask1.tolasaa.repl.co/' + TOKEN, drop_pending_updates=True)
    return "ok", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))"""
