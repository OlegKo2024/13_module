import asyncio
import time

print('Асинхронные силачи')


async def start_strongman(name, power, balls=5):
    print(f'Силач {name} начал соревнования')
    for i in range(1, 6):
        print(f'Силач {name} поднял {i}')
        await asyncio.sleep(balls / power)
    print(f'Силач {name} закончил соревнования')


async def start_tournament():
    power_man_1 = asyncio.create_task(start_strongman('Pasha', 3))
    power_man_2 = asyncio.create_task(start_strongman('Denis', 4))
    power_man_3 = asyncio.create_task(start_strongman('Apollon', 5))
    await power_man_1
    await power_man_2
    await power_man_3


start = time.time()
asyncio.run(start_tournament())
end = time.time()
print(f'Working = {round(end - start, 2)}')
