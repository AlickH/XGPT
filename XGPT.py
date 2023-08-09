from tkinter import *
from tkinter import ttk
import json
import threading
import subprocess
import time, os, sys
import requests.exceptions
from xabcai_gpt import xabcai_gpt
import tiktoken

def get_macos_theme():
    applescript = "tell application \"System Events\" to tell appearance preferences to get dark mode"
    out = subprocess.run(['osascript', '-e', applescript], capture_output=True, text=True).stdout.strip()
    if out == "true":
        result = "Dark"
        return result

last_theme = get_macos_theme()
def check_theme_periodically():
    global last_theme
    while True:
        current_theme = get_macos_theme()
        if current_theme != last_theme:
            set_button_colors(current_theme)
            set_background_colors(current_theme)
            last_theme = current_theme
        time.sleep(1)

history_file = os.path.expanduser("~/.GetGPT/history.json")
record_file = os.path.expanduser("~/.GetGPT/record.json")
getgpt_folder = os.path.expanduser("~/.GetGPT")
window_position = os.path.expanduser("~/.GetGPT/window_position.txt")

if not os.path.isdir(getgpt_folder):
    os.makedirs(getgpt_folder)
else:
    pass
    
if not os.path.isfile(history_file):
    with open(history_file, "w") as file:
        json.dump([], file)
if not os.path.isfile(record_file):
    with open(record_file, "w") as file:
        json.dump([], file)
if not os.path.isfile(record_file):
    with open(window_position, "w") as file:
        file.write("")
else:
    pass

history = []
record = []
model = "gpt-3.5-turbo-16k"

def token_len(model, history):
    encoding = tiktoken. encoding_for_model(model)
    codelist = encoding.encode(str(history))
    token_size = len(codelist)
    return token_size

def on_text_change(event):
    text = input_box.get("1.0", "end-1c")
    input_token_size = token_len(model, text)
    prompt_token_size = token_len(model, '{"role": "user", "content": ""}')
    total_token_size = int(previous_history_token_size) + int(input_token_size) + int(prompt_token_size)
    label_var.set(model + "\nToken: " + str(total_token_size))
    return total_token_size

try:
    with open(history_file, "r") as file:
        previous_history = json.load(file)
    with open(record_file, "r") as file:
        previous_record = json.load(file)
except FileNotFoundError:
    pass
    
previous_history_token_size = token_len(model, previous_history)

def reload_record():
    with open(record_file, "r") as file:
        load_record = json.load(file)
        display_record(conversation, load_record)

def copy_text(event):
    event.widget.event_generate("<<Copy>>")
    
def set_no_border(widget):
    widget.config(highlightthickness=0)
    
def on_entry_click(event):
    result = get_macos_theme()
    if input_box.get("1.0", END).strip() == "Write a message...":
        input_box.delete(1.0, END)
        if result == "Dark":
            input_box.configure(fg="#AFA8A0")
        else:
            input_box.configure(fg="#293140")
        
def on_entry_leave(event):
    if input_box.get("1.0", END).strip() == "":
        input_box.insert(1.0, "Write a message...")
        input_box.configure(fg="gray")

def set_background_colors(theme):
    if theme == "Dark":
        conversation.configure(bg="#161616")
        conversation.tag_config("user", foreground="orange", background="#151718", font=("PingFang SC", 16, "bold"), lmargin1=20)
        conversation.tag_config("assistant", foreground="green", background="#161616",font=("PingFang SC", 16, "bold"), lmargin1=20)
        conversation.tag_config("ask", font=("PingFang SC", 14),  foreground="#AFA8A0", background="#151718", lmargin1=60, lmargin2=60, rmargin=40)
        conversation.tag_config("answer", font=("PingFang SC", 14),  foreground="#AFA8A0", background="#161616", lmargin1=60, lmargin2=60, rmargin=40)
        conversation.tag_config("ask_margin", font=("PingFang SC", 5), background="#151718")
        conversation.tag_config("answer_margin", font=("PingFang SC", 5), background="#161616")
        conversation.tag_config("seperator", font=("PingFang SC", 1), background="#1E1E1D")
        conversation.tag_configure("highlight", background="#3D5049")
        input_box.configure(bg="#151718")
    else:
        conversation.configure(bg="#F5F5F7")
        conversation.tag_config("user", foreground="orange", background="#FFFFFF", font=("PingFang SC", 16, "bold"),  lmargin1=20)
        conversation.tag_config("assistant", foreground="green", background="#F5F5F7", font=("PingFang SC", 16, "bold"),  lmargin1=20)
        conversation.tag_config("ask", font=("PingFang SC", 14),  foreground="#293140", background="#FFFFFF", lmargin1=60, lmargin2=60, rmargin=40)
        conversation.tag_config("answer", font=("PingFang SC", 14),  foreground="#293140", background="#F5F5F7", lmargin1=60, lmargin2=60, rmargin=40)
        conversation.tag_config("ask_margin", font=("PingFang SC", 5), background="#FFFFFF")
        conversation.tag_config("answer_margin", font=("PingFang SC", 5), background="#F5F5F7")
        conversation.tag_config("seperator", font=("PingFang SC", 1), background="#D7D6D8")
        conversation.tag_configure("highlight", background="#6DB2DE")
        input_box.configure(bg="#FFFFFF")
        
def set_button_colors(theme):
    if theme == "Dark":
        button_submit.configure(style="Dark.TButton")
        button_new.configure(style="Dark.TButton")
    else:
        button_submit.configure(style="Light.TButton")
        button_new.configure(style="Light.TButton")

window = Tk()
window.title("X-GPT")
window.wm_minsize(450, 600)
window.wm_maxsize(800, 1000)

frame = Frame(window)
frame.pack(fill="both", expand=True)

def on_mouse_down(event):
    global prev_y
    prev_y = event.y
    
def on_mouse_drag(event):
    global prev_y
    try:
        delta_y = event.y - prev_y
    except AttributeError:
        return
    conversation.yview_scroll(int(-1*(delta_y/120)), "units")
    prev_y = event.y

# 创建滚动文本框，用于显示对话内容
scrollbar = ttk.Scrollbar(frame, orient=VERTICAL)
scrollbar.pack(side=RIGHT, fill=Y, padx=0, pady=0)
conversation = Text(frame, yscrollcommand=scrollbar.set, width=50, height=30, font=("PingFang SC", 14))
conversation.pack(side=LEFT, fill="both", expand=True, padx=0, pady=0)
conversation.configure(state="disabled")
conversation.bind("<Command-c>", copy_text)
set_no_border(conversation)
scrollbar.config(command=conversation.yview)
conversation.bind("<Button-1>", on_mouse_down)
conversation.bind("<B1-Motion>", on_mouse_drag)
    
label_frame = ttk.Frame(window)
label_frame.pack(fill=X, expand=False)
user_avatar = ttk.Label(label_frame, text="🙋    User", foreground="orange", font=("PingFang SC", 16, "bold"), anchor="w")
user_avatar.pack(side=LEFT,padx=(20,0), pady=(20,5), fill=X, expand=True)
label_var = StringVar(value=str(model) + "\nToken: " + str(previous_history_token_size))
token_label = ttk.Label(label_frame, textvariable=label_var, foreground="gray", font=("PingFang SC", 10, "bold"), anchor="e", justify="right", wraplength=100)
token_label.pack(side=RIGHT,padx=(0,60), pady=(25,0), fill=X, expand=True)

# 创建输入框
input_box = Text(window, height=3, font=("PingFang SC", 14))
input_box.pack(fill="both", expand=False, padx=60, pady=(0, 10))
input_box.focus_set()
input_box.insert(1.0, "Write a message...")
input_box.bind('<FocusIn>', on_entry_click)
input_box.bind('<FocusOut>', on_entry_leave)
input_box.configure(fg="gray", font=("PingFang SC", 14))
set_no_border(input_box)
set_background_colors(last_theme)
input_box.bind("<KeyRelease>", on_text_change)

def highlight_selected_text(event):
    conversation.tag_remove("highlight", "1.0", END)
    conversation.tag_add("highlight", "sel.first", "sel.last")
conversation.bind("<<Selection>>", highlight_selected_text)

window_width = conversation.winfo_reqwidth() + 20
window_height = conversation.winfo_reqheight() + input_box.winfo_reqheight() + 20
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width - window_width)
y = 0
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

def display_record(conversation, record):
    conversation.configure(state="normal")
    conversation.delete('1.0', END)
    for item in record:
        role = item["role"]
        content = item["content"]
        if role == "user":
            conversation.insert(END, "\n🙋    User\n", "user")
            conversation.insert(END, "\n", "ask_margin")
            conversation.insert(END, f"{content}\n\n".lstrip(), "ask")
            conversation.insert(END, "\n", "seperator")
        elif role == "assistant":
            conversation.insert(END, "\n🧑‍⚕️    Assistant\n", "assistant")
            conversation.insert(END, "\n", "answer_margin")
            conversation.insert(END, f"{content}\n\n".lstrip(), "answer")
            conversation.insert(END, "\n", "seperator")
    conversation.config(state="disable")
    conversation.see(END)
    
reload_record()

def send_message():
    user_input = input_box.get("1.0", "end-1c").strip()
    if user_input == "" or user_input == "Write a message...":
        pass
    else:
        global history, record
        history = previous_history if isinstance(previous_history, list) else []
        if history and history[-1]['role'] == 'user' and history[-1]['content'] == user_input:
            history.pop()
        history.append({"role": "user", "content": user_input})
        
        
        record = previous_record if isinstance(previous_record, list) else []
        record.append({"role": "user", "content": user_input})
        
    
        if user_input:
            conversation.configure(state="normal")
            conversation.insert(END, "\n🙋    User\n", "user")
            conversation.insert(END, "\n", "ask_margin")
            conversation.insert(END, user_input.lstrip() + "\n\n", "ask")
            conversation.insert(END, "\n", "seperator")
            conversation.see(END)
            input_box.delete("1.0", END)
            window.update()
            
            conversation.insert(END, "\n🧑‍⚕️    Assistant\n", "assistant")
            conversation.insert(END, "\n", "answer_margin")
            window.update()
            result_event = threading.Event()
            result = threading.Thread(target=generate_response, args=(model, history, result_event))
            result.start()
            window.after(100, check_result, result, result_event)

style = ttk.Style()
style.configure("Dark.TButton", foreground="lightgray", background="brown")
style.configure("Light.TButton", foreground="black", background="white")

button_frame = Frame(window)
button_frame.pack()

def option_selected(selection):
    print("选中的选项是:", selection)

button_new = ttk.Button(button_frame, text="New Chat", command="")
button_new.configure(width=8) 
button_new.pack(side=LEFT, padx=(20,20), pady=(0,10))

button_submit = ttk.Button(button_frame, text="Save & Submit", command=send_message)
button_submit.configure(width=10) 
button_submit.pack(side=LEFT, padx=10, pady=(0,10))

selected_option = StringVar()
option_menu = ttk.OptionMenu(button_frame, selected_option, *[ "Archive", "选项1", "选项2", "选项3"], command=option_selected)
option_menu.config(width=8)
option_menu.pack(side=RIGHT, padx=(20,20), pady=(0,10))
set_button_colors(last_theme)

# 根据组件尺寸计算窗口大小
def resize_window(event):
    window_height = window.winfo_reqheight()
    input_box_height = input_box.winfo_reqheight()
    conversation.config(height= (window_height - input_box_height) // 30)
window.bind("<Configure>", resize_window)

# 处理用户按键事件
def handle_keypress(event):
    if event.keysym == "Return" and event.state == 0x0004:  # Command/Windows key + Enter
        send_message()

# 使用 ChatGPT 生成助手回复
def generate_response(model, user_input, result_event):
    global history, record
    result = ""
    try:
        response = xabcai_gpt(model, user_input)
        for item in response.iter_lines():
            if item:
                output = item.decode('utf-8')
                for char in output:
                    animate_output(char)
                    time.sleep(0.02)
                animate_output("\n")
                result += output + "\n"
    except requests.exceptions.ConnectionError:
        prompt = "我没有接收到你的问题哦，请检查你的网络连接。"
        for char in prompt:
            animate_output(char)
        history.pop(-1)
        record.pop(-1)
        time.sleep(2)
        reload_record()
        pass
    except (requests.exceptions.HTTPError, IndexError):
        prompt = "链接未响应，请换一个频道。"
        for char in prompt:
            animate_output(char)
        history.pop(-1)
        record.pop(-1)
        time.sleep(2)
        reload_record()
        pass
        time.sleep(0.05)
    conversation.insert(END, "\n", "answer")
    conversation.insert(END, "\n", "seperator")
    conversation.config(state="disable")
    conversation.see(END)
    result_event.set()
    if result == "":
        pass
    else:
        add_to_context({"role": "assistant", "content": result.rstrip("\n")})
        save_history(history)
        record.append({"role": "assistant", "content": result.rstrip("\n")})
        save_record(record)

def add_to_context(message):
    history.append(message)
    if len(history) > 20:
        for _ in range(2):
            if history:
                history.pop(0)

def animate_output(text):
    conversation.insert(END, text, "answer")
    conversation.see(END)
    window.update_idletasks()
    
def check_result(result_thread, result_event):
    if result_event.is_set() and result_thread.is_alive():
        window.after(100, check_result, result_thread, result_event)
    elif result_event.is_set() and not result_thread.is_alive():
        save_history(history)

def save_history(history):
    with open(history_file, "w") as file:
        json.dump(history, file, ensure_ascii=False)

def save_record(record):
    with open(record_file, "w") as file:
        json.dump(record, file, ensure_ascii=False)

# 绑定按键事件和发送按钮事件
input_box.bind("<KeyPress>", handle_keypress)
window.bind("<Command-Return>", lambda event: send_message())

#conversation.config(padx=10, pady=10)
input_box.config(padx=10, pady=10)


theme_check_thread = threading.Thread(target=check_theme_periodically)
#theme_check_thread = threading.Thread(target=darkdetect.listener, args=(check_theme_periodically, ))
theme_check_thread.daemon = True  # 设置线程为后台线程
theme_check_thread.start()

#窗口关闭不退出和重新打开
def on_closing(event=None):
    with open(window_position, "w") as file:
        file.write(window.geometry())
    window.withdraw()
def on_dock_icon_click():
    window.deiconify()
    with open(window_position, "r") as file:
            geometry = file.read()
            window.geometry(geometry)
window.protocol("WM_DELETE_WINDOW", on_closing)
window.createcommand('tk::mac::ReopenApplication', on_dock_icon_click)

# 运行主循环
window.mainloop()