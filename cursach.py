import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.config import Config

Config.set("kivy", "keyboard_mode", "systemanddock") #экранная клавиатура

Window.size = (720, 1612)


def get_random_line_number(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        return random.randint(0, len(lines) - 1)  # Возвращаем случайный индекс


def get_line_from_file(filename, line_number):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        return lines[line_number].strip()  # Получаем строку по индексу


class NumericTextInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        # Разрешаем ввод только цифр
        if substring.isdigit() or substring == '':
            super().insert_text(substring, from_undo=from_undo)


class MyApp(App):
    def build(self):
        # Создаем BoxLayout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Поле для ввода текста (только цифры)
        self.text_input = NumericTextInput(hint_text='Введите ваш ответ здесь', multiline=False, size_hint_y=None,
                                           height=40)
        layout.add_widget(self.text_input)

        # Создаем ScrollView для прокрутки текста
        scroll_view = ScrollView(size_hint=(1, 0.6))  # Задаем высоту 60%
        self.label = Label(text='Здесь будет текст', size_hint_y=None, font_size='24sp', halign='center')
        self.label.bind(size=self._update_label_text_size)  # Обновление размера текста
        self.label.bind(texture_size=self.label.setter('size'))  # Автоматически изменяем размер Label по тексту
        scroll_view.add_widget(self.label)  # Добавляем Label в ScrollView
        layout.add_widget(scroll_view)

        # Метка для отображения результата
        self.result_label = Label(text='', size_hint_y=None, height=40)
        layout.add_widget(self.result_label)

        # Кнопка снизу
        button = Button(text='Показать ответ', size_hint_y=None, height=80)  # Увеличиваем высоту кнопки
        button.bind(on_press=self.on_button_press)  # Привязываем нажатие кнопки к методу
        layout.add_widget(button)

        # Инициализация переменных
        self.random_line_number = get_random_line_number('file1.txt')
        self.line_from_file1 = get_line_from_file('file1.txt', self.random_line_number)
        self.label.text = self.line_from_file1
        self.second_line_shown = False
        self.file2_line = None

        return layout

    def _update_label_text_size(self, instance, value):
        # Центрируем текст в Label
        self.label.text_size = (value[0], None)
        self.label.center_x = instance.center_x

    def on_button_press(self, instance):
        file2 = 'file2.txt'

        if not self.second_line_shown:
            # Получаем строку из второго файла с тем же индексом
            self.file2_line = get_line_from_file(file2, self.random_line_number)
            self.second_line_shown = True

            # Проверяем ответ пользователя
            self.check_answer()
        else:
            # Обновляем текст из первого файла
            self.random_line_number = get_random_line_number('file1.txt')
            self.line_from_file1 = get_line_from_file('file1.txt', self.random_line_number)
            self.label.text = self.line_from_file1
            self.second_line_shown = False  # Сбрасываем флаг для следующего показа строки из второго файла

            # Очищаем поле ввода
            self.text_input.text = ''
            # Очищаем текст о правильности ответа
            self.result_label.text = ''

    def check_answer(self):
        # Проверяем, что поле ввода не пустое
        if self.text_input.text:
            answer = int(self.text_input.text)  # Преобразуем текст в число
            # Предполагаем, что self.file2_line содержит правильный ответ
            correct_answer = int(self.file2_line)  # Преобразуем строку в число

            # Выводим результат проверки
            if answer == correct_answer:
                self.result_label.text = 'Правильно!'
                self.result_label.color = (0, 1, 0, 1)  # green
            else:
                self.result_label.text = f'Неправильно! Правильный ответ: {correct_answer}'
                self.result_label.color = (1, 0, 0, 1)  # red



if __name__ == '__main__':
    MyApp().run()
