from PyQt5.QtWidgets import QLabel, QComboBox, QDialog, QDialogButtonBox, QVBoxLayout


class Custom_Dialog(QDialog):
    def __init__(self, type):
        super().__init__()
        if type == 'update_DB_question':
            self.setWindowTitle("Внимание")

            QBtn = QDialogButtonBox.Yes | QDialogButtonBox.No

            self.button_box = QDialogButtonBox(QBtn)
            self.button_box.accepted.connect(self.accept)
            self.button_box.rejected.connect(self.reject)

            self.layout = QVBoxLayout()
            message = QLabel("Обновить базу данных?")
            self.layout.addWidget(message)
            self.layout.addWidget(self.button_box)
            self.setLayout(self.layout)

        elif type == 'update_DB':
            self.setWindowTitle("Внимание")

            QBtn = QDialogButtonBox.Ok

            self.button_box = QDialogButtonBox(QBtn)
            self.button_box.accepted.connect(self.accept)
            self.button_box.rejected.connect(self.reject)

            self.layout = QVBoxLayout()
            message = QLabel(
                "Выберите для какой платформы обновить данные.\nОставьте пустым, если обновить для всех платформ.")
            self.list_platforms_dlg = QComboBox(self)
            self.list_platforms_dlg.addItems(["", "PS4", "PS5",
                                              "XBOX ONE", "XBOX Series S/X", "Nintendo Switch"])

            self.layout.addWidget(self.list_platforms_dlg)
            self.layout.addWidget(message)
            self.layout.addWidget(self.button_box)
            self.setLayout(self.layout)
        elif type == 'write_to_file_question':
            self.setWindowTitle("Внимание")

            QBtn = QDialogButtonBox.Yes | QDialogButtonBox.No

            self.button_box = QDialogButtonBox(QBtn)
            self.button_box.accepted.connect(self.accept)
            self.button_box.rejected.connect(self.reject)

            self.layout = QVBoxLayout()
            message = QLabel("Записать найденные данные в файл 'out.txt'?")
            self.layout.addWidget(message)
            self.layout.addWidget(self.button_box)
            self.setLayout(self.layout)
