# [alright](#)

<samp>

Python wrapper for WhatsApp web made with selenium inspired by [PyWhatsApp](https://github.com/shauryauppal/PyWhatsapp)


## Why alright ? 

I was looking for a way to control and automate WhatsApp web with Python, I came across some very nice libaries and wrappers implementations including;

- [pywhatkit](https://pypi.org/project/pywhatkit/)
- [pywhatsapp](https://github.com/tax/pywhatsapp)
- [PyWhatsapp](https://github.com/shauryauppal/PyWhatsapp)
- [WebWhatsapp-Wrapper](https://github.com/mukulhase/WebWhatsapp-Wrapper)
- and many others

So I tried [**pywhatkit**](https://pypi.org/project/pywhatkit/), really cool one well crafted to be used by others but its implementations require you to open a new browser tap and scan QR code everytime you send a message no matter if its the same person, which was deal breaker for using it.

I then tried [**pywhatsapp**](https://github.com/tax/pywhatsapp) which is based on [yowsup](https://github.com/tgalal/yowsup) and thus requiring you to do some registration with yowsup before using it of which after bit of googling I got scared of having my number blocked when I do that so I went for the next option

I then went for [**WebWhatsapp-Wrapper**](https://github.com/mukulhase/WebWhatsapp-Wrapper), it has some good documentation and recent commits so I had hopes it gonna work but It didn't for me, and after having couples of errors I abandoned it to look for the next alternative.

Which is [**PyWhatsapp**](https://github.com/shauryauppal/PyWhatsapp) by [shauryauppal](https://github.com/shauryauppal/), which was more of cli tool than a wrapper which suprisingly worked and it's approach allows you to dynamically send whatsapp message to unsaved contacts without rescanning QR-code everytime.

So what I did is more of a refactoring of the implementation of that tool to be more of wrapper to easily allow people to run different scripts on top of it instead of just using as a tool I then thought of sharing the codebase to people who might struggled to do this as I did.


....
</samp>