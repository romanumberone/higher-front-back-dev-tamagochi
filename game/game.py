"""Модуль с интерфейсом и реализацией класса игры"""

from abc import ABC, abstractmethod
from typing import Any

from .tamagochi import AbstractTamagochi
from .clicker import AbstractClicker
from .models import Food, Medicine
from .exceptions import NotEnoughMoney


class AbstractGame(ABC):
    """Интерфейс для логики игры"""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ):
        """
        Абстрактный метод инициализации класса игры

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды
        :param all_medicine: все доступные варианты лекарств
        """
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """
        Абстрактный метод для логики действия "работа

        :return: количество заработанных монет
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Абстрактный метод для покупки еды"""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Абстрактный метод для покупки лекарства"""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Абстрактный метод для кормления тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Абстрактный метод для лечения тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self):
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self):
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """
        Абстрактный метод для получения статуса (всех характеристик) тамагочи

        :return: словарь со всеми характеристиками тамагочи
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """
        Абстрактное свойство для доступа к сумке с едой

        :return: список с имеющимися (купленными) объектами еды
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """
        Абстрактное свойство для доступа к сумке с лекарствами

        :return: список с имеющимися (купленными) объектами лекарств
        """
        raise NotImplementedError


class Game(AbstractGame):
    """Реализация логики игры"""

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ):
        """
        Инициализация класса игры

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды
        :param all_medicine: все доступные варианты лекарств
        """
        self.tamagochi = tamagochi
        self.clicker = clicker
        self._all_food = all_food
        self._all_medicine = all_medicine

        # монеты храним в игре, чтобы не зависеть от реализации кликера
        self._coins = getattr(clicker, "coins", 0)

        # сумки с купленными предметами
        self._food: list[Food] = []
        self._medicine: list[Medicine] = []

    def work(self) -> int:
        """
        Логика действия "работа"

        :return: количество заработанных монет
        """
        income = self.clicker.income_per_click
        self.clicker.click()
        self._coins += income
        return income

    def buy_food(self) -> None:
        """Покупка еды"""
        if not self._all_food:
            raise ValueError("Нет доступной еды для покупки")

        self._print_choices(self._all_food, "еды")
        index = self._ask_index(len(self._all_food))
        food = self._all_food[index]

        self.spend(food.price)
        self._food.append(food)

    def buy_medicine(self) -> None:
        """Покупка лекарства"""
        if not self._all_medicine:
            raise ValueError("Нет доступных лекарств для покупки")

        self._print_choices(self._all_medicine, "лекарств")
        index = self._ask_index(len(self._all_medicine))
        template = self._all_medicine[index]
        # копируем, чтобы у каждой покупки был свой счётчик применений
        medicine = Medicine(
            name=template.name,
            price=template.price,
            heal_hp=template.heal_hp,
            number_of_uses=template.number_of_uses,
        )

        self.spend(medicine.price)
        self._medicine.append(medicine)

    def feed_tamagochi(self) -> None:
        """Кормление тамагочи"""
        if not self._food:
            raise ValueError("В сумке нет еды")

        self._print_choices(self._food, "еды")
        index = self._ask_index(len(self._food))
        food = self._food.pop(index)

        self.tamagochi.feed(food)
        self.tamagochi.update()

    def heal_tamagochi(self) -> None:
        """Лечение тамагочи"""
        if not self._medicine:
            raise ValueError("В сумке нет лекарств")

        self._print_choices(self._medicine, "лекарств")
        index = self._ask_index(len(self._medicine))
        medicine = self._medicine[index]

        self.tamagochi.heal(medicine)

        # если лекарство закончилось — выбрасываем его из сумки
        if medicine.is_empty():
            self._medicine.pop(index)

        self.tamagochi.update()

    def rest_tamagochi(self):
        """Отдых тамагочи"""
        self.tamagochi.rest()
        self.tamagochi.update()

    def play_with_tamagochi(self):
        """Игра с тамагочи"""
        self.tamagochi.play()
        self.tamagochi.update()

    def get_status(self) -> dict[str, Any]:
        """
        Получение статуса тамагочи

        :return: словарь со всеми характеристиками тамагочи
        """
        status = dict(self.tamagochi.status)
        status["coins"] = self._coins
        return status

    def spend(self, amount: int) -> None:
        """
        Списать монеты за покупку

        :param amount: сумма списания
        :raises NotEnoughMoney: если не хватает монет
        """
        if self._coins < amount:
            raise NotEnoughMoney("Недостаточно монет для покупки")
        self._coins -= amount
        # синхронизируем внутренние монеты кликера, если они есть
        if hasattr(self.clicker, "spend"):
            try:
                self.clicker.spend(amount)
            except NotEnoughMoney:
                pass

    @property
    def coins(self) -> int:
        """Текущее количество монет"""
        return self._coins

    @property
    def food(self) -> list[Food]:
        """
        Сумка с едой

        :return: список с имеющимися (купленными) объектами еды
        """
        return self._food

    @property
    def medicine(self) -> list[Medicine]:
        """
        Сумка с лекарствами

        :return: список с имеющимися (купленными) объектами лекарств
        """
        return self._medicine

    # ---- вспомогательные методы ----

    @staticmethod
    def _print_choices(items: list, kind: str) -> None:
        """Выводит нумерованный список предметов"""
        print(f"Доступные варианты {kind}: ")
        for i, item in enumerate(items):
            print(f"  {i + 1}. {item}")

    @staticmethod
    def _ask_index(count: int) -> int:
        """
        Запрашивает у пользователя номер (с 1) и валидирует его

        :param count: количество доступных вариантов
        :return: корректный индекс (с 0)
        """
        while True:
            try:
                value = int(input("Введите номер: "))
                if 1 <= value <= count:
                    return value - 1
                print("Неверный номер, попробуйте снова.")
            except ValueError:
                print("Введите число.")
