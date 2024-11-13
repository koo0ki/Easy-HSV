import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from config import BANNER, COLORS, VALID_EXTENSIONS, WINDOW_NAME

def print_colored_banner():
    try:
        print(BANNER)
    except:
        pass

class HSVApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Easy HSV")
        self.root.geometry("1200x800")
        
        self.control_frame = ttk.Frame(root, padding="10")
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.image_frame = ttk.Frame(root)
        self.image_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        
        ttk.Label(self.control_frame, text="Select Image:", font=('Arial', 12, 'bold')).pack(pady=5)
        self.image_listbox = tk.Listbox(self.control_frame, width=30, height=10)
        self.image_listbox.pack(pady=5)
        self.image_listbox.bind('<<ListboxSelect>>', self.on_select_image)
        
        ttk.Label(self.control_frame, text="HSV Controls:", font=('Arial', 12, 'bold')).pack(pady=10)
        
        self.hsv_sliders = {}
        for name, max_val in [('H min', 180), ('S min', 255), ('V min', 255),
                            ('H max', 180), ('S max', 255), ('V max', 255)]:
            frame = ttk.Frame(self.control_frame)
            frame.pack(fill=tk.X, pady=2)
            ttk.Label(frame, text=f"{name}:").pack(side=tk.LEFT)
            var = tk.IntVar(value=0 if 'min' in name else max_val)
            slider = ttk.Scale(frame, from_=0, to=max_val, orient=tk.HORIZONTAL, 
                             variable=var, command=self.update_image)
            slider.pack(side=tk.RIGHT, fill=tk.X, expand=True)
            self.hsv_sliders[name] = var
        
        self.canvas = tk.Canvas(self.image_frame)
        self.canvas.pack(expand=True, fill=tk.BOTH)
        
        self.load_images()
        self.current_image = None
        self.photo = None
        
    def load_images(self):
        assets_folder = os.path.join(os.path.dirname(__file__), "assets")
        self.image_files = [f for f in os.listdir(assets_folder) 
                          if f.lower().endswith(VALID_EXTENSIONS)]
        
        for image in self.image_files:
            self.image_listbox.insert(tk.END, image)
            
        if not self.image_files:
            messagebox.showerror("Error", "No images found in assets folder!")
            
    def on_select_image(self, event):
        selection = self.image_listbox.curselection()
        if selection:
            image_name = self.image_files[selection[0]]
            self.current_image = cv2.imread(os.path.join('assets', image_name))
            self.update_image()
            
    def update_image(self, *args):
        if self.current_image is None:
            return
            
        hsv = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2HSV)
        
        h_min = np.array([
            self.hsv_sliders['H min'].get(),
            self.hsv_sliders['S min'].get(),
            self.hsv_sliders['V min'].get()
        ], np.uint8)
        
        h_max = np.array([
            self.hsv_sliders['H max'].get(),
            self.hsv_sliders['S max'].get(),
            self.hsv_sliders['V max'].get()
        ], np.uint8)
        
        thresh = cv2.inRange(hsv, h_min, h_max)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        img_copy = self.current_image.copy()
        cv2.drawContours(img_copy, contours, -1, (0, 255, 0), 2)
        
        img_rgb = cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width > 1 and canvas_height > 1:
            img_pil.thumbnail((canvas_width, canvas_height), Image.LANCZOS)
        
        self.photo = ImageTk.PhotoImage(img_pil)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

def main():
    root = tk.Tk()
    app = HSVApp(root)
    root.mainloop()

print_colored_banner()
if __name__ == "__main__":
    main()
