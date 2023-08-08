import tkinter as tk
from tkinter import filedialog
from PIL import Image
import os

def resize_image():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    try:
        original_image = Image.open(file_path)
        resized_image = original_image.resize((216, 216))
        filename, file_extension = os.path.splitext(os.path.basename(file_path))
        destination_folder = filedialog.askdirectory()
        if not destination_folder:
            return
        resized_image.save(os.path.join(destination_folder, f"resized_{filename}{file_extension}"))
        result_label.config(text="Image resized and saved successfully.", fg="green")
    except Exception as e:
        result_label.config(text=f"Error resizing and saving image: {e}", fg="red")

def main():
    root = tk.Tk()
    root.title("Image Resizer")

    label = tk.Label(root, text="Click the button to resize an image.")
    label.pack(pady=10)

    button = tk.Button(root, text="Select Image", command=resize_image)
    button.pack(pady=10)

    global result_label
    result_label = tk.Label(root, text="", fg="green")
    result_label.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
