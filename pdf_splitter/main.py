import os
from PyPDF2 import PdfReader, PdfWriter


folder_name = input('Digite o nome da pasta [enter para criar pasta com nome de "result"]: ')
if not folder_name:
    folder_name = 'result'

folder = f'pdf_splitter/{folder_name}'


def write_pdf(pdf_reader, pdf_writer, output, start, end):
    for page in range(start, end):
        pdf_writer.add_page(pdf_reader.pages[page])
        with open(output, 'ab') as output_pdf:
            pdf_writer.write(output_pdf)

def split(path, name_of_split, start=0, end=None):

    pdf = PdfReader(path)

    if end is None:
        end = len(pdf.pages)

    if start < 0 or start > end or end >= len(pdf.pages):
        raise ValueError('Número não é apropriado')
    
    pdf_writer = PdfWriter()
    
    if not os.path.isdir(folder):
        os.mkdir(folder)

    output = os.path.join(folder, f'{name_of_split}.pdf')

    write_pdf(pdf_reader=pdf, pdf_writer=pdf_writer, output=output, start=start, end=end)


def group_in_chunks(path, name, n):
    pdf = PdfReader(path)
    
    if not os.path.isdir(folder):
        os.mkdir(folder)

    x, y = divmod(len(pdf.pages), n)
    start, end = 0, n
    for t in range(x):
        pdf_writer = PdfWriter()
        output = os.path.join(folder, f'{name}_{t}.pdf')
        write_pdf(pdf_reader=pdf, pdf_writer=pdf_writer, output=output, start=start, end=end)
        start = end
        end = end + n
    if y:
        pdf_writer = PdfWriter()
        output = os.path.join(folder, f'{name}_{t+1}.pdf')
        write_pdf(pdf_reader=pdf, pdf_writer=pdf_writer, output=output, start=start, end=len(pdf.pages))

    print('PDF salvo em:', folder_name)


if __name__ == '__main__':
    path = 'pdf_splitter/micro.pdf'
    name = 'regex_resume'
    # split(path, name, start=0, end=5)
    group_in_chunks(path, name, 3)
