import tkinter as tk
import os
import json
from data.lists.region_list import REGION_LIST
from gui.modules.AutocompleteEntry import AutocompleteEntry as AE
from tkinter import ttk

global question_widgets, final_question
question_widgets = {}
final_question = 1

highlightbackground = "#c8c8c8"
highlightcolor = "#393939"
bg_active = "#ffffff"
bg_inactive = "#e8e7e7"
code_active = "#c5e6f4"

def select_code(qid, code):
    """Đặt lựa chọn của câu hỏi tại index thành code"""
    if 0 <= qid < len(question_widgets):
        question_widgets[qid]["var"].set(code)

def generate_questions(question_frame, form, wrap_length=600, canvas=None, scrollable_frame=None):
    global final_question
    question_counter = 0  # Biến đếm số thứ tự câu hỏi

    generate_questions.canvas = canvas
    generate_questions.scrollable_frame = scrollable_frame

    for current_question in form["questions"]:
        render_labels = True
        render_items = True

        widget_info = {}
        widget_items = []
        
        qid = current_question["id"]
        qtype = current_question["type"]

        question_counter += 1
        widget_info["index"] = question_counter
        # Main frame for this question
        widget_frame = tk.Frame(
            question_frame,
            padx=10, pady=10,
            highlightthickness=2,
            highlightbackground=highlightbackground,
            highlightcolor=highlightcolor,
            bg=bg_active,
        )
        widget_frame.pack(fill="x", pady=5)

        # Số thứ tự câu hỏi
        number_label = tk.Label(
            widget_frame,
            text=f"{question_counter}",
            font=("Arial", 9, "italic"),
            fg="gray",
            bg=widget_frame["bg"],
            anchor="ne"
        )
        number_label.place(relx=1.0, rely=0.0, anchor="ne", x=-2, y=2)
        widget_items.append(number_label)

        if render_labels:
            # Title
            title = tk.Label(
                widget_frame,
                text=current_question["title"], font=("Arial", 12, "bold"),
                anchor="w", justify="left", 
                bg=widget_frame["bg"],
                wraplength=wrap_length,
            )
            title.pack(anchor="w")
            widget_items.append(title)

            # Desciription
            if current_question["description"] != "":
                description = None
                description = tk.Label(
                        widget_frame, 
                        text=current_question["description"], font=("Arial", 11),
                        anchor="w", justify="left", 
                        bg=widget_frame["bg"],
                        wraplength=wrap_length - 10
                    )
                description.pack(anchor="w")
                widget_items.append(description)

            # Tip 
            if current_question["tip"] != "":
                tip = None
                tip = tk.Label(
                        widget_frame, 
                        text=current_question["tip"], font=("Arial", 10, "italic"),
                        anchor="w", justify="left", 
                        bg=widget_frame["bg"],
                        wraplength=wrap_length
                    )
                tip.pack(anchor="w")
                widget_items.append(tip)

                # Store widget info
            widget_info["type"] = qtype
            widget_info["frame"] = widget_frame
            
        
        if render_items:
            match qtype:
            # --- TEXT ---
                case "text":
                    entries = {}

                    for field_id, field_data in current_question.get("fields", {}).items():
                        # Hiển thị tiêu đề
                        label = tk.Label(
                            widget_frame,
                            text=field_data.get("title", field_id),
                            font=("Arial", 11, "bold"),
                            bg=widget_frame["bg"],
                            anchor="w"
                        )
                        label.pack(fill="x", pady=(8, 0))
                        widget_items.append(label)

                        # Tạo ô nhập
                        entry = tk.Entry(
                            widget_frame,
                            font=("Arial", 12),
                            bg="white"
                        )
                        entry.pack(fill="x", pady=(0, 8))

                        entries[field_id] = entry

                    # Lưu các entries vào widget_info để truy cập sau này
                    widget_info["entries"] = entries

            # --- NUMBER CODE ---
                case "number_code":
                    code_labels = {}

                    for code, option in current_question["options"].items():
                        row = tk.Frame(
                            widget_frame, 
                            bg=widget_frame["bg"]
                        )
                        row.pack(fill="x")
                        widget_items.append(row)

                        lbl_code = tk.Label(
                            row, 
                            text=code, 
                            width=5, 
                            relief="solid", borderwidth=1,
                            bg=bg_inactive
                        )
                        lbl_code.pack(side="left", padx=(0,5))
                        

                        lbl_text = tk.Label(
                            row, 
                            text=option["title"], anchor="w",
                            bg=widget_frame["bg"],
                            wraplength=wrap_length-80,
                            justify="left")
                        lbl_text.pack(side="left", fill="x")
                        widget_items.append(lbl_text)

                        # row.bind("<Button-1>", lambda e, qid=qid, c=code: select_code(qid, c))

                        
                        code_labels[code] = {"code": lbl_code}

                    widget_info["code_labels"] = code_labels

                # --- PROMPT ---
                case "prompt":
                    lbl_info = tk.Label(
                        widget_frame,
                        text="Bấm [Enter] để tiếp tục",
                        font=("Arial",12,"italic"), 
                        wraplength=wrap_length,
                        justify="left", state="disabled",
                        bg=widget_frame["bg"]
                    )
                    lbl_info.pack(fill="x", pady=4)
                    widget_items.append(lbl_info)
                    widget_info["info_label"] = lbl_info

                # --- PROMPT ---
                case "complete":
                    lbl_info = tk.Label(
                        widget_frame,
                        text="Bấm [Enter] để lưu file",
                        font=("Arial",12,"italic"), 
                        wraplength=wrap_length,
                        justify="left", state="disabled",
                        bg=widget_frame["bg"]
                    )
                    lbl_info.pack(fill="x", pady=4)
                    widget_items.append(lbl_info)
                    widget_info["info_label"] = lbl_info
                    final_question = question_counter

                # --- SCORE ---
                case "score":
                    score_frame = tk.Frame(
                        widget_frame, 
                        bg=question_frame["bg"]
                    )
                    score_frame.pack(pady=4)
                    widget_items.append(score_frame)

                    
                    code_labels = {}
                    for code, opt in current_question["options"].items():
                        col = tk.Frame(
                            score_frame,
                            highlightthickness=1, 
                            pady=0)
                        col.pack(side="left", padx=0)

                        lbl_code = tk.Label(
                            col, 
                            text=code, 
                            width=5, 
                            relief="solid", borderwidth=1,
                            bg=bg_inactive
                        )
                        
                        lbl_code.pack()

                        code_labels[code] = {"code": lbl_code}

                    widget_info["code_labels"] = code_labels

                # --- DROPDOWN ---
                case "dropdown":
                    selected = tk.StringVar()
                    autoEntry = AE(widget_frame, REGION_LIST, textvariable=selected)
                    autoEntry.pack(fill="x", pady=(4, 8))

                    widget_info["dropdown"] = autoEntry
                    widget_info["selected"] = selected

        widget_info["widget_items"] = widget_items
        question_widgets[qid] = widget_info




global progress_var
progress_var = None

def set_progress_var(target):
    global progress_var
    progress_var=target

def update(id):
    from logic.handler import load_cache
    global progress_var
    cache = load_cache()
    scroll_to_question = True

    # Update the state of all question widgets based on the current id
    for qid, widget in question_widgets.items():
        active = (qid == id)
        bg_color = bg_active if active else bg_inactive

        if active:
            index = question_widgets[id]["index"]
            if index > 1 and index < final_question:
                progress = (index / final_question) * 100
                progress_var.set(progress)
            if index == 1:
                progress_var.set(0)
            
            widget["frame"].focus_set()

        widget["frame"].config(bg=bg_color)
        for item in widget["widget_items"]:
            item.config(bg=bg_color)

        match widget["type"]:
            case "text":
                first_entry = None
                if "entries" in widget:
                    for entry in widget["entries"].values():
                        if active:
                            if first_entry == None:
                                first_entry = entry
                                first_entry.focus_set()
                            entry.config(state="normal")
                        else:
                            entry.config(state="disabled")
            case "dropdown":
                if active:
                    widget["dropdown"].focus_set()

            case "number_code":
                if qid in cache:
                    cur_ans = str(cache[qid])  # Đáp án đã chọn từ cache

                    for code, label_dict in widget["code_labels"].items():
                        code_str = str(code)
                        selected = (code_str == cur_ans)

                        code_lbl = label_dict["code"]

                        if selected:
                            code_lbl.config(bg=code_active)
                        else:
                            code_lbl.config(bg=bg_inactive)
            case "score":
                if qid in cache:
                    cur_ans = str(cache[qid])  # Đáp án đã chọn từ cache

                    for code, label_dict in widget["code_labels"].items():
                        code_str = str(code)
                        selected = (code_str == cur_ans)

                        code_lbl = label_dict["code"]

                        if selected:
                            code_lbl.config(bg=code_active)
                        else:
                            code_lbl.config(bg=bg_inactive)

    if scroll_to_question:
        if hasattr(generate_questions, "canvas") and hasattr(generate_questions, "scrollable_frame"):
            canvas = generate_questions.canvas
            scrollable_frame = generate_questions.scrollable_frame

            if id in question_widgets:
                widget_frame = question_widgets[id]["frame"]
                canvas.update_idletasks()

                # Tính khoảng cách từ đầu scrollable_frame đến widget
                widget_y = widget_frame.winfo_rooty() - scrollable_frame.winfo_rooty()
                canvas_height = canvas.winfo_height()
                total_height = scrollable_frame.winfo_height()

                # Tính tỉ lệ để cuộn
                target = widget_y / total_height
                target = min(max(target, 0), 1) - 0.025
                canvas.yview_moveto(target)