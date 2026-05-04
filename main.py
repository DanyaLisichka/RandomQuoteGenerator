import tkinter as tk
from tkinter import messagebox
import random
import json
import os

HISTORY_FILE = "history.json"

quotes = [
    {"text": "Оставайся голодным, оставайся глупым.", "author": "Стив Джобс", "topic": "Мотивация"},
    {"text": "Код подобен юмору. Когда вам приходится что-то объяснять, это плохо.", "author": "Дом Кори", "topic": "Программирование"},
    {"text": "Разговоры ничего не стоят. Покажите мне код", "author": "Линус Торвальдс", "topic": "Programming"},
    {"text": "Единственное ограничение - это ваш разум.", "author": "Неизвестный", "topic": "Мотивация"},
]

history = []


def load_history():
    global history
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)


def save_history():
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)


def generate_quote():
    author_filter = author_entry.get().strip()
    topic_filter = topic_entry.get().strip()

    filtered = quotes

    if author_filter:
        filtered = [q for q in filtered if q["author"].lower() == author_filter.lower()]

    if topic_filter:
        filtered = [q for q in filtered if q["topic"].lower() == topic_filter.lower()]

    if not filtered:
        messagebox.showwarning("Ошибка", "Нет цитат по заданным фильтрам")
        return

    quote = random.choice(filtered)

    text = f'{quote["text"]}\n— {quote["author"]} [{quote["topic"]}]'
    quote_label.config(text=text)

    history.append(quote)
    update_history_list()
    save_history()


def update_history_list():
    history_listbox.delete(0, tk.END)
    for q in history:
        history_listbox.insert(
            tk.END,
            f'{q["text"][:70]} — {q["author"]}'
        )


def add_quote():
    text = new_text_entry.get().strip()
    author = new_author_entry.get().strip()
    topic = new_topic_entry.get().strip()

    if not text or not author or not topic:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
        return

    quotes.append({
        "text": text,
        "author": author,
        "topic": topic
    })

    messagebox.showinfo("Успех", "Цитата добавлена")

    new_text_entry.delete(0, tk.END)
    new_author_entry.delete(0, tk.END)
    new_topic_entry.delete(0, tk.END)



root = tk.Tk()
root.title("Random Quote Generator")
root.geometry("600x500")

# Цитата
quote_label = tk.Label(root, text="Нажмите кнопку", wraplength=500, justify="center")
quote_label.pack(pady=10)

# Фильтры
tk.Label(root, text="Фильтр по автору").pack()
author_entry = tk.Entry(root)
author_entry.pack()

tk.Label(root, text="Фильтр по теме").pack()
topic_entry = tk.Entry(root)
topic_entry.pack()

# Кнопка генерации
generate_btn = tk.Button(root, text="Сгенерировать цитату", command=generate_quote)
generate_btn.pack(pady=10)

# История
tk.Label(root, text="История").pack()
history_listbox = tk.Listbox(root, width=70, height=10)
history_listbox.pack()

# Добавление цитаты
tk.Label(root, text="Добавить новую цитату").pack(pady=5)

new_text_entry = tk.Entry(root, width=50)
new_text_entry.pack()
new_text_entry.insert(0, "Текст")

new_author_entry = tk.Entry(root)
new_author_entry.pack()
new_author_entry.insert(0, "Автор")

new_topic_entry = tk.Entry(root)
new_topic_entry.pack()
new_topic_entry.insert(0, "Тема")

add_btn = tk.Button(root, text="Добавить", command=add_quote)
add_btn.pack(pady=5)

# Загрузка истории
load_history()
update_history_list()

root.mainloop()