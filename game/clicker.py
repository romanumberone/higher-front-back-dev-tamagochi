"""Модуль с интерфейсом и реализацией кликера."""

from abc import ABC, abstractmethod


class AbstractClicker(ABC):
    """Интерфейс для кликера."""

    @abstractmethod
    def __init__(self) -> None:
        """Инициализирует кликер."""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Совершает клик, накапливая доход."""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Возвращает количество монет за один клик."""
        raise NotImplementedError


class Clicker(AbstractClicker):
    """Реализация кликера с накоплением монет."""

    def __init__(
        self,
        income_per_click: int = 1,
    ) -> None:
        """
        Инициализация кликера.

        :param income_per_click: количество монет за один клик
        """
        self._income_per_click = income_per_click

    def click(self) -> None:
        """Клик для накапливания монет."""

    @property
    def income_per_click(self) -> int:
        """Возвращает количество монет за клик."""
        return self._income_per_click
