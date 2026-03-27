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


class UserAccount:
    def __init__(self, name: str) -> None:
        if not name or not name.strip():
            raise ValueError("User name cannot be empty")
        
        self.name: str = name
        self.purchase_history: list[Order] = []

    def is_verified_user(self) -> bool:
        return len(self.purchase_history) > 0
    
    def add_purchase(self, order: Order) -> None:
        self.purchase_history.append(order)


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
        if popularity_rating < 0:
            raise ValueError("Popularity rating cannot be negative")
        
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
        return [item for item in self.items if item.category == category]




