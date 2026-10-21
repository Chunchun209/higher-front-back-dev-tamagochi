"""Модуль с интерфейсом и реализацией кликера."""

from abc import ABC, abstractmethod


class AbstractClicker(ABC):
    """Интерфейс для кликера."""

    @abstractmethod
    def __init__(self) -> None:
        """Абстрактный метод инициализации."""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Абстрактный метод клика для накапливания монет."""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Абстрактное свойство для доступа к количеству монет за клик."""
        raise NotImplementedError


class Clicker(AbstractClicker):
    """Реализация кликера для заработка монет."""

    def __init__(self, income_per_click: int = 1, *args, **kwargs) -> None:
        self._income_per_click = income_per_click

    @property
    def income_per_click(self) -> int:
        """Возвращает количество монет за один клик."""
        return self._income_per_click

    def click(self) -> None:
        """Логика совершения клика."""
        print(f"Клик. Заработано {self.income_per_click} монет")
