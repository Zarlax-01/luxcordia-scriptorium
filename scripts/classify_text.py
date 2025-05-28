# classify_text.py

import os
import re
import json

INPUT_DIR = "input/fragments_raw"
OUTPUT_DIR = "output/syntheses"

def detect_entity_and_cycle(text):
    match = re.search(r"\[(\w+)\s*//\s*Cycle\s*(\w+)", text)
    if match:
        entity = match.group(1)
        cycle = match.group(2)
        return entity, cycle
    return "Unknown", "Unknown"

def classify_text(text):
    themes = []
    if "feu" in text or "brûle" in text:
        themes.append("transmutation")
    if "je" in text and "souffre" in text:
        themes.append("sacrifice")
    if "vérité" in text or "ombre" in text:
        themes.append("révélation")
    return themes if themes else ["non déterminé"]

def generate_deepseek_format(entity, cycle, text, themes):
    return {
        "source": "Luxcordia-SCRIPTORIVM",
        "entity": entity,
        "cycle": cycle,
        "themes": themes,
        "language": "FR",
        "original_text": text,
        "summary_request": "Please analyze this fragment and suggest symbolic, poetic and cultural interpretations based on your models."
    }

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".txt"):
            with open(os.path.join(INPUT_DIR, filename), "r", encoding="utf-8") as f:
                text = f.read()
            
            entity, cycle = detect_entity_and_cycle(text)
            themes = classify_text(text)
            deepseek_data = generate_deepseek_format(entity, cycle, text, themes)

            output_path = os.path.join(OUTPUT_DIR, filename.replace(".txt", ".json"))
            with open(output_path, "w", encoding="utf-8") as out:
                json.dump(deepseek_data, out, ensure_ascii=False, indent=2)

            print(f"[✓] Fragment traité : {filename} → {output_path}")

if __name__ == "__main__":
    main()
