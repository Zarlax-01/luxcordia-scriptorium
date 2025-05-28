# generate_markdown_structures.py

import os
import json
from typing import Dict, Any

# Dossiers d'entrée/sortie
INPUT_DIR = os.path.join("output", "fiches_bilingues")
OUTPUT_DIR = os.path.join("output", "markdown")

# Crée le dossier de sortie si nécessaire
def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

# Génère le contenu Markdown pour un fragment donné
def generate_markdown(data: Dict[str, Any]) -> str:
    entity = data.get("entity", "Unknown")
    cycle = data.get("cycle", "Unknown")
    themes = data.get("themes", [])
    original_fr = data.get("original_fr", "")
    original_en = data.get("original_en", "")
    summary_en = data.get("summary_request_en", "")
    summary_fr = data.get("summary_request_fr_back", "")

    md: list[str] = []
    md.append(f"# Fragment : {entity} // Cycle {cycle}\n")
    md.append(f"**Thèmes :** {', '.join(themes)}\n")
    md.append("---\n")
    md.append("## Texte Original (FR)\n")
    md.append(f"{original_fr}\n")
    md.append("---\n")
    md.append("## Translation (EN)\n")
    md.append(f"{original_en}\n")
    md.append("---\n")
    md.append("## Requête de Synthèse\n")
    md.append(f"- **EN** : {summary_en}\n")
    md.append(f"- **FR (vérification)** : {summary_fr}\n")
    md.append("---\n")
    md.append("## Usage Suggéré\n")
    md.append("- Podcast snippet\n")
    md.append("- Chant rituel\n")
    md.append("- Fragment pour Luxccordion\n")

    return "".join(md)

# Traitement principal
def main():
    ensure_output_dir()
    for fname in os.listdir(INPUT_DIR):
        if not fname.endswith('.json'):
            continue
        src_path = os.path.join(INPUT_DIR, fname)
        with open(src_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        markdown_content = generate_markdown(data)
        out_fname = fname.replace('.json', '.md')
        out_path = os.path.join(OUTPUT_DIR, out_fname)
        with open(out_path, 'w', encoding='utf-8') as out:
            out.write(markdown_content)

        print(f"[✓] Markdown généré : {out_fname}")

if __name__ == '__main__':
    main()
