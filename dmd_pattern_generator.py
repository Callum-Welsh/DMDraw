import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

class DMDPatternGenerator:
    def __init__(self):
        # Initialize the pattern array (912 columns x 1140 rows)
        self.width = 912
        self.height = 1140
        self.pattern = np.zeros((self.height, self.width), dtype=np.uint8)
        
        # GUI setup
        self.root = tk.Tk()
        self.root.title("DMD Pattern Generator")
        self.root.geometry("1200x800")
        
        # Variables
        self.preview_image = None
        self.preview_photo = None
        
        self.setup_gui()
        self.update_preview()
    
    def setup_gui(self):
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Control panel (left side) - make it scrollable
        control_frame = tk.Frame(main_frame, width=300)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Create a canvas with scrollbar for the control panel
        control_canvas = tk.Canvas(control_frame, width=300)
        control_scrollbar = tk.Scrollbar(control_frame, orient=tk.VERTICAL, command=control_canvas.yview)
        scrollable_control_frame = tk.Frame(control_canvas)
        
        # Configure the canvas
        control_canvas.configure(yscrollcommand=control_scrollbar.set)
        
        # Pack the scrollbar and canvas
        control_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        control_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create a window in the canvas for the scrollable frame
        control_canvas.create_window((0, 0), window=scrollable_control_frame, anchor=tk.NW)
        
        # Configure the scrollable frame to expand
        scrollable_control_frame.bind(
            "<Configure>",
            lambda e: control_canvas.configure(scrollregion=control_canvas.bbox("all"))
        )
        
        # Title
        title_label = tk.Label(scrollable_control_frame, text="DMD Pattern Generator", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Pattern tools
        tools_frame = tk.LabelFrame(scrollable_control_frame, text="Pattern Tools", padx=10, pady=10)
        tools_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Rectangle tool
        rect_frame = tk.Frame(tools_frame)
        rect_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(rect_frame, text="Rectangle:").pack(anchor=tk.W)
        
        rect_inputs = tk.Frame(rect_frame)
        rect_inputs.pack(fill=tk.X)
        
        tk.Label(rect_inputs, text="X:").grid(row=0, column=0, sticky=tk.W)
        self.x1_var = tk.StringVar(value="0")
        tk.Entry(rect_inputs, textvariable=self.x1_var, width=8).grid(row=0, column=1, padx=(5, 10))
        
        tk.Label(rect_inputs, text="Y:").grid(row=0, column=2, sticky=tk.W)
        self.y1_var = tk.StringVar(value="0")
        tk.Entry(rect_inputs, textvariable=self.y1_var, width=8).grid(row=0, column=3, padx=(5, 10))
        
        tk.Label(rect_inputs, text="W:").grid(row=1, column=0, sticky=tk.W)
        self.w_var = tk.StringVar(value="100")
        tk.Entry(rect_inputs, textvariable=self.w_var, width=8).grid(row=1, column=1, padx=(5, 10))
        
        tk.Label(rect_inputs, text="H:").grid(row=1, column=2, sticky=tk.W)
        self.h_var = tk.StringVar(value="100")
        tk.Entry(rect_inputs, textvariable=self.h_var, width=8).grid(row=1, column=3, padx=(5, 10))
        
        tk.Button(rect_frame, text="Add Rectangle", command=self.add_rectangle).pack(pady=5)
        
        # Circle tool
        circle_frame = tk.Frame(tools_frame)
        circle_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(circle_frame, text="Circle:").pack(anchor=tk.W)
        
        circle_inputs = tk.Frame(circle_frame)
        circle_inputs.pack(fill=tk.X)
        
        tk.Label(circle_inputs, text="Center X:").grid(row=0, column=0, sticky=tk.W)
        self.cx_var = tk.StringVar(value="456")
        tk.Entry(circle_inputs, textvariable=self.cx_var, width=8).grid(row=0, column=1, padx=(5, 10))
        
        tk.Label(circle_inputs, text="Center Y:").grid(row=0, column=2, sticky=tk.W)
        self.cy_var = tk.StringVar(value="570")
        tk.Entry(circle_inputs, textvariable=self.cy_var, width=8).grid(row=0, column=3, padx=(5, 10))
        
        tk.Label(circle_inputs, text="Radius:").grid(row=1, column=0, sticky=tk.W)
        self.radius_var = tk.StringVar(value="100")
        tk.Entry(circle_inputs, textvariable=self.radius_var, width=8).grid(row=1, column=1, padx=(5, 10))
        
        tk.Button(circle_frame, text="Add Circle", command=self.add_circle).pack(pady=5)
        
        # Line tool
        line_frame = tk.Frame(tools_frame)
        line_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(line_frame, text="Line:").pack(anchor=tk.W)
        
        line_inputs = tk.Frame(line_frame)
        line_inputs.pack(fill=tk.X)
        
        tk.Label(line_inputs, text="X1:").grid(row=0, column=0, sticky=tk.W)
        self.lx1_var = tk.StringVar(value="0")
        tk.Entry(line_inputs, textvariable=self.lx1_var, width=8).grid(row=0, column=1, padx=(5, 10))
        
        tk.Label(line_inputs, text="Y1:").grid(row=0, column=2, sticky=tk.W)
        self.ly1_var = tk.StringVar(value="0")
        tk.Entry(line_inputs, textvariable=self.ly1_var, width=8).grid(row=0, column=3, padx=(5, 10))
        
        tk.Label(line_inputs, text="X2:").grid(row=1, column=0, sticky=tk.W)
        self.lx2_var = tk.StringVar(value="100")
        tk.Entry(line_inputs, textvariable=self.lx2_var, width=8).grid(row=1, column=1, padx=(5, 10))
        
        tk.Label(line_inputs, text="Y2:").grid(row=1, column=2, sticky=tk.W)
        self.ly2_var = tk.StringVar(value="100")
        tk.Entry(line_inputs, textvariable=self.ly2_var, width=8).grid(row=1, column=3, padx=(5, 10))
        
        tk.Button(line_frame, text="Add Line", command=self.add_line).pack(pady=5)
        
        # Grid tool
        grid_frame = tk.Frame(tools_frame)
        grid_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(grid_frame, text="Grid:").pack(anchor=tk.W)
        
        grid_inputs = tk.Frame(grid_frame)
        grid_inputs.pack(fill=tk.X)
        
        tk.Label(grid_inputs, text="Start X:").grid(row=0, column=0, sticky=tk.W)
        self.grid_x_var = tk.StringVar(value="0")
        tk.Entry(grid_inputs, textvariable=self.grid_x_var, width=8).grid(row=0, column=1, padx=(5, 10))
        
        tk.Label(grid_inputs, text="Start Y:").grid(row=0, column=2, sticky=tk.W)
        self.grid_y_var = tk.StringVar(value="0")
        tk.Entry(grid_inputs, textvariable=self.grid_y_var, width=8).grid(row=0, column=3, padx=(5, 10))
        
        tk.Label(grid_inputs, text="Square Size:").grid(row=1, column=0, sticky=tk.W)
        self.grid_size_var = tk.StringVar(value="10")
        tk.Entry(grid_inputs, textvariable=self.grid_size_var, width=8).grid(row=1, column=1, padx=(5, 10))
        
        tk.Label(grid_inputs, text="Spacing:").grid(row=1, column=2, sticky=tk.W)
        self.grid_spacing_var = tk.StringVar(value="20")
        tk.Entry(grid_inputs, textvariable=self.grid_spacing_var, width=8).grid(row=1, column=3, padx=(5, 10))
        
        tk.Button(grid_frame, text="Add Grid", command=self.add_grid).pack(pady=5)
        
        # Text tool
        text_frame = tk.Frame(tools_frame)
        text_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(text_frame, text="Text:").pack(anchor=tk.W)
        
        text_inputs = tk.Frame(text_frame)
        text_inputs.pack(fill=tk.X)
        
        tk.Label(text_inputs, text="Text:").grid(row=0, column=0, sticky=tk.W)
        self.text_var = tk.StringVar(value="Hello")
        tk.Entry(text_inputs, textvariable=self.text_var, width=15).grid(row=0, column=1, columnspan=3, padx=(5, 10), sticky=tk.EW)
        
        tk.Label(text_inputs, text="X:").grid(row=1, column=0, sticky=tk.W)
        self.text_x_var = tk.StringVar(value="100")
        tk.Entry(text_inputs, textvariable=self.text_x_var, width=8).grid(row=1, column=1, padx=(5, 10))
        
        tk.Label(text_inputs, text="Y:").grid(row=1, column=2, sticky=tk.W)
        self.text_y_var = tk.StringVar(value="100")
        tk.Entry(text_inputs, textvariable=self.text_y_var, width=8).grid(row=1, column=3, padx=(5, 10))
        
        tk.Label(text_inputs, text="Size:").grid(row=2, column=0, sticky=tk.W)
        self.text_size_var = tk.StringVar(value="20")
        tk.Entry(text_inputs, textvariable=self.text_size_var, width=8).grid(row=2, column=1, padx=(5, 10))
        
        tk.Button(text_frame, text="Add Text", command=self.add_text).pack(pady=5)
        
        # Utility buttons
        utility_frame = tk.LabelFrame(scrollable_control_frame, text="Utilities", padx=10, pady=10)
        utility_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Button(utility_frame, text="Clear Pattern", command=self.clear_pattern).pack(fill=tk.X, pady=2)
        tk.Button(utility_frame, text="Invert Pattern", command=self.invert_pattern).pack(fill=tk.X, pady=2)
        tk.Button(utility_frame, text="Random Pattern", command=self.random_pattern).pack(fill=tk.X, pady=2)
        tk.Button(utility_frame, text="Flip Horizontal (X-axis)", command=self.flip_horizontal).pack(fill=tk.X, pady=2)
        tk.Button(utility_frame, text="Flip Vertical (Y-axis)", command=self.flip_vertical).pack(fill=tk.X, pady=2)
        
        # Preview controls
        preview_controls_frame = tk.LabelFrame(scrollable_control_frame, text="Preview Controls", padx=10, pady=10)
        preview_controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Preview scale slider
        tk.Label(preview_controls_frame, text="Preview Scale:").pack(anchor=tk.W)
        
        slider_frame = tk.Frame(preview_controls_frame)
        slider_frame.pack(fill=tk.X, pady=5)
        
        self.preview_scale_var = tk.DoubleVar(value=1.0)  # Default to pixel perfect
        self.preview_scale_slider = tk.Scale(
            slider_frame, 
            from_=0.1, 
            to=5.0, 
            orient=tk.HORIZONTAL,
            variable=self.preview_scale_var,
            command=self.on_preview_scale_change,
            resolution=0.1
        )
        self.preview_scale_slider.pack(fill=tk.X)
        
        # Scale labels
        labels_frame = tk.Frame(slider_frame)
        labels_frame.pack(fill=tk.X)
        tk.Label(labels_frame, text="10%", font=("Arial", 8)).pack(side=tk.LEFT)
        tk.Label(labels_frame, text="5x Zoom", font=("Arial", 8)).pack(side=tk.RIGHT)
        
        # Pixel perfect indicator
        self.pixel_perfect_label = tk.Label(preview_controls_frame, text="", font=("Arial", 9, "bold"), fg="blue")
        self.pixel_perfect_label.pack(anchor=tk.CENTER, pady=2)
        
        # Isotropic primitives toggle
        self.iso_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            preview_controls_frame,
            text="Isotropic primitives (DMD lattice)",
            variable=self.iso_var
        ).pack(anchor=tk.W)


        
        # Save button
        save_frame = tk.LabelFrame(scrollable_control_frame, text="Save", padx=10, pady=10)
        save_frame.pack(fill=tk.X)
        
        tk.Button(save_frame, text="Save as BMP", command=self.save_bmp, bg="green", fg="white").pack(fill=tk.X)
        
        # Preview panel (right side)
        preview_frame = tk.LabelFrame(main_frame, text="Preview", padx=10, pady=10)
        preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create a frame for the canvas with scrollbars
        canvas_frame = tk.Frame(preview_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas with scrollbars
        self.preview_canvas = tk.Canvas(canvas_frame, bg="white")
        self.h_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.preview_canvas.xview)
        self.v_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.preview_canvas.yview)
        
        # Configure canvas scrolling
        self.preview_canvas.configure(xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)
        
        # Pack scrollbars and canvas
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.preview_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind mouse events for panning
        self.preview_canvas.bind("<Button-1>", self.on_mouse_down)
        self.preview_canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.preview_canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        
        # Panning variables
        self.pan_start_x = 0
        self.pan_start_y = 0
        self.is_panning = False
        
        # Easter egg counter
        self.random_click_count = 0
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def add_rectangle(self):
        if self.iso_var.get():
            self.add_rectangle_iso()
        else:
            self.add_rectangle_legacy()

    # Legacy rectangle (kept for rollback)
    def add_rectangle_legacy(self):
        try:
            x = int(np.sqrt(4)*int(self.x1_var.get()))
            y = int(self.y1_var.get())
            w = int(self.w_var.get())
            h = int(self.h_var.get())
            x = max(0, min(x, self.width - 1))
            y = max(0, min(y, self.height - 1))
            w = max(1, min(w, self.width - x))
            h = max(1, min(h, self.height - y))
            self.pattern[y:y+h, x:x+w] = 1
            self.update_preview()
            self.status_var.set(f"(Legacy) Added rectangle at ({x}, {y}) with size {w}x{h}")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for rectangle coordinates")

    # Isotropic rectangle on DMD lattice
    def add_rectangle_iso(self):
        try:
            x = int(self.x1_var.get())
            y = int(self.y1_var.get())
            w = int(self.w_var.get())
            h = int(self.h_var.get())
            # Clamp BMP-space bounds
            x = max(0, min(x, self.width - 1))
            y = max(0, min(y, self.height - 1))
            w = max(1, min(w, self.width - x))
            h = max(1, min(h, self.height - y))
            # Build masks based on physical mapping
            # Condition A: (2c in [2x, 2(x+w))) and (r in [y, y+h))
            # Condition B: (2c+1 in [2x, 2(x+w))) and (r+1 in [y, y+h))
            rows = np.arange(self.height)[:, None]
            cols = np.arange(self.width)[None, :]
            cond_a = (cols >= x) & (cols < x + w) & (rows >= y) & (rows < y + h)
            cond_b = (cols >= x) & (cols < x + w) & (rows + 1 >= y) & (rows + 1 < y + h)
            mask = cond_a | cond_b
            self.pattern[mask] = 1
            self.update_preview()
            self.status_var.set(f"(Iso) Added rectangle at ({x}, {y}) size {w}x{h}")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for rectangle coordinates")
    
    def add_circle(self):
        if self.iso_var.get():
            self.add_circle_iso()
        else:
            self.add_circle_legacy()

    # Legacy circle (kept for rollback)
    def add_circle_legacy(self):
        try:
            cx = int(np.sqrt(4)*int(self.cx_var.get()))
            cy = int(self.cy_var.get())
            radius = int(self.radius_var.get())
            y, x = np.ogrid[:self.height, :self.width]
            dist = np.sqrt((np.sqrt(4)*x - cx)**2 + ((y - cy))**2)
            self.pattern[dist <= radius] = 1
            self.update_preview()
            self.status_var.set(f"(Legacy) Added circle at ({cx}, {cy}) with radius {radius}")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for circle parameters")

    # Isotropic circle on DMD lattice (operate in physical P-grid)
    def add_circle_iso(self):
        try:
            cx_b = int(self.cx_var.get())
            cy_b = int(self.cy_var.get())
            radius_p = int(self.radius_var.get())
            # Center in physical grid
            cx_p = 2 * cx_b
            cy_p = cy_b
            # Build BMP-space grids
            rows = np.arange(self.height)[:, None]
            cols = np.arange(self.width)[None, :]
            # Distances for the two physical mirrors per BMP pixel
            dx0 = (2 * cols - cx_p)
            dy0 = (rows - cy_p)
            dx1 = (2 * cols + 1 - cx_p)
            dy1 = (rows + 1 - cy_p)
            inside = (dx0 * dx0 + dy0 * dy0 <= radius_p * radius_p) | \
                     (dx1 * dx1 + dy1 * dy1 <= radius_p * radius_p)
            self.pattern[inside] = 1
            self.update_preview()
            self.status_var.set(f"(Iso) Added circle at ({cx_b}, {cy_b}) with radius {radius_p} (P units)")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for circle parameters")
    
    def add_line(self):
        if self.iso_var.get():
            self.add_line_iso()
        else:
            self.add_line_legacy()

    # Legacy line (kept for rollback)
    def add_line_legacy(self):
        try:
            x1 = int(np.sqrt(4)*int(self.lx1_var.get()))
            y1 = int(self.ly1_var.get())
            x2 = int(np.sqrt(4)*int(self.lx2_var.get()))
            y2 = int(self.ly2_var.get())
            self.bresenham_line(x1, y1, x2, y2)
            self.update_preview()
            self.status_var.set(f"(Legacy) Added line from ({x1}, {y1}) to ({x2}, {y2})")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for line coordinates")

    # Isotropic line on DMD lattice (draw in physical grid and map back)
    def add_line_iso(self):
        try:
            x1_b = int(self.lx1_var.get())
            y1_b = int(self.ly1_var.get())
            x2_b = int(self.lx2_var.get())
            y2_b = int(self.ly2_var.get())
            # Physical endpoints
            x1_p, y1_p = 2 * x1_b, y1_b
            x2_p, y2_p = 2 * x2_b, y2_b
            for (xp, yp) in self._bresenham_line_physical(x1_p, y1_p, x2_p, y2_p):
                c, r = self._p_to_bmp(xp, yp)
                if c is not None and 0 <= c < self.width and 0 <= r < self.height:
                    self.pattern[r, c] = 1
            self.update_preview()
            self.status_var.set(f"(Iso) Added line from ({x1_b}, {y1_b}) to ({x2_b}, {y2_b})")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for line coordinates")

    # Physical grid Bresenham
    def _bresenham_line_physical(self, x1: int, y1: int, x2: int, y2: int):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        x, y = x1, y1
        sx = 1 if x2 > x1 else -1
        sy = 1 if y2 > y1 else -1
        if dx >= dy:
            err = dx // 2
            while True:
                yield (x, y)
                if x == x2 and y == y2:
                    break
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy // 2
            while True:
                yield (x, y)
                if x == x2 and y == y2:
                    break
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy

    def _p_to_bmp(self, xp: int, yp: int):
        if xp % 2 == 0:
            c = xp // 2
            r = yp
        else:
            c = (xp - 1) // 2
            r = yp - 1
        if r < 0:
            return (None, None)
        return (c, r)
    
    def add_grid(self):
        if self.iso_var.get():
            self.add_grid_iso()
        else:
            self.add_grid_legacy()

    # Legacy grid (kept for rollback)
    def add_grid_legacy(self):
        """Add a square grid pattern with specified square size and spacing (legacy mapping)"""
        try:
            start_x = int(np.sqrt(4)*int(self.grid_x_var.get()))
            start_y = int(self.grid_y_var.get())
            square_size = int(self.grid_size_var.get())
            spacing = int(self.grid_spacing_var.get())
            total_spacing = square_size + spacing
            max_squares_x = (self.width - start_x) // total_spacing
            max_squares_y = (self.height - start_y) // total_spacing
            squares_added = 0
            for i in range(max_squares_x):
                for j in range(max_squares_y):
                    square_x = start_x + i * total_spacing
                    square_y = start_y + j * total_spacing
                    if (square_x + square_size <= self.width and 
                        square_y + square_size <= self.height):
                        self.pattern[square_y:square_y + square_size, 
                                   square_x:square_x + square_size] = 1
                        squares_added += 1
            self.update_preview()
            self.status_var.set(f"(Legacy) Added grid: {squares_added} squares starting at ({int(start_x/np.sqrt(4))}, {start_y})")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for grid parameters")

    # Isotropic grid on DMD lattice
    def add_grid_iso(self):
        try:
            # Read parameters (BMP-space start; sizes in physical units)
            start_x_b = int(self.grid_x_var.get())
            start_y_b = int(self.grid_y_var.get())
            square_size_p = int(self.grid_size_var.get())
            spacing_p = int(self.grid_spacing_var.get())
            total_p = square_size_p + spacing_p
            # Physical start
            start_x_p = 2 * start_x_b
            start_y_p = start_y_b
            phys_width = self.width * 2
            phys_height = self.height + 1
            # Precompute BMP index grids
            rows = np.arange(self.height)[:, None]
            cols = np.arange(self.width)[None, :]
            # Accumulate mask
            mask = np.zeros_like(self.pattern, dtype=bool)
            squares_added = 0
            i = 0
            while True:
                x0 = start_x_p + i * total_p
                if x0 >= phys_width or x0 + square_size_p > phys_width:
                    break
                j = 0
                row_added = False
                while True:
                    y0 = start_y_p + j * total_p
                    if y0 >= phys_height or y0 + square_size_p > phys_height:
                        break
                    # Inside test for both physical mirrors mapped from each BMP pixel
                    cond0 = (2 * cols >= x0) & (2 * cols < x0 + square_size_p) & (rows >= y0) & (rows < y0 + square_size_p)
                    cond1 = (2 * cols + 1 >= x0) & (2 * cols + 1 < x0 + square_size_p) & (rows + 1 >= y0) & (rows + 1 < y0 + square_size_p)
                    mask |= (cond0 | cond1)
                    squares_added += 1
                    row_added = True
                    j += 1
                if not row_added:
                    break
                i += 1
            self.pattern[mask] = 1
            self.update_preview()
            self.status_var.set(f"(Iso) Added grid: {squares_added} squares starting at ({start_x_b}, {start_y_b})")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for grid parameters")
    
    def add_text(self):
        if self.iso_var.get():
            self.add_text_iso()
        else:
            self.add_text_legacy()

    # Legacy text (kept for rollback)
    def add_text_legacy(self):
        """Add text to the pattern with DLP 4500 diagonal grid compensation (legacy mapping)"""
        try:
            text = self.text_var.get()
            x = int(np.sqrt(4)*int(self.text_x_var.get()))
            y = int(self.text_y_var.get())
            size = int(self.text_size_var.get())
            if not text.strip():
                messagebox.showerror("Error", "Please enter some text")
                return
            temp_width = len(text) * size * 2
            temp_height = size * 2
            temp_img = Image.new('L', (temp_width, temp_height), 255)
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(temp_img)
            try:
                font = ImageFont.truetype("arial.ttf", size)
            except:
                try:
                    font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", size)
                except:
                    font = ImageFont.load_default()
            draw.text((0, 0), text, fill=0, font=font)
            text_array = np.array(temp_img)
            text_binary = (text_array < 128).astype(np.uint8)
            rows = np.any(text_binary, axis=1)
            cols = np.any(text_binary, axis=0)
            if np.any(rows) and np.any(cols):
                rmin, rmax = np.where(rows)[0][[0, -1]]
                cmin, cmax = np.where(cols)[0][[0, -1]]
                text_content = text_binary[rmin:rmax+1, cmin:cmax+1]
                text_height, text_width = text_content.shape
                if (x + text_width <= self.width and y + text_height <= self.height and x >= 0 and y >= 0):
                    self.pattern[y:y + text_height, x:x + text_width] = text_content
                    self.update_preview()
                    self.status_var.set(f"(Legacy) Added text '{text}' at ({int(x/np.sqrt(4))}, {y}) with size {size}")
                else:
                    messagebox.showerror("Error", "Text would extend beyond pattern boundaries")
            else:
                messagebox.showerror("Error", "Could not render text")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for text parameters")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add text: {str(e)}")

    # Isotropic text on DMD lattice
    def add_text_iso(self):
        try:
            text = self.text_var.get()
            x_b = int(self.text_x_var.get())
            y_b = int(self.text_y_var.get())
            size = int(self.text_size_var.get())
            if not text.strip():
                messagebox.showerror("Error", "Please enter some text")
                return
            # Rasterize glyph to binary
            temp_width = len(text) * size * 2
            temp_height = size * 2
            temp_img = Image.new('L', (temp_width, temp_height), 255)
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(temp_img)
            try:
                font = ImageFont.truetype("arial.ttf", size)
            except:
                try:
                    font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", size)
                except:
                    font = ImageFont.load_default()
            draw.text((0, 0), text, fill=0, font=font)
            text_array = np.array(temp_img)
            text_binary = (text_array < 128)
            rows_any = np.any(text_binary, axis=1)
            cols_any = np.any(text_binary, axis=0)
            if not (np.any(rows_any) and np.any(cols_any)):
                messagebox.showerror("Error", "Could not render text")
                return
            rmin, rmax = np.where(rows_any)[0][[0, -1]]
            cmin, cmax = np.where(cols_any)[0][[0, -1]]
            text_content = text_binary[rmin:rmax+1, cmin:cmax+1]
            th, tw = text_content.shape
            # Physical anchor
            x_p = 2 * x_b
            y_p = y_b
            # Coordinates of on-pixels in glyph
            gy, gx = np.where(text_content)
            xp = x_p + gx
            yp = y_p + gy
            # Map to BMP pixels
            is_even = (xp % 2 == 0)
            c_even = xp[is_even] // 2
            r_even = yp[is_even]
            c_odd = (xp[~is_even] - 1) // 2
            r_odd = yp[~is_even] - 1
            # Concatenate
            c_all = np.concatenate([c_even, c_odd])
            r_all = np.concatenate([r_even, r_odd])
            # Validate bounds
            valid = (c_all >= 0) & (c_all < self.width) & (r_all >= 0) & (r_all < self.height)
            self.pattern[r_all[valid], c_all[valid]] = 1
            self.update_preview()
            self.status_var.set(f"(Iso) Added text '{text}' at ({x_b}, {y_b}) size {size}")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for text parameters")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add text: {str(e)}")
    
    def bresenham_line(self, x1, y1, x2, y2):
        """Bresenham's line algorithm for drawing lines"""
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        x, y = x1, y1
        n = 1 + dx + dy
        x_inc = 1 if x2 > x1 else -1
        y_inc = 1 if y2 > y1 else -1
        error = dx - dy
        dx *= 2
        dy *= 2
        
        for _ in range(n):
            if 0 <= x < self.width and 0 <= y < self.height:
                self.pattern[y, x] = 1
            
            if x == x2 and y == y2:
                break
                
            if error > 0:
                x += x_inc
                error -= dy
            else:
                y += y_inc
                error += dx
    
    def clear_pattern(self):
        self.pattern = np.zeros((self.height, self.width), dtype=np.uint8)
        self.update_preview()
        self.status_var.set("Pattern cleared")
    
    def invert_pattern(self):
        self.pattern = 1 - self.pattern
        self.update_preview()
        self.status_var.set("Pattern inverted")
    
    def random_pattern(self):
        self.random_click_count += 1
        
        # Easter egg: Princeton shield every 10th click
        if self.random_click_count % 10 == 0:
            self.create_princeton_shield()
            self.status_var.set("🎓 Princeton Shield generated! (Easter egg)")
        else:
            self.pattern = np.random.randint(0, 2, (self.height, self.width), dtype=np.uint8)
            self.status_var.set("Random pattern generated")
        
        self.update_preview()
    
    def flip_horizontal(self):
        """Flip the pattern horizontally (about the Y-axis)"""
        self.pattern = np.fliplr(self.pattern)
        self.update_preview()
        self.status_var.set("Pattern flipped horizontally")
    
    def flip_vertical(self):
        """Flip the pattern vertically (about the X-axis)"""
        self.pattern = np.flipud(self.pattern)
        self.update_preview()
        self.status_var.set("Pattern flipped vertically")
    
    def on_preview_scale_change(self, value):
        """Callback for preview scale slider changes"""
        scale = float(value)
        
        # Update pixel perfect indicator
        if abs(scale - 1.0) < 0.05:  # Within 5% of 1.0
            self.pixel_perfect_label.config(text="PIXEL PERFECT", fg="green")
        else:
            self.pixel_perfect_label.config(text="", fg="blue")
        
        self.update_preview()
    
    def on_mouse_down(self, event):
        """Handle mouse button press for panning"""
        self.pan_start_x = event.x
        self.pan_start_y = event.y
        self.is_panning = True
        self.preview_canvas.config(cursor="fleur")  # Change cursor to indicate panning
    
    def on_mouse_drag(self, event):
        """Handle mouse drag for panning"""
        if self.is_panning:
            # Calculate the difference in position
            dx = event.x - self.pan_start_x
            dy = event.y - self.pan_start_y
            
            # Scroll the canvas
            self.preview_canvas.xview_scroll(-dx, "units")
            self.preview_canvas.yview_scroll(-dy, "units")
            
            # Update start position
            self.pan_start_x = event.x
            self.pan_start_y = event.y
    
    def on_mouse_up(self, event):
        """Handle mouse button release"""
        self.is_panning = False
        self.preview_canvas.config(cursor="")  # Reset cursor
    
    def update_preview(self):
        # Get the preview scale from slider (1.0 = pixel perfect, 0.1 = 10% scale, 5.0 = 5x zoom)
        preview_scale = self.preview_scale_var.get()
        
        # Map BMP (912x1140) to physical DMD (approx 1824 x 1141) using (2c, r) and (2c+1, r+1)
        physical_map = self._bmp_to_dmd_physical()
        phys_height, phys_width = physical_map.shape
        
        # Calculate preview dimensions based on scale
        preview_width = int(phys_width * preview_scale)
        preview_height = int(phys_height * preview_scale)
        
        # Convert numpy array to PIL Image
        img = Image.fromarray(physical_map * 255, mode='L')
        img = img.resize((preview_width, preview_height), Image.NEAREST)
        
        # Convert to PhotoImage for tkinter
        self.preview_photo = ImageTk.PhotoImage(img)
        
        # Update canvas
        self.preview_canvas.delete("all")
        
        # Configure canvas scroll region to match image size
        self.preview_canvas.configure(scrollregion=(0, 0, preview_width, preview_height))
        
        # Create image at origin (0,0) instead of center
        self.preview_canvas.create_image(0, 0, image=self.preview_photo, anchor=tk.NW)

    # --- Legacy preview retained for easy rollback ---
    def update_preview_legacy(self):
        preview_scale = self.preview_scale_var.get()
        preview_width = int(np.sqrt(4)*int(self.width * preview_scale))
        preview_height = int(self.height * preview_scale)
        img = Image.fromarray(self.pattern * 255, mode='L')
        img = img.resize((preview_width, preview_height), Image.NEAREST)
        self.preview_photo = ImageTk.PhotoImage(img)
        self.preview_canvas.delete("all")
        self.preview_canvas.configure(scrollregion=(0, 0, preview_width, preview_height))
        self.preview_canvas.create_image(0, 0, image=self.preview_photo, anchor=tk.NW)

    # --- Helper: map BMP grid to physical DMD mirror occupancy ---
    def _bmp_to_dmd_physical(self) -> np.ndarray:
        """Create a physical mirror occupancy map from the 912x1140 BMP grid.
        For each BMP pixel (c, r) == 1, light DMD mirrors at (2c, r) and (2c+1, r+1).
        Returns an array of shape ((height+1), (2*width)) of dtype uint8.
        """
        phys_height = self.height + 1
        phys_width = self.width * 2
        physical = np.zeros((phys_height, phys_width), dtype=np.uint8)
        ones_y, ones_x = np.where(self.pattern == 1)
        # (2c, r)
        physical[ones_y, 2 * ones_x] = 1
        # (2c+1, r+1) with clipping at bottom row
        valid = ones_y + 1 < phys_height
        physical[ones_y[valid] + 1, 2 * ones_x[valid] + 1] = 1
        return physical
        
    def create_princeton_shield(self):
        """Create a Princeton University shield pattern from BMP file"""
        try:
            # Load the Princeton seal BMP file
            seal_img = Image.open("Princeton_seal.BMP")
            
            # Convert to grayscale and then to binary (1-bit)
            seal_img = seal_img.convert('L')
            seal_array = np.array(seal_img)
            
            # Threshold to create binary image (0 or 1)
            # Assuming white background and dark seal - invert if needed
            seal_binary = (seal_array < 128).astype(np.uint8)
            
            # Get the dimensions of the seal
            seal_height, seal_width = seal_binary.shape
            
            # Clear the pattern first
            self.pattern = np.zeros((self.height, self.width), dtype=np.uint8)
            
            # Calculate center position to place the seal
            center_x = self.width // 2
            center_y = self.height // 2
            
            # Calculate starting positions for the seal
            start_x = center_x - seal_width // 2
            start_y = center_y - seal_height // 2
            
            # Ensure the seal fits within the pattern bounds
            if start_x < 0:
                start_x = 0
            if start_y < 0:
                start_y = 0
            if start_x + seal_width > self.width:
                start_x = self.width - seal_width
            if start_y + seal_height > self.height:
                start_y = self.height - seal_height
            
            # Copy the seal into the pattern
            self.pattern[start_y:start_y + seal_height, start_x:start_x + seal_width] = seal_binary
            
        except Exception as e:
            # Fallback to simple pattern if file loading fails
            self.pattern = np.zeros((self.height, self.width), dtype=np.uint8)
            # Create a simple centered rectangle as fallback
            center_x = self.width // 2
            center_y = self.height // 2
            size = min(self.width, self.height) // 4
            x1 = center_x - size // 2
            y1 = center_y - size // 2
            x2 = center_x + size // 2
            y2 = center_y + size // 2
            self.pattern[y1:y2, x1:x2] = 1
    
    def save_bmp(self):
        # Show save dialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".bmp",
            filetypes=[("BMP files", "*.bmp"), ("All files", "*.*")],
            title="Save DMD Pattern as BMP"
        )
        
        if filename:
            try:
                # Create 1-bit BMP
                img = Image.fromarray(self.pattern * 255, mode='L')
                img = img.convert('1')  # Convert to 1-bit
                img.save(filename, 'BMP')
                
                self.status_var.set(f"Pattern saved to {filename}")
                messagebox.showinfo("Success", f"Pattern saved successfully to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = DMDPatternGenerator()
    app.run()
