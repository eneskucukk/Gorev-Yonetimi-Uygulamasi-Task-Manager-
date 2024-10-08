import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QLabel, QListWidget, QHBoxLayout, QComboBox, QMessageBox
)
from PyQt5.QtCore import Qt

class TaskManagerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Görev Yönetimi Uygulaması")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Görev başlığı girişi
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Görev başlığını girin...")
        self.layout.addWidget(self.task_input)

        # Kategori seçimi
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Genel", "İş", "Kişisel", "Diğer"])
        self.layout.addWidget(self.category_combo)

        # Görevleri listelemek için liste widget'ı
        self.tasks_list = QListWidget()
        self.layout.addWidget(self.tasks_list)

        # Görev ekleme butonu
        self.add_button = QPushButton("Görev Ekle")
        self.add_button.clicked.connect(self.add_task)
        self.layout.addWidget(self.add_button)

        # Görev tamamlama butonu
        self.complete_button = QPushButton("Görevi Tamamla")
        self.complete_button.clicked.connect(self.complete_task)
        self.layout.addWidget(self.complete_button)

        # Görev silme butonu
        self.delete_button = QPushButton("Görev Sil")
        self.delete_button.clicked.connect(self.delete_task)
        self.layout.addWidget(self.delete_button)

        # Görevleri yükle
        self.load_tasks()

    def add_task(self):
        task = self.task_input.text()
        category = self.category_combo.currentText()
        if task:
            tasks = self.load_existing_tasks()
            tasks.append({"task": task, "category": category, "completed": False})
            with open("tasks.json", "w") as file:
                json.dump(tasks, file)
            self.tasks_list.addItem(f"{task} [{category}]")
            self.task_input.clear()
        else:
            QMessageBox.warning(self, "Hata", "Lütfen bir görev girin.")

    def load_tasks(self):
        tasks = self.load_existing_tasks()
        for task in tasks:
            status = "✓" if task["completed"] else "✗"
            self.tasks_list.addItem(f"{status} {task['task']} [{task['category']}]")

    def load_existing_tasks(self):
        try:
            with open("tasks.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def complete_task(self):
        selected_item = self.tasks_list.currentItem()
        if selected_item:
            task_text = selected_item.text()
            task_title = task_text.split(" ")[1]  # "✓" veya "✗" işaretini temizle
            tasks = self.load_existing_tasks()
            for task in tasks:
                if task["task"] == task_title:
                    task["completed"] = not task["completed"]
                    break
            with open("tasks.json", "w") as file:
                json.dump(tasks, file)
            self.tasks_list.clear()
            self.load_tasks()
        else:
            QMessageBox.warning(self, "Hata", "Lütfen tamamlamak için bir görev seçin.")

    def delete_task(self):
        selected_item = self.tasks_list.currentItem()
        if selected_item:
            task_to_delete = selected_item.text().split(" ")[1]  # "✓" veya "✗" işaretini temizle
            tasks = self.load_existing_tasks()
            tasks = [task for task in tasks if task["task"] != task_to_delete]
            with open("tasks.json", "w") as file:
                json.dump(tasks, file)
            self.tasks_list.takeItem(self.tasks_list.row(selected_item))
            self.task_input.clear()
        else:
            QMessageBox.warning(self, "Hata", "Lütfen silmek için bir görev seçin.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TaskManagerApp()
    window.show()
    sys.exit(app.exec_())

