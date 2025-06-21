import asyncio

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent


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
    print('Вызов вывода результата', answer)
    return f"Мой ответ: {answer} !!!"

async def llm_start() -> None:
    print('start llm')
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

async def just_a_cycle() -> None:
    for i in range(10):
        print('iteration', i)
        await asyncio.sleep(1)

async def main() -> None:
    await asyncio.gather(
        llm_start(),
        just_a_cycle(),
    )


if __name__ == "__main__":
    asyncio.run(main())
