from parser import PDFParser
import argparse
from pathlib import Path

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='PDF Parser Application')
    parser.add_argument('pdf_path', type=str, help='Path to the PDF file to parse')
    args = parser.parse_args()

    # Create PDF parser instance
    pdf_parser = PDFParser()

    try:
        # Parse the PDF
        result = pdf_parser.parse_pdf(args.pdf_path)
        
        # Print basic information
        print(f"\nFile: {result['file_name']}")
        print(f"Number of pages: {result['num_pages']}")
        print("\nMetadata:")
        for key, value in result['metadata'].items():
            print(f"{key}: {value}")
        
        # Print text content
        print("\nText content:")
        for i, page_text in enumerate(result['text_content'], 1):
            print(f"\n--- Page {i} ---")
            print(page_text)

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 