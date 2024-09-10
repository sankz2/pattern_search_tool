import sys
import os
import shutil
import tarfile
import zipfile
from ahocorapy.keywordtree import KeywordTree
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit,
                               QFileDialog, QListWidget, QListWidgetItem, QMessageBox, QGroupBox, QFormLayout)
from PySide6.QtCore import Qt

class FileExtractorErrorDetector(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Extractor and Error Detector")
        self.setGeometry(100, 100, 800, 600)

        self.uploaded_files = []
        self.extracted_folders = []

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Title
        title_label = QLabel("File Extractor and Error Detector")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px;")
        main_layout.addWidget(title_label)

        # Upload Group
        upload_group = QGroupBox("Upload and Extract Files")
        upload_layout = QFormLayout()

        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("Choose file")
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_file)
        extract_button = QPushButton("Upload and Extract")
        extract_button.clicked.connect(self.upload_and_extract)

        self.download_extracted_button = QPushButton("Download Extracted Files")
        self.download_extracted_button.setEnabled(False)
        self.download_extracted_button.clicked.connect(self.download_extracted_files)

        upload_layout.addRow(self.file_input, browse_button)
        upload_layout.addRow(extract_button)
        upload_layout.addRow(self.download_extracted_button)
        upload_group.setLayout(upload_layout)
        main_layout.addWidget(upload_group)

        # Detection Group
        detect_group = QGroupBox("Error Detection")
        detect_layout = QFormLayout()

        self.error_detection_folder_input = QLineEdit()
        self.error_detection_folder_input.setPlaceholderText("Choose error detection folder")
        browse_error_folder_button = QPushButton("Browse")
        browse_error_folder_button.clicked.connect(self.browse_error_detection_folder)
        upload_error_folder_button = QPushButton("Upload for Detection")
        upload_error_folder_button.clicked.connect(self.upload_error_detection_folder)

        self.pattern_input = QLineEdit()
        self.pattern_input.setPlaceholderText("Enter patterns (space-separated)")
        self.pattern_input.returnPressed.connect(self.handle_enter_pressed)

        self.pattern_list = QListWidget()

        pattern_buttons_layout = QHBoxLayout()
        add_presets_button = QPushButton("Add Presets")
        add_presets_button.clicked.connect(self.add_presets)
        delete_pattern_button = QPushButton("Delete Selected Pattern")
        delete_pattern_button.clicked.connect(self.delete_selected_pattern)
        pattern_buttons_layout.addWidget(add_presets_button)
        pattern_buttons_layout.addWidget(delete_pattern_button)

        start_detection_button = QPushButton("Start Detection")
        start_detection_button.clicked.connect(self.start_detection)

        self.download_result_button = QPushButton("Download Result")
        self.download_result_button.setEnabled(False)
        self.download_result_button.clicked.connect(self.download_result)

        detect_layout.addRow(self.error_detection_folder_input, browse_error_folder_button)
        detect_layout.addRow(upload_error_folder_button)
        detect_layout.addRow(self.pattern_input)
        detect_layout.addRow(self.pattern_list)
        detect_layout.addRow(pattern_buttons_layout)
        detect_layout.addRow(start_detection_button)
        detect_layout.addRow(self.download_result_button)
        detect_group.setLayout(detect_layout)
        main_layout.addWidget(detect_group)

        self.setLayout(main_layout)

    def browse_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Choose file", "", "Archives (*.tar.gz *.zip)")
        if file_path:
            self.file_input.setText(file_path)

    def upload_and_extract(self):
        file_path = self.file_input.text()
        if not file_path:
            QMessageBox.warning(self, "Warning", "No file selected")
            return

        filename = os.path.basename(file_path)
        saved_path = os.path.join(os.path.expanduser("~"), 'uploads', filename)
        os.makedirs(os.path.dirname(saved_path), exist_ok=True)
        shutil.copy(file_path, saved_path)
        self.uploaded_files.append(saved_path)

        folder_name = os.path.splitext(filename)[0]
        if folder_name.endswith('.tar'):
            folder_name = os.path.splitext(folder_name)[0]

        extract_folder = os.path.join(os.path.expanduser("~"), 'extracted', folder_name)
        os.makedirs(os.path.dirname(extract_folder), exist_ok=True)

        if os.path.exists(extract_folder):
            shutil.rmtree(extract_folder)

        if saved_path.endswith('.tar.gz'):
            self.extract_tar_gz(saved_path, extract_folder)
        elif saved_path.endswith('.zip'):
            self.extract_zip(saved_path, extract_folder)

        self.extracted_folders.append(extract_folder)
        self.error_detection_folder_input.setText(extract_folder)  # Automatically enter the path
        self.file_input.setText("")
        self.download_extracted_button.setEnabled(True)

        QMessageBox.information(self, "Success", "File extracted successfully")

    def extract_tar_gz(self, file_path, destination_folder):
        with tarfile.open(file_path, "r:gz") as tar:
            tar.extractall(path=destination_folder)
        self.extract_nested_files(destination_folder)

    def extract_zip(self, file_path, destination_folder):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(destination_folder)
        self.extract_nested_files(destination_folder)

    def extract_nested_files(self, folder_path):
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.zip'):
                    file_path = os.path.join(root, file)
                    nested_folder = os.path.splitext(file_path)[0]
                    os.makedirs(nested_folder, exist_ok=True)
                    self.extract_zip(file_path, nested_folder)
                    os.remove(file_path)
                    self.extract_nested_files(nested_folder)
                elif file.endswith('.tar.gz'):
                    file_path = os.path.join(root, file)
                    nested_folder = os.path.splitext(os.path.splitext(file_path)[0])[0]
                    os.makedirs(nested_folder, exist_ok=True)
                    self.extract_tar_gz(file_path, nested_folder)
                    os.remove(file_path)
                    self.extract_nested_files(nested_folder)

    def browse_error_detection_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Choose Error Detection Folder")
        if folder_path:
            self.error_detection_folder_input.setText(folder_path)

    def upload_error_detection_folder(self):
        folder_path = self.error_detection_folder_input.text()
        if not folder_path:
            QMessageBox.warning(self, "Warning", "No folder selected for detection")
            return

        self.error_detection_folder = folder_path
        QMessageBox.information(self, "Success", "Error detection folder selected")

    def handle_enter_pressed(self):
        pattern = self.pattern_input.text().strip()
        if pattern:
            self.add_pattern(pattern)
            self.pattern_input.clear()

    def add_presets(self):
        presets = ["Exception", "exception", "Error", "error", "Failed", "failed"]
        for preset in presets:
            self.add_pattern(preset)

    def add_pattern(self, pattern):
        for i in range(self.pattern_list.count()):
            item = self.pattern_list.item(i)
            if item.text() == pattern:
                return
        list_item = QListWidgetItem(pattern)
        self.pattern_list.addItem(list_item)

    def delete_selected_pattern(self):
        selected_items = self.pattern_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "No pattern selected to delete")
            return

        for item in selected_items:
            self.pattern_list.takeItem(self.pattern_list.row(item))

    def start_detection(self):
        error_detection_folder = self.error_detection_folder
        patterns = [self.pattern_list.item(i).text() for i in range(self.pattern_list.count())]

        if not error_detection_folder:
            QMessageBox.warning(self, "Warning", "No error detection folder provided")
            return

        if not patterns:
            QMessageBox.warning(self, "Warning", "No patterns provided")
            return

        self.result_folder = self.detect_errors_in_folder(error_detection_folder, patterns)

        self.download_result_button.setEnabled(True)

        QMessageBox.information(self, "Success", "Error detection complete. Result file ready for download.")

    def detect_errors_in_folder(self, folder_path, patterns):
        output_folder = folder_path + "_output"
        os.makedirs(output_folder, exist_ok=True)

        kwtree = KeywordTree(case_insensitive=True)
        for pattern in patterns:
            kwtree.add(pattern.lower())
        kwtree.finalize()

        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.log'):
                    input_file_path = os.path.join(root, file)
                    output_file_path = os.path.join(output_folder, os.path.splitext(file)[0] + "_output.log")

                    with open(input_file_path, 'r', encoding='utf-8', errors='ignore') as infile, \
                            open(output_file_path, 'w', encoding='utf-8') as outfile:
                        for line in infile:
                            if kwtree.search(line.lower()):
                                outfile.write(line)

        return output_folder

    def download_result(self):
        destination_folder = QFileDialog.getExistingDirectory(self, "Choose Destination Folder")
        if not destination_folder:
            QMessageBox.warning(self, "Warning", "No destination folder selected")
            return

        self.copy_extracted_files(self.result_folder, destination_folder)
        QMessageBox.information(self, "Success", "Result files downloaded successfully")

    def download_extracted_files(self):
        destination_folder = QFileDialog.getExistingDirectory(self, "Choose Destination Folder")
        if not destination_folder:
            QMessageBox.warning(self, "Warning", "No destination folder selected")
            return

        for folder in self.extracted_folders:
            print(f"Copying from {folder} to {destination_folder}")
            self.copy_extracted_files(folder, destination_folder)

        QMessageBox.information(self, "Success", "Extracted files downloaded successfully")

    def copy_extracted_files(self, src, dest):
        try:
            if os.path.isdir(src):
                print(f"Copying directory: {src} to {dest}")
                shutil.copytree(src, os.path.join(dest, os.path.basename(src)), dirs_exist_ok=True)
            else:
                print(f"Copying file: {src} to {dest}")
                shutil.copy(src, dest)
        except Exception as e:
            print(f"Error copying files: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileExtractorErrorDetector()
    window.show()
    sys.exit(app.exec())
