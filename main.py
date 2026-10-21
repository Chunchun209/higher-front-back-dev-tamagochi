"""Главный модуль для запуска игры 'Тамагочи с кликером'."""

import os

from game.models import Food, Medicine
from game.tamagochi import Tamagochi
from game.clicker import Clicker
from game.game import Game
from game.exceptions import TamagochiIsGone, NotEnoughMoney


def main() -> None:
    """Точка входа в игра. Инициализирует сущности и запускает игровой цикл."""
    all_food = [
        Food(name='Бургер', satiety=20, price=40),
        Food(name='Салат', satiety=10, price=20),
        Food(name='Яблоко', satiety=10, price=15)
    ]

    all_medicine = [
        Medicine(name='Ибупрофен', price=30, heal_hp=20, number_of_uses=2)
    ]

    tamagochi = Tamagochi()
    clicker = Clicker(10, 20)
    game = Game(
        tamagochi,
        clicker,
        all_food=all_food,
        all_medicine=all_medicine
    )

    output = 'Добро пожаловать в Тамагочи-кликер!'

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(output)
        output = ''

        print(f"Сумка с едой: {game.food}")
        print(f"Сумка с лекарствами: {game.medicine}")

        status = game.get_status()
        print(
            f"\nСтатус: голод {status['hunger']}/100, "
            f"здоровье {status['hp']}/100, энергия {status['energy']}/100, "
            f"усталость {status['fatigue']}/100, монет {status['coins']}\n"
        )

        if game.tamagochi.is_sick():
            print("=======Тамагочи болеет======")
            print("=======Отдых действует менее эффективно=======")

        print("1. Пойти на работу")
        print("2. Купить еду")
        print("3. Купить лекарство")
        print("4. Покормить")
        print("5. Вылечить")
        print("6. Играть")
        print("7. Отдых")
        print("0. Выход")

        user_input = input("Выберите действие: ")

        try:
            match user_input:
                case "1":
                    income = game.work()
                    output = f'Вы заработали {income} монет'
                    game.tamagochi.update()
                case "2":
                    print(f"Ваш баланс: {status['coins']} монет. Меню:")
                    for i, food_item in enumerate(all_food):
                        print(f"[{i}] {food_item}")
                    food_idx = int(input("Выберите номер еды: "))
                    game.buy_food(food_idx)
                    output = 'Вы успешно купили еду'
                case "3":
                    print(f"Ваш баланс: {status['coins']} монет. Аптека:")
                    for i, med_item in enumerate(all_medicine):
                        print(f"[{i}] {med_item}")
                    med_idx = int(input("Выберите номер лекарства: "))
                    game.buy_medicine(med_idx)
                    output = 'Вы успешно купили лекарство'
                case "4":
                    if not game.food:
                        output = "Сумка с едой пуста!"
                        continue
                    for i, food_item in enumerate(game.food):
                        print(f"[{i}] {food_item.name}")
                    bag_food_idx = int(input("Выберите номер еды из сумки: "))
                    game.feed_tamagochi(bag_food_idx)
                    output = 'Вы покормили питомца'
                case "5":
                    if not game.medicine:
                        output = "Сумка с лекарствами пуста!"
                        continue
                    for i, med_item in enumerate(game.medicine):
                        print(f"[{i}] {med_item.name}")
                    bag_med_idx = int(input("Выберите номер лекарства: "))
                    game.heal_tamagochi(bag_med_idx)
                    output = 'Вы полечили питомца'

                case "6":
                    game.play_with_tamagochi()
                    output = 'Вы поиграли с питомцем'
                case "7":
                    game.rest_tamagochi()
                    output = 'Питомец отдохнул'
                case "0":
                    break
                case _:
                    output = "Неверная команда"

        except (ValueError, IndexError):
            output = "Ошибка ввода: Некорректный выбор предмета."
        except NotEnoughMoney as error:
            output = f"Ошибка экономики: {error}"
        except TamagochiIsGone as error:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n==========================================")
            print(f"ИГРА ОКОНЧЕНА: {error}")
            print("==========================================\n")
            break


if __name__ == "__main__":
    main()
