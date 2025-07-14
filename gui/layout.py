# gui/layout.py
import tkinter as tk
from tkinter import ttk
import json
import logic.handler as h

questions_frame_size = 0.8  # Tỷ lệ chiều rộng của khung câu hỏi
controls_frame_size = 1 - questions_frame_size


def setup_layout(root, window_width, window_height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.resizable(width=False, height=True)
    root.minsize(window_width, window_height)
    root.maxsize(screen_width, int(screen_height / 1.0895))

    main_frame = tk.Frame(root)
    main_frame.pack(fill="both", expand=True)

    layout = tk.Frame(main_frame)
    layout.pack(fill="both", expand=True)

    left_wrapper = tk.Frame(layout, width=int(window_width * questions_frame_size))
    left_wrapper.pack(side="left", fill="both", expand=True)

    tk.Label(left_wrapper, text="Câu hỏi", font=("Arial", 12, "bold")).pack(pady=(10, 10), fill="x")
    tk.Frame(left_wrapper, height=1, bg="#cccccc").pack(fill="x", padx=(0, 16), pady=(0, 5))

    canvas_frame = tk.Frame(left_wrapper)
    canvas_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(canvas_frame, highlightthickness=0, name="canvas")
    scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    left_frame = tk.Frame(canvas, name="scrollable_frame")
    canvas_window = canvas.create_window((0, 0), window=left_frame, anchor="nw")

    def on_canvas_resize(event):
        canvas.itemconfig(canvas_window, width=event.width)
    canvas.bind("<Configure>", on_canvas_resize)

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    left_frame.bind("<Configure>", on_configure)

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    
    right_frame = tk.Frame(layout, width=int(window_width * controls_frame_size))
    right_frame.pack(side="right", fill="y")

    # Right controls
    tk.Label(right_frame, text="Điều khiển", font=("Arial", 12, "bold")).pack(pady=(10, 10), padx=10)
    tk.Frame(right_frame, height=1, bg="#cccccc").pack(fill="x", pady=(0, 5))

    # Tạo frame phụ để chứa 2 nút
    enter_frame = tk.Frame(right_frame)
    enter_frame.pack(pady=(5, 10), fill="x", padx=1)

    # Nút bên trái: "New"
    btn_next = tk.Button(enter_frame, text="Mở", command=h.new)
    btn_next.grid(row=0, column=0, sticky="ew", padx=(0, 5))

    # Nút bên phải: "Enter"
    btn_enter = tk.Button(enter_frame, text="Mới", command=h.new)
    btn_enter.grid(row=0, column=1, sticky="ew")

    # Đặt tỉ lệ cột co giãn đều
    enter_frame.grid_columnconfigure(0, weight=1)
    enter_frame.grid_columnconfigure(1, weight=1)

    btn_back = tk.Button(right_frame, text="⬆", command=h.go_up)
    btn_back.pack(pady=1, fill="x", padx=1)

    btn_next = tk.Button(right_frame, text="⬇", command=h.go_down)
    btn_next.pack(pady=1, fill="x", padx=1)

    btn_save = tk.Button(right_frame, text="Lưu", command=h.save_answer)
    btn_save.pack(pady=10, fill="x", padx=1)

    # Settings
    tk.Frame(right_frame, height=1, bg="#cccccc").pack(fill="x", pady=(0, 5))
    tk.Label(right_frame, text="Cài đặt", font=("Arial", 11, "bold")).pack(pady=(5, 5), anchor="w", padx=10)
    
    surveyor_id, surveyor_name, survey_month, form_link, location = h.load_settings_from_file() or ("", "", "", "", "")

    def on_change_settings(*args):
        h.save_settings_to_file(
            var_id.get().strip(),
            var_name.get().strip(),
            var_month.get().strip(),
            var_link.get().strip(),
            var_location.get().strip()
        )


    tk.Label(right_frame, text="Mã số PVV:").pack(anchor="w", padx=10)
    var_id = tk.StringVar(value=surveyor_id)
    var_id.trace_add("write", on_change_settings)
    entry_id = tk.Entry(right_frame, textvariable=var_id)
    entry_id.pack(fill="x", padx=10)

    tk.Label(right_frame, text="Họ tên PVV:").pack(anchor="w", padx=10)
    var_name = tk.StringVar(value=surveyor_name)
    var_name.trace_add("write", on_change_settings)
    entry_name = tk.Entry(right_frame, textvariable=var_name)
    entry_name.pack(fill="x", padx=10)

    tk.Label(right_frame, text="Địa điểm thực hiện:").pack(anchor="w", padx=10)

    # Danh sách địa điểm có thể chọn
    location_options = ["CATI", "FIELD HCM", "HA NOI", "CAN THO", "VINH", "BMT", "DANANG", "HAIPHONG"]

    var_location = tk.StringVar(value=location)
    var_location.trace_add("write", on_change_settings)

    combo_location = ttk.Combobox(
        right_frame, 
        textvariable=var_location, 
        values=location_options,
        state="readonly"  # Chỉ chọn, không cho nhập tay
    )
    combo_location.pack(fill="x", padx=10)

    tk.Label(right_frame, text="Mã tháng:").pack(anchor="w", padx=10)
    var_month = tk.StringVar(value=survey_month)
    var_month.trace_add("write", on_change_settings)
    entry_month = tk.Entry(right_frame, textvariable=var_month)
    entry_month.pack(fill="x", padx=10)

    tk.Label(right_frame, text="Link biểu mẫu:").pack(anchor="w", padx=10)
    var_link = tk.StringVar(value=form_link)
    var_link.trace_add("write", on_change_settings)
    entry_link = tk.Entry(right_frame, textvariable=var_link)
    entry_link.pack(fill="x", padx=10)

        # --- Bottom status area ---
    bottom_frame = tk.Frame(root, height=30, bg="#f0f0f0")
    bottom_frame.pack(side="bottom", fill="x")

    # Left side: progress bar

    progress_var = tk.DoubleVar(value=0)
    progress_bar = ttk.Progressbar(bottom_frame, variable=progress_var, maximum=100)
    progress_bar.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=5)

    return left_frame, right_frame, canvas, progress_var
