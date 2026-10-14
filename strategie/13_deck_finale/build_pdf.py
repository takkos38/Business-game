import re, json, sys
src = sys.argv[1]; out = sys.argv[2]
deck = json.load(open(f'{src}/project/deck.json', encoding='utf-8'))
ICONS = {
 'Home': '<path d="M3 11l9-8 9 8"/><path d="M5 10v10h14V10"/>',
 'Verified': '<circle cx="12" cy="12" r="9"/><path d="M8 12l3 3 5-6"/>',
 'ThumbsUp': '<path d="M7 11v9H4v-9z"/><path d="M7 11l4-7c1.5 0 2.5 1 2 3l-1 3h6a2 2 0 0 1 2 2l-2 7a2 2 0 0 1-2 1H7"/>',
 'Globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c3 3 3 15 0 18c-3-3-3-15 0-18z"/>',
 'Users': '<circle cx="9" cy="8" r="3.5"/><path d="M2 20c0-4 3-6 7-6s7 2 7 6"/><circle cx="17" cy="9" r="2.5"/><path d="M17 14c3 0 5 2 5 5"/>',
 'Star': '<path d="M12 3l2.8 5.8 6.2.9-4.5 4.4 1 6.2L12 17.3 6.5 20.3l1-6.2L3 9.7l6.2-.9z"/>',
}
H=[94,94,99,187,200,193,265,251,250,280,317,330]
V=['4,4','4,4','4,6','8,7','9,3','9,0','12,4','11,7','11,7','13,1','14,8','15,4']
cols=''.join(
 f'<div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;gap:6px">'
 f'<p style="font-family:\'Bricolage Grotesque\', Arial, sans-serif;font-size:26px;font-weight:800;line-height:30px">{v}</p>'
 f'<div style="width:100%;height:{h}px;background:{"#F25C3B" if i in (3,6,8) else "#2E7D55"};border-radius:10px 10px 0 0"></div></div>'
 for i,(h,v) in enumerate(zip(H,V)))
bars=f'<div style="height:376px;display:flex;flex-direction:row;align-items:flex-end;gap:12px">{cols}</div>'
pages=[]
for sid in deck['order']:
    if sid=='intro': continue
    s=open(f'{src}/project/slides/{sid}.html',encoding='utf-8').read()
    s=re.sub(r'<aside>.*?</aside>','',s,flags=re.S)
    s=re.sub(r'<x-embed.*?</x-embed>','',s,flags=re.S)
    s=re.sub(r'<x-shape kind="line" style="[^"]*"></x-shape>','<div style="height:0;border-top:2px solid #D9CFBF"></div>',s)
    def icon(m):
        return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
                f'stroke-linecap="round" stroke-linejoin="round" style="{m.group(2)};flex:none">{ICONS[m.group(1)]}</svg>')
    s=re.sub(r'<x-icon name="(\w+)" style="([^"]*)"></x-icon>',icon,s)
    s=s.replace('color:transparent;white-space:nowrap','color:#2E7D55;white-space:nowrap').replace('white-space:nowrap; color:#00000000','white-space:nowrap; color:#2E7D55')
    s=s.replace('<div style="height:376px"></div>',bars)
    s=re.sub(r'(<th style="[^"]*?);text-align:right',r'\1',s)
    s=re.sub(r'\sdata-(build-in|transition)="[^"]*"','',s)
    pages.append(s)
css='''*{margin:0;padding:0;box-sizing:border-box}
@page{size:1920px 1080px;margin:0}
html,body{margin:0;background:#FFF8EE;-webkit-print-color-adjust:exact;print-color-adjust:exact}
section{position:relative;width:1920px;height:1080px;overflow:hidden;break-after:page;page-break-after:always}
section:last-child{break-after:auto;page-break-after:auto}
div{display:flex;flex-direction:column}
p{line-height:1.4}h1{line-height:1.1;font-weight:600}h2{line-height:1.15;font-weight:600}h3{line-height:1.2;font-weight:600}
table{width:100%;border-collapse:separate;border-spacing:0;overflow:hidden}
th,td{padding:.35em .6em;text-align:left;border-top:1px solid rgba(128,128,128,.25);font-weight:400}
tr:first-child th{border-top:none;font-weight:700}
svg{display:block}'''
html=f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Sainplement – Finale Top Chef Kuisto</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400..800&family=DM+Sans:wght@400..700&display=swap">
<style>{css}</style></head><body>
{chr(10).join(pages)}
</body></html>'''
open(out,'w',encoding='utf-8').write(html)
print(len(pages),'pages')
