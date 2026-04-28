import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json

class BookTracker:
    def __init__(self, master):
        self.master = master
        self.master.title("Book Tracker")
        self.books = []

        # Создаем интерфейс
        self.create_widgets()
        self.load_data()  # Попытка подгрузить сохраненные данные

    def create_widgets(self):
        # Поля для ввода
        frame_input = tk.Frame(self.master)
        frame_input.pack(padx=10, pady=10)

        tk.Label(frame_input, text="Название книги").grid(row=0, column=0, sticky="w")
        tk.Label(frame_input, text="Автор").grid(row=1, column=0, sticky="w")
        tk.Label(frame_input, text="Жанр").grid(row=2, column=0, sticky="w")
        tk.Label(frame_input, text="Количество страниц").grid(row=3, column=0, sticky="w")

        self.title_entry = tk.Entry(frame_input)
        self.author_entry = tk.Entry(frame_input)
        self.genre_entry = tk.Entry(frame_input)
        self.pages_entry = tk.Entry(frame_input)

        self.title_entry.grid(row=0, column=1)
        self.author_entry.grid(row=1, column=1)
        self.genre_entry.grid(row=2, column=1)
        self.pages_entry.grid(row=3, column=1)

        # Кнопка для добавления книги
        btn_add = tk.Button(frame_input, text="Добавить книгу", command=self.add_book)
        btn_add.grid(row=4, column=0, columnspan=2, pady=5)

        # Таблица для отображения книг
        columns = ("Название", "Автор", "Жанр", "Страницы")
        self.tree = ttk.Treeview(self.master, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Фильтры
        filter_frame = tk.Frame(self.master)
        filter_frame.pack(padx=10, pady=5)

        # Фильтр по жанру
        tk.Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0)
        self.genre_filter_var = tk.StringVar()
        self.genre_filter_entry = tk.Entry(filter_frame, textvariable=self.genre_filter_var)
        self.genre_filter_entry.grid(row=0, column=1)
        self.genre_filter_entry.bind("<KeyRelease>", lambda e: self.apply_filters())

        # Фильтр по страницам (больше)
        tk.Label(filter_frame, text="Страниц >").grid(row=0, column=2)
        self.pages_filter_var = tk.StringVar()
        self.pages_filter_entry = tk.Entry(filter_frame, textvariable=self.pages_filter_var)
        self.pages_filter_entry.grid(row=0, column=3)
        self.pages_filter_entry.bind("<KeyRelease>", lambda e: self.apply_filters())

        # Меню для сохранения/загрузки
        menubar = tk.Menu(self.master)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Сохранить в JSON", command=self.save_data)
        filemenu.add_command(label="Загрузить из JSON", command=self.load_data)
        menubar.add_cascade(label="Файл", menu=filemenu)
        self.master.config(menu=menubar)

        # Кнопки для очистки фильтров
        clear_btn = tk.Button(filter_frame, text="Очистить фильтры", command=self.clear_filters)
        clear_btn.grid(row=0, column=4, padx=5)

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages = self.pages_entry.get().strip()

        # Проверка
        if not title or not author or not genre or not pages:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
            return
        if not pages.isdigit():
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом")
            return

        book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": int(pages)
        }
        self.books.append(book)
        self.refresh_tree()
        self.clear_entries()

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)

    def refresh_tree(self, filtered_books=None):
        for i in self.tree.get_children():
            self.tree.delete(i)
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
        filename = filedialog.asksaveasfilename(defaultextension=".json",
                                                filetypes=[("JSON files", "*.json")])
        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(self.books, f, ensure_ascii=False, indent=4)
                messagebox.showinfo("Успех", "Данные сохранены")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")

    def load_data(self):
        filename = filedialog.askopenfilename(defaultextension=".json",
                                              filetypes=[("JSON файлы", "*.json")])
        if filename:
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    self.books = json.load(f)
                self.refresh_tree()
                messagebox.showinfo("Успех", "Данные загружены")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()