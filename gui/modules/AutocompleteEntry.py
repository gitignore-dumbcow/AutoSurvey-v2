import unicodedata
from unidecode import unidecode
import tkinter as tk

def remove_accents(input_str):
    # Loại bỏ dấu tiếng Việt
    nfkd = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)]).lower()

class AutocompleteEntry(tk.Entry):
    def __init__(self, master, completion_list, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._completion_list = completion_list
        self._normalized_list = [(item, unidecode(item.lower())) for item in completion_list]

        self.var = self["textvariable"] = kwargs.get("textvariable", tk.StringVar())
        self.var.trace_add("write", self.show_suggestions)

        self.popup = None
        self.listbox = None
        self.bind("<Return>", self.select_first_suggestion)
        self.bind("<FocusOut>", lambda e: self.hide_suggestions())

    def show_suggestions(self, *_):
        typed = unidecode(self.var.get().lower())
        matches = [orig for orig, norm in self._normalized_list if typed in norm]

        if matches:
            if not self.popup:
                self.popup = tk.Toplevel(self)
                self.popup.wm_overrideredirect(True)
                self.popup.attributes('-topmost', True)

                x = self.winfo_rootx()
                y = self.winfo_rooty() + self.winfo_height()
                self.popup.geometry(f"+{x}+{y}")

                self.listbox = tk.Listbox(self.popup)
                self.listbox.pack()

            self.listbox.delete(0, tk.END)
            for item in matches:
                self.listbox.insert(tk.END, item)

            # 🔸 Cập nhật lại chiều cao theo số lượng gợi ý
            self.listbox.configure(height=min(10, len(matches)),width=50)
        else:
            self.hide_suggestions()

    def select_first_suggestion(self, event=None):
        if self.popup and self.listbox.size() > 0:
            self.var.set(self.listbox.get(0))
        self.hide_suggestions()
        self.icursor(tk.END)

    def hide_suggestions(self):
        if self.popup:
            self.popup.destroy()
            self.popup = None
            self.listbox = None
