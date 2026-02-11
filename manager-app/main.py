import os
import secrets
import json
import shutil
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk

# KONFIGURASI PATH
BASE_PATH = os.path.join(os.path.dirname(__file__), "..", "src", "assets", "artwork")
JSON_PATH = os.path.join(BASE_PATH, "artworks.json")

class ArtworkCMS:
    def __init__(self, root):
        self.root = root
        self.root.title("Artwork Global CMS - Visual Manager")
        self.root.geometry("1200x900")
        self.root.configure(bg="#1e1e1e")
        
        self.img_cache = []
        self.current_cat = None
        self.show_main_menu()

    def clear_screen(self):
        self.img_cache = []
        for widget in self.root.winfo_children():
            widget.destroy()

    def get_thumbnail(self, path, size=(80, 80)):
        try:
            img = Image.open(path)
            img.thumbnail(size)
            photo = ImageTk.PhotoImage(img)
            self.img_cache.append(photo)
            return photo
        except:
            return None

    # --- FUNGSI GIT PUSH ---
    def git_sync_global(self):
        """Push semua perubahan (Gambar + JSON) ke GitHub sekaligus"""
        if not messagebox.askyesno("Git Deploy", "Kirim semua perubahan ke GitHub/Website sekarang?"):
            return

        try:
            # Cari root folder (asumsi .git ada di satu tingkat di atas script)
            root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            
            # Eksekusi Git Command
            subprocess.run(["git", "add", "."], cwd=root_dir, check=True)
            subprocess.run(["git", "commit", "-m", "CMS: Global Gallery Update"], cwd=root_dir, check=True)
            subprocess.run(["git", "push", "origin", "main"], cwd=root_dir, check=True)
            
            messagebox.showinfo("Git Success", "Mantap! Perubahan sudah live di GitHub. 🚀")
        except Exception as e:
            messagebox.showerror("Git Error", f"Gagal Push! Cek koneksi atau pastikan branch lu 'main'.\n{e}")

    def show_main_menu(self):
        self.clear_screen()
        frame = tk.Frame(self.root, bg="#1e1e1e")
        frame.pack(expand=True)
        
        tk.Label(frame, text="ARTWORK MANAGER", font=("Arial", 28, "bold"), fg="#4a9eff", bg="#1e1e1e").pack(pady=10)
        tk.Label(frame, text="Select folder to edit or push changes to web", fg="#888", bg="#1e1e1e").pack(pady=5)
        
        # Grid Tombol Kategori
        btn_container = tk.Frame(frame, bg="#1e1e1e")
        btn_container.pack(pady=30)
        
        categories = ['2d', '3d', 'illustration', 'WIP']
        for cat in categories:
            tk.Button(btn_container, text=cat.upper(), width=15, height=6, bg="#333", fg="white",
                      font=("Arial", 10, "bold"), relief="flat",
                      command=lambda c=cat: self.show_content_grid(c)).pack(side="left", padx=10)

        # --- TOMBOL PUSH GLOBAL ---
        # Ditaruh di folder utama (Main Menu)
        tk.Frame(frame, height=2, bg="#333").pack(fill="x", pady=20) # Garis pemisah
        
        push_btn = tk.Button(frame, text="🚀 DEPLOY ALL CHANGES TO WEB", 
                             width=40, height=3, bg="#6f42c1", fg="white",
                             font=("Arial", 12, "bold"), relief="flat",
                             command=self.git_sync_global)
        push_btn.pack(pady=10)
        
        tk.Label(frame, text="Note: Ini akan nge-push semua gambar baru dan file JSON ke GitHub", 
                 font=("Arial", 9, "italic"), fg="#555", bg="#1e1e1e").pack()

    # --- BAGIAN GRID & EDITOR (Sama seperti sebelumnya) ---
    def show_content_grid(self, category):
        self.current_cat = category
        self.clear_screen()
        header = tk.Frame(self.root, bg="#333", height=60)
        header.pack(fill="x")
        tk.Button(header, text="< BACK", bg="#444", fg="white", command=self.show_main_menu).pack(side="left", padx=15, pady=10)
        
        canvas = tk.Canvas(self.root, bg="#1e1e1e", highlightthickness=0)
        grid = tk.Frame(canvas, bg="#1e1e1e")
        scroll = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        canvas.create_window((0,0), window=grid, anchor="nw")

        path = os.path.join(BASE_PATH, category)
        if not os.path.exists(path): os.makedirs(path)
        files = os.listdir(path)
        groups = {}
        for f in sorted(files):
            if "_" in f and not f.endswith('.json'):
                cid = f.split('_')[0]
                if cid not in groups: groups[cid] = []
                groups[cid].append(f)

        for i, (cid, slides) in enumerate(groups.items()):
            thumb = self.get_thumbnail(os.path.join(path, slides[0]), (150, 150))
            btn = tk.Button(grid, image=thumb, text=f"ID: {cid}\n{len(slides)} Slides", 
                            compound="top", bg="#2d2d2d", fg="white", font=("Arial", 9),
                            command=lambda c=cid, s=slides: self.open_content_editor(c, s))
            btn.grid(row=i//5, column=i%5, padx=15, pady=15)
            
        grid.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def open_content_editor(self, content_id, slides):
        self.clear_screen()
        self.editing_slides = list(slides)
        path = os.path.join(BASE_PATH, self.current_cat)
        
        edit_frame = tk.Frame(self.root, bg="#1e1e1e")
        edit_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Panel Kiri (Visual Slides)
        left_panel = tk.Frame(edit_frame, width=400, bg="#2d2d2d")
        left_panel.pack(side="left", fill="both")
        
        self.slide_canvas = tk.Canvas(left_panel, bg="#111", highlightthickness=0)
        self.slide_inner = tk.Frame(self.slide_canvas, bg="#111")
        self.slide_canvas.pack(side="top", fill="both", expand=True, padx=5)
        self.slide_canvas.create_window((0,0), window=self.slide_inner, anchor="nw")
        
        self.refresh_visual_slides()
        tk.Button(left_panel, text="+ IMPORT", bg="#27ae60", fg="white", command=self.import_files).pack(fill="x", padx=10, pady=10)

        # Panel Kanan (Form)
        right_panel = tk.Frame(edit_frame, bg="#1e1e1e")
        right_panel.pack(side="right", fill="both", expand=True, padx=20)
        
        tk.Label(right_panel, text="JUDUL:", fg="white", bg="#1e1e1e").pack(anchor="w")
        self.ent_title = tk.Entry(right_panel, font=("Arial", 12), bg="#333", fg="white"); self.ent_title.pack(fill="x", pady=5)
        
        tk.Label(right_panel, text="DESKRIPSI:", fg="white", bg="#1e1e1e").pack(anchor="w")
        self.txt_desc = tk.Text(right_panel, height=6, bg="#333", fg="white"); self.txt_desc.pack(fill="x", pady=5)

        footer = tk.Frame(self.root, bg="#1e1e1e")
        footer.pack(side="bottom", fill="x")
        tk.Button(footer, text="CANCEL", bg="#c0392b", fg="white", command=lambda: self.show_content_grid(self.current_cat)).pack(side="left", padx=20, pady=10)
        tk.Button(footer, text="SAVE", bg="#f39c12", fg="white", command=lambda: self.final_save(content_id)).pack(side="right", fill="x", expand=True, padx=20, pady=10)

    def refresh_visual_slides(self):
        for w in self.slide_inner.winfo_children(): w.destroy()
        path = os.path.join(BASE_PATH, self.current_cat)
        for i, filename in enumerate(self.editing_slides):
            row = tk.Frame(self.slide_inner, bg="#222", pady=5)
            row.pack(fill="x", pady=2, padx=5)
            thumb = self.get_thumbnail(os.path.join(path, filename))
            tk.Label(row, image=thumb, bg="#222").pack(side="left", padx=5)
            tk.Button(row, text="X", bg="#cc0000", fg="white", command=lambda f=filename: self.remove_slide(f)).pack(side="right", padx=10)
        self.slide_inner.update_idletasks()
        self.slide_canvas.config(scrollregion=self.slide_canvas.bbox("all"))

    def remove_slide(self, filename):
        self.editing_slides.remove(filename)
        self.refresh_visual_slides()

    def import_files(self):
        files = filedialog.askopenfilenames()
        if files:
            dest = os.path.join(BASE_PATH, self.current_cat)
            for f in files:
                name = f"NEW_{secrets.token_hex(2)}_{os.path.basename(f)}"
                shutil.copy(f, os.path.join(dest, name))
                self.editing_slides.append(name)
            self.refresh_visual_slides()

    def final_save(self, old_id):
        path = os.path.join(BASE_PATH, self.current_cat)
        new_id = secrets.token_hex(4)
        final_files = []
        for i, old_name in enumerate(self.editing_slides):
            ext = old_name.split('.')[-1]
            new_name = f"{new_id}_{i+1}.{ext}"
            os.rename(os.path.join(path, old_name), os.path.join(path, new_name))
            final_files.append(new_name)

        self.update_json(old_id, new_id, self.ent_title.get(), self.txt_desc.get("1.0", tk.END).strip(), final_files)
        messagebox.showinfo("Saved", "Data disimpan secara lokal.")
        self.show_content_grid(self.current_cat)

    def update_json(self, old_id, new_id, title, desc, slides):
        data = []
        if os.path.exists(JSON_PATH):
            with open(JSON_PATH, 'r', encoding='utf-8') as f:
                try: data = json.load(f)
                except: data = []
        data = [item for item in data if item.get('id') != old_id]
        data.append({"id": new_id, "category": self.current_cat, "title": title, "description": desc, "slides": slides})
        with open(JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = ArtworkCMS(root)
    root.mainloop()