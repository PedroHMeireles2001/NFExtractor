import os
import PyPDF2
import pytesseract
from pdf2image import convert_from_path


# Crie uma pasta para armazenar os arquivos PDF separados


pytesseract.pytesseract.tesseract_cmd = os.path.join(os.getcwd(),"Tesseract/tesseract.exe")

# Função para extrair texto usando OCR
def extract_text_from_image(image):
    return pytesseract.image_to_string(image, lang='por')

# Função para salvar uma página específica de um PDF como um novo PDF
def save_pdf_page(pdf_reader, page_number, output_path):
    pdf_writer = PyPDF2.PdfWriter()
    pdf_writer.add_page(pdf_reader.pages[page_number])
    with open(output_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

# Função para extrair número da nota fiscal do texto
def extract_invoice_number(text):
    import re
    match = re.search(r'N[°º]\s*(\d{3}\.\d{3}\.\s*\d{3})', text)
    if match:
        return match.group(1).replace(' ', '').replace('.', '')
    return None

pdf_files = [f for f in os.listdir("input") if f.endswith('.pdf')]

for pdf_path in pdf_files:
    output_folder = f'output/{pdf_path.replace(".pdf","")}'
    os.makedirs(output_folder, exist_ok=True)
    print(os.path.join("input", pdf_path))
    with open(os.path.join("input", pdf_path), 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)

        # Processar cada página
        for page_num in range(num_pages):
            # Converter a página em uma imagem
            images = convert_from_path(os.path.join("input",pdf_path), first_page=page_num + 1, last_page=page_num + 1,
                                       poppler_path=os.path.join(os.getcwd(), "poppler/Library/bin"))

            if images:
                # Extrair texto da imagem
                text = extract_text_from_image(images[0])

                # Extrair o número da nota fiscal
                invoice_number = extract_invoice_number(text)

                output_image_path = os.path.join(output_folder, f'Page_{page_num}.jpg')

                if invoice_number:
                    output_image_path = os.path.join(output_folder, f'{invoice_number}.jpg')

                images[0].save(output_image_path, 'JPEG', quality=10)

            else:
                print(f'Erro ao converter a página {page_num + 1} para imagem')
# Abra o PDF original

