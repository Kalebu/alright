# If you DO have the WhatsApp Desktop app installed
from alright import WhatsApp

msg = "hey I'm done its tuesday"
messenger = WhatsApp()
numbers = ['00000000000', '00000000000', '00000000000']
for number in numbers:
    messenger.find_user(number)
    messenger.send_picture('/Users/arsalankhan/Downloads/tiger.jpeg', "Text to accompany image")
