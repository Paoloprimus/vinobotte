(function(){
var SEZ=[['Valpolicella','/valpolicella/'],['Soave e Recioto di Soave','/soave/'],['Lessini Durello','/durello/'],['Bardolino','/bardolino/'],['Custoza','/custoza/'],['Prosecco DOC','/prosecco/'],['Colli Euganei','/euganei/'],['Venezia','/venezia/'],['Conegliano Valdobbiadene','/conegliano/'],['Asolo Montello','/asolo/'],['Delle Venezie','/venezie/']];
var css=`
:root[data-theme=light]{--bg:#faf8f4;--ink:#1d1b19;--line:#d9d3c8;--acc:#7a1f2b}
:root[data-theme=dark]{--bg:#171513;--ink:#f1ece4;--line:#3a352f;--acc:#e08a96}
body{padding-top:0!important;display:block!important}
.sh-head{max-width:none!important;margin:0!important;text-align:left!important;position:sticky;top:0;z-index:50;display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:8px;padding:8px 12px;background:var(--bg);border-bottom:1px solid var(--line);font:16px/1.3 Georgia,'Times New Roman',serif;color:var(--ink)}
.sh-head *{box-sizing:border-box}
.sh-tit{display:flex;flex-direction:column;align-items:center;color:var(--acc);text-decoration:none;text-align:center;line-height:1.15}
.sh-tit .t1{font-size:19px;font-weight:700}
.sh-tit .t2{font-size:12px;color:var(--ink)}
.sh-dx{display:flex;justify-content:flex-end;gap:6px}
.sh-b{display:inline-flex;align-items:center;justify-content:center;font:inherit;font-size:15px;color:var(--ink);background:none;border:1px solid var(--line);border-radius:4px;padding:7px;cursor:pointer}
.sh-b:hover,.sh-b:focus-visible{border-color:var(--acc);color:var(--acc)}
.sh-vel{position:fixed;inset:0;z-index:60;background:rgba(0,0,0,.4)}
.sh-pan{position:fixed;top:0;bottom:0;z-index:70;width:min(320px,86vw);background:var(--bg);color:var(--ink);padding:16px;overflow:auto;font:16px/1.4 Georgia,'Times New Roman',serif;transition:transform .2s}
.sh-pan.sx{left:0;border-right:1px solid var(--line);transform:translateX(-102%)}
.sh-pan.dx{right:0;border-left:1px solid var(--line);transform:translateX(102%)}
.sh-pan.on{transform:none}
.sh-pan h2{margin:0 0 12px;font-size:18px;font-variant:small-caps;letter-spacing:.12em;color:var(--acc);font-weight:400}
.sh-pan a{display:block;padding:9px 4px;color:var(--ink);text-decoration:none;border-bottom:1px solid var(--line)}
.sh-pan a:hover,.sh-pan a:focus-visible{color:var(--acc)}
.sh-pan .sub a{padding-left:16px;font-size:15px}
.sh-pan .x{float:right}
.sh-pan fieldset{border:0;padding:0;margin:0 0 16px}
.sh-pan legend{font-weight:700;margin-bottom:6px}
.sh-pan label{display:block;padding:4px 0}
.sh-foot{margin-top:40px;padding:18px 16px;border-top:1px solid var(--line);text-align:center;font:14px/1.6 Georgia,'Times New Roman',serif;color:var(--ink)}
.sh-foot a{color:var(--acc);text-decoration:none;margin:0 8px}
.sh-foot a:hover{text-decoration:underline}
@media (max-width:560px){.sh-tit .t1{font-size:17px}.sh-tit .t2{font-size:10.5px}}
`;
var st=document.createElement('style');st.textContent=css;document.head.appendChild(st);
function g(k){try{return localStorage.getItem(k)}catch(e){return null}}
function s(k,v){try{localStorage.setItem(k,v)}catch(e){}}
function applica(){
 var t=g('vb-tema')||'auto',z=g('vb-testo')||'normale',r=document.documentElement;
 if(t==='auto')r.removeAttribute('data-theme');else r.setAttribute('data-theme',t);
 document.body.style.zoom=z==='grande'?'1.15':'';
}
var head=document.createElement('header');head.className='sh-head';
head.innerHTML='<div><button class="sh-b" id="sh-m" aria-label="Menu" title="Menu" aria-expanded="false" aria-controls="sh-pm"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16"/></svg></button></div><a class="sh-tit" href="/"><span class="t1">VinoBotte</span><span class="t2">Guida produttori italiani vini DOC e DOCG</span></a><div class="sh-dx"><button class="sh-b" id="sh-i" aria-label="Impostazioni" title="Impostazioni" aria-expanded="false" aria-controls="sh-pi"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/></svg></button><button class="sh-b" id="sh-e" type="button" aria-label="Esci" title="Esci"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"/></svg></button></div>';
var vel=document.createElement('div');vel.className='sh-vel';vel.hidden=true;
var pm=document.createElement('nav');pm.id='sh-pm';pm.className='sh-pan sx';pm.setAttribute('aria-label','Menu');
pm.innerHTML='<button class="sh-b x" data-chiudi>✕</button><h2>Menu</h2><a href="/">Home</a><a href="/veneto/">Veneto</a><div class="sub">'+SEZ.map(function(x){return '<a href="'+x[1]+'">'+x[0]+'</a>'}).join('')+'</div>';
var pi=document.createElement('aside');pi.id='sh-pi';pi.className='sh-pan dx';pi.setAttribute('aria-label','Impostazioni');
pi.innerHTML='<button class="sh-b x" data-chiudi>✕</button><h2>Impostazioni</h2><fieldset><legend>Tema</legend><label><input type="radio" name="vb-tema" value="auto"> Automatico</label><label><input type="radio" name="vb-tema" value="light"> Chiaro</label><label><input type="radio" name="vb-tema" value="dark"> Scuro</label></fieldset><fieldset><legend>Dimensione del testo</legend><label><input type="radio" name="vb-testo" value="normale"> Normale</label><label><input type="radio" name="vb-testo" value="grande"> Grande</label></fieldset>';
var foot=document.createElement('footer');foot.className='sh-foot';
foot.innerHTML='<div><a href="/privacy/">Privacy</a><a href="/nota-metodologica/">Nota metodologica</a><a href="mailto:info@vinobot.it">Contatti</a></div><div>© 2026 VinoBot. Tutti i diritti riservati.</div>';
document.body.insertBefore(head,document.body.firstChild);
document.body.appendChild(vel);document.body.appendChild(pm);document.body.appendChild(pi);document.body.appendChild(foot);
function apri(p,b){chiudi();p.classList.add('on');vel.hidden=false;b.setAttribute('aria-expanded','true');}
function chiudi(){[pm,pi].forEach(function(p){p.classList.remove('on')});vel.hidden=true;document.getElementById('sh-m').setAttribute('aria-expanded','false');document.getElementById('sh-i').setAttribute('aria-expanded','false');}
function tog(p,id){var b=document.getElementById(id);p.classList.contains('on')?chiudi():apri(p,b);}
document.getElementById('sh-m').onclick=function(){tog(pm,'sh-m')};
document.getElementById('sh-i').onclick=function(){tog(pi,'sh-i')};
vel.onclick=chiudi;
document.addEventListener('keydown',function(e){if(e.key==='Escape')chiudi()});
[pm,pi].forEach(function(p){p.querySelector('[data-chiudi]').onclick=chiudi});
['vb-tema','vb-testo'].forEach(function(n){
 var v=g(n)||(n==='vb-tema'?'auto':'normale');
 pi.querySelectorAll('input[name='+n+']').forEach(function(i){i.checked=i.value===v;i.onchange=function(){s(n,i.value);applica()}});
});
applica();
})();
