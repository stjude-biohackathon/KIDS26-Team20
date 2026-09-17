"""
Document processing functions for PDFs and other file formats
"""
import fitz
import base64
import os
import shutil
import subprocess
import requests
import re
import tempfile
from pathlib import Path
from defusedxml import ElementTree as ET
from pypdf import PdfReader
from langchain_community.llms import Ollama


class ExtractedPDFPage:
    """A lightweight page wrapper that preserves the extract_text() interface."""

    def __init__(self, text, page_number):
        self._text = text or ""
        self.page_number = page_number

    def extract_text(self):
        return self._text


def _contains_devanagari(text):
    return bool(re.search(r"[\u0900-\u097F]", text or ""))


def _is_probably_garbled(text):
    if not text:
        return True

    stripped = text.strip()
    if not stripped:
        return True

    # Common marker when font-to-unicode mappings are missing in PDFs.
    if len(re.findall(r"\(cid:\d+\)", stripped)) >= 3:
        return True

    replacement_chars = stripped.count("\ufffd") + stripped.count("\x00")
    if replacement_chars / max(len(stripped), 1) > 0.02:
        return True

    return False


def getPDFContent(path):
    """Extract text from PDF pages with Hindi-friendly fallback handling."""
    try:
        reader = PdfReader(path, strict=False)
        if len(reader.pages) == 0:
            print(f"PDF structure error: no pages found in {path}")
            return []

        extracted_pages = []

        # PyMuPDF often extracts Indic scripts more reliably than pypdf for some fonts.
        with fitz.open(path) as fitz_doc:
            for i, page in enumerate(reader.pages):
                pypdf_text = page.extract_text() or ""
                fitz_text = ""

                if i < len(fitz_doc):
                    fitz_text = fitz_doc[i].get_text("text") or ""

                use_fitz = False
                if _is_probably_garbled(pypdf_text) and fitz_text.strip():
                    use_fitz = True
                elif not _contains_devanagari(pypdf_text) and _contains_devanagari(fitz_text):
                    use_fitz = True
                elif not pypdf_text.strip() and fitz_text.strip():
                    use_fitz = True

                final_text = fitz_text if use_fitz else pypdf_text
                extracted_pages.append(ExtractedPDFPage(final_text, i + 1))

        return extracted_pages
    except Exception as e:
        print(f"Error reading PDF {path}: {e}")
        return []


def convert_to_pdf(input_file, output_dir):
    """Convert files to PDF using LibreOffice"""
    # Validate and normalize input path within safe directory
    safe_input_root = os.path.realpath('data/pdfs')
    if not safe_input_root.endswith(os.sep):
        safe_input_root += os.sep

    normalized_input = os.path.realpath(input_file)
    if not normalized_input.startswith(safe_input_root):
        raise ValueError("Input file is outside the safe directory")

    input_path = Path(normalized_input)

    # Validate and normalize output path within safe directory
    safe_output_root = os.path.realpath('data/pdfs')
    if not safe_output_root.endswith(os.sep):
        safe_output_root += os.sep

    normalized_output = os.path.realpath(output_dir)
    if not normalized_output.startswith(safe_output_root):
        raise ValueError("Output directory is outside the safe directory")

    output_path = Path(normalized_output)

    allowed_extensions = {'.doc', '.docx', '.txt'}

    if input_path.suffix.lower() not in allowed_extensions:
        raise ValueError("Unsupported file type for PDF conversion")
    if not input_path.is_file():
        raise ValueError("Input file does not exist")
    if not output_path.is_dir():
        raise ValueError("Output directory does not exist")

    staged_name = {
        '.doc': 'input.doc',
        '.docx': 'input.docx',
        '.txt': 'input.txt',
    }[input_path.suffix.lower()]
    output_stem = input_path.stem
    valid_stem = (
        output_stem
        and len(output_stem) <= 255
        and output_stem.isascii()
        and all(character.isalnum() or character in '_-' for character in output_stem)
    )
    if not valid_stem:
        raise ValueError("Invalid output filename")
    output_name = f'{output_stem}.pdf'

    # Normalize and validate the destination path stays within the output directory
    output_root = os.fspath(output_path)
    if not output_root.endswith(os.sep):
        output_root += os.sep

    normalized_destination = os.path.realpath(
        os.path.join(output_root, output_name)
    )

    if not normalized_destination.startswith(output_root):
        raise ValueError("Output path is outside the output directory")

    destination = Path(normalized_destination)

    # Use only fixed command arguments; user-controlled paths stay outside the subprocess.
    with tempfile.TemporaryDirectory() as temporary_directory:
        temporary_path = Path(temporary_directory)
        shutil.copyfile(input_path, temporary_path / staged_name)
        command = ["soffice", "--headless", "--convert-to", "pdf", staged_name]
        subprocess.run(command, check=True, shell=False, cwd=temporary_directory)
        shutil.move(temporary_path / 'input.pdf', destination)


def extractPDFImages(path, title, data_list):
    """Extract images from PDF and describe them using LLaVA"""
    pdf_file = fitz.open(path)
    for page_index in range(len(pdf_file)):
        page = pdf_file[page_index]
        image_list = page.get_images()
        for image_index, img in enumerate(image_list, start=1):
            xref = img[0]
            base_image = pdf_file.extract_image(xref)
            image_bytes = base_image["image"]
            image_b64 = base64.b64encode(image_bytes).decode("utf-8")
            prompt = 'Describe this image and make sure to include anything notable about it (include text you see in the image): '
            ollama = Ollama(base_url="http://localhost:11434", model="llava")
            response = ollama.invoke(prompt, images=[image_b64])
            print(response, end='', flush=True)
            data_list.append({'title': title, 'page': page_index, 'content': response, 'type': 'image'})


def highlight_pdf(input_file, output_file, source_grp):
    """Highlight PDF based on source groups with color coding"""
    input_pdf = fitz.open(input_file)
    # iterate through source_grp
    for source in source_grp:
        page_idx = source['page'] - 1
        highlight_text = source['context']
        for idx in range(len(input_pdf)):
            if idx != page_idx:
                continue
            page = input_pdf[idx]
            hightlight_sentences = highlight_text.split('.')
            hightlight_sentences = [sentence for sentence in hightlight_sentences if len(sentence) > 10]
            for sentence in hightlight_sentences:
                if(len(sentence) == 0):
                    continue
                text_instances = page.search_for(sentence)

                for inst in text_instances:
                    highlight = page.add_highlight_annot(inst)
                    highlight.set_colors()
                    highlight.update()

                    if 'vector_score' in source and 'bm25_score' in source:
                        if source['vector_score'] > 0.5 or source['bm25_score'] > 0.5:
                           # highlight with green color rgb(120, 198, 121)
                            highlight.set_colors(stroke=[0.486, 0.988, 0])
                            highlight.update()
                        elif source['vector_score'] > 0.3 or source['bm25_score'] > 0.3:
                            # highlight with yellow color
                            highlight.set_colors(stroke=[1, 1, 0])
                            highlight.update()
                        elif source['vector_score'] > 0.15 or source['bm25_score'] > 0.15:
                            # highlight with light yellow color (247, 252, 185)
                            highlight.set_colors(stroke=[0.97, 0.98, 0.72])
                            highlight.update()
                        else:
                            # highlight gray (220,220,220)
                            highlight.set_colors(stroke=[0.863, 0.863, 0.863])
                            highlight.update()

                    # check if source has distance key
                    elif 'vector_score' in source:
                        if source['vector_score'] > 0.5:
                            # highlight with green color rgb(120, 198, 121)
                            highlight.set_colors(stroke=[0.486, 0.988, 0])
                            highlight.update()
                        elif source['vector_score'] > 0.3:
                            # highlight with yellow color
                            highlight.set_colors(stroke=[1, 1, 0])
                            highlight.update()
                        elif source['vector_score'] > 0.15:
                            # highlight with light yellow color (247, 252, 185)
                            highlight.set_colors(stroke=[0.97, 0.98, 0.72])
                            highlight.update()
                        else:
                            # highlight gray (220,220,220)
                            highlight.set_colors(stroke=[0.863, 0.863, 0.863])
                            highlight.update()

                    # check if source has score key
                    elif 'bm25_score' in source:
                        if source['bm25_score'] > 0.5:
                            # highlight with green color rgb(120, 198, 121)
                            highlight.set_colors(stroke=[0.486, 0.988, 0])
                            highlight.update()
                        elif source['bm25_score'] > 0.3:
                            # highlight with yellow color
                            highlight.set_colors(stroke=[1, 1, 0])
                            highlight.update()
                        elif source['bm25_score'] > 0.15:
                            # highlight with light yellow color (247, 252, 185)
                            highlight.set_colors(stroke=[0.97, 0.98, 0.72])
                            highlight.update()
                        else:
                            # highlight gray (220,220,220)
                            highlight.set_colors(stroke=[0.863, 0.863, 0.863])
                            highlight.update()
                    
                    else:
                        # highlight gray (220,220,220)
                        highlight.set_colors(stroke=[0.863, 0.863, 0.863])
                        highlight.update()

    input_pdf.save(output_file, garbage=4, deflate=True, clean=True)


def get_toc_from_grobid(pdf_path):
    """
    Extract the table of contents from a PDF file using GROBID.
    Grobid is available at http://localhost:8070 by default.
    """
    # Validate and normalize PDF path within safe directory
    safe_pdf_root = os.path.realpath('data/pdfs')
    if not safe_pdf_root.endswith(os.sep):
        safe_pdf_root += os.sep

    normalized_pdf_path = os.path.realpath(pdf_path)
    if not normalized_pdf_path.startswith(safe_pdf_root):
        raise ValueError("PDF path is outside the safe directory")

    # Use GROBID to extract the table of contents
    url = 'http://host.docker.internal:8070/api/processFulltextDocument'
    files = {'input': open(normalized_pdf_path, 'rb')}
    data = {'consolidateHeader': '1', 'teiCoordinates': 'head'}
    response = requests.post(url, files=files, data=data)
    
    # Parse the response to get the table of contents
    toc = []
    if response.status_code == 200:
        xml_content = response.content
        # Parse the XML content and get <head> elements across entire XML
        root = ET.fromstring(xml_content)

        for head in root.findall('.//{http://www.tei-c.org/ns/1.0}head'):
            # Extract the text from the <head> element
            head_text = head.text.strip() if head.text else ''
            # get page number from coords attribute from head <head coords="1,72.02,292.61,212.67,11.99"> 
            coords = head.get('coords')
            page = coords.split(',')[0] if coords else '1'
            # add to toc if not empty as pymupdf format
            if head_text:
                toc.append([1, head_text, int(page) ])  # Assuming level 1 for all headings
            
    else:
        print(f"Error: {response.status_code} - {response.text}")

    # remove header and footer from toc by removing repetitive elements
    if len(toc) > 0:
        # find most common element in toc
        for i in range(len(toc)-1, 0, -1):
            if toc[i][1] == toc[i-1][1]:
                toc.pop(i)
    
    return toc
