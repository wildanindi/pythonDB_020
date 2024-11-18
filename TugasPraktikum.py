import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk

# Membuat database dan tabel jika belum ada
def create_database():
    conn = sqlite3.connect('nilai_siswa.db')  # Menghubungkan ke database
    cursor = conn.cursor()
    # Membuat tabel nilai_siswa dengan kolom id, nama_siswa, biologi, fisika, inggris, prediksi_fakultas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    ''')
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi

# Mengambil data dari database
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nilai_siswa")  # Mengambil semua data dari tabel
    rows = cursor.fetchall()  # Mengambil semua baris hasil query
    conn.close()
    return rows  # Mengembalikan data

# Menyimpan data baru ke database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    # Menyimpan data baru ke tabel nilai_siswa
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))
    conn.commit()
    conn.close()

# Memperbarui data di database
def update_database():
    selected_item = tree.selection()  # Memeriksa apakah ada data yang dipilih di Treeview
    if not selected_item:
        messagebox.showwarning("Warning", "Pilih data yang ingin diupdate.")
        return
    
    try:
        # Mengambil ID dari item yang dipilih dan nilai dari input
        record_id = tree.item(selected_item, 'values')[0]
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        # Memastikan nama tidak kosong
        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")
        
        prediksi = calculate_prediction(biologi, fisika, inggris)  # Menghitung prediksi fakultas

        # Mengupdate data di database berdasarkan ID
        conn = sqlite3.connect('nilai_siswa.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE nilai_siswa
            SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
            WHERE id = ?
        ''', (nama, biologi, fisika, inggris, prediksi, record_id))
        conn.commit()
        conn.close()

        # Menampilkan pesan sukses dan menyegarkan tampilan data
        messagebox.showinfo("Sukses", "Data berhasil diupdate.")
        clear_inputs()
        display_data()
    except ValueError as ve:
        # Menampilkan pesan error jika ada nilai input yang salah
        messagebox.showerror("Error", str(ve))
    except Exception as e:
        # Menampilkan pesan error untuk kesalahan lain
        messagebox.showerror("Error", "Terjadi kesalahan saat mengupdate data.")

# Menghapus data dari database
def delete_database():
    selected_item = tree.selection()  # Memeriksa apakah ada data yang dipilih di Treeview
    if not selected_item:
        messagebox.showwarning("Warning", "Pilih data yang ingin dihapus.")
        return
    
    # Mengambil ID dari item yang dipilih
    record_id = tree.item(selected_item, 'values')[0]
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))  # Menghapus data berdasarkan ID
    conn.commit()
    conn.close()

    # Menampilkan pesan sukses dan menyegarkan tampilan data
    messagebox.showinfo("Sukses", "Data berhasil dihapus.")
    clear_inputs()
    display_data()

# Menghitung prediksi fakultas berdasarkan nilai tertinggi
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak Diketahui"

# Menangani tombol Submit
def submit():
    try:
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        # Memastikan nama tidak kosong
        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")
        
        prediksi = calculate_prediction(biologi, fisika, inggris)  # Menghitung prediksi fakultas

        save_to_database(nama, biologi, fisika, inggris, prediksi)  # Menyimpan data ke database
        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
        
        clear_inputs()  # Membersihkan input
        display_data()  # Menyegarkan tampilan data
    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", "Terjadi kesalahan saat menyimpan data.")

# Membersihkan input
def clear_inputs():
    nama_var.set("")
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")

# Menampilkan data di Treeview
def display_data():
    for item in tree.get_children():  # Menghapus data di Treeview
        tree.delete(item)
    
    for row in fetch_data():  # Memasukkan data dari database ke Treeview
        tree.insert('', 'end', values=row)

# GUI setup menggunakan Tkinter
root = Tk()
root.title("Input Nilai Siswa")
root.geometry("600x400")

create_database()  # Membuat database

# Label dan Entry untuk input
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=10)
nama_var = StringVar()
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=20, pady=20)

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=10)
biologi_var = StringVar()
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=10)

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=10)
fisika_var = StringVar()
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=10)

Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=10)
inggris_var = StringVar()
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=10)

# Tombol untuk Submit, Update, dan Delete data
Button(root, text="Submit", command=submit).grid(row=4, column=0, padx=10, pady=10)
Button(root, text="Update", command=update_database).grid(row=4, column=1, padx=10, pady=10)
Button(root, text="Delete", command=delete_database).grid(row=4, column=2, padx=10, pady=10)

# Treeview untuk menampilkan data
columns = ('id', 'nama_siswa', 'biologi', 'fisika', 'inggris', 'prediksi_fakultas')
tree = ttk.Treeview(root, columns=columns, show='headings')
tree.heading('id', text='ID')
tree.heading('nama_siswa', text='Nama Siswa')
tree.heading('biologi', text='Biologi')
tree.heading('fisika', text='Fisika')
tree.heading('inggris', text='Inggris')
tree.heading('prediksi_fakultas', text='Prediksi Fakultas')

tree.column('id', width=30)
tree.column('nama_siswa', width=100)
tree.column('biologi', width=60)
tree.column('fisika', width=60)
tree.column('inggris', width=60)
tree.column('prediksi_fakultas', width=100)

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)  # Menempatkan Treeview

display_data()  # Menampilkan data awal
root.mainloop()  # Menjalankan aplikasi
