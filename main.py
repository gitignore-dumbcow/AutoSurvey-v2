import tkinter as tk
import json
from gui.layout import setup_layout
import gui.render as render
from logic.handler import handle_enter, handle_keypress, go_up, go_down

WINDOW_WIDTH = 800 
WINDOW_HEIGHT = 600


# Parameters for rendering the form

FORM_TEMPLATE = "data/form_template.json"
with open(FORM_TEMPLATE, "r", encoding="utf-8") as f:
    form = json.load(f)
current_question_id = form["questions"][0]["id"]
answers = {}

# Initialize the main application window
root = tk.Tk()
root.title("AutoSurvey")

left_frame, right_frame, canvas = setup_layout(root, WINDOW_WIDTH, WINDOW_HEIGHT)

render.generate_questions(left_frame, form, 620, canvas=canvas, scrollable_frame=left_frame)

root.bind("<Return>", handle_enter)
root.bind("<Key>", handle_keypress)
root.bind("<Up>", lambda event: go_up())
root.bind("<Down>", lambda event: go_down())

root.mainloop()
