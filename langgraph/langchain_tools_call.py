# Этот модуль демонстрирует вызов моделью цепочки инструментов для достижения результата.

from langchain.agents import AgentType, initialize_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


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

# llm_with_tools = llm.bind_tools(tools)
#
# result = llm_with_tools.invoke(
#     "Сколько будет (2+2)*5?"
# )

agent = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.OPENAI_FUNCTIONS, 
    verbose=False
)

result = agent.invoke(
    input={'input': "Сколько будет (2+2)*5?"},
    recursion_limit=25,
)

print('result:', result)
