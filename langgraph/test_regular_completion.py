from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": "Сколько будет 2+2?"
        }
    ]
)

print(completion.choices[0].message.content)
