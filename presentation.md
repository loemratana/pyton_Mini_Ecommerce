---
marp: true
theme: default
paginate: true
---

# Python E-Commerce Application
## Object-Oriented Programming (OOP) Implementation

---

## 🎯 Project Overview

A complete, Tkinter-based Python E-Commerce system designed with modularity and robust architecture in mind.

**Core Features:**
- **Authentication:** Secure Login, Registration, and **Password Management**.
- **Product Management:** Admin inventory control with **Duplicate Name Validation**.
- **User Roles:** Distinct workflows for Admins and Customers.
- **Product Visuals:** High-quality grid view with **Star Rating Display**.
- **Shopping Cart & Checkout:** Manual **Shipping Fee** entry and **Cash Payment** processing.
- **Data Analytics:** Reporting using **Pandas** and **Matplotlib**.

---

## 🏗️ Core OOP Concepts Applied

The application strongly adheres to Object-Oriented Programming principles to ensure the code is clean, scalable, and maintainable:

1. **Encapsulation**
2. **Inheritance**
3. **Polymorphism**

---

## 🔒 1. Encapsulation

**Concept:** Hiding the internal state of an object and requiring all interaction to occur through specialized methods.

**Application in the Project:**
- **`Product` Class** (`models/product.py`): Attributes like `__price` and `__stock` are private. Modification is strictly validated.
- **`ShoppingCart` Class** (`models/cart.py`): Stock availability and item management are encapsulated.
- **`User` Class** (`models/user.py`): Direct password updates are encapsulated in dedicated methods.

---

## 🧬 2. Inheritance

**Concept:** A mechanism where a new class derives properties and behaviors from an existing base class.

**Application in the Project:**
- **Base Class `User`** (`models/user.py`): Defines shared attributes for ID, credentials, and roles.
- **Derived Classes `Admin` and `Customer`** (`models/user.py`): They inherit base attributes but gain specialized implementations:
  - **`Customer`**: Shopping, reviews, and wishlist.
  - **`Admin`**: Product stock, category, and user management.

---

## 🎭 3. Polymorphism

**Concept:** The ability of different objects to interact using the same interface but with specific implementations.

**Application in the Project:**
- **`view_products()` Method** (`models/user.py`): 
  - **Admin Implementation:** Shows technical data (ID, Stock, Raw Price).
  - **Customer Implementation:** Shows marketing data (Name, Star Ratings).
- **GUI Dynamic Rendering** (`gui/profile_tab.py`): The `ProfileTab` dynamically changes its layout using `isinstance()` logic.
  - **Admins** see management tools. 
  - **Customers** see account settings and password security.

---

## 🛡️ Authentication & Security

- **Security Control:** Prevents duplicate product/category names to ensure data integrity.
- **Direct Shipping Entry:** Checkout logic supports dynamic shipping fee calculation.
- **Password Self-Service:** Logged-in users can update their security credentials directly from their profile.

---

## 📊 System Architecture

The project is structured into distinct, modular layers:

- **Models (`models/`):** The OOP backbone (`Product`, `User`, `Cart`, `Order`).
- **Data Layer (`data/`):** 
  - `DataManager` handles multi-file JSON I/O (`products`, `orders`, `users`).
  - `Analytics` processes sales data for business intelligence.
- **GUI Layer (`gui/`):** 
  - `AuthGUI` manages the entry barrier (Login/Register).
  - `AppGUI` manages the main workspace with specialized tabs.

---

## 🚀 Conclusion

By leveraging **Encapsulation**, **Inheritance**, and **Polymorphism**, the E-Commerce application achieves:

✅ **Security:** User accounts and sensitive inventory data are protected and validated.
✅ **Scalability:** The modular structure allows easy addition of new features (e.g., Coupons, Shipping).
✅ **Maintainability:** Separation of concerns ensures that backend data logic and frontend GUI logic remain decoupled.
