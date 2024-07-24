import telebot 
import sqlite3
import time
from config import API_TOKEN,admin,file_path


bot = telebot.TeleBot(API_TOKEN)
users=[]





@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = int(message.from_user.id)
    f_name = message.from_user.first_name
    l_name = message.from_user.last_name
    username = message.from_user.username
    timestr = time.strftime("%Y:%m:%d-%H:%M")

    if username == None: 
        bot.reply_to(message,f"فیلد username خالی است.آن را پر کنید و دوباره امتحان کنید")
    
    else:
        bot.reply_to(message,f'خوش آمدید \nنام شما:{f_name}\nنام خانوادگی شما:{l_name} \n id: {user_id} \n username: @{username} \n date: {timestr} ')

    if username != None:

        
        with sqlite3.connect('users.db') as connection:

            cursor = connection.cursor()
            
            insert_data_query="""
                INSERT INTO users(id,user,date)
                VALUES (?,?,?,?)
                """
            data = (
                message.chat.id,
                f"{message.from_user.username}",
                f"{time.strftime("%Y:%m:%d-%H:%M")}"
            )
            cursor.execute(insert_data_query,data)

    


@bot.message_handler(commands=['addword'])
def showlist(message):
    if message.from_user.username == admin :
       
        with open('users.txt','r') as file:
            data=file.read()
        
        user= list(map(lambda user:user + '\n' , users))
        bot.send_message(message.chat.id,f"{data}")

    else:
        bot.reply_to(message,"شما دسترسی به این محتوا ندارید")



bot.infinity_polling()