import heapq
import random

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import getFont, stringWidth


class PDF:
    def __init__(self, name, pagesize=letter):
        self.font = 'Helvetica'
        self.face = getFont(self.font).face
        self.size = 6

        self.canvasWidth, self.canvasHeight = pagesize
        self.fontHeight = self.getTextHeight(' ')
        self.spaceWidth = self.getTextWidth(' ')

        self.colors = list(colors.getAllNamedColors().values())

        self.c = canvas.Canvas(name, pagesize=pagesize)
        self.c.setFont(self.font, self.size)

    def drawText(self, text, x, y, color=colors.black):
        width = self.getTextWidth(text)
        self.c.setFillColor(color)
        self.c.drawString(x, self.canvasHeight - self.fontHeight - y, text)
        return width, self.fontHeight

    def generate_random_word(self):
        with open('words.txt') as f:
            return heapq.nlargest(1, f, key=lambda x: random.random())[0].lower().strip()

    def fillPage(self):
        for wordY in range(0, int(self.canvasHeight), int(self.fontHeight)):
            wordX = 0
            while True:
                word = self.generate_random_word()
                width = self.getTextWidth(word)
                self.drawText(word, wordX, wordY, random.choice(self.colors))
                wordX += width + self.spaceWidth
                if wordX > self.canvasWidth:
                    break

    def save(self):
        self.c.save()

    def getTextWidth(self, text):
        return stringWidth(text, self.font, self.size)

    def getTextHeight(self, text):
        return (self.face.ascent - self.face.descent) / 1000 * self.size


if __name__ == '__main__':
    pdf = PDF('cram.pdf')
    for _ in range(16):
        pdf.fillPage()
    pdf.save()
