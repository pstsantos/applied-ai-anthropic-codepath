┌─────────────────────────┐          ┌─────────────────────────┐
│       UserAccount       │          │          Menu           │
├─────────────────────────┤          ├─────────────────────────┤
│ - name: String          │          │ - items: List<Item>     │
│ - purchaseHistory:      │          ├─────────────────────────┤
│     List<Order>         │          │ + addItem(Item)         │
├─────────────────────────┤          │ + removeItem(Item)      │
│ + isVerifiedUser(): bool│          │ + filterByCategory(     │
└─────────────────────────┘          │     String): List<Item> │
           │                         └─────────────────────────┘
           │ places                             │ contains
           ▼                                    ▼
┌─────────────────────────┐          ┌─────────────────────────┐
│          Order          │          │          Item           │
├─────────────────────────┤          ├─────────────────────────┤
│ - items: List<OrderItem>│          │ - name: String          │
├─────────────────────────┤          │ - price: Float          │
│ + addItem(OrderItem)    │          │ - category: String      │
│ + computeTotal(): Float │          │ - popularityRating: Int │
└─────────────────────────┘          └─────────────────────────┘
           │                                    ▲
           │ contains                           │ references
           ▼                                    │
┌─────────────────────────┐                     │
│        OrderItem        │─────────────────────┘
├─────────────────────────┤
│ - item: Item            │
│ - quantity: Int         │
├─────────────────────────┤
│ + getSubtotal(): Float  │
└─────────────────────────┘
