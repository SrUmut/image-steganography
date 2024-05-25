import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog
import os
import hide_data as hd
import extract_data as ed
import rsa

def get_key(path, key_type):
    match key_type:
        case "RSA Public Key":
            with open(path, "rb") as f:
                return rsa.PublicKey.load_pkcs1(f.read())
        case "RSA Private Key":
            with open(path, "rb") as f:
                return rsa.PrivateKey.load_pkcs1(f.read())

def hide():
    # if encrytion is checked
    if enc_checkbox_var.get():
        if encryption_key_type_combo.get() == "RSA Public Key":
            if can_encrypt():
                key_path = encryption_key_path.get()
                key = get_key(key_path, encryption_key_type_var.get())
                done = hd.hide(hd_input_image_path.get(), hd_input_file_path.get(), hd_output_image_path.get(), key)
    # if encryption is not checked
    else:
        done = hd.hide(hd_input_image_path.get(), hd_input_file_path.get(), hd_output_image_path.get())
    if done == hd.TOO_LARGE_DATA:
        tk.messagebox.showwarning("Error", f"Data size is too large for the image.")
    if not done:
        tk.messagebox.showinfo("Complete", f"Data is successfully hidden in the image.")


def extract():
    print("Extracting data...")
    # if decryption is checked
    if dec_checkbox_var.get():
        key_path = decryption_key_path.get()
        key = get_key(key_path, decryption_key_type_var.get())
        ed.extract(ed_input_image_path.get(), ed_output_file_path.get(), key)
    # if decryption is not checked
    else:
        ed.extract(ed_input_image_path.get(), ed_output_file_path.get())
    print("Extraction is complete!")

def get_input_path(variable, filetypes):
    initial_dir = os.getcwd()
    file_path = filedialog.askopenfilename(initialdir=initial_dir, title="Select File", filetypes=filetypes)
    variable.set(file_path)

def get_output_path(variable, filetypes):
    initial_dir = os.getcwd()
    file_path = filedialog.asksaveasfilename(initialdir=initial_dir, title="Save File", filetypes=filetypes)
    variable.set(file_path)

def toggle_encryption():
    if enc_checkbox_var.get():
        start_button.pack_forget()
        encryption_key_frame.pack(fill="x", padx=10, pady=10)
        can_encrypt_button.pack(padx=10, pady=10)
        start_button.pack(padx=10, pady=10)
    else:
        encryption_key_frame.pack_forget()
        can_encrypt_button.pack_forget()

def toggle_decryption():
    if dec_checkbox_var.get():
        ed_start_button.pack_forget()
        decryption_key_frame.pack(fill="x", padx=10, pady=10)
        ed_start_button.pack(padx=10, pady=10)
    else:
        decryption_key_frame.pack_forget()

def max_data_size_for_enc(key):
    return rsa.common.bit_size(key.n) // 8 - 11

def can_encrypt():
    key_path = encryption_key_path.get()
    with open(key_path, "rb") as f:
        try:
            key = rsa.PublicKey.load_pkcs1(f.read())
        except:
            tk.messagebox.showwarning("Error", "Invalid key file.")
            return False
    file_path = hd_input_file_path.get()
    if os.path.getsize(file_path) > max_data_size_for_enc(key):
        tk.messagebox.showwarning("Error", f"Data size is too large. Maximum data size: {max_data_size_for_enc(key)} bytes")
        return False
    tk.messagebox.showwarning("Can Encrypt", f"You can encrypt.")
    return True
    
window = ttk.Window()
window.title("PNG Steganography")
window.geometry("720x480")
window.resizable(False, False)

notebook = ttk.Notebook(window)


## Hide Data
hide_data = ttk.Frame(notebook)

# input image
hd_input_image_frame = ttk.Frame(hide_data)
hd_input_image_button = ttk.Button(hd_input_image_frame, text="Input Image", command=lambda: get_input_path(hd_input_image_path, [("PNG Image", "*.png")]))
hd_input_image_button.pack(side="left")
hd_input_image_path = tk.StringVar()
hd_input_image_entry = ttk.Entry(hd_input_image_frame, width=60, textvariable=hd_input_image_path)
hd_input_image_entry.pack(side="left", padx=10)
hd_input_image_frame.pack(fill="x", padx=10, pady=10)

# input file
hd_input_file_frame = ttk.Frame(hide_data)
hd_input_file_button = ttk.Button(hd_input_file_frame, text="Input File", command=lambda: get_input_path(hd_input_file_path, [("File to Hide", "*")]))
hd_input_file_button.pack(side="left")
hd_input_file_path = tk.StringVar()
hd_input_file_entry = ttk.Entry(hd_input_file_frame, width=60, textvariable=hd_input_file_path)
hd_input_file_entry.pack(side="left", padx=10)
hd_input_file_frame.pack(fill="x", padx=10, pady=10)


# output image
hd_output_image_frame = ttk.Frame(hide_data)
hd_output_image_button = ttk.Button(hd_output_image_frame, text="Output Image", command=lambda: get_output_path(hd_output_image_path, [("PNG Image", "*.png")]))
hd_output_image_button.pack(side="left")
hd_output_image_path = tk.StringVar()
hd_output_image_entry = ttk.Entry(hd_output_image_frame, width=60, textvariable=hd_output_image_path)
hd_output_image_entry.pack(side="left", padx=10)
hd_output_image_frame.pack(fill="x", padx=10, pady=10)

# encryption
enc_checkbox_var = tk.BooleanVar(value=False)
encrypt_checkbox = ttk.Checkbutton(hide_data, text="Encrypt Data", variable=enc_checkbox_var, command=lambda: toggle_encryption())
encrypt_checkbox.pack(padx=10, pady=10)

encryption_key_frame = ttk.Frame(hide_data)
encryption_button = ttk.Button(encryption_key_frame, text="Encryption Key", command=lambda: get_input_path(encryption_key_path, [("", "*.txt"), ("", "*.key"), ("", "*.pem")]))
encryption_button.pack(side="left")
encryption_key_path = tk.StringVar()
encryption_key_entry = ttk.Entry(encryption_key_frame, width=40, textvariable=encryption_key_path)
encryption_key_entry.pack(side="left", padx=10)
encryption_key_types = ("RSA Public Key", "")
encryption_key_type_var = tk.StringVar(value=encryption_key_types[0])
encryption_key_type_combo = ttk.Combobox(encryption_key_frame, values=encryption_key_types, textvariable=encryption_key_type_var)
encryption_key_type_combo.pack(side="left", padx=10)

can_encrypt_button = ttk.Button(hide_data, text="Can Encrypt?", command=lambda: can_encrypt())

# start button
start_button = ttk.Button(hide_data, text="Start", command=lambda: hide())
start_button.pack(padx=10, pady=10)




## Extract Data
extract_data = ttk.Frame(notebook)

# input image
ed_input_image_frame = ttk.Frame(extract_data)
ed_input_image_button = ttk.Button(ed_input_image_frame, text="Input Image", command=lambda: get_input_path(ed_input_image_path, [("PNG Image", "*.png")]))
ed_input_image_button.pack(side="left")
ed_input_image_path = tk.StringVar()
ed_input_image_entry = ttk.Entry(ed_input_image_frame, width=60, textvariable=ed_input_image_path)
ed_input_image_entry.pack(side="left", padx=10)
ed_input_image_frame.pack(fill="x", padx=10, pady=10)

# output file
ed_output_file_frame = ttk.Frame(extract_data)
ed_output_file_button = ttk.Button(ed_output_file_frame, text="Output File", command=lambda: get_output_path(ed_output_file_path, [("Just file name", "*.*")]))
ed_output_file_button.pack(side="left")
ed_output_file_path = tk.StringVar()
ed_output_file_entry = ttk.Entry(ed_output_file_frame, width=60, textvariable=ed_output_file_path)
ed_output_file_entry.pack(side="left", padx=10)
ed_output_file_frame.pack(fill="x", padx=10, pady=10)


# decryption
dec_checkbox_var = tk.BooleanVar(value=False)
decrypt_checkbox = ttk.Checkbutton(extract_data, text="Decrypt Data", variable=dec_checkbox_var, command=lambda: toggle_decryption())
decrypt_checkbox.pack(padx=10, pady=10)

decryption_key_frame = ttk.Frame(extract_data)
decryption_button = ttk.Button(decryption_key_frame, text="Decryption Key", command=lambda: get_input_path(decryption_key_path, [("", "*.txt"), ("", "*.key"), ("", "*.pem")]))
decryption_button.pack(side="left")
decryption_key_path = tk.StringVar()
decryption_key_entry = ttk.Entry(decryption_key_frame, width=40, textvariable=decryption_key_path)
decryption_key_entry.pack(side="left", padx=10)
decryption_key_types = ("RSA Private Key", "")
decryption_key_type_var = tk.StringVar(value=decryption_key_types[0])
decryption_key_type_combo = ttk.Combobox(decryption_key_frame, values=decryption_key_types, textvariable=decryption_key_type_var)
decryption_key_type_combo.pack(side="left", padx=10)

# start button
ed_start_button = ttk.Button(extract_data, text="Start", command=lambda: extract())
ed_start_button.pack(padx=10, pady=10)

notebook.add(hide_data, text="Hide Data")
notebook.add(extract_data, text="Extract Data")
notebook.pack(expand=True, fill="both")



# Events
#encrypt_checkbox.bind()

window.mainloop()

