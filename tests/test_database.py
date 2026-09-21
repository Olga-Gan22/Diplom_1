import pytest
from praktikum.database import Database
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING


def test_database_initialization():
    """Проверяем, что при создании БД списки инициализируются и не пустые."""
    db = Database()
    
    # Проверяем, что списки созданы
    assert isinstance(db.buns, list)
    assert isinstance(db.ingredients, list)
    
    # Проверяем, что они не пустые (база наполняется в __init__)
    assert len(db.buns) > 0
    assert len(db.ingredients) > 0


def test_available_buns_returns_list():
    """Проверяем метод available_buns."""
    db = Database()
    buns = db.available_buns()
    
    # Проверяем тип возврата
    assert isinstance(buns, list)
    
    # Проверяем, что вернулись именно объекты Bun
    assert all(isinstance(bun, Bun) for bun in buns)
    
    # Проверяем конкретные данные, которые мы знаем (из кода __init__)
    # Ищем булку "black bun"
    black_bun = next((b for b in buns if b.name == "black bun"), None)
    assert black_bun is not None
    assert black_bun.price == 100


def test_available_ingredients_returns_list():
    """Проверяем метод available_ingredients."""
    db = Database()
    ingredients = db.available_ingredients()
    
    assert isinstance(ingredients, list)
    assert all(isinstance(ing, Ingredient) for ing in ingredients)
    
    # Проверяем наличие конкретного ингредиента (например, соуса)
    hot_sauce = next((i for i in ingredients if i.name == "hot sauce"), None)
    assert hot_sauce is not None
    assert hot_sauce.type == INGREDIENT_TYPE_SAUCE
    
    # Проверяем наличие начинки
    cutlet = next((i for i in ingredients if i.name == "cutlet"), None)
    assert cutlet is not None
    assert cutlet.type == INGREDIENT_TYPE_FILLING
