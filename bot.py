import os
import random
from wsgiref.util import request_uri
from requests import request
import telebot
# types use for create button
from telebot import types
from PIL import ImageGrab
from playsound import playsound
from datetime import datetime


##########################################################################################
class Data:
  request_for_restart=0
  request_for_shutdown=0

  @staticmethod
  def readfile(filename):
      with open(filename,'r') as f:
        return f.read()

  @staticmethod
  def writefile(filename,fileData):
    with open(filename,'w+') as f:
        f.write(fileData)

# def create_menu(*args):

    markup=types.ReplyKeyboardMarkup(row_width=2)
   
    for arg in args:
        btn=types.KeyboardButton(arg)   
        markup.add(btn)   
    return markup    
   
def start_cmd(user,check):
  
  userChatId=user.chat.id
  userUsername=user.chat.username

  markup=types.ReplyKeyboardMarkup(row_width=2)
  btn1=types.KeyboardButton('📷 Take a screen shot')
  btn2=types.KeyboardButton('🔋 Power options')
  btn3=types.KeyboardButton('🔉 Play sound')
  btn4=types.KeyboardButton('📂 File manager')
  markup.add(btn1,btn2,btn3,btn4) 
  bot.send_message(userChatId,'Hello, welcome to my os remote bot',reply_markup=markup)

  if (check):
    pass
  else:
    print(f"User {userUsername} with ID {userChatId} started the bot ")

def save_cmd(user):
  userText=user.text
  userChatId=user.chat.id
  theMessage=userText.replace('/save','')  
  randNumber=random.randint(10001,99999)
  Data.writefile(f'database/data_{randNumber}.txt',theMessage)
  bot.send_message(userChatId,f'Your message with name : " data_{randNumber} " is saved.')

def saved_files_cmd(user):
  
  userChatId=user.chat.id
  
  filesList=''
  for root,dirs,files in os.walk('database'):
    for file in files:
      filesList=filesList+"\n"+file       
  bot.send_message(userChatId, f'files that you saved :\n {filesList}')

def power_option_cmd(user):
  userChatId=user.chat.id
  markup=types.ReplyKeyboardMarkup(row_width=2)
  btn1=types.KeyboardButton('❌ Shutdown')
  btn2=types.KeyboardButton('🔄 Restart')
  btn3=types.KeyboardButton('🏠 Home')
  markup.add(btn1,btn2,btn3) 
  bot.send_message(userChatId,'Power Option :',reply_markup=markup)
  
def restart_cmd(user):
  Data.request_for_restart=1
  Data.request_for_shutdown=0
  userChatId=user.chat.id
  bot.send_message(userChatId,'Do you wish to restart  the server ?\n send /yes to restart or /no to discard')

def shutdown_cmd(user):
  Data.request_for_shutdown=1
  Data.request_for_restart=0
  userChatId=user.chat.id
  bot.send_message(userChatId,'Do you wish to shutdown the server ?\n send /yes to shutdown or /no to discard')  

def restart_or_shutdown_cmd(user):
  userChatId=user.chat.id  
  
  if (Data.request_for_restart) :
    bot.send_message(userChatId,'Server is restarting ... ')
    os.system('reboot')
    Data.request_for_shutdown=0
    Data.request_for_restart=0

  elif (Data.request_for_shutdown) :    
    bot.send_message(userChatId,'server is shuting down ... ')
    os.system('shutdown')  
    Data.request_for_shutdown=0
    Data.request_for_restart=0

  else:
    bot.send_message(userChatId,'Process faild !!! ')

def screenshot_cmd(user):
  userChatId=user.chat.id
  bot.send_message(userChatId,'Taking a screen shot ... ')
  pic=ImageGrab.grab()
  pic.save('screenshot.png')
  photo=open('screenshot.png','rb') 
  bot.send_photo(userChatId,photo,caption='My  server desktop screen shot')
  photo.close()
  os.remove('screenshot.png')
  
def playsound_cmd(user):
  userChatId=user.chat.id
  bot.send_message(userChatId,'Your music  is playing now ... ')
  playsound('music/song_001.mp3')
 
def file_manager_cmd(user):
  userChatId=user.chat.id
  markup=types.ReplyKeyboardMarkup(row_width=2)
  btn1=types.KeyboardButton('📂 Files list')
  btn2=types.KeyboardButton('⬇️ Download')  
  btn3=types.KeyboardButton('🏠 Home')
  markup.add(btn1,btn2,btn3)
  bot.send_message(userChatId,'Welcome to file manager ',reply_markup=markup)

def files_list_cmd(user):
  userChatId=user.chat.id
  bot.send_message(userChatId,' For showing files list  use :\n /fileslist [directory path] ')


def download_cmd(user):
  userChatId=user.chat.id
  bot.send_message(userChatId,' For download  use :\n /download [file path] ')  

def start_download(user):
  userChatId=user.chat.id
  userText=user.text
  filePath=userText.replace('/download ','')  
  
  if os.path.isdir(filePath):     
      bot.send_message(userChatId,f'{filePath} is directory')
  else :
      if os.path.isfile(filePath):          
          bot.send_message(userChatId,f'{filePath} is file')
          with open(filePath,'rb') as file:
            bot.send_document(userChatId,file,caption='This is your file ')
      else:            
          bot.send_message(userChatId,'Not Found !!!')

def show_files_list(user):
  userChatId=user.chat.id
  userText=user.text
  directory=userText.replace('/fileslist ','')
  dirPath='/home/me/MyPro/'+directory
   
  if os.path.isdir(dirPath):     
      bot.send_message(userChatId,'Scanning files ....')
      
      for root,dirs,files in os.walk(dirPath):
        bot.send_message(userChatId, 'Your files list is :\n')
        for file in files:
            bot.send_message(userChatId, file)

      
  else :
    bot.send_message(userChatId,f'I could not find the {dirPath} directory')
  
    
##########################################################################################

TOKEN=Data.readfile('config/token.txt')
bot=telebot.TeleBot(TOKEN)
os.system('clear')

@bot.message_handler(content_types=['text'])
def main(user):

    adminsID=Data.readfile('config/adminsID.txt').splitlines()
    adminsUsername=Data.readfile('config/adminsUsername.txt').splitlines()
    userText=user.text
    userChatId=user.chat.id
    userUsername=user.chat.username
    userFirstName=user.chat.first_name
    userLastName=user.chat.last_name    

    print('---------------------------------------------------')
    print("User ID : " + str(userChatId))
    print("Username : @" + userUsername)
    print("User first name : "+ userFirstName)
    if (userLastName != None):
        print("User last name : " + userLastName)
    print("Text : "+ userText)
    print('---------------------------------------------------')
    
    if (str(userChatId) in adminsID and  userUsername in adminsUsername):
      if (userText == '/start' or userText == '🏠 Home'):
          if (userText=='🏠 Home'):
            check=1
          else:
            check=0  
          start_cmd(user,check)
      if (userText == '/save'):
        bot.send_message(userChatId,'you must send message like :\n /save [message]')    
      if (userText.startswith('/save ')):
          save_cmd(user)    
      if (userText == '/savedfiles'):    
        saved_files_cmd(user)
      if (userText == '🔋 Power options' ) :
        power_option_cmd(user) 
      if (userText == '📷 Take a screen shot'):
        screenshot_cmd(user)
      if( userText == '🔉 Play sound'):
        playsound_cmd(user)  
      if (userText == '❌ Shutdown'):
        shutdown_cmd(user)
      if (userText == '🔄 Restart'):
        restart_cmd(user)
      if (userText== '/yes'):
        restart_or_shutdown_cmd(user)  
      if (userText == '📂 File manager' or userText=='/filemanager'):
        file_manager_cmd(user)
      if(userText=='📂 Files list'):
        files_list_cmd(user)
      if(userText=='⬇️ Download'):
        download_cmd(user)
      
      if (userText.startswith('/download ')):
          start_download(user)
      if (userText =='/download'):
        download_cmd(user)
      if (userText=='/fileslist'):
        files_list_cmd(user)  
      if (userText.startswith('/fileslist ')):
         show_files_list(user)
    else:
      bot.send_message(userChatId,
      """
      Sorry! you do not have permision to remote access.you
      must login with admin user.

      """
      )
 
###########################################################################################
bot.polling(True)