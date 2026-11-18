from tkinter import filedialog
import pygame as pg
from PIL import Image
import customtkinter as ctk
import yt_dlp as y
import os
import json

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("gold")

JSON_B = "biblioteca.json"

class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Culke")
        self.geometry("650x500")

        pg.mixer.init()

        self.current_ruta = None
        self.is_playing = False

        self.gui_reproductor()

    def gui_reproductor(self):

        self.panel_izq = ctk.CTkFrame(self, fg_color="Gray", corner_radius=40, width=350)
        self.panel_izq.pack(side="left", fill="both", expand=False, pady=10, padx=10)

        self.lbl_nombre = ctk.CTkLabel(
            self.panel_izq, text="MUSICA", font=("Arial", 16, "bold")
        )
        self.lbl_nombre.pack(pady=(20, 10))

        self.img_frame = ctk.CTkFrame(self.panel_izq,
            border_color="White",
            border_width=2,
            width=350,
            height=250
        )
        self.img_frame.pack(pady=10)
        self.img_frame.propagate(False)

        self.lbl_img = ctk.CTkLabel(
            self.img_frame,
            text="[ Sin Reproducir ]", 
            font=("Arial", 12)
        )
        self.lbl_img.pack(expand=True)

        self.fila_butons = ctk.CTkFrame(self.panel_izq, fg_color="transparent")
        self.fila_butons.pack(pady=15)

        self.butonA = ctk.CTkButton(
            self.fila_butons, 
            command=self.back,
            text="<<",
            width=100,
            height=40,
            font=("Arial", 16, "bold")
        )
        self.butonA.pack(pady=10, side="left")

        self.butonP = ctk.CTkButton(
            self.fila_butons, 
            command=self.play,
            text="Play",
            width=100,
            height=40,
            font=("Arial", 16, "bold")
        )
        self.butonP.pack(pady=10, side="left")

        self.butonN = ctk.CTkButton(
            self.fila_butons, 
            command=self.next,
            text=">>",
            width=100,
            height=40,
            font=("Arial", 16, "bold")
        )
        self.butonN.pack(pady=10, side="left")

        self.panel_drc = ctk.CTkFrame(self, fg_color="Black", corner_radius=40, width=350)
        self.panel_drc.pack(side="left", fill="both", expand=True, pady=10)

        self.lbl_x = ctk.CTkLabel(
            self.panel_drc, text="Mi Musica", font=("Arial", 14, "bold")
        )
        self.lbl_x.pack(pady=15)

        self.scrollArea = ctk.CTkScrollableFrame(
            self.panel_drc, width=250, height=320, fg_color="#121212"
        )
        self.scrollArea.pack(padx=10, pady=5)

        self.actions = ctk.CTkFrame(
            self.panel_drc, fg_color="transparent"
        )
        self.actions.pack(side="bottom", pady=10)

        self.butonD = ctk.CTkButton(
            self.actions, 
            command=self.descarga,
            text="Descargar(url)",
            width=70
        )
        self.butonD.pack(pady=10, side="left")

        self.butonI = ctk.CTkButton(
            self.actions, 
            command=self.importar,
            text="Importar(MP3/MP4)",
            width=70
        )
        self.butonI.pack(pady=10, side="left")

        self.act_list()

#==============FUNCIONES==================

    def car_json(self):
        if os.path.exists(JSON_B):
            with open(JSON_B, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    def meter_json(self, titulo, ruta):

        libreria = self.car_json()

        entry = {"ruta": ruta, "titulo": titulo}

        libreria.append(entry)

        with open(JSON_B, "w", encoding="utf-8") as f:
            json.dump(libreria, f, indent=4, ensure_ascii=False)

    def act_list(self):

        for widget in self.scrollArea.winfo_children():
            widget.destroy()

        biblioteca = self.car_json()

        if not biblioteca:
            lbl_vacio = ctk.CTkLabel(
                self.scrollArea, text="No hay canciones aún", text_color="#888888"
            )
            lbl_vacio.pack(pady=20)
            return

        for item in biblioteca:
            titulo = item.get("titulo", "Sin titulo")
            ruta = item.get("ruta", "")

            icono = "🎬"

            btn_cancion = ctk.CTkButton(
                self.scrollArea,
                text=f"{icono} {titulo}",
                anchor="w",
                fg_color="transparent",
                hover_color="#2b2b2b",
                text_color="#ffffff",
                command=lambda r=ruta, tit=titulo: self.reproducir_pista(
                    r, tit
                ),
            )
            btn_cancion.pack(fill="x", pady=2, padx=5)

    def reproducir_pista(self, ruta, titulo):
        if not os.path.exists(ruta):
            print(f"El archivo no existe: {ruta}")
            return

        self.current_ruta = ruta
        self.lbl_nombre.configure(text=titulo)

        try:
            pg.mixer.music.load(ruta)
            pg.mixer.music.play()
            self.is_playing = True
            self.butonP.configure(text="Pause")
        except Exception as e:
            print(f"Error al reproducir con Pygame: {e}")

        self.lbl_img.configure(image="", text="🎵 [ Archivo MP3 ]")

    def play(self):
        if not self.current_ruta:
            print("No hay pista seleccionada")
            return

        if self.is_playing:
            pg.mixer.music.pause()
            self.is_playing = False
            self.butonP.configure(text="Play")

        else:
            pg.mixer.music.unpause()
            self.is_playing = True
            self.butonP.configure(text="Pause")

    def next(self):
        biblioteca = self.car_json()
        if not biblioteca:
            return
        try:
            idx = next(
                i
                for i, item in enumerate(biblioteca)
                if item["ruta"] == self.current_ruta
            )
            sig_idx = (idx + 1) % len(biblioteca)
        except (StopIteration, TypeError):
            sig_idx = 0

        pista = biblioteca[sig_idx]
        self.reproducir_pista(pista["ruta"], pista["titulo"])

    def back(self):
        biblioteca = self.car_json()
        if not biblioteca:
            return
        try:
            idx = next(
                i
                for i, item in enumerate(biblioteca)
                if item["ruta"] == self.current_ruta
            )
            ant_idx = (idx - 1) % len(biblioteca)
        except (StopIteration, TypeError):
            ant_idx = len(biblioteca) - 1

        pista = biblioteca[ant_idx]
        self.reproducir_pista(pista["ruta"], pista["titulo"])

    def descarga(self):
        Descarga(master=self)

    def importar(self):

        archivos = filedialog.askopenfilenames(
            title="Seleccionar archivos multimedia",
        filetypes=[
            ("Archivos multimedia", "*.mp3")
            ]
        )

        if not archivos:
            return

        biblioteca = self.car_json()

        for archivo in archivos:

            name_ext = os.path.basename(archivo)
            name, ext = os.path.splitext(name_ext)

            titulo = name.replace("_", " ").title()

            exist = any(item.get("ruta") == archivo for item in biblioteca)

            if not exist:
                self.meter_json(titulo, archivo)

            self.act_list()


#===========================================================================
#==========================Pestana de Descarga==============================
#===========================================================================

class Descarga(ctk.CTkToplevel):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.title("Descarga")
        self.geometry("400x500")

        self.master_app = master

        self.gui_des()

    def gui_des(self):
        self.url_entry = ctk.CTkEntry(
            self,
            placeholder_text="Pega tu enlace aqui...",
            width=400,
        )
        self.url_entry.pack(pady=40)

        self.filaRuta = ctk.CTkFrame(self, fg_color="transparent")
        self.filaRuta.pack(pady=20, padx=20, fill="x")

        self.entryB = ctk.CTkEntry(
            self.filaRuta,
            placeholder_text="Carpeta de destino",
        )
        self.entryB.pack(side="left", expand=True, fill="x", padx=(0, 8))

        self.broserB = ctk.CTkButton(
            self.filaRuta,
            text="Examinar...",
            width=90,
            command=self.broser,
            text_color="Black",
        )
        self.broserB.pack(side="left")

        self.button = ctk.CTkButton(
            self,
            text="Descargar",
            command=self.descarga,
            text_color="Black",
        )
        self.button.pack(pady=10)

    def broser(self):
        location = filedialog.askdirectory()
        if location:
            self.entryB.delete(0, ctk.END)
            self.entryB.insert(0, location)

    def descarga(self):
        url = self.url_entry.get()
        ruta = self.entryB.get()

        if not ruta:
            ruta = "."

        if not url:
            return

        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "outtmpl": f"{ruta}/%(title)s.%(ext)s",
        }

        try:
            with y.YoutubeDL(ydl_opts) as yd:
                info = yd.extract_info(url, download=True)
                titulo = info.get("title", "Audio de YouTube")

                filename = yd.prepare_filename(info)
                filename_mp3 = os.path.splitext(filename)[0] + ".mp3"

                if self.master_app:
                    self.master_app.meter_json(titulo, filename_mp3)
                    self.master_app.act_list()

            self.destroy()

        except Exception as e:
            print(f"Error en la descarga: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
