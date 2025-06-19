# Этот модуль демонстрирует вызов моделью цепочки инструментов для достижения результата.

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import initialize_agent, AgentType


@tool
def add(a: int, b: int) -> int:
    """Складывает 2 числа"""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Умножает 2 числа"""
    return a * b

@tool
def return_prepared_answer(answer: int) -> str:
    """Подготоваливает результат к выводу"""
    return f'Мой ответ: {answer} !!!'

tools = [add, multiply, return_prepared_answer]
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

agent = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.OPENAI_FUNCTIONS, 
    verbose=True
)

result = agent.run("Сколько будет (2+2)*5?")

print('result:', result)
