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
- **Authentication:** Secure Login and Registration system for all users.
- **Product Management:** Admin control for inventory (Add/Update/Delete).
- **User Roles:** Distinct workflows and permissions for Admins and Customers.
- **User Management:** Admin tools to create new Admins and view all users.
- **Shopping Cart & Checkout:** Persistent sessions and order processing.
- **Data Analytics:** Advanced reporting using **Pandas** and **Matplotlib**.

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
- **`Product` Class:** Attributes like `__price` and `__stock` are private. Modification happens only via controlled setter methods that validate data.
- **`ShoppingCart` Class:** The `__items` storage is protected. Logical checks (like stock availability) are performed within the class before any modification.
- **User Data:** Account credentials like passwords are encapsulated within User objects and persisted securely in `users.txt`.

---

## 🧬 2. Inheritance

**Concept:** A mechanism where a new class derives properties and behaviors from an existing base class.

**Application in the Project:**
- **Base Class `User`:** Defines shared attributes: `user_id`, `name`, `email`, `password`, and `role`.
- **Derived Classes `Admin` and `Customer`:** 
  - They inherit all base attributes but implement unique functionality.
  - **`Customer`**: Focuses on shopping and order history.
  - **`Admin`**: Gains specialized management tools for products and users.

---

## 🎭 3. Polymorphism

**Concept:** The ability of different objects to interact using the same interface but with specific implementations.

**Application in the Project:**
- **`view_products()` Method:** 
  - **Admin Implementation:** Shows technical data (ID, Stock, Raw Price).
  - **Customer Implementation:** Shows marketing data (Name, Discounted Price).
- **GUI Dynamic Rendering:** The `ProfileTab` dynamically changes its layout. If the logged-in object is an `Admin`, it renders **User Management Tools**; otherwise, it shows only personal info.

---

## 🛡️ Authentication & Security

**New System Features:**
- **Login GUI:** Validates users against a persistent database (`users.txt`).
- **Registration Form:** Allows new customers to self-register with automatic ID generation.
- **Admin Elevation:** Existing Admins can create new Admin accounts, showcasing restricted access control logic.
- **Session Persistence:** Remembers user carts across sessions using JSON storage.

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
