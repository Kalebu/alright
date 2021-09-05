# [alright](#)

<samp>

Python wrapper for WhatsApp web made with selenium inspired by [PyWhatsApp](https://github.com/shauryauppal/PyWhatsapp)

[![Downloads](https://pepy.tech/badge/alright)](https://pepy.tech/project/alright)
[![Downloads](https://pepy.tech/badge/alright/month)](https://pepy.tech/project/alright)
[![Downloads](https://pepy.tech/badge/alright/week)](https://pepy.tech/project/alright)

[![Youtube demo](https://img.youtube.com/vi/yitQTt-NukM/0.jpg)](https://www.youtube.com/watch?v=yitQTt-NukM)

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

Underneath alright is **Selenium** which is one does all the automation work by directly controlling the browser, so you need to have a selenium driver on your machine for **alright** to work. But luckily alright uses [webdrive-manager](https://pypi.org/project/webdriver-manager/), which does this automatically. You just need to install a browser. By default alright uses [Google Chrome](https://www.google.com/chrome/).

## What you can do with alright?

- [Send Messages](#sending-messages)
- [Send Images](#sending-images)
- [Send Videos](#sending-videos)
- [Send Documents](#sending-documents)

*When you're running your program made with **alright**, you can only have one controlled browser window at a time, If you run while another window is live it raise an error so make sure to close the controlled window before running another one*

### Unsaved contact vs saved contacts

Alright allows you to send the messages and media to both unsaved contacts as explained earlier but there is a tiny distinction on how you do that, you will observe this clearly as use the package.

The first step before sending anything to the user is first to locate the user and then you can start sending the informations thats where the main difference lies btn saved and unsaved contacts.

#### Saved contacts

To saved contact use method *find_by_username()* to locate saved user,you can also use the same method to locate WhatsApp groups, The parameter can be either be;

- saved username
- mobile number
- group name

Here an Example on how to do that

```python
>>> from alright import WhatsApp
>>> messenger = WhatsApp()
>>> messenger.find_by_username('saved-name or number or group')
```

#### Unsaved contacts

In sending message to unsaved whatsapp contacts use *find_user()* method to locate the user and The parameter can only be users number with country code with (+) omitted as shown below;

```python
>>> from alright import WhatsApp
>>> messenger = WhatsApp()
>>> messenger.find_user('255-74848xxxx')
```

Now Let's dive in on how we can get started on sending messages and medias

### Sending Messages

To send a message with alright, you first need to target a specific user by using *find_user()* method (include the **country code** in your number withour '+' symbol) and then after that you can start sending messages to the target user using *send_message()* method as shown in the example below;

```python
>>> from alright import WhatsApp
>>> messenger = WhatsApp()
>>> messenger.find_user('2557xxxxxz')
>>> messages = ['Morning my love', 'I wish you a good night!']
>>> for message in messages:  
        messenger.send_message(message)    
```

#### Multiple numbers

Here how to send a message to multiple users, Let's say we want to wish merry-x mass to all our contacts, our code is going to look like this;

```python
>>> from alright import WhatsApp
>>> messenger = WhatsApp()
>>> numbers = ['2557xxxxxx', '2557xxxxxx', '....']
>>> for number in numbers:
        messenger.find_user(number)
        messenger.send_message("I wish you a Merry X-mass and Happy new year ")
```

*You have to include the **country code** in your number for this library to work but don't include the (+) symbol*

### Sending Images

Sending Images is nothing new, its just the fact you have to include a path to your image instead or raw string characters and also you have use *send_image()*, Here an example;

```python
>>> from alright import WhatsApp
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

The rest of the documents such as docx, pdf, audio etc. falls into documents category. You can use *send_files()* to do that.

```python
>>> from alright import WhatsApp
>>> messenger = WhatsApp()
>>> messenger.find_user('mobile')
>>> messenger.send_file('path-to-file')
```

Well! thats all for now from the package, to request new feature make an issue.

## Contributions

**alright** is an open-source package under **MIT** license, so contributions are warmly welcome whether that be a code , docs or typo just fork it.

when contributing to code please make an issue for that before making your changes so that we can have a discussion before implementation.

## Issues

If you're facing any issue or difficulty with the usage of the package just raise one so that we can fix it as soon as possible.

## Give it a star

Was this useful to you ? Then give it a star so that more people can manke use of this. 

## Credits

All the credits to:

- [kalebu](https://github.com/kalebu)
- [shauryauppal](https://github.com/shauryauppal/)
- and all the contributors

</samp>
