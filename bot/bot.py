import logging
import re

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import paramiko
import os
import subprocess

import psycopg2
from psycopg2 import Error

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

# Подключаем логирование
logging.basicConfig(
    filename='logfile.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context):
    user = update.effective_user
    update.message.reply_text(f'Привет {user.full_name}!')


def helpCommand(update: Update, context):
    update.message.reply_text('Help!')


def findPhoneNumbersCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')

    return 'findPhoneNumbers'

def findEmailCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска email: ')

    return 'findEmail'

def verifyPasswordCommand(update: Update, context):
    update.message.reply_text('Введите текст для проверки пароля: ')

    return 'verifyPassword'

def getReleaseCommand(update: Update, context):
    update.message.reply_text('Подтвердите действие(Y/N): ')

    return 'getRelease'

def getUnameCommand(update: Update, context):
    update.message.reply_text('Подтвердите действие(Y/N): ')

    return 'getUname'

def getUptimeCommand(update: Update, context):
    update.message.reply_text('Подтвердите действие(Y/N): ')

    return 'getUptime'

def getDfCommand(update: Update, context):
    update.message.reply_text('Подтвердите действие(Y/N): ')

    return 'getDf'

def getFreeCommand(update: Update, context):
    update.message.reply_text('Подтвердите действие(Y/N): ')

    return 'getFree'

def getMpstatCommand(update: Update, context):
    update.message.reply_text('Подтвердите действие(Y/N): ')

    return 'getMpstat'

def getWCommand(update: Update, context):
    update.message.reply_text('Подтвердите действие(Y/N): ')

    return 'getW'

def getAuthsCommand(update: Update, context):
    update.message.reply_text('Подтвердите действие(Y/N): ')

    return 'getAuths'
def getCriticalCommand(update: Update, context):
    update.message.reply_text('Подтвердите действие(Y/N): ')

    return 'getCritical'
def getPsCommand(update: Update, context):
    update.message.reply_text('Подтвердите действие(Y/N): ')

    return 'getPs'

def getSsCommand(update: Update, context):
    update.message.reply_text('Подтвердите действие(Y/N): ')

    return 'getSs'

def getServicesCommand(update: Update, context):
    update.message.reply_text('Подтвердите действие(Y/N): ')

    return 'getServices'

def getAptListCommand(update: Update, context):
    update.message.reply_text('Напишите \'all\', если хотите узнать информацию о всех пакетах или название конкретного пакета для вывода информации только о нем')

    return ('getAptList')

def getEmailsCommand(update: Update, context):
    update.message.reply_text('Подтвердите действие(Y/N): ')

    return 'getEmails'
def getPhoneNumbersCommand(update: Update, context):
    update.message.reply_text('Подтвердите действие(Y/N): ')

    return 'getPhoneNumbers'

def getReplLogsCommand(update: Update, context):
    update.message.reply_text('Подтвердите действие(Y/N): ')

    return 'getReplLogs'
def findPhoneNumbers(update: Update, context):
    user_input = update.message.text  # Получаем текст, содержащий(или нет) номера телефонов

    phoneNumRegex = re.compile(r'(8|\+7)( \d{3} \d{3} \d{2} \d{2}|\d{10}| \(\d{3}\) \d{3} \d{2} \d{2}|\(\d{3}\)\d{7}|-\d{3}-\d{3}-\d{2}-\d{2})')  # формат 8 (000) 000-00-00
    #phoneNumRegex = re.compile(r'8 \(\d{3}\) \d{3}-\d{2}-\d{2}')  # формат 8 (000) 000-00-00

    phoneNumberList = phoneNumRegex.findall(user_input)  # Ищем номера телефонов

    if not phoneNumberList:  # Обрабатываем случай, когда номеров телефонов нет
        update.message.reply_text('Телефонные номера не найдены')
        return  ConversationHandler.END# Завершаем выполнение функции

    phoneNumbers = ''  # Создаем строку, в которую будем записывать номера телефонов
    phoneNumbersList = list()
    for i in range(len(phoneNumberList)):
        phoneNumberRow = f'{i + 1}. {phoneNumberList[i][0]}{phoneNumberList[i][1]}'
        phoneNumbersList.append(f'{phoneNumberList[i][0]}{phoneNumberList[i][1]}')
        phoneNumbers += f'{phoneNumberRow}\n'  # Записываем очередной номер

    phoneNumbers += '\nCохраняем найденные телефоны в базу данных\n'
    update.message.reply_text(phoneNumbers)  # Отправляем сообщение пользователю
    connection = None

    try:
        load_dotenv()
        host = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')
        username = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        database = os.getenv('DB_DATABASE')
        connection = psycopg2.connect(user=username,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)

        cursor = connection.cursor()
        for elem in phoneNumbersList:
            cursor.execute(f"INSERT INTO Phones (phonename) VALUES ('{elem}');")
        connection.commit()
        logging.info("Команда успешно выполнена")
        update.message.reply_text("Успешно сохранено")
    except (Exception, Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
        update.message.reply_text("Возникла ошибка при работе с базой данных")
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
    return ConversationHandler.END  # Завершаем работу обработчика диалога

def findEmail(update: Update, context):
    user_input = update.message.text  # Получаем текст, содержащий(или нет) номера телефонов

    emailRegex = re.compile(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

    emailList = emailRegex.findall(user_input)  # Ищем номера телефонов

    if not emailList:  # Обрабатываем случай, когда номеров телефонов нет
        update.message.reply_text('Email не найдены')
        return ConversationHandler.END # Завершаем выполнение функции

    emailResults = ''  # Создаем строку, в которую будем записывать номера телефонов
    emails = list()
    for i in range(len(emailList)):
        emails.append(f'{emailList[i]}')
        emailResults += f'{i + 1}. {emailList[i]}\n'  # Записываем очередной номер

    emailResults += '\nCохраняем найденные email в базу данных\n'
    update.message.reply_text(emailResults)  # Отправляем сообщение пользователю
    connection = None

    try:
        load_dotenv()
        host = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')
        username = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        database = os.getenv('DB_DATABASE')
        connection = psycopg2.connect(user=username,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)

        cursor = connection.cursor()
        for elem in emails:
            cursor.execute(f"INSERT INTO Emails (EmailName) VALUES ('{elem}');")
        connection.commit()
        logging.info("Команда успешно выполнена")
        update.message.reply_text("Успешно сохранено")
    except (Exception, Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
        update.message.reply_text("Возникла ошибка при работе с базой данных")
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
    return ConversationHandler.END  # Завершаем работу обработчика диалога


def verifyPassword(update: Update, context):
    user_input = update.message.text  # Получаем текст, содержащий(или нет) номера телефонов

    passwordRegex = re.compile(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()])[A-Za-z\d!@#$%^&*()]{8,}$')

    answer= ''
    if passwordRegex.match(user_input) is None:
        answer = 'Пароль простой'
    else:
        answer = 'Пароль сложный'

    update.message.reply_text(answer)  # Отправляем сообщение пользователю
    return ConversationHandler.END  # Завершаем работу обработчика диалога


def getRelease(update : Update, context):
    user_input = update.message.text
    if user_input != 'y' and user_input != 'Y':
        update.message.reply_text("Команда прервана")
        return ConversationHandler.END
    load_dotenv()
    host = os.getenv('RM_HOST')
    port = os.getenv('RM_PORT')
    username = os.getenv('RM_USER')
    password = os.getenv('RM_PASSWORD')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('hostnamectl')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def getUname(update : Update, context):
    user_input = update.message.text
    if user_input != 'y' and user_input != 'Y':
        update.message.reply_text("Команда прервана")
        return ConversationHandler.END
    load_dotenv()
    host = os.getenv('RM_HOST')
    port = os.getenv('RM_PORT')
    username = os.getenv('RM_USER')
    password = os.getenv('RM_PASSWORD')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('lscpu && hostname')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def getUptime(update : Update, context):
    user_input = update.message.text
    if user_input != 'y' and user_input != 'Y':
        update.message.reply_text("Команда прервана")
        return ConversationHandler.END
    load_dotenv()
    host = os.getenv('RM_HOST')
    port = os.getenv('RM_PORT')
    username = os.getenv('RM_USER')
    password = os.getenv('RM_PASSWORD')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('uptime')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def getDf(update : Update, context):
    user_input = update.message.text
    if user_input != 'y' and user_input != 'Y':
        update.message.reply_text("Команда прервана")
        return ConversationHandler.END
    load_dotenv()
    host = os.getenv('RM_HOST')
    port = os.getenv('RM_PORT')
    username = os.getenv('RM_USER')
    password = os.getenv('RM_PASSWORD')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('df')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def getFree(update : Update, context):
    user_input = update.message.text
    if user_input != 'y' and user_input != 'Y':
        update.message.reply_text("Команда прервана")
        return ConversationHandler.END
    load_dotenv()
    host = os.getenv('RM_HOST')
    port = os.getenv('RM_PORT')
    username = os.getenv('RM_USER')
    password = os.getenv('RM_PASSWORD')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('free -h')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def getMpstat(update : Update, context):
    user_input = update.message.text
    if user_input != 'y' and user_input != 'Y':
        update.message.reply_text("Команда прервана")
        return ConversationHandler.END
    load_dotenv()
    host = os.getenv('RM_HOST')
    port = os.getenv('RM_PORT')
    username = os.getenv('RM_USER')
    password = os.getenv('RM_PASSWORD')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('mpstat')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def getW(update : Update, context):
    user_input = update.message.text
    if user_input != 'y' and user_input != 'Y':
        update.message.reply_text("Команда прервана")
        return ConversationHandler.END
    load_dotenv()
    host = os.getenv('RM_HOST')
    port = os.getenv('RM_PORT')
    username = os.getenv('RM_USER')
    password = os.getenv('RM_PASSWORD')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('w')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def getAuths(update : Update, context):
    user_input = update.message.text
    if user_input != 'y' and user_input != 'Y':
        update.message.reply_text("Команда прервана")
        return ConversationHandler.END
    load_dotenv()
    host = os.getenv('RM_HOST')
    port = os.getenv('RM_PORT')
    username = os.getenv('RM_USER')
    password = os.getenv('RM_PASSWORD')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('last -n 20')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END
def getCritical(update : Update, context):
    user_input = update.message.text
    if user_input != 'y' and user_input != 'Y':
        update.message.reply_text("Команда прервана")
        return ConversationHandler.END
    load_dotenv()
    host = os.getenv('RM_HOST')
    port = os.getenv('RM_PORT')
    username = os.getenv('RM_USER')
    password = os.getenv('RM_PASSWORD')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('journalctl -r -p crit -n 5')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def getPs(update : Update, context):
    user_input = update.message.text
    if user_input != 'y' and user_input != 'Y':
        update.message.reply_text("Команда прервана")
        return ConversationHandler.END
    load_dotenv()
    host = os.getenv('RM_HOST')
    port = os.getenv('RM_PORT')
    username = os.getenv('RM_USER')
    password = os.getenv('RM_PASSWORD')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('ps')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def getSs(update : Update, context):
    user_input = update.message.text
    if user_input != 'y' and user_input != 'Y':
        update.message.reply_text("Команда прервана")
        return ConversationHandler.END
    load_dotenv()
    host = os.getenv('RM_HOST')
    port = os.getenv('RM_PORT')
    username = os.getenv('RM_USER')
    password = os.getenv('RM_PASSWORD')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('ss -s')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def getServices(update : Update, context):
    user_input = update.message.text
    if user_input != 'y' and user_input != 'Y':
        update.message.reply_text("Команда прервана")
        return ConversationHandler.END
    load_dotenv()
    host = os.getenv('RM_HOST')
    port = os.getenv('RM_PORT')
    username = os.getenv('RM_USER')
    password = os.getenv('RM_PASSWORD')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('service --status-all')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
    return ConversationHandler.END

def getAptList(update : Update, context):
    user_input = update.message.text
    load_dotenv()
    host = os.getenv('RM_HOST')
    port = os.getenv('RM_PORT')
    username = os.getenv('RM_USER')
    password = os.getenv('RM_PASSWORD')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    if user_input != 'all':
        stdin, stdout, stderr = client.exec_command(f'dpkg --get-selections | grep {user_input}')
        data = stdout.read() + stderr.read()
        client.close()
        data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
        update.message.reply_text(data)
        return ConversationHandler.END
    else:
        stdin, stdout, stderr = client.exec_command('dpkg --get-selections | head -50')
        data = stdout.read() + stderr.read()
        client.close()
        data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
        update.message.reply_text(data)
        return ConversationHandler.END

def getEmails(update : Update, context):
    user_input = update.message.text
    if user_input != 'y' and user_input != 'Y':
        update.message.reply_text("Команда прервана")
        return ConversationHandler.END
    connection = None

    try:
        load_dotenv()
        host = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')
        username = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        database = os.getenv('DB_DATABASE')
        connection = psycopg2.connect(user=username,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Emails;")
        data = cursor.fetchall()
        answer = ''
        for row in data:
            answer += f'{row[1]}\n'
        update.message.reply_text(answer)
        logging.info("Команда успешно выполнена")
    except (Exception, Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
    return ConversationHandler.END

def getPhoneNumbers(update : Update, context):
    user_input = update.message.text
    if user_input != 'y' and user_input != 'Y':
        update.message.reply_text("Команда прервана")
        return ConversationHandler.END
    connection = None

    try:
        load_dotenv()
        host = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')
        username = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        database = os.getenv('DB_DATABASE')
        connection = psycopg2.connect(user=username,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Phones;")
        data = cursor.fetchall()
        answer = ''
        for row in data:
            answer += f'{row[1]}\n'
        update.message.reply_text(answer)
        logging.info("Команда успешно выполнена")
    except (Exception, Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
    return ConversationHandler.END

def getReplLogs(update : Update, context):
    user_input = update.message.text
    if user_input != 'y' and user_input != 'Y':
        update.message.reply_text("Команда прервана")
        return ConversationHandler.END
    load_dotenv()
    host = os.getenv('RM_HOST')
    port = os.getenv('RM_PORT')
    username = os.getenv('RM_USER')
    password = os.getenv('RM_PASSWORD')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('cat /tmp/postgresql/postgresql.log | grep repl')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    #command = "cat /tmp/postgresql/postgresql.log | grep repl | tail -n 15"
    #res = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #if res.returncode != 0 or res.stderr.decode() != "":
    #    update.message.reply_text("Can not open log file!")
    #else:
    #    update.message.reply_text(res.stdout.decode().strip('\n'))
    update.message.reply_text(data)
    return ConversationHandler.END
def echo(update: Update, context):
    update.message.reply_text(update.message.text)


def main():
    updater = Updater(TOKEN, use_context=True)

    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher

    # Обработчик диалога
    convHandlerFindPhoneNumbers = ConversationHandler(
        entry_points=[CommandHandler('find_phone_number', findPhoneNumbersCommand)],
        states={
            'findPhoneNumbers': [MessageHandler(Filters.text & ~Filters.command, findPhoneNumbers)],
        },
        fallbacks=[]
    )

    convHandlerFindEmail = ConversationHandler(
        entry_points=[CommandHandler('find_email', findEmailCommand)],
        states={
            'findEmail': [MessageHandler(Filters.text & ~Filters.command, findEmail)],
        },
        fallbacks=[]
    )

    convHandlerVerifyPassword = ConversationHandler(
        entry_points=[CommandHandler('verify_password', verifyPasswordCommand)],
        states={
            'verifyPassword': [MessageHandler(Filters.text & ~Filters.command, verifyPassword)],
        },
        fallbacks=[]
    )

    convHandlerGetRelease = ConversationHandler(
        entry_points=[CommandHandler('get_release', getReleaseCommand)],
        states={
            'getRelease': [MessageHandler(Filters.text & ~Filters.command, getRelease)],
        },
        fallbacks=[]
    )
    convHandlerGetUname = ConversationHandler(
        entry_points=[CommandHandler('get_uname', getUnameCommand)],
        states={
            'getUname': [MessageHandler(Filters.text & ~Filters.command, getUname)],
        },
        fallbacks=[]
    )
    convHandlerGetUptime = ConversationHandler(
        entry_points=[CommandHandler('get_uptime', getUptimeCommand)],
        states={
            'getUptime': [MessageHandler(Filters.text & ~Filters.command, getUptime)],
        },
        fallbacks=[]
    )
    convHandlerGetDf = ConversationHandler(
        entry_points=[CommandHandler('get_df', getDfCommand)],
        states={
            'getDf': [MessageHandler(Filters.text & ~Filters.command, getDf)],
        },
        fallbacks=[]
    )
    convHandlerGetFree = ConversationHandler(
        entry_points=[CommandHandler('get_free', getFreeCommand)],
        states={
            'getFree': [MessageHandler(Filters.text & ~Filters.command, getFree)],
        },
        fallbacks=[]
    )
    convHandlerGetMpstat = ConversationHandler(
        entry_points=[CommandHandler('get_mpstat', getMpstatCommand)],
        states={
            'getMpstat': [MessageHandler(Filters.text & ~Filters.command, getMpstat)],
        },
        fallbacks=[]
    )
    convHandlerGetW = ConversationHandler(
        entry_points=[CommandHandler('get_w', getWCommand)],
        states={
            'getW': [MessageHandler(Filters.text & ~Filters.command, getW)],
        },
        fallbacks=[]
    )
    convHandlerGetAuths = ConversationHandler(
        entry_points=[CommandHandler('get_auths', getAuthsCommand)],
        states={
            'getAuths': [MessageHandler(Filters.text & ~Filters.command, getAuths)],
        },
        fallbacks=[]
    )
    convHandlerGetCritical = ConversationHandler(
        entry_points=[CommandHandler('get_critical', getCriticalCommand)],
        states={
            'getCritical': [MessageHandler(Filters.text & ~Filters.command, getCritical)],
        },
        fallbacks=[]
    )
    convHandlerGetPs = ConversationHandler(
        entry_points=[CommandHandler('get_ps', getPsCommand)],
        states={
            'getPs': [MessageHandler(Filters.text & ~Filters.command, getPs)],
        },
        fallbacks=[]
    )
    convHandlerGetSs = ConversationHandler(
        entry_points=[CommandHandler('get_ss', getSsCommand)],
        states={
            'getSs': [MessageHandler(Filters.text & ~Filters.command, getSs)],
        },
        fallbacks=[]
    )
    convHandlerGetServices = ConversationHandler(
        entry_points=[CommandHandler('get_services', getServicesCommand)],
        states={
            'getServices': [MessageHandler(Filters.text & ~Filters.command, getServices)],
        },
        fallbacks=[]
    )
    convHandlerGetAptList = ConversationHandler(
        entry_points=[CommandHandler('get_apt_list', getAptListCommand)],
        states={
            'getAptList': [MessageHandler(Filters.text & ~Filters.command, getAptList)],
        },
        fallbacks=[]
    )
    convHandlerGetEmails = ConversationHandler(
        entry_points=[CommandHandler('get_emails', getEmailsCommand)],
        states={
            'getEmails': [MessageHandler(Filters.text & ~Filters.command, getEmails)],
        },
        fallbacks=[]
    )
    convHandlerGetPhoneNumbers = ConversationHandler(
        entry_points=[CommandHandler('get_phone_numbers', getPhoneNumbersCommand)],
        states={
            'getPhoneNumbers': [MessageHandler(Filters.text & ~Filters.command, getPhoneNumbers)],
        },
        fallbacks=[]
    )
    convHandlerGetReplLogs = ConversationHandler(
        entry_points=[CommandHandler('get_repl_logs', getReplLogsCommand)],
        states={
            'getReplLogs': [MessageHandler(Filters.text & ~Filters.command, getReplLogs)],
        },
        fallbacks=[]
    )
    # Регистрируем обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", helpCommand))
    dp.add_handler(convHandlerFindPhoneNumbers)
    dp.add_handler(convHandlerFindEmail)
    dp.add_handler(convHandlerVerifyPassword)
    dp.add_handler(convHandlerGetRelease)
    dp.add_handler(convHandlerGetUname)
    dp.add_handler(convHandlerGetUptime)
    dp.add_handler(convHandlerGetDf)
    dp.add_handler(convHandlerGetFree)
    dp.add_handler(convHandlerGetMpstat)
    dp.add_handler(convHandlerGetW)
    dp.add_handler(convHandlerGetAuths)
    dp.add_handler(convHandlerGetCritical)
    dp.add_handler(convHandlerGetPs)
    dp.add_handler(convHandlerGetSs)
    dp.add_handler(convHandlerGetServices)
    dp.add_handler(convHandlerGetAptList)
    dp.add_handler(convHandlerGetEmails)
    dp.add_handler(convHandlerGetPhoneNumbers)
    dp.add_handler(convHandlerGetReplLogs)

    # Регистрируем обработчик текстовых сообщений
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Запускаем бота
    updater.start_polling()

    # Останавливаем бота при нажатии Ctrl+C
    updater.idle()


if __name__ == '__main__':
    main()
