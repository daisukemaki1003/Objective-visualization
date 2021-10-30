import json
import os.path
import tkinter as tk
import tkinter.simpledialog as simpledialog
import tkinter.ttk as ttk
from functools import partial


FRAME_WIDTH = 700


def run_gui():
	main_view = tk.Tk()
	main_view.title('Objective-visualization')
	main_view.geometry(str(FRAME_WIDTH) + "x560")
	
	# -------------- Style -------------- #
	style = ttk.Style()
	style.configure("example.TNotebook.Tab",
	                background="lightyellow",
	                foreground="black")
	
	style.map(
		"example.TNotebook.Tab",
		background={('active', 'orange'),
		            ('disabled', 'black'),
		            ('selected', 'lightgreen')},
		foreground=[('active', 'gray'),
		            ('disabled', 'gray'),
		            ('selected', 'black')])
	# -------------- Style -------------- #
	
	# 画面切り替え
	nb = ttk.Notebook(main_view, style="example.TNotebook")
	
	tab1 = tk.Frame(nb)  # 画面1
	tab2 = tk.Frame(nb)  # 画面2
	
	nb.add(tab1, text="目標の設定", padding=10)
	nb.add(tab2, text="過去の目標", padding=10)
	nb.pack(expand=1, fill="both")
	
	PurposeCreation(tab1)
	tab1_main(tab2)
	main_view.mainloop()


def tab1_main(tab1):
	# 文字を表示する。
	param_name = tk.Label(tab1, text="タブ1の内容")
	param_name.place(x=10, y=10)
	return 0


class PurposeCreation(tk.Frame):
	def __init__(self, master):
		super().__init__(master)
		# include path
		json_open = open('../settings/setting.json', 'r')
		json_data = json.load(json_open)
		item_name_file = os.path.join(json_data["template_dir"], json_data["template"]["item_names"])
		
		# 項目名のテンプレート読み込み
		json_open = open(item_name_file, 'r')
		self.temporarily_json = json.load(json_open)
		
		# 保存するjson path
		self.json_path = os.path.join(json_data['data_dir'], json_data['accumulated_file'] + '.json')
		self.choosing = 'Title'
		
		self.create_base_obj()
		first_key = list(self.temporarily_json.keys())[1]
		self.create_text_area(first_key)
	
	def create_base_obj(self):
		left_frame = tk.Frame(self.master)
		left_frame.pack(side='left')
		
		left_frame_label = tk.Frame(left_frame)
		left_frame_label.pack(side='top')
		
		options_title = dict(bg="white", bd=0, width=20, height=20,
		                     listvariable=tk.StringVar(value=list(self.temporarily_json.keys())), selectmode="single")
		self.listbox = tk.Listbox(left_frame_label, options_title)
		self.listbox.pack(side='left')
		self.listbox.bind('<<ListboxSelect>>', self._selected)
		
		scrollbar = tk.Scrollbar(left_frame_label, orient=tk.VERTICAL, command=self.listbox.yview)
		self.listbox['yscrollcommand'] = scrollbar.set
		scrollbar.pack(side='left')
		
		# add btn
		f = tk.Frame(left_frame)
		f.pack(side='bottom')
		self.add = tk.Button(f, text='+', command=lambda: self._add_listbox())
		self.delete = tk.Button(f, text='-', command=lambda: self._delete_selected_listbox())
		self.add.pack(side='left')
		self.delete.pack(side='left')
	
	def create_text_area(self, label):
		self.right_frame = tk.Frame(self.master)
		self.right_frame.pack(side='right')
		self.textarea = tk.Text(self.right_frame)
		self.textarea.insert('1.0', self.temporarily_json[label])
		self.textarea.pack(side='top')
		
		btn = tk.Button(self.right_frame, text='save', command=partial(self._save_data))
		btn.pack(side='top')
		if self.listbox.curselection():
			self.choosing = self.listbox.get(self.listbox.curselection())
	
	def _add_listbox(self):
		inputdata = simpledialog.askstring("Input Box", "値を入力してください", )
		self.listbox.insert(tk.END, inputdata)
		self.temporarily_json[inputdata] = ''
	
	def _delete_selected_listbox(self):
		selectedIndex = tk.ACTIVE
		self.listbox.delete(selectedIndex)
		self.temporarily_json.pop(self.choosing)  # delete json key
	
	def _selected(self, event):
		select_item_index = self.listbox.curselection()
		if select_item_index:
			# save json
			self.temporarily_json[self.choosing] = self.textarea.get('1.0', 'end -1c')
			self.right_frame.destroy()
			self.create_text_area(self.listbox.get(select_item_index))
	
	def _save_data(self):
		self.temporarily_json[self.choosing] = self.textarea.get('1.0', 'end -1c')
		print(json.dumps(self.temporarily_json, ensure_ascii=False, indent=2))
		json_data = dict()
		json_data['Title'] = self.temporarily_json['Title']
		json_data['Do_num'] = '01'
		json_data['Contents'] = [{"content_title": k, "content_value": v} for k, v in self.temporarily_json.items() if
		                         k != 'Title']
		
		# 辞書オブジェクトをJSONファイルへ出力
		with open(self.json_path, mode='w', encoding='utf-8') as file:
			json.dump(json_data, file, ensure_ascii=False, indent=2)
