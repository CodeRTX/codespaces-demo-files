import tkinter as tk
from tkinter import messagebox
from quiz_data import get_questions
import random

class QuizApp:
    def __init__(self, root, num_questions=15):
        self.root = root
        self.root.title("GK & Current Affairs Quiz")
        self.num_questions = num_questions
        self.questions = get_questions(self.num_questions)
        self.question_index = 0
        self.score = 0
        self.create_widgets()
        self.display_question()

    def create_widgets(self):
        self.question_label = tk.Label(self.root, text="", wraplength=400, justify="left")
        self.question_label.pack(pady=20)

        self.options = []
        for _ in range(4):
            btn = tk.Button(self.root, text="", command=lambda b=_: self.check_answer(b))
            btn.pack(fill="x", pady=5)
            self.options.append(btn)

        self.score_label = tk.Label(self.root, text="Score: 0")
        self.score_label.pack(pady=20)

    def display_question(self):
        question = self.questions[self.question_index]
        self.question_label.config(text=question["question"])
        options = question["incorrect_answers"] + [question["correct_answer"]]
        random.shuffle(options)
        for i, option in enumerate(options):
            self.options[i].config(text=option)

    def check_answer(self, btn_index):
        selected_answer = self.options[btn_index].cget("text")
        correct_answer = self.questions[self.question_index]["correct_answer"]
        if selected_answer == correct_answer:
            self.score += 1
        self.question_index += 1
        if self.question_index < self.num_questions:
            self.display_question()
        else:
            self.show_results()

    def show_results(self):
        percentage = (self.score / self.num_questions) * 100
        messagebox.showinfo("Quiz Completed", f"Your Score: {self.score}/{self.num_questions}\nPercentage: {percentage:.2f}%")
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
