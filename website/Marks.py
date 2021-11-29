#Amazingly simple how easy it is to convert markdown to HTML
#thanks to this goofy library
import markdown

def MarkdownToHTML():
    Bruh=input("Enter the filename ")
    with open(Bruh, 'r') as f:
        text = f.read()
        html = markdown.markdown(text)
    Bruh2=input("Enter the filename you want to save it as (don't add file extension) ")
    Bruh3=Bruh2+".html"
    with open(Bruh3, 'w') as f:
        f.write(html)
    return Bruh2

#MarkdownToHTML()
