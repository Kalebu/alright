# If you DO NOT have the WhatsApp Desktop app installed
from alright import WhatsApp
messenger = WhatsApp()
messenger.find_user('2556929069077')
messenger.send_message("hey I'm done its tuesday ")
input()

# If you DO have the WhatsApp Desktop app installed
from alright import WhatsApp

msg = "hey I'm done its tuesday"
messenger = WhatsApp()
messenger.send_message1('2556929069077', msg)
