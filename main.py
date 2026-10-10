import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from urllib.parse import urlparse

import qrcode
from PIL import Image, ImageTk


class QRCodeGenerator:
    """Desktop application for generating QR codes from URLs."""

    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("620x680")
        self.root.minsize(520, 600)
        self.root.configure(bg="#202124")

        self.qr_image = None
        self.preview_image = None

        self._build_interface()

    def _build_interface(self):
        header = tk.Frame(self.root, bg="#202124")
        header.pack(fill="x", padx=25, pady=(25, 15))

        tk.Label(
            header,
            text="QR Code Generator",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#202124",
        ).pack()

        tk.Label(
            header,
            text="Turn any website URL into a scannable QR code",
            font=("Arial", 11),
            fg="#b8b8b8",
            bg="#202124",
        ).pack(pady=(8, 0))

        input_frame = tk.Frame(self.root, bg="#202124")
        input_frame.pack(fill="x", padx=30, pady=10)

        tk.Label(
            input_frame,
            text="Website URL",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#202124",
        ).pack(anchor="w", pady=(0, 8))

        self.url_entry = tk.Entry(
            input_frame,
            font=("Arial", 13),
            relief="flat",
            bg="white",
            fg="#202124",
            insertbackground="#202124",
        )
        self.url_entry.pack(fill="x", ipady=10)
        self.url_entry.bind("<Return>", lambda event: self.generate_qr())

        self.generate_button = ttk.Button(
            input_frame,
            text="Generate QR Code",
            command=self.generate_qr,
        )
        self.generate_button.pack(fill="x", pady=(12, 0), ipady=5)

        self.preview_frame = tk.Frame(
            self.root,
            bg="#303134",
            highlightthickness=1,
            highlightbackground="#555555",
        )
        self.preview_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=20,
        )

        self.preview_label = tk.Label(
            self.preview_frame,
            text="Your QR code will appear here",
            font=("Arial", 12),
            fg="#b8b8b8",
            bg="#303134",
        )
        self.preview_label.pack(expand=True, padx=15, pady=15)

        self.save_button = ttk.Button(
            self.root,
            text="Save QR Code as PNG",
            command=self.save_qr,
            state="disabled",
        )
        self.save_button.pack(fill="x", padx=30, pady=(0, 12), ipady=5)

        self.status_label = tk.Label(
            self.root,
            text="Enter a URL to get started.",
            font=("Arial", 10),
            fg="#b8b8b8",
            bg="#202124",
        )
        self.status_label.pack(fill="x", padx=30, pady=(0, 18))

    @staticmethod
    def validate_url(value):
        """Validate that the input is an HTTP or HTTPS URL."""
        value = value.strip()

        if not value:
            return False

        try:
            parsed = urlparse(value)
            return (
                parsed.scheme.lower() in ("http", "https")
                and bool(parsed.hostname)
                and "." in parsed.hostname
                and " " not in value
            )
        except ValueError:
            return False

    def generate_qr(self):
        url = self.url_entry.get().strip()

        if not self.validate_url(url):
            messagebox.showwarning(
                "Invalid URL",
                "Enter a valid website URL starting with http:// or https://.",
            )
            self.status_label.config(text="Please enter a valid URL.")
            return

        try:
            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)

            self.qr_image = qr.make_image(
                fill_color="black",
                back_color="white",
            ).convert("RGB")

            preview = self.qr_image.copy()
            preview.thumbnail((300, 300), Image.Resampling.LANCZOS)

            self.preview_image = ImageTk.PhotoImage(preview)
            self.preview_label.config(
                image=self.preview_image,
                text="",
                bg="white",
            )
            self.preview_frame.config(bg="white")

            self.save_button.config(state="normal")
            self.status_label.config(text="QR code generated successfully.")

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
            )

    def save_qr(self):
        if self.qr_image is None:
            messagebox.showwarning(
                "No QR Code",
                "Generate a QR code before saving.",
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
            output_path = Path(destination)

            if output_path.suffix.lower() != ".png":
                output_path = output_path.with_suffix(".png")

            self.qr_image.save(output_path, format="PNG")
            self.status_label.config(
                text=f"Saved: {output_path.name}"
            )
            messagebox.showinfo(
                "Saved Successfully",
                f"QR code saved to:\n{output_path}",
            )

        except (OSError, ValueError) as error:
            messagebox.showerror(
                "Save Error",
                f"Unable to save the QR code:\n{error}",
            )


def main():
    root = tk.Tk()
    QRCodeGenerator(root)
    root.mainloop()


if __name__ == "__main__":
    main()