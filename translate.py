import argparse
import regex as re
import os
import deepl
from tqdm import tqdm
from googletrans import Translator, LANGUAGES

DEEPL_API_KEY = "INSERT_YOUR_DEEPL_API_KEY"
deepl_translator = deepl.Translator(DEEPL_API_KEY) if DEEPL_API_KEY else None
translator = Translator()

ASS_TAG_PATTERN = re.compile(r"(\{.*?\})")

def extract_dialogue_lines(file_path):
    """Extrage liniile de subtitrare și păstrează structura"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        dialogue_lines = [line for line in lines if line.startswith("Dialogue:")]
        return lines, dialogue_lines
    except Exception as e:
        print(f"Eroare la citirea fișierului '{file_path}': {e}")
        return [], []

def split_text_preserving_tags(text):
    """Împarte textul păstrând tag-urile ASS"""
    segments = ASS_TAG_PATTERN.split(text)
    return [segment for segment in segments if segment.strip()]

def translate_text(text, target_lang="en", source_lang=None, model="google", fallback=False):
    """Traduce textul păstrând tag-urile ASS, cu fallback între API-uri"""
    segments = split_text_preserving_tags(text)
    translated_segments = []

    for segment in segments:
        if ASS_TAG_PATTERN.match(segment):
            translated_segments.append(segment)
        else:
            try:
                if model == "google":
                    translated_segments.append(translator.translate(segment, src=source_lang, dest=target_lang).text)
                elif model == "deepl" and deepl_translator:
                    translated_segments.append(deepl_translator.translate_text(segment, source_lang=source_lang, target_lang=target_lang).text)
                else:
                    translated_segments.append(segment) 
            except Exception as e:
                if fallback:
                    print(f" {model.capitalize()} a eșuat. Se încearcă alt API...")
                    return translate_text(text, target_lang, source_lang, "google" if model == "deepl" else "deepl", False)
                else:
                    print(f"Eroare la traducere: {e}")
                    translated_segments.append(segment) 

    return "".join(translated_segments)

def translate_ass_file(input_file, output_file, target_langs, model="google", source_lang=None, fallback=False, limit=None):
    """Traduce un fișier .ass și creează versiuni traduse"""
    lines, dialogue_lines = extract_dialogue_lines(input_file)

    if not lines:
        return

    for lang in target_langs:
        if lang not in LANGUAGES:
            print(f"Limba '{lang}' nu este suportată.")
            continue

        translated_lines = []
        temp_output = f"{os.path.splitext(output_file)[0]}_{lang}.ass"

        print(f"\nTraducere în {LANGUAGES[lang].upper()} ({model})...")

        count = 0
        for line in tqdm(lines, desc=f"Traducere în {lang.upper()}", unit="linie"):
            if line in dialogue_lines:
                if limit and count >= limit:
                    translated_lines.append(line)
                    continue
                count += 1

                parts = line.split(",", 9)
                original_text = parts[-1].strip()
                translated_text = translate_text(original_text, lang, source_lang, model, fallback)
                parts[-1] = translated_text
                translated_lines.append(",".join(parts))
            else:
                translated_lines.append(line)

        with open(temp_output, "w", encoding="utf-8") as file:
            file.writelines(translated_lines)

        print(f"Fișier tradus salvat: {temp_output}")

parser = argparse.ArgumentParser(description="Traducător avansat pentru fișiere .ass")
parser.add_argument("files", nargs="+", help="Fișierele .ass care trebuie traduse")
parser.add_argument("--model", choices=["google", "deepl"], default="google", help="Alege modelul de traducere")
parser.add_argument("--lang", required=True, help="Limbi pentru traducere (ex: en,fr,ro)")
parser.add_argument("--source", help="Limbă sursă (implicit autodetect)")
parser.add_argument("--fallback", action="store_true", help="Activează fallback între API-uri")
parser.add_argument("--limit", type=int, help="Număr maxim de replici traduse")

args = parser.parse_args()
target_langs = args.lang.split(",")

for file in args.files:
    if os.path.exists(file):
        output_file = file.replace(".ass", "_translated.ass")
        translate_ass_file(file, output_file, target_langs, args.model, args.source, args.fallback, args.limit)
    else:
        print(f"Fișierul nu există: {file}")
    
