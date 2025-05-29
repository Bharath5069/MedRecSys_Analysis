# Medical Recommendation System

A simple Python utility to parse PDF files and extract their content.

## Features

- Extract text content from PDF files
- Access PDF metadata
- Get basic file information (number of pages, filename)
- (Coming soon) Table extraction
- (Coming soon) Image extraction

## Requirements

Make sure you have Python 3.7+ installed and the following package:
- pypdf

## Usage

### Command Line Interface

```bash
python main.py path/to/your/file.pdf
```

### As a Library

```python
from parser import PDFParser

# Create parser instance
pdf_parser = PDFParser()

# Parse a PDF file
result = pdf_parser.parse_pdf("path/to/your/file.pdf")

# Access the extracted data
print(f"Number of pages: {result['num_pages']}")
print(f"File name: {result['file_name']}")
print(f"Metadata: {result['metadata']}")
print(f"Text content: {result['text_content']}")
```

## Error Handling

The parser will raise exceptions in the following cases:
- File not found
- Unsupported file format (only .pdf files are supported)
- PDF parsing errors

## Contributing

Feel free to submit issues and enhancement requests! 
