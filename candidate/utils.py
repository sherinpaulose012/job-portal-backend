# candidate/utils.py

import os
from datetime import datetime

def resume_upload_path(instance, filename):

    extension = filename.split('.')[-1]

    new_filename = (
        f"candidate_{instance.user.id}_"
        f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
        f".{extension}"
    )

    return os.path.join(
        'resumes',
        new_filename
    )

import pdfplumber
from docx import Document


def extract_resume_text(file_path):

    if file_path.endswith(".pdf"):

        text = ""

        with pdfplumber.open(file_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:

                    text += page_text + "\n"

        return text

    elif file_path.endswith(".docx"):

        doc = Document(file_path)

        return "\n".join(
            para.text
            for para in doc.paragraphs
        )

    return ""

import re


def clean_resume_text(text):

    text = re.sub(r"\s+", " ", text)

    text = re.sub(r"\n+", "\n", text)

    return text.strip()

import re

from .skills import SKILLS


def extract_skills(text):

    text = text.lower()

    found = []

    for skill in SKILLS:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):

            found.append(skill)

    return sorted(list(set(found)))

import re


def extract_experience(text):

    pattern = r"(\d+)\+?\s+years?"

    matches = re.findall(pattern, text, flags=re.I)

    if matches:

        return max(int(x) for x in matches)

    return 0

def extract_education(text):

    degrees = [

        "bachelor",

        "master",

        "b.tech",

        "m.tech",

        "bsc",

        "msc",

        "phd",

        "mba"

    ]

    text = text.lower()

    result = []

    for degree in degrees:

        if degree in text:

            result.append(degree)

    return result

def tokenize(text):

    return text.split()

