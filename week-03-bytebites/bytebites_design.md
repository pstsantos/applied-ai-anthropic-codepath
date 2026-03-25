classDiagram
    class UserAccount {
        +String name
        +List~Order~ purchaseHistory
        +isVerifiedUser() bool
    }

    class Menu {
        +List~Item~ items
        +addItem(Item) void
        +removeItem(Item) void
        +filterByCategory(String) List~Item~
    }

    class Item {
        +String name
        +Float price
        +String category
        +Int popularityRating
    }

    class OrderItem {
        +Item item
        +Int quantity
        +getSubtotal() Float
    }

    class Order {
        +List~OrderItem~ items
        +addItem(OrderItem) void
        +computeTotal() Float
    }

    UserAccount "1" --> "0..*" Order : places
    Menu "1" o-- "1..*" Item : contains
    Order "1" *-- "1..*" OrderItem : contains
    OrderItem ..> Item : references

