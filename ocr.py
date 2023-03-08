import pytesseract
import fitz
from PIL import Image
import argparse
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4, portrait

# Parse command line arguments
parser = argparse.ArgumentParser(description='Exctract text from pdf and write to pdf')
parser.add_argument('-i', '--input', help='input pdf file')
parser.add_argument('-o', '--output', help='output pdf file')
parser.add_argument('-l', '--lang', help='language of the text')
args = parser.parse_args()
infile = args.input
outfile = 'output.txt' if args.output is None else args.output
language = 'eng' if args.lang is None else args.lang
if not os.path.exists('output/png'):
    os.mkdir('output/png')

# Convert each page to an image
pages =fitz.open(infile)
for page in pages:
    pix = page.get_pixmap(matrix=fitz.Matrix(5.0, 5.0))
    pix.save('output/png/page-%i.png' % page.number)

# Write images to txt
f = open('output/text.txt', 'a')
for i in range(0, len(pages)):
    filename = 'output/png/page-%i.png' % page.number
    text = str(((pytesseract.image_to_string(Image.open(filename), lang=language))))
    #text = text.replace('-\n', '')
    f.write(text)
f.close()

# Write pdf
mystyle = ParagraphStyle(name='normal',fontSize=10,leading=1.2*12,parent=getSampleStyleSheet()['Normal'])       
doc = SimpleDocTemplate(outfile, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=25, pageSize=A4)
doc.pagesize = portrait(A4)

with open('output/text.txt') as f:
    text = f.read()
paragraphs = text.split('\n')
os.remove('output/text.txt')

elements = []
for p in paragraphs:  
    elements.append(Paragraph(p))
doc.build(elements)
