"""Модуль с интерфейсом и реализацией класса игры."""

from abc import ABC, abstractmethod
from typing import Any
from copy import copy

from game.tamagochi import AbstractTamagochi
from game.clicker import AbstractClicker
from game.models import Food, Medicine
from game.exceptions import TamagochiIsGone, NotEnoughMoney


class AbstractGame(ABC):
    """Интерфейс для логики игры."""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ):
        """Абстрактный метод инициализации."""
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """Абстрактный метод для работы."""
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Абстрактный метод для покупки еды."""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Абстрактный метод для покупки лекарства."""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Абстрактный метод для кормления."""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Абстрактный метод для лечения."""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self):
        """Абстрактный метод для отдыха."""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self):
        """Абстрактный метод для игры."""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """Абстрактный метод для получения статуса."""
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """Абстрактное свойство для рюкзака с едой."""
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """Абстрактное свойство для рюкзака с лекарствами."""
        raise NotImplementedError


class Game(AbstractGame):
    """Реализация логики и игрового цикла Тамагочи."""

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ):
        """Инициализирует состояние игры."""
        self._tamagochi = tamagochi
        self._clicker = clicker
        self._all_food = all_food
        self._all_medicine = all_medicine
        self._bag_food: list[Food] = []
        self._bag_medicine: list[Medicine] = []
        self._coins = 0

    @property
    def food(self) -> list[Food]:
        """Возвращает список купленной еды в сумке."""
        return self._bag_food

    @property
    def medicine(self) -> list[Medicine]:
        """Возвращает список купленных лекарств в сумке."""
        return self._bag_medicine

    @property
    def tamagochi(self) -> AbstractTamagochi:
        """Предоставляет доступ к объекту тамагочи."""
        return self._tamagochi

    def _check_alive(self) -> None:
        """Проверяет состояние здоровья питомца."""
        if not self._tamagochi.is_alive():
            raise TamagochiIsGone("К сожалению, ваш питомец погиб.")

    def work(self) -> int:
        """Совершает клик и начисляет заработанные монеты."""
        self._check_alive()
        self._clicker.click()
        earnings = self._clicker.income_per_click
        self._coins += earnings
        return earnings

    def buy_food(self, index: int = 0) -> None:
        """Покупает еду из ассортимента по индексу."""
        self._check_alive()
        selected_food = self._all_food[index]

        if self._coins < selected_food.price:
            raise NotEnoughMoney("Недостаточно монет для покупки еды.")

        self._coins -= selected_food.price
        self._bag_food.append(selected_food)

    def buy_medicine(self, index: int = 0) -> None:
        """Покупает лекарство из ассортимента по индексу."""
        self._check_alive()
        selected_med = self._all_medicine[index]

        if self._coins < selected_med.price:
            raise NotEnoughMoney("Недостаточно монет для покупки лекарства.")

        self._coins -= selected_med.price
        self._bag_medicine.append(copy(selected_med))

    def feed_tamagochi(self, index: int = 0) -> None:
        """Кормит питомца едой из рюкзака по указанному индексу."""
        self._check_alive()
        if not self._bag_food:
            return

        selected_food = self._bag_food.pop(index)
        self._tamagochi.feed(selected_food)

    def heal_tamagochi(self, index: int = 0) -> None:
        """Лечит питомца лекарством из рюкзака по указанному индексу."""
        self._check_alive()
        if not self._bag_medicine:
            return

        selected_med = self._bag_medicine[index]
        self._tamagochi.heal(selected_med)

        if selected_med.is_empty():
            self._bag_medicine.pop(index)

    def rest_tamagochi(self) -> None:
        """Отправляет тамагочи отдыхать."""
        self._check_alive()
        self._tamagochi.rest()

    def play_with_tamagochi(self) -> None:
        """Запускает игру с тамагочи."""
        self._check_alive()
        self._tamagochi.play()

    def get_status(self) -> dict[str, Any]:
        """Собирает полный статус игры для тестов и вывода."""
        status_data: dict[str, Any] = dict(self._tamagochi.status)
        status_data.update({
            "coins": self._coins
        })
        return status_data
