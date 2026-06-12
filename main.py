import pynput
import pyautogui
import tkinter as tk
from tkinter import colorchooser
import math

# 初始化全局变量
pos1 = (0, 0)
pos2 = (0, 0)
scale_factor = 100
transparent_mode = False
text_color = "black"
root = None

def on_press(key):
    global pos1, pos2, transparent_mode
    try:
        if key == pynput.keyboard.KeyCode(char='1'):
            x, y = pyautogui.position()
            pos1 = (x, y)
        elif key == pynput.keyboard.KeyCode(char='2'):
            x, y = pyautogui.position()
            pos2 = (x, y)
        elif key == pynput.keyboard.Key.f12:
            transparent_mode = not transparent_mode
            toggle_transparent_mode()
    except AttributeError:
        pass

def toggle_transparent_mode():
    global root, scale_frame, color_btn
    transparent_color = '#000001'
    default_bg = 'SystemButtonFace'

    if transparent_mode:
        root.overrideredirect(True)
        scale_frame.pack_forget()
        color_btn.pack_forget()
        root.configure(bg=transparent_color)
        root.attributes('-transparentcolor', transparent_color)
    else:
        root.overrideredirect(False)
        root.title("坐标距离计算器（带缩放+透明模式）")
        scale_frame.pack(pady=5, padx=10, fill=tk.X)
        color_btn.pack(pady=5)
        root.configure(bg=default_bg)
        root.attributes('-transparentcolor', '')

def update_scale_factor(*args):
    global scale_factor
    try:
        input_value = entry_var.get().strip()
        if input_value:
            new_factor = float(input_value)
            scale_factor = new_factor if new_factor != 0 else 100
    except ValueError:
        scale_factor = 100

def choose_text_color():
    global text_color
    selected_color = colorchooser.askcolor(title="选择文字颜色")[1]
    if selected_color:
        text_color = selected_color

def calculate_euclidean_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    raw_distance = math.hypot(x1 - x2, y1 - y2)
    scaled_distance = (raw_distance / scale_factor) * 100
    return round(scaled_distance, 2)

def update_ui():
    distance = calculate_euclidean_distance(pos1, pos2)

    if transparent_mode:
        pos1_label.config(
            text=f"pos1坐标：{pos1}",
            fg=text_color,
            bg='#000001'
        )
        pos2_label.config(
            text=f"pos2坐标：{pos2}",
            fg=text_color,
            bg='#000001'
        )
        distance_label.config(
            text=f"换算后距离：{distance}",
            fg=text_color,
            bg='#000001'
        )
    else:
        pos1_label.config(
            text=f"pos1坐标：{pos1}",
            fg=text_color,
            bg='SystemButtonFace'
        )
        pos2_label.config(
            text=f"pos2坐标：{pos2}",
            fg=text_color,
            bg='SystemButtonFace'
        )
        distance_label.config(
            text=f"换算后距离：{distance}",
            fg=text_color,
            bg='SystemButtonFace'
        )

    scale_label.config(text=f"当前缩放系数：{scale_factor:.1f}")
    root.after(100, update_ui)

# 初始化UI
root = tk.Tk()
root.title("坐标距离计算器（带缩放+透明模式）")
root.attributes('-topmost', True)
window_width = 350
window_height = 220
screen_width, screen_height = pyautogui.size()
root.geometry(f"{window_width}x{window_height}+{screen_width - 350}+{100}")

scale_frame = tk.Frame(root)
scale_frame.pack(pady=5, padx=10, fill=tk.X)

scale_label_title = tk.Label(scale_frame, text="缩放基准值：", font=("Arial", 10))
scale_label_title.pack(side=tk.LEFT)

entry_var = tk.StringVar(value=str(scale_factor))
entry_var.trace("w", update_scale_factor)
scale_entry = tk.Entry(scale_frame, textvariable=entry_var, width=10, font=("Arial", 10))
scale_entry.pack(side=tk.LEFT, padx=5)

scale_label = tk.Label(scale_frame, text=f"当前缩放系数：{scale_factor:.1f}", font=("Arial", 10))
scale_label.pack(side=tk.LEFT)

color_btn = tk.Button(root, text="选择文字颜色", command=choose_text_color)
color_btn.pack(pady=5)

pos1_label = tk.Label(root, font=("Arial", 10), text=f"pos1坐标：{pos1}", fg=text_color)
pos1_label.pack(pady=3)

pos2_label = tk.Label(root, font=("Arial", 10), text=f"pos2坐标：{pos2}", fg=text_color)
pos2_label.pack(pady=3)

distance_label = tk.Label(root, font=("Arial", 12, "bold"), text=f"换算后距离：0.00", fg=text_color)
distance_label.pack(pady=10)

update_ui()

if __name__ == '__main__':
    keyboard_listener = pynput.keyboard.Listener(on_press=on_press)
    keyboard_listener.start()
    root.mainloop()
    keyboard_listener.stop()
