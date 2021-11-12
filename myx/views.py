import uuid

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseNotFound

from .converters import Converter


def index(request):
    if request.method == "POST":
        req = request.FILES
        conv = Converter(req)
        checks = list(request.POST.keys())
        extension = conv.extension
        converted = []
        
        if "png2jpg" in checks:
            file = conv.png2jpg()
            converted.append(file)
        if "jpg2png" in checks:
            file = conv.jpg2png()
            converted.append(file)
        if "png2webp" in checks or "jpg2webp" in checks:
            file = conv.img2webp()
            converted.append(file)
        if "img2pdf" in checks:
            file = conv.img2pdf()
            converted.append(file)
        if "webp2png" in checks:
            file = conv.webp2png()
            converted.append(file)
        if "webp2jpg" in checks:
            file = conv.webp2jpg()
            converted.append(file)
        if "pdf2jpg" in checks:
            file = conv.pdf2img()
            converted.append(file)
        if "pdf2mp3" in checks:
            file = conv.pdf2speech()
            converted.append(file)
        if "docx2pdf" in checks:
            file = conv.docx2pdf()
            converted.append(file)
        if "mkv2mp4" in checks:
            file = conv.mkv2mp4()
            converted.append(file)
        file = conv.archive(converted, True)

        return render(request, 'index.html', {"context":{"file_link":file}})
    return render(request, 'index.html', {})


def convert(request, convert_type):
    if convert_type == "png2jpg":
        if request.method == "POST":
            req = request.FILES
            conv = Converter(req)
            file = conv.png2jpg()

            return render(request, 'convert.html', {"context":{"file_link":file}})
        accept = ".png"
        return render(request, 'convert.html', {"context":{"accept":accept, "multiple":True}})
    
    if convert_type == "jpg2png":
        if request.method == "POST":
            req = request.FILES
            conv = Converter(req)
            file = conv.jpg2png()

            return render(request, 'convert.html', {"context":{"file_link":file}})
        accept = ".jpg, .jpeg"
        return render(request, 'convert.html', {"context":{"accept":accept, "multiple":True}})
    
    if convert_type == "img2webp":
        if request.method == "POST":
            req = request.FILES
            conv = Converter(req)
            file = conv.img2webp()

            return render(request, 'convert.html', {"context":{"file_link":file}})
        accept = ".png, .jpg, .jpeg"
        return render(request, 'convert.html', {"context":{"accept":accept, "multiple":True}})

    if convert_type == "img2pdf":
        if request.method == "POST":
            req = request.FILES
            conv = Converter(req)
            file = conv.img2pdf()

            return render(request, 'convert.html', {"context":{"file_link":file}})
        accept = ".png, .jpg, .jpeg, .webp"
        return render(request, 'convert.html', {"context":{"accept":accept, "multiple":True}})

    if convert_type == "webp2png":
        if request.method == "POST":
            req = request.FILES
            conv = Converter(req)
            file = conv.webp2png()

            return render(request, 'convert.html', {"context":{"file_link":file}})
        accept = ".webp"
        return render(request, 'convert.html', {"context":{"accept":accept, "multiple":True}})
    
    if convert_type == "webp2jpg":
        if request.method == "POST":
            req = request.FILES
            conv = Converter(req)
            file = conv.webp2jpg()

            return render(request, 'convert.html', {"context":{"file_link":file}})
        accept = ".webp"
        return render(request, 'convert.html', {"context":{"accept":accept, "multiple":True}})
    
    if convert_type == "pdf2img":
        if request.method == "POST":
            req = request.FILES
            conv = Converter(req)
            file = conv.pdf2img()

            return render(request, 'convert.html', {"context":{"file_link":file}})
        accept = ".pdf"
        return render(request, 'convert.html', {"context":{"accept":accept, "multiple":False}})
    
    if convert_type == "pdfmerge":
        if request.method == "POST":
            req = request.FILES
            conv = Converter(req)
            file = conv.pdfmerge()

            return render(request, 'convert.html', {"context":{"file_link":file}})
        accept = ".pdf"
        return render(request, 'convert.html', {"context":{"accept":accept, "multiple":True}})
    
    if convert_type == "pdf2speech":
        if request.method == "POST":
            req = request.FILES
            conv = Converter(req)
            file = conv.pdf2speech()

            return render(request, 'convert.html', {"context":{"file_link":file}})
        accept = ".pdf"
        return render(request, 'convert.html', {"context":{"accept":accept, "multiple":False}})
    
    if convert_type == "docx2pdf":
        if request.method == "POST":
            req = request.FILES
            conv = Converter(req)
            file = conv.docx2pdf()

            return render(request, 'convert.html', {"context":{"file_link":file}})
        accept = ".docx, .doc"
        return render(request, 'convert.html', {"context":{"accept":accept, "multiple":False}})
    
    if convert_type == "mkv2mp4":
        if request.method == "POST":
            req = request.FILES
            conv = Converter(req)
            file = conv.mkv2mp4()

            return render(request, 'convert.html', {"context":{"file_link":file}})
        accept = ".mkv"
        return render(request, 'convert.html', {"context":{"accept":accept, "multiple":False}})
    
    
    else:
        return HttpResponseNotFound("Page not found")