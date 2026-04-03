import tkinter as tk
from tkinter import filedialog, messagebox
from data_handler import save_item, read_items, search_items, delete_item
from models import validate_input, format_item
import os
import shutil
import time
from PIL import Image, ImageTk


class LostAndFoundGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Lost & Found")
        self.root.geometry("500x600")

        self.main_menu()
        self.root.mainloop()

    # ================= CLEAR SCREEN =================
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ================= MAIN MENU =================
    def main_menu(self):
        self.clear_screen()

        tk.Label(self.root, text="Lost & Found System", font=("Arial", 18)).pack(pady=20)

        tk.Button(self.root, text="Report Item", width=20, command=self.report_item).pack(pady=10)
        tk.Button(self.root, text="Search Item", width=20, command=self.search_item).pack(pady=10)
        tk.Button(self.root, text="View All Items", width=20, command=self.view_items).pack(pady=10)

    # ================= REPORT ITEM =================
    def report_item(self):
        self.clear_screen()

        tk.Label(self.root, text="Report Item", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Item Name").pack()
        name_entry = tk.Entry(self.root, width=30)
        name_entry.pack(pady=5)

        tk.Label(self.root, text="Description").pack()
        desc_entry = tk.Entry(self.root, width=30)
        desc_entry.pack(pady=5)

        tk.Label(self.root, text="Location").pack()
        location_entry = tk.Entry(self.root, width=30)
        location_entry.pack(pady=5)

        tk.Label(self.root, text="Mobile No").pack()
        mobile_entry = tk.Entry(self.root, width=30)
        mobile_entry.pack(pady=5)

        image_path = tk.StringVar()
        preview_label = tk.Label(self.root)
        preview_label.pack(pady=10)

        def upload_image():
            file_path = filedialog.askopenfilename(
                filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
            )
            if file_path:
                image_path.set(file_path)

                img = Image.open(file_path)
                img = img.resize((150, 150))
                photo = ImageTk.PhotoImage(img)

                preview_label.config(image=photo)
                preview_label.image = photo

        tk.Button(self.root, text="Upload Image", command=upload_image).pack(pady=5)

        def submit():
            name = name_entry.get().strip()
            desc = desc_entry.get().strip()
            location = location_entry.get().strip()
            mobile_no = mobile_entry.get().strip()
            img_src = image_path.get()

            if not validate_input(name, desc, location, mobile_no):
                messagebox.showerror("Error", "Please fill all fields")
                return

            if not os.path.exists("images"):
                os.makedirs("images")

            img_dest = ""

            if img_src:
                try:
                    ext = img_src.split(".")[-1]
                    safe_name = name.replace(" ", "_")
                    filename = f"{safe_name}_{int(time.time())}.{ext}"
                    img_dest = os.path.join("images", filename)

                    shutil.copy(img_src, img_dest)
                except Exception as e:
                    messagebox.showerror("Error", f"Image failed: {e}")
                    return

            item = format_item(name, desc, location, mobile_no, img_dest)
            save_item(item)

            messagebox.showinfo("Success", "Item saved successfully!")
            self.main_menu()

        tk.Button(self.root, text="Submit", command=submit).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=5)

    # ================= SEARCH =================
    def search_item(self):
        self.clear_screen()

        tk.Label(self.root, text="Search Item", font=("Arial", 16)).pack(pady=10)

        search_entry = tk.Entry(self.root, width=30)
        search_entry.pack(pady=5)

        canvas = tk.Canvas(self.root)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def checkout(item):
            delete_item(item)
            messagebox.showinfo("Success", "Item checked out!")
            self.search_item()

        def search():
            for widget in scroll_frame.winfo_children():
                widget.destroy()

            keyword = search_entry.get().strip()
            results = search_items(keyword)

            if not results:
                tk.Label(scroll_frame, text="No items found").pack()
                return

            for item in results:
                tk.Label(scroll_frame, text=f"{item['name']} - {item['description']}").pack() 
                tk.Label(scroll_frame, text=f"Location: {item['location']}").pack()
                tk.Label(scroll_frame, text=f"Mobile No: {item['mobile_no']}").pack()


                tk.Button(
                    scroll_frame,
                    text="Checkout",
                    command=lambda i=item: checkout(i)
                ).pack(pady=5)

                tk.Label(scroll_frame, text="-" * 30).pack()

        tk.Button(self.root, text="Search", command=search).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=5)

    # ================= VIEW ITEMS =================
    def view_items(self):
        self.clear_screen()

        tk.Label(self.root, text="All Items", font=("Arial", 16)).pack(pady=10)

        items = read_items()

        canvas = tk.Canvas(self.root)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def checkout(item):
            delete_item(item)
            messagebox.showinfo("Success", "Item checked out!")
            self.view_items()

        if not items:
            tk.Label(scroll_frame, text="No items found").pack()

        for item in items:
            tk.Label(scroll_frame, text=f"Name: {item['name']}", font=("Arial", 10, "bold")).pack()
            tk.Label(scroll_frame, text=f"Description: {item['description']}").pack()
            tk.Label(scroll_frame, text=f"Location: {item['location']}").pack()
            tk.Label(scroll_frame, text=f"Mobile No: {item['mobile_no']}").pack()

            if item["image"] and os.path.exists(item["image"]):
                try:
                    img = Image.open(item["image"])
                    img = img.resize((120, 120))
                    photo = ImageTk.PhotoImage(img)

                    label = tk.Label(scroll_frame, image=photo)
                    label.image = photo
                    label.pack(pady=5)
                except:
                    pass

            tk.Button(
                scroll_frame,
                text="Checkout",
                command=lambda i=item: checkout(i)
            ).pack(pady=5)

            tk.Label(scroll_frame, text="-" * 40).pack(pady=5)

        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)


