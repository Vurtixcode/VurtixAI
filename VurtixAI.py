import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import time
import random
import json
import numpy as np
import webbrowser
from datetime import datetime, timedelta
import re
import math

class SmoothButton(tk.Canvas):
    def __init__(self, master=None, text="", command=None, 
                 width=120, height=40, corner_radius=12, 
                 bg_color="#1a1a1a", fg_color="#10a37f", 
                 hover_color="#0d8a72", text_color="white", 
                 font=("Segoe UI", 11, "bold"), icon=None, **kwargs):
        super().__init__(master, width=width, height=height, 
                        highlightthickness=0, bg=bg_color, **kwargs)
        
        self.command = command
        self.corner_radius = corner_radius
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = font
        self.text = text
        self.width = width
        self.height = height
        self.icon = icon
        self.is_hovered = False
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.bind("<ButtonRelease-1>", self.on_release)
        
        self.draw_button()
    
    def draw_button(self, color=None):
        """Отрисовка кнопки с закругленными углами"""
        if color is None:
            color = self.hover_color if self.is_hovered else self.fg_color
        
        self.delete("all")
        
        # Рисуем закругленный прямоугольник с тенью
        self.create_rounded_rect(2, 2, self.width-2, self.height-2, 
                               self.corner_radius, fill=color, outline="")
        
        # Добавляем текст
        self.create_text(self.width//2, self.height//2, 
                        text=self.text, fill=self.text_color, 
                        font=self.font, anchor="center")
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius=12, **kwargs):
        """Создание прямоугольника с закругленными углами"""
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def on_enter(self, event):
        """Анимация при наведении"""
        self.is_hovered = True
        self.animate_color(self.fg_color, self.hover_color)
    
    def on_leave(self, event):
        """Анимация при уходе курсора"""
        self.is_hovered = False
        self.animate_color(self.hover_color, self.fg_color)
    
    def on_click(self, event):
        """Анимация клика"""
        self.animate_click()
        if self.command:
            self.after(150, self.command)
    
    def on_release(self, event):
        """Возврат после клика"""
        color = self.hover_color if self.is_hovered else self.fg_color
        self.draw_button(color)
    
    def animate_color(self, from_color, to_color):
        """Плавная анимация изменения цвета"""
        steps = 8
        delay = 20
        
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        def rgb_to_hex(rgb):
            return '#{:02x}{:02x}{:02x}'.format(*rgb)
        
        start_rgb = hex_to_rgb(from_color)
        end_rgb = hex_to_rgb(to_color)
        
        for step in range(steps + 1):
            ratio = step / steps
            current_rgb = [
                int(start_rgb[i] + (end_rgb[i] - start_rgb[i]) * ratio)
                for i in range(3)
            ]
            current_color = rgb_to_hex(tuple(current_rgb))
            
            def update_color(color=current_color):
                self.draw_button(color)
            
            self.after(step * delay, update_color)
    
    def animate_click(self):
        """Анимация нажатия кнопки"""
        darker_color = self.darken_color(self.hover_color if self.is_hovered else self.fg_color, 0.7)
        self.draw_button(darker_color)
        
        def reset_color():
            color = self.hover_color if self.is_hovered else self.fg_color
            self.draw_button(color)
        
        self.after(120, reset_color)
    
    def darken_color(self, hex_color, factor=0.7):
        """Затемнение цвета"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darker_rgb = tuple(int(c * factor) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*darker_rgb)

class TypeWriter:
    """Класс для анимации печати текста"""
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.current_text = ""
        self.is_typing = False
        
    def type_text(self, text, delay=0.03):
        """Анимированная печать текста"""
        self.is_typing = True
        self.text_widget.delete(1.0, tk.END)
        self.current_text = ""
        
        def type_char(i=0):
            if i < len(text) and self.is_typing:
                self.current_text += text[i]
                self.text_widget.delete(1.0, tk.END)
                self.text_widget.insert(tk.END, self.current_text)
                self.text_widget.see(tk.END)
                self.text_widget.after(int(delay * 1000), type_char, i + 1)
            else:
                self.is_typing = False
                
        type_char()
    
    def stop_typing(self):
        """Остановка анимации печати"""
        self.is_typing = False

class AISelfLearner:
    def __init__(self):
        self.knowledge_base = {}
        self.learning_progress = 0
        self.total_capacity = 1000
        self.is_learning = False
        self.learning_thread = None
        self.last_learn_time = datetime.now()
        self.learning_topics = [
            "Python Syntax", "Data Structures", "Algorithms", "Machine Learning",
            "Web Development", "GUI Programming", "Data Analysis", "OOP Concepts",
            "Error Handling", "Optimization", "Async Programming", "Design Patterns"
        ]
        
    def auto_learn(self):
        """Автоматическое обучение каждые 10 секунд"""
        self.is_learning = True
        
        def learning_loop():
            while self.is_learning:
                try:
                    # Ждем 10 секунд между обучениями
                    time.sleep(10)
                    
                    if self.is_learning:
                        self.learn_new_concept()
                        self.learning_progress += 1
                        
                except Exception as e:
                    print(f"Ошибка автообучения: {e}")
        
        self.learning_thread = threading.Thread(target=learning_loop, daemon=True)
        self.learning_thread.start()
    
    def learn_new_concept(self):
        """Изучение нового концепта"""
        topic = random.choice(self.learning_topics)
        concepts = {
            "Python Syntax": ["Variables", "Functions", "Loops", "Conditionals"],
            "Data Structures": ["Lists", "Dictionaries", "Tuples", "Sets"],
            "Algorithms": ["Sorting", "Searching", "Recursion", "Dynamic Programming"]
        }
        
        concept = random.choice(concepts.get(topic, ["Programming Concept"]))
        self.last_learn_time = datetime.now()
        
        return f"Изучено: {concept} в {topic}"
    
    def stop_learning(self):
        """Остановка обучения"""
        self.is_learning = False

class ChatGPTStyleAI:
    def __init__(self):
        self.code_templates = {
            'factorial': self._factorial_template,
            'calculator': self._calculator_template,
            'sorting': self._sorting_template,
            'web': self._web_template,
            'gui': self._gui_template
        }
        
    def _sorting_template(self):
        return '''def bubble_sort(arr):
    """
    Сортировка пузырьком с оптимизацией.
    
    Args:
        arr (list): Список для сортировки
        
    Returns:
        list: Отсортированный список
    """
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

def quick_sort(arr):
    """
    Быстрая сортировка (QuickSort).
    
    Args:
        arr (list): Список для сортировки
        
    Returns:
        list: Отсортированный список
    """
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# Пример использования
if __name__ == "__main__":
    numbers = [64, 34, 25, 12, 22, 11, 90]
    print(f"Исходный список: {numbers}")
    print(f"Сортировка пузырьком: {bubble_sort(numbers.copy())}")
    print(f"Быстрая сортировка: {quick_sort(numbers.copy())}")'''
    
    def _web_template(self):
        return '''import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_website(url):
    """
    Простой веб-скрепинг с обработкой ошибок.
    
    Args:
        url (str): URL веб-страницы
        
    Returns:
        dict: Данные со страницы
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Извлечение данных
        title = soup.find('title').get_text() if soup.find('title') else 'No title'
        paragraphs = [p.get_text() for p in soup.find_all('p')][:5]
        
        return {
            'title': title,
            'paragraphs': paragraphs,
            'status_code': response.status_code
        }
        
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None

# Пример использования
if __name__ == "__main__":
    data = scrape_website('https://example.com')
    if data:
        print(f"Заголовок: {data['title']}")
        print("Первые параграфы:")
        for i, p in enumerate(data['paragraphs'], 1):
            print(f"{i}. {p}")'''
    
    def _gui_template(self):
        return '''import tkinter as tk
from tkinter import ttk

class GUIApp:
    """
    Простое GUI приложение на tkinter.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Мое приложение")
        self.root.geometry("400x300")
        
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="Добро пожаловать!", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Поле ввода
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(input_frame, text="Введите текст:").pack(side=tk.LEFT)
        self.entry_var = tk.StringVar()
        entry = ttk.Entry(input_frame, textvariable=self.entry_var, width=30)
        entry.pack(side=tk.LEFT, padx=10)
        
        # Кнопки
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="ОК", command=self.on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Отмена", command=self.on_cancel).pack(side=tk.LEFT, padx=5)
        
        # Текстовое поле
        self.text_area = tk.Text(main_frame, height=8, width=40)
        self.text_area.pack(fill=tk.BOTH, expand=True)
    
    def on_ok(self):
        """Обработчик кнопки OK"""
        text = self.entry_var.get()
        if text:
            self.text_area.insert(tk.END, f"{text}\\n")
            self.entry_var.set("")
    
    def on_cancel(self):
        """Обработчик кнопки Отмена"""
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()'''
    
    def _factorial_template(self):
        return '''def factorial(n: int) -> int:
    """
    Вычисляет факториал числа с обработкой ошибок.
    
    Args:
        n (int): Неотрицательное целое число
        
    Returns:
        int: Факториал числа n
        
    Raises:
        TypeError: Если n не целое число
        ValueError: Если n отрицательное
    """
    if not isinstance(n, int):
        raise TypeError("Факториал определён только для целых чисел")
    
    if n < 0:
        raise ValueError("Факториал не определён для отрицательных чисел")
    
    if n == 0:
        return 1
    
    result = 1
    for i in range(1, n + 1):
        result *= i
    
    return result

# Пример использования
if __name__ == "__main__":
    try:
        print(f"Факториал 5: {factorial(5)}")  # 120
        print(f"Факториал 0: {factorial(0)}")  # 1
    except (TypeError, ValueError) as e:
        print(f"Ошибка: {e}")'''
    
    def _calculator_template(self):
        return '''class Calculator:
    """
    Простой калькулятор с базовыми операциями.
    Поддерживает сложение, вычитание, умножение, деление.
    """
    
    def __init__(self):
        self.history = []
    
    def add(self, a: float, b: float) -> float:
        """Сложение двух чисел"""
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def subtract(self, a: float, b: float) -> float:
        """Вычитание двух чисел"""
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result
    
    def multiply(self, a: float, b: float) -> float:
        """Умножение двух чисел"""
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result
    
    def divide(self, a: float, b: float) -> float:
        """Деление двух чисел"""
        if b == 0:
            raise ValueError("Деление на ноль невозможно")
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result
    
    def get_history(self) -> list:
        """Возвращает историю операций"""
        return self.history

# Пример использования
if __name__ == "__main__":
    calc = Calculator()
    print(f"Сложение: {calc.add(10, 5)}")
    print(f"Умножение: {calc.multiply(4, 3)}")
    print("История:", calc.get_history())'''
    
    def _general_template(self, prompt):
        return f'''# Решение для: {prompt}
# Сгенерировано AI с стиле ChatGPT/DeepSeek

def solution():
    """
    Основная функция решения задачи.
    """
    # TODO: Реализовать логику based on requirements
    print("Функция решения задачи")
    
    # Пример сложной логики
    data = prepare_data()
    result = process_data(data)
    return result

def prepare_data():
    """
    Подготовка данных для обработки.
    """
    return {{"sample": "data"}}

def process_data(data):
    """
    Обработка данных с проверкой ошибок.
    """
    try:
        # Логика обработки
        return "Обработанные данные"
    except Exception as e:
        print(f"Ошибка обработки: {{e}}")
        return None

if __name__ == "__main__":
    # Запуск решения
    result = solution()
    print(f"Результат: {{result}}")'''
    
    def generate_code(self, prompt, deep_think=False):
        """Генерация кода в стиле ChatGPT"""
        if deep_think:
            time.sleep(2.5)  # DeepThink задержка
            
        prompt_lower = prompt.lower()
        
        # Определяем тип запроса
        if any(word in prompt_lower for word in ['factorial', 'факториал']):
            return self._factorial_template()
        elif any(word in prompt_lower for word in ['calculator', 'calc', 'калькулятор']):
            return self._calculator_template()
        elif any(word in prompt_lower for word in ['sort', 'сортиров']):
            return self._sorting_template()
        elif any(word in prompt_lower for word in ['web', 'scraping', 'парсинг']):
            return self._web_template()
        elif any(word in prompt_lower for word in ['gui', 'interface', 'интерфейс']):
            return self._gui_template()
        else:
            return self._general_template(prompt)

class DeepSeekAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DeepSeek AI Assistant")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0d1117')
        
        # Стиль ChatGPT/DeepSeek
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#0d1117')
        self.style.configure('TLabel', background='#0d1117', foreground='white')
        self.style.configure('TEntry', fieldbackground='#161b22', foreground='white')
        self.style.configure('TCombobox', fieldbackground='#161b22', foreground='white')
        
        self.ai = ChatGPTStyleAI()
        self.learner = AISelfLearner()
        self.typewriter = None
        
        self.setup_ui()
        self.learner.auto_learn()  # Автообучение при запуске
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header с стилем DeepSeek
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(header_frame, text="🧠 DeepSeek AI Assistant", 
                              font=('Segoe UI', 24, 'bold'), 
                              bg='#0d1117', fg='#10a37f')
        title_label.pack(side=tk.LEFT)
        
        # Статус обучения
        self.learning_status = tk.StringVar(value="🔄 Автообучение: 0/1000")
        status_label = tk.Label(header_frame, textvariable=self.learning_status,
                               font=('Segoe UI', 10), bg='#0d1117', fg='#8b949e')
        status_label.pack(side=tk.RIGHT)
        
        # Input area
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(input_frame, text="Введите запрос:", 
                font=('Segoe UI', 11), bg='#0d1117', fg='white').pack(anchor=tk.W)
        
        input_container = tk.Frame(input_frame, bg='#161b22', relief=tk.FLAT, bd=1)
        input_container.pack(fill=tk.X, pady=5)
        
        self.prompt_var = tk.StringVar()
        self.prompt_entry = tk.Entry(input_container, textvariable=self.prompt_var, 
                                    font=('Segoe UI', 11), bg='#161b22', fg='white',
                                    relief=tk.FLAT, bd=0, insertbackground='white')
        self.prompt_entry.pack(fill=tk.X, padx=10, pady=8)
        self.prompt_entry.bind('<Return>', lambda e: self.generate_code())
        
        # Кнопки действий
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Гладкие кнопки с разными цветами
        buttons = [
            ("🚀 Сгенерировать код", self.generate_code, "#10a37f", "#0d8a72", 180),
            ("🤔 DeepThink", self.deep_think_generate, "#8b5cf6", "#7c3aed", 120),
            ("🌐 Поиск в интернете", self.web_search, "#0ea5e9", "#0284c7", 160),
            ("📊 Статус обучения", self.show_learning_status, "#f59e0b", "#d97706", 140)
        ]
        
        for text, command, color, hover_color, width in buttons:
            btn = SmoothButton(button_frame, text=text, command=command,
                              width=width, height=42, corner_radius=12,
                              fg_color=color, hover_color=hover_color,
                              font=('Segoe UI', 10, 'bold'))
            btn.pack(side=tk.LEFT, padx=5)
        
        # Output area
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tk.Label(output_frame, text="Сгенерированный код:", 
                font=('Segoe UI', 11, 'bold'), bg='#0d1117', fg='white').pack(anchor=tk.W)
        
        # Текстовое поле с стилем code editor
        self.code_text = scrolledtext.ScrolledText(output_frame, height=20,
                                                  bg='#161b22', fg='#e6edf3',
                                                  font=('Cascadia Code', 10),
                                                  relief=tk.FLAT, bd=0,
                                                  insertbackground='#e6edf3')
        self.code_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.typewriter = TypeWriter(self.code_text)
        
        # Статус бар
        status_bar = tk.Frame(main_frame, bg='#161b22', height=30)
        status_bar.pack(fill=tk.X, pady=(10, 0))
        status_bar.pack_propagate(False)
        
        self.status_var = tk.StringVar(value="Готов к работе | DeepSeek AI v1.0")
        status_label = tk.Label(status_bar, textvariable=self.status_var,
                               bg='#161b22', fg='#8b949e', font=('Segoe UI', 9))
        status_label.pack(side=tk.LEFT, padx=10)
        
        # Обновление статуса обучения
        self.update_learning_status()
    
    def update_learning_status(self):
        """Обновление статуса обучения"""
        if self.learner.is_learning:
            self.learning_status.set(f"🔄 Автообучение: {self.learner.learning_progress}/1000")
            self.root.after(5000, self.update_learning_status)  # Обновлять каждые 5 сек
    
    def generate_code(self):
        """Генерация кода"""
        prompt = self.prompt_var.get()
        if not prompt:
            messagebox.showwarning("Внимание", "Пожалуйста, введите запрос!")
            return
        
        self.status_var.set("🤖 Генерирую код...")
        thread = threading.Thread(target=self._generate_thread, args=(prompt, False))
        thread.daemon = True
        thread.start()
    
    def deep_think_generate(self):
        """Генерация с DeepThink"""
        prompt = self.prompt_var.get()
        if not prompt:
            messagebox.showwarning("Внимание", "Пожалуйста, введите запрос!")
            return
        
        self.status_var.set("🤔 DeepThink - обдумываю...")
        thread = threading.Thread(target=self._generate_thread, args=(prompt, True))
        thread.daemon = True
        thread.start()
    
    def _generate_thread(self, prompt, deep_think):
        """Поток генерации кода"""
        try:
            code = self.ai.generate_code(prompt, deep_think)
            
            self.root.after(0, lambda: self.typewriter.type_text(code, 0.03))
            self.root.after(0, lambda: self.status_var.set("✅ Код сгенерирован!"))
            
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"❌ Ошибка: {str(e)}"))
    
    def web_search(self):
        """Поиск в интернете"""
        prompt = self.prompt_var.get()
        if not prompt:
            messagebox.showwarning("Внимание", "Пожалуйста, введите запрос для поиска!")
            return
        
        search_query = f"python programming {prompt}"
        search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
        webbrowser.open(search_url)
        self.status_var.set("🌐 Открываю поиск в браузере...")
    
    def show_learning_status(self):
        """Показать статус обучения"""
        status = f"""
📊 Статус обучения DeepSeek AI:

• Прогресс обучения: {self.learner.learning_progress}/1000
• Автообучение: {'🟢 Включено' if self.learner.is_learning else '🔴 Выключено'}
• Последнее обновление: {self.learner.last_learn_time.strftime('%H:%M:%S')}
• Изучено концептов: {self.learner.learning_progress}

AI автоматически обучается каждые 10 секунд!
        """
        messagebox.showinfo("Статус обучения", status)

def main():
    """Запуск приложения"""
    print("🚀 Запуск DeepSeek AI Assistant...")
    print("Стиль: ChatGPT/DeepSeek")
    print("Функции: Автообучение, DeepThink, Поиск")
    time.sleep(1)
    
    root = tk.Tk()
    app = DeepSeekAIApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()