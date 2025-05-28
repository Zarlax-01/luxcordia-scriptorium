# scripts/translate_bi.py
from typing import Any
from googletrans import Translator  # type: ignore
import os, json

INPUT_DIR  = "output/syntheses"
OUTPUT_DIR = "output/fiches_bilingues"

def translate_text(translator: Any, text: str, dest: str) -> str:
    return translator.translate(text, dest=dest).text

def process_file(translator: Any, filename: str):
    data = json.load(open(os.path.join(INPUT_DIR, filename), encoding="utf-8"))
    original = data.get("original_text", "")
    summary_request = data.get("summary_request", "")

    # Sécurité : ignorer si texte manquant
    if not original or not summary_request:
        print(f"[⚠] Skipped (missing fields) : {filename}")
        return

    en = translate_text(translator, original, "en")
    fr_back = translate_text(translator, summary_request, "fr")

    bilingual: dict[str, str] = {
        "entity": data["entity"],
        "cycle": data["cycle"],
        "themes": data["themes"],
        "original_fr": original,
        "original_en": en,
        "summary_request_en": summary_request,
        "summary_request_fr_back": fr_back,
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, filename)
    with open(out_path, "w", encoding="utf-8") as out:
        json.dump(bilingual, out, ensure_ascii=False, indent=2)

    print(f"[✓] Gratuit traduit : {filename} → {out_path}")

if __name__ == "__main__":
    translator = Translator()
    for fn in os.listdir(INPUT_DIR):
        if fn.endswith(".json"):
            process_file(translator, fn)
