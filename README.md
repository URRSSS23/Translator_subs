# Translator_subs
Translate subtitles easy

```bash

pip install googletrans==4.0.0-rc1 deepl regex argparse tqdm
```


```bash
# for lang 
python -c "from googletrans import LANGUAGES; print(LANGUAGES)"
```
```bash
#RO
python translate.py "test.ass" --model google --lang ro
```

```bash
python translate.py "test.ass" --model deepl --lang en,fr
```

```bash
# for multiple translate
python translate.py "test1.ass" "test2.ass" --model google --lang es
```
More functions:
```bash
# Specify source language: If the subtitle is in English, but you want to make sure it detects correctly:
-
python translate.py "test.ass" --model google --lang ro --source en
```
```bash
# Automatic fallback between APIs: If DeepL crashes, it automatically switches to Google Translate:

python translate.py "test.ass" --model deepl --lang ro --fallback
```
```bash
# Limit to a number of lines: Translate only the first 50 lines for the test:

python translate.py "test.ass" --model google --lang ro --limit 50
```
