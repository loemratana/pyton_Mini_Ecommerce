# Modern UI Theme Configuration
# Professional color scheme with gradients and modern design

import customtkinter as ctk

class ModernTheme:
    """Modern color theme for the e-commerce application"""
    
    # Primary Colors (Modern gradient palette)
    PRIMARY = "#6366F1"          # Indigo
    PRIMARY_DARK = "#4F46E5"     # Dark Indigo
    PRIMARY_LIGHT = "#818CF8"    # Light Indigo
    PRIMARY_HOVER = "#4F46E5"    # For hover state
    
    # Accent Colors
    SUCCESS = "#10B981"          # Emerald
    SUCCESS_HOVER = "#059669"    # Dark emerald
    WARNING = "#F59E0B"          # Amber
    DANGER = "#EF4444"           # Red
    DANGER_HOVER = "#DC2626"     # Dark red
    INFO = "#3B82F6"             # Blue
    
    # Grays (Neutral palette)
    BG_PRIMARY = "#0F172A"       # Very dark blue (almost black)
    BG_SECONDARY = "#1E293B"     # Dark slate
    BG_TERTIARY = "#334155"      # Medium slate
    
    SURFACE = "#1E293B"          # Card/frame background
    SURFACE_HOVER = "#334155"    # Hover state
    
    TEXT_PRIMARY = "#F1F5F9"     # Nearly white
    TEXT_SECONDARY = "#CBD5E1"   # Light gray
    TEXT_TERTIARY = "#94A3B8"    # Medium gray
    
    BORDER = "#334155"           # Border color
    BORDER_LIGHT = "#475569"     # Light border
    
    # Cache for font objects
    _fonts = {}
    
    @staticmethod
    def setup_appearance():
        """Apply the modern theme globally"""
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize fonts after root is expected to exist
        ModernTheme._fonts["header"] = ctk.CTkFont(family="Segoe UI", size=28, weight="bold")
        ModernTheme._fonts["title"] = ctk.CTkFont(family="Segoe UI", size=22, weight="bold")
        ModernTheme._fonts["subtitle"] = ctk.CTkFont(family="Segoe UI", size=18, weight="bold")
        ModernTheme._fonts["label"] = ctk.CTkFont(family="Segoe UI", size=13, weight="normal")
        ModernTheme._fonts["small"] = ctk.CTkFont(family="Segoe UI", size=11, weight="normal")
        
        ModernTheme.setup_table_style()
    
    @staticmethod
    def setup_table_style():
        """Configure modern styling for ttk.Treeview components"""
        from tkinter import ttk
        style = ttk.Style()
        
        # Check available themes and use 'clam' if available for better customizability
        if "clam" in style.theme_names():
            style.theme_use("clam")
        
        # Configure Treeview colors and fonts
        style.configure("Treeview",
                        background=ModernTheme.SURFACE,
                        foreground=ModernTheme.TEXT_PRIMARY,
                        fieldbackground=ModernTheme.SURFACE,
                        borderwidth=0,
                        font=("Segoe UI", 10),
                        rowheight=45) # Increased row height for modern look
        
        # Selection colors
        style.map("Treeview", 
                  background=[('selected', ModernTheme.PRIMARY)],
                  foreground=[('selected', '#FFFFFF')])
        
        # Heading configuration
        style.configure("Treeview.Heading",
                        background=ModernTheme.BG_SECONDARY,
                        foreground=ModernTheme.TEXT_PRIMARY,
                        borderwidth=0,
                        font=("Segoe UI", 11, "bold"),
                        relief="flat",
                        padding=12)
        
        # Heading hover effect
        style.map("Treeview.Heading",
                  background=[('active', ModernTheme.BG_TERTIARY)])

        # Striped rows (if supported by the specific implementation)
        # We'll use tags in the actual implementations to handle this
    
    @staticmethod
    def get_font(name):
        """Get a cached font or fall back to tuple if not initialized"""
        return ModernTheme._fonts.get(name, ("Segoe UI", 12))

    @staticmethod
    def get_header_font():
        return ModernTheme.get_font("header")
    
    @staticmethod
    def get_title_font():
        return ModernTheme.get_font("title")
    
    @staticmethod
    def get_subtitle_font():
        return ModernTheme.get_font("subtitle")
    
    @staticmethod
    def get_label_font():
        return ModernTheme.get_font("label")
    
    @staticmethod
    def get_small_font():
        return ModernTheme.get_font("small")
    
    @staticmethod
    def create_modern_button(parent, text, command=None, color="primary", width=140, height=40, font=None):
        """Create a modern styled button"""
        color_map = {
            "primary": (ModernTheme.PRIMARY, ModernTheme.PRIMARY_DARK),
            "success": (ModernTheme.SUCCESS, "#059669"),
            "danger": (ModernTheme.DANGER, "#DC2626"),
            "secondary": (ModernTheme.SURFACE_HOVER, ModernTheme.BG_TERTIARY),
            "info": (ModernTheme.INFO, "#2563EB"),
        }
        
        fg_color, hover_color = color_map.get(color, color_map["primary"])
        
        btn = ctk.CTkButton(
            parent,
            text=text,
            command=command,
            fg_color=fg_color,
            hover_color=hover_color,
            text_color=ModernTheme.TEXT_PRIMARY,
            height=height,
            width=width if width else 140,
            corner_radius=10,
            border_width=0,
            font=font if font else ModernTheme.get_label_font(),
            cursor="hand2"
        )
        return btn
    
    @staticmethod
    def create_modern_card(parent, corner_radius=15):
        """Create a modern card frame"""
        return ctk.CTkFrame(
            parent,
            fg_color=ModernTheme.SURFACE,
            corner_radius=corner_radius,
            border_width=1,
            border_color=ModernTheme.BORDER
        )
