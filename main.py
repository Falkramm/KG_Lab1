import tkinter as tk
from tkinter import colorchooser
import colorsys


class ColorConverterApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Color Converter")

        self.cmyk_labels = []
        self.rgb_labels = []
        self.hls_labels = []

        self.create_color_inputs()
        self.create_color_labels()

        self.root.mainloop()

    def create_color_inputs(self):
        self.cmyk_inputs = []
        self.rgb_inputs = []
        self.hls_inputs = []

        cmyk_frame = tk.Frame(self.root)
        cmyk_frame.pack()
        for i in range(4):
            label = tk.Label(cmyk_frame, text=f"CMYK[{i}]")
            label.grid(row=0, column=i)
            input_box = tk.Entry(cmyk_frame, width=5)
            input_box.grid(row=1, column=i)
            self.cmyk_inputs.append(input_box)

        rgb_frame = tk.Frame(self.root)
        rgb_frame.pack()
        for i in range(3):
            label = tk.Label(rgb_frame, text=f"RGB[{i}]")
            label.grid(row=0, column=i)
            input_box = tk.Entry(rgb_frame, width=5)
            input_box.grid(row=1, column=i)
            self.rgb_inputs.append(input_box)

        hls_frame = tk.Frame(self.root)
        hls_frame.pack()
        for i in range(3):
            label = tk.Label(hls_frame, text=f"HLS[{i}]")
            label.grid(row=0, column=i)
            input_box = tk.Entry(hls_frame, width=5)
            input_box.grid(row=1, column=i)
            self.hls_inputs.append(input_box)

        for entry in self.cmyk_inputs:
            entry.bind("<Key>", self.update_cmyk)

        for entry in self.rgb_inputs:
            entry.bind("<Key>", self.update_rgb)

        for entry in self.hls_inputs:
            entry.bind("<Key>", self.update_hls)

    def create_color_labels(self):
        labels_frame = tk.Frame(self.root)
        labels_frame.pack()

        cmyk_frame = tk.Frame(labels_frame)
        cmyk_frame.grid(row=0, column=0, padx=10)
        cmyk_label = tk.Label(cmyk_frame, text="CMYK:")
        cmyk_label.pack()
        for i in range(4):
            label = tk.Label(cmyk_frame, text="")
            label.pack()
            self.cmyk_labels.append(label)

        rgb_frame = tk.Frame(labels_frame)
        rgb_frame.grid(row=0, column=1, padx=10)
        rgb_label = tk.Label(rgb_frame, text="RGB:")
        rgb_label.pack()
        for i in range(3):
            label = tk.Label(rgb_frame, text="")
            label.pack()
            self.rgb_labels.append(label)

        hls_frame = tk.Frame(labels_frame)
        hls_frame.grid(row=0, column=2, padx=10)
        hls_label = tk.Label(hls_frame, text="HLS:")
        hls_label.pack()
        for i in range(3):
            label = tk.Label(hls_frame, text="")
            label.pack()
            self.hls_labels.append(label)

    def update_cmyk(self, event):
        try:
            c, m, y, k = [float(entry.get()) for entry in self.cmyk_inputs]
            r, g, b = self.cmyk_to_rgb(c, m, y, k)
            h, l, s = self.rgb_to_hls(r, g, b)
            self.set_background_color(r, g, b)
            self.update_cmyk_labels(c, m, y, k)
            self.update_rgb_labels(r, g, b)
            self.update_hls_labels(h, l, s)
        except ValueError:
            pass

    def update_rgb(self, event):
        try:
            r, g, b = [int(entry.get()) for entry in self.rgb_inputs]
            c, m, y, k = self.rgb_to_cmyk(r, g, b)
            h, l, s = self.rgb_to_hls(r, g, b)
            self.set_background_color(r, g, b)
            self.update_rgb_labels(r, g, b)
            self.update_cmyk_labels(c, m, y, k)
            self.update_hls_labels(h, l, s)
        except ValueError:
            pass

    def update_hls(self, event):
        try:
            h, l, s = [float(entry.get()) for entry in self.hls_inputs]
            r, g, b = self.hls_to_rgb(h, l, s)
            c, m, y, k = self.rgb_to_cmyk(r, g, b)
            self.set_background_color(r, g, b)
            self.update_hls_labels(h, l, s)
            self.update_rgb_labels(r, g, b)
            self.update_cmyk_labels(c, m, y, k)
        except ValueError:
            pass

    def set_background_color(self, r, g, b):
        try:
            hex_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
            self.root.configure(bg=hex_color)
        except ValueError:
            pass

    def update_cmyk_labels(self, c, m, y, k):
        self.cmyk_labels[0].config(text=f"C: {c:.2f}")
        self.cmyk_labels[1].config(text=f"M: {m:.2f}")
        self.cmyk_labels[2].config(text=f"Y: {y:.2f}")
        self.cmyk_labels[3].config(text=f"K: {k:.2f}")

    def update_rgb_labels(self, r, g, b):
        self.rgb_labels[0].config(text=f"R: {r}")
        self.rgb_labels[1].config(text=f"G: {g}")
        self.rgb_labels[2].config(text=f"B: {b}")

    def update_hls_labels(self, h, l, s):
        self.hls_labels[0].config(text=f"H: {h:.2f}")
        self.hls_labels[1].config(text=f"L: {l:.2f}")
        self.hls_labels[2].config(text=f"S: {s:.2f}")

    def cmyk_to_rgb(self, c, m, y, k):
        r = int((1 - c) * (1 - k) * 255)
        g = int((1 - m) * (1 - k) * 255)
        b = int((1 - y) * (1 - k) * 255)
        return r, g, b

    def rgb_to_cmyk(self, r, g, b):
        c = 1 - r / 255
        m = 1 - g / 255
        y = 1 - b / 255
        k = min(c, m, y)

        if k == 1:
            return 0, 0, 0, 1

        c = (c - k) / (1 - k)
        m = (m - k) / (1 - k)
        y = (y - k) / (1 - k)

        return c, m, y, k

    def rgb_to_hls(self, r, g, b):
        r /= 255
        g /= 255
        b /= 255
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        h *= 360
        l *= 100
        s *= 100
        return h, l, s

    def hls_to_rgb(self, h, l, s):
        h /= 360
        l /= 100
        s /= 100
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)
        return r, g, b


app = ColorConverterApp()
