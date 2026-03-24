import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk
from gui.theme import ModernTheme

class CategoryTab(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=ModernTheme.BG_PRIMARY)
        self.app = app
        
        # Main container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Header
        header_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 25))
        
        self.header = ctk.CTkLabel(header_frame, text="📂 Category Management",
                                   font=ModernTheme.get_title_font(),
                                   text_color=ModernTheme.TEXT_PRIMARY)
        self.header.pack(anchor="w")
        
        self.sub_header = ctk.CTkLabel(header_frame, text="Organize your product inventory by category",
                                       font=ModernTheme.get_small_font(),
                                       text_color=ModernTheme.TEXT_SECONDARY)
        self.sub_header.pack(anchor="w", pady=(5, 0))

        # Toolbar with search and actions
        toolbar_frame = ModernTheme.create_modern_card(main_container)
        toolbar_frame.pack(fill="x", pady=(0, 20))
        
        toolbar_content = ctk.CTkFrame(toolbar_frame, fg_color="transparent")
        toolbar_content.pack(fill="x", padx=20, pady=15)
        
        # Search section
        search_frame = ctk.CTkFrame(toolbar_content, fg_color="transparent")
        search_frame.pack(side="left", fill="x", expand=True)
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="🔍 Search categories...", 
                                         width=250, height=40,
                                         fg_color=ModernTheme.SURFACE,
                                         border_color=ModernTheme.BORDER,
                                         border_width=1,
                                         text_color=ModernTheme.TEXT_PRIMARY)
        self.search_entry.pack(side="left", padx=(0, 15))
        self.search_entry.bind("<KeyRelease>", self.on_search)
        
        # Action buttons
        action_frame = ctk.CTkFrame(toolbar_content, fg_color="transparent")
        action_frame.pack(side="right")
        
        self.add_btn = ModernTheme.create_modern_button(action_frame, "✨ New Category",
                                                        command=self.add_category, color="success", 
                                                        height=40, width=150)
        self.add_btn.pack(side="right", padx=(10, 0))
        
        self.del_btn = ModernTheme.create_modern_button(action_frame, "🗑️ Delete",
                                                        command=self.delete_category, color="danger",
                                                        height=40, width=100)
        self.del_btn.pack(side="right", padx=5)
        self.del_btn.configure(state="disabled")
        
        self.edit_btn = ModernTheme.create_modern_button(action_frame, "✏️ Edit",
                                                         command=self.edit_category, color="primary",
                                                         height=40, width=100)
        self.edit_btn.pack(side="right", padx=5)
        self.edit_btn.configure(state="disabled")

        # Tabs: Table view and Card view
        view_tab_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        view_tab_frame.pack(fill="x", pady=(0, 15))
        
        view_label = ctk.CTkLabel(view_tab_frame, text="📋 View:",
                                 font=ModernTheme.get_label_font(),
                                 text_color=ModernTheme.TEXT_SECONDARY)
        view_label.pack(side="left", padx=(0, 10))
        
        self.view_var = tk.StringVar(value="table")
        table_radio = ctk.CTkRadioButton(view_tab_frame, text="Table", value="table",
                                        variable=self.view_var, command=self.switch_view,
                                        fg_color=ModernTheme.PRIMARY,
                                        text_color=ModernTheme.TEXT_PRIMARY)
        table_radio.pack(side="left", padx=5)
        
        card_radio = ctk.CTkRadioButton(view_tab_frame, text="Cards", value="card",
                                       variable=self.view_var, command=self.switch_view,
                                       fg_color=ModernTheme.PRIMARY,
                                       text_color=ModernTheme.TEXT_PRIMARY)
        card_radio.pack(side="left", padx=5)

        # Table view container
        self.table_frame_container = ModernTheme.create_modern_card(main_container)
        self.table_frame_container.pack(fill="both", expand=True)
        
        # Centralized styling is already initialized in app.py via ModernTheme.setup_appearance()

        cols = ("ID", "Category Name", "Description", "Products Count")
        self.tree = ttk.Treeview(self.table_frame_container, columns=cols, show="headings", height=15)
        
        # Configure alternating row colors
        self.tree.tag_configure('oddrow', background=ModernTheme.BG_SECONDARY)
        self.tree.tag_configure('evenrow', background=ModernTheme.SURFACE)
        
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Card view container
        self.card_view_container = ctk.CTkScrollableFrame(main_container, fg_color="transparent")
        self.card_view_container.pack(fill="both", expand=True)
        self.card_view_container.pack_forget()  # Hidden initially
        
        self.refresh_table()

    def on_search(self, event):
        self.refresh_table()

    def on_select(self, event):
        state = "normal" if self.tree.selection() else "disabled"
        self.del_btn.configure(state=state)
        self.edit_btn.configure(state=state)

    def switch_view(self):
        if self.view_var.get() == "table":
            # Show table, hide cards
            self.table_frame_container.pack(fill="both", expand=True)
            self.card_view_container.pack_forget()
            self.refresh_table()
        else:
            # Show cards, hide table
            self.table_frame_container.pack_forget()
            self.card_view_container.pack(fill="both", expand=True)
            self.refresh_cards()

    def refresh_table(self):
        for item in self.tree.get_children(): 
            self.tree.delete(item)
        
        query = self.search_entry.get().lower()
        categories = self.app.categories
        
        if query:
            categories = [c for c in categories if query in c.name.lower() or query in c.description.lower()]
        
        for i, c in enumerate(categories):
            tag = 'oddrow' if i % 2 == 0 else 'evenrow'
            product_count = len([p for p in self.app.products if p.get_category() == c.name])
            self.tree.insert("", tk.END, values=(c.cat_id, c.name, c.description, product_count), tags=(tag,))

    def refresh_cards(self):
        # Clear previous cards
        for widget in self.card_view_container.winfo_children():
            widget.destroy()
        
        query = self.search_entry.get().lower()
        categories = self.app.categories
        
        if query:
            categories = [c for c in categories if query in c.name.lower() or query in c.description.lower()]
        
        if not categories:
            empty_label = ctk.CTkLabel(self.card_view_container, text="No categories found",
                                      font=ModernTheme.get_label_font(),
                                      text_color=ModernTheme.TEXT_SECONDARY)
            empty_label.pack(pady=40)
            return
        
        # Display as cards (2 columns)
        cards_container = ctk.CTkFrame(self.card_view_container, fg_color="transparent")
        cards_container.pack(fill="both", expand=True)
        
        for idx, cat in enumerate(categories):
            card = ModernTheme.create_modern_card(cards_container)
            # Grid layout: 2 columns
            col = idx % 2
            row = idx // 2
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            
            card_content = ctk.CTkFrame(card, fg_color="transparent")
            card_content.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Category header
            cat_header = ctk.CTkFrame(card_content, fg_color="transparent")
            cat_header.pack(fill="x", pady=(0, 10))
            
            cat_name_label = ctk.CTkLabel(cat_header, text=f"📁 {cat.name}",
                                         font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
                                         text_color=ModernTheme.PRIMARY)
            cat_name_label.pack(anchor="w")
            
            # Stats
            product_count = len([p for p in self.app.products if p.get_category() == cat.name])
            stats_label = ctk.CTkLabel(card_content, text=f"📦 {product_count} products",
                                      font=ModernTheme.get_label_font(),
                                      text_color=ModernTheme.TEXT_SECONDARY)
            stats_label.pack(anchor="w", pady=(0, 15))
            
            # Description
            desc_label = ctk.CTkLabel(card_content, text=cat.description if cat.description else "No description",
                                     font=ModernTheme.get_label_font(),
                                     text_color=ModernTheme.TEXT_SECONDARY,
                                     wraplength=250)
            desc_label.pack(anchor="w", pady=(0, 20))
            
            # Action buttons
            action_btn_frame = ctk.CTkFrame(card_content, fg_color="transparent")
            action_btn_frame.pack(fill="x")
            
            edit_card_btn = ModernTheme.create_modern_button(action_btn_frame, "✏️ Edit",
                                                             command=lambda c=cat: self.edit_category_from_card(c),
                                                             color="primary", width=80, height=35)
            edit_card_btn.pack(side="left", padx=(0, 10))
            
            delete_card_btn = ModernTheme.create_modern_button(action_btn_frame, "🗑️ Delete",
                                                               command=lambda c=cat: self.delete_category_by_id(c.cat_id),
                                                               color="danger", width=80, height=35)
            delete_card_btn.pack(side="left")
        
        # Configure grid weights
        cards_container.grid_columnconfigure(0, weight=1)
        cards_container.grid_columnconfigure(1, weight=1)

    def add_category(self):
        self._open_category_form()

    def edit_category(self):
        sel = self.tree.selection()
        if not sel: return
        cid = self.tree.item(sel[0])['values'][0]
        cat = next((c for c in self.app.categories if c.cat_id == cid), None)
        if cat:
            self._open_category_form(cat)

    def edit_category_from_card(self, cat):
        self._open_category_form(cat)

    def delete_category_by_id(self, cat_id):
        if messagebox.askyesno("Confirm", "Delete this category?"):
            self.app.categories = [c for c in self.app.categories if c.cat_id != cat_id]
            self.app.data_manager.save_categories(self.app.categories)
            if self.view_var.get() == "card":
                self.refresh_cards()
            else:
                self.refresh_table()

    def delete_category(self):
        sel = self.tree.selection()
        if not sel: return
        cid = self.tree.item(sel[0])['values'][0]
        self.delete_category_by_id(cid)

    def _open_category_form(self, category=None):
        form = ctk.CTkToplevel(self)
        form.title("✏️ Edit Category" if category else "✨ New Category")
        form.geometry("500x400")
        form.configure(fg_color=ModernTheme.BG_PRIMARY)
        form.attributes("-topmost", True)
        
        # Main container
        main_frame = ctk.CTkFrame(form, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Header
        title_text = "Edit Category" if category else "Create New Category"
        title = ctk.CTkLabel(main_frame, text=title_text,
                            font=ModernTheme.get_title_font(),
                            text_color=ModernTheme.PRIMARY)
        title.pack(anchor="w", pady=(0, 25))

        # Form card
        form_card = ModernTheme.create_modern_card(main_frame)
        form_card.pack(fill="both", expand=True)
        
        input_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        input_frame.pack(padx=25, pady=25, fill="both", expand=True)

        # Name field
        ctk.CTkLabel(input_frame, text="Category Name",
                     font=ModernTheme.get_label_font(),
                     text_color=ModernTheme.TEXT_PRIMARY).pack(anchor="w", pady=(0, 8))
        name_e = ctk.CTkEntry(input_frame, width=300, height=45, 
                              placeholder_text="e.g., Electronics",
                              fg_color=ModernTheme.SURFACE,
                              border_color=ModernTheme.BORDER,
                              border_width=1)
        name_e.insert(0, category.name if category else "")
        name_e.pack(pady=(0, 20))
        
        # Description field
        ctk.CTkLabel(input_frame, text="Description",
                     font=ModernTheme.get_label_font(),
                     text_color=ModernTheme.TEXT_PRIMARY).pack(anchor="w", pady=(0, 8))
        desc_e = ctk.CTkEntry(input_frame, width=300, height=80,
                              placeholder_text="Add a description...",
                              fg_color=ModernTheme.SURFACE,
                              border_color=ModernTheme.BORDER,
                              border_width=1)
        desc_e.insert(0, category.description if category else "")
        desc_e.pack(pady=(0, 25))
        
        # Button frame
        button_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        button_frame.pack(fill="x")
        
        def save():
            name = name_e.get().strip()
            desc = desc_e.get().strip()
            if not name:
                messagebox.showwarning("Invalid", "Category name cannot be empty")
                return
                
            # Duplicate Category Name Validation
            for c in self.app.categories:
                # If editing, skip the CURRENT category object
                if category and c.cat_id == category.cat_id:
                    continue
                
                if c.name.lower() == name.lower():
                    messagebox.showwarning("Duplicate Category", f"A category with the name '{name}' already exists.")
                    return
            
            from models.category import Category
            if category:
                category.name = name
                category.description = desc
            else:
                new_id = max([c.cat_id for c in self.app.categories], default=0) + 1
                new_c = Category(new_id, name, desc)
                self.app.categories.append(new_c)
            
            self.app.data_manager.save_categories(self.app.categories)
            if self.view_var.get() == "card":
                self.refresh_cards()
            else:
                self.refresh_table()
            form.destroy()
            
        save_btn = ModernTheme.create_modern_button(button_frame, "💾 Save Category",
                                                    command=save, color="success", width=300, height=50)
        save_btn.pack()
