#!/usr/bin/env python3
"""
fix_admin.py — Corrige tous les bugs JS de shop_admin.html
Usage: python3 fix_admin.py [chemin/vers/shop_admin.html]
"""
import sys, re, os

path = sys.argv[1] if len(sys.argv) > 1 else 'templates/shop_admin.html'
if not os.path.exists(path):
    print(f"ERREUR: {path} introuvable")
    sys.exit(1)

with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

original = html
fixes = 0

# Fix 1: Apostrophes cassantes dans les strings JS
for old, new in [
    ("Appliquer l'image", "Appliquer l\\'image"),
    ("Lancer l'audit",    "Lancer l\\'audit"),
]:
    n = html.count(old)
    if n:
        html = html.replace(old, new)
        print(f"Fix apostrophe '{old}' ({n}x)")
        fixes += n

# Fix 2: SECS array
m = re.search(r"(const SECS=\[[^\]]+)\]", html)
if m and 'wordpress' not in m.group(0):
    html = html.replace(m.group(0), m.group(1) + ",'wordpress','seo','keywords','calendar']")
    print("Fix SECS array (+wordpress/seo/keywords/calendar)")
    fixes += 1

# Fix 3: go() routing WordPress
if "n==='wordpress'" not in html:
    m2 = re.search(r"(if\(n==='apropos'\)[^\n]+\n)\}", html)
    if m2:
        html = html.replace(m2.group(0),
            m2.group(1) +
            "  if(n==='wordpress') { if(typeof loadWordPress==='function') loadWordPress(); }\n"
            "  if(n==='seo') { if(typeof initSEOPanel==='function') initSEOPanel(); }\n"
            "  if(n==='keywords') { if(typeof initKeywordsPanel==='function') initKeywordsPanel(); }\n"
            "  if(n==='calendar') { if(typeof initCalendarPanel==='function') initCalendarPanel(); }\n}", 1)
        print("Fix go() routing WordPress")
        fixes += 1

# Fix 4: loadWordPress function
if 'function loadWordPress' not in html and 'function initSEOPanel' in html:
    html = html.replace(
        'function initSEOPanel',
        'function loadWordPress(){if(typeof checkWPStatus==="function")checkWPStatus();if(typeof loadWPPosts==="function")loadWPPosts();}\nfunction initSEOPanel', 1)
    print("Fix loadWordPress() ajoutee")
    fixes += 1

# Fix 5: KniUI polyfill (si KniUI utilisé mais non défini)
if 'KniUI.danger' in html and 'window.KniUI = {' not in html:
    POLYFILL = '''
/* KniUI POLYFILL */
if (typeof KniUI === 'undefined') {
  window.KniUI = {
    toast: Object.assign(
      function(opts){ toast(typeof opts==='string' ? opts : (opts.msg||''), opts.type!=='error'); },
      { success:(m,t)=>toast((t?t+' — ':'')+m,true), error:(m,t)=>toast((t?t+' — ':'')+m,false), warning:(m,t)=>toast((t?t+' — ':'')+m,false) }
    ),
    danger:  async(m,o)=>confirm((o&&o.title?o.title+'\\n\\n':'')+m.replace(/<[^>]+>/g,'')),
    confirm: async(m,o)=>confirm((o&&o.title?o.title+'\\n\\n':'')+m.replace(/<[^>]+>/g,'')),
    warning: async(m,o)=>confirm((o&&o.title?o.title+'\\n\\n':'')+m.replace(/<[^>]+>/g,'')),
    loading: { show:(m)=>{const e=document.getElementById('kniLoadOverlay');if(e)e.style.display='flex';}, hide:()=>{const e=document.getElementById('kniLoadOverlay');if(e)e.style.display='none';} },
  };
}
'''
    # Insérer après toast()
    pos = html.find('t._t=setTimeout')
    if pos > 0:
        end = html.find('\n}', pos) + 2
        html = html[:end] + '\n' + POLYFILL + html[end:]
        print("Fix KniUI polyfill ajouté")
        fixes += 1

# Fix 6: pcard cliquable
if 'onclick="showProd({{ p.id }})"' not in html:
    old = '<div class="pcard" data-cat="{{ p.category }}" data-nm="{{ p.name|lower }}" data-stk="{{ p.stock }}" id="pc-{{ p.id }}">'
    new = '<div class="pcard" data-cat="{{ p.category }}" data-nm="{{ p.name|lower }}" data-stk="{{ p.stock }}" id="pc-{{ p.id }}" onclick="showProd({{ p.id }})" style="cursor:pointer">'
    if old in html:
        html = html.replace(old, new)
        print("Fix pcard onclick='showProd()' ajouté")
        fixes += 1

if html == original:
    print("Aucun fix nécessaire (fichier déjà à jour)")
else:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"\n✅ {fixes} fix(es) appliqué(s) → {path}")
