"""Модуль с интерфейсом и реализациями класса тамагочи."""

from abc import ABC, abstractmethod

from game.models import Food, Medicine


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи."""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """Абстрактный метод для кормления тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Абстрактный метод для игры с тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Абстрактный метод для отдыха тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """Абстрактный метод для лечения тамагочи."""
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """Абстрактное свойство для доступа ко всем состояниям тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """Абстрактный метод для проверки жив ли тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """Абстрактный метод для проверки, не заболел ли тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """Абстрактный метод для обновления состояний тамагочи."""
        raise NotImplementedError


class Tamagochi(AbstractTamagochi):
    """Реализация логики питомца Тамагочи с классическими шкалами."""

    def __init__(self) -> None:
        """Инициализирует начальные показатели тамагочи."""
        self._hp = 100
        self._energy = 100
        self._hunger = 0
        self._fatigue = 0
        self._is_sick = False

    @property
    def status(self) -> dict[str, int]:
        """Возвращает словарь со всеми показателями питомца."""
        return {
            "hp": self._hp,
            "energy": self._energy,
            "hunger": self._hunger,
            "fatigue": self._fatigue,
        }

    def is_alive(self) -> bool:
        """Проверяет, жив ли питомец."""
        return self._hp > 0

    def is_sick(self) -> bool:
        """Проверяет, болен ли питомец."""
        return self._is_sick

    def _change_hp(self, value: int) -> None:
        """Внутренний метод изменения здоровья."""
        self._hp = min(100, max(0, self._hp + value))

    def _change_hunger(self, value: int) -> None:
        """Внутренний метод изменения голода."""
        self._hunger = min(100, max(0, self._hunger + value))

    def _change_energy(self, value: int) -> None:
        """Внутренний метод изменения энергии."""
        self._energy = min(100, max(0, self._energy + value))

    def _change_fatigue(self, value: int) -> None:
        """Внутренний метод изменения усталости."""
        self._fatigue = min(100, max(0, self._fatigue + value))

    def feed(self, food: Food) -> None:
        """Накормить питомца. Уменьшает голод."""
        self._change_hunger(-food.satiety)
        self._change_energy(-5)
        self.update()

    def play(self) -> None:
        """Поиграть с питомцем. Увеличивает усталость и голод."""
        self._change_fatigue(15)
        self._change_energy(-15)
        self._change_hunger(10)
        self.update()

    def rest(self) -> None:
        """Отправить питомца отдыхать. Снижает усталость."""
        coef = 0.5 if self._is_sick else 1.0
        self._change_energy(int(40 * coef))
        self._change_fatigue(-int(40 * coef))
        self._change_hunger(10)
        self.update()

    def heal(self, medicine: Medicine) -> None:
        """Вылечить питомца с помощью лекарства."""
        if not medicine.is_empty():
            self._change_hp(medicine.heal_hp)
            medicine.uses += 1
            if self._hp > 50 and self._hunger < 50 and self._fatigue < 50:
                self._is_sick = False

    def update(self) -> None:
        """Обновление состояния питомца на каждом ходу."""
        self._change_hunger(5)
        self._change_fatigue(5)

        if self._hunger >= 80 or self._fatigue >= 80:
            self._is_sick = True

        if self._is_sick:
            self._change_hp(-10)
