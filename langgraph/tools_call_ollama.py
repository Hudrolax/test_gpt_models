from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent


# 1) Инструменты остаются без изменений
@tool()
def add(a: int, b: int) -> int:
    """Складывает два числа."""
    print('Вызов сложения', a, b)
    return a + b

@tool()
def multiply(a: int, b: int) -> int:
    """Умножает два числа."""
    print('Вызов умножения', a, b)
    return a * b

@tool()
def return_prepared_answer(answer: int) -> str:
    """Форматирует итог."""
    print('Вызов выводы результата', answer)
    return f"Мой ответ: {answer} !!!"

tools = [add, multiply, return_prepared_answer]

llm = ChatOllama(model="llama3-groq-tool-use:8b")
# llm = ChatOllama(model="MFDoom/deepseek-r1-tool-calling:14b")

agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt="Ты помощник, который решает арифметические задачи по цепочке инструментов.",
)

query = "Сколько будет (2+2)*5?"
state = agent.invoke({"messages": [("human", query)]})

final_answer = state["messages"]
print("Result:", final_answer)
