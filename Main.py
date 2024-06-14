import os
import PyPDF2
import pytesseract
from pdf2image import convert_from_path

# Defina o caminho para o arquivo PDF original
pdf_path = 'notas_fiscais.pdf'

# Crie uma pasta para armazenar os arquivos PDF separados
output_folder = 'output'
os.makedirs(output_folder, exist_ok=True)

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

# Abra o PDF original
with open(pdf_path, 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)

    # Processar cada página
    for page_num in range(num_pages):
        # Converter a página em uma imagem
        images = convert_from_path(pdf_path, first_page=page_num + 1, last_page=page_num + 1, poppler_path=os.path.join(os.getcwd(),"poppler/Library/bin"))

        if images:
            # Extrair texto da imagem
            text = extract_text_from_image(images[0])

            # Extrair o número da nota fiscal
            invoice_number = extract_invoice_number(text)

            if invoice_number:
                # Salvar a página como um novo PDF com o nome contendo o número da nota fiscal
                output_image_path = os.path.join(output_folder, f'nota_fiscal_{invoice_number}.png')
                images[0].save(output_image_path, 'PNG')
                print(f'Salvo: {output_image_path} ({(page_num / num_pages) * 100:.2f}%)')
            else:
                print(f'Número da nota fiscal não encontrado na página {page_num + 1}')
        else:
            print(f'Erro ao converter a página {page_num + 1} para imagem')