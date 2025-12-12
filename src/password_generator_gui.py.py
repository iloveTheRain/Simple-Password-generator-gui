from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QHBoxLayout, QSlider, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

import sys
import string
import random

from time import sleep
from pathlib import Path
from colorama import init, Fore


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Generator")
        self.setFixedSize(200,200)

        cont = QWidget()
        self.setCentralWidget(cont)
        self.layout1 = QVBoxLayout(cont)

        self.silder = QSlider(Qt.Orientation.Horizontal)
        self.silder.setMinimum(8)
        self.silder.setMaximum(24)

        self.label = QLabel("8")        
        self.silder.valueChanged.connect(lambda data: self.label.setText(str(data)))

        self.button = QPushButton("Generate Password!")
        self.button.clicked.connect(self.start_button)

        new_cont = QWidget()
        new_layout = QHBoxLayout(new_cont)

        
        new_layout.addWidget(self.label)
        new_layout.addWidget(self.silder)
        self.layout1.addWidget(new_cont)
        
        self.output = QLabel("")
        self.output.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.output.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.layout1.addWidget(self.button)
        self.layout1.addWidget(self.output)

        self.save_button = QPushButton("Save Password")
        self.save_button.clicked.connect(self.save_password)

    
    def get_password(self):
        chars = string.ascii_letters
        numbers = string.digits
        speical = "!@#$%^&*()-_+=][}{|~"

        all_chars = chars +  numbers + speical

        password = "".join(random.choice(all_chars) for i in range(int(self.label.text())))

        return password
    
    def start_button(self):
        self.output.setText(self.get_password())
        self.layout1.addWidget(self.save_button)
        self.save_button.setText("Save Password")
        sleep(0.05)

    def save_password(self):
        path = Path(__file__).parent.resolve()
        full_path = path / "password.txt"

        try:
            with open(full_path, 'r') as r_file:
                content = r_file.read()
                if self.output.text() in content:
                    print(Fore.RED + "Password already exists!")
                    self.save_button.setText("Password Already Exists!")
                    return

            with open(full_path, 'a') as file:  
                file.write(self.output.text() + '\n')  
                print(Fore.GREEN + "Password Saved!")
                self.save_button.setText("Password Saved!")

        except FileNotFoundError:
            with open(full_path, 'w') as file:
                file.write(self.output.text() + '\n')
                print(Fore.GREEN + "Password Saved!")
                self.save_button.setText("Password Saved!")

        except Exception as e:
            print(Fore.RED + f"Error saving password: {e}")
            self.save_button.setText("Save Failed!")



if __name__ == '__main__':
    init(autoreset=True)

    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    app.exec()