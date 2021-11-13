import uuid
import shutil
import os, uuid
from zipfile import ZipFile

from django.conf import Settings, settings
from django.core.files.storage import FileSystemStorage

import PyPDF2
from gtts import gTTS
from PIL import Image
#import pdf2docx as p2d
import ffmpeg
import docx2pdf as d2p
import ppt2pdf as p2p
import img2pdf as i2p
import pdf2image as p2i
from PyPDF2 import PdfFileMerger

output = os.path.join(settings.BASE_DIR, 'output')
media = os.path.join(settings.BASE_DIR, 'media')


class Converter:
    def __init__(self, request):
        try:
            self.file_total = request.getlist('uploaded')
        except:
            self.file_total = 1
        self.o_name, self.extension = self.original_name(request['uploaded'].name)
        
        if len(self.file_total) > 1:
            self.request = request.getlist('uploaded')
        else:
            self.request = request['uploaded']
        
        self.ffs = FileSystemStorage()
        self.id = uuid.uuid4().hex
        self.uid = self.id + f".{self.extension}" # Giving the file a Unique name with the original extension
        if len(self.file_total) > 1:
            self.saved_files = []
            self.save_files()
        else:
            self.file = self.ffs.save(self.uid, self.request)
        
    
    def save_files(self):
        for x in range(len(self.request)):
            self.ffs.save(f"{self.id}_temp\{self.id}_{x}.{self.extension}", self.request[x])


    def original_name(self, name):
        """
        Get original file name and extension
        """
        temp = name.split(".")
        extension = temp[-1]
        temp.pop()
        return "".join(temp), extension

    def archive(self, files=None, index=False):
        """
        Archive a list of files in a directory
        """
        temp_dir = f"{settings.BASE_DIR}\media\{self.id}_temp\\"
        if not files:
            files = os.listdir(temp_dir)    
        
        if index:
            path = f"output\{self.id[0:8]}-{self.o_name}.zip"
            zipobj = ZipFile(f"{settings.BASE_DIR}\{path}", 'w')
            for x in files:
                name = x.split('\\')[1]
                zipobj.write(os.path.abspath(f"{settings.BASE_DIR}\{x}"), name)
            zipobj.close()
            return path
        else:
            zipobj = ZipFile(f"{settings.BASE_DIR}\output\{self.o_name}.zip", 'w')
            for x in files:
                zipobj.write(os.path.abspath(f"{settings.BASE_DIR}\media\{self.id}_temp\{x}"), x)
            zipobj.close()
            #shutil.rmtree(f"media\{self.id}_temp")


    def png2jpg(self):
        """
        Convert PNG to JPG
        """
        if len(self.file_total) > 1:
            temp_folder = f"{media}\{self.id}_temp"
            files = os.listdir(temp_folder)
            for x in range(len(files)):
                filename = f"{self.o_name}_{x}.jpg"
                self.saved_files.append(filename)
                im = Image.open(f"{temp_folder}\{files[x]}")
                rgb_im = im.convert('RGB')
                rgb_im.save(f"{temp_folder}\{filename}")

            self.archive(files=self.saved_files)
            path = f"output\{self.o_name}.zip"
            return path
        else:
            im = Image.open(media + f"\{self.uid}")
            rgb_im = im.convert('RGB')
            path = f'{settings.BASE_DIR}\output\{self.o_name}.jpg'
            rgb_im.save(path)
            path = f"output\{self.o_name}.jpg"
            return path

    def jpg2png(self):
        """
        Convert JPG to PNG
        """
        if len(self.file_total) > 1:
            temp_folder = f"{media}\{self.id}_temp"
            files = os.listdir(temp_folder)
            for x in range(len(files)):
                filename = f"{self.o_name}_{x}.png"
                self.saved_files.append(filename)
                im = Image.open(f"{temp_folder}\{files[x]}")
                im.save(f"{temp_folder}\{filename}")
            self.archive(files=self.saved_files)
            path = f"output\{self.o_name}.zip"
            return path
        else:
            im = Image.open(media + f"\{self.uid}")
            path = f'{settings.BASE_DIR}\output\{self.o_name}.png'
            im.save(path)
            path = f"output\{self.o_name}.png"
            return path

    def img2webp(self):
        if len(self.file_total) > 1:
            temp_folder = f"{settings.BASE_DIR}\media\{self.id}_temp"
            files = os.listdir(temp_folder)
            for x in range(len(files)):
                filename = f"{self.o_name}_{x}.webp"
                self.saved_files.append(filename)
                im = Image.open(f"{temp_folder}\{files[x]}")
                rgb_im = im.convert('RGB')
                rgb_im.save(f"{temp_folder}\{filename}")

            self.archive(files=self.saved_files)
            path = f"output\{self.o_name}.zip"
            return path
        else:
            image = Image.open(media + f"\{self.uid}")
            rgb_im = image.convert('RGB')
            path = f'{settings.BASE_DIR}\output\{self.o_name}.webp'
            rgb_im.save(path)
            path = f"output\{self.o_name}.webp"
            return path
    
    def webp2png(self):
        return self.jpg2png()
    
    def jpg2webp(self):
        return self.img2webp()
    
    def webp2jpg(self):
        return self.png2jpg()


    def img2pdf(self):
        """
        Convert image (PNG/JPG) to PDF
        """
        if len(self.file_total) > 1:
            temp_folder = f"{media}\{self.id}_temp"
            files = os.listdir(temp_folder)
            destination = f"{settings.BASE_DIR}\output\{self.o_name}.pdf"
            with open(destination, "ab") as f:
                f.write(i2p.convert([f"{temp_folder}\{i}" for i in files]))
            path = f"output\{self.o_name}.pdf"
            return path

        else:
            source = media + f"\{self.uid}"
            destination = f"{settings.BASE_DIR}\output\{self.o_name}.pdf"
            with open(f"{destination}", "wb") as f:
                f.write(i2p.convert(source))
            path = f"output\{self.o_name}.pdf"
            return path

    def pdf2img(self):
        """
        """
        source = media + f"\{self.uid}"
        pages = p2i.convert_from_path(source, poppler_path=f"{settings.BASE_DIR}\libs\poppler")
        temp_folder = f"{media}\{self.id}_temp"
        os.mkdir(temp_folder)
        files = []
        
        for i in range(len(pages)):
            file_name = f"{temp_folder}\{self.o_name}-{i}.jpg"
            pages[i].save(file_name, "JPEG")
            files.append(file_name)
        
        self.archive()
        return f"output\{self.o_name}.zip"

    def pdfmerge(self):
        temp_folder = f"{media}\{self.id}_temp"
        files = os.listdir(temp_folder)
        merger = PdfFileMerger()
        for pdf in files:
            merger.append(fileobj=open(f"{temp_folder}\{pdf}", 'rb'))

        merger.write(f"{settings.BASE_DIR}\output\{self.o_name}.pdf")
        merger.close()
        path = f"output\{self.o_name}.pdf"
        return path
    
    def pdf2speech(self):
        location = f"{media}\{self.uid}"
        pdf_file = open(location, 'rb')
        pdf_Reader = PyPDF2.PdfFileReader(pdf_file)
        pages = pdf_Reader.numPages
        textList = []

        for i in range(pages):
            try:
                page = pdf_Reader.getPage(i)    
                textList.append(page.extractText())
            except:
                pass
    
        text = " ".join(textList)
        audio = gTTS(text=text, lang="en", slow=False)
        destination = path = f"{settings.BASE_DIR}\output\{self.o_name}.mp3"
        audio.save(destination)
        path = f"output\{self.o_name}.mp3"
        return path


    #def pdf2docx(self):
    #    pdf_file = media + f'\{self.uid}'
    #    docx_file = f'output\{self.o_name}.docx'

    #    p2d.parse(pdf_file, docx_file)
    #    return docx_file

    def docx2pdf(self):
        docx_file = media + f'\{self.uid}'
        pdf_file = f'{settings.BASE_DIR}\output\{self.o_name}.pdf'
        
        d2p.convert(docx_file, pdf_file)
        path = f"output\{self.o_name}.pdf"
        return pdf_file

    def mkv2mp4(self):
        location = f"{media}\{self.uid}"
        out_name = f"{settings.BASE_DIR}\output\{self.o_name}.mp4"
        ffmpeg.input(location).output(out_name).run(overwrite_output=True, cmd=f'{settings.BASE_DIR}\libs\\ffmpeg.exe')
        path = f"output\{self.o_name}.mp4"
        return path
        