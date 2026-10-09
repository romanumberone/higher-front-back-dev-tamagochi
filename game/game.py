"""Модуль с интерфейсом и реализацией класса игры."""

import copy
from abc import ABC, abstractmethod
from typing import Any

from .tamagochi import AbstractTamagochi
from .clicker import AbstractClicker
from .models import Food, Medicine
from .exceptions import (
    NotEnoughMoney,
    ShopIsEmpty,
    InventoryIsEmpty,
)


class AbstractGame(ABC):
    """Интерфейс для логики игры."""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ) -> None:
        """
        Инициализирует класс игры.

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды
        :param all_medicine: все доступные варианты лекарств
        """
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """
        Выполняет действие - Работа

        :return: количество заработанных монет
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Покупает еду."""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Покупает лекарство."""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Кормит тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Лечит тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self):
        """Даёт тамагочи отдохнуть."""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self):
        """Играет с тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """
        Возвращает статус тамагочи.

        :return: словарь со всеми характеристиками тамагочи
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """
        Возвращает сумку с едой.

        :return: список имеющейся еды
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """
        Возвращает сумку с лекарствами.

        :return: список имеющихся лекарств
        """
        raise NotImplementedError


class Game(AbstractGame):
    """Реализация логики игры."""

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ):
        """
        Инициализация класса игры.

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды
        :param all_medicine: все доступные варианты лекарств
        """
        self._tamagochi = tamagochi
        self._clicker = clicker
        self._all_food = list(all_food)
        self._all_medicine = list(all_medicine)
        self._coins = 0
        self._food: list[Food] = []
        self._medicine: list[Medicine] = []

    @property
    def tamagochi(self) -> AbstractTamagochi:
        """Возвращает тамагочи."""
        return self._tamagochi

    def work(self) -> int:
        """
        Выполняет действие - Работа.

        Начисляет доход за клик и обновляет состояние питомца.

        :return: количество заработанных монет
        """
        income = self._clicker.income_per_click
        self._clicker.click()
        self._coins += income
        self._tick()
        return income

    def buy_food(self) -> None:
        """
        Покупает еду.

        :raises ShopIsEmpty: если в магазине нет еды
        """
        if not self._all_food:
            raise ShopIsEmpty("Нет доступной еды для покупки")

        self._print_choices(self._all_food, "еды")
        index = self._ask_index(len(self._all_food))
        food = self._all_food[index]

        self._spend(food.price)
        self._food.append(food)
        self._tick()

    def buy_medicine(self) -> None:
        """
        Покупает лекарства.

        :raises ShopIsEmpty: если в магазине нет лекарств
        """
        if not self._all_medicine:
            raise ShopIsEmpty("Нет доступных лекарств для покупки")

        self._print_choices(self._all_medicine, "лекарств")
        index = self._ask_index(len(self._all_medicine))
        medicine = copy.copy(self._all_medicine[index])

        self._spend(medicine.price)
        self._medicine.append(medicine)
        self._tick()

    def feed_tamagochi(self) -> None:
        """
        Кормление тамагочи.

        :raises InventoryIsEmpty: если в сумке нет еды
        """
        if not self._food:
            raise InventoryIsEmpty("В сумке нет еды")

        self._print_choices(self._food, "еды")
        index = self._ask_index(len(self._food))
        food = self._food.pop(index)

        self._tamagochi.feed(food)
        self._tick()

    def heal_tamagochi(self) -> None:
        """
        Лечение тамагочи.

        :raises InventoryIsEmpty: если в сумке нет лекарств
        """
        if not self._medicine:
            raise InventoryIsEmpty("В сумке нет лекарств")

        self._print_choices(self._medicine, "лекарств")
        index = self._ask_index(len(self._medicine))
        medicine = self._medicine[index]

        self._tamagochi.heal(medicine)

        if medicine.is_empty():
            self._medicine.pop(index)

        self._tick()

    def rest_tamagochi(self):
        """Отдых тамагочи."""
        self._tamagochi.rest()
        self._tick()

    def play_with_tamagochi(self):
        """Игра с тамагочи."""
        self._tamagochi.play()
        self._tick()

    def get_status(self) -> dict[str, Any]:
        """
        Возвращает статус тамагочи.

        :return: словарь со всеми характеристиками тамагочи
        """
        status = dict(self._tamagochi.status)
        status["coins"] = self._coins
        return status

    def _tick(self) -> None:
        """Обновляет состояние тамагочи за один игровой тик."""
        self._tamagochi.update()

    def _spend(self, amount: int) -> None:
        """
        Списать монеты за покупку.

        :param amount: сумма списания
        :raises NotEnoughMoney: если не хватает монет
        """
        if self._coins < amount:
            raise NotEnoughMoney("Недостаточно монет для покупки")
        self._coins -= amount

    @property
    def coins(self) -> int:
        """Возвращает текущее количество монет."""
        return self._coins

    @property
    def food(self) -> list[Food]:
        """
        Сумка с едой.

        :return: список имеющейся еды
        """
        return list(self._food)

    @property
    def medicine(self) -> list[Medicine]:
        """
        Сумка с лекарствами.

        :return: список с имеющимися (купленными) объектами лекарств
        """
        return list(self._medicine)

    @staticmethod
    def _print_choices(items: list, kind: str) -> None:
        """Выводит нумерованный список предметов."""
        lines = [f"Доступные варианты {kind}:"]
        lines.extend(
            f"  {i}. {item}" for i, item in enumerate(items, start=1)
        )
        print("\n".join(lines))

    @staticmethod
    def _ask_index(count: int) -> int:
        """
        Запрашивает у пользователя номер и валидирует его.

        :param count: количество доступных вариантов
        :return: корректный индекс (с нуля)
        """
        while True:
            try:
                value = int(input("Введите номер: "))
                if 1 <= value <= count:
                    return value - 1
                print("Неверный номер, попробуйте снова.")
            except ValueError:
                print("Введите число.")
