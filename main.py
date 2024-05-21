#!usr/bin/python3


if __name__ == "__main__":
    import sys
    from simple_spreadsheet_converter import SimpleGlossaryConverter, ConverterGUI
    from PyQt5 import QtWidgets

    app = QtWidgets.QApplication([])
    widget = ConverterGUI.ConverterGUI()
    widget.show()

    sys.exit(app.exec())
