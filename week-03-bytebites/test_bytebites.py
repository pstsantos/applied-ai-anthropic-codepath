import pytest
from models import Item, Menu, Order, OrderItem, UserAccount


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def item():
    return Item(name="Burger", price=10.0, category="Mains", popularity_rating=3)

@pytest.fixture
def menu():
    m = Menu()
    m.add_item(Item(name="Fries",  price=4.00,  category="Sides",  popularity_rating=5))
    m.add_item(Item(name="Burger", price=10.00, category="Mains",  popularity_rating=3))
    m.add_item(Item(name="Steak",  price=25.00, category="Mains",  popularity_rating=4))
    m.add_item(Item(name="Soda",   price=3.00,  category="Drinks", popularity_rating=2))
    return m

@pytest.fixture
def user():
    return UserAccount(name="Alice")


# ── Item — validation ─────────────────────────────────────────────────────────

def test_item_rejects_empty_name():
    with pytest.raises(ValueError):
        Item(name="", price=5.0, category="Mains", popularity_rating=3)

def test_item_rejects_negative_price():
    with pytest.raises(ValueError):
        Item(name="Burger", price=-1.0, category="Mains", popularity_rating=3)

def test_item_rejects_rating_above_5():
    with pytest.raises(ValueError):
        Item(name="Burger", price=5.0, category="Mains", popularity_rating=6)

def test_item_rejects_negative_rating():
    with pytest.raises(ValueError):
        Item(name="Burger", price=5.0, category="Mains", popularity_rating=-1)

def test_item_accepts_boundary_rating_0():
    item = Item(name="Burger", price=5.0, category="Mains", popularity_rating=0)
    assert item.popularity_rating == 0

def test_item_accepts_boundary_rating_5():
    item = Item(name="Burger", price=5.0, category="Mains", popularity_rating=5)
    assert item.popularity_rating == 5


# ── Menu.filter_by_category ───────────────────────────────────────────────────

def test_filter_by_category_returns_matching_items(menu):
    result = menu.filter_by_category("Mains")
    assert len(result) == 2
    assert all(i.category == "Mains" for i in result)

def test_filter_by_category_is_case_insensitive(menu):
    assert len(menu.filter_by_category("mains")) == 2
    assert len(menu.filter_by_category("MAINS")) == 2

def test_filter_by_category_returns_empty_for_unknown(menu):
    assert menu.filter_by_category("Desserts") == []


# ── Menu.filter_by_max_price ──────────────────────────────────────────────────

def test_filter_by_max_price_includes_items_at_threshold(menu):
    result = menu.filter_by_max_price(10.00)
    prices = [i.price for i in result]
    assert 4.00 in prices
    assert 10.00 in prices
    assert 25.00 not in prices

def test_filter_by_max_price_returns_empty_when_all_exceed(menu):
    assert menu.filter_by_max_price(1.00) == []

def test_filter_by_max_price_does_not_mutate_menu(menu):
    original_count = len(menu.items)
    menu.filter_by_max_price(5.00)
    assert len(menu.items) == original_count


# ── Menu.sort_by_price ────────────────────────────────────────────────────────

def test_sort_by_price_ascending(menu):
    result = menu.sort_by_price(ascending=True)
    prices = [i.price for i in result]
    assert prices == sorted(prices)

def test_sort_by_price_descending(menu):
    result = menu.sort_by_price(ascending=False)
    prices = [i.price for i in result]
    assert prices == sorted(prices, reverse=True)

def test_sort_by_price_defaults_to_ascending(menu):
    result = menu.sort_by_price()
    assert result[0].price == min(i.price for i in menu.items)

def test_sort_by_price_does_not_mutate_menu(menu):
    first_before = menu.items[0].name
    menu.sort_by_price()
    assert menu.items[0].name == first_before


# ── Menu.sort_by_popularity ───────────────────────────────────────────────────

def test_sort_by_popularity_highest_first(menu):
    result = menu.sort_by_popularity()
    ratings = [i.popularity_rating for i in result]
    assert ratings == sorted(ratings, reverse=True)

def test_sort_by_popularity_does_not_mutate_menu(menu):
    first_before = menu.items[0].name
    menu.sort_by_popularity()
    assert menu.items[0].name == first_before


# ── Order.compute_total ───────────────────────────────────────────────────────

def test_compute_total_sums_subtotals(item):
    order = Order()
    order.add_item(OrderItem(item, quantity=2))  # 2 * 10.0 = 20.0
    assert order.compute_total() == 20.0

def test_compute_total_across_multiple_lines(item):
    cheap = Item(name="Fries", price=4.0, category="Sides", popularity_rating=2)
    order = Order()
    order.add_item(OrderItem(item, quantity=1))   # 10.0
    order.add_item(OrderItem(cheap, quantity=2))  # 8.0
    assert order.compute_total() == 18.0


# ── Order.get_item_count ──────────────────────────────────────────────────────

def test_get_item_count_sums_quantities(item):
    cheap = Item(name="Fries", price=4.0, category="Sides", popularity_rating=2)
    order = Order()
    order.add_item(OrderItem(item, quantity=2))
    order.add_item(OrderItem(cheap, quantity=4))
    assert order.get_item_count() == 6

def test_get_item_count_empty_order():
    assert Order().get_item_count() == 0


# ── UserAccount.add_purchase ──────────────────────────────────────────────────

def test_add_purchase_adds_to_history(user, item):
    order = Order()
    order.add_item(OrderItem(item, quantity=1))
    user.add_purchase(order)
    assert len(user.purchase_history) == 1

def test_add_purchase_rejects_empty_order(user):
    with pytest.raises(ValueError):
        user.add_purchase(Order())


# ── UserAccount.is_verified_user ──────────────────────────────────────────────

def test_is_verified_user_false_with_no_purchases(user):
    assert user.is_verified_user() is False

def test_is_verified_user_true_after_purchase(user, item):
    order = Order()
    order.add_item(OrderItem(item, quantity=1))
    user.add_purchase(order)
    assert user.is_verified_user() is True


# ── UserAccount.compute_total_spent ──────────────────────────────────────────

def test_compute_total_spent_sums_all_orders(user, item):
    order1 = Order()
    order1.add_item(OrderItem(item, quantity=2))  # 20.0
    order2 = Order()
    order2.add_item(OrderItem(item, quantity=1))  # 10.0
    user.add_purchase(order1)
    user.add_purchase(order2)
    assert user.compute_total_spent() == 30.0

def test_compute_total_spent_returns_zero_with_no_purchases(user):
    assert user.compute_total_spent() == 0.0


# ── Menu.remove_item ──────────────────────────────────────────────────────────

def test_remove_item_removes_existing_item(menu):
    item = menu.items[0]
    menu.remove_item(item)
    assert item not in menu.items

def test_remove_item_reduces_count(menu):
    original_count = len(menu.items)
    menu.remove_item(menu.items[0])
    assert len(menu.items) == original_count - 1

def test_remove_item_ignores_unknown_item(menu):
    stranger = Item(name="Ghost", price=9.0, category="Mains", popularity_rating=1)
    original_count = len(menu.items)
    menu.remove_item(stranger)
    assert len(menu.items) == original_count


# ── OrderItem — quantity validation ───────────────────────────────────────────

def test_order_item_rejects_zero_quantity(item):
    with pytest.raises(ValueError):
        OrderItem(item, quantity=0)

def test_order_item_rejects_negative_quantity(item):
    with pytest.raises(ValueError):
        OrderItem(item, quantity=-1)
