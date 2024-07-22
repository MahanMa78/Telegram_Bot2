import telebot 

from config import API_TOKEN,admin,file_path

bot = telebot.TeleBot(API_TOKEN)

users=[]

@bot.message_handler(commands=['start'])
def welcome(message):
    id = int(message.from_user.id)
    f_name = message.from_user.first_name
    l_name = message.from_user.last_name
    username = message.from_user.username

    if username == None: 
        bot.reply_to(message,f"فیلد username خالی است.آن را پر کنید و دوباره امتحان کنید")
    
    else:
        bot.reply_to(message,f'خوش آمدید \nنام شما:{f_name}\nنام خانوادگی شما:{l_name} \n id: {id} \n username: @{username}')

    if username != None:
        # users.append(username)

        existing_data = read_existing_data(file_path)

        if username not in existing_data:
            with open('users.txt','a') as new_user:
                new_user.write('@'+username+'\n')


def read_existing_data(file_path):
    try:
        with open('users.txt','r') as file:
            existing_data = set(line.strip() for line in file)
    except FileNotFoundError:
        existing_data = set()
    return existing_data


def send_from_file():
    with open('users.txt','r') as file:
        file.read()

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