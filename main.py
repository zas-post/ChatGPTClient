import sys
import requests
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QComboBox,
    QStyleFactory,
)
from PyQt5.QtGui import QIcon


class ChatApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Секция 1: Поле для ввода API Token
        self.api_token_label = QLabel("API Token")
        self.api_token_input = QLineEdit()
        self.api_token_input.setPlaceholderText("Введите свой токен")
        layout.addWidget(self.api_token_label)
        layout.addWidget(self.api_token_input)

        # Секция 2: Поле для ввода запроса
        self.prompt_label = QLabel("Введите свой запрос")
        self.prompt_input = QLineEdit()
        self.prompt_input.setPlaceholderText("Введите запрос к нейросети")
        layout.addWidget(self.prompt_label)
        layout.addWidget(self.prompt_input)

        # Секция 3: Выпадающий список для выбора модели
        self.model_selector = QComboBox()
        self.model_selector.addItem("GPT-3.5 Turbo", "openai/gpt-3.5-turbo")
        self.model_selector.addItem("GPT-4o", "openai/gpt-4o")
        self.model_selector.addItem(
            "Hermes 3 405B Instruct (free)", "nousresearch/hermes-3-llama-3.1-405b:free"
        )
        layout.addWidget(QLabel("Выберите модель"))
        layout.addWidget(self.model_selector)

        # Кнопка для отправки запроса
        self.send_button = QPushButton("Отправить запрос")
        self.send_button.clicked.connect(self.send_request)
        layout.addWidget(self.send_button)

        # Кнопка для очистки
        self.clear_button = QPushButton("Очистить")
        self.clear_button.clicked.connect(self.clear_fields)
        layout.addWidget(self.clear_button)

        # Поле для отображения результатов
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)

        self.setLayout(layout)
        self.setWindowTitle("ChatGPT Client")
        self.setWindowIcon(QIcon("fav_logo.webp"))
        self.resize(400, 400)

    def send_request(self):
        # Получение данных от пользователя
        api_key = self.api_token_input.text()
        prompt = self.prompt_input.text()
        model = self.model_selector.currentData()

        # URL запроса
        url = "https://openrouter.ai/api/v1/chat/completions"

        # Данные для отправки
        data = {"model": model, "prompt": prompt, "max_tokens": 100}

        # Заголовки запроса
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        try:
            # Отправка запроса
            response = requests.post(url, json=data, headers=headers)

            # Обработка ответа
            if response.status_code == 200:
                result = response.json()
                generated_text = result["choices"][0]["text"]
                self.result_display.setPlainText(
                    "Сгенерированный текст:\n" + generated_text
                )
            else:
                self.result_display.setPlainText(
                    f"Ошибка: {response.status_code}\n{response.text}"
                )
        except requests.exceptions.RequestException as e:
            self.result_display.setPlainText(f"Произошла ошибка при запросе: {e}")

    def clear_fields(self):
        self.prompt_input.clear()
        self.result_display.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ex = ChatApp()
    ex.show()
    sys.exit(app.exec_())
