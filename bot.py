import telebot
from telebot.types import *
from telebot import custom_filters
from pymongo import MongoClient 

client = MongoClient("mongodb+srv://really651:K4vSnRMEsZhqsTqS@cluster0.pxc2foz.mongodb.net/?retryWrites=true&w=majority")

db = client["PromoBot"]
collection = db["promo"]


bot = telebot.TeleBot("6062326465:AAHezYHb8bs_X4q3UCXgb0ZMTxAdRlxseRc", parse_mode="html")

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
	if check== False:
	   return bot.send_message(message.chat.id, "⚠️Before using this bot, You need to be a member of My Updates Channel⚠️", reply_markup = sub)
	else:
		pass
	bot.set_state(message.from_user.id, get_link, message.chat.id)
	bot.send_message(message.chat.id, "Incredible, Now send me your post from @share251bot then i\'ll give you, your own link!", reply_markup = canc)

@bot.message_handler(content_types =["photo"], state=get_link)
def handle_getLink(message):	
	try:
		for i in message.reply_markup.keyboard:
		  		for x in i:
		  			bot.send_message(message.chat.id, f"Here is your own link: \n\n<code>{x.url}</code>", disable_web_page_preview=True)
		  			bot.delete_state(message.from_user.id, message.chat.id) 
		  			bot.send_message(message.chat.id, f"👋Hey {message.from_user.first_name}! \n\nThis bot can help you to make promotion/post simply:", reply_markup = keyboard)
	except:
		bot.send_message(message.chat.id, "It seems that you have not sent me correct info! Try Again!", reply_markup = canc)

@bot.message_handler(func = lambda message: True, state=get_link)
def handle_getLinks(message):
	if message.text =="❌Cancel":
		bot.delete_state(message.from_user.id, message.chat.id) 
		bot.send_message(message.chat.id, f"👋Hey {message.from_user.first_name}! \n\nThis bot can help you to make promotion/post simply:", reply_markup = keyboard)
	else:
		bot.send_message(message.chat.id, "Please send me your post from @share251bot!")
	
link = "link"
caption = "caption"
text = "text"

linkphoto = "linkphoto"
photo = "photo"
captionphoto = "captionphoto"
textphoto = "textphoto"

keyboard = ReplyKeyboardMarkup(resize_keyboard = True)
keyboard.add("📝CREATE POST", "📃HOW TO USE")
keyboard.add("📢PROJECT CHANNEL")

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
def start_message(message):
	id = message.from_user.id
	user = collection.find_one({"user_id": id})
	check = check_sub(message)
	if user:
		if check == False:
			bot.send_message(message.chat.id, "⚠️Before using this bot, You need to be a member of My Updates Channel⚠️", reply_markup = sub)
		else:
			bot.send_message(message.chat.id, f"👋Hey {message.from_user.first_name}! \n\nThis bot can help you to make promotion/post simply:", reply_markup = keyboard)
	else:
		collection.insert_one({"user_id": id})
		if check == False:
			bot.send_message(message.chat.id, "⚠️Before using this bot, You need to be a member of My Updates Channel⚠️", reply_markup = sub)
		else:
			bot.send_message(message.chat.id, f"👋Hey {message.from_user.first_name}! \n\nThis bot can help you to make promotion/post simply:", reply_markup = keyboard)
	
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
			bot.send_message(message.chat.id, f"👋Hey {message.from_user.first_name}! \n\nThis bot can help you to make promotion/post simply:", reply_markup = keyboard)
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
			bot.send_message(message.chat.id, f"👋Hey {message.from_user.first_name}! \n\nThis bot can help you to make promotion/post simply:", reply_markup = keyboard)
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
			bot.send_message(message.chat.id, f"👋Hey {message.from_user.first_name}! \n\nThis bot can help you to make promotion/post simply:", reply_markup = keyboard)
	bot.delete_state(message.from_user.id, message.chat.id)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    check = check_sub(message)
    if check == False:
    	return bot.send_message(message.chat.id, "⚠️Before using this bot, You need to be a member of My Updates Channel⚠️", reply_markup = sub)
    else:
    	pass
    options = ReplyKeyboardMarkup(resize_keyboard = True, row_width=2)
    options.add("📄TEXT", "📷PHOTO")
    options.add("◀️Back")
    if message.text =="📝CREATE POST":
    	bot.send_message(message.chat.id, "Choose the type of button:", reply_markup = typebtn)
    if message.text =="NORMAL BUTTON":
    	bot.send_message(message.chat.id, "Choose the type of promotion you wanna make:", reply_markup = options)
    if message.text =="📄TEXT":
    	bot.set_state(message.from_user.id, link, message.chat.id)
    	bot.send_message(message.chat.id, "Well, Send me the link of your promotion:", reply_markup = cancel)
    if message.text =="📷PHOTO":
    	bot.set_state(message.from_user.id, linkphoto, message.chat.id)
    	bot.send_message(message.chat.id, "Well, Send me the link of your promotion:", reply_markup = cancel)
    if message.text =="🔙Back":
    	bot.send_message(message.chat.id, f"👋Hey {message.from_user.first_name}! \n\nThis bot can help you to make promotion/post simply:", reply_markup = keyboard)
    if message.text =="◀️Back":
    	bot.send_message(message.chat.id, "Choose the type of button:", reply_markup = typebtn)
    if message.text =="📲LOGIN BUTTON":
    	bot.send_message(message.chat.id, "Choose the type of button\nNB: for @share251bot users only!:", reply_markup = loginmenu)
    if message.text =="🗞TEXT":
    	bot.set_state(message.from_user.id, llink, message.chat.id)
    	bot.send_message(message.chat.id, "Well, Send me the link of your promotion\nNB: for @share251bot users only!\nDon\'t have a link for @Share251bot? then click ❌Cancel and Send me /link251 😎:", reply_markup = cancel)
    if message.text =="📸PHOTO":
    	bot.set_state(message.from_user.id, lplink, message.chat.id)
    	bot.send_message(message.chat.id, "Well, Send me the link of your promotion\nNB: for @share251bot users only!\nDon\'t have a link for @Share251bot? then click ❌Cancel and Send me /link251 😎:", reply_markup = cancel)
    if message.text =="📃HOW TO USE":
    	bot.send_message(message.chat.id, help)
    if message.text =="📢PROJECT CHANNEL":
    	bot.send_message(message.chat.id, project)

bot.add_custom_filter(custom_filters.StateFilter(bot))

print("Successful")
bot.infinity_polling()
