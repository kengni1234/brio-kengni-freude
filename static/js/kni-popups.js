/**
 * KniUI — Système de pop-ups professionnel
 * k-Ni Store · Kengni Finance
 * Version 3.0 — Toast · Confirm · Alert · Loading · Prompt
 */
(function(global){
'use strict';

/* ═══════════════════════════════════════════════════════════
   STYLES INJECTÉS (une seule fois)
═══════════════════════════════════════════════════════════ */
const CSS = `
/* ─ TOAST ─────────────────────────────────────────────────── */
#kni-toast-wrap{
  position:fixed;top:1.1rem;right:1.1rem;z-index:99999;
  display:flex;flex-direction:column;gap:.55rem;pointer-events:none;
  max-width:370px;
}
.kni-toast{
  display:flex;align-items:flex-start;gap:.75rem;
  padding:.85rem 1rem .85rem .9rem;
  background:#1e293b;color:#f1f5f9;
  border-radius:14px;
  box-shadow:0 8px 32px rgba(0,0,0,.35),0 2px 8px rgba(0,0,0,.2);
  border:1px solid rgba(255,255,255,.07);
  font-family:inherit;font-size:.85rem;font-weight:500;line-height:1.4;
  pointer-events:all;cursor:default;overflow:hidden;position:relative;
  animation:kni-slide-in .3s cubic-bezier(.34,1.56,.64,1) both;
  max-width:370px;min-width:240px;
}
.kni-toast.kni-out{animation:kni-slide-out .25s ease forwards}
.kni-toast-icon{
  width:32px;height:32px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-size:1rem;flex-shrink:0;margin-top:.05rem;
}
.kni-toast-body{flex:1;min-width:0}
.kni-toast-title{font-weight:700;font-size:.87rem;margin-bottom:.15rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.kni-toast-msg{font-size:.8rem;color:#94a3b8;line-height:1.4}
.kni-toast.no-msg .kni-toast-title{font-weight:600;font-size:.84rem;margin:0}
.kni-toast-close{
  background:none;border:none;color:#64748b;cursor:pointer;
  font-size:.95rem;padding:.15rem .2rem;border-radius:5px;
  line-height:1;margin-top:.05rem;flex-shrink:0;transition:.15s;
}
.kni-toast-close:hover{background:rgba(255,255,255,.08);color:#f1f5f9}
.kni-toast-action{
  display:block;margin-top:.45rem;
  font-size:.75rem;font-weight:700;letter-spacing:.03em;
  background:rgba(255,255,255,.08);border:none;
  color:#e2e8f0;border-radius:6px;padding:.3rem .65rem;
  cursor:pointer;transition:.15s;text-decoration:none;
}
.kni-toast-action:hover{background:rgba(255,255,255,.14)}
.kni-toast-bar{
  position:absolute;bottom:0;left:0;height:3px;
  border-radius:0 0 14px 14px;
  animation:kni-bar var(--kni-dur,3.5s) linear forwards;
  transform-origin:left;
}
/* Types */
.kni-toast.success .kni-toast-icon{background:rgba(16,185,129,.18);color:#10b981}
.kni-toast.success .kni-toast-bar{background:#10b981}
.kni-toast.error   .kni-toast-icon{background:rgba(239,68,68,.18);color:#f87171}
.kni-toast.error   .kni-toast-bar{background:#f87171}
.kni-toast.warning .kni-toast-icon{background:rgba(245,158,11,.18);color:#fbbf24}
.kni-toast.warning .kni-toast-bar{background:#fbbf24}
.kni-toast.info    .kni-toast-icon{background:rgba(99,102,241,.18);color:#818cf8}
.kni-toast.info    .kni-toast-bar{background:#818cf8}
.kni-toast.loading .kni-toast-icon{background:rgba(0,176,116,.18);color:#00b074}
.kni-toast.loading .kni-toast-bar{background:#00b074;animation:kni-loading-bar 1.8s ease-in-out infinite}
.kni-toast.shop    .kni-toast-icon{background:rgba(0,176,116,.18);color:#00b074}
.kni-toast.shop    .kni-toast-bar{background:#00b074}
/* ─ SPINNER dans loading ─ */
.kni-spin{
  width:20px;height:20px;border:2.5px solid rgba(0,176,116,.25);
  border-top-color:#00b074;border-radius:50%;
  animation:kni-spin .7s linear infinite;
}

/* ─ CONFIRM / ALERT / PROMPT ──────────────────────────────── */
.kni-overlay{
  position:fixed;inset:0;z-index:999998;
  background:rgba(0,0,0,.6);backdrop-filter:blur(4px);
  display:flex;align-items:center;justify-content:center;padding:1rem;
  animation:kni-fade-in .2s ease;
}
.kni-overlay.kni-out{animation:kni-fade-out .2s ease forwards}
.kni-dialog{
  background:#1e293b;border:1px solid rgba(255,255,255,.09);
  border-radius:20px;padding:2rem 2rem 1.5rem;
  max-width:420px;width:100%;
  box-shadow:0 24px 64px rgba(0,0,0,.5),0 4px 16px rgba(0,0,0,.3);
  animation:kni-pop .3s cubic-bezier(.34,1.56,.64,1) both;
  font-family:inherit;
}
.kni-overlay.kni-out .kni-dialog{animation:kni-pop-out .2s ease forwards}
.kni-dialog-ico{
  width:56px;height:56px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-size:1.6rem;margin:0 auto 1.1rem;
}
.kni-dialog-ico.confirm {background:rgba(99,102,241,.15);color:#818cf8}
.kni-dialog-ico.danger  {background:rgba(239,68,68,.15); color:#f87171}
.kni-dialog-ico.warning {background:rgba(245,158,11,.15);color:#fbbf24}
.kni-dialog-ico.info    {background:rgba(0,176,116,.15); color:#00b074}
.kni-dialog-ico.success {background:rgba(16,185,129,.15);color:#10b981}
.kni-dialog-title{
  font-size:1.1rem;font-weight:800;color:#f1f5f9;
  text-align:center;margin-bottom:.6rem;
}
.kni-dialog-msg{
  font-size:.87rem;color:#94a3b8;text-align:center;
  line-height:1.65;margin-bottom:1.5rem;
}
.kni-dialog-input{
  width:100%;background:rgba(255,255,255,.06);
  border:1.5px solid rgba(255,255,255,.1);
  color:#f1f5f9;border-radius:10px;
  padding:.65rem .9rem;font-size:.9rem;font-family:inherit;
  outline:none;transition:.2s;margin-bottom:1.2rem;box-sizing:border-box;
}
.kni-dialog-input:focus{border-color:#00b074;background:rgba(0,176,116,.05)}
.kni-dialog-btns{display:flex;gap:.65rem;flex-direction:row-reverse}
.kni-btn{
  flex:1;padding:.65rem 1rem;border-radius:10px;border:none;
  font-size:.87rem;font-weight:700;font-family:inherit;
  cursor:pointer;transition:.18s;letter-spacing:.01em;
}
.kni-btn-cancel{
  background:rgba(255,255,255,.06);color:#94a3b8;
  border:1px solid rgba(255,255,255,.1);
}
.kni-btn-cancel:hover{background:rgba(255,255,255,.1);color:#f1f5f9}
.kni-btn-confirm{background:#00b074;color:#fff}
.kni-btn-confirm:hover{background:#00c888;transform:translateY(-1px)}
.kni-btn-danger{background:linear-gradient(135deg,#ef4444,#dc2626);color:#fff}
.kni-btn-danger:hover{background:linear-gradient(135deg,#f87171,#ef4444);transform:translateY(-1px)}
.kni-btn-warning{background:linear-gradient(135deg,#f59e0b,#d97706);color:#fff}
.kni-btn-warning:hover{filter:brightness(1.1);transform:translateY(-1px)}

/* ─ LOADING OVERLAY ───────────────────────────────────────── */
.kni-loader{
  position:fixed;inset:0;z-index:999999;
  background:rgba(0,0,0,.65);backdrop-filter:blur(6px);
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1.2rem;
  animation:kni-fade-in .2s ease;
}
.kni-loader-ring{
  width:52px;height:52px;
  border:4px solid rgba(0,176,116,.2);
  border-top-color:#00b074;border-radius:50%;
  animation:kni-spin .8s linear infinite;
}
.kni-loader-label{
  color:#e2e8f0;font-size:.9rem;font-weight:600;font-family:inherit;
  background:rgba(30,41,59,.85);padding:.5rem 1.2rem;
  border-radius:20px;border:1px solid rgba(255,255,255,.08);
}

/* ─ NOTIFICATION BANNER ──────────────────────────────────── */
.kni-banner{
  position:fixed;top:0;left:0;right:0;z-index:99999;
  padding:.7rem 1.5rem;text-align:center;
  font-family:inherit;font-size:.85rem;font-weight:700;
  display:flex;align-items:center;justify-content:center;gap:.6rem;
  animation:kni-banner-in .35s cubic-bezier(.34,1.56,.64,1) both;
  cursor:default;
}
.kni-banner.out{animation:kni-banner-out .25s ease forwards}
.kni-banner.success{background:#00b074;color:#fff}
.kni-banner.error  {background:#ef4444;color:#fff}
.kni-banner.warning{background:#f59e0b;color:#1a1a1a}
.kni-banner.info   {background:#6366f1;color:#fff}

/* ─ KEYFRAMES ─────────────────────────────────────────────── */
@keyframes kni-slide-in{from{opacity:0;transform:translateX(60px) scale(.9)}to{opacity:1;transform:none}}
@keyframes kni-slide-out{to{opacity:0;transform:translateX(80px) scale(.85);max-height:0;margin:0;padding:0}}
@keyframes kni-fade-in{from{opacity:0}to{opacity:1}}
@keyframes kni-fade-out{to{opacity:0}}
@keyframes kni-pop{from{opacity:0;transform:scale(.8) translateY(20px)}to{opacity:1;transform:none}}
@keyframes kni-pop-out{to{opacity:0;transform:scale(.85) translateY(12px)}}
@keyframes kni-spin{to{transform:rotate(360deg)}}
@keyframes kni-bar{from{transform:scaleX(1)}to{transform:scaleX(0)}}
@keyframes kni-loading-bar{0%{transform:translateX(-100%)}100%{transform:translateX(200%)}}
@keyframes kni-banner-in{from{opacity:0;transform:translateY(-100%)}to{opacity:1;transform:none}}
@keyframes kni-banner-out{to{opacity:0;transform:translateY(-100%)}}

/* ─ MOBILE ─────────────────────────────────────────────────── */
@media(max-width:500px){
  #kni-toast-wrap{top:auto;bottom:1rem;right:.75rem;left:.75rem;max-width:100%}
  .kni-toast{animation:kni-slide-up .3s cubic-bezier(.34,1.56,.64,1) both}
  .kni-toast.kni-out{animation:kni-slide-down .25s ease forwards}
  .kni-dialog{border-radius:16px 16px 0 0;position:fixed;bottom:0;left:0;right:0;max-width:100%;margin:0}
  .kni-overlay{align-items:flex-end;padding:0}
}
@keyframes kni-slide-up{from{opacity:0;transform:translateY(60px)}to{opacity:1;transform:none}}
@keyframes kni-slide-down{to{opacity:0;transform:translateY(80px)}}
`;

/* Inject styles once */
function _injectStyles(){
  if(document.getElementById('kni-popup-styles')) return;
  const s = document.createElement('style');
  s.id = 'kni-popup-styles';
  s.textContent = CSS;
  document.head.appendChild(s);
}

/* ═══════════════════════════════════════════════════════════
   ICONS SVG (inline — no FA dependency for popups)
═══════════════════════════════════════════════════════════ */
const ICONS = {
  success: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>',
  error:   '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>',
  warning: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>',
  info:    '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>',
  shop:    '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path><line x1="3" y1="6" x2="21" y2="6"></line><path d="M16 10a4 4 0 0 1-8 0"></path></svg>',
  trash:   '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"></path></svg>',
  alert:   '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>',
  question:'<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>',
  check:   '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="9 11 12 14 22 4" transform="translate(-9,-1)"></polyline><path d="M8 12l3 3 5-5"></path></svg>',
  edit:    '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>',
};

/* ═══════════════════════════════════════════════════════════
   TOAST
═══════════════════════════════════════════════════════════ */
let _wrap = null;
function _getWrap(){
  if(!_wrap || !document.contains(_wrap)){
    _wrap = document.getElementById('kni-toast-wrap');
    if(!_wrap){
      _wrap = document.createElement('div');
      _wrap.id = 'kni-toast-wrap';
      document.body.appendChild(_wrap);
    }
  }
  return _wrap;
}

/**
 * KniToast.show(options)
 * options: { type, title, msg, duration, action, actionLabel, icon }
 * type: 'success'|'error'|'warning'|'info'|'loading'|'shop'
 * Returns: remove function
 */
function toast(opts){
  _injectStyles();
  if(typeof opts === 'string') opts = {msg: opts};
  const {
    type     = 'info',
    title    = '',
    msg      = '',
    duration = type==='loading' ? 0 : (type==='error' ? 5000 : 3800),
    action   = null,
    actionLabel = 'Voir',
    icon     = null,
    id       = null,
  } = opts;

  const wrap = _getWrap();

  // Remove existing toast with same id
  if(id){
    const prev = document.getElementById('kni-t-'+id);
    if(prev) _removeToast(prev, true);
  }

  const el = document.createElement('div');
  el.className = `kni-toast ${type}`;
  if(id) el.id = 'kni-t-'+id;
  if(!msg) el.classList.add('no-msg');
  if(duration > 0) el.style.setProperty('--kni-dur', duration+'ms');

  const iconHtml = type==='loading'
    ? `<div class="kni-toast-icon"><div class="kni-spin"></div></div>`
    : `<div class="kni-toast-icon">${icon||ICONS[type]||ICONS.info}</div>`;

  const titleHtml = title ? `<div class="kni-toast-title">${title}</div>` : '';
  const msgHtml   = msg   ? `<div class="kni-toast-msg">${msg}</div>` : '';
  const actHtml   = action ? `<button class="kni-toast-action" id="kni-ta">${actionLabel}</button>` : '';
  const barHtml   = duration > 0 ? `<div class="kni-toast-bar"></div>` : '';

  el.innerHTML = `
    ${iconHtml}
    <div class="kni-toast-body">
      ${titleHtml}
      ${msgHtml}
      ${actHtml}
    </div>
    <button class="kni-toast-close" aria-label="Fermer">✕</button>
    ${barHtml}`;

  el.querySelector('.kni-toast-close').onclick = () => _removeToast(el);
  if(action){ el.querySelector('#kni-ta').onclick = () => { action(); _removeToast(el); }; }

  wrap.appendChild(el);

  // Max 5 toasts
  const all = wrap.querySelectorAll('.kni-toast:not(.kni-out)');
  if(all.length > 5) _removeToast(all[0]);

  let timer = null;
  if(duration > 0) timer = setTimeout(() => _removeToast(el), duration);

  const remove = () => { if(timer) clearTimeout(timer); _removeToast(el); };
  return remove;
}

function _removeToast(el, instant){
  if(!el || el.classList.contains('kni-out')) return;
  if(instant){ el.remove(); return; }
  el.classList.add('kni-out');
  setTimeout(() => el.remove(), 280);
}

/* Shorthand helpers */
toast.success = (msg, title='', opts={}) => toast({type:'success', title, msg, ...opts});
toast.error   = (msg, title='', opts={}) => toast({type:'error',   title, msg, duration:5500, ...opts});
toast.warning = (msg, title='', opts={}) => toast({type:'warning', title, msg, ...opts});
toast.info    = (msg, title='', opts={}) => toast({type:'info',    title, msg, ...opts});
toast.shop    = (msg, title='', opts={}) => toast({type:'shop',    title, msg, ...opts});
toast.loading = (msg, title='Chargement…', id='load', opts={}) =>
  toast({type:'loading', title, msg, id, duration:0, ...opts});

/* ═══════════════════════════════════════════════════════════
   CONFIRM / ALERT / PROMPT
═══════════════════════════════════════════════════════════ */

function _dialog(opts){
  _injectStyles();
  return new Promise(resolve => {
    const {
      type        = 'confirm',  // 'confirm'|'alert'|'prompt'
      variant     = 'confirm',  // 'confirm'|'danger'|'warning'|'info'|'success'
      title       = 'Confirmer',
      msg         = '',
      confirmText = 'Confirmer',
      cancelText  = 'Annuler',
      placeholder = '',
      defaultVal  = '',
      icon        = null,
    } = opts;

    const ov = document.createElement('div');
    ov.className = 'kni-overlay';

    const icoMap = {confirm:'question', danger:'trash', warning:'alert', info:'info', success:'check'};
    const icoHtml = icon||ICONS[icoMap[variant]]||ICONS.question;

    const inputHtml = type==='prompt'
      ? `<input class="kni-dialog-input" id="kni-prompt-input" type="text" placeholder="${placeholder}" value="${defaultVal}">`
      : '';
    const cancelHtml = type!=='alert'
      ? `<button class="kni-btn kni-btn-cancel" id="kni-cancel">${cancelText}</button>`
      : '';
    const confirmClass = variant==='danger' ? 'kni-btn-danger'
                        : variant==='warning' ? 'kni-btn-warning'
                        : 'kni-btn-confirm';

    ov.innerHTML = `
      <div class="kni-dialog" role="dialog" aria-modal="true">
        <div class="kni-dialog-ico ${variant}">${icoHtml}</div>
        <div class="kni-dialog-title">${title}</div>
        ${msg ? `<div class="kni-dialog-msg">${msg}</div>` : ''}
        ${inputHtml}
        <div class="kni-dialog-btns">
          <button class="kni-btn ${confirmClass}" id="kni-confirm">${confirmText}</button>
          ${cancelHtml}
        </div>
      </div>`;

    document.body.appendChild(ov);

    // Focus
    setTimeout(() => {
      if(type==='prompt'){
        const inp = ov.querySelector('#kni-prompt-input');
        inp && inp.focus();
      } else {
        const btn = ov.querySelector('#kni-confirm');
        btn && btn.focus();
      }
    }, 50);

    function close(val){
      ov.classList.add('kni-out');
      setTimeout(() => { ov.remove(); resolve(val); }, 220);
    }

    ov.querySelector('#kni-confirm').onclick = () => {
      if(type==='prompt'){
        const val = ov.querySelector('#kni-prompt-input').value;
        close(val);
      } else {
        close(true);
      }
    };

    const cancelBtn = ov.querySelector('#kni-cancel');
    if(cancelBtn) cancelBtn.onclick = () => close(type==='prompt' ? null : false);

    // ESC key
    function onKey(e){
      if(e.key==='Escape'){ document.removeEventListener('keydown',onKey); close(false); }
      if(e.key==='Enter' && type!=='prompt'){ document.removeEventListener('keydown',onKey); close(true); }
    }
    document.addEventListener('keydown', onKey);

    // Click outside
    ov.onclick = e => { if(e.target===ov) close(false); };
  });
}

const confirm = (msg, opts={}) => _dialog({type:'confirm', variant:'confirm', title:'Confirmer', msg, ...opts});
const danger  = (msg, opts={}) => _dialog({type:'confirm', variant:'danger',  title:'Supprimer ?', msg, confirmText:'Supprimer', ...opts});
const warning = (msg, opts={}) => _dialog({type:'confirm', variant:'warning', title:'Attention',   msg, ...opts});
const alert   = (msg, opts={}) => _dialog({type:'alert',   variant:'info',    title:'Information', msg, cancelText:'', confirmText:'OK', ...opts});
const prompt  = (msg, opts={}) => _dialog({type:'prompt',  variant:'info',    title:'Saisir',      msg, confirmText:'Valider', ...opts});

/* ═══════════════════════════════════════════════════════════
   LOADING OVERLAY
═══════════════════════════════════════════════════════════ */
let _loader = null;

const loading = {
  show(label='Chargement…'){
    _injectStyles();
    if(_loader) return;
    _loader = document.createElement('div');
    _loader.className = 'kni-loader';
    _loader.innerHTML = `
      <div class="kni-loader-ring"></div>
      <div class="kni-loader-label" id="kni-loader-label">${label}</div>`;
    document.body.appendChild(_loader);
  },
  update(label){ const el = document.getElementById('kni-loader-label'); if(el) el.textContent=label; },
  hide(){
    if(!_loader) return;
    _loader.style.animation='kni-fade-out .2s ease forwards';
    setTimeout(() => { _loader&&_loader.remove(); _loader=null; }, 220);
  }
};

/* ═══════════════════════════════════════════════════════════
   BANNER (top bar)
═══════════════════════════════════════════════════════════ */
function banner(msg, type='success', duration=4000){
  _injectStyles();
  let b = document.getElementById('kni-banner');
  if(b){ b.classList.remove('out'); b.textContent=msg; b.className='kni-banner '+type; }
  else {
    b = document.createElement('div');
    b.id = 'kni-banner';
    b.className = 'kni-banner '+type;
    b.textContent = msg;
    document.body.appendChild(b);
  }
  if(duration > 0) setTimeout(() => {
    b.classList.add('out');
    setTimeout(() => b&&b.remove(), 260);
  }, duration);
}

/* ═══════════════════════════════════════════════════════════
   EXPORT
═══════════════════════════════════════════════════════════ */
const KniUI = { toast, confirm, danger, warning, alert, prompt, loading, banner, ICONS };

/* Global shortcuts */
global.KniUI    = KniUI;
global.kniToast = toast;  // alias court

/* Rétro-compatibilité : surcharge des toast() existants selon le contexte */
global._KniReady = true;

})(typeof window !== 'undefined' ? window : this);
