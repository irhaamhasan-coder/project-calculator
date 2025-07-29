from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
import math

class CalculatorLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.expression = ""
        self.memory = []  # Memory list

        self.history = []
        self.history_visible = False

        self.main_layout = BoxLayout(orientation='vertical')
     
        self.display = TextInput(
            text="0",
            readonly=True,
            halign="right",
            font_size=48,
            size_hint_y=0.2
        )
        self.display.bind(on_touch_down=self.hide_history)
        self.main_layout.add_widget(self.display)

        self.toggle_history_btn = Button(
            text='⏳',
            size_hint_y=None,
            height=40,
        )
        self.toggle_history_btn.bind(on_press=self.toggle_history)
        self.main_layout.add_widget(self.toggle_history_btn)

       
        self.history_panel = ScrollView(size_hint=(1, 0.6))
        self.history_box = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.history_box.bind(minimum_height=self.history_box.setter('height'))
        self.history_panel.add_widget(self.history_box)

        Window.bind(size=self.on_window_resize)

        self.button_grid = GridLayout(cols=4, spacing=6, padding=10, size_hint_y=0.8)

        buttons = [
            ('MS', self.memory_store), ('MR', self.memory_recall), ('MC', self.memory_clear), ('Mv', self.memory_view),
            ('M+', self.memory_add), ('M-', self.memory_subtract), ('1/x', self.reciprocal), ('%', self.percent),
            ('x²', self.square), ('√x', self.square_root), ('CE', self.clear_entry), ('C', self.clear_all),
            ('7', self.add_char), ('8', self.add_char), ('9', self.add_char), ('÷', self.add_operator),
            ('4', self.add_char), ('5', self.add_char), ('6', self.add_char), ('×', self.add_operator),
            ('1', self.add_char), ('2', self.add_char), ('3', self.add_char), ('−', self.add_operator),
            ('±', self.negate), ('0', self.add_char), ('.', self.add_char), ('+', self.add_operator),
            ('⌫', self.backspace), ('=', self.evaluate)
        ]

        for label, callback in buttons:
            btn = Button(text=label, font_size=22)
            btn.bind(on_press=callback)
            self.button_grid.add_widget(btn)

        self.main_layout.add_widget(self.button_grid)
        self.add_widget(self.main_layout)

    
    def on_window_resize(self, window, size):
        width, height = size

        if self.history_panel.parent:
            self.main_layout.remove_widget(self.history_panel)
        if self.button_grid.parent:
            self.main_layout.remove_widget(self.button_grid)

        if width >= 800:
            # Side-by-side view
            container = BoxLayout(orientation='horizontal', size_hint_y=0.8)
            container.add_widget(self.button_grid)
            container.add_widget(self.history_panel)
            self.main_layout.add_widget(container)
        else:
            # Toggle-based view
            if self.history_visible:
                self.main_layout.add_widget(self.history_panel)
            else:
                self.main_layout.add_widget(self.button_grid)

    
    def toggle_history(self, instance):
        self.history_visible = not self.history_visible
        self.on_window_resize(Window, Window.size)

    def update_history_panel(self):
        self.history_box.clear_widgets()
        for expr, result in reversed(self.history[-20:]):
            btn = Button(
                text=f"{expr} = {result}",
                size_hint_y=None,
                height=40
            )
            btn.bind(on_press=lambda btn: self.load_history_entry(btn.text))
            self.history_box.add_widget(btn)
        
    def load_history_entry(self, entry):
        try:
            expr, result = entry.split(" = ")
            self.expression = expr
            self.update_display()
            self.toggle_history(None)
        except:
            pass

    def hide_history(self, instance, touch):
        if self.history_visible and self.display.collide_point(*touch.pos):
            self.toggle_history(None)

    def update_display(self):
        self.display.text = self.expression if self.expression else "0"

    def add_char(self, instance):
        char = instance.text
        if self.display.text == "0" or self.expression.endswith("="):
            self.expression = ""
        self.expression += char
        self.update_display()

    def add_operator(self, instance):
        op = instance.text
        if op == '×': op = '*'
        elif op == '÷': op = '/'
        elif op == '−': op = '-'
        elif op == '+': op = '+'
        if self.expression and self.expression[-1] in "+−*/":
            self.expression = self.expression[:-1] + op
        else:
            self.expression += op
        self.update_display()

    def clear_entry(self, instance):
        self.expression = ""
        self.update_display()

    def clear_all(self, instance):
        self.expression = ""
        self.update_display()

    def backspace(self, instance):
        self.expression = self.expression[:-1]
        self.update_display()

    def negate(self, instance):
        try:
            if self.expression:
                value = eval(self.expression)
                self.expression = str(-value)
                self.update_display()
        except:
            self.display.text = "Error"

    def evaluate(self, instance):
        try:
            result = str(eval(self.expression))
            self.history.append((self.expression, result))
            self.expression = result
            self.update_display()
            self.toggle_history(None)
        except:
            self.display.text = "Error"
            self.expression = ""


    def square(self, instance):
        try:
            value = eval(self.expression)
            self.expression = str(value ** 2)
            self.update_display()
        except:
            self.display.text = "Error"

    def square_root(self, instance):
        try:
            value = eval(self.expression)
            if value < 0:
                self.display.text = "Error"
            else:
                self.expression = str(math.sqrt(value))
                self.update_display()
        except:
            self.display.text = "Error"

    def reciprocal(self, instance):
        try:
            value = eval(self.expression)
            if value == 0:
                self.display.text = "Error"
            else:
                self.expression = str(1 / value)
                self.update_display()
        except:
            self.display.text = "Error"

    def percent(self, instance):
        try:
            value = eval(self.expression)
            self.expression = str(value / 100)
            self.update_display()
        except:
            self.display.text = "Error"

    # ─── Memory Functionality ────────────────────────

    def memory_store(self, instance):
        try:
            value = eval(self.expression)
            self.memory.append(value)
        except:
            self.display.text = "Error"

    def memory_recall(self, instance):
        if self.memory:
            self.expression = str(self.memory[-1])
            self.update_display()

    def memory_clear(self, instance):
        self.memory.clear()

    def memory_add(self, instance):
        try:
            if self.memory:
                self.memory[-1] += eval(self.expression)
            else:
                self.memory.append(eval(self.expression))
        except:
            self.display.text = "Error"

    def memory_subtract(self, instance):
        try:
            if self.memory:
                self.memory[-1] -= eval(self.expression)
            else:
                self.memory.append(-eval(self.expression))
        except:
            self.display.text = "Error"

    def memory_view(self, instance):
        if self.memory:
            print("Memory values:", self.memory)  # You can later show this on-screen in a ScrollView

class CalculatorApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return CalculatorLayout()

if __name__ == "__main__":
    CalculatorApp().run()
