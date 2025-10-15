import tkinter as tk
from tkinter import ttk

# ----------------------------
# Data Setup
# ----------------------------
coffee_menu = {
    "Espresso": {"price": 120, "stock": 10},
    "Cappuccino": {"price": 150, "stock": 8},
    "Latte": {"price": 160, "stock": 7},
    "Mocha": {"price": 180, "stock": 5},
    "Americano": {"price": 140, "stock": 9},
    "Cold Coffee": {"price": 130, "stock": 6}
}

# Resources per cup
resources = {"Milk (ml)": 1000, "Water (ml)": 2000, "Coffee (g)": 500, "Sugar (g)": 300}

# ----------------------------
# Tkinter Setup
# ----------------------------
root = tk.Tk()
root.title("☕ Deeksha's Coffee Machine")
root.geometry("500x580")
root.config(bg="#f5e6cc")

# Variables
selected_coffee = tk.StringVar()
quantity = tk.IntVar(value=1)
selected_payment = tk.StringVar()
selected_milk = tk.StringVar()
selected_sugar = tk.StringVar()
selected_temp = tk.StringVar()
total_cost = tk.StringVar(value="₹0")
status_msg = tk.StringVar(value="")

# ----------------------------
# Utility Functions
# ----------------------------
def switch_frame(frame):
    """Switch between frames"""
    frame.tkraise()

def update_stock_display():
    """Update stock labels on home page"""
    stock_text = "\n".join(
        [f"{coffee}: {details['stock']} cups left" for coffee, details in coffee_menu.items()]
    )
    stock_label.config(text=f"☕ Current Stock:\n{stock_text}")

    resource_text = "\n".join([f"{r}: {v}" for r, v in resources.items()])
    resource_label.config(text=f"🧃 Available Resources:\n{resource_text}")

def show_stock():
    """Toggle visibility of stock and resources"""
    if stock_label.winfo_ismapped():
        stock_label.pack_forget()
        resource_label.pack_forget()
    else:
        stock_label.pack(pady=5)
        resource_label.pack(pady=5)

def calculate_total():
    """Calculate total cost"""
    coffee = selected_coffee.get()
    qty = quantity.get()
    if not coffee or qty <= 0:
        total_cost.set("Invalid selection")
        return
    if coffee_menu[coffee]["stock"] < qty:
        total_cost.set("Out of stock")
        return
    cost = coffee_menu[coffee]["price"] * qty
    total_cost.set(f"₹{cost}")

def place_order():
    """Simulate order preparation and update stock/resources"""
    coffee = selected_coffee.get()
    qty = quantity.get()

    if not coffee:
        status_msg.set("Please select a coffee first.")
        return
    if coffee_menu[coffee]["stock"] < qty:
        status_msg.set(f"Sorry, only {coffee_menu[coffee]['stock']} left.")
        return

    # Deduct from stock and resources
    coffee_menu[coffee]["stock"] -= qty
    resources["Milk (ml)"] -= 100 * qty
    resources["Water (ml)"] -= 150 * qty
    resources["Coffee (g)"] -= 20 * qty
    resources["Sugar (g)"] -= 10 * qty

    # Start staged progress animation
    progress_bar["value"] = 0
    status_msg.set("🛒 Order placed. Starting preparation...")
    root.after(800, lambda: make_coffee_stage(0))

def make_coffee_stage(stage):
    """Simulate each stage of coffee preparation"""
    stages = [
        ("Grinding coffee beans...", 25),
        ("Heating water and milk...", 50),
        ("Pouring coffee...", 75),
        ("Final touches and aroma...", 90),
        ("✅ Your coffee is ready. Please collect ☕", 100)
    ]

    if stage < len(stages):
        message, progress = stages[stage]
        status_msg.set(message)
        progress_bar["value"] = progress
        root.after(1200, lambda: make_coffee_stage(stage + 1))

def reset_for_next_order():
    """Reset selections and go back to home"""
    selected_coffee.set("")
    quantity.set(1)
    total_cost.set("₹0")
    status_msg.set("")
    progress_bar["value"] = 0
    update_stock_display()
    switch_frame(home_frame)

# ----------------------------
# Frame 1 — Home Page
# ----------------------------
home_frame = tk.Frame(root, bg="#f5e6cc")
home_frame.place(relwidth=1, relheight=1)

tk.Label(home_frame, text="Welcome to \n☕ Deeksha's Café☕", font=("Arial", 18, "bold"),
         bg="#f5e6cc", fg="#3e2723").pack(pady=20)
tk.Label(home_frame, text="Today's Coffee Menu", font=("Arial", 14, "bold"),
         bg="#f5e6cc", fg="#4e342e").pack(pady=5)

menu_text = "\n".join([f"{name} - ₹{details['price']}" for name, details in coffee_menu.items()])
tk.Label(home_frame, text=menu_text, bg="#f5e6cc", font=("Arial", 11)).pack(pady=10)

# Hidden initially
stock_label = tk.Label(home_frame, text="", bg="#f5e6cc", font=("Arial", 10))
resource_label = tk.Label(home_frame, text="", bg="#f5e6cc", font=("Arial", 10))

# Buttons
tk.Button(home_frame, text="View Stock & Resources", command=show_stock,
          bg="#6d4c41", fg="white", font=("Arial", 12, "bold"), width=22).pack(pady=10)
tk.Button(home_frame, text="Start Order →", command=lambda: switch_frame(order_frame),
          bg="#4e342e", fg="white", font=("Arial", 12, "bold"), width=15).pack(pady=15)

# ----------------------------
# Frame 2 — Order Page
# ----------------------------
order_frame = tk.Frame(root, bg="#f5e6cc")
order_frame.place(relwidth=1, relheight=1)

tk.Label(order_frame, text="Place Your Order", font=("Arial", 16, "bold"),
         bg="#f5e6cc", fg="#3e2723").pack(pady=15)

# Coffee Selection
tk.Label(order_frame, text="Select Coffee:", bg="#f5e6cc", font=("Arial", 11, "bold")).pack()
coffee_dropdown = ttk.Combobox(order_frame, values=list(coffee_menu.keys()), textvariable=selected_coffee)
coffee_dropdown.pack(pady=5)

# Milk Type
tk.Label(order_frame, text="Milk Type:", bg="#f5e6cc", font=("Arial", 11, "bold")).pack()
milk_dropdown = ttk.Combobox(order_frame, values=["Regular", "Low Fat", "Soy", "Almond"], textvariable=selected_milk)
milk_dropdown.pack(pady=5)

# Sugar Level
tk.Label(order_frame, text="Sugar Level:", bg="#f5e6cc", font=("Arial", 11, "bold")).pack()
sugar_dropdown = ttk.Combobox(order_frame, values=["No Sugar", "Less Sugar", "Normal", "Extra Sweet"], textvariable=selected_sugar)
sugar_dropdown.pack(pady=5)

# Temperature
tk.Label(order_frame, text="Temperature:", bg="#f5e6cc", font=("Arial", 11, "bold")).pack()
temp_dropdown = ttk.Combobox(order_frame, values=["Hot", "Warm", "Cold"], textvariable=selected_temp)
temp_dropdown.pack(pady=5)

# Quantity
tk.Label(order_frame, text="Quantity:", bg="#f5e6cc", font=("Arial", 11, "bold")).pack(pady=(10, 0))
tk.Entry(order_frame, textvariable=quantity, width=5, font=("Arial", 12), justify="center").pack(pady=5)

# Payment Mode
tk.Label(order_frame, text="Payment Mode:", bg="#f5e6cc", font=("Arial", 11, "bold")).pack()
payment_dropdown = ttk.Combobox(order_frame, values=["Cash", "Card", "UPI"], textvariable=selected_payment)
payment_dropdown.pack(pady=5)

# Buttons and Total
tk.Button(order_frame, text="Calculate Total", command=calculate_total, bg="#8d6e63", fg="white",
          font=("Arial", 12, "bold"), width=15).pack(pady=10)
tk.Label(order_frame, textvariable=total_cost, font=("Arial", 14, "bold"),
         bg="#f5e6cc", fg="#3e2723").pack(pady=5)

tk.Button(order_frame, text="Place Order", command=place_order, bg="#4e342e", fg="white",
          font=("Arial", 12, "bold"), width=15).pack(pady=10)

# Progress bar + status
progress_bar = ttk.Progressbar(order_frame, orient="horizontal", length=250, mode="determinate")
progress_bar.pack(pady=10)
tk.Label(order_frame, textvariable=status_msg, font=("Arial", 11, "italic"),
         bg="#f5e6cc", fg="#3e2723").pack(pady=10)

tk.Button(order_frame, text="Next Order →", command=reset_for_next_order,
          bg="#6d4c41", fg="white", font=("Arial", 12, "bold"), width=15).pack(pady=15)

# ----------------------------
# Initialize
# ----------------------------
update_stock_display()
switch_frame(home_frame)
root.mainloop()
