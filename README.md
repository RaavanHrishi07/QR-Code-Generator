# QR Code Generator

A simple desktop application built with Python and Tkinter that converts website URLs into QR codes. Preview the generated QR code and save it as a PNG image.

## Features

- Generate QR codes from website URLs.
- Validate URL input before generating a QR code.
- Preview QR codes directly in the application.
- Save generated QR codes as PNG images.
- Simple desktop interface built with Tkinter.
- Error handling for invalid URLs and saving problems.

## Technologies Used

- Python 3.11+
- Tkinter
- qrcode
- Pillow

## Installation

1. Clone the repository:

       git clone https://github.com/RaavanHrishi07/QR-Code-Generator.git

2. Open the project directory:

       cd QR-Code-Generator

3. Install the required dependencies:

       python -m pip install -r requirements.txt

## How to Run

Start the application with:

    python main.py

Enter a website URL beginning with `https://` or `http://`, click **Generate QR Code**, and then use **Save QR Code as PNG** to save the image.

## Project Structure

    QR-Code-Generator/
    ├── main.py
    ├── requirements.txt
    ├── .gitignore
    ├── README.md
    └── LICENSE

## Requirements

- Python 3.11 or later
- Internet access is not required to generate QR codes once the dependencies are installed.

## Future Improvements

- Custom QR code colours.
- Adjustable QR code size.
- Support for additional QR code content types.

## Author

[RaavanHrishi07](https://github.com/RaavanHrishi07)

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
