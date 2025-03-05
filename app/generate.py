from openai import AsyncOpenAI
from config import AI_TOKEN

client = AsyncOpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=AI_TOKEN,
)

async def ai_generate(text: str):
    try:
        completion = await client.chat.completions.create( 
            model="deepseek/deepseek-chat",
            messages=[
                {
                    "role": "user",
                    "content": text
                }
            ]
        )
        print(completion)
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Ошибка при генерации ответа: {e}")
        return "Произошла ошибка при генерации ответа."