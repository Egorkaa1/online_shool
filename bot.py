from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes

TOKEN = 'Token bot'  

schedule = {
    "Понедельник 🎀 ": "09:00 - Математика\n10:30 - Русский язык\n12:00 - Физика",
    "Вторник 🎀 ": "09:00 - Английский язык\n10:30 - Химия\n12:00 - История",
    "Среда 🎀 ": "09:00 - География\n10:30 - Литература\n12:00 - Информатика",
    "Четверг 🎀 ": "09:00 - Биология\n10:30 - Физкультура\n12:00 - Искусство",
    "Пятница 🎀 ": "09:00 - Математика\n10:30 - Английский язык\n12:00 - Русский язык"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    welcome_text = f"Привет, {user.first_name}! Я — ваш ботик  онлайн-школе.\n" \
                   "Вы можете узнать расписание уроков, отправить обратную связь или получить информацию о преподавателях."
    
    keyboard = [
        [KeyboardButton("Расписание 🎀")],
        [KeyboardButton("Обратная связь 🎀")],
        [KeyboardButton("Преподаватели 🎀")]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
   
    if text == "Расписание":
        schedule_text = "\n".join([f"{day}: {lessons}" for day, lessons in schedule.items()])
        await update.message.reply_text(f"Расписание уроков:\n{schedule_text}")
    
    elif text == "Обратная связь":
        await update.message.reply_text("Прошу, напишите вашу обратную связь о курсе:")
        context.user_data['waiting_for_feedback'] = True
    
    elif text == "Преподаватели":
        teachers_info = """Информация об учителях:
        
1. Иванов И  — Математика и Физика
2. Елена Б  — Русский язык и Литература
3. Сидоров С — Английский язык и История
4. Карина М  — Биология и Химия
        
Если у вас появились вопросики к учителям,прошу напишите их здесь)
"""
        await update.message.reply_text(teachers_info)
    
    else:
       
        if context.user_data.get('waiting_for_feedback'):
            feedback_message = text
          
            await update.message.reply_text("Пасибки за вашу обратную связь!")
            context.user_data['waiting_for_feedback'] = False
        else:
            await update.message.reply_text("Сори,я не понял(а) ваш запрос. Прошу, используйте кнопочки меню ☹️")

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    
  
    application.add_handler(MessageHandler(None, handle_message))
    
    application.run_polling()

if __name__ == '__main__':
    main()