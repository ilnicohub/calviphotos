#!/usr/bin/env python3
"""
Scans `photos/` subdirectories, generates thumbnails and JSON manifests:
- `galleries.json` at repo root with list of galleries
- `photos/<gallery>/index.json` with list of images and thumb paths

Requires Pillow. Run: `python3 scripts/generate_galleries.py`
"""
import os
import sys
import json
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHOTOS_DIR = os.path.join(ROOT, 'photos')

VALID_EXT = {'.jpg','.jpeg','.png','.webp'}

def ensure_dir(p):
    if not os.path.exists(p):
        os.makedirs(p, exist_ok=True)

def is_image(fname):
    return os.path.splitext(fname.lower())[1] in VALID_EXT

def make_thumb(src, dst, width=900):
    try:
        with Image.open(src) as im:
            im.convert('RGB')
            w,h = im.size
            if w <= width:
                im.save(dst, 'JPEG', quality=85)
            else:
                nh = int(width * h / w)
                im.resize((width, nh), Image.LANCZOS).save(dst, 'JPEG', quality=85)
        return True
    except Exception as e:
        print('Errore thumb', src, e)
        return False

def sane_title(name):
    return name.replace('-', ' ').replace('_', ' ')

def main():
    galleries = []
    if not os.path.isdir(PHOTOS_DIR):
        print('Nessuna cartella photos/ trovata. Crea `photos/<nome-partita>/` e aggiungi foto.')
        return 0

    for entry in sorted(os.listdir(PHOTOS_DIR)):
        gpath = os.path.join(PHOTOS_DIR, entry)
        if not os.path.isdir(gpath):
            continue
        # collect images
        files = [f for f in sorted(os.listdir(gpath)) if is_image(f)]
        if not files:
            continue
        thumbs_dir = os.path.join(gpath, 'thumbs')
        ensure_dir(thumbs_dir)

        images = []
        for fname in files:
            src = os.path.join(gpath, fname)
            thumb_name = os.path.splitext(fname)[0] + '.jpg'
            thumb_path = os.path.join(thumbs_dir, thumb_name)
            # create thumbnail if missing or older than source
            if not os.path.exists(thumb_path) or os.path.getmtime(thumb_path) < os.path.getmtime(src):
                ok = make_thumb(src, thumb_path)
                if not ok:
                    continue
            rel_file = os.path.join('photos', entry, fname).replace('\\','/')
            rel_thumb = os.path.join('photos', entry, 'thumbs', thumb_name).replace('\\','/')
            images.append({
                'name': fname,
                'file': '/' + rel_file,
                'thumb': '/' + rel_thumb
            })

        # write index.json for gallery
        gallery_index = {
            'title': sane_title(entry),
            'folder': entry,
            'count': len(images),
            'images': images
        }
        with open(os.path.join(gpath, 'index.json'), 'w', encoding='utf-8') as f:
            json.dump(gallery_index, f, ensure_ascii=False, indent=2)

        galleries.append({
            'title': gallery_index['title'],
            'folder': entry,
            'count': len(images),
            'preview': images[0]['thumb'] if images else ''
        })

    # write galleries.json at root
    out = os.path.join(ROOT, 'galleries.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(galleries, f, ensure_ascii=False, indent=2)

    print(f'Generati {len(galleries)} gallerie.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
