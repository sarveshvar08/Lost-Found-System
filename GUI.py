import tkinter as tk
from tkinter import filedialog, messagebox
from data_handler import save_item
from models import validate_input, format_item
import os
import shutil
import time


class LostAndFoundGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Lost & Found")
        self.root.geometry("400x450")

        self.main_menu()

        self.root.mainloop()

    # ================= CLEAR SCREEN =================
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ================= MAIN MENU =================
    def main_menu(self):
        self.clear_screen()

        tk.Label(self.root, text="Lost & Found System", font=("Arial", 16)).pack(pady=20)

        tk.Button(self.root, text="Report Item", width=20, command=self.report_item).pack(pady=10)
        tk.Button(self.root, text="Search Item", width=20, command=self.search_item).pack(pady=10)
        tk.Button(self.root, text="View All Items", width=20, command=self.view_items).pack(pady=10)

    # ================= REPORT ITEM =================
    def report_item(self):
        self.clear_screen()

        tk.Label(self.root, text="Report Item", font=("Arial", 14)).pack(pady=10)

        # Name
        tk.Label(self.root, text="Item Name").pack()
        name_entry = tk.Entry(self.root, width=30)
        name_entry.pack(pady=5)

        # Description
        tk.Label(self.root, text="Description").pack()
        desc_entry = tk.Entry(self.root, width=30)
        desc_entry.pack(pady=5)

        # Image path
        image_path = tk.StringVar()

        # Upload image
        def upload_image():
            file_path = filedialog.askopenfilename(
                filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
            )
            if file_path:
                image_path.set(file_path)
                messagebox.showinfo("Selected", "Image selected!")

        tk.Button(self.root, text="Upload Image", command=upload_image).pack(pady=5)

        # Submit
        def submit():
            name = name_entry.get().strip()
            desc = desc_entry.get().strip()
            img_src = image_path.get()

            # Validate
            if not validate_input(name, desc):
                messagebox.showerror("Error", "Please fill all fields")
                return

            # Create images folder
            if not os.path.exists("images"):
                os.makedirs("images")

            img_dest = ""

            # Copy image
            if img_src:
                try:
                    ext = img_src.split(".")[-1]
                    safe_name = name.replace(" ", "_")
                    filename = f"{safe_name}_{int(time.time())}.{ext}"

                    img_dest = os.path.join("images", filename)

                    shutil.copy(img_src, img_dest)

                except Exception as e:
                    messagebox.showerror("Error", f"Image copy failed: {e}")
                    return

            # Save data
            item = format_item(name, desc, img_dest)
            save_item(item)

            messagebox.showinfo("Success", "Item saved successfully!")
            self.main_menu()

        tk.Button(self.root, text="Submit", command=submit).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=5)

    # ================= SEARCH =================
    def search_item(self):
        self.clear_screen()

        tk.Label(self.root, text="Search Screen (Next Step)", font=("Arial", 14)).pack(pady=20)
        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)

    # ================= VIEW =================
    def view_items(self):
        self.clear_screen()

        tk.Label(self.root, text="View Items Screen (Next Step)", font=("Arial", 14)).pack(pady=20)
        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)

