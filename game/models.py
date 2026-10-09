"""Модуль с моделями."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Food:
    """Модель объекта еды."""

    name: str
    satiety: int
    price: int

    def __repr__(self) -> str:
        """Возвращает читаемое представление объекта еды."""
        return (
            f"{self.name} стоимость: {self.price}, "
            f"утоляет голод на {self.satiety} единиц"
        )


@dataclass
class Medicine:
    """Модель объекта лекарства."""

    name: str
    price: int
    heal_hp: int
    number_of_uses: int
    uses: int = 0

    def is_empty(self) -> bool:
        """Проверяет, закончилось ли лекарство."""
        return self.uses >= self.number_of_uses

    def __repr__(self) -> str:
        """Возвращает читаемое представление объекта лекарства."""
        return (
            f'{self.name} стоимость: {self.price}, '
            f'лечит на {self.heal_hp} HP, использований: '
            f'{self.number_of_uses - self.uses}/{self.number_of_uses}'
        )
