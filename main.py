import os

from game.models import Food, Medicine
from game.tamagochi import BasicTamagochi
from game.clicker import Clicker
from game.game import Game
from game.exceptions import GameError


MENU = "\n".join([
    "1. Пойти на работу",
    "2. Купить еду",
    "3. Купить лекарство",
    "4. Покормить",
    "5. Вылечить",
    "6. Играть",
    "7. Отдых",
    "0. Выход",
])


STATUS_TEMPLATE = (
    "\nСтатус: голод {hunger}, здоровье {hp}, "
    "настроение {mood}, монет {coins}\n"
)

SICK_WARNING = (
    "=======Тамагочи болеет======\n"
    "=======Отдых действует менее эффективно======="
)


def _clear_screen() -> None:
    """Очищает экран терминала."""
    os.system("cls" if os.name == "nt" else "clear")


def main():
    """Запускает основной игровой цикл."""
    all_food = [
        Food(name='Бургер', satiety=20, price=40),
        Food(name='Салат', satiety=10, price=20),
        Food(name='Яблоко', satiety=10, price=15)
    ]

    all_medicine = [
        Medicine(name='Ибупрофен', price=30, heal_hp=20, number_of_uses=2)
    ]

    tamagochi = BasicTamagochi("Бакс")
    clicker = Clicker(income_per_click=10)
    game = Game(
        tamagochi,
        clicker,
        all_food=all_food,
        all_medicine=all_medicine,
    )

    print("Добро пожаловать в Тамагочи-кликер!")
    output = ''

    while True:
        lines = [
            output,
            f"Сумка с едой: {game.food}",
            f"Сумка с лекарствами: {game.medicine}",
            STATUS_TEMPLATE.format(**game.get_status()),
        ]
        if game.tamagochi.is_sick():
            lines.append(SICK_WARNING)
        lines.append(MENU)
        print("\n".join(lines))

        try:
            match input("Выберите действие: "):
                case "1":
                    income = game.work()
                    output = f'Вы заработали {income} монет'
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
        except GameError as error:
            output = str(error)
        
        if not game.tamagochi.is_alive():
            print(f"{game.tamagochi.name} погиб. Игра окончена.")
            break

        _clear_screen()



if __name__ == '__main__':
    main()
