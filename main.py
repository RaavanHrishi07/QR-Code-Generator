
import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, ttk
from pathlib import Path
from urllib.parse import urlparse

import qrcode
from PIL import Image, ImageTk


class QRCodeGenerator:
    """Generate and customise QR codes from website URLs."""

    ERROR_LEVELS = {
        "Low (7%)": qrcode.constants.ERROR_CORRECT_L,
        "Medium (15%)": qrcode.constants.ERROR_CORRECT_M,
        "Quartile (25%)": qrcode.constants.ERROR_CORRECT_Q,
        "High (30%)": qrcode.constants.ERROR_CORRECT_H,
    }

    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("660x820")
        self.root.minsize(560, 740)
        self.root.configure(bg="#202124")

        self.qr_image = None
        self.preview_image = None
        self.qr_color = "#000000"
        self.background_color = "#FFFFFF"

        self._build_interface()

    def _build_interface(self):
        tk.Label(
            self.root,
            text="QR Code Generator",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#202124",
        ).pack(pady=(18, 5))

        tk.Label(
            self.root,
            text="Create and customise your QR codes",
            font=("Arial", 11),
            fg="#b8b8b8",
            bg="#202124",
        ).pack(pady=(0, 15))

        input_frame = tk.Frame(self.root, bg="#202124")
        input_frame.pack(fill="x", padx=30)

        tk.Label(
            input_frame,
            text="Website URL",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#202124",
        ).pack(anchor="w", pady=(0, 7))

        self.url_entry = tk.Entry(
            input_frame,
            font=("Arial", 13),
            relief="flat",
            bg="white",
            fg="#202124",
        )
        self.url_entry.pack(fill="x", ipady=8)
        self.url_entry.bind(
            "<Return>", lambda event: self.generate_qr()
        )

        colors_frame = tk.Frame(self.root, bg="#202124")
        colors_frame.pack(fill="x", padx=30, pady=12)

        self.qr_color_button = tk.Button(
            colors_frame,
            text="QR Colour: Black",
            bg=self.qr_color,
            fg="white",
            command=self.choose_qr_color,
        )
        self.qr_color_button.pack(
            side="left", fill="x", expand=True, padx=(0, 5), ipady=5
        )

        self.bg_color_button = tk.Button(
            colors_frame,
            text="Background: White",
            bg=self.background_color,
            fg="black",
            command=self.choose_background_color,
        )
        self.bg_color_button.pack(
            side="left", fill="x", expand=True, padx=(5, 0), ipady=5
        )

        options_frame = tk.Frame(self.root, bg="#202124")
        options_frame.pack(fill="x", padx=30, pady=(0, 12))

        tk.Label(
            options_frame,
            text="QR Block Size",
            font=("Arial", 10, "bold"),
            fg="white",
            bg="#202124",
        ).grid(row=0, column=0, sticky="w", pady=(0, 5))

        self.size_var = tk.IntVar(value=10)
        self.size_slider = tk.Scale(
            options_frame,
            from_=5,
            to=20,
            orient="horizontal",
            variable=self.size_var,
            bg="#202124",
            fg="white",
            troughcolor="#555555",
            highlightthickness=0,
            activebackground="#8ab4f8",
            length=220,
        )
        self.size_slider.grid(row=1, column=0, sticky="ew", padx=(0, 15))

        tk.Label(
            options_frame,
            text="Error Correction",
            font=("Arial", 10, "bold"),
            fg="white",
            bg="#202124",
        ).grid(row=0, column=1, sticky="w", pady=(0, 5))

        self.error_var = tk.StringVar(value="Medium (15%)")
        self.error_combo = ttk.Combobox(
            options_frame,
            textvariable=self.error_var,
            values=list(self.ERROR_LEVELS.keys()),
            state="readonly",
            width=18,
        )
        self.error_combo.grid(row=1, column=1, sticky="ew", ipady=4)

        options_frame.columnconfigure(0, weight=1)
        options_frame.columnconfigure(1, weight=1)

        ttk.Button(
            self.root,
            text="Generate QR Code",
            command=self.generate_qr,
        ).pack(fill="x", padx=30, ipady=6)

        self.preview_frame = tk.Frame(
            self.root,
            bg="#303134",
            highlightthickness=1,
            highlightbackground="#555555",
        )
        self.preview_frame.pack(
            fill="both", expand=True, padx=30, pady=15
        )

        self.preview_label = tk.Label(
            self.preview_frame,
            text="Your QR code will appear here",
            font=("Arial", 12),
            fg="#b8b8b8",
            bg="#303134",
        )
        self.preview_label.pack(expand=True, padx=12, pady=12)

        self.save_button = ttk.Button(
            self.root,
            text="Save QR Code as PNG",
            command=self.save_qr,
            state="disabled",
        )
        self.save_button.pack(fill="x", padx=30, pady=(0, 10), ipady=6)

        self.status_label = tk.Label(
            self.root,
            text="Enter a URL to get started.",
            font=("Arial", 10),
            fg="#b8b8b8",
            bg="#202124",
        )
        self.status_label.pack(fill="x", padx=30, pady=(0, 15))

    @staticmethod
    def validate_url(value):
        value = value.strip()

        if not value or " " in value:
            return False

        try:
            parsed = urlparse(value)
            return (
                parsed.scheme.lower() in ("http", "https")
                and bool(parsed.hostname)
                and "." in parsed.hostname
            )
        except ValueError:
            return False

    @staticmethod
    def _button_text_color(hex_color):
        value = hex_color.lstrip("#")
        red, green, blue = (
            int(value[i:i + 2], 16) for i in (0, 2, 4)
        )
        brightness = (red * 299 + green * 587 + blue * 114) / 1000
        return "black" if brightness > 150 else "white"

    def choose_qr_color(self):
        selected = colorchooser.askcolor(
            color=self.qr_color,
            title="Choose QR Code Colour",
            parent=self.root,
        )

        if selected and selected[1]:
            self.qr_color = selected[1].upper()
            self.qr_color_button.config(
                text=f"QR Colour: {self.qr_color}",
                bg=self.qr_color,
                fg=self._button_text_color(self.qr_color),
            )
            self._refresh_existing_qr()

    def choose_background_color(self):
        selected = colorchooser.askcolor(
            color=self.background_color,
            title="Choose Background Colour",
            parent=self.root,
        )

        if selected and selected[1]:
            self.background_color = selected[1].upper()
            self.bg_color_button.config(
                text=f"Background: {self.background_color}",
                bg=self.background_color,
                fg=self._button_text_color(self.background_color),
            )
            self._refresh_existing_qr()

    def _refresh_existing_qr(self):
        url = self.url_entry.get().strip()
        if url and self.validate_url(url):
            self.generate_qr()

    def generate_qr(self):
        url = self.url_entry.get().strip()

        if not self.validate_url(url):
            messagebox.showwarning(
                "Invalid URL",
                "Enter a valid website URL starting with "
                "http:// or https://.",
                parent=self.root,
            )
            self.status_label.config(text="Please enter a valid URL.")
            return

        try:
            qr = qrcode.QRCode(
                version=None,
                error_correction=self.ERROR_LEVELS[self.error_var.get()],
                box_size=self.size_var.get(),
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)

            self.qr_image = qr.make_image(
                fill_color=self.qr_color,
                back_color=self.background_color,
            ).convert("RGB")

            preview = self.qr_image.copy()
            preview.thumbnail((320, 320), Image.Resampling.LANCZOS)

            self.preview_image = ImageTk.PhotoImage(preview)
            self.preview_label.config(
                image=self.preview_image,
                text="",
                bg=self.background_color,
            )
            self.preview_frame.config(bg=self.background_color)
            self.save_button.config(state="normal")
            self.status_label.config(
                text=(
                    f"QR generated | Block size: {self.size_var.get()} | "
                    f"Error correction: {self.error_var.get()}"
                )
            )

        except Exception as error:
            self.qr_image = None
            self.preview_image = None
            self.preview_label.config(
                image="",
                text="QR code could not be generated.",
                bg="#303134",
            )
            self.preview_frame.config(bg="#303134")
            self.save_button.config(state="disabled")
            messagebox.showerror(
                "Generation Error",
                f"Unable to generate the QR code:\n{error}",
                parent=self.root,
            )

    def save_qr(self):
        if self.qr_image is None:
            messagebox.showwarning(
                "No QR Code",
                "Generate a QR code before saving.",
                parent=self.root,
            )
            return

        destination = filedialog.asksaveasfilename(
            title="Save QR Code",
            defaultextension=".png",
            filetypes=[("PNG image", "*.png")],
            initialfile="qr_code.png",
        )

        if not destination:
            return

        try:
            output_path = Path(destination).with_suffix(".png")
            self.qr_image.save(output_path, format="PNG")
            self.status_label.config(text=f"Saved: {output_path.name}")
            messagebox.showinfo(
                "Saved Successfully",
                f"QR code saved to:\n{output_path}",
                parent=self.root,
            )
        except (OSError, ValueError) as error:
            messagebox.showerror(
                "Save Error",
                f"Unable to save the QR code:\n{error}",
                parent=self.root,
            )


def main():
    root = tk.Tk()
    QRCodeGenerator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
