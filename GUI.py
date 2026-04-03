def search_item(self):
    self.clear_screen()

    import tkinter as tk
    from data_handler import search_items

    tk.Label(self.root, text="Search Item", font=("Arial", 14)).pack(pady=10)

    # Input field
    search_entry = tk.Entry(self.root, width=30)
    search_entry.pack(pady=5)

    # Result display
    result_box = tk.Text(self.root, height=12, width=45)
    result_box.pack(pady=10)

    # Search logic
    def search():
        keyword = search_entry.get().strip()

        result_box.delete(1.0, tk.END)

        if not keyword:
            result_box.insert(tk.END, "Enter a keyword\n")
            return

        results = search_items(keyword)

        if not results:
            result_box.insert(tk.END, "No items found\n")
            return

        for item in results:
            name = item.get("name", "")
            desc = item.get("description", "")

            result_box.insert(tk.END, f"Name: {name}\n")
            result_box.insert(tk.END, f"Description: {desc}\n")
            result_box.insert(tk.END, "-" * 40 + "\n")

    # Buttons
    tk.Button(self.root, text="Search", width=15, command=search).pack(pady=5)
    tk.Button(self.root, text="Back", width=15, command=self.main_menu).pack(pady=5)