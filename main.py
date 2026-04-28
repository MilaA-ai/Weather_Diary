import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

# Загрузка данных
try:
    with open("weather.json", "r", encoding="utf-8") as f:
        records = json.load(f)
except:
    records = []

def save_data():
    with open("weather.json", "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=4)

def update_list(show_list=None):
    listbox.delete(0, tk.END)
    if show_list is None:
        show_list = records
    if not show_list:
        listbox.insert(0, "Список пуст")
        return
    for r in show_list:
        osadki = "Да" if r["rain"] else "Нет"
        listbox.insert(tk.END, f"{r['date']} | {r['temp']}°C | {r['desc']} | Осадки: {osadki}")

def add_record():
    date = entry_date.get().strip()
    temp = entry_temp.get().strip()
    desc = entry_desc.get().strip()
    rain = rain_var.get()
    
    # Проверка даты
    if not date:
        messagebox.showerror("Ошибка", "Введите дату!")
        return
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except:
        messagebox.showerror("Ошибка", "Неверный формат даты!\nИспользуйте ГГГГ-ММ-ДД")
        return
    
    # Проверка температуры
    if not temp:
        messagebox.showerror("Ошибка", "Введите температуру!")
        return
    try:
        temp = float(temp)
    except:
        messagebox.showerror("Ошибка", "Температура должна быть числом!")
        return
    
    # Проверка описания
    if not desc:
        messagebox.showerror("Ошибка", "Введите описание погоды!")
        return
    
    # Добавляем
    records.append({
        "date": date,
        "temp": temp,
        "desc": desc,
        "rain": rain
    })
    
    save_data()
    update_list()
    
    # Очистка полей
    entry_date.delete(0, tk.END)
    entry_temp.delete(0, tk.END)
    entry_desc.delete(0, tk.END)
    rain_var.set(False)
    
    messagebox.showinfo("Успех", "Запись добавлена!")

def delete_record():
    selected = listbox.curselection()
    if not selected:
        messagebox.showerror("Ошибка", "Выберите запись для удаления!")
        return
    
    records.pop(selected[0])
    save_data()
    update_list()
    messagebox.showinfo("Успех", "Запись удалена!")

def filter_records():
    date_filter = filter_date.get().strip()
    temp_filter = filter_temp.get().strip()
    
    filtered = records.copy()
    
    # Фильтр по дате
    if date_filter:
        try:
            datetime.strptime(date_filter, "%Y-%m-%d")
            filtered = [r for r in filtered if r["date"] == date_filter]
        except:
            messagebox.showerror("Ошибка", "Неверный формат даты фильтра!\nИспользуйте ГГГГ-ММ-ДД")
            return
    
    # Фильтр по температуре (> значение)
    if temp_filter:
        try:
            temp_val = float(temp_filter)
            filtered = [r for r in filtered if r["temp"] > temp_val]
        except:
            messagebox.showerror("Ошибка", "Температура фильтра должна быть числом!")
            return
    
    update_list(filtered)

def reset_filter():
    filter_date.delete(0, tk.END)
    filter_temp.delete(0, tk.END)
    update_list()

# Окно
root = tk.Tk()
root.title("Weather Diary")
root.geometry("550x650")  # Исправлено: x вместо _

# Заголовок
tk.Label(root, text="ДНЕВНИК ПОГОДЫ", font=("Arial", 14, "bold")).pack(pady=10)

# ===== Форма добавления =====
add_frame = tk.LabelFrame(root, text="Добавить запись")
add_frame.pack(fill="x", padx=10, pady=5)

row1 = tk.Frame(add_frame)
row1.pack(pady=5)

tk.Label(row1, text="Дата (ГГГГ-ММ-ДД):").pack(side="left", padx=5)
entry_date = tk.Entry(row1, width=12)
entry_date.pack(side="left", padx=5)

tk.Label(row1, text="Температура:").pack(side="left", padx=5)
entry_temp = tk.Entry(row1, width=8)
entry_temp.pack(side="left", padx=5)

row2 = tk.Frame(add_frame)
row2.pack(pady=5)

tk.Label(row2, text="Описание:").pack(side="left", padx=5)
entry_desc = tk.Entry(row2, width=30)
entry_desc.pack(side="left", padx=5)

row3 = tk.Frame(add_frame)
row3.pack(pady=5)

rain_var = tk.BooleanVar()
tk.Checkbutton(row3, text="Осадки были", variable=rain_var).pack(side="left", padx=5)

tk.Button(add_frame, text="Добавить запись", command=add_record, bg="green", fg="white").pack(pady=5)

# ===== Фильтрация =====
filter_frame = tk.LabelFrame(root, text="Фильтрация")
filter_frame.pack(fill="x", padx=10, pady=5)

row_f = tk.Frame(filter_frame)
row_f.pack(pady=10)

tk.Label(row_f, text="Дата:").pack(side="left", padx=5)
filter_date = tk.Entry(row_f, width=12)
filter_date.pack(side="left", padx=5)

tk.Label(row_f, text="Температура >").pack(side="left", padx=5)
filter_temp = tk.Entry(row_f, width=8)
filter_temp.pack(side="left", padx=5)

tk.Button(row_f, text="Применить фильтр", command=filter_records, bg="blue", fg="white").pack(side="left", padx=5)
tk.Button(row_f, text="Сбросить", command=reset_filter, bg="orange").pack(side="left", padx=5)

# ===== Список записей =====
list_frame = tk.LabelFrame(root, text="Список записей")
list_frame.pack(fill="both", expand=True, padx=10, pady=5)

listbox = tk.Listbox(list_frame, height=12, font=("Arial", 9))
listbox.pack(fill="both", expand=True, padx=5, pady=5)

# ===== Кнопка удаления =====
tk.Button(root, text="Удалить выбранную запись", command=delete_record, bg="red", fg="white").pack(pady=10)

# Показываем данные
update_list()

root.mainloop()