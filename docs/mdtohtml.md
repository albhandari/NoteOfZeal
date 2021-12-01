# Markdown to HTML


Markdown to HTML code, need to import marks and pdfkit
```python
import Marks
import pdfkit
#pip install pdfkit 
def MarkdownConverter():
    ask=input("Would you like to convert from to HTML or PDF? ")
    if (ask=="HTML" or ask=="html"):
        Marks.MarkdownToHTML()
    elif(ask=="PDF" or ask=="pdf"):
        noob=Marks.MarkdownToHTML()
        noobHTML=noob+".html"
        noobPDF=noob+"PDF"
        pdfkit.from_file(noobHTML, noobPDF)
    else:
        MarkdownConverter()

MarkdownConverter()
