# -*- coding: utf-8 -*-
"""Build the portfolio. Python 3 standard library only."""
from pathlib import Path
from html import escape
import json, shutil
ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'src/data'
OUT = ROOT / 'dist'
def read(name): return json.loads((DATA / (name+'.json')).read_text())
def esc(value): return escape(str(value), quote=True)
site = read('site')
def pill(label, href): return f'<a class="pill" href="{esc(href)}">{esc(label)}</a>'
def image(src, alt, eager=False): return f'<img src="{esc(src)}" alt="{esc(alt)}" loading="{"eager" if eager else "lazy"}" decoding="async">'
def card(project):
 return f'''<a class="project-card" href="{esc(project['slug'])}.html">{image(project['cover'],project['title'])}<div class="card-title"><h3>{esc(project['title'])}</h3><span class="arrow" aria-hidden="true">↗</span></div><p>{esc(project['description'])}</p></a>'''
def experience(job):
 company=f'<a href="{esc(job["url"])}">{esc(job["company"])}</a>' if job['url'] else esc(job['company'])
 return f'<article class="job"><h3>{company}</h3><p class="period">{esc(job["period"])}</p><div class="prose">{job["body"]}</div></article>'
def contacts():
 return f'''<footer class="contacts" id="Contacts"><h2>Контакты</h2><dl><div><dt>Телеграм</dt><dd><a href="https://t.me/{esc(site['telegram'].lower())}">@{esc(site['telegram'])}</a></dd></div><div><dt>Почта</dt><dd><a href="mailto:{esc(site['email'])}">{esc(site['email'])}</a></dd></div></dl></footer>'''
def shell(title, body, description=None):
 return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(description or site['intro'])}"><meta name="theme-color" content="#fafafa"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description or site['intro'])}"><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="styles/tokens.css"><link rel="stylesheet" href="styles/site.css"></head><body><a class="skip-link" href="#main">К содержимому</a>{body}</body></html>'''
def home():
 nav=''.join(pill(label,href) for label,href in [('Кейсы','#Case'),('Резюме','#CV'),('Контакты','#Contacts')])
 return shell(site['title'],f'''<main id="main"><header class="hero"><nav aria-label="Основная навигация">{nav}</nav><div class="hero-intro">{image(site['portrait'],'Марьям — UX/UI дизайнер',True)}<h1>{esc(site['intro'])}</h1></div></header><section class="projects section" id="Case"><h2>Кейсы, которыми хочу поделиться</h2><div class="project-grid">{''.join(card(p) for p in site['projects'])}</div></section><section class="resume section" id="CV"><h2>Резюме</h2><div class="resume-card">{''.join(experience(j) for j in site['experience'])}</div></section></main>{contacts()}''')
def case(project):
 blocks=read(project['slug']);body='';has_h1=False
 for index,b in enumerate(blocks):
  if b['type']=='image': body+=f'<figure class="case-image">{image(b["src"],b["alt"],index<3)}</figure>'
  elif b['type']=='heading':
   level=1 if b['level']==1 and not has_h1 else 2
   has_h1 |= level==1
   body+=f'<h{level}>{b["html"]}</h{level}>'
  else: body+=f'<div class="prose">{b["html"]}</div>'
 if not has_h1:body=f'<h1 class="sr-only">{esc(project["title"])}</h1>'+body
 index=site['projects'].index(project);nxt=site['projects'][(index+1)%len(site['projects'])]
 return shell(project['title']+' — '+site['name'],f'''<header class="case-nav">{pill('← Назад к портфолио','index.html#Case')}</header><main class="case" id="main">{body}<nav class="case-next" aria-label="Следующий кейс"><span>Следующий кейс</span><a href="{nxt['slug']}.html">{esc(nxt['title'])} ↗</a></nav></main>{contacts()}''',project['description'])
def design_system():
 colors=[('Фон','--color-background'),('Поверхность','--color-surface'),('Текст','--color-text'),('Акцент','--color-accent')]
 swatches=''.join(f'<div><span class="swatch" style="background:var({token})"></span><strong>{name}</strong><code>{token}</code></div>' for name,token in colors)
 return shell('Дизайн-система портфолио',f'''<header class="case-nav">{pill('← Портфолио','index.html')}</header><main class="case system" id="main"><h1>Дизайн-система</h1><p>Общие правила и компоненты портфолио. Изменения в tokens.css применяются ко всему сайту.</p><h2>Палитра</h2><div class="swatches">{swatches}</div><h2>Типографика</h2><p class="type-sample">Заголовок первого уровня</p><h2>Заголовок раздела</h2><h3>Название проекта</h3><p>Основной текст — Inter, 16 px. Шрифты хранятся в проекте.</p><h2>Кнопки и ссылки</h2>{pill('Посмотреть кейсы','index.html#Case')}<h2>Карточка проекта</h2><div class="system-card">{card(site['projects'][0])}</div><h2>Размеры</h2><p>Скругления: 32 / 24 / 999 px. Шаг отступов: 8 px. Сетка проектов: две колонки на широком экране, одна на узком.</p></main>''')
def build():
 OUT.mkdir(exist_ok=True)
 shutil.copytree(ROOT/'public',OUT,dirs_exist_ok=True)
 shutil.copytree(ROOT/'src/styles',OUT/'styles',dirs_exist_ok=True)
 (OUT/'index.html').write_text(home())
 for project in site['projects']:(OUT/(project['slug']+'.html')).write_text(case(project))
 (OUT/'design-system.html').write_text(design_system())
 print('Готово: dist/index.html. Предпросмотр: python3 -m http.server 8080 --directory dist')
if __name__=='__main__':build()
