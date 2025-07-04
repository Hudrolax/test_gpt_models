import asyncio
import os
from getpass import getpass

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = getpass("Enter your OpenAI API key: ")

@tool()
async def add(a: int, b: int) -> int:
    """Складывает два числа."""
    print('Вызов сложения', a, b)
    return a + b

@tool()
async def multiply(a: int, b: int) -> int:
    """Умножает два числа."""
    print('Вызов умножения', a, b)
    return a * b

@tool()
async def return_prepared_answer(answer: int) -> str:
    """Подготавливает результат к выводу."""
    print('Вызов выводы результата', answer)
    return f"Мой ответ: {answer} !!!"

async def llm_work() -> None:
    tools = [add, multiply, return_prepared_answer]

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt="Ты помощник, который решает арифметические задачи по цепочке инструментов."
    )

    query = "Сколько будет (2+2)*5?"
    state = await agent.ainvoke({"messages": [("human", query)]})

    final_answer = state["messages"][-1].content
    print("Result:", final_answer)

async def cycle() -> None:
    for i in range(10):
        print(i)
        await asyncio.sleep(0.5)

async def main() -> None:
    await asyncio.gather(
        llm_work(),
        cycle()
    )

if __name__ == '__main__':
    asyncio.run(main())
