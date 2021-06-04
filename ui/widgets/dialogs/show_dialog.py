from PyQt6.QtWidgets import QMessageBox


class CustomDialog:

    @staticmethod
    def message(title="Title", text="Text", info="Info"):
        msg = QMessageBox()
        msg.setStyleSheet("background-color: #fefefe;")
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setInformativeText(info)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    @staticmethod
    def warningMessage(text="Text", info="Info"):
        msg = QMessageBox()
        msg.setStyleSheet("background-color: #fefefe;")
        msg.setWindowTitle("Warning")
        msg.setText(text)
        msg.setInformativeText(info)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
