import os
from getpass import getpass

from langchain_core.tools import tool
from langchain_deepseek.chat_models import ChatDeepSeek
from langgraph.prebuilt import create_react_agent

# 1) API-ключ DeepSeek
if "DEEPSEEK_API_KEY" not in os.environ:
    os.environ["DEEPSEEK_API_KEY"] = getpass("Enter your DeepSeek API key: ")

# 2) Определяем инструменты
@tool()
def add(a: int, b: int) -> int:
    """Складывает два числа."""
    return a + b

@tool()
def multiply(a: int, b: int) -> int:
    """Умножает два числа."""
    return a * b

@tool()
def return_prepared_answer(answer: int) -> str:
    """Подготавливает результат к выводу."""
    return f"Мой ответ: {answer} !!!"

tools = [add, multiply, return_prepared_answer]

llm = ChatDeepSeek(model="deepseek-chat", temperature=0)

# 4) Инициализируем LangGraph-агента
agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt="Ты помощник, который решает арифметические задачи по цепочке инструментов."
)

# 5) Запускаем агента на вопросе
query = "Сколько будет (2+2)*5?"
state = agent.invoke({"messages": [("human", query)]})

# 6) Извлекаем финальный ответ из истории сообщений
final_answer = state["messages"][-1].content
print("Result:", final_answer)
