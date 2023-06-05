import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime
from reportlab.pdfgen import canvas
from pyfiglet import Figlet


class RestaurantApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Restaurant Billing App")
        self.geometry("600x600")
        self.configure(bg="white")

        self.menu_items = [
            {"name": "Pizza", "price": 12.99},
            {"name": "Burger", "price": 8.99},
            {"name": "Pasta", "price": 9.99},
            {"name": "Salad", "price": 6.99},
        ]
        self.selected_items = []

        self.dark_mode = False

        self.create_menu_display()
        self.create_order_management()
        self.create_order_summary()
        self.create_customer_details()
        self.create_receipt_buttons()
        self.create_pdf_receipt_button()
        self.create_dark_mode_button()

    def create_menu_display(self):
        self.menu_frame = tk.Frame(self, bg="white")
        self.menu_frame.pack(pady=20)

        for i, item in enumerate(self.menu_items):
            item_label = tk.Label(self.menu_frame, text=f"{item['name']} - ${item['price']:.2f}", bg="white")
            item_label.grid(row=i, column=0, padx=20, pady=5)

            quantity_entry = tk.Entry(self.menu_frame, width=5)
            quantity_entry.grid(row=i, column=1, padx=10, pady=5)

            add_button = tk.Button(self.menu_frame, text="Add", bg="white", command=lambda item=item,
                                                                                     quantity_entry=quantity_entry:
            self.add_item(item, quantity_entry))
            add_button.grid(row=i, column=2, padx=10, pady=5)

    def create_order_management(self):
        self.order_frame = tk.Frame(self, bg="white")
        self.order_frame.pack(pady=20)

        self.order_label = tk.Label(self.order_frame, text="Order Management", bg="white", font=("Arial", 16, "bold"))
        self.order_label.pack()

        self.order_listbox = tk.Listbox(self.order_frame, width=50)
        self.order_listbox.pack(pady=10)

    def create_order_summary(self):
        self.order_summary_frame = tk.Frame(self, bg="white")
        self.order_summary_frame.pack(pady=20)

        self.order_summary_label = tk.Label(self.order_summary_frame, text="Order Summary", bg="white",
                                            font=("Arial", 16, "bold"))
        self.order_summary_label.pack()

        self.total_label = tk.Label(self.order_summary_frame, text="Total Amount: $0.00", bg="white", font=("Arial", 12))
        self.total_label.pack(pady=5)

    def create_customer_details(self):
        self.customer_details_frame = tk.Frame(self, bg="white")
        self.customer_details_frame.pack(pady=20)

        self.name_label = tk.Label(self.customer_details_frame, text="Name:", bg="white")
        self.name_label.grid(row=0, column=0, padx=5, pady=5)

        self.name_entry = tk.Entry(self.customer_details_frame, width=30)
        self.name_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

        self.age_label = tk.Label(self.customer_details_frame, text="Age:", bg="white")
        self.age_label.grid(row=1, column=0, padx=5, pady=5)

        self.age_entry = tk.Entry(self.customer_details_frame, width=30)
        self.age_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        self.details_label = tk.Label(self.customer_details_frame, text="Details:", bg="white")
        self.details_label.grid(row=2, column=0, padx=5, pady=5)

        self.details_entry = tk.Entry(self.customer_details_frame, width=30)
        self.details_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

    def create_receipt_buttons(self):
        self.receipt_frame = tk.Frame(self, bg="white")
        self.receipt_frame.pack(pady=20)

        self.print_button = tk.Button(self.receipt_frame, text="Print Receipt", bg="white",
                                      command=self.print_receipt)
        self.print_button.grid(row=0, column=0, padx=10)

        self.save_csv_button = tk.Button(self.receipt_frame, text="Save Order Details (CSV)", bg="white",
                                         command=self.save_order_details_csv)
        self.save_csv_button.grid(row=0, column=1, padx=10)

    def create_pdf_receipt_button(self):
        self.pdf_button = tk.Button(self.receipt_frame, text="Save Receipt (PDF)", bg="white",
                                    command=self.save_receipt_as_pdf)
        self.pdf_button.grid(row=0, column=2, padx=10)

    def create_dark_mode_button(self):
        self.dark_mode_frame = tk.Frame(self, bg="white")
        self.dark_mode_frame.pack(pady=20)

        self.dark_mode_label = tk.Label(self.dark_mode_frame, text="Dark Mode", bg="white",
                                        font=("Arial", 16, "bold"))
        self.dark_mode_label.grid(row=0, column=0, columnspan=2)

        self.dark_mode_button = tk.Button(self.dark_mode_frame, text="Toggle Dark Mode", bg="white",
                                          command=self.toggle_dark_mode)
        self.dark_mode_button.grid(row=1, column=0, columnspan=2, pady=10)

    def add_item(self, item, quantity_entry):
        quantity = quantity_entry.get()

        if quantity:
            try:
                quantity = int(quantity)
                if quantity > 0:
                    item_with_quantity = {
                        "name": item["name"],
                        "price": item["price"],
                        "quantity": quantity
                    }

                    self.selected_items.append(item_with_quantity)

                    quantity_entry.delete(0, tk.END)
                else:
                    messagebox.showerror("Error", "Quantity should be a positive integer.")
            except ValueError:
                messagebox.showerror("Error", "Quantity should be a positive integer.")
        else:
            item_with_quantity = {
                "name": item["name"],
                "price": item["price"],
                "quantity": 1
            }

            self.selected_items.append(item_with_quantity)

        self.update_order_summary()

    def update_order_summary(self):
        self.order_listbox.delete(0, tk.END)

        for item in self.selected_items:
            name = item["name"]
            quantity = item["quantity"]
            price = item["price"]
            total_price = quantity * price
            item_text = f"{name} ({quantity}) - ${total_price:.2f}"
            self.order_listbox.insert(tk.END, item_text)

        total_amount = self.calculate_total_amount()
        self.total_label.config(text=f"Total Amount: ${total_amount:.2f}")

    def calculate_total_amount(self):
        return sum(item["quantity"] * item["price"] for item in self.selected_items)

    def print_receipt(self):
        customer_name = self.name_entry.get()
        customer_age = self.age_entry.get()
        customer_details = self.details_entry.get()

        receipt = f"*** THE JAMMU PIZZA ***\n"
        receipt += f"Customer Name: {customer_name}\n"
        receipt += f"Customer Age: {customer_age}\n"
        receipt += f"Customer Details: {customer_details}\n\n"
        receipt += "Order Details:\n"
        for item in self.selected_items:
            name = item["name"]
            quantity = item["quantity"]
            price = item["price"]
            total_price = quantity * price
            item_text = f"{name} ({quantity}) - ${total_price:.2f}"
            receipt += f"{item_text}\n"
        receipt += f"Total Amount: ${self.calculate_total_amount():.2f}"

        messagebox.showinfo("Receipt", receipt)

    def save_order_details_csv(self):
        customer_name = self.name_entry.get()
        customer_age = self.age_entry.get()
        customer_details = self.details_entry.get()

        filename = f"order_details_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Customer Name", "Customer Age", "Customer Details", "Order Details"])
            writer.writerow([customer_name, customer_age, customer_details, ""])
            writer.writerow(["Item Name", "Quantity", "Price"])
            for item in self.selected_items:
                writer.writerow([item["name"], item["quantity"], item["price"]])
            writer.writerow(["Total Amount", self.calculate_total_amount()])

        messagebox.showinfo("Order Details Saved", f"Order details saved as {filename}")

    def save_receipt_as_pdf(self):
        customer_name = self.name_entry.get()
        customer_age = self.age_entry.get()
        customer_details = self.details_entry.get()

        receipt_filename = f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

        c = canvas.Canvas(receipt_filename)
        c.setPageSize((400, 600))

        f = Figlet(font="slant")
        store_name = f.renderText("THE JAMMU PIZZA")
        c.setFont("Helvetica-Bold", 20)
        c.drawString(50, 550, store_name)

        c.setFont("Helvetica", 12)
        c.drawString(50, 500, "Customer Name: " + customer_name)
        c.drawString(50, 480, "Customer Age: " + customer_age)
        c.drawString(50, 460, "Customer Details: " + customer_details)

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 420, "Order Details")

        c.setFont("Helvetica", 12)
        y = 400
        for item in self.selected_items:
            name = item["name"]
            quantity = item["quantity"]
            price = item["price"]
            total_price = quantity * price
            item_text = f"{name} ({quantity}) - ${total_price:.2f}"
            c.drawString(50, y, item_text)
            y -= 20

        c.setFont("Helvetica-Bold", 14)
        total_amount = self.calculate_total_amount()
        c.drawString(50, y - 20, "Total Amount: $" + f"{total_amount:.2f}")

        c.showPage()
        c.save()

        messagebox.showinfo("Receipt Saved", f"Receipt saved as {receipt_filename}")

    def toggle_dark_mode(self):
        if self.dark_mode:
            self.configure(bg="white")
            self.menu_frame.configure(bg="white")
            self.order_frame.configure(bg="white")
            self.order_summary_frame.configure(bg="white")
            self.customer_details_frame.configure(bg="white")
            self.receipt_frame.configure(bg="white")
            self.dark_mode_frame.configure(bg="white")
            self.dark_mode = False
        else:
            self.configure(bg="black")
            self.menu_frame.configure(bg="black")
            self.order_frame.configure(bg="black")
            self.order_summary_frame.configure(bg="black")
            self.customer_details_frame.configure(bg="black")
            self.receipt_frame.configure(bg="black")
            self.dark_mode_frame.configure(bg="black")
            self.dark_mode = True


if __name__ == "__main__":
    app = RestaurantApp()
    app.mainloop()
