from models import Item, Menu, Order, OrderItem, UserAccount


# ============================================================================
# STEP 1: Create some menu items
# ============================================================================
burger = Item(
    name="Spicy Burger",
    price=12.99,
    category="Mains",
    popularity_rating=4
)

fries = Item(
    name="Crispy Fries",
    price=4.50,
    category="Sides",
    popularity_rating=5
)

soda = Item(
    name="Large Soda",
    price=3.00,
    category="Drinks",
    popularity_rating=3
)

dessert = Item(
    name="Chocolate Cake",
    price=6.99,
    category="Desserts",
    popularity_rating=5
)

print("✅ Created 4 menu items:")
print(f"   - {burger.name} (${burger.price})")
print(f"   - {fries.name} (${fries.price})")
print(f"   - {soda.name} (${soda.price})")
print(f"   - {dessert.name} (${dessert.price})")
print()


# ============================================================================
# STEP 2: Create a menu and add items
# ============================================================================
menu = Menu()
menu.add_item(burger)
menu.add_item(fries)
menu.add_item(soda)
menu.add_item(dessert)

print("✅ Created menu with 4 items")
print()


# ============================================================================
# STEP 3: Filter menu by category
# ============================================================================
drinks = menu.filter_by_category("Drinks")
desserts = menu.filter_by_category("Desserts")
mains = menu.filter_by_category("Mains")

print("✅ Filtered menu by category:")
print(f"   - Drinks: {[item.name for item in drinks]}")
print(f"   - Desserts: {[item.name for item in desserts]}")
print(f"   - Mains: {[item.name for item in mains]}")
print()


# ============================================================================
# STEP 4: Create a user account
# ============================================================================
user = UserAccount(name="Alice")
print(f"✅ Created user: {user.name}")
print(f"   Is verified? {user.is_verified_user()}  (no purchases yet)")
print()


# ============================================================================
# STEP 5: Create an order and add items
# ============================================================================
order = Order()

# Add burger x2
order_item_1 = OrderItem(item=burger, quantity=2)
order.add_item(order_item_1)
print(f"✅ Added 2x {burger.name} → subtotal: ${order_item_1.get_subtotal():.2f}")

# Add fries x1
order_item_2 = OrderItem(item=fries, quantity=1)
order.add_item(order_item_2)
print(f"✅ Added 1x {fries.name} → subtotal: ${order_item_2.get_subtotal():.2f}")

# Add soda x2
order_item_3 = OrderItem(item=soda, quantity=2)
order.add_item(order_item_3)
print(f"✅ Added 2x {soda.name} → subtotal: ${order_item_3.get_subtotal():.2f}")

print()


# ============================================================================
# STEP 6: Compute order total
# ============================================================================
total = order.compute_total()
print(f"✅ Order total: ${total:.2f}")
print()


# ============================================================================
# STEP 7: Finalize purchase (add order to user history)
# ============================================================================
user.add_purchase(order)
print(f"✅ Order added to user history")
print(f"   Is {user.name} verified now? {user.is_verified_user()}  (has purchases)")
print(f"   Purchase history size: {len(user.purchase_history)}")
print()


# ============================================================================
# STEP 8: Create another order to show multiple purchases
# ============================================================================
order2 = Order()
order_item_4 = OrderItem(item=dessert, quantity=1)
order2.add_item(order_item_4)
user.add_purchase(order2)

print(f"✅ Added second order to {user.name}'s history")
print(f"   Total orders: {len(user.purchase_history)}")
print()


# ============================================================================
# DEMO SUMMARY
# ============================================================================
print("=" * 60)
print("DEMO SUMMARY")
print("=" * 60)
print(f"Menu items: {len(menu.items)}")
print(f"User: {user.name}")
print(f"User verified: {user.is_verified_user()}")
print(f"User purchase history: {len(user.purchase_history)} orders")
print(f"First order total: ${user.purchase_history[0].compute_total():.2f}")
print(f"Second order total: ${user.purchase_history[1].compute_total():.2f}")
print(f"Total spent: ${sum(o.compute_total() for o in user.purchase_history):.2f}")