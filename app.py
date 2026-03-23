import customtkinter as ctk
from tkinter import filedialog
import os
import threading
from PIL import Image

# Interface Configuration
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ShutterShieldApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ShutterShield - EXIF Sanitizer")
        self.geometry("500x400")
        
        self.input_path = ""
        self.input_type = ""
        self.output_folder = ""

        # UI Elements
        self.label_title = ctk.CTkLabel(self, text="🛡️ ShutterShield", font=("Roboto", 24, "bold"))
        self.label_title.pack(pady=20)

        self.btn_input_file = ctk.CTkButton(self, text="Select Single Photo", command=self.select_input_file)
        self.btn_input_file.pack(pady=10)

        self.btn_input_folder = ctk.CTkButton(self, text="Select Photo Folder", command=self.select_input_folder)
        self.btn_input_folder.pack(pady=10)

        self.btn_output = ctk.CTkButton(self, text="Select Output Folder", command=self.select_output)
        self.btn_output.pack(pady=10)

        self.progress = ctk.CTkProgressBar(self, width=400)
        self.progress.pack(pady=20)
        self.progress.set(0)

        self.status_label = ctk.CTkLabel(self, text="Waiting for input...", font=("Roboto", 12))
        self.status_label.pack(pady=5)

        self.btn_start = ctk.CTkButton(self, text="Start Cleaning", fg_color="green", hover_color="darkgreen", 
                                       state="disabled", command=self.start_scrubbing_thread)
        self.btn_start.pack(pady=10)

    def select_input_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.input_path = file_path
            self.input_type = "file"
            self.check_ready()

    def select_input_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.input_path = folder_path
            self.input_type = "folder"
            self.check_ready()

    def select_output(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_folder = folder_path
            self.check_ready()

    def check_ready(self):
        if self.input_path and self.output_folder:
            self.btn_start.configure(state="normal")
            self.status_label.configure(text="Ready to clean.")

    def start_scrubbing_thread(self):
        self.btn_start.configure(state="disabled")
        self.progress.set(0)
        threading.Thread(target=self.process_images, daemon=True).start()

    def process_images(self):
        valid_extensions = ('.jpg', '.jpeg', '.png')
        
        files_to_process = []
        if self.input_type == "folder":
            image_files = [f for f in os.listdir(self.input_path) if f.lower().endswith(valid_extensions)]
            if not image_files:
                self.after(0, lambda: self.status_label.configure(text="No images found in the selected folder."))
                self.after(0, lambda: self.btn_start.configure(state="normal"))
                return
            for f in image_files:
                files_to_process.append((os.path.join(self.input_path, f), f))
        elif self.input_type == "file":
            filename = os.path.basename(self.input_path)
            if not filename.lower().endswith(valid_extensions):
                self.after(0, lambda: self.status_label.configure(text="Invalid file type selected."))
                self.after(0, lambda: self.btn_start.configure(state="normal"))
                return
            files_to_process.append((self.input_path, filename))

        total_files = len(files_to_process)

        for index, (input_full_path, filename) in enumerate(files_to_process):
            output_path = os.path.join(self.output_folder, f"clean_{filename}")
            
            self.after(0, lambda f=filename: self.status_label.configure(text=f"Processing: {f}..."))
            
            try:
                # Core Privacy Feature: Lossless EXIF Stripping
                with Image.open(input_full_path) as img:
                    kwargs = {}
                    # For JPEGs, quality=100 would artificially bloat the file.
                    # quality='keep' tells Pillow to reuse original compression.
                    if img.format in ['JPEG', 'MPO']:
                        kwargs['quality'] = 'keep'
                        kwargs['subsampling'] = 'keep' # Keep original chroma subsampling (crucial for file size)
                        kwargs['optimize'] = True      # Optimize Huffman trees (can even result in a smaller file size)
                        
                    # Save the image forcing absolute removal of EXIF data (exif=b"")
                    # Pillow defaults to dropping most other metadata during save().
                    img.save(output_path, exif=b"", **kwargs)
            except Exception as e:
                print(f"Error processing {filename}: {e}")

            self.after(0, lambda i=index: self.progress.set((i + 1) / total_files))

        self.after(0, lambda: self.status_label.configure(text="✅ Cleaning completed successfully! EXIF data removed."))
        self.after(0, lambda: self.btn_start.configure(state="normal"))

if __name__ == "__main__":
    app = ShutterShieldApp()
    app.mainloop()