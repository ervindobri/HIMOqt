from PyQt6.QtWidgets import QMessageBox


class CustomDialog:

    @staticmethod
    def message(title, text, info):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setInformativeText(info)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setStandardButtons(QMessageBox.StandardButtons.Ok)
        msg.exec()
