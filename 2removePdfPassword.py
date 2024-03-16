import os
import sys
import PyPDF2

def remove_password_from_pdf(pdf_file, password):
    try:
        with open(pdf_file, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            if pdf_reader.is_encrypted:
                pdf_reader.decrypt(password)
                pdf_writer = PyPDF2.PdfWriter()
                for page_num in range(len(pdf_reader.pages)):
                    pdf_writer.add_page(pdf_reader.pages[page_num])
                with open(f"unlocked_{os.path.basename(pdf_file)}", 'wb') as output_file:
                    pdf_writer.write(output_file)
                print(f"Password removed from {pdf_file}")
            else:
                print(f"{pdf_file} is not encrypted")
    except Exception as e:
        print(f"Error processing {pdf_file}: {str(e)}")

def main(directory, password_file):
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return
    
    with open(password_file, 'r') as file:
        password = file.read().strip()

    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            filepath = os.path.join(directory, filename)
            remove_password_from_pdf(filepath, password)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python program.py <directory> <password_file>")
        sys.exit(1)

    directory = sys.argv[1]
    password_file = sys.argv[2]
    main(directory, password_file)


    #usage
    #python3 2removePdfPassword.py ./DirectoryWithPassWordFiles/ ./passwordDir/FileContainingPassword.txt
