import asyncio
import random
import time
from kahoot import client  # pip install kahoot-py

async def create_bot(pin, bot_id, name_prefix, vote_mode):
    try:
        bot_name = f"{name_prefix}{bot_id}_{random.randint(100,999)}"
        bot = client.Client()
        
        await bot.join(pin, bot_name)
        print(f"✅ {bot_name} присоединился")
        
        @bot.event
        async def on_question(question):
            await asyncio.sleep(random.uniform(1.2, 3.8))  # имитация человека
            
            if not question.get("choices"):
                return
                
            num_choices = len(question["choices"])
            
            if vote_mode == "random":
                answer = random.randint(0, num_choices - 1)
            elif vote_mode == "fixed":
                answer = 0  # всегда первый вариант (A)
            elif vote_mode == "last":
                answer = num_choices - 1  # всегда последний
            else:
                answer = random.randint(0, num_choices - 1)
            
            await bot.answer(answer)
            # print(f"{bot_name} ответил: {answer+1}")
        
        await bot.run()
    except Exception as e:
        print(f"❌ {bot_name} ошибка: {e}")

async def main():
    print("="*50)
    print("       Kahoot Bot Flooder с меню")
    print("="*50)
    
    pin = int(input("Введите PIN-код игры: "))
    
    name_prefix = input("Префикс ника ботов (например Bot_ или Player): ") or "Bot_"
    
    print("\nВыберите режим голосования:")
    print("1. Случайно")
    print("2. Всегда первый вариант (A)")
    print("3. Всегда последний вариант")
    mode_choice = input("Выберите (1-3): ").strip()
    
    if mode_choice == "2":
        vote_mode = "fixed"
    elif mode_choice == "3":
        vote_mode = "last"
    else:
        vote_mode = "random"
    
    num_bots = int(input("\nСколько ботов запустить? (рекомендую начинать с 10-30): "))
    
    print(f"\nЗапускаем {num_bots} ботов с префиксом '{name_prefix}'...")
    print("Режим голосования:", vote_mode)
    print("-" * 50)
    
    tasks = []
    for i in range(num_bots):
        tasks.append(create_bot(pin, i + 1, name_prefix, vote_mode))
        
        # Плавный запуск, чтобы не убить соединение
        if i % 15 == 0 and i > 0:
            await asyncio.sleep(1.5)
    
    await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == "__main__":
    asyncio.run(main())
