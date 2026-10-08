"""Модуль с интерфейсом и реализацией кликера"""

from abc import ABC, abstractmethod

from .exceptions import NotEnoughMoney


class AbstractClicker(ABC):
    """Интерфейс для кликера"""

    @abstractmethod
    def __init__(self) -> None:
        """Абстрактный метод инициализации"""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Абстрактный метод клика для накапливания монет"""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Абстрактное свойство для доступа к количеству монет за клик"""
        raise NotImplementedError


class Clicker(AbstractClicker):
    """Реализация кликера с накоплением монет"""

    def __init__(
        self, income_per_click: int = 1, initial_coins: int = 0
    ) -> None:
        """
        Инициализация кликера

        :param income_per_click: количество монет за один клик
        :param initial_coins: начальное количество монет
        """
        self._income_per_click = income_per_click
        self._coins = initial_coins

    def click(self) -> None:
        """Клик для накапливания монет"""
        self._coins += self._income_per_click

    @property
    def income_per_click(self) -> int:
        """Количество монет за клик"""
        return self._income_per_click

    @property
    def coins(self) -> int:
        """Текущее количество монет"""
        return self._coins

    def spend(self, amount: int) -> None:
        """
        Потратить монеты

        :param amount: сумма для списания
        :raises NotEnoughMoney: если не хватает монет
        """
        if self._coins < amount:
            raise NotEnoughMoney("Недостаточно монет для покупки")
        self._coins -= amount
