classDiagram
    class Customer {
        +String name
        +List~Order~ purchaseHistory
    }

    class MenuItem {
        +String name
        +Float price
        +String category
        +Float popularityRating
    }

    class Menu {
        +List~MenuItem~ items
        +filterByCategory(category: String) List~MenuItem~
    }

    class Order {
        +List~MenuItem~ selectedItems
        +computeTotal() Float
    }

    class Validation {
        +verifyCustomer(customer: Customer) Boolean
    }

    Customer "1" --> "0..*" Order : places
    Order "1" o-- "1..*" MenuItem : contains
    Menu "1" *-- "1..*" MenuItem : holds
    Validation ..> Customer : validates
