import telebot 
import sqlite3
import time
from datetime import datetime
from config import API_TOKEN,admin,file_path

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = int(message.from_user.id)
    f_name = message.from_user.first_name
    l_name = message.from_user.last_name
    username = message.from_user.username
    timestr = time.strftime("%Y:%m:%d-%H:%M")

    if username == None: 
        bot.reply_to(message,f"فیلد username خالی است.آن را پر کنید و دوباره امتحان کنید")
    

    elif username != None:
        if check_username_exists(username):
            bot.reply_to(message, "این نام کاربری قبلا در دیتابیس وجود دارد.")

        else:
            with sqlite3.connect('users.db') as connection:

                cursor = connection.cursor()
                
                insert_data_query="""
                    INSERT INTO users(id,user,date)
                    VALUES (?,?,?)
                    """
                data = (
                    message.chat.id,
                    f"{message.from_user.username}",
                    f"{time.strftime("%Y:%m:%d-%H:%M")}"
                )
                cursor.execute(insert_data_query,data)


def check_username_exists(username):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT 1 FROM users WHERE user = ?', (username,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result is not None


@bot.message_handler(commands=['show_user'])
def show_user(message):
    user_id = int(message.from_user.id)
    f_name = message.from_user.first_name
    l_name = message.from_user.last_name
    username = message.from_user.username
    timestr = time.strftime("%Y:%m:%d-%H:%M")
    bot.reply_to(message,f'خوش آمدید \nنام شما:{f_name}\nنام خانوادگی شما:{l_name} \n id: {user_id} \n username: @{username} \n date: {timestr} ')

@bot.message_handler(commands=['users'])
def show_users(message):
    if message.from_user.username == admin :
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute("SELECT user FROM users")
        rows = cursor.fetchall()
        usernames = [row[0] for row in rows]
        cursor.close()
        connection.close()  
        
        response = "\n@".join([username.strip() for username in usernames])
        bot.reply_to(message,"@" + response)
        
    else:
        bot.reply_to(message,"شما دسترسی به این محتوا ندارید")


@bot.message_handler(commands=['show_user'])
def show_user(message):
    user_id = message.from_user.id
    f_name = message.from_user.first_name
    l_name = message.from_user.last_name
    username = message.from_user.username
    timestr = time.strftime("%Y:%m:%d-%H:%M")
    days = check_point(username)

    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("SELECT date FROM users WHERE user = ? " , (username,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    a= result[0]
    bot.reply_to(message,f'خوش آمدید \nname : {f_name}\nlast name : {l_name} \n id: {user_id} \n username: @{username} \n date: {a}\n points : {days} ')


def check_point(username):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("SELECT date FROM users WHERE user = ? " , (username,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    if result:
        created_at = result[0]
        created_date = datetime.strptime(created_at, '%Y:%m:%d-%H:%M')
        days_since = (datetime.now() - created_date).days
        return days_since
    else:
        return None

bot.infinity_polling()