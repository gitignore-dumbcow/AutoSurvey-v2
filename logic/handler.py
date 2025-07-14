import json
import os
from gui.render import question_widgets, update

FORM_TEMPLATE = "data/form_template.json"

with open(FORM_TEMPLATE, "r", encoding="utf-8") as f:
    form = json.load(f)

questions = {q["id"]: q for q in form["questions"]}
current_id = form["questions"][0]["id"]

answers = {}
selected_code = None

def load_cache(clear = False, file=None):    
    if file == None:
        CACHE_FILE = "output/cache.json"
    else:
        return
    if os.path.exists(CACHE_FILE):
        if(clear):
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump("", f, ensure_ascii=False, indent=2)
        else:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)

load_cache(True)

def open_file():
    update("s0")

def handle_enter(event=None):
    global current_id, selected_code

    cache_answers()  

    question = questions[current_id]
    widget = question_widgets[current_id]

    match question["type"]:
        case "text":
            if "entries" not in widget:
                return

            entries: dict = widget["entries"]
            entry_widgets = list(entries.values())
            field_ids = list(entries.keys())

            # Xác định entry đang active
            if event is not None and event.widget in entry_widgets:
                current_idx = entry_widgets.index(event.widget)

                if current_idx + 1 < len(entry_widgets):
                    # Focus vào entry tiếp theo
                    next_entry = entry_widgets[current_idx + 1]
                    next_entry.focus_set()
                    return  # Không chuyển câu
                else:
                    # Không còn entry nào → chuyển sang câu hỏi kế tiếp
                    next_q = question.get("next")
                    if next_q == "success":
                        save_answer()
                    elif next_q:
                        current_id = next_q

            # Nếu không đến từ Entry hợp lệ (hoặc không có event)
            elif event is None:
                # fallback chuyển câu luôn
                next_q = question.get("next")
                if next_q == "success":
                    save_answer()
                elif next_q:
                    current_id = next_q
        case "number_code":
            if selected_code is None:
                next_q = question["next"]
            else:
                next_q = question["options"][selected_code]["next"]

            if next_q == "success":
                save_answer()
            else:
                current_id = next_q
                selected_code = None
        case "score":
            if selected_code is None:
                next_q = question["next"]
            else:
                next_q = question["options"][selected_code]["next"]

            if next_q == "success":
                save_answer()
            else:
                current_id = next_q
                selected_code = None
        case _:
            next_q = question.get("next")
            if next_q == "success":
                save_answer()
            elif next_q:
                current_id = next_q

    update(current_id)

    select_code(None)


def select_code(code):
    global selected_code
    selected_code = code



# Handle keypress
def handle_keypress(event):
    if current_id not in question_widgets:
        return

    q = questions[current_id]
    qtype = q["type"]
    key = event.char

    if key == "0":
        key = "10"

    if qtype == "number_code":
        if key in q["options"]:
            select_code(key)
            cache_answers()
            update(current_id)

    elif qtype == "score":
        if key in q["options"]:
            select_code(key)
            cache_answers()
            update(current_id)


# Navigation buttons
def go_up():
    global current_id
    ids = list(questions.keys())
    idx = ids.index(current_id)
    if idx > 0:
        current_id = ids[idx - 1]
        update(current_id)

def go_down():
    ids = list(questions.keys())
    idx = ids.index(current_id)
    if idx < len(ids) - 1:
        handle_enter()

SETTINGS_FILE = "data/settings.json"

def load_settings_from_file():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            settings = json.load(f)

            surveyor_id = settings.get("surveyor_id", "")
            surveyor_name = settings.get("surveyor_name", "")
            survey_month = settings.get("survey_month", "")
            form_link = settings.get("form_link", "")
            location = settings.get("location")

            return surveyor_id, surveyor_name, survey_month, form_link, location

def save_settings_to_file(surveyor_id, surveyor_name, survey_month, form_link, location):
    settings = {
        "surveyor_id": surveyor_id,
        "surveyor_name": surveyor_name,
        "survey_month": survey_month,
        "location": location,
        "form_link": form_link
    }
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)

OUTPUT_DIR = "output"

def save_answer():
    surveyor_id, surveyor_name, survey_month, form_link, location = load_settings_from_file() or ("", "", "", "")

    filename = f"{"Test"}.json"
    filepath = os.path.join(OUTPUT_DIR, filename)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output = {
    "answers": answers,
    "surveyor_id": surveyor_id,
    "surveyor_name": surveyor_name,
    "survey_month": survey_month,
    "location" : location,
    "form_link": form_link
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

def new():
    load_cache(True)
    update("s0")

def cache_answers():
    """Thu thập câu trả lời hiện tại và lưu vào file cache"""
    question = questions[current_id]
    widget = question_widgets[current_id]

    match question["type"]:
        case "text":
            values = {}
            for field_id, entry in widget["entries"].items():
                val = entry.get().strip()
                if val:
                    values[field_id] = val

            if values:
                answers[current_id] = values
            elif current_id in answers:
                del answers[current_id]  # Xóa nếu đã từng nhập rồi xoá trắng


        case "number_code":
            if selected_code in question["options"]:
                answers[current_id] = selected_code

        case "score":
            if selected_code in question["options"]:
                answers[current_id] = selected_code

        case "dropdown":
            selected = widget.get("selected")
            if selected:
                value = selected.get().strip()
                if value:
                    answers[current_id] = value
                elif current_id in answers:
                    del answers[current_id]

        case _:
            # Có thể thêm các loại khác nếu cần
            pass

    # Ghi cache ra file
    cache_file = "output/cache.json"
    os.makedirs("output", exist_ok=True)
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(answers, f, ensure_ascii=False, indent=2)

