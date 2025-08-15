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
        
        # Control panel (left side)
        control_frame = tk.Frame(main_frame, width=300)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Title
        title_label = tk.Label(control_frame, text="DMD Pattern Generator", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Pattern tools
        tools_frame = tk.LabelFrame(control_frame, text="Pattern Tools", padx=10, pady=10)
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
        utility_frame = tk.LabelFrame(control_frame, text="Utilities", padx=10, pady=10)
        utility_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Button(utility_frame, text="Clear Pattern", command=self.clear_pattern).pack(fill=tk.X, pady=2)
        tk.Button(utility_frame, text="Invert Pattern", command=self.invert_pattern).pack(fill=tk.X, pady=2)
        tk.Button(utility_frame, text="Random Pattern", command=self.random_pattern).pack(fill=tk.X, pady=2)
        
        # Preview controls
        preview_controls_frame = tk.LabelFrame(control_frame, text="Preview Controls", padx=10, pady=10)
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
        

        
        # Save button
        save_frame = tk.LabelFrame(control_frame, text="Save", padx=10, pady=10)
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
        try:
            x = int(int(self.x1_var.get()))
            y = int(np.sqrt(4)*int(self.y1_var.get()))
            w = int(int(self.w_var.get()))
            h = int(np.sqrt(4)*int(self.h_var.get()))
            
            # Ensure coordinates are within bounds
            x = max(0, min(x, self.width - 1))
            y = max(0, min(y, self.height - 1))
            w = max(1, min(w, self.width - x))
            h = max(1, min(h, self.height - y))
            
            self.pattern[y:y+h, x:x+w] = 1
            self.update_preview()
            self.status_var.set(f"Added rectangle at ({x}, {y}) with size {w}x{h}")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for rectangle coordinates")
    
    def add_circle(self):
        try:
            cx = int(np.sqrt(4)*int(self.cx_var.get()))
            cy = int(self.cy_var.get())
            radius = int(self.radius_var.get())
            
            # Create coordinate grids
            y, x = np.ogrid[:self.height, :self.width]
            
            # Calculate distance from center
            dist = np.sqrt((np.sqrt(4)*x - cx)**2 + ((y - cy))**2)
            
            # Set pixels within radius to 1
            self.pattern[dist <= radius] = 1
            self.update_preview()
            self.status_var.set(f"Added circle at ({cx}, {cy}) with radius {radius}")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for circle parameters")
    
    def add_line(self):
        try:
            x1, y1 = int(self.lx1_var.get()), int(self.ly1_var.get())
            x2, y2 = int(self.lx2_var.get()), int(self.ly2_var.get())
            
            # Use Bresenham's line algorithm
            self.bresenham_line(x1, y1, x2, y2)
            self.update_preview()
            self.status_var.set(f"Added line from ({x1}, {y1}) to ({x2}, {y2})")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for line coordinates")
    
    def add_grid(self):
        """Add a square grid pattern with specified square size and spacing"""
        try:
            # Get grid parameters
            start_x = int(self.grid_x_var.get())
            start_y = int(self.grid_y_var.get())
            square_size = int(self.grid_size_var.get())
            spacing = int(self.grid_spacing_var.get())
            
            # Apply DLP 4500 diagonal grid scaling (same as rectangle/circle)
            # X coordinates are scaled by sqrt(4) = 2
            scaled_start_x = int(np.sqrt(4) * start_x)
            
            # Calculate grid parameters
            total_spacing = square_size + spacing
            
            # Calculate how many squares can fit in the pattern
            max_squares_x = (self.width - scaled_start_x) // total_spacing
            max_squares_y = (self.height - start_y) // total_spacing
            
            # Create the grid
            squares_added = 0
            for i in range(max_squares_x):
                for j in range(max_squares_y):
                    # Calculate square position
                    square_x = scaled_start_x + i * total_spacing
                    square_y = start_y + j * total_spacing
                    
                    # Ensure square fits within bounds
                    if (square_x + square_size <= self.width and 
                        square_y + square_size <= self.height):
                        # Add the square
                        self.pattern[square_y:square_y + square_size, 
                                   square_x:square_x + square_size] = 1
                        squares_added += 1
            
            self.update_preview()
            self.status_var.set(f"Added grid: {squares_added} squares starting at ({start_x}, {start_y})")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for grid parameters")
    
    def add_text(self):
        """Add text to the pattern with DLP 4500 diagonal grid compensation"""
        try:
            # Get text parameters
            text = self.text_var.get()
            x = int(self.text_x_var.get())
            y = int(self.text_y_var.get())
            size = int(self.text_size_var.get())
            
            if not text.strip():
                messagebox.showerror("Error", "Please enter some text")
                return
            
            # Apply DLP 4500 diagonal grid scaling (same as other tools)
            # X coordinates are scaled by sqrt(4) = 2
            scaled_x = int(np.sqrt(4) * x)
            
            # Create a temporary image to render the text
            # Use a larger temporary image to ensure text fits
            temp_width = len(text) * size * 2  # Estimate width needed
            temp_height = size * 2  # Estimate height needed
            
            # Create temporary image with white background
            temp_img = Image.new('L', (temp_width, temp_height), 255)
            
            # Create a drawing object
            from PIL import ImageDraw, ImageFont
            
            draw = ImageDraw.Draw(temp_img)
            
            # Try to use a default font, fallback to basic if not available
            try:
                # Try to use a system font
                font = ImageFont.truetype("arial.ttf", size)
            except:
                try:
                    # Try alternative font names
                    font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", size)
                except:
                    # Fallback to default font
                    font = ImageFont.load_default()
            
            # Draw the text in black
            draw.text((0, 0), text, fill=0, font=font)
            
            # Convert to numpy array and threshold to binary
            text_array = np.array(temp_img)
            text_binary = (text_array < 128).astype(np.uint8)
            
            # Get the actual text bounds (crop to actual text content)
            # Find the bounding box of the text
            rows = np.any(text_binary, axis=1)
            cols = np.any(text_binary, axis=0)
            
            if np.any(rows) and np.any(cols):
                rmin, rmax = np.where(rows)[0][[0, -1]]
                cmin, cmax = np.where(cols)[0][[0, -1]]
                
                # Crop to actual text content
                text_content = text_binary[rmin:rmax+1, cmin:cmax+1]
                text_height, text_width = text_content.shape
                
                # Check if text fits within pattern bounds
                if (scaled_x + text_width <= self.width and 
                    y + text_height <= self.height and
                    scaled_x >= 0 and y >= 0):
                    
                    # Add the text to the pattern
                    self.pattern[y:y + text_height, scaled_x:scaled_x + text_width] = text_content
                    
                    self.update_preview()
                    self.status_var.set(f"Added text '{text}' at ({x}, {y}) with size {size}")
                else:
                    messagebox.showerror("Error", "Text would extend beyond pattern boundaries")
            else:
                messagebox.showerror("Error", "Could not render text")
                
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
        
        # Calculate preview dimensions based on scale
        preview_width = int(np.sqrt(4)*int(self.width * preview_scale))
        preview_height = int(self.height * preview_scale)
        
        # Convert numpy array to PIL Image
        img = Image.fromarray(self.pattern * 255, mode='L')
        img = img.resize((preview_width, preview_height), Image.NEAREST)
        
        # Convert to PhotoImage for tkinter
        self.preview_photo = ImageTk.PhotoImage(img)
        
        # Update canvas
        self.preview_canvas.delete("all")
        
        # Configure canvas scroll region to match image size
        self.preview_canvas.configure(scrollregion=(0, 0, preview_width, preview_height))
        
        # Create image at origin (0,0) instead of center
        self.preview_canvas.create_image(0, 0, image=self.preview_photo, anchor=tk.NW)
        
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
