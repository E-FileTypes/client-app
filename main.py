import sys
from e_filetypes_py import efiletypes
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QTextEdit, QCheckBox, QMessageBox

class EncryptionApp(QMainWindow):

    def __init__(self):
        super().__init__()


        self.selected_file = ""
        self.passkey = ""
        self.keep_file = True
        self.chunking = True
        self.ignore_encrypted = False
        self.ignore_existing = False
        self.initUI()
        

    def initUI(self):
        self.setWindowTitle("E-FileTypes App")
        self.setGeometry(100, 100, 400, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        tab_widget = QTabWidget()
        central_layout = QVBoxLayout()
        central_layout.setContentsMargins(10, 10, 10, 10)
        central_layout.setSpacing(10)
        central_layout.addWidget(tab_widget)
        central_widget.setLayout(central_layout)


        file_tab = QWidget()


        tab_widget.addTab(file_tab, "Encrypt")
        encrypt_section = QVBoxLayout()
        file_tab.setLayout(encrypt_section)

        file_selector_label = QLabel("Select a file:")
        encrypt_section.addWidget(file_selector_label)

        file_selector_button = QPushButton("Browse")
        encrypt_section.addWidget(file_selector_button)
        file_selector_button.clicked.connect(self.select_file)

        password_label = QLabel("Enter password:")
        encrypt_section.addWidget(password_label)

        password_textbox = QTextEdit()
        password_textbox.setPlaceholderText("Enter password here")
        password_textbox.setFixedHeight(50)
        password_textbox.textChanged.connect(self.get_password)
        encrypt_section.addWidget(password_textbox)

        generate_password_button1 = QPushButton("Generate Passkey")
        generate_password_button1.clicked.connect(self.generate_passkey_in_box)
        generate_password_button2 = QPushButton("Generate Passphrase")
        generate_password_button2.clicked.connect(self.generate_passphrase_in_box)
        encrypt_section.addWidget(generate_password_button1)
        encrypt_section.addWidget(generate_password_button2)

        keep_file_checkbox = QCheckBox("Keep File")
        keep_file_checkbox.setChecked(True)
        keep_file_checkbox.toggled.connect(self.setOptions)
        chunking_checkbox = QCheckBox("Chunking")
        chunking_checkbox.setChecked(True)
        chunking_checkbox.toggled.connect(self.setOptions)
        ignore_encrypted_checkbox = QCheckBox("Ignore Encrypted")
        ignore_encrypted_checkbox.toggled.connect(self.setOptions)

        encrypt_section.addWidget(keep_file_checkbox)
        encrypt_section.addWidget(chunking_checkbox)
        encrypt_section.addWidget(ignore_encrypted_checkbox)

        encrypt_section.addStretch(1)

        encrypt_button = QPushButton("Encrypt")
        encrypt_section.addWidget(encrypt_button)
        encrypt_button.clicked.connect(self.encrypt)

        # Create 'Decrypt' section (similar to 'Encrypt' section). laborious code written by github copilot
        decrypt_tab = QWidget()
        tab_widget.addTab(decrypt_tab, "Decrypt")
        decrypt_section = QVBoxLayout()
        decrypt_tab.setLayout(decrypt_section)

        file_selector_label_decrypt = QLabel("Select a file:")
        decrypt_section.addWidget(file_selector_label_decrypt)
        file_selector_button_decrypt = QPushButton("Browse")
        decrypt_section.addWidget(file_selector_button_decrypt)
        file_selector_button_decrypt.clicked.connect(self.select_file)

        password_label_decrypt = QLabel("Enter password:")
        decrypt_section.addWidget(password_label_decrypt)

        password_textbox_decrypt = QTextEdit()
        password_textbox_decrypt.setPlaceholderText("Enter password here")
        password_textbox_decrypt.setFixedHeight(50)
        password_textbox_decrypt.textChanged.connect(self.get_password)
        decrypt_section.addWidget(password_textbox_decrypt)

        keep_file_checkbox_decrypt = QCheckBox("Keep File")
        keep_file_checkbox_decrypt.setChecked(True)
        keep_file_checkbox_decrypt.toggled.connect(self.setOptions)
        ignore_encrypted_checkbox_decrypt = QCheckBox("Ignore Existing")
        ignore_encrypted_checkbox_decrypt.toggled.connect(self.setOptions)

        decrypt_section.addWidget(keep_file_checkbox_decrypt)
        decrypt_section.addWidget(ignore_encrypted_checkbox_decrypt)


        decrypt_section.addStretch(1)

        decrypt_button = QPushButton("Decrypt")
        decrypt_section.addWidget(decrypt_button)
        decrypt_button.clicked.connect(self.decrypt)

    def select_file(self):
        file_dialog = QFileDialog()
        QFileDialog.setOption(file_dialog, QFileDialog.Option.ReadOnly)
        QFileDialog.setFileMode(file_dialog, QFileDialog.FileMode.ExistingFile)
        
        file = file_dialog.getOpenFileName(self, "Select a file")[0]
        if file:
            self.selected_file = file
            self.update()
            msg = QMessageBox()
            msg.setWindowTitle("File selected")
            msg.setText("File selected: " + file)
            msg.exec()
    
    def setOptions(self):
        if self.sender().text() == "Keep File":
            self.keep_file = not self.keep_file
        elif self.sender().text() == "Chunking":
            self.chunking = not self.chunking
        elif self.sender().text() == "Ignore Encrypted":
            self.ignore_encrypted = not self.ignore_encrypted
        elif self.sender().text() == "Ignore Existing":
            self.ignore_existing = not self.ignore_existing
        self.update()
        
    def get_password(self):
        self.passkey = self.sender().toPlainText()
        self.update()

    def generate_passkey_in_box(self):
        self.passkey = efiletypes.generate_passkey()
        # Update the password textbox
        self.sender().parent().children()[4].setText(self.passkey)
        self.update()
    
    def generate_passphrase_in_box(self):
        self.passkey = efiletypes.generate_passphrase()
        # Update the password textbox
        self.sender().parent().children()[4].setText(self.passkey)
        self.update()

    def encrypt(self):
        if self.selected_file == "":
            msg = QMessageBox()
            msg.setWindowTitle("No file selected")
            msg.setText("Please select a file to encrypt")
            msg.exec()
            return
        if self.passkey == "":
            msg = QMessageBox()
            msg.setWindowTitle("No password")
            msg.setText("Please enter a password")
            msg.exec()
            return
        msg = QMessageBox()
        msg.setWindowTitle("Encrypting")
        msg.setText("Encrypting... this may take a while...")
        msg.exec()
        try:
            efiletypes.encrypt(path=self.selected_file, passkey=self.passkey, keep_file=self.keep_file, chunking=self.chunking, ignore_encrypted=self.ignore_encrypted)
        except Exception as e:
            print(e)
            msg = QMessageBox()
            msg.setWindowTitle("Encryption failed")
            msg.setText(f"Encryption failed. {e} Please try again.")
            msg.exec()
            return
        msg = QMessageBox()
        msg.setWindowTitle("Encryption complete")
        msg.setText("Encryption complete")
        msg.exec()

    def decrypt(self):
        if self.selected_file == "":
            msg = QMessageBox()
            msg.setWindowTitle("No file selected")
            msg.setText("Please select a file to decrypt")
            msg.exec()
            return
        if self.passkey == "":
            msg = QMessageBox()
            msg.setWindowTitle("No password")
            msg.setText("Please enter a password")
            msg.exec()
            return
        msg = QMessageBox()
        msg.setWindowTitle("Decrypting")
        msg.setText("Decrypting... this may take a while...")
        msg.exec()
        try:
            efiletypes.decrypt(path=self.selected_file, passkey=self.passkey, keep_file=self.keep_file, ignore_existing=self.ignore_existing)
        except Exception as e:
            print(e)
            msg = QMessageBox()
            msg.setWindowTitle("Decryption failed")
            msg.setText(f"Decryption failed. {e} Please try again.")
            msg.exec()
            return
        msg = QMessageBox()
        msg.setWindowTitle("Decryption complete")
        msg.setText("Decryption complete")
        msg.exec()

def main():
    app = QApplication(sys.argv)
    window = EncryptionApp()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()