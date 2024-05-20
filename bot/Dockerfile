# указываем версию python
FROM python:3.9-slim
# указываем рабочую директорию
WORKDIR /bot
# копируем файлы из нашей директории в такую же директорию контейнера
COPY . .
# устанавливаем необходимые библиотеки и зависимости для работы бота
RUN pip install --no-cache-dir -r requirements.txt
# запускаем бота
CMD ["python", "./bot.py"]
