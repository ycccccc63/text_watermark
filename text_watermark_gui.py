import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class EasyPasteWatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文字浮水印嵌入 / 擷取系統 text_watermark_gui.pytext_watermark_gui.py")
        self.root.geometry("1180x920")
        self.root.configure(bg="#F8FAFC")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview.Heading", font=("Microsoft JhengHei", 10, "bold"))
        style.configure("Treeview", font=("Microsoft JhengHei", 10), rowheight=25)

        # 建立右鍵選單
        self.create_context_menu()
        
        # 建立主介面
        self.create_widgets()

    def create_context_menu(self):
        """建立滑鼠右鍵選單（剪下、複製、貼上、全選）"""
        self.context_menu = tk.Menu(self.root, tearoff=0, font=("Microsoft JhengHei", 10))
        self.context_menu.add_command(label="剪下 (Cut)", command=lambda: self.focus_widget_event("<<Cut>>"))
        self.context_menu.add_command(label="複製 (Copy)", command=lambda: self.focus_widget_event("<<Copy>>"))
        self.context_menu.add_command(label="貼上 (Paste)", command=lambda: self.focus_widget_event("<<Paste>>"))
        self.context_menu.add_separator()
        self.context_menu.add_command(label="全選 (Select All)", command=lambda: self.focus_widget_event("<<SelectAll>>"))

    def show_context_menu(self, event):
        """顯示右鍵選單"""
        event.widget.focus_set()
        self.context_menu.tk_popup(event.x_root, event.y_root)

    def focus_widget_event(self, event_name):
        """針對當前取得焦點的元件執行剪貼簿事件"""
        try:
            focused = self.root.focus_get()
            if focused:
                focused.event_generate(event_name)
        except Exception:
            pass

    def bind_input_features(self, widget):
        """給輸入框綁定右鍵選單與快捷鍵"""
        # Windows / Linux 右鍵
        widget.bind("<Button-3>", self.show_context_menu)
        # macOS 右鍵
        widget.bind("<Button-2>", self.show_context_menu)
        widget.bind("<Control-1>", self.show_context_menu)

    def paste_from_clipboard(self, text_widget, clear_first=True):
        """按鈕專用的貼上功能：取得剪貼簿內容並貼入"""
        try:
            clipboard_text = self.root.clipboard_get()
            if clear_first:
                if isinstance(text_widget, tk.Text):
                    text_widget.delete("1.0", tk.END)
                    text_widget.insert("1.0", clipboard_text)
                elif isinstance(text_widget, tk.Entry):
                    text_widget.delete(0, tk.END)
                    text_widget.insert(0, clipboard_text)
            else:
                if isinstance(text_widget, tk.Text):
                    text_widget.insert(tk.INSERT, clipboard_text)
                elif isinstance(text_widget, tk.Entry):
                    text_widget.insert(tk.INSERT, clipboard_text)
        except Exception as e:
            messagebox.showwarning("提示", "剪貼簿中沒有可貼上的文字內容！")

    def create_widgets(self):
        # 頂部標題區
        title_frame = tk.Frame(self.root, bg="#0F172A", padx=20, pady=15)
        title_frame.pack(fill="x")
        
        lbl_title = tk.Label(title_frame, text="文字浮水印嵌入 / 擷取系統", font=("Microsoft JhengHei", 18, "bold"), fg="#FFFFFF", bg="#0F172A")
        lbl_title.pack(side="left")

        lbl_sub = tk.Label(title_frame, text="支援右鍵貼上與一鍵帶入剪貼簿", font=("Microsoft JhengHei", 10), fg="#94A3B8", bg="#0F172A")
        lbl_sub.pack(side="left", padx=15, pady=(5,0))

        # 主版面
        main_frame = tk.Frame(self.root, bg="#F8FAFC", padx=20, pady=15)
        main_frame.pack(fill="both", expand=True)

        left_frame = tk.Frame(main_frame, bg="#F8FAFC")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right_frame = tk.Frame(main_frame, bg="#F8FAFC")
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # --- 區塊 1: 輸入原始文字 ---
        sec1_header = tk.Frame(left_frame, bg="#F8FAFC")
        sec1_header.pack(fill="x")
        
        sec1_title = tk.Label(sec1_header, text="1  輸入原始文字", font=("Microsoft JhengHei", 11, "bold"), fg="#2563EB", bg="#F8FAFC")
        sec1_title.pack(side="left")

        btn_paste_orig = tk.Button(sec1_header, text="📋 一鍵貼上文字", font=("Microsoft JhengHei", 9, "bold"), bg="#DC2626", fg="white", relief="flat", command=lambda: self.paste_from_clipboard(self.txt_original))
        btn_paste_orig.pack(side="right", padx=(5, 0))

        btn_load_text = tk.Button(sec1_header, text="📂 載入文字檔", font=("Microsoft JhengHei", 9), command=self.load_text_file)
        btn_load_text.pack(side="right")
        
        self.txt_original = tk.Text(left_frame, height=8, font=("Microsoft JhengHei", 10), bd=1, relief="solid")
        self.txt_original.pack(fill="x", pady=(5, 15))
        self.bind_input_features(self.txt_original)

        # --- 區塊 2: 輸入同義詞對照表 ---
        sec2_header = tk.Frame(left_frame, bg="#F8FAFC")
        sec2_header.pack(fill="x")

        sec2_title = tk.Label(sec2_header, text="2  同義詞對照表 (詞集庫)", font=("Microsoft JhengHei", 11, "bold"), fg="#2563EB", bg="#F8FAFC")
        sec2_title.pack(side="left")

        btn_paste_dict = tk.Button(sec2_header, text="📋 一鍵貼上詞庫", font=("Microsoft JhengHei", 9, "bold"), bg="#DC2626", fg="white", relief="flat", command=lambda: self.paste_from_clipboard(self.txt_dict))
        btn_paste_dict.pack(side="right", padx=(5, 0))

        btn_load_dict = tk.Button(sec2_header, text="📂 載入詞庫檔", font=("Microsoft JhengHei", 9), command=self.load_dict_file)
        btn_load_dict.pack(side="right")

        self.txt_dict = tk.Text(left_frame, height=10, font=("Microsoft JhengHei", 10), bd=1, relief="solid")
        self.txt_dict.pack(fill="x", pady=(5, 15))
        self.bind_input_features(self.txt_dict)

        # --- 區塊 3: 設定嵌入位元 ---
        sec3_title = tk.Label(right_frame, text="+  欲嵌入位元序列 (二進位)", font=("Microsoft JhengHei", 11, "bold"), fg="#2563EB", bg="#F8FAFC")
        sec3_title.pack(anchor="w")

        bit_input_frame = tk.Frame(right_frame, bg="#F8FAFC")
        bit_input_frame.pack(fill="x", pady=(5, 10))

        tk.Label(bit_input_frame, text="位元序列：", font=("Microsoft JhengHei", 10), bg="#F8FAFC").pack(side="left")
        self.entry_bits = tk.Entry(bit_input_frame, font=("Consolas", 12, "bold"), fg="#1E40AF", bd=1, relief="solid")
        self.entry_bits.pack(side="left", fill="x", expand=True, padx=(5, 5))
        self.entry_bits.insert(0, "010111")
        self.bind_input_features(self.entry_bits)

        btn_paste_bits = tk.Button(bit_input_frame, text="📋 貼上", font=("Microsoft JhengHei", 9), command=lambda: self.paste_from_clipboard(self.entry_bits))
        btn_paste_bits.pack(side="right")

        # 表格對照
        columns = ("carrier", "bit", "selected")
        self.tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=8)
        self.tree.heading("carrier", text="原文匹配詞")
        self.tree.heading("bit", text="欲藏位元")
        self.tree.heading("selected", text="替換後詞彙")
        self.tree.column("carrier", width=110, anchor="center")
        self.tree.column("bit", width=80, anchor="center")
        self.tree.column("selected", width=110, anchor="center")
        self.tree.pack(fill="both", expand=True, pady=(0, 10))

        btn_embed = tk.Button(right_frame, text="🔒 藏入數位浮水印", font=("Microsoft JhengHei", 11, "bold"), bg="#4F46E5", fg="white", relief="flat", command=self.embed_watermark, pady=8)
        btn_embed.pack(fill="x", pady=(0, 15))

        # --- 下方區塊 4: 輸出文字 ---
        sec4_header = tk.Frame(self.root, bg="#F8FAFC")
        sec4_header.pack(fill="x", padx=20)

        sec4_title = tk.Label(sec4_header, text="3  嵌入浮水印後之輸出文字", font=("Microsoft JhengHei", 11, "bold"), fg="#2563EB", bg="#F8FAFC")
        sec4_title.pack(side="left")

        btn_copy_output = tk.Button(sec4_header, text="📄 複製輸出結果", font=("Microsoft JhengHei", 9), command=self.copy_output_to_clipboard)
        btn_copy_output.pack(side="right")

        self.txt_watermarked = tk.Text(self.root, height=4, font=("Microsoft JhengHei", 10), bd=1, relief="solid", bg="#F0FDF4")
        self.txt_watermarked.pack(fill="x", padx=20, pady=(5, 15))
        self.bind_input_features(self.txt_watermarked)

        # --- 下方區塊 5: 擷取驗證 ---
        sec5_header = tk.Frame(self.root, bg="#F8FAFC")
        sec5_header.pack(fill="x", padx=20)

        sec5_title = tk.Label(sec5_header, text="4  擷取文字浮水印", font=("Microsoft JhengHei", 11, "bold"), fg="#2563EB", bg="#F8FAFC")
        sec5_title.pack(side="left")

        btn_paste_extract = tk.Button(sec5_header, text="📋 一鍵貼上待測文字", font=("Microsoft JhengHei", 9), command=lambda: self.paste_from_clipboard(self.txt_extract_input))
        btn_paste_extract.pack(side="right")

        extract_frame = tk.Frame(self.root, bg="#F8FAFC")
        extract_frame.pack(fill="x", padx=20, pady=(5, 20))

        self.txt_extract_input = tk.Text(extract_frame, height=3, font=("Microsoft JhengHei", 10), bd=1, relief="solid")
        self.txt_extract_input.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.bind_input_features(self.txt_extract_input)

        btn_extract = tk.Button(extract_frame, text="🔍 擷取浮水印", font=("Microsoft JhengHei", 11, "bold"), bg="#0284C7", fg="white", relief="flat", command=self.extract_watermark, width=14)
        btn_extract.pack(side="left", padx=(0, 10), fill="y")

        self.lbl_extracted_result = tk.Label(extract_frame, text="——", font=("Consolas", 18, "bold"), fg="#854D0E", bg="#FEF3C7", width=14)
        self.lbl_extracted_result.pack(side="left", fill="y")

    def copy_output_to_clipboard(self):
        text = self.txt_watermarked.get("1.0", tk.END).strip()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            messagebox.showinfo("成功", "已將嵌入浮水印的文字複製到剪貼簿！")

    def load_text_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.txt_original.delete("1.0", tk.END)
                self.txt_original.insert("1.0", f.read())

    def load_dict_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.txt_dict.delete("1.0", tk.END)
                self.txt_dict.insert("1.0", f.read())

    def parse_dictionary(self):
        dict_lines = self.txt_dict.get("1.0", tk.END).strip().splitlines()
        pairs = []
        for line in dict_lines:
            line = line.strip()
            if "," in line:
                parts = line.split(",")
                if len(parts) >= 2:
                    w0, w1 = parts[0].strip(), parts[1].strip()
                    if w0 and w1:
                        pairs.append((w0, w1))
        return pairs

    def parse_bits(self):
        raw_bits = self.entry_bits.get().strip().replace(" ", "")
        return [int(b) for b in raw_bits if b in ('0', '1')]

    def embed_watermark(self):
        original_text = self.txt_original.get("1.0", tk.END).strip()
        pairs = self.parse_dictionary()
        bits = self.parse_bits()

        if not original_text or not pairs or not bits:
            messagebox.showwarning("警告", "請確保原始文字、同義詞對照表與位元序列皆有輸入內容！")
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        watermarked_text = original_text
        bit_idx = 0

        for w0, w1 in pairs:
            if bit_idx >= len(bits):
                break
            target_bit = bits[bit_idx]
            chosen_word = w0 if target_bit == 0 else w1

            if w0 in watermarked_text:
                watermarked_text = watermarked_text.replace(w0, chosen_word, 1)
                self.tree.insert("", "end", values=(w0, target_bit, chosen_word))
                bit_idx += 1
            elif w1 in watermarked_text:
                watermarked_text = watermarked_text.replace(w1, chosen_word, 1)
                self.tree.insert("", "end", values=(w1, target_bit, chosen_word))
                bit_idx += 1

        self.txt_watermarked.delete("1.0", tk.END)
        self.txt_watermarked.insert("1.0", watermarked_text)
        self.txt_extract_input.delete("1.0", tk.END)
        self.txt_extract_input.insert("1.0", watermarked_text)

    def extract_watermark(self):
        text = self.txt_extract_input.get("1.0", tk.END).strip()
        pairs = self.parse_dictionary()
        extracted_bits = []

        for w0, w1 in pairs:
            pos_w0 = text.find(w0) if w0 in text else -1
            pos_w1 = text.find(w1) if w1 in text else -1

            if pos_w0 == -1 and pos_w1 == -1:
                continue
            if pos_w0 != -1 and (pos_w1 == -1 or pos_w0 < pos_w1):
                extracted_bits.append("0")
            elif pos_w1 != -1 and (pos_w0 == -1 or pos_w1 < pos_w0):
                extracted_bits.append("1")

        self.lbl_extracted_result.config(text="".join(extracted_bits) if extracted_bits else "未發現")

if __name__ == "__main__":
    root = tk.Tk()
    app = EasyPasteWatermarkApp(root)
    root.mainloop()