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

## Getting started

You need to do a little bit of work to get [**alright**](https://github.com/Kalebu/alright) to running, but don't worry I gotcha you, everything will work well if you just carefully follow through the documentation.

### Installation

We need to have alright installed on our machine to start using which can either be done directly from **GitHub** or using **pip**.

#### installing directly

You first need to clone or download the repo to your local directory and then move into the project directory as shown in the example and then run the below command; 

```bash
git clone https://github.com/Kalebu/alright
cd alright
alright > python setup.py install 
....
```

#### installing from pip

```bash
pip install alright 
```

### Setting up Selenium 

Underneath alright is **Selenium**  which is one does all the automation work by directly controlling the browser, so you need to have a selenium driver on your machine for **alright** to work.

So primarly I developed **alright** and tested on a Chrome browser and therefore it gonna require you to have [Chrome](https://www.google.com/chrome/) and [chromedriver](https://chromedriver.chromium.org/downloads) other browser support coming soon.

*You need to make sure you download the chromedriver compatible with Chrome version you're using otherwise it won't work and also don't forget to extract the zip version of a driver*

Here a [guide](https://help.zenplanner.com/hc/en-us/articles/204253654-How-to-Find-Your-Internet-Browser-Version-Number-Google-Chrome) to check the version of chrome you're using 

#### Adding selenium driver to path

One more final step to set up is to add the selenium driver location to **path** so as it can be discovered by **alright**, which varies depending on the operating system you're using.

For instance lets say example the current location our driver is in */home/kalebu/chrome-driver* (You can view full path to your driver by running **pwd** command), Here how you would do that.

##### Linux

For linux to permanently add path to browser do this;

```bash
nano ~/.bashrc
```

and then add the command to export the folder at the very bottom of the file & then Ctrl+X to save it

```bash
export PATH=$PATH:"/home/kalebu/chrome-driver"
```

##### Window

For window users you follow this [guide](https://www.forbeslindesay.co.uk/post/42833119552/permanently-set-environment-variables-on-windows) to actually do that.

Now after that we're now ready to automating and controlling whatsappp web using **alright**

## What you can do with alright?

- [Send Messages](#sending-messages)
- [Send Images](#sending-images)
- [Send Videos](#sending-videos)
- [Send Documents](#sending-documents)

### Sending Messages

To send a message with alright, you first need to target a specific user by using *find_user()* method and then after that you can start sending messages to the target user using *send_message()* method as shown in the example below;

```python
>>> from alright import WhatsApp
>>> messenger = WhatsApp()
>>> messenger.find_user('2557xxxxxz')
>>> messages = ['Morning my love', 'I wish you a good night!']
>>> for message in messages:  
        messenger.send_message(message)    
```

#### Multiple numbers

Here how to send a message to multiple users, Let's say we wanta wish merry-x mass to all our contacts, our code is going to look like this;

```python
>>> from alright import WhatsApp
>>> messenger = WhatsApp()
>>> numbers = ['2557xxxxxx', '2557xxxxxx', '....']
>>> for number in numbers:
        messenger.find_user(number)
        messenger.send_message("I wish you a Merry X-mass and Happy new year ")
```

*You have to include the country code in your number for this library to work but don't include the (+) symbol*

### Sending Images

Sending message is nothing new, its just the fact you have to include a path to your image instead or raw string characters and also you have use *send_image()*, Here an example;

```python
>>> form alright import WhatsApp
>>> messenger = WhatsApp()
>>> messenger.find_user('mobile')
>>> messenger.send_image('path-to-image')
```

### Sending Videos

Samewise to videos just *send_videos()*  method;

```python
>>> from alright import WhatsApp
>>> messenger = WhatsApp()
>>> messenger.find_user('mobile')
>>> messenger.send_video('path-to-video)

```

### Sending Documents

The rest of the documents such as docx, pdf, audio, you name it falls into the category of documents and you can *send_files()* to that.

```python
>>> from alright import WhatsApp
>>> messenger = WhatsApp()
>>> messenger.find_user('mobile')
>>> messenger.send_file('path-to-file')
```

Well thats all for now for the package, to request new feature make an issue.

## Contributions

**alright** is opensource package under **MIT** license, so contributions are warmly welcome whether that be a code , docs or typo just fork it.

when contributing to code please make an issue for that before going making your changes so that we can have a prior discussion on implementation

## Issues

If you're facing any issue or difficult with the usage of the package just raise one so as we can fix it as soon as possible.

## Give it a star

Was this useful to you ? then give it a star so that more people can know about this. 

## Credits

All the credits to;

- [kalebu](https://github.com/kalebu)
- [shauryauppal](https://github.com/shauryauppal/)
- and all the contributors

</samp>