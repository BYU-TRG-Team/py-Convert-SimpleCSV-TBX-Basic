import sys
from os import path
from PyQt5 import QtCore, QtWidgets, QtGui
import langcodes


class ConverterGUI(QtWidgets.QWidget):
    """Provides a Qt GUI for the simple glossary converter."""

    CODES = langcodes.LANGUAGE_ALPHA3.keys()


    class LogStream(QtCore.QObject):
        """An output stream to replace <stdout>."""

        text_written = QtCore.pyqtSignal(str)

        def write(self, text):
            self.text_written.emit(str(text))

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSV to TBX-Basic Converter")
        self.resize(400, 500)

        self.src_lang_label = QtWidgets.QLabel("Source lang code: ")
        self.src_lang_combo_box = QtWidgets.QComboBox()
        self.src_lang_combo_box.resize(30, 25)
        self.src_lang_combo_box.addItems(self.CODES)
        self.src_lang_combo_box.setCurrentText(langcodes.DEFAULT_LANGUAGE)
        # maybe add a button to search for a lang code based on lang name?
        # self.src_lang_search_btn = QtWidgets.QPushButton()

        self.input_files_dir_path_label = QtWidgets.QLabel("Input CSV files directory path: ")
        self.input_files_dir_path_input = QtWidgets.QLineEdit()
        self.input_files_dir_path_input.textChanged.connect(self._validate_form)
        self.input_files_dir_path_browse_btn = QtWidgets.QPushButton("Browse...")
        self.input_files_dir_path_browse_btn.clicked.connect(self._input_files_dir_path_browse_btn_on_click)

        self.output_file_path_label = QtWidgets.QLabel("Output XML file path: ")
        self.output_file_path_input = QtWidgets.QLineEdit()
        self.output_file_path_input.textChanged.connect(self._validate_form)
        self.output_file_path_browse_btn = QtWidgets.QPushButton("Browse...")
        self.output_file_path_browse_btn.clicked.connect(self._output_file_path_browse_btn_on_click)

        self.fields_layout = QtWidgets.QGridLayout()
        self.fields_layout.addWidget(self.src_lang_label, 0, 0)
        self.fields_layout.addWidget(self.src_lang_combo_box, 0, 1)
        self.fields_layout.addItem(QtWidgets.QSpacerItem(0, 15), 1, 0)
        self.fields_layout.addWidget(self.input_files_dir_path_label, 2, 0)
        self.fields_layout.addWidget(self.input_files_dir_path_input, 3, 0)
        self.fields_layout.addWidget(self.input_files_dir_path_browse_btn, 3, 1)
        self.fields_layout.addWidget(self.output_file_path_label, 4, 0)
        self.fields_layout.addWidget(self.output_file_path_input, 5, 0)
        self.fields_layout.addWidget(self.output_file_path_browse_btn, 5, 1)

        self.log_label = QtWidgets.QLabel("Conversion log:")
        self.log_box = QtWidgets.QTextEdit()
        self.log_box.height = 200
        self.convert_btn = QtWidgets.QPushButton("Convert")
        self.convert_btn.clicked.connect(self._convert_btn_on_click)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addLayout(self.fields_layout)
        self.main_layout.addSpacerItem(QtWidgets.QSpacerItem(0, 25))
        self.main_layout.addWidget(self.log_label)
        self.main_layout.addWidget(self.log_box)
        self.main_layout.addSpacerItem(QtWidgets.QSpacerItem(0, 25))
        self.main_layout.addWidget(self.convert_btn)

        self._validate_form()

        sys.stdout = self.LogStream(text_written=self._write_to_log_box)

    def closeEvent(self, event):
        sys.stdout = sys.__stdout__
        super().closeEvent(event)

    def _write_to_log_box(self, text):
        log_box_cursor = self.log_box.textCursor()
        log_box_cursor.movePosition(QtGui.QTextCursor.End)
        log_box_cursor.insertText(text)
        self.log_box.setTextCursor(log_box_cursor)
        self.log_box.ensureCursorVisible()

    def _validate_form(self):
        if not path.exists(self.input_files_dir_path_input.text()):
            self.convert_btn.setEnabled(False)
            return

        if not path.exists(path.dirname(self.output_file_path_input.text())):
            self.convert_btn.setEnabled(False)
            return

        self.convert_btn.setEnabled(True)

    def _input_files_dir_path_browse_btn_on_click(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                            caption="Select directory",
                                                            directory=path.expanduser('~'))
        if folder != '':
            self.input_files_dir_path_input.setText(folder)

    def _output_file_path_browse_btn_on_click(self):
        file_dialog = QtWidgets.QFileDialog(self,
                                            caption="Select output file location:",
                                            directory=path.expanduser('~'),
                                            filter="XML Files|.xml")
        file = file_dialog.getSaveFileName(self)
        if len(file) != 0:
            self.output_file_path_input.setText(file[0])

    def _convert_btn_on_click(self):
        from .SimpleGlossaryConverter import SimpleGlossaryConverter
        from os import listdir

        input_dir = self.input_files_dir_path_input.text()
        files = [path.join(input_dir, f) for f in listdir(input_dir)]

        output_dir = self.output_file_path_input.text()

        converter = SimpleGlossaryConverter(self.src_lang_combo_box.currentText())
        converter.convert(output_dir, *files)
        print(f"Successfully converted to: '{path.basename(output_dir)}'")
