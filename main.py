import os

from game.models import Food, Medicine
from game.tamagochi import BasicTamagochi
from game.clicker import Clicker
from game.game import Game
from game.exceptions import NotEnoughMoney, TamagochiIsGone


def main():
    all_food = [
        Food(name='Бургер', satiety=20, price=40),
        Food(name='Салат', satiety=10, price=20),
        Food(name='Яблоко', satiety=10, price=15)
    ]

    all_medicine = [
        Medicine(name='Ибупрофен', price=30, heal_hp=20, number_of_uses=2)
    ]

    tamagochi = BasicTamagochi("Бакс")

    clicker = Clicker(income_per_click=10, initial_coins=20)

    #  Вместо AbstractGame импортируйте
    #  и создайте инстанс от своей реализации
    game = Game(
        tamagochi,
        clicker,
        all_food=all_food,
        all_medicine=all_medicine
    )

    print("Добро пожаловать в Тамагочи-кликер!")
    output = ''

    while True:
        print(output)

        print(f"Сумка с едой: {game.food}")
        print(f"Сумка с лекарствами: {game.medicine}")

        status = game.get_status()
        print(
            f"\nСтатус: голод {status['hunger']}, здоровье {status['hp']}, "
            f"энергия {status['mood']}, монет {status['coins']}\n"
        )
        if game.tamagochi.is_sick():
            print("=======Тамагочи болеет======")
            print("=======Отдых действует менее эффективно=======")
        print("1. Пойти на работу")
        print("2. Купить еду")
        print("3. Купить лекарство")
        print("4. Покормить")
        print("5. Вылечить")
        print("6. Играть")
        print("7. Отдых")
        print("0. Выход")


        try:
            choice = input("Выберите действие: ")
            match choice:
                case "1":
                    income = game.work()
                    output = f'Вы заработали {income} монет'
                    game.tamagochi.update()
                case "2":
                    game.buy_food()
                    output = 'Еда куплена'
                case "3":
                    game.buy_medicine()
                    output = 'Лекарство куплено'
                case "4":
                    game.feed_tamagochi()
                    output = 'Вы покормили питомца'
                case "5":
                    game.heal_tamagochi()
                    output = 'Вы вылечили питомца'
                case "6":
                    game.play_with_tamagochi()
                    output = 'Вы поиграли с питомцем'
                case "7":
                    game.rest_tamagochi()
                    output = 'Питомец отдохнул'
                case "0":
                    break
                case _:
                    output = 'Неверная команда'
        except NotEnoughMoney as error:
            output = str(error)
        except TamagochiIsGone as error:
            output = str(error)
        except ValueError as error:
            output = str(error)
        
        os.system('clear')


if __name__ == '__main__':
    main()
