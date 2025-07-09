    #     score_frame = tk.Frame(frame_q, bg=frame_q["bg"])
            #     score_frame.pack(fill="x", pady=4)

            #     code_cols = {}
            #     code_labels = {}
            #     for code, opt in q["options"].items():
            #         col = tk.Frame(score_frame, highlightthickness=1, bg="#f0f0f0", pady=0)
            #         col.pack(side="left", padx=2)

            #         lbl_code = tk.Label(col, text=code, width=5, relief="solid", borderwidth=1)
            #         lbl_code.pack()

            #         # Only keyboard control; no mouse clicks
            #         # but still allow focus highlight:
            #         col.bind("<FocusIn>", lambda e, qid=qid, c=code: select_code(qid, c))
            #         col.configure(takefocus=True)

            #         code_cols[code] = col
            #         code_labels[code] = {"code": lbl_code, "text": lbl_text}
            #         widget_info["labels"].extend([lbl_code, lbl_text])

            #     widget_info["code_cols"] = code_cols
            #     widget_info["code_labels"] = code_labels
