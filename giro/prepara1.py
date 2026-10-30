import json,re,sys
from urllib.parse import urlparse
src=sys.argv[1]; d=json.load(open(src)); out={}
BADH=re.compile(r'(themes?|skechers|qode|mikado|aitthemes|wpopal|ozdesign|sitejet|wix|squarespace|godaddy|webnode|shopify|wordpress|elementor)',re.I)
BADFB=re.compile(r'(policy\.php|^about|privacy|video\.php|profile\.php|sharer|share\.php|dialog|plugins|^tr\b|login|help|^pages/category/?$)',re.I)
def clean_social(k,u):
    p=urlparse(u); path=p.path.strip('/')
    if not path or BADH.search(path): return None
    if k=='facebook':
        if BADFB.search(path): return None
        h=path.split('/')[0] if not path.startswith(('pages/','people/')) else path.split('/')[1]
        if path.startswith('pages/category'): h=path.split('/')[-1].rsplit('-',1)[0]
        return u.split('?')[0].split('#')[0].rstrip('/'),h
    if k=='instagram':
        h=path.split('/')[0]
        if h in('p','reel','explore','accounts','sharer') : return None
        return f'https://www.instagram.com/{h}/', '@'+h
    if k=='youtube':
        if path.startswith('embed') or path.startswith('watch'): return None
        return u.split('?')[0].rstrip('/'), path.replace('user/','').replace('channel/','canale ').split('/')[0]
    if k=='x':
        h=path.split('/')[0]
        if h in('privacy','articles','share','intent','home') or BADH.search(h): return None
        return f'https://x.com/{h}','@'+h
    if k=='linkedin':
        if not path.startswith('company/'): return None
        return u.split('?')[0].rstrip('/'), path.split('/')[1]
    return None
NAMES={'facebook':'Facebook','instagram':'Instagram','youtube':'YouTube','x':'X','linkedin':'LinkedIn'}
SHOPOK=re.compile(r'(/(shop|negozio|store|e-?shop|e-?commerce|wineshop|enoteca-online|shop-online)(/|$)|^shop\.|\.shop$|/store/)',re.I)
SHOPBAD=re.compile(r'(cookie|privacy|terms|condizion|termini|shopify\.com|wpml|localhost|footlocker|acconsento|cdn\.|lodgify|checkout|wpopal|add-to-cart|share=|/[a-z-]*/\d{4}/\d\d/)',re.I)
def pick_shop(urls):
    c=[u.split('?')[0].split('#')[0] for u in urls if not SHOPBAD.search(u)]
    c=[u for u in c if SHOPOK.search(urlparse(u).netloc.replace('www.','')+urlparse(u).path)]
    c=sorted(set(c),key=lambda u:(len(urlparse(u).path.strip('/').split('/')),len(u)))
    return c[0] if c else None
def pick_email(em,site):
    host=urlparse(site).netloc.replace('www.','').lower(); host=host.split('.')[-2]+'.'+host.split('.')[-1] if host.count('.')>=1 else host
    em=[e.strip().strip('.').lower() for e in em]; em=[e for e in em if '@' in e and not re.search(r'(sitejet|qode|themes|support@|wix|noreply|example|sentry|webmaster|pec|legalmail|tobu|@2x)',e)]
    own=[e for e in em if e.split('@')[1].endswith(host.split('.')[0]+'.'+host.split('.')[-1]) or host.split('.')[0] in e.split('@')[1]]
    for pool in (own,em if len(em)==1 else []):
        pri=[e for e in pool if re.match(r'(info|vendite|ordini|cantina|commerciale|ufficio|contatti|wine|azienda|sales|export)',e)]
        if pri: return pri[0]
        if pool: return pool[0]
    return None
GROUP={}
for x in d:
    for k,u in x.get('social',{}).items():
        r=clean_social(k,u)
        if r: GROUP.setdefault((k,r[0].lower()),[]).append(x['slug'])
EXCL={'poggio-al-lupo','pinino','fattoria-di-valiano','grattamacco','capraia','castelgiocondo-e-luce-della-vite','la-braccesca','le-mortelle','pian-delle-vigne'}
for x in d:
    if 'errore' in x or x['slug'] in EXCL: continue
    o={}
    soc=[]
    for k in('facebook','instagram','youtube','x','linkedin'):
        u=x.get('social',{}).get(k)
        r=clean_social(k,u) if u else None
        if r and len(GROUP.get((k,r[0].lower()),[]))>1: r=None   # profilo condiviso tra più cantine: non attribuibile
        if r: soc.append((NAMES[k],r[0],r[1]))
    if soc: o['social']=soc
    sh=pick_shop(x.get('shop',[]))
    if sh: o['shop']=sh
    em=pick_email(x.get('email',[]),x['url'])
    if em: o['email']=em
    tl=[re.sub(r'\s+',' ',t).strip() for t in x.get('tel',[]) if len(re.sub(r'\D','',t))>=8]
    if tl: o['tel']=tl[0]
    o['pagine']=x['pagine'][:1]
    out[x['slug']]=o
json.dump(out,open(src.replace('.json','_l1.json'),'w'),ensure_ascii=False,indent=0)
print(len(out),'schede;',sum(1 for o in out.values() if 'social' in o),'social;',sum(1 for o in out.values() if 'shop' in o),'shop;',sum(1 for o in out.values() if 'email' in o),'email;',sum(1 for o in out.values() if 'tel' in o),'tel')
for s,o in out.items():
    if 'social' in o or 'shop' in o: print(s,[f'{a}:{c}' for a,b,c in o.get('social',[])],o.get('shop',''))
