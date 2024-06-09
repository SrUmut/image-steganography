# Default modules
import tkinter as tk
from tkinter import filedialog
import os

# Modules that need to be downloaded
import ttkbootstrap as ttk
import rsa

# My modules
from hide_data import ALPHA_LEVEL
import hide_data as hd
import extract_data as ed

def get_input_path(variable, file_types):
    initial_dir = os.getcwd()
    file_path = filedialog.askopenfilename(initialdir=initial_dir, title="Select File", filetypes=file_types)
    variable.set(file_path)

def get_output_path(variable, file_types):
    initial_dir = os.getcwd()
    file_path = filedialog.asksaveasfilename(initialdir=initial_dir, title="Save File", filetypes=file_types)
    variable.set(file_path)

def toggle_enc():
    # if buttton is checked show encryption elements
    if hd_enc_checkbox_var.get():
        hd_hide_button.pack_forget()
        hd_enc_key_frame.pack(padx=10, pady=10, fill="x")
        #hd_can_enc_button.pack(padx=10, pady=10)
        hd_hide_button.pack(padx=10, pady=10)
    # if buttton is unchecked hide encryption elements
    else:
        hd_enc_key_frame.pack_forget()
        #hd_can_enc_button.pack_forget()

def toggle_dec():
    # if buttton is checked show decryption elements
    if ed_dec_checkbox_var.get():
        ed_extract_button.pack_forget()
        ed_dec_key_frame.pack(fill="x", padx=10, pady=10)
        ed_extract_button.pack(padx=10, pady=10)
    else:
        ed_dec_key_frame.pack_forget()

def get_key(path, type):
    try:
        with open(path, "rb") as f:
            match type:
                case "Public Key":
                    return rsa.PublicKey.load_pkcs1(f.read())
                case "Private Key":
                    return rsa.PrivateKey.load_pkcs1(f.read())
    except:
        return False
                    
def hide():
    key = None
    # if encryption is checked
    if hd_enc_checkbox_var.get():
        key_path = hd_enc_key_path.get()
        key = get_key(key_path, hd_enc_key_type_var.get())
        # if get key returned false raise error
        if not key:
            tk.messagebox.showwarning("Error", f"Please provide a legit key!")
    process = hd.main(hd_input_image_path.get(), hd_input_file_path.get(), hd_output_image_path.get(), key)
    if process == hd.DONE:
        tk.messagebox.showinfo("Hiding Complete", f"Data is successfully hidden.")
    elif process == hd.NES:
        tk.messagebox.showwarning("Error", f"Not enough space for data!")
    elif process == hd.ENC_ERR:
        tk.messagebox.showwarning("Error", f"Problem with encryption! Data might be too large to encrypt.")
        

def extract():
    key = None
    # if decrpytion is checked
    if ed_dec_checkbox_var.get():
        key_path = ed_dec_key_path.get()
        key = get_key(key_path, ed_dec_key_type_var.get())
        if not key:
            tk.messagebox.showwarning("Error", f"Please provide a legit key!")
    if ed.main(ed_input_image_path.get(), ed_output_file_path.get(), key):
        tk.messagebox.showinfo("Extraction Complete", f"Data is successfully extracted.")
    else:
        tk.messagebox.showinfo("Complete", f"Extraction failed!")


window = ttk.Window()
window.title("PNG Steganography")
window.geometry("720x480")
window.resizable(False, False)
notebook = ttk.Notebook(window)


key_types = ("Public Key", "Private Key")


### Hide Data
hide_data = ttk.Frame(notebook)

## input image
hd_input_image_frame = ttk.Frame(hide_data)
hd_input_image_button = ttk.Button(hd_input_image_frame, text="Input Image", command= lambda: get_input_path(hd_input_image_path, [("PNG Image", "*.png")]))
hd_input_image_path = tk.StringVar()
hd_input_image_entry = ttk.Entry(hd_input_image_frame, textvariable=hd_input_image_path)

hd_input_image_button.pack(side="left", padx=(0, 10))
hd_input_image_entry.pack(side="left", expand=True, fill="x")
hd_input_image_frame.pack(fill="x", padx=10, pady=10)

## input file
hd_input_file_frame = ttk.Frame(hide_data)
hd_input_file_button = ttk.Button(hd_input_file_frame, text="Input File", command=lambda: get_input_path(hd_input_file_path, [("Input File", "*")]))
hd_input_file_path = tk.StringVar()
hd_input_file_entry = ttk.Entry(hd_input_file_frame, textvariable=hd_input_file_path)

hd_input_file_button.pack(side="left", padx=(0, 10))
hd_input_file_entry.pack(side="left", expand=True, fill="x")
hd_input_file_frame.pack(fill="x", padx=10, pady=10)

## output image (steganographic image)
hd_output_image_frame = ttk.Frame(hide_data)
hd_output_image_button = ttk.Button(hd_output_image_frame, text="Output Image", command= lambda: get_output_path(hd_output_image_path, [("Output PNG", "*.png")]))
hd_output_image_path = tk.StringVar()
hd_output_image_entry = ttk.Entry(hd_output_image_frame, textvariable=hd_output_image_path)

hd_output_image_button.pack(side="left", padx=(0, 10))
hd_output_image_entry.pack(side="left", expand=True, fill="x")
hd_output_image_frame.pack(fill="x", padx=10, pady=10)


## encryption
hd_enc_checkbox_var = tk.BooleanVar(value=False)
hd_enc_checkbox = ttk.Checkbutton(hide_data, text="RSA Encryption", variable=hd_enc_checkbox_var, command=lambda: toggle_enc())
hd_enc_checkbox.pack(padx=10, pady=10)

hd_enc_key_frame = ttk.Frame(hide_data)
hd_enc_key_button = ttk.Button(hd_enc_key_frame, text="Encryption Key", command=lambda: get_input_path(hd_enc_key_path, [("", "*.txt"), ("", "*.key"), ("", "*.pem")]))
hd_enc_key_path = tk.StringVar()
hd_enc_key_entry = ttk.Entry(hd_enc_key_frame, textvariable=hd_enc_key_path)
hd_enc_key_type_var = tk.StringVar(value=key_types[0])
hd_enc_key_type_combobox = ttk.Combobox(hd_enc_key_frame, values=key_types, textvariable=hd_enc_key_type_var)

hd_enc_key_button.pack(side="left", padx=(0, 10))
hd_enc_key_entry.pack(side="left", padx=(0, 10), expand=True, fill="x")
hd_enc_key_type_combobox.pack(side="left")
#hd_enc_key_frame.pack(padx=10, pady=10, fill="x")

#hd_can_enc_button = ttk.Button(hide_data, text="Can Encrypt?", command=lambda: can_encrypt())
#hd_can_enc_button.pack(padx=10, pady=10)

## hide button
hd_hide_button = ttk.Button(hide_data, text="Hide", command=lambda: hide())
hd_hide_button.pack(padx=10, pady=10)




### Extract Data
extract_data = ttk.Frame(notebook)

## input image
ed_input_image_frame = ttk.Frame(extract_data)
ed_input_image_button = ttk.Button(ed_input_image_frame, text="Input Image", command=lambda: get_input_path(ed_input_image_path, [("PNG Image", "*.png")]))
ed_input_image_path = tk.StringVar()
ed_input_image_entry = ttk.Entry(ed_input_image_frame, textvariable=ed_input_image_path)

ed_input_image_button.pack(side="left", padx=(0, 10))
ed_input_image_entry.pack(side="left", expand=True, fill="x")
ed_input_image_frame.pack(padx=10, pady=10, fill="x")

## output file
ed_output_file_frame = ttk.Frame(extract_data)
ed_output_file_button = ttk.Button(ed_output_file_frame, text="Output File", command=lambda: get_output_path(ed_output_file_path, [("Just file name", "*.*")]))
ed_output_file_path = tk.StringVar()
ed_output_file_entry = ttk.Entry(ed_output_file_frame, textvariable=ed_output_file_path)

ed_output_file_button.pack(side="left", padx=(0, 10))
ed_output_file_entry.pack(side="left", expand=True, fill="x")
ed_output_file_frame.pack(padx=10, pady=10, fill="x")

## decryption
ed_dec_checkbox_var = tk.BooleanVar(value=False)
ed_dec_checkbox = ttk.Checkbutton(extract_data, text="RSA Decryption", variable=ed_dec_checkbox_var, command=lambda: toggle_dec())
ed_dec_key_frame = ttk.Frame(extract_data)
ed_dec_key_button = ttk.Button(ed_dec_key_frame, text="Decryption Key", command=lambda: get_input_path(ed_dec_key_path, [("", "*.txt"), ("", "*.key"), ("", "*.pem")]))
ed_dec_key_path = tk.StringVar()
ed_dec_key_entry = ttk.Entry(ed_dec_key_frame, textvariable=ed_dec_key_path)
ed_dec_key_type_var = tk.StringVar(value=key_types[0])
ed_dec_key_type_combo = ttk.Combobox(ed_dec_key_frame, values=key_types, textvariable=ed_dec_key_type_var)

ed_dec_checkbox.pack(padx=10, pady=10)
ed_dec_key_button.pack(side="left", padx=(0, 10))
ed_dec_key_entry.pack(side="left", padx=(0, 10), expand=True, fill="x")
ed_dec_key_type_combo.pack(side="left")
#ed_dec_key_frame.pack(fill="x", padx=10, pady=10)

## extract button
ed_extract_button = ttk.Button(extract_data, text="Extract", command=lambda: extract())
ed_extract_button.pack(padx=10, pady=10)



notebook.add(hide_data, text="Hide Data")
notebook.add(extract_data, text="Extract Data")
notebook.pack(expand=True, fill="both")

window.mainloop()
