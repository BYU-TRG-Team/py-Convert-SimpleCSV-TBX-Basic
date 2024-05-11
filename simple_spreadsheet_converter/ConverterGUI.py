from PyQt5 import QtWidgets
import langcodes


class ConverterGUI(QtWidgets.QWidget):
    """Provides a Qt GUI for the simple glossary converter."""

    CODES = langcodes.LANGUAGE_ALPHA3.keys()

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
        self.input_files_dir_path_browse_btn = QtWidgets.QPushButton("Browse...")
        self.input_files_dir_path_browse_btn.clicked.connect(self.output_file_path_browse_btn_on_click)

        self.output_file_path_label = QtWidgets.QLabel("Output XML file path: ")
        self.output_file_path_input = QtWidgets.QLineEdit()
        self.output_file_path_browse_btn = QtWidgets.QPushButton("Browse...")

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

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addLayout(self.fields_layout)
        self.main_layout.addSpacerItem(QtWidgets.QSpacerItem(0, 25))
        self.main_layout.addWidget(self.log_label)
        self.main_layout.addWidget(self.log_box)
        self.main_layout.addSpacerItem(QtWidgets.QSpacerItem(0, 25))
        self.main_layout.addWidget(self.convert_btn)

    def output_file_path_browse_btn_on_click(self):
        from os import path
        file_dialog = QtWidgets.QFileDialog(self, caption="Select output file location:", directory=path.expanduser(), filter="XML Files|.xml")
        file_dialog.getSaveFileName()
