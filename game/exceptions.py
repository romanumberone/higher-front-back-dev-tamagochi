"""Модуль с исключениями."""


class GameError(Exception):
    """Базовое исключение игры."""


class TamagochiIsGone(GameError):
    """Ошибка при смерти тамагочи."""


class NotEnoughMoney(GameError):
    """Ошибка когда не хватает монет для покупки."""


class MedicineIsEmpty(GameError):
    """Ошибка, когда лекарство закончилось."""


class ShopIsEmpty(GameError):
    """Ошибка, когда в магазине нет подходящих товаров."""


class InventoryIsEmpty(GameError):
    """Ошибка, когда в сумке нет нужных предметов."""
