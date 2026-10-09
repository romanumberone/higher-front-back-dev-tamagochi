"""Модуль с интерфейсом и реализациями класса тамагочи."""

from abc import ABC, abstractmethod

from .models import Food, Medicine
from .exceptions import TamagochiIsGone


DEFAULT_MAX_HUNGER = 100
DEFAULT_MAX_HP = 100
DEFAULT_MAX_MOOD = 100
DEFAULT_MAX_ENERGY = 100


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи."""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """
        Кормит тамагочи.

        :param food: объект еды для кормления
        """
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Играет с тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Даёт тамагочи отдохнуть."""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """
        Лечит тамагочи.

        :param medicine: лекарство для лечения
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """
        Возвращает все состояния тамагочи.

        :return: словарь со всеми состояниями тамагочи
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Проверяет, жив ли тамагочи.

        :return: True если жив, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """
        Проверяет, болеет ли тамагочи.

        :return: True если тамагочи болеет, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """
        Обновляет состояния тамагочи.

        Должен использоваться после каждого взаимодействия
        с тамагочи.
        """
        raise NotImplementedError


class BasicTamagochi(AbstractTamagochi):
    """Базовая реализация тамагочи с основными параметрами."""

    def __init__(
        self,
        name: str = "Тамагочи",
        max_hunger: int = DEFAULT_MAX_HUNGER,
        max_hp: int = DEFAULT_MAX_HP,
        max_mood: int = DEFAULT_MAX_MOOD,
        max_energy: int = DEFAULT_MAX_ENERGY,
    ) -> None:
        """
        Инициализация тамагочи.

        :param name: имя тамагочи
        :param max_hunger: максимальный уровень ГОЛОДА
        :param max_hp: максимальный уровень здоровья
        :param max_mood: максимальный уровень настроения
        :param max_energy: максимальный уровень энергии
        """
        self._name = name
        self._max_hunger = max_hunger
        self._max_hp = max_hp
        self._max_mood = max_mood
        self._max_energy = max_energy

        self._hunger = 0
        self._hp = max_hp
        self._mood = max_mood
        self._energy = max_energy
        self._sick = False

    @property
    def name(self) -> str:
        """Возвращает имя тамагочи."""
        return self._name

    def _ensure_alive(self, action: str) -> None:
        """
        Проверяет, что тамагочи жив.

        :param action: название действия для сообщения об ошибке
        :raises TamagochiIsGone: если тамагочи мёртв
        """
        if not self.is_alive():
            raise TamagochiIsGone(f"Тамагочи умер, {action} нельзя")

    def feed(self, food: Food) -> None:
        """
        Кормит тамагочи и снижает уровень голода.

        :param food: объект еды для кормления
        """
        self._ensure_alive("кормить")
        self._hunger = max(0, self._hunger - food.satiety)

    def play(self) -> None:
        """
        Играет с тамагочи.

        Игра повышает настроение, но увеличивает голод
        и тратит энергию.
        """
        self._ensure_alive("играть")
        self._mood = min(self._max_mood, self._mood + 15)
        self._hunger = min(self._max_hunger, self._hunger + 10)
        self._energy = max(0, self._energy - 10)

    def rest(self) -> None:
        """
        Даёт тамагочи отдохнуть.

        Отдых восстанавливает энергию и здоровье,
        немного повышает настроение.
        """
        self._ensure_alive("отдыхать")
        if self._sick:
            self._mood = min(self._max_mood, self._mood + 5)
            self._energy = min(self._max_energy, self._energy + 20)
        else:
            self._hp = min(self._max_hp, self._hp + 10)
            self._mood = min(self._max_mood, self._mood + 5)
            self._energy = min(self._max_energy, self._energy + 20)

    def heal(self, medicine: Medicine) -> None:
        """
        Лечит тамагочи.

        :param medicine: лекарство для лечения
        """
        self._ensure_alive("лечить")
        if medicine.is_empty():
            return
        self._hp = min(self._max_hp, self._hp + medicine.heal_hp)
        medicine.uses += 1
        # если здоровье восстановлено — питомец больше не болеет
        self._sick = False

    @property
    def status(self) -> dict[str, int]:
        """
        Возвращает все состояния тамагочи.

        :return: словарь со всеми состояниями тамагочи
        """
        return {
            "hunger": self._hunger,
            "hp": self._hp,
            "mood": self._mood,
            "energy": self._energy,
        }

    def is_alive(self) -> bool:
        """
        Проверка жив ли тамагочи.

        :return: True если жив, иначе False
        """
        return self._hp > 0

    def is_sick(self) -> bool:
        """
        Проверка, не заболел ли тамагочи.

        :return: True если тамагочи болеет, иначе False
        """
        return self._sick

    def update(self) -> None:
        """
        Обновление состояний тамагочи.

        Используется после каждого взаимодействия с тамагочи.
        Голод и настроение меняются со временем, здоровье
        зависит от них, а при плохих показателях питомец
        может заболеть.
        """
        if not self.is_alive():
            return

        self._hunger = min(self._max_hunger, self._hunger + 5)
        self._energy = min(self._max_energy, self._energy + 5)
        self._mood = max(0, self._mood - 5)

        if self._hunger >= self._max_hunger or self._mood == 0:
            self._hp = max(0, self._hp - 5)
        else:
            self._hp = min(self._max_hp, self._hp + 2)

        if self._hp < 30 or self._mood < 20:
            self._sick = True
