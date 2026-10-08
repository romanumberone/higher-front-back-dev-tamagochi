"""Модуль с интерфейсом и реализациями класса тамагочи"""

from abc import ABC, abstractmethod

from .models import Food, Medicine
from .exceptions import TamagochiIsGone


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи"""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """
        Абстрактный метод для кормления тамагочи

        :param food: объект еды для кормления
        """
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """
        Абстрактный метод для лечения тамагочи

        :param medicine: лекарство для лечения
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """
        Абстрактное свойство для доступа ко всем состояниям тамагочи

        :return: словарь со всеми состояниями тамагочи
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Абстрактный метод для проверки жив ли тамагочи

        :return: True если жив, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """
        Абстрактный метод для проверки, не заболел ли тамагочи

        :return: True если тамагочи болеет, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """
        Абстрактный метод для обновления состояний тамагочи.
        Должен использоваться после каждого взаимодействия с тамагочи
        """
        raise NotImplementedError


class BasicTamagochi(AbstractTamagochi):
    """Базовая реализация тамагочи с основными параметрами"""

    def __init__(
        self,
        name: str = "Тамагочи",
        max_hunger: int = 100,
        max_hp: int = 100,
        max_mood: int = 100,
        max_energy: int = 100,
    ) -> None:
        """
        Инициализация тамагочи

        :param name: имя тамагочи
        :param max_hunger: максимальный уровень ГОЛОДА
        (0 — сыт, 100 — очень голоден)
        :param max_hp: максимальный уровень здоровья
        :param max_mood: максимальный уровень настроения
        :param max_energy: максимальный уровень энергии
        """
        self.name = name
        self._max_hunger = max_hunger
        self._max_hp = max_hp
        self._max_mood = max_mood
        self._max_energy = max_energy

        # текущие значения
        self._hunger = 0            # 0 = сыт, 100 = очень голоден
        self._hp = max_hp           # 0 = мёртв
        self._mood = max_mood       # 100 = счастлив, 0 = грустный
        self._energy = max_energy   # 100 = полон сил, 0 = выдохся
        self._sick = False          # болеет ли тамагочи

    def feed(self, food: Food) -> None:
        """
        Метод для кормления тамагочи — снижает голод

        :param food: объект еды для кормления
        """
        if not self.is_alive():
            raise TamagochiIsGone("Тамагочи умер, кормить нельзя")
        # еда насыщает — голод уменьшается
        self._hunger = max(0, self._hunger - food.satiety)

    def play(self) -> None:
        """
        Метод для игры с тамагочи.
        Игра повышает настроение, но увеличивает голод и тратит энергию.
        """
        if not self.is_alive():
            raise TamagochiIsGone("Тамагочи умер, играть нельзя")
        self._mood = min(self._max_mood, self._mood + 15)
        self._hunger = min(self._max_hunger, self._hunger + 10)
        self._energy = max(0, self._energy - 10)

    def rest(self) -> None:
        """
        Метод для отдыха тамагочи.
        Отдых восстанавливает энергию и здоровье, немного повышает настроение.
        """
        if not self.is_alive():
            raise TamagochiIsGone("Тамагочи умер, отдыхать нельзя")
        if self._sick:
            # во время болезни отдых не лечит,
            # но восстанавливает энергию и настроение
            self._mood = min(self._max_mood, self._mood + 5)
            self._energy = min(self._max_energy, self._energy + 20)
        else:
            self._hp = min(self._max_hp, self._hp + 10)
            self._mood = min(self._max_mood, self._mood + 5)
            self._energy = min(self._max_energy, self._energy + 20)

    def heal(self, medicine: Medicine) -> None:
        """
        Метод для лечения тамагочи

        :param medicine: лекарство для лечения
        """
        if not self.is_alive():
            raise TamagochiIsGone("Тамагочи умер, лечить нельзя")
        if medicine.is_empty():
            return
        self._hp = min(self._max_hp, self._hp + medicine.heal_hp)
        medicine.uses += 1
        # если здоровье восстановлено — питомец больше не болеет
        self._sick = False

    @property
    def status(self) -> dict[str, int]:
        """
        Свойство для доступа ко всем состояниям тамагочи

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
        Проверка жив ли тамагочи

        :return: True если жив, иначе False
        """
        return self._hp > 0

    def is_sick(self) -> bool:
        """
        Проверка, не заболел ли тамагочи

        :return: True если тамагочи болеет, иначе False
        """
        return self._sick

    def update(self) -> None:
        """
        Обновление состояний тамагочи.
        Используется после каждого взаимодействия с тамагочи.
        """
        if not self.is_alive():
            return

        # голод постепенно растёт
        self._hunger = min(self._max_hunger, self._hunger + 5)

        # энергия постепенно восстанавливается в покое
        self._energy = min(self._max_energy, self._energy + 5)

        # настроение постепенно падает
        self._mood = max(0, self._mood - 5)

        # если тамагочи сильно голоден или
        # в плохом настроении — теряет здоровье
        if self._hunger >= self._max_hunger or self._mood == 0:
            self._hp = max(0, self._hp - 5)
        else:
            self._hp = min(self._max_hp, self._hp + 2)

        # заболевает при низком здоровье или настроении
        if self._hp < 30 or self._mood < 20:
            self._sick = True
