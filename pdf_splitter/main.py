import os
from PyPDF2 import PdfReader, PdfWriter
import typer
from typing_extensions import Annotated


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
def cut(
        path: Annotated[str, typer.Option(help='Caminho do pdf')],
        name_of_split: Annotated[str, typer.Option(help='Nome do novo pdf')],
        folder: Annotated[str, typer.Option(help='Local onde será salvo o pdf')],
        start: Annotated[int, typer.Option(help='Página de inicio')] = 0,
        end: Annotated[int, typer.Option(help='Página de fim')] = None
    ):
    """Corta um pdf em local específico"""

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
def batch(
        path: Annotated[str, typer.Option(help='Caminho do pdf')],
        name: Annotated[str, typer.Option(help='Nome do novo pdf')],
        folder: Annotated[str, typer.Option(help='Local onde será salvo o pdf')], 
        n: Annotated[int, typer.Option(help='Quantidade de página em cada lote')],
        send: Annotated[bool, typer.Option(help='Define se arquivo será ou não enviado ao drive')] = False
    ):
    """Agrupa em lotes um pdf"""
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

    typer.echo(f'PDF salvo em: {folder}')

    if send:
        typer.echo('Enviando pdf para drive')


if __name__ == '__main__':
    app()
