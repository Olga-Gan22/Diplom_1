import pytest
from unittest.mock import Mock

from praktikum.burger import Burger
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING


class TestBurger:

    def test_init_bun_is_none(self):
        # Проверка, что при создании объекта Burger поле bun по умолчанию равно None
        burger = Burger()
        assert burger.bun is None

    def test_init_ingredients_empty(self):
        # Проверка, что при создании объекта Burger список ингредиентов изначально пуст
        burger = Burger()
        assert burger.ingredients == []

    def test_set_buns_sets_bun(self):
        # Проверяет корректность установки булки через метод set_buns: объект булки сохраняется в поле bun
        burger = Burger()
        mock_bun = Mock()
        burger.set_buns(mock_bun)
        assert burger.bun is mock_bun

    def test_add_ingredient_appends_to_list(self):
        # Проверка, что добавление ингредиента через add_ingredient помещает его в конец списка ingredients
        burger = Burger()
        mock_ingredient = Mock()
        burger.add_ingredient(mock_ingredient)
        assert mock_ingredient in burger.ingredients
        assert len(burger.ingredients) == 1

    def test_add_ingredient_multiple(self):
        # Проверяет добавление нескольких ингредиентов подряд: порядок и количество сохраняются
        burger = Burger()
        m1 = Mock()
        m2 = Mock()
        burger.add_ingredient(m1)
        burger.add_ingredient(m2)
        assert len(burger.ingredients) == 2
        assert burger.ingredients[0] is m1
        assert burger.ingredients[1] is m2

    @pytest.mark.parametrize("initial_count,remove_index,expected_count", [
        (1, 0, 0),
        (3, 0, 2),
        (3, 2, 2),
        (3, 1, 2),
    ])
    def test_remove_ingredient(self, initial_count, remove_index, expected_count):
        # Параметризованный тест: проверяет удаление ингредиента по индексу и корректное уменьшение длины списка
        burger = Burger()
        for i in range(initial_count):
            m = Mock()
            m.get_name.return_value = f"ingredient_{i}"
            burger.add_ingredient(m)
        burger.remove_ingredient(remove_index)
        assert len(burger.ingredients) == expected_count

    def test_remove_ingredient_removes_correct_item(self):
        # Проверяет, что удаляется именно ингредиент по указанному индексу, а не другой элемент списка
        burger = Burger()
        i1 = Mock()
        i2 = Mock()
        i3 = Mock()
        burger.add_ingredient(i1)
        burger.add_ingredient(i2)
        burger.add_ingredient(i3)
        burger.remove_ingredient(1)
        assert burger.ingredients[0] is i1
        assert burger.ingredients[1] is i3
        assert i2 not in burger.ingredients

    @pytest.mark.parametrize("index,new_index,expected_order", [
        (0, 2, [1, 2, 0]),
        (2, 0, [2, 0, 1]),
        (0, 1, [1, 0, 2]),
        (1, 0, [1, 0, 2]),
    ])
    def test_move_ingredient(self, index, new_index, expected_order):
        # Параметризованный тест: проверяет перемещение ингредиента с одного индекса на другой и корректный порядок элементов
        burger = Burger()
        ingredients = []
        for i in range(3):
            m = Mock()
            m.get_name.return_value = f"ingredient_{i}"
            ingredients.append(m)
            burger.add_ingredient(m)
        burger.move_ingredient(index, new_index)
        for pos, original_idx in enumerate(expected_order):
            assert burger.ingredients[pos].get_name() == f"ingredient_{original_idx}"

    def test_move_ingredient_same_index(self):
        # Проверяет поведение при попытке переместить ингредиент на тот же самый индекс: список не должен измениться
        burger = Burger()
        i1, i2, i3 = Mock(), Mock(), Mock()
        burger.add_ingredient(i1)
        burger.add_ingredient(i2)
        burger.add_ingredient(i3)
        burger.move_ingredient(1, 1)
        assert burger.ingredients[0] is i1
        assert burger.ingredients[1] is i2
        assert burger.ingredients[2] is i3

    def test_move_ingredient_to_end(self):
        # Проверяет перемещение первого ингредиента в конец списка: остальные элементы сдвигаются, порядок корректен
        burger = Burger()
        i1, i2, i3 = Mock(), Mock(), Mock()
        burger.add_ingredient(i1)
        burger.add_ingredient(i2)
        burger.add_ingredient(i3)
        burger.move_ingredient(0, 2)
        assert burger.ingredients[0] is i2
        assert burger.ingredients[1] is i3
        assert burger.ingredients[2] is i1

    @pytest.mark.parametrize("index", [0, 1, 2])
    def test_remove_ingredient_single_from_three(self, index):
        # Параметризованный тест: удаляет по одному ингредиенту из списка из трёх и проверяет, что остаётся ровно два
        burger = Burger()
        i1, i2, i3 = Mock(), Mock(), Mock()
        burger.add_ingredient(i1)
        burger.add_ingredient(i2)
        burger.add_ingredient(i3)
        burger.remove_ingredient(index)
        assert len(burger.ingredients) == 2

    def test_get_price_only_bun(self):
        # Проверяет расчёт цены бургера, состоящего только из булки: цена = 2 * цена булки
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_price.return_value = 100.0
        burger.set_buns(mock_bun)
        assert burger.get_price() == 200.0

    def test_get_price_bun_and_ingredients(self):
        # Проверяет расчёт полной цены бургера: сумма двух булок и всех ингредиентов
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_price.return_value = 100.0
        burger.set_buns(mock_bun)

        i1 = Mock()
        i1.get_price.return_value = 50.0
        i2 = Mock()
        i2.get_price.return_value = 75.0
        burger.add_ingredient(i1)
        burger.add_ingredient(i2)

        assert burger.get_price() == 325.0

    @pytest.mark.parametrize("bun_price,ingredient_prices,expected", [
        (100.0, [], 200.0),
        (50.0, [25.0], 125.0),
        (200.0, [100.0, 150.0, 50.0], 700.0),
        (0.0, [], 0.0),
        (100.0, [0.0, 0.0], 200.0),
    ])
    def test_get_price_parametrized(self, bun_price, ingredient_prices, expected):
        # Параметризованный тест расчёта цены: проверяет корректность суммы для разных комбинаций цен булки и ингредиентов
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_price.return_value = bun_price
        burger.set_buns(mock_bun)
        for price in ingredient_prices:
            m = Mock()
            m.get_price.return_value = price
            burger.add_ingredient(m)
        assert burger.get_price() == expected

    def test_get_price_no_ingredients_real_bun(self):
        # Проверяет расчёт цены с реальным объектом Bun (не моком): цена должна быть равна 2 * цене булки
        burger = Burger()
        burger.set_buns(Bun("white bun", 200))
        assert burger.get_price() == 400.0

    def test_get_receipt_format(self):
        # Проверяет формат чека: строки с булками, ингредиентами и итоговой ценой должны соответствовать ожидаемому шаблону
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_name.return_value = "white bun"
        mock_bun.get_price.return_value = 200.0
        burger.set_buns(mock_bun)

        sauce = Mock()
        sauce.get_type.return_value = INGREDIENT_TYPE_SAUCE
        sauce.get_name.return_value = "hot sauce"
        sauce.get_price.return_value = 100.0
        burger.add_ingredient(sauce)

        filling = Mock()
        filling.get_type.return_value = INGREDIENT_TYPE_FILLING
        filling.get_name.return_value = "cutlet"
        filling.get_price.return_value = 100.0
        burger.add_ingredient(filling)

        receipt = burger.get_receipt()

        expected_lines = [
            "(==== white bun ====)",
            "= sauce hot sauce =",
            "= filling cutlet =",
            "(==== white bun ====)\n",
            "Price: 600.0",
        ]
        expected_receipt = "\n".join(expected_lines)
        assert receipt == expected_receipt

    def test_get_receipt_only_bun(self):
        # Проверяет формат чека для бургера без ингредиентов: только две строки с булкой и итоговая цена
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_name.return_value = "black bun"
        mock_bun.get_price.return_value = 100.0
        burger.set_buns(mock_bun)

        receipt = burger.get_receipt()

        expected_lines = [
            "(==== black bun ====)",
            "(==== black bun ====)\n",
            "Price: 200.0",
        ]
        expected_receipt = "\n".join(expected_lines)
        assert receipt == expected_receipt

    @pytest.mark.parametrize("bun_name,ingredient_type,ingredient_name,bun_price,ingredient_price", [
        ("white bun", INGREDIENT_TYPE_SAUCE, "chili sauce", 50.0, 30.0),
        ("black bun", INGREDIENT_TYPE_FILLING, "beef", 100.0, 200.0),
    ])
    def test_get_receipt_parametrized(
        self,
        bun_name,
        ingredient_type,
        ingredient_name,
        bun_price,
        ingredient_price,
    ):
        # Параметризованный тест формата чека: проверяет корректные строки и цену для разных комбинаций булки и одного ингредиента
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_name.return_value = bun_name
        mock_bun.get_price.return_value = bun_price
        burger.set_buns(mock_bun)

        m = Mock()
        m.get_type.return_value = ingredient_type
        m.get_name.return_value = ingredient_name
        m.get_price.return_value = ingredient_price
        burger.add_ingredient(m)

        receipt = burger.get_receipt()
        expected_price = bun_price * 2 + ingredient_price

        expected_lines = [
            f"(==== {bun_name} ====)",
            f"= {ingredient_type.lower()} {ingredient_name} =",
            f"(==== {bun_name} ====)\n",
            f"Price: {expected_price}",
        ]
        expected_receipt = "\n".join(expected_lines)
        assert receipt == expected_receipt

    def test_get_receipt_with_real_ingredient(self):
        # Создаёт бургер с реальными объектами Bun и Ingredient (не моками),
        # формирует чек и проверяет корректность строк и итоговой цены.
        burger = Burger()
        burger.set_buns(Bun("black bun", 100))
        burger.add_ingredient(Ingredient(INGREDIENT_TYPE_SAUCE, "hot sauce", 100))
        burger.add_ingredient(Ingredient(INGREDIENT_TYPE_FILLING, "cutlet", 100))

        receipt = burger.get_receipt()
        lines = receipt.split('\n')
        
        assert lines[0] == "(==== black bun ====)", "Неверная верхняя булка"
        assert lines[1] == "= sauce hot sauce =", "Неверный соус"
        assert lines[2] == "= filling cutlet =", "Неверная начинка"
        assert lines[3] == "(==== black bun ====)", "Неверная нижняя булка"
        
        last_line = lines[-1]
        assert last_line.startswith("Price: ")
        price_value = float(last_line.replace("Price: ", ""))
        assert price_value == 400.0, f"Неверная сумма: {price_value}"

    def test_get_receipt_multiple_same_type(self):
        # Проверяет формирование чека при добавлении нескольких ингредиентов
        # одного типа: каждый выводится отдельной строкой, цена суммируется.
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_name.return_value = "red bun"
        mock_bun.get_price.return_value = 300.0
        burger.set_buns(mock_bun)

        s1 = Mock()
        s1.get_type.return_value = INGREDIENT_TYPE_SAUCE
        s1.get_name.return_value = "hot sauce"
        s1.get_price.return_value = 100.0

        s2 = Mock()
        s2.get_type.return_value = INGREDIENT_TYPE_SAUCE
        s2.get_name.return_value = "chili sauce"
        s2.get_price.return_value = 300.0

        burger.add_ingredient(s1)
        burger.add_ingredient(s2)

        receipt = burger.get_receipt()
        lines = receipt.split('\n')

        assert lines[0] == "(==== red bun ====)", "Неверная верхняя булка"
        assert lines[1] == "= sauce hot sauce =", "Неверный первый соус"
        assert lines[2] == "= sauce chili sauce =", "Неверный второй соус"
        assert lines[3] == "(==== red bun ====)", "Неверная нижняя булка"

        last_line = lines[-1]
        assert last_line.startswith("Price: ")
        price_value = float(last_line.replace("Price: ", ""))
        assert price_value == 1000.0, f"Неверная сумма: {price_value}"

    @pytest.mark.parametrize("bun_name,bun_price,ingredients,expected_price", [
        ("white bun", 100.0, [], 200.0),
        ("black bun", 50.0, [("sauce", "sour cream", 200.0)], 300.0),
        ("red bun", 300.0, [
            ("sauce", "hot sauce", 100.0),
            ("filling", "cutlet", 100.0),
            ("filling", "sausage", 300.0),
        ], 1100.0),
    ])
    def test_get_receipt_full_parametrized(self, bun_name, bun_price, ingredients, expected_price):
        # Параметризованный тест: проверяет формирование чека для разных комбинаций
        # булок и ингредиентов — корректность строк и совпадение итоговой цены.
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_name.return_value = bun_name
        mock_bun.get_price.return_value = bun_price
        burger.set_buns(mock_bun)

        for ing_type, ing_name, ing_price in ingredients:
            m = Mock()
            m.get_type.return_value = ing_type
            m.get_name.return_value = ing_name
            m.get_price.return_value = ing_price
            burger.add_ingredient(m)

        receipt = burger.get_receipt()
        lines = receipt.split('\n')

        assert lines[0] == f"(==== {bun_name} ====)", f"Неверная верхняя булка: {lines[0]}"
        for i, (ing_type, ing_name, _) in enumerate(ingredients):
            assert lines[i + 1] == f"= {ing_type} {ing_name} =", f"Ошибка в ингредиенте {i}"
        assert lines[len(ingredients) + 1] == f"(==== {bun_name} ====)", "Неверная нижняя булка"

        last_line = lines[-1]
        assert last_line.startswith("Price: ")
        actual_price = float(last_line.replace("Price: ", ""))
        assert actual_price == expected_price, f"Цена не совпадает: {actual_price} != {expected_price}"
