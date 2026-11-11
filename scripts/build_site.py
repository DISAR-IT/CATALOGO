#!/usr/bin/env python3
"""Genera el sitio estático DISAR a partir de los productos gestionados en Pages CMS.
No necesita paquetes Python externos.
"""
from pathlib import Path
import json, shutil, sys

BASE = Path(__file__).resolve().parents[1]
DIST = BASE / 'dist'
CONTENT = BASE / 'content' / 'productos'


def build():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    shutil.copy2(BASE / 'index.html', DIST / 'index.html')
    if (BASE / 'images').is_dir():
        shutil.copytree(BASE / 'images', DIST / 'images', dirs_exist_ok=True)
    result=[]
    codes={}
    for path in sorted(CONTENT.glob('*.json')):
        try:
            record=json.loads(path.read_text(encoding='utf-8'))
        except (ValueError,OSError) as exc:
            raise ValueError(f'JSON inválido: {path}: {exc}') from exc
        if not all(str(record.get(k) or '').strip() for k in ('id','title','category','brand')):
            raise ValueError(f'Faltan código, título, categoría o marca en {path}')
        if record.get('visible') is False:
            continue
        uid=path.stem
        record['_uid']=uid
        # Los prefijos de ruta absolutos que guarda Pages CMS se vuelven
        # relativos, para funcionar también en un subdirectorio de GitHub Pages.
        image=str(record.get('image') or '')
        if image.startswith('/images/'):
            record['image']=image[1:]
        record['tags']=' '.join(str(record.get(k) or '') for k in ('title','id','brand','category','desc','keywords'))
        record.setdefault('imageUrl','')
        record.setdefault('price',None)
        code=str(record['id'])
        codes.setdefault(code,[]).append(uid)
        result.append(record)
    result.sort(key=lambda p: (int(p.get('order') or 0) if int(p.get('order') or 0)>0 else 999999, str(p['title'])))
    dest=DIST/'data'/'productos.json'
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(result,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    duplicates={k:v for k,v in codes.items() if len(v)>1}
    print(f'Catálogo generado: {len(result)} productos visibles.')
    if duplicates:
        print(f'Aviso: {len(duplicates)} códigos repetidos; los artículos conservan IDs internos distintos: {duplicates}')
    missing=[]
    for p in result:
        img=p.get('image','')
        if img.startswith('images/') and not (DIST/img).is_file() and not p.get('imageUrl'):
            missing.append(img)
    if missing:
        print(f'Aviso: faltan {len(missing)} fotografías locales en images/ (no venían en el HTML original).')
    return len(result)

if __name__ == '__main__':
    try: build()
    except Exception as exc:
        print(f'ERROR: {exc}',file=sys.stderr)
        sys.exit(1)
