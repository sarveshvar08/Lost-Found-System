import tkinter as tk

class LostAndFoundGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Lost & Found")
        self.root.geometry("400x400")

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

    # ================= REPORT SCREEN =================
    def report_item(self):
        self.clear_screen()

        tk.Label(self.root, text="Report Screen", font=("Arial", 14)).pack(pady=20)

        tk.Button(self.root, text="Back", width=15, command=self.main_menu).pack(pady=10)

    # ================= SEARCH SCREEN =================
    def search_item(self):
        self.clear_screen()

        tk.Label(self.root, text="Search Screen", font=("Arial", 14)).pack(pady=20)

        tk.Button(self.root, text="Back", width=15, command=self.main_menu).pack(pady=10)

    # ================= VIEW SCREEN =================
    def view_items(self):
        self.clear_screen()

        tk.Label(self.root, text="View Items Screen", font=("Arial", 14)).pack(pady=20)

        tk.Button(self.root, text="Back", width=15, command=self.main_menu).pack(pady=10)


# ================= RUN APP =================
if __name__ == "__main__":
    app = LostAndFoundGUI()