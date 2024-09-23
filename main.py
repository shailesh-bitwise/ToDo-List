from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.list import OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.snackbar import Snackbar
from kivy.core.window import Window  # Import Window here
import os
import json

class MainApp(MDApp):
    dialog = None
    tasks = []

    def build(self):
        # Load tasks from file if exists
        self.load_tasks()
        return Builder.load_file("todolist.kv")

    def show_exit_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Exit",
                text="Are you sure you want to exit?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_press=self.close_exit_dialog
                    ),
                    MDFlatButton(
                        text="EXIT",
                        on_press=self.exit_app
                    ),
                ],
            )
        self.dialog.open()

    def close_exit_dialog(self, instance):
        if self.dialog:
            self.dialog.dismiss()

    def exit_app(self, instance):
        if self.dialog:
            self.dialog.dismiss()
        Window.close()

    def save_todo_item(self, _):
        if not self.dialog: return
        text = self.content.text
        if not text.strip():
            Snackbar(text="Task cannot be empty").open()
            return
        self.root.ids.todo_list.add_widget(OneLineListItem(text=text, on_release=self.show_task_options))
        self.tasks.append({"text": text, "completed": False})
        self.save_tasks()
        self.dialog.dismiss()

    def close_dialog(self, _):
        if not self.dialog: return
        self.dialog.dismiss()

    def show_dialog(self):
        if not self.dialog:
            dialog = BoxLayout(orientation="horizontal", spacing="12dp", size_hint_y=None, height="80dp")
            self.content = MDTextField(hint_text="Task")
            dialog.add_widget(self.content)
            self.dialog = MDDialog(
                title="Add Task:",
                type="custom",
                content_cls=dialog,
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_press=self.close_dialog
                    ),
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_press=self.save_todo_item
                    ),
                ],
            )
        else:
            self.content.text = ""
        self.dialog.open()

    def on_start(self):
        for task in self.tasks:
            task_widget = OneLineListItem(text=task["text"], on_release=self.show_task_options)
            if task["completed"]:
                task_widget.text = f"[s]{task['text']}[/s]"
            self.root.ids.todo_list.add_widget(task_widget)

    def show_task_options(self, instance):
        """ Show dialog with options to delete or edit a task """
        self.selected_task = instance
        self.task_dialog = MDDialog(
            title=instance.text,
            buttons=[
                MDFlatButton(
                    text="DELETE",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_press=self.delete_task
                ),
                MDFlatButton(
                    text="EDIT",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_press=self.edit_task
                ),
                MDFlatButton(
                    text="MARK COMPLETED",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_press=self.mark_completed
                ),
            ]
        )
        self.task_dialog.open()

    def delete_task(self, _):
        self.root.ids.todo_list.remove_widget(self.selected_task)
        self.tasks = [task for task in self.tasks if task["text"] != self.selected_task.text]
        self.save_tasks()
        self.task_dialog.dismiss()

    def edit_task(self, _):
        self.show_dialog()
        self.content.text = self.selected_task.text
        self.tasks = [task for task in self.tasks if task["text"] != self.selected_task.text]
        self.root.ids.todo_list.remove_widget(self.selected_task)
        self.task_dialog.dismiss()

    def mark_completed(self, _):
        for task in self.tasks:
            if task["text"] == self.selected_task.text:
                task["completed"] = True
                self.selected_task.text = f"[s]{task['text']}[/s]"
                break
        self.save_tasks()
        self.task_dialog.dismiss()

    def save_tasks(self):
        """ Save tasks to a file """
        with open("tasks.json", "w") as file:
            json.dump(self.tasks, file)

    def load_tasks(self):
        """ Load tasks from a file if it exists """
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as file:
                self.tasks = json.load(file)

if __name__ == "__main__":
    MainApp().run()
