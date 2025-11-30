# WELCOME AND INFORMATION MESSAGES
WELCOME_MESSAGE = """👋 Welcome to FasterPostMaker!

This bot helps you create professional promotional posts with custom buttons in just a few simple steps.

Please select an option below to get started."""

HELP_MESSAGE = """📖 **How to Use FasterPostMaker**

This bot allows you to create promotional posts with two types of buttons:

**Normal Buttons** - Standard URL buttons that link to any website
**Login Buttons** - Telegram login buttons (requires @share251bot integration)

Simply follow the step-by-step prompts to create your post. The bot will guide you through:
1. Entering your link/URL
2. Adding your post text or photo
3. Customizing your button labels

It's fast, easy, and saves you time!"""

# USER STATUS MESSAGES
BANNED_MESSAGE = "⚠️ Access Denied: Your account has been banned from using this bot."

PREMIUM_ONLY_MESSAGE = """🎁 **Premium Feature**

This feature is only available for premium users.

To upgrade your account, please contact: @betterparrot"""

# ADMIN PANEL MESSAGES
ADMIN_WELCOME = """😎 **Admin Panel**

Welcome to the administration panel.
Please choose an action from the options below."""

ADMIN_ONLY_MESSAGE = "⚠️ Permission Denied: Only the bot owner can manage administrators."

CANCELLED_MESSAGE = "❌ Operation cancelled."

MAIN_MENU_MESSAGE = "📋 Main Menu"

# USER MANAGEMENT MESSAGES
USER_FOUND_TEMPLATE = """✅ **User Information**

**Admin Status:** {is_admin}
**Ban Status:** {is_banned}
**Premium Status:** {is_premium}"""

USER_NOT_FOUND = "❌ User not found (404). Please verify the User ID and try again."

USER_NOT_IN_DB = "❌ This user does not exist in the database."

USER_ALREADY_BANNED = "⚠️ This user is already banned."

USER_ALREADY_UNBANNED = "⚠️ This user is not currently banned."

USER_BANNED_SUCCESS = "✅ User has been successfully banned."

USER_UNBANNED_SUCCESS = "✅ User has been successfully unbanned."

USER_PROMOTED_ADMIN = "✅ User successfully promoted to administrator."

USER_DEMOTED_ADMIN = "✅ Administrator privileges successfully removed."

USER_BECAME_ADMIN = "🎉 Congratulations! You have been granted administrator privileges."

USER_PREMIUM_GRANTED = "✅ Premium access granted to user."

USER_PREMIUM_REMOVED = "✅ Premium access revoked from user."

USER_GOT_PREMIUM = "🎁 Congratulations! You now have premium access to all features."

USER_LOST_PREMIUM = "📢 Your premium access has expired. Please contact support to renew."

# BROADCAST MESSAGES
BROADCAST_SUCCESS = "✅ Message successfully broadcasted to all users!"

BROADCAST_CONFIRM = "📤 **Confirm Broadcast**\n\nAre you sure you want to send this message to all users?"

BROADCAST_TEXT_CONFIRM = "📤 **Confirm Broadcast**\n\nAre you sure you want to broadcast this message?"

SEND_PHOTO_PROMPT = "📸 Please send a photo to broadcast."

CHOOSE_BROADCAST_TYPE = """📢 **Broadcast Type**

Choose the type of content you want to broadcast:

• **TEXT** - Send a text message
• **PHOTO** - Send a photo with optional caption"""

# POST CREATION MESSAGES
LINK_PROMPT = "🔗 Please send me the URL/link for your promotion:"

LINK_PROMPT_SHARE251 = """🔗 **Enter Promotion Link**

Please send me your promotion link.

**Note:** This feature requires @share251bot integration.
If you don't have a share251bot link, click ❌Cancel and use /link251 to get one."""

CAPTION_PROMPT = "✍️ Great! Now send me the caption/text for your promotion:"

TEXT_PROMPT = "✍️ Perfect! Now send me the text for your post:"

PHOTO_PROMPT = "📸 Excellent! Now send me the photo for your promotion:"

PHOTO_CAPTION_PROMPT = "✍️ Now send me the caption for your photo (optional):"

PHOTO_SEND_PROMPT = "📸 Please send the photo for your promotion:"

BUTTON_TEXT_PROMPT = """🔘 **Button Labels**

Finally, send me the text for your button(s).

For multiple buttons, separate them with commas.
Example: `Join Channel, Visit Website`"""

INVALID_LINK = """❌ **Invalid Link**

Please provide a valid URL.

**Note:** Make sure your link starts with *https://*"""

INVALID_LINK_SIMPLE = "❌ Invalid link. Please provide a valid URL."

SEND_BROADCAST_TEXT = "✍️ Great! Send me the text message you want to broadcast:"

SEND_BROADCAST_PHOTO = "📸 Perfect! Send me the photo you want to broadcast (caption is optional):"

# SHARE251 INTEGRATION MESSAGES
SHARE251_PROMPT = """🔗 **Get Share251 Link**

Please forward me your post from @share251bot, and I'll extract the link for you!"""

SHARE251_LINK_TEMPLATE = """✅ **Link Extracted Successfully**

Here is your link:

`{link}`

You can now use this link to create promotional posts!"""

SHARE251_INVALID = "❌ Unable to extract link. Please make sure you're forwarding a valid post from @share251bot."

SHARE251_RETRY = "📮 Please send me your post from @share251bot."

# PROMPT MESSAGES
SEND_USER_ID = "🆔 Please send me the User ID:"

SEND_USER_ID_ADMIN = "🆔 Please send me the User ID of the person you want to manage:"

CHOOSE_BUTTON_TYPE = """🔘 **Button Type**

Choose the type of button you want to add to your post:"""

CHOOSE_POST_TYPE = """📝 **Post Type**

What type of promotional post do you want to create?"""

CHOOSE_LOGIN_BUTTON_TYPE = """🔘 **Login Button Type**

Choose your post format:

**Note:** This feature requires @share251bot integration."""

# STATISTICS AND SYSTEM MESSAGES

TOTAL_USERS_TEMPLATE = "📊 **Total Users:** {count}"

FEATURE_MAINTENANCE = "🔧 This feature is currently under maintenance. Please try again later."

ERROR_TEMPLATE = "⚠️ **Error:** {error}"
