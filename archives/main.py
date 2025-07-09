import tkinter as tk
import json
import os
import helper as h

FORM_TEMPLATE = "form_template.json"
OUTPUT_DIR = "output"
CANDIDATE_ID = "12"
CANDIDATE_NAME = "Trần Thế Bách"
SETTINGS_FILE = "settings.json"

# GUI
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

with open(FORM_TEMPLATE, "r", encoding="utf-8") as f:
    form = json.load(f)

questions = {q["id"]: q for q in form["questions"]}
answers = {}
current_question_id = form["questions"][0]["id"]
question_widgets = {}
selected_code = None



# Save function
def save_and_quit():
    filename = f"{CANDIDATE_ID}_{h.sanitize_filename(CANDIDATE_NAME)}.json"
    filepath = os.path.join(OUTPUT_DIR, filename)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output = {
    "answers": answers,
    "candidate_id": CANDIDATE_ID,
    "candidate_name": CANDIDATE_NAME,
    "month": candidate_month.get(),
    "form_link": form_link.get()
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\u0110\u00e3 l\u01b0u v\u00e0o: {OUTPUT_DIR}")
    #root.quit()

# Handle Enter

def handle_enter(event=None):
    global current_question_id, selected_code
    question = questions[current_question_id]
    widget = question_widgets[current_question_id]

    match question["type"]:
        case "text":
            val = widget["entry"].get().strip()
            
            answers[current_question_id] = val
            current_question_id = question["next"]
            update_states()

        case "number_code":
            answers[current_question_id] = selected_code
            if selected_code is None:
                next_q = question["next"]
            else:
                next_q = question["options"][selected_code]["next"]

            if next_q == "end":
                save_and_quit()
            else:
                current_question_id = next_q
                selected_code = None
                update_states()


# Navigation buttons
def go_back():
    global current_question_id, selected_code  # Thêm dòng này
    ids = list(questions.keys())
    idx = ids.index(current_question_id)
    if idx > 0:
        current_question_id = ids[idx - 1]
        selected_code = None
        update_states()

def go_next():
    ids = list(questions.keys())
    idx = ids.index(current_question_id)
    if idx < len(ids) - 1:
        handle_enter()



def select_code(qid, code):
    global selected_code
    selected_code = code

    widget = question_widgets[qid]
    is_active = (qid == current_question_id)

    for c, row in widget["code_rows"].items():
        lbl_code = widget["code_labels"][c]["code"]
        lbl_text = widget["code_labels"][c]["text"]

        row.config(bg="white" if is_active else "#f0f0f0")
        lbl_text.config(bg="white" if is_active else "#f0f0f0")

        if c == code:
            lbl_code.config(bg="#cceeff", highlightbackground="#3399ff")
        else:
            lbl_code.config(bg="white" if is_active else "#f0f0f0", highlightbackground="#cccccc")



# Update states

def update_states():
    for qid, widget in question_widgets.items():
        active = qid == current_question_id
        bg_color = "white" if active else "#f0f0f0"
        widget["frame"].config(bg=bg_color)
        for lbl in widget.get("labels", []):
            lbl.config(bg=bg_color)

        match widget["type"]:
            case "text":
                widget["entry"].config(state="normal" if active else "disabled")
            case "number_code":
                for code, row in widget["code_rows"].items():
                    if active:
                        row.bind("<Button-1>", lambda e, qid=qid, c=code: select_code(qid, c))
                    else:
                        row.unbind("<Button-1>")

    highlight_question(current_question_id)

# Render all questions

def render_all_questions():
    for q in form["questions"]:
        qid = q["id"]
        qtype = q["type"]

        frame_q = tk.Frame(
            left_frame,
            padx=10, pady=10,
            highlightthickness=1,
            highlightbackground="#cccccc",
        )
        frame_q.pack(fill="x", pady=5)

        label_parts = q["label"].split("\n", 1)
        bold_part = label_parts[0]
        rest_part = label_parts[1] if len(label_parts) > 1 else ""

        labels = []
        label_bold = tk.Label(
            frame_q, text=bold_part, font=("Arial", 12, "bold"), anchor="w",
            justify="left", wraplength=WINDOW_WIDTH * 0.6 - 20, bg=frame_q["bg"]
        )
        label_bold.pack(anchor="w")
        labels.append(label_bold)

        if rest_part:
            label_rest = tk.Label(
                frame_q, text=rest_part, font=("Arial", 12), anchor="w",
                justify="left", wraplength=WINDOW_WIDTH * 0.6 - 20, bg=frame_q["bg"]
            )
            label_rest.pack(anchor="w")
            labels.append(label_rest)

        widget_info = {"type": qtype, "frame": frame_q, "labels": labels}

        if qtype == "text":
            entry = tk.Entry(frame_q, font=("Arial", 12))
            entry.pack(fill="x", pady=4)
            widget_info["entry"] = entry

        elif qtype == "number_code":
            code_rows = {}
            code_labels = {}
            for code, opt in q["options"].items():
                row = tk.Frame(frame_q, highlightthickness=1)
                row.pack(fill="x", pady=0)

                lbl_code = tk.Label(
                    row,
                    text=code,
                    width=5,
                    bg=row["bg"],
                    relief="solid",
                    borderwidth=1,
                    highlightthickness=0,
                    highlightbackground="#cccccc"
                )

                lbl_code.pack(side="left")
                lbl_text = tk.Label(row, text=opt["label"], anchor="w", bg=row["bg"])
                lbl_text.pack(side="left", fill="x")

                row.config(bg="#f0f0f0")
                row.bind("<Button-1>", lambda e, qid=qid, c=code: select_code(qid, c))

                code_rows[code] = row
                code_labels[code] = {"code": lbl_code, "text": lbl_text}

            widget_info["code_rows"] = code_rows
            widget_info["code_labels"] = code_labels

        question_widgets[qid] = widget_info


def highlight_question(qid):
    for qkey, widget in question_widgets.items():
        is_active = (qkey == qid)
        highlight_color = "#000000" if is_active else "#cccccc"
        bg_color = "white" if is_active else "#f0f0f0"

        frame = widget["frame"]
        frame.config(highlightbackground=highlight_color, bg=bg_color)

        for lbl in widget.get("labels", []):
            lbl.config(bg=bg_color)

        if widget["type"] == "number_code":
            for code, row in widget["code_rows"].items():
                lbl_code = widget["code_labels"][code]["code"]
                lbl_text = widget["code_labels"][code]["text"]

                if answers.get(qkey) == code:
                    row.config(bg=bg_color, highlightbackground=bg_color, highlightthickness=0)
                    lbl_code.config(bg="#c5e6f4", highlightbackground="#97bce3")
                    lbl_text.config(bg=bg_color)
                else:
                    row.config(bg=bg_color, highlightbackground=bg_color, highlightthickness=0)
                    lbl_code.config(bg=bg_color)
                    lbl_text.config(bg=bg_color)

# Handle keypress
def handle_keypress(event):
    if current_question_id not in question_widgets:
        return
    q = questions[current_question_id]
    if q["type"] == "number_code":
        key = event.char
        if key in q["options"]:
            select_code(current_question_id, key)

def load_settings_from_file():
    global CANDIDATE_ID, CANDIDATE_NAME
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            settings = json.load(f)
            CANDIDATE_ID = settings.get("candidate_id", "")
            CANDIDATE_NAME = settings.get("candidate_name", "")
            candidate_month.set(settings.get("month", ""))
            form_link.set(settings.get("form_link", ""))
        
def save_settings_to_file():
    settings = {
        "candidate_id": CANDIDATE_ID,
        "candidate_name": CANDIDATE_NAME,
        "month": candidate_month.get(),
        "form_link": form_link.get()
    }
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)

def open_settings_window():
    settings_window = tk.Toplevel(root)
    settings_window.title("Cài đặt thông tin chung")
    settings_window.geometry("400x300")
    settings_window.grab_set()

    def save_settings():
        nonlocal entry_id, entry_name, entry_month, entry_link
        global CANDIDATE_ID, CANDIDATE_NAME

        CANDIDATE_ID = entry_id.get().strip()
        CANDIDATE_NAME = entry_name.get().strip()
        candidate_month.set(entry_month.get().strip())
        form_link.set(entry_link.get().strip())

        save_settings_to_file()
        settings_window.destroy()

    tk.Label(settings_window, text="Mã số PVV:").pack(anchor="w", padx=10)
    entry_id = tk.Entry(settings_window)
    entry_id.insert(0, CANDIDATE_ID)
    entry_id.pack(fill="x", padx=10)

    tk.Label(settings_window, text="Họ Tên PVV:").pack(anchor="w", padx=10)
    entry_name = tk.Entry(settings_window)
    entry_name.insert(0, CANDIDATE_NAME)
    entry_name.pack(fill="x", padx=10)

    tk.Label(settings_window, text="Mã tháng:").pack(anchor="w", padx=10)
    entry_month = tk.Entry(settings_window)
    entry_month.insert(0, candidate_month.get())
    entry_month.pack(fill="x", padx=10)

    tk.Label(settings_window, text="Link biểu mẫu:").pack(anchor="w", padx=10)
    entry_link = tk.Entry(settings_window)
    entry_link.insert(0, form_link.get())
    entry_link.pack(fill="x", padx=10)

    tk.Button(settings_window, text="Lưu", command=save_settings).pack(pady=15)


# GUI Setup
root = tk.Tk()
root.title("Khảo sát")

candidate_month = tk.StringVar(value="")
form_link = tk.StringVar(value="")

load_settings_from_file()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - WINDOW_WIDTH) // 2
y = (screen_height - WINDOW_HEIGHT) // 2
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
root.resizable(width=False, height=True)
root.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)

# Main layout
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

# Horizontal layout: left (70%) - separator - right (30%)
layout = tk.Frame(main_frame)
layout.pack(fill="both", expand=True)

# Khung bao gồm cả tiêu đề + canvas
left_wrapper = tk.Frame(layout, width=int(WINDOW_WIDTH * 0.6))
left_wrapper.pack(side="left", fill="both", expand=True)

# Tiêu đề Câu hỏi (không cuộn)
tk.Label(left_wrapper, text="Câu hỏi", font=("Arial", 12, "bold")).pack(pady=(10, 5), fill="x")
tk.Frame(left_wrapper, height=1, bg="#cccccc").pack(fill="x", padx=(0,16), pady=(0, 5))


# Canvas + Scrollbar
canvas_frame = tk.Frame(left_wrapper)
canvas_frame.pack(fill="both", expand=True)

canvas = tk.Canvas(canvas_frame, highlightthickness=0)
scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# Khung thực tế chứa các câu hỏi
left_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=left_frame, anchor="nw")
canvas_window = canvas.create_window((0, 0), window=left_frame, anchor="nw")

def on_canvas_resize(event):
    canvas.itemconfig(canvas_window, width=event.width)

# Update scrollregion
def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

def _on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

left_frame.bind("<Configure>", on_configure)

right_frame = tk.Frame(layout, width=int(WINDOW_WIDTH * 0.4))
right_frame.pack(side="right", fill="y")

# Right controls
tk.Label(right_frame, text="Điều khiển", font=("Arial", 12, "bold")).pack(pady=(10, 5), padx=10)
tk.Frame(right_frame, height=1, bg="#cccccc").pack(fill="x", pady=(0, 5))

btn_settings = tk.Button(right_frame, text="⚙️ Cài đặt", command=open_settings_window)
btn_settings.pack(pady=(5, 10), fill="x", padx=1)

btn_enter = tk.Button(right_frame, text="Enter / Tiếp", command=handle_enter)
btn_enter.pack(pady=(5,10), fill="x", padx=1)

btn_back = tk.Button(right_frame, text="←", command=go_back)
btn_back.pack(pady=1, fill="x", padx=1)

btn_next = tk.Button(right_frame, text="→", command=go_next)
btn_next.pack(pady=1, fill="x", padx=1)

# Render questions
render_all_questions()
update_states()

# Bindings
root.bind("<Return>", handle_enter)
root.bind("<Key>", handle_keypress)
root.bind("<Left>", lambda event: go_back())
root.bind("<Right>", lambda event: go_next())

canvas.bind("<Configure>", on_canvas_resize)
canvas.bind_all("<MouseWheel>", _on_mousewheel)

root.mainloop()
