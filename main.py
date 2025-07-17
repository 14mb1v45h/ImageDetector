# main.py - Cyberdudebivash's Image File Inspection Utility
# This app detects and inspects image files, extracting metadata like creation date, location, metadata details,
# system information (e.g., camera make/model), and source details.
# Uses Tkinter for GUI, Pillow and exifread for image analysis.
# Note: For educational purposes. Supports common image formats with EXIF data (e.g., JPEG).

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
from PIL import Image
import exifread
from datetime import datetime

class ImageInspectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cyberdudebivash's Image File Inspection Utility")
        self.root.geometry("600x500")
        
        # UI Elements
        self.label = tk.Label(root, text="Select an image file or folder to scan:")
        self.label.pack(pady=10)
        
        self.select_file_btn = tk.Button(root, text="Select Image File", command=self.select_file)
        self.select_file_btn.pack(pady=5)
        
        self.select_folder_btn = tk.Button(root, text="Scan Folder for Images", command=self.select_folder)
        self.select_folder_btn.pack(pady=5)
        
        self.results_text = scrolledtext.ScrolledText(root, width=70, height=20, wrap=tk.WORD)
        self.results_text.pack(pady=10)
        
        self.image_list = tk.Listbox(root, width=70, height=5)
        self.image_list.pack(pady=5)
        self.image_list.bind('<<ListboxSelect>>', self.analyze_selected_image)
        self.image_list.pack_forget()  # Hidden initially
        
        self.analyze_btn = tk.Button(root, text="Analyze Selected Image", command=self.analyze_from_list)
        self.analyze_btn.pack(pady=5)
        self.analyze_btn.pack_forget()  # Hidden initially

    def select_file(self):
        file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image Files", "*.jpg *.jpeg *.png *.tiff *.bmp")])
        if file_path:
            if self.is_image(file_path):
                self.analyze_image(file_path)
            else:
                messagebox.showerror("Error", "Selected file is not a valid image.")

    def select_folder(self):
        folder_path = filedialog.askdirectory(title="Select Folder to Scan")
        if folder_path:
            self.scan_folder(folder_path)

    def is_image(self, file_path):
        try:
            with Image.open(file_path):
                return True
        except:
            return False

    def scan_folder(self, folder_path):
        self.image_list.delete(0, tk.END)
        self.results_text.delete(1.0, tk.END)
        images = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                if self.is_image(file_path):
                    images.append(file_path)
                    self.image_list.insert(tk.END, file_path)
        
        if images:
            self.image_list.pack()
            self.analyze_btn.pack()
            self.results_text.insert(tk.END, f"Found {len(images)} image(s) in the folder.\nSelect an image from the list to analyze.\n")
        else:
            messagebox.showinfo("No Images", "No image files found in the selected folder.")

    def analyze_from_list(self):
        selected = self.image_list.curselection()
        if selected:
            file_path = self.image_list.get(selected[0])
            self.analyze_image(file_path)

    def analyze_selected_image(self, event):
        # Optional: Auto-analyze on selection (but we'll use button for explicit action)
        pass

    def analyze_image(self, file_path):
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"Analyzing: {file_path}\n\n")
        
        # File Metadata
        try:
            stat = os.stat(file_path)
            creation_date = datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
            self.results_text.insert(tk.END, f"File Creation Date: {creation_date}\n")
            self.results_text.insert(tk.END, f"File Size: {stat.st_size} bytes\n")
            self.results_text.insert(tk.END, f"File Path: {file_path}\n\n")
        except Exception as e:
            self.results_text.insert(tk.END, f"Error fetching file metadata: {str(e)}\n\n")
        
        # Image Metadata (EXIF)
        try:
            with open(file_path, 'rb') as f:
                tags = exifread.process_file(f)
                
                # Creation Date from EXIF
                exif_date = tags.get('EXIF DateTimeOriginal')
                if exif_date:
                    self.results_text.insert(tk.END, f"EXIF Capture Date: {str(exif_date)}\n")
                
                # Location (GPS)
                gps_info = tags.get('GPS GPSInfo')
                if gps_info:
                    lat = tags.get('GPS GPSLatitude')
                    lon = tags.get('GPS GPSLongitude')
                    if lat and lon:
                        self.results_text.insert(tk.END, f"GPS Location: Latitude {str(lat)}, Longitude {str(lon)}\n")
                else:
                    self.results_text.insert(tk.END, "No GPS location data found.\n")
                
                # System/Camera Info
                make = tags.get('Image Make')
                model = tags.get('Image Model')
                software = tags.get('Image Software')
                if make:
                    self.results_text.insert(tk.END, f"Camera Make: {str(make)}\n")
                if model:
                    self.results_text.insert(tk.END, f"Camera Model: {str(model)}\n")
                if software:
                    self.results_text.insert(tk.END, f"Software: {str(software)}\n")
                
                # Other Metadata
                self.results_text.insert(tk.END, "\nFull EXIF Metadata:\n")
                for tag in tags:
                    self.results_text.insert(tk.END, f"{tag}: {str(tags[tag])}\n")
                
                # Source Details (inferred from metadata)
                self.results_text.insert(tk.END, "\nSource Details: Inferred from EXIF data above (e.g., camera, software).\n")
        except Exception as e:
            self.results_text.insert(tk.END, f"Error fetching EXIF metadata: {str(e)}\n")
            self.results_text.insert(tk.END, "Note: Some images (e.g., PNG, BMP) may not have EXIF data.\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageInspectorApp(root)
    root.mainloop()