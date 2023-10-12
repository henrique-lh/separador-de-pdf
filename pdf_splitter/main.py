import os
from PyPDF2 import PdfReader, PdfWriter
import typer

app = typer.Typer()


def write_pdf(pdf_reader: PdfReader, pdf_writer: PdfWriter, output: str, start: int, end: int):
    """Escreve novo arquivo pdf

    Args:
        pdf_reader (PdfReader): Página do pdf lido
        pdf_writer (PdfWriter): Classe que escreve nova página
        output (str): Local onde será escrito
        start (int): Página de inicio
        end (int): Página de fim 
    """
    for page in range(start, end):
        pdf_writer.add_page(pdf_reader.pages[page])
        with open(output, 'ab') as output_pdf:
            pdf_writer.write(output_pdf)


@app.command()
def split(path: str, name_of_split: str, folder: str, start: int=0, end: int=None):
    """Corta um pdf de uma página x até uma uma página y

    Args:
        path (str): Caminho do pdf
        name_of_split (str): Nome do novo pdf
        folder (str): Local onde será salvo o pdf
        start (int, optional): Página de inicio. Defaults to 0.
        end (int, optional): Página de fim. Defaults to None.

    Raises:
        ValueError: Valor de página que não é possível acessar/escrever
    """

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


@app.command()
def group_in_chunks(path: str, name: str, folder: str, n: int):
    """Agrupa um arquivo pdf em lotes iguais

    Args:
        path (str): Caminho do pdf
        name (str): Nome do novo pdf
        folder (str): Local onde será salvo o pdf
        n (int): Quantidade de página em cada lote

    Examples:
        1) Dividir um pdf de 50 páginas em 10 páginas iguais, totalizando 5 lotes
            divmod(50, 10) = (5, 0)
        2) Dividir um pdf de 51 páginas em 10 páginas iguais, totalizando 6 lotes
            divmod(51, 10) = (5, 1)
    """
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

    print('PDF salvo em:', folder)


if __name__ == '__main__':
    app()
