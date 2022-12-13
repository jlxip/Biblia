#!/usr/bin/env python

import os

if not os.path.isdir('libros'):
    print('🫠')
    exit()
if os.path.isdir('dist'):
    print('🤨')
    exit()

# jinja2
import jinja2 as jj2
env = jj2.Environment(
    loader=jj2.FileSystemLoader('./template'),
    autoescape=jj2.select_autoescape()
)

index_t = env.get_template('index.html')
libro_t = env.get_template('libro.html')
cap_t = env.get_template('cap.html')

# Vámonos
os.mkdir('dist')
os.mkdir('dist/libros')

# Construir cada libro
libros = os.listdir('libros')
libros = sorted(libros)
for i in libros:
    libro = i.split('-')[1]
    os.mkdir('dist/libros/'+libro)

    caps = os.listdir('libros/'+i)
    caps = sorted(caps)

    rcaps = list(range(1, len(caps)+1))
    with open('dist/libros/%s/index.html' % libro, 'w') as f:
        f.write(libro_t.render(libro=libro, caps=rcaps))

    # Cada capítulo
    for j in caps:
        cap = j.split('.txt')[0]
        with open('libros/%s/%s' % (i, j), 'r') as f:
            raw = f.read()
        raw = raw.split('---\n')
        versos = raw[0].splitlines()
        notas = raw[1] if len(raw) > 1 else ''

        # Omitir versos vacíos
        versos = [(a+1, b) for a, b in enumerate(versos) if b]
        with open('dist/libros/%s/%s.html' % (libro, cap), 'w') as f:
            f.write(cap_t.render(libro=libro, cap=cap, versos=versos, notas=notas))

# Construir index
with open('README.txt', 'r') as f:
    readme = f.read().replace('\n', '<br>')
libros = [i.split('-')[1] for i in libros]
with open('dist/index.html', 'w') as f:
    f.write(index_t.render(libros=libros, readme=readme))

# Copiar archivos estáticos
import shutil
shutil.copytree('static', 'dist/static')

# CNAME
with open('dist/CNAME', 'w') as f:
    f.write('biblia.jlxip.net')
