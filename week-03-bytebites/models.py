from __future__ import annotations

'''
UserAccount // user info and past
Menu // manages what's available
Item // a single food/drink product with name, price, category, rating
OrderItem // item being added to order
Order // total/final order
'''


class Order:
    def __init__(self) -> None:
        self.items: list[OrderItem] = []

    def add_item(self, order_item: OrderItem) -> None:
        self.items.append(order_item)

    def compute_total(self) -> float:
        return sum(item.get_subtotal() for item in self.items)

    def get_item_count(self) -> int:
        return sum(order_item.quantity for order_item in self.items)


class UserAccount:
    def __init__(self, name: str) -> None:
        if not name or not name.strip():
            raise ValueError("User name cannot be empty")
        
        self.name: str = name
        self.purchase_history: list[Order] = []

    def is_verified_user(self) -> bool:
        return len(self.purchase_history) > 0
    
    def add_purchase(self, order: Order) -> None:
        if not order.items:
            raise ValueError("Cannot add an empty order to purchase history")
        self.purchase_history.append(order)

    def compute_total_spent(self) -> float:
        return sum(order.compute_total() for order in self.purchase_history)


class Item:
    def __init__(
        self,
        name: str,
        price: float,
        category: str,
        popularity_rating: int,
    ) -> None:
        if not name or not name.strip():
            raise ValueError("Item name cannot be empty")
        if price < 0:
            raise ValueError("Item price cannot be negative")
        if not category or not category.strip():
            raise ValueError("Item category cannot be empty")
        if not (0 <= popularity_rating <= 5):
            raise ValueError("Popularity rating must be between 0 and 5")
        
        self.name: str = name
        self.price: float = price
        self.category: str = category
        self.popularity_rating: int = popularity_rating


class OrderItem:
    def __init__(self, item: Item, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        
        self.item: Item = item
        self.quantity: int = quantity

    def get_subtotal(self) -> float:
        return self.item.price * self.quantity


class Menu:
    def __init__(self) -> None:
        self.items: list[Item] = []

    def add_item(self, item: Item) -> None:
        self.items.append(item)

    def remove_item(self, item: Item) -> None:
        if item in self.items:
            self.items.remove(item)

    def filter_by_category(self, category: str) -> list[Item]:
        return [item for item in self.items if item.category.lower() == category.lower()]

    def filter_by_max_price(self, max_price: float) -> list[Item]:
        return [item for item in self.items if item.price <= max_price]

    def sort_by_price(self, ascending: bool = True) -> list[Item]:
        return sorted(self.items, key=lambda item: item.price, reverse=not ascending)

    def sort_by_popularity(self) -> list[Item]:
        return sorted(self.items, key=lambda item: item.popularity_rating, reverse=True)


if __name__ == "__main__":

    def make_item(name="Burger", price=10.0, category="Mains", rating=3):
        return Item(name=name, price=price, category=category, popularity_rating=rating)

    def make_order(*order_items):
        order = Order()
        for oi in order_items:
            order.add_item(oi)
        return order

    passed = 0
    failed = 0

    def check(label, condition):
        global passed, failed
        if condition:
            print(f"  PASS  {label}")
            passed += 1
        else:
            print(f"  FAIL  {label}")
            failed += 1

    def raises(label, exc_type, fn):
        global passed, failed
        try:
            fn()
            print(f"  FAIL  {label} (no exception raised)")
            failed += 1
        except exc_type:
            print(f"  PASS  {label}")
            passed += 1

    # ── Menu.filter_by_max_price ──────────────────────────────────────────────
    print("\n--- Menu.filter_by_max_price ---")
    menu = Menu()
    cheap  = make_item("Fries",  price=4.00)
    mid    = make_item("Burger", price=10.00)
    pricey = make_item("Steak",  price=25.00)
    menu.add_item(cheap); menu.add_item(mid); menu.add_item(pricey)

    result = menu.filter_by_max_price(10.00)
    check("includes items at or below threshold", cheap in result and mid in result)
    check("excludes items above threshold", pricey not in result)
    check("returns empty when all exceed threshold", menu.filter_by_max_price(1.00) == [])
    check("does not mutate menu", len(menu.items) == 3)

    # ── Menu.sort_by_price ────────────────────────────────────────────────────
    print("\n--- Menu.sort_by_price ---")
    check("ascending", [i.price for i in menu.sort_by_price(ascending=True)] == [4.00, 10.00, 25.00])
    check("descending", [i.price for i in menu.sort_by_price(ascending=False)] == [25.00, 10.00, 4.00])
    check("defaults to ascending", menu.sort_by_price()[0].price == 4.00)
    check("does not mutate menu", menu.items[0].price == 4.00)

    # ── Menu.sort_by_popularity ───────────────────────────────────────────────
    print("\n--- Menu.sort_by_popularity ---")
    pop_menu = Menu()
    pop_menu.add_item(make_item("A", rating=2))
    pop_menu.add_item(make_item("B", rating=5))
    pop_menu.add_item(make_item("C", rating=3))
    check("highest rating first", [i.popularity_rating for i in pop_menu.sort_by_popularity()] == [5, 3, 2])
    check("does not mutate menu", pop_menu.items[0].popularity_rating == 2)

    # ── Menu.filter_by_category (case-insensitivity) ──────────────────────────
    print("\n--- Menu.filter_by_category (case-insensitive) ---")
    cat_menu = Menu()
    cat_menu.add_item(make_item(category="Drinks"))
    check("lowercase input matches stored case", len(cat_menu.filter_by_category("drinks")) == 1)
    check("uppercase input matches stored case", len(cat_menu.filter_by_category("DRINKS")) == 1)

    # ── Order.get_item_count ──────────────────────────────────────────────────
    print("\n--- Order.get_item_count ---")
    item_a = make_item("A")
    item_b = make_item("B")
    order = make_order(OrderItem(item_a, quantity=2), OrderItem(item_b, quantity=4))
    check("sums quantities across all lines", order.get_item_count() == 6)
    check("empty order returns 0", Order().get_item_count() == 0)

    # ── UserAccount.add_purchase ──────────────────────────────────────────────
    print("\n--- UserAccount.add_purchase ---")
    user = UserAccount("Alice")
    user.add_purchase(make_order(OrderItem(make_item(), quantity=1)))
    check("adds order to history", len(user.purchase_history) == 1)
    raises("rejects empty order", ValueError, lambda: user.add_purchase(Order()))
    check("empty order does not verify user", not UserAccount("Bob").is_verified_user())

    # ── UserAccount.compute_total_spent ───────────────────────────────────────
    print("\n--- UserAccount.compute_total_spent ---")
    spender = UserAccount("Carol")
    item = make_item(price=5.00)
    spender.add_purchase(make_order(OrderItem(item, quantity=2)))  # 10.00
    spender.add_purchase(make_order(OrderItem(item, quantity=3)))  # 15.00
    check("sums totals across all orders", spender.compute_total_spent() == 25.00)
    check("returns 0 with no purchases", UserAccount("Dave").compute_total_spent() == 0.0)

    # ── Item popularity_rating bounds ─────────────────────────────────────────
    print("\n--- Item.popularity_rating bounds ---")
    raises("rejects rating above 5", ValueError, lambda: make_item(rating=6))
    raises("rejects negative rating", ValueError, lambda: make_item(rating=-1))
    check("accepts 0", make_item(rating=0).popularity_rating == 0)
    check("accepts 5", make_item(rating=5).popularity_rating == 5)

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n{'='*40}")
    print(f"  {passed} passed  |  {failed} failed")
    print(f"{'='*40}")

