import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os

class BookTracker:
    DEFAULT_FILE = "books.json"

    def __init__(self, master):
        self.master = master
        self.master.title("Book Tracker")
        self.books = []

        self.create_widgets()

        self.load_data(auto=True)

    def create_widgets(self):
        frame_input = tk.Frame(self.master)
        frame_input.pack(padx=10, pady=10, fill=tk.X)

        labels = ["Название книги", "Автор", "Жанр", "Количество страниц"]
        self.entries = {}
        for i, label in enumerate(labels):
            tk.Label(frame_input, text=label).grid(row=i, column=0, sticky="w")
            entry = tk.Entry(frame_input)
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=2)
            self.entries[label] = entry

        btn_add = tk.Button(frame_input, text="Добавить книгу", command=self.add_book)
        btn_add.grid(row=len(labels), column=0, columnspan=2, pady=5)

        frame_input.columnconfigure(1, weight=1)

        columns = ("Название", "Автор", "Жанр", "Страницы")
        self.tree = ttk.Treeview(self.master, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        filter_frame = tk.Frame(self.master)
        filter_frame.pack(padx=10, pady=5, fill=tk.X)

        tk.Label(filter_frame, text="Фильтр по жанру:").pack(side=tk.LEFT)
        self.genre_filter_var = tk.StringVar()
        genre_entry = tk.Entry(filter_frame, textvariable=self.genre_filter_var)
        genre_entry.pack(side=tk.LEFT, padx=5)
        genre_entry.bind("<KeyRelease>", lambda e: self.apply_filters())

        tk.Label(filter_frame, text="Страниц >").pack(side=tk.LEFT)
        self.pages_filter_var = tk.StringVar()
        pages_entry = tk.Entry(filter_frame, textvariable=self.pages_filter_var, width=5)
        pages_entry.pack(side=tk.LEFT, padx=5)
        pages_entry.bind("<KeyRelease>", lambda e: self.apply_filters())

        btn_clear_filters = tk.Button(filter_frame, text="Очистить фильтры", command=self.clear_filters)
        btn_clear_filters.pack(side=tk.LEFT, padx=5)

        menubar = tk.Menu(self.master)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Сохранить в JSON", command=self.save_data)
        filemenu.add_command(label="Загрузить из JSON", command=self.load_data)
        menubar.add_cascade(label="Файл", menu=filemenu)
        self.master.config(menu=menubar)

    def add_book(self):
        title = self.entries["Название книги"].get().strip()
        author = self.entries["Автор"].get().strip()
        genre = self.entries["Жанр"].get().strip()
        pages_str = self.entries["Количество страниц"].get().strip()

        if not title or not author or not genre or not pages_str:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
            return
        if not pages_str.isdigit():
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом")
            return

        book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": int(pages_str)
        }
        self.books.append(book)
        self.refresh_tree()
        self.clear_entries()

    def clear_entries(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def refresh_tree(self, filtered_books=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        data = filtered_books if filtered_books is not None else self.books
        for book in data:
            self.tree.insert("", tk.END, values=(
                book["title"], book["author"], book["genre"], book["pages"]
            ))

    def apply_filters(self):
        genre_filter = self.genre_filter_var.get().lower()
        pages_filter = self.pages_filter_var.get()

        filtered = []
        for book in self.books:
            if genre_filter and genre_filter not in book["genre"].lower():
                continue
            if pages_filter:
                try:
                    if book["pages"] <= int(pages_filter):
                        continue
                except ValueError:
                    continue
            filtered.append(book)

        self.refresh_tree(filtered)

    def clear_filters(self):
        self.genre_filter_var.set("")
        self.pages_filter_var.set("")
        self.refresh_tree()

    def save_data(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON файлы", "*.json")]
        )
        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(self.books, f, ensure_ascii=False, indent=4)
                messagebox.showinfo("Успех", "Данные успешно сохранены")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")

    def load_data(self, auto=False):
        filename = self.DEFAULT_FILE if auto else filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON файлы", "*.json")]
        )
        if filename:
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    self.books = json.load(f)
                self.refresh_tree()
                if not auto:
                    messagebox.showinfo("Успех", "Данные загружены")
            except Exception as e:
                if not auto:
                    messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()