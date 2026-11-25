#!/usr/bin/env python3
"""Inspect the rendered companion PDF; optionally produce page images.

Dependencies: PyMuPDF; Pillow only when --render-dir is supplied.
This is a document-integrity check, not mathematical proof verification.
"""
from pathlib import Path
import argparse
import hashlib
import json
import fitz


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--render-dir', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    path = root / 'PNP_Best_Proof_Attempt_CC09_2026-11-24.pdf'
    doc = fitz.open(path)
    breaches, counts, texts, links = [], [], [], []
    if args.render_dir:
        from PIL import Image, ImageDraw
        args.render_dir.mkdir(parents=True, exist_ok=True)
    for i, page in enumerate(doc):
        text = page.get_text()
        texts.append(text)
        counts.append(len(text.split()))
        for block in page.get_text('blocks'):
            if block[0] < 40 or block[1] < 15 or block[2] > 574 or block[3] > 777:
                breaches.append({'page': i + 1, 'box': list(block[:4]), 'text': block[4][:80]})
        for link in page.get_links():
            links.append({'page': i + 1, 'kind': link['kind'],
                          'target': link.get('uri', link.get('page'))})
        if args.render_dir:
            page.get_pixmap(matrix=fitz.Matrix(1.2, 1.2), alpha=False).save(
                args.render_dir / f'page-{i + 1:02d}.png')
    if args.render_dir:
        for start in range(0, len(doc), 9):
            canvas = Image.new('RGB', (1320, 1725), '#dce4eb')
            draw = ImageDraw.Draw(canvas)
            for j in range(start, min(start + 9, len(doc))):
                im = Image.open(args.render_dir / f'page-{j + 1:02d}.png')
                im.thumbnail((420, 544))
                x, y = 10 + 440 * ((j - start) % 3), 10 + 575 * ((j - start) // 3)
                canvas.paste(im, (x, y))
                draw.text((x, y + 546), f'Page {j + 1}', fill='black')
            canvas.save(args.render_dir / f'montage-{start // 9 + 1}.png')
        (args.render_dir / 'extracted.txt').write_text('\n\n'.join(texts))
    all_text = '\n'.join(texts)
    required = ['Mathematical status', 'Open obligation 15', '48,770', '27,386', 'References']
    missing = [x for x in required if x not in all_text]
    bad_internal_links = [x for x in links if x['kind'] == 1 and
                          (not isinstance(x['target'], int) or not 0 <= x['target'] < len(doc))]
    result = {
        'pdf': path.name, 'pages': len(doc), 'bytes': path.stat().st_size,
        'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'words_extracted': sum(counts), 'page_word_counts': counts,
        'geometry_breaches': breaches, 'missing_required_text': missing,
        'unresolved_double_question_marks': all_text.count('??'),
        'bad_internal_links': bad_internal_links,
        'external_link_annotations': sum(x['kind'] == 2 for x in links),
        'outline_entries': len(doc.get_toc()),
        'scope': 'Document integrity only; not a proof assistant or mathematical referee.'
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    if breaches or missing or bad_internal_links or '??' in all_text:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
