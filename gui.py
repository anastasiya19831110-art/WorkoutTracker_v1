import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from models import Workout
from storage import save_workout, load_workouts
from analysis import get_workout_report, show_workout_chart
from utils import validate_duration_format, clean_text


class WorkoutApp:
    """
    Главный класс приложения для управления графическим интерфейсом.
    Обеспечивает ввод данных, их валидацию, отображение таблицы и вызов анализа.
    """

    def __init__(self, root):
        """Инициализация главного окна, создание виджетов и загрузка таблицы."""
        self.root = root
        self.root.title("Трекер тренировок")
        self.root.geometry("950x650")

        # --- Секция ввода данных ---
        tk.Label(root, text="Длительность (мин):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.value_entry = tk.Entry(root)
        self.value_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(root, text="Вид спорта:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.activity_entry = tk.Entry(root)
        self.activity_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Установка текущей даты по умолчанию
        current_date = datetime.now().strftime("%Y-%m-%d")
        tk.Label(root, text="Дата (ГГГГ-ММ-ДД):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.date_entry = tk.Entry(root)
        self.date_entry.insert(0, current_date)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(root, text="Заметки:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.notes_entry = tk.Entry(root)
        self.notes_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Выбор типа нагрузки (Кардио/Силовая)
        self.intensity_var = tk.StringVar(value="Кардио")
        tk.Radiobutton(root, text="Кардио", variable=self.intensity_var, value="Кардио").grid(row=4, column=0,
                                                                                              sticky="e")
        tk.Radiobutton(root, text="Силовая", variable=self.intensity_var, value="Силовая").grid(row=4, column=1,
                                                                                                sticky="w")

        # --- Кнопки и управление ---
        tk.Button(root, text="Добавить тренировку", command=self.add_data, bg="#2196F3", fg="white", width=20).grid(
            row=5, column=0, pady=10, padx=5)

        # Фрейм аналитики (выбор периода и запуск анализа)
        analysis_frame = tk.Frame(root)
        analysis_frame.grid(row=5, column=1, columnspan=5, pady=10, padx=5, sticky="w")

        tk.Button(analysis_frame, text="Показать анализ", command=self.run_analysis, width=20).pack(side=tk.LEFT)

        tk.Label(analysis_frame, text=" Месяц:").pack(side=tk.LEFT)
        self.month_entry = tk.Entry(analysis_frame, width=5)
        self.month_entry.insert(0, str(datetime.now().month))
        self.month_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(analysis_frame, text="Год:").pack(side=tk.LEFT)
        self.year_entry = tk.Entry(analysis_frame, width=7)
        self.year_entry.insert(0, str(datetime.now().year))
        self.year_entry.pack(side=tk.LEFT, padx=5)

        # --- Настройка таблицы результатов (Treeview) ---
        columns = ("value", "activity", "date", "notes", "intensity")
        self.tree = ttk.Treeview(root, columns=columns, show='headings')

        self.tree.heading("value", text="Мин.")
        self.tree.heading("activity", text="Вид спорта")
        self.tree.heading("date", text="Дата")
        self.tree.heading("notes", text="Заметки")
        self.tree.heading("intensity", text="Тип")

        self.tree.column("value", width=70)
        self.tree.column("activity", width=150)
        self.tree.column("notes", width=300)

        self.tree.grid(row=6, column=0, columnspan=6, padx=10, pady=10, sticky="nsew")

        # Настройка растягивания таблицы
        root.grid_rowconfigure(6, weight=1)
        root.grid_columnconfigure(1, weight=1)

        self.refresh_table()

    def run_analysis(self):
        """Получает параметры периода, вызывает генерацию отчета и строит график."""
        try:
            m = int(self.month_entry.get())
            y = int(self.year_entry.get())
            report_text, filtered_df = get_workout_report(y, m)
            messagebox.showinfo(f"Анализ тренировок за {m:02d}.{y}", report_text)
            if filtered_df is not None:
                show_workout_chart(filtered_df)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные месяц и год")

    def add_data(self):
        """
        Собирает данные из полей ввода, выполняет валидацию и очистку через регулярные выражения.
        При успехе сохраняет тренировку в файл и обновляет таблицу.
        """
        raw_val = self.value_entry.get()

        # 1. Валидация числового ввода (re)
        if not validate_duration_format(raw_val):
            messagebox.showerror("Ошибка", "Введите корректную длительность (число)")
            return

        # 2. Очистка текстовых строк (re)
        activity = clean_text(self.activity_entry.get())
        notes = clean_text(self.notes_entry.get())

        if not activity:
            messagebox.showerror("Ошибка", "Поле 'Вид спорта' не может быть пустым")
            return

        try:
            # Создание объекта модели и сохранение в хранилище
            w = Workout(
                value=float(raw_val.replace(',', '.')),
                activity=activity,
                date=self.date_entry.get(),
                notes=notes,
                intensity=self.intensity_var.get()
            )
            save_workout([w])
            self.refresh_table()

            # Очистка полей ввода после успешного сохранения
            self.value_entry.delete(0, tk.END)
            self.activity_entry.delete(0, tk.END)
            self.notes_entry.delete(0, tk.END)

            messagebox.showinfo("Успех", "Тренировка добавлена!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")

    def refresh_table(self):
        """Загружает актуальные данные из CSV и перерисовывает содержимое таблицы."""
        for i in self.tree.get_children():
            self.tree.delete(i)
        for w in load_workouts():
            self.tree.insert("", "end", values=(
                w['value'],
                w['activity'],
                w['date'],
                w['notes'],
                w['intensity']
            ))