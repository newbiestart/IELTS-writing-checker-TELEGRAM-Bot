import asyncio
import base64
import requests

from aiogram import Bot, Dispatcher, types, Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram import F
from aiogram.enums import ChatMemberStatus

from config import BOT_TOKEN, GEMINI_API_KEY, CHANNEL_USERNAME
# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
router = Router()
dp = Dispatcher(storage=MemoryStorage())

# Define states for the conversation flow
class IELTSStates(StatesGroup):
    task1_image = State()
    task1_essay = State()
    task2_topic = State()
    task2_essay = State()

# --- Keyboards ---
main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="IELTS check")]],
    resize_keyboard=True
)

ielts_check_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Task 1"), KeyboardButton(text="Task 2")],
        [KeyboardButton(text="Back")]
    ],
    resize_keyboard=True
)

@router.message.middleware()
async def subscription_check(handler, event, data):
    message = event
    user_id = message.from_user.id

    if message.text in ["/start", "IELTS check", "Back"]:
        return await handler(event, data)

    try:
        member = await message.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED]:
            await message.answer(
                f"Please subscribe to our channel to use this bot: {CHANNEL_USERNAME}\n\n"
                "After subscribing, you can continue to use the bot.",
                disable_web_page_preview=True
            )
        else:
            return await handler(event, data)
    except Exception as e:
        print(f"Error during subscription check: {e}")
        await message.answer("An error occurred. Please try again later.")

# --- Handlers ---
@router.message(Command('start'))
async def start_command(message: types.Message):
    await message.answer(
        "👋 Welcome! I'm your AI IELTS Writing assistant. I can evaluate your Task 1 "
        "and Task 2 essays using the power of Gemini 2.0 Flash AI. I'll provide a "
        "detailed report with a band score and feedback, just like a real examiner. "
        "Ready to improve your writing? 🚀",
        reply_markup=main_menu_kb
    )

@router.message(F.text == "IELTS check")
async def ielts_check_menu(message: types.Message):
    await message.answer("Choose a task to get started:", reply_markup=ielts_check_kb)

@router.message(F.text == "Back")
async def back_to_main_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Returning to the main menu.", reply_markup=main_menu_kb)

@router.message(F.text == "Task 1")

@router.message(F.text == "Task 1")
async def task1_start(message: types.Message, state: FSMContext):
    await state.set_state(IELTSStates.task1_image)
    await message.answer("Please send me the **image** for your Task 1 essay (e.g., graph, chart, map).", reply_markup=types.ReplyKeyboardRemove())

@router.message(IELTSStates.task1_image, F.photo)
async def task1_receive_image(message: types.Message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id
    await state.update_data(photo_file_id=photo_file_id)
    await state.set_state(IELTSStates.task1_essay)
    await message.answer("Great! Now, please send me your **Task 1 essay** in text format.")
async def task1_receive_essay(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    photo_file_id = user_data.get('photo_file_id')
    essay_text = message.text

    await message.answer("Your Task 1 essay is being evaluated. This may take a moment...", reply_markup=main_menu_kb)
    
    await state.clear()
    
    try:
        gemini_response = await evaluate_essay_with_gemini(message.bot, photo_file_id, essay_text, is_task1=True)
        await message.answer(gemini_response)
    except Exception as e:
        await message.answer(f"An error occurred during evaluation: {e}")

# --- Task 2 Flow ---
@router.message(F.text == "Task 2")
async def task2_start(message: types.Message, state: FSMContext):
    await state.set_state(IELTSStates.task2_topic)
    await message.answer("Please send me the **topic** for your Task 2 essay.", reply_markup=types.ReplyKeyboardRemove())

@router.message(IELTSStates.task2_topic, F.text)
async def task2_receive_topic(message: types.Message, state: FSMContext):
    essay_topic = message.text
    await state.update_data(essay_topic=essay_topic)
    await state.set_state(IELTSStates.task2_essay)
    await message.answer("Got it. Now, please send me your **Task 2 essay** in text format.")

@router.message(IELTSStates.task2_essay, F.text)
async def task2_receive_essay(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    essay_topic = user_data.get('essay_topic')
    essay_text = message.text

    await message.answer("Your Task 2 essay is being evaluated. This may take a moment...", reply_markup=main_menu_kb)
    
    await state.clear()

    try:
        gemini_response = await evaluate_essay_with_gemini(message.bot, None, essay_text, is_task1=False, topic=essay_topic)
        await message.answer(gemini_response)
    except Exception as e:
        await message.answer(f"An error occurred during evaluation: {e}")


async def evaluate_essay_with_gemini(bot: Bot, photo_file_id: str, essay: str, is_task1: bool, topic: str = None):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY
    }

    prompt_prefix = "You are a professional IELTS examiner. Evaluate the following essay based on the IELTS Writing band descriptors (Task Achievement, Cohesion and Coherence, Lexical Resource, Grammatical Range and Accuracy). Provide a band score for each criterion and an overall band score. Then, give detailed feedback on strengths and weaknesses and suggest improvements.\n\n"
    
    if is_task1:
        file_info = await bot.get_file(photo_file_id)
        photo_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"
        
        response = requests.get(photo_url)
        response.raise_for_status()
        image_data = response.content
        
        base64_image = base64.b64encode(image_data).decode('utf-8')
        
        data = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt_prefix + "Here is the image for the task."},
                        {"inline_data": {"mime_type": "image/jpeg", "data": base64_image}},
                        {"text": f"Here is the essay to be evaluated:\n\n{essay}"}
                    ]
                }
            ]
        }
    else:
        full_prompt = (
            f"{prompt_prefix}The essay topic is: **{topic}**\n\n"
            f"Here is the essay to be evaluated:\n\n{essay}"
        )
        data = {
            "contents": [
                {
                    "parts": [{"text": full_prompt}]
                }
            ]
        }
        
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    result = response.json()
    gemini_text_response = result['candidates'][0]['content']['parts'][0]['text']
    
    return gemini_text_response

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
