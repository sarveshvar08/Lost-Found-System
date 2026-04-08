import customtkinter as ctk
from tkinter import filedialog, messagebox
from data_handler import save_item, read_items, search_items, delete_item
from models import validate_input, format_item
import os, shutil, time
from PIL import Image

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class LostAndFoundApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Lost & Found")
        self.geometry("650x700")

        self.show_home()

    # ================= CLEAR =================
    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    # ================= HOME =================
    def show_home(self):
        self.clear()

        ctk.CTkLabel(self, text="Lost & Found", font=("Comic Sans MS", 40, "bold")).pack(pady=30)

        self.menu_btn("Report Item", self.report_item)
        self.menu_btn("Search Item", self.search_item)
        self.menu_btn("View All Items", self.view_items)

    def menu_btn(self, text, cmd):
        ctk.CTkButton(self, text=text, width=220, height=45, command=cmd).pack(pady=10)

    # ================= REPORT =================
    def report_item(self):
        self.clear()

        ctk.CTkLabel(self, text="Report Item", font=("Comic Sans MS", 24)).pack(pady=20)

        name = ctk.CTkEntry(self, placeholder_text="Item Name", width=300)
        name.pack(pady=10)

        desc = ctk.CTkEntry(self, placeholder_text="Description", width=300)
        desc.pack(pady=10)

        loc = ctk.CTkEntry(self, placeholder_text="Location", width=300)
        loc.pack(pady=10)

        mobile = ctk.CTkEntry(self, placeholder_text="Mobile Number", width=300)
        mobile.pack(pady=10)

        image_path = ""

        preview = ctk.CTkLabel(self, text="")
        preview.pack(pady=10)

        def upload():
            nonlocal image_path
            path = filedialog.askopenfilename(filetypes=[("Image", "*.png *.jpg")])
            if path:
                image_path = path
                img = ctk.CTkImage(light_image=Image.open(path), size=(140, 140))
                preview.configure(image=img)

        ctk.CTkButton(self, text="Upload Image", command=upload).pack(pady=10)

        def submit():
            n, d, l, m = name.get(), desc.get(), loc.get(), mobile.get()

            validate=validate_input(n, d, l, m)
            if validate==False:
                messagebox.showerror("Error", "Fill all fields")
                return
            if validate == "mobile_error":
                messagebox.showerror("Error", "Invalid mobile number")
                return

            if not os.path.exists("images"):
                os.makedirs("images")

            img_dest = ""
            if image_path:
                ext = image_path.split(".")[-1]
                fname = f"{n}_{int(time.time())}.{ext}"
                img_dest = os.path.join("images", fname)
                shutil.copy(image_path, img_dest)

            item = format_item(n, d, l, m, img_dest)
            save_item(item)

            messagebox.showinfo("Success", "Item Saved!")
            self.show_home()

        ctk.CTkButton(self, text="Submit", command=submit).pack(pady=10)
        ctk.CTkButton(self, text="Back", command=self.show_home).pack()

    # ================= CARD =================
    def card(self, parent, item, refresh):
        card = ctk.CTkFrame(parent, corner_radius=12)
        card.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(card, text=item["name"], font=("Arial", 16, "bold")).pack(anchor="w", padx=10, pady=5)
        ctk.CTkLabel(card, text=item["description"]).pack(anchor="w", padx=10)

        ctk.CTkLabel(card, text=f"📍 {item['location']}").pack(anchor="w", padx=10)
        ctk.CTkLabel(card, text=f"📞 {item['mobile_no']}").pack(anchor="w", padx=10)

        if item["image"] and os.path.exists(item["image"]):
            img = ctk.CTkImage(light_image=Image.open(item["image"]), size=(100, 100))
            ctk.CTkLabel(card, image=img, text="").pack(pady=5)

        ctk.CTkButton(
            card,
            text="Checkout",
            fg_color="red",
            command=lambda: self.checkout(item, refresh)
        ).pack(pady=10)

    def checkout(self, item, refresh):
        delete_item(item)
        messagebox.showinfo("Done", "Checked out")
        refresh()

    # ================= SEARCH =================
    def search_item(self):
        self.clear()

        ctk.CTkLabel(self, text="Search Item", font=("Comic Sans MS", 24)).pack(pady=20)

        entry = ctk.CTkEntry(self, placeholder_text="Search...", width=300)
        entry.pack(pady=10)

        frame = ctk.CTkScrollableFrame(self, width=550, height=450)
        frame.pack(pady=10)

        def search():
            for w in frame.winfo_children():
                w.destroy()

            results = search_items(entry.get())

            if not results:
                ctk.CTkLabel(frame, text="No items found").pack()
                return

            for item in results:
                self.card(frame, item, self.search_item)

        ctk.CTkButton(self, text="Search", command=search).pack(pady=10)
        ctk.CTkButton(self, text="Back", command=self.show_home).pack()

    # ================= VIEW =================
    def view_items(self):
        self.clear()

        ctk.CTkLabel(self, text="All Items", font=("Comic Sans MS", 24)).pack(pady=20)

        frame = ctk.CTkScrollableFrame(self, width=550, height=500)
        frame.pack(pady=10)

        items = read_items()

        if not items:
            ctk.CTkLabel(frame, text="No items available").pack()

        for item in items:
            self.card(frame, item, self.view_items)

        ctk.CTkButton(self, text="Back", command=self.show_home).pack(pady=10)


