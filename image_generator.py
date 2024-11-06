import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import customtkinter as ctk
from openai import AzureOpenAI
import requests
import io
from PIL import Image, ImageTk
import json
import os
from datetime import datetime
import threading
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

__author__ = "Dipankar Boruah"
__version__ = "1.0.0"
__license__ = "MIT"

class ImageGeneratorApp:
    def __init__(self, root):
        self.version = __version__
        self.root = root
        self.root.title("AI Image Generator Platform")
        self.root.geometry("1200x800")
        
        # Azure OpenAI Configuration
        self.api_key = ""  # Will be set through UI
        self.endpoint = ""  # Will be set through UI
        self.api_version = "2023-12-01-preview"
        
        # Style Configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Left panel for controls
        self.left_panel = ttk.Frame(self.main_frame, padding="5", width=400)
        self.left_panel.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # API Configuration Section
        self.setup_api_config()
        
        # Generation Settings Section
        self.setup_generation_settings()
        
        # Progress Section
        self.setup_progress_section()
        
        # Prompt Section
        self.setup_prompt_section()
        
        # Right panel for image display
        self.right_panel = ttk.Frame(self.main_frame, padding="5")
        self.right_panel.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(0, weight=1)
        
        # Image Display Area
        self.setup_image_display()
        
        # Status Bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
    def setup_api_config(self):
        api_frame = ttk.LabelFrame(self.left_panel, text="API Configuration", padding="5")
        api_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(api_frame, text="API Key:").grid(row=0, column=0, sticky=tk.W)
        self.api_key_entry = ttk.Entry(api_frame, show="*", width=40)
        self.api_key_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(api_frame, text="Endpoint:").grid(row=1, column=0, sticky=tk.W)
        self.endpoint_entry = ttk.Entry(api_frame, width=40)
        self.endpoint_entry.grid(row=1, column=1, padx=5, pady=2)
        
        # View/Hide API Key button
        self.show_key = tk.BooleanVar(value=False)
        ttk.Checkbutton(api_frame, text="Show API Key", variable=self.show_key, 
                       command=self.toggle_api_key_visibility).grid(row=0, column=2, padx=5)
        
        ttk.Button(api_frame, text="Save Config", command=self.save_settings).grid(row=2, column=1, pady=5)
        
    def setup_generation_settings(self):
        settings_frame = ttk.LabelFrame(self.left_panel, text="Generation Settings", padding="5")
        settings_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Model selection
        ttk.Label(settings_frame, text="Model:").grid(row=0, column=0, sticky=tk.W)
        self.model_var = tk.StringVar(value="dall-e-3")
        model_options = ["dall-e-3", "dall-e-2"]
        self.model_combo = ttk.Combobox(settings_frame, textvariable=self.model_var, values=model_options)
        self.model_combo.grid(row=0, column=1, padx=5, pady=2)
        self.model_combo.bind('<<ComboboxSelected>>', self.update_size_options)
        
        # Size selection
        ttk.Label(settings_frame, text="Image Size:").grid(row=1, column=0, sticky=tk.W)
        self.size_var = tk.StringVar(value="1024x1024")
        self.size_combo = ttk.Combobox(settings_frame, textvariable=self.size_var)
        self.size_combo.grid(row=1, column=1, padx=5, pady=2)
        
        # Aspect Ratio selection
        ttk.Label(settings_frame, text="Aspect Ratio:").grid(row=2, column=0, sticky=tk.W)
        self.aspect_var = tk.StringVar(value="square")
        aspect_options = ["square", "portrait", "landscape"]
        self.aspect_combo = ttk.Combobox(settings_frame, textvariable=self.aspect_var, values=aspect_options)
        self.aspect_combo.grid(row=2, column=1, padx=5, pady=2)
        self.aspect_combo.bind('<<ComboboxSelected>>', self.update_size_options)
        
        # Quality selection
        ttk.Label(settings_frame, text="Quality:").grid(row=3, column=0, sticky=tk.W)
        self.quality_var = tk.StringVar(value="standard")
        quality_options = ["standard", "hd"]
        self.quality_combo = ttk.Combobox(settings_frame, textvariable=self.quality_var, values=quality_options)
        self.quality_combo.grid(row=3, column=1, padx=5, pady=2)
        
        # Style selection
        ttk.Label(settings_frame, text="Style:").grid(row=4, column=0, sticky=tk.W)
        self.style_var = tk.StringVar(value="vivid")
        style_options = ["vivid", "natural"]
        self.style_combo = ttk.Combobox(settings_frame, textvariable=self.style_var, values=style_options)
        self.style_combo.grid(row=4, column=1, padx=5, pady=2)
        
        # Set initial size options
        self.update_size_options(None)
        
    def setup_progress_section(self):
        self.progress_frame = ttk.LabelFrame(self.left_panel, text="Generation Progress", padding="5")
        self.progress_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame, 
            mode='indeterminate', 
            length=300
        )
        self.progress_bar.grid(row=0, column=0, padx=5, pady=5)
        
        self.time_label = ttk.Label(self.progress_frame, text="Estimated time: waiting...")
        self.time_label.grid(row=1, column=0, padx=5)
        
    def setup_prompt_section(self):
        prompt_frame = ttk.LabelFrame(self.left_panel, text="Prompt", padding="5")
        prompt_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Prompt input
        self.prompt_text = scrolledtext.ScrolledText(prompt_frame, width=40, height=10)
        self.prompt_text.grid(row=0, column=0, padx=5, pady=5)
        
        # Example prompts dropdown
        ttk.Label(prompt_frame, text="Example Prompts:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.example_var = tk.StringVar()
        example_prompts = [
            "A serene landscape with mountains at sunset",
            "A futuristic city with flying cars",
            "A cute robot playing with a cat",
            "An underwater scene with bioluminescent creatures",
            "A magical forest with glowing mushrooms"
        ]
        self.example_combo = ttk.Combobox(prompt_frame, textvariable=self.example_var, values=example_prompts)
        self.example_combo.grid(row=2, column=0, padx=5, pady=2, sticky=(tk.W, tk.E))
        self.example_combo.bind('<<ComboboxSelected>>', self.use_example_prompt)
        
        # Buttons
        button_frame = ttk.Frame(prompt_frame)
        button_frame.grid(row=3, column=0, pady=5)
        
        ttk.Button(button_frame, text="Generate", command=self.generate_image).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Save Image", command=self.save_image).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Clear Prompt", command=self.clear_prompt).grid(row=0, column=2, padx=5)
        
    def setup_image_display(self):
        self.image_frame = ttk.LabelFrame(self.right_panel, text="Generated Image", padding="5")
        self.image_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.image_frame.grid_columnconfigure(0, weight=1)
        self.image_frame.grid_rowconfigure(0, weight=1)
        
        self.image_label = ttk.Label(self.image_frame)
        self.image_label.grid(row=0, column=0, padx=5, pady=5)
        
    def toggle_api_key_visibility(self):
        if self.show_key.get():
            self.api_key_entry.configure(show="")
        else:
            self.api_key_entry.configure(show="*")
            
    def update_size_options(self, event):
        if self.model_var.get() == "dall-e-3":
            # DALL-E 3 dimensions
            aspect_ratio = self.aspect_var.get()
            if aspect_ratio == "square":
                size_options = ["1024x1024"]
            elif aspect_ratio == "portrait":
                size_options = ["1024x1792", "1024x1408"]
            elif aspect_ratio == "landscape":
                size_options = ["1792x1024", "1408x1024"]
        else:  # dall-e-2
            # DALL-E 2 dimensions
            size_options = ["256x256", "512x512", "1024x1024"]
            
        self.size_combo.configure(values=size_options)
        if self.size_var.get() not in size_options:
            self.size_var.set(size_options[0])
            
    def use_example_prompt(self, event):
        self.prompt_text.delete(1.0, tk.END)
        self.prompt_text.insert(tk.END, self.example_var.get())
        
    def clear_prompt(self):
        self.prompt_text.delete(1.0, tk.END)
        
    def generate_image(self):
        if not self.api_key_entry.get() or not self.endpoint_entry.get():
            self.status_var.set("Please configure API settings first!")
            return
            
        if not self.prompt_text.get(1.0, tk.END).strip():
            self.status_var.set("Please enter a prompt first!")
            return
            
        self.status_var.set("Generating image...")
        threading.Thread(target=self._generate_image_thread, daemon=True).start()
        
    def _generate_image_thread(self):
        try:
            # Start timing and progress indication
            start_time = datetime.now()
            self.root.after(0, self._start_progress)
            
            # Initialize Azure OpenAI client
            client = AzureOpenAI(
                api_key=self.api_key_entry.get(),
                api_version=self.api_version,
                azure_endpoint=self.endpoint_entry.get()
            )
            
            # Update status with quality and size info
            quality_factor = 1.5 if self.quality_var.get() == "hd" else 1
            estimated_time = 5 * quality_factor
            
            self.root.after(0, lambda: self.time_label.config(
                text=f"Estimated time: {estimated_time:.1f} seconds"
            ))
            
            # Parse size into width and height
            width, height = map(int, self.size_var.get().split('x'))
            
            # Generate image using the new API
            generation_params = {
                "model": self.model_var.get(),
                "prompt": self.prompt_text.get("1.0", tk.END).strip(),
                "size": f"{width}x{height}",
                "quality": self.quality_var.get(),
                "style": self.style_var.get(),
                "n": 1
            }
            
            # Remove style parameter if using DALL-E 2
            if self.model_var.get() == "dall-e-2":
                generation_params.pop("style", None)
            
            response = client.images.generate(**generation_params)
            
            # Get the image URL from the response
            image_url = response.data[0].url
            image_data = requests.get(image_url).content
            image = Image.open(io.BytesIO(image_data))
            
            # Store the current image for saving later
            self.current_image = image
            
            # Calculate display size while maintaining aspect ratio
            display_max_size = (800, 800)
            image_aspect_ratio = width / height
            if image_aspect_ratio > 1:  # landscape
                display_width = min(width, display_max_size[0])
                display_height = int(display_width / image_aspect_ratio)
            else:  # portrait or square
                display_height = min(height, display_max_size[1])
                display_width = int(display_height * image_aspect_ratio)
                
            # Resize for display
            display_size = (display_width, display_height)
            image_display = image.copy()
            image_display.thumbnail(display_size, Image.Resampling.LANCZOS)
            
            # Calculate actual generation time
            end_time = datetime.now()
            generation_time = (end_time - start_time).total_seconds()
            
            # Update UI in the main thread
            photo = ImageTk.PhotoImage(image_display)
            self.root.after(0, self._update_image_display, photo)
            self.root.after(0, lambda: self.status_var.set(
                f"Image generated successfully in {generation_time:.1f} seconds!"
            ))
            self.root.after(0, self._stop_progress)
            
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Error: {str(e)}"))
            self.root.after(0, self._stop_progress)
            
    def _start_progress(self):
        self.progress_bar.start(10)
        
    def _stop_progress(self):
        self.progress_bar.stop()
        
    def _update_image_display(self, photo):
        self.photo = photo  # Keep a reference to prevent garbage collection
        self.image_label.configure(image=photo)
        
    def save_image(self):
        if hasattr(self, 'current_image'):
            filename = f"generated_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                initialfile=filename,
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
            )
            if file_path:
                self.current_image.save(file_path)
                self.status_var.set(f"Image saved to {file_path}")
        else:
            self.status_var.set("No image to save!")
            
    def save_settings(self):
        settings = {
            "api_key": self.api_key_entry.get(),
            "endpoint": self.endpoint_entry.get()
        }
        try:
            with open("config.json", "w") as f:
                json.dump(settings, f)
            self.status_var.set("Settings saved successfully!")
        except Exception as e:
            self.status_var.set(f"Error saving settings: {str(e)}")
            
    def load_settings(self):
        try:
            if os.path.exists("config.json"):
                with open("config.json", "r") as f:
                    settings = json.load(f)
                self.api_key_entry.insert(0, settings.get("api_key", ""))
                self.endpoint_entry.insert(0, settings.get("endpoint", ""))
        except Exception as e:
            self.status_var.set(f"Error loading settings: {str(e)}")
            
    def on_closing(self):
        """Handle window closing event"""
        try:
            self.save_settings()
        except:
            pass
        self.root.destroy()

def main():
    root = tk.Tk()
    app = ImageGeneratorApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)  # Handle window closing
    root.mainloop()

if __name__ == "__main__":
    main()
