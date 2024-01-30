# PDF Cracker

Disclaimer: I made this tool to learn about opening encrypted PDF files, and somehow ended up with multiprocessing. I only used this on PDFs I created. This tool should not be used on files you are unauthorized to access.

Usage:

```sh
python main.py [PATH]
```

Example:

```sh
python main.py secret.pdf
```

Why?

A former employer "secured" our payroll PDFs with the last four digits of our SSN. For obvious reasons, this isn't very secure. I wanted to see how easy it would be to extract this information from the PDF file since there are only 10k possible endings to an SSN.
