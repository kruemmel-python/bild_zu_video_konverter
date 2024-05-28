# Importieren der benötigten Module
import cv2  # OpenCV für Bild- und Videobearbeitung
import os  # Betriebssystemfunktionen, z.B. zum Löschen von Dateien
import tkinter as tk  # Tkinter für die GUI-Erstellung
from tkinter import filedialog  # Dialogfenster zum Öffnen und Speichern von Dateien
from PIL import Image, ImageTk  # PIL für Bildbearbeitung und Tkinter-Integration

# Initialisierung der Hauptanwendung mit tkinter
root = tk.Tk()
root.title("Bild zu Video Konverter")  # Titel des Hauptfensters setzen

# Liste zur Speicherung der Pfade der ausgewählten Bilder
image_list = []

def select_image():
    """Ein Bild auswählen und zur Liste hinzufügen."""
    max_images = 200
    if len(image_list) < max_images:
        # Dialog zum Auswählen mehrerer Bilder öffnen
        file_paths = filedialog.askopenfilenames(
            title=f"Wählen Sie bis zu {max_images} Bilder nacheinander aus",
            filetypes=[("Image files", "*.jpg *.png *.bmp")]
        )
        # Überprüfen, ob die Gesamtanzahl der ausgewählten Bilder das Limit überschreitet
        if len(image_list) + len(file_paths) > max_images:
            message_label.config(text=f"Sie können maximal {max_images} Bilder auswählen!")
            return
        # Hinzufügen der ausgewählten Bildpfade zur Liste
        for file_path in file_paths:
            image_list.append(file_path)
        display_images()
    else:
        message_label.config(text=f"Sie können maximal {max_images} Bilder auswählen!")


# Funktion zum Anzeigen der ausgewählten Bilder
def display_images():
    image_label.config(image="")  # Vorheriges Bild im Label löschen
    canvas_width, canvas_height = 640, 460  # Größe des Canvas festlegen
    canvas = Image.new("RGB", (canvas_width, canvas_height))  # Leeres Canvas erstellen
    for i, file_path in enumerate(image_list):  # Über alle ausgewählten Bilder iterieren
        # Bild laden, Größe anpassen und auf das Canvas setzen
        image = Image.open(file_path).resize(
            (canvas_width // len(image_list), canvas_height), Image.LANCZOS
        )
        canvas.paste(image, (i * canvas_width // len(image_list), 0))  # Bild einfügen
    photo = ImageTk.PhotoImage(canvas)  # Canvas in ein Tkinter-kompatibles Bild umwandeln
    image_label.config(image=photo)  # Bild im Label anzeigen
    image_label.image = photo  # Referenz auf das Bild halten, um es sichtbar zu halten

# Funktion zum Konvertieren der Bilder in ein Video
def convert_image():
    if image_list:  # Überprüfen, ob Bilder ausgewählt wurden
        try:
            video_length = int(length_entry.get())  # Länge des Videos vom Benutzer einlesen
        except ValueError:  # Wenn die Eingabe keine gültige Zahl ist
            # Fehlermeldung anzeigen
            message_label.config(text="Bitte geben Sie eine gültige Zahl für die Länge des Videos ein!")
            return
        # VideoWriter-Objekt erstellen für das Schreiben des Videos
        video = cv2.VideoWriter(
            "video.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 30, (1920, 1080)
        )
        frame_count = video_length * 30 // len(image_list)  # Anzahl der Frames pro Bild berechnen
        for file_path in image_list:  # Über alle Bilder iterieren
            # Bild laden, Größe anpassen und zum Video hinzufügen
            image = cv2.resize(cv2.imread(file_path), (1920, 1080))
            for _ in range(frame_count):  # Bild für die berechnete Anzahl von Frames hinzufügen
                video.write(image)
        video.release()  # VideoWriter-Objekt freigeben
        message_label.config(text="Ihr Video ist fertig!")  # Erfolgsmeldung anzeigen
        download_button.config(state=tk.NORMAL)  # Download-Button aktivieren
    else:  # Wenn keine Bilder ausgewählt wurden
        # Fehlermeldung anzeigen
        message_label.config(text="Bitte wählen Sie mindestens ein Bild aus!")

# Funktion zum Herunterladen des erstellten Videos
def download_video():
    # Dialog zum Speichern des Videos öffnen
    save_path = filedialog.asksaveasfilename(
        title="Speichern Sie das Video, Name bitte mit .mp4 eingeben",
        filetypes=[("MP4 files", "*.mp4")],  # Erlaubte Dateiformate
        defaultextension=".mp4"  # Standarderweiterung festlegen
    )
    if save_path:  # Wenn ein Speicherort ausgewählt wurde
        # Video von temporärem Pfad zum gewählten Speicherort kopieren
        with open("video.mp4", "rb") as source, open(save_path, "wb") as destination:
            destination.write(source.read())
        message_label.config(text="Ihr Video wurde gespeichert!")  # Erfolgsmeldung anzeigen
        os.remove("video.mp4")  # Temporäre Videodatei löschen

# Widgets für die GUI erstellen und anordnen
image_label = tk.Label(root, text="Kein Bild ausgewählt", width=80, height=40)
select_button = tk.Button(root, text="Bild auswählen", command=select_image)
convert_button = tk.Button(root, text="Bild in Video umwandeln", command=convert_image)
download_button = tk.Button(root, text="Video speichern", command=download_video, state=tk.DISABLED)
message_label = tk.Label(root, text="")
length_label = tk.Label(root, text="Länge des Videos in Sekunden:")
length_entry = tk.Entry(root)

# Widgets im Hauptfenster positionieren
image_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
select_button.grid(row=1, column=0, padx=10, pady=10)
convert_button.grid(row=1, column=1, padx=10, pady=10)
download_button.grid(row=1, column=2, padx=10, pady=10)
message_label.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
length_label.grid(row=3, column=0, padx=10, pady=10)
length_entry.grid(row=3, column=1, padx=10, pady=10)

# Hauptanwendung starten
root.mainloop()
