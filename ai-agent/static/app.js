// SVG icon helpers
const ICON_AGENT = '<div class="agent-eye-avatar" aria-hidden="true"><span class="agent-eye agent-eye--l"><span class="agent-eye-sclera"><span class="agent-eye-track"><span class="agent-eye-iris"><span class="agent-eye-pupil"></span></span></span></span></span><span class="agent-eye agent-eye--r"><span class="agent-eye-sclera"><span class="agent-eye-track"><span class="agent-eye-iris"><span class="agent-eye-pupil"></span></span></span></span></span></div>';

// #6 User avatar — color được generate từ session ID
const _USER_COLORS = ['#7c9fff','#a78bfa','#34d399','#f472b6','#fb923c','#60a5fa','#a3e635'];
const _sessionColor = _USER_COLORS[Math.floor(Math.random() * _USER_COLORS.length)];
const _userInitial = 'U'; // có thể customize sau
// Gradient background: sáng hơn ở góc trên-trái, đậm hơn ở góc dưới-phải
const ICON_USER = '<div class="user-avatar-initial" style="'
  + 'background:linear-gradient(145deg,' + _sessionColor + '28 0%,' + _sessionColor + '45 100%);'
  + 'border-color:' + _sessionColor + '88;'
  + 'color:' + _sessionColor + '">' + _userInitial + '</div>';
const ICON_TOOL  = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>`;
const ICON_CHEVRON_DOWN = `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="var(--soft)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>`;
const ICON_CHEVRON_RIGHT= `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="var(--soft)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>`;
const ICON_FILE  = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--soft)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><polyline points="13 2 13 9 20 9"/></svg>`;
const ICON_MIC   = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>`;
const ICON_MIC_OFF=`<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--red)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="1" y1="1" x2="23" y2="23"/><path d="M9 9v3a3 3 0 0 0 5.12 2.12M15 9.34V4a3 3 0 0 0-5.94-.6"/><path d="M17 16.95A7 7 0 0 1 5 12v-2m14 0v2a7 7 0 0 1-.11 1.23"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>`;
const ICON_TRASH = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/></svg>`;
const ICON_SUN   = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>`;
const ICON_MOON  = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`;

// ── Welcome screen HTML — dùng chung ở mọi nơi ──
const EYE_AVATAR_HTML = `<div class="agent-eye-avatar" aria-hidden="true"><span class="agent-eye agent-eye--l"><span class="agent-eye-sclera"><span class="agent-eye-track"><span class="agent-eye-iris"><span class="agent-eye-pupil"></span></span></span></span></span><span class="agent-eye agent-eye--r"><span class="agent-eye-sclera"><span class="agent-eye-track"><span class="agent-eye-iris"><span class="agent-eye-pupil"></span></span></span></span></span></div>`;

// #12 — Pool chips để shuffle mỗi lần load
const ALL_CHIPS = [
  {label:'Thời tiết Hà Nội', q:'Thời tiết Hà Nội hôm nay?', icon:'<path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9z"/>'},
  {label:'File trong Desktop', q:'Liệt kê file trong Desktop', icon:'<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>'},
  {label:'RAM & CPU', q:'RAM và CPU đang dùng bao nhiêu?', icon:'<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>'},
  {label:'Phân tích màn hình', q:'Chụp màn hình và mô tả đang làm gì', icon:'<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/>'},
  {label:'Mở Safari', q:'Mở Safari và vào google.com', icon:'<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>'},
  {label:'Tạo file', q:'Tạo file notes.txt trên Desktop', icon:'<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="12" y1="18" x2="12" y2="12"/><line x1="9" y1="15" x2="15" y2="15"/>'},
  {label:'Tìm kiếm web', q:'Tìm kiếm tin tức AI mới nhất hôm nay', icon:'<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>'},
  {label:'Kiểm tra disk', q:'Dung lượng ổ đĩa còn bao nhiêu?', icon:'<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>'},
  {label:'Viết code Python', q:'Viết hàm Python đọc file CSV và tính tổng cột số', icon:'<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>'},
  {label:'Đặt nhắc nhở', q:'Nhắc tôi uống nước sau 30 phút', icon:'<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>'},
];

function _shuffleChips(){
  const arr = [...ALL_CHIPS];
  for(let i = arr.length - 1; i > 0; i--){
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr.slice(0, 6);
}

/**
 * ID luồng chat — crypto.randomUUID() chỉ có trên secure context (https / localhost).
 * Truy cập http://192.168.x.x hoặc IP LAN: randomUUID không tồn tại → gây lỗi khi gửi.
 */
function randomStreamId(){
  if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function'){
    return crypto.randomUUID();
  }
  const buf = new Uint8Array(16);
  if (typeof crypto !== 'undefined' && crypto.getRandomValues){
    crypto.getRandomValues(buf);
  } else {
    for (let i = 0; i < 16; i++) buf[i] = (Math.random() * 256) | 0;
  }
  buf[6] = (buf[6] & 0x0f) | 0x40;
  buf[8] = (buf[8] & 0x3f) | 0x80;
  const h = [...buf].map(b => b.toString(16).padStart(2, '0')).join('');
  return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
}

// #10 Chip keyboard navigation
function _initChipKeyNav(){
  const chips = document.querySelectorAll('.chip');
  chips.forEach((chip, i) => {
    chip.setAttribute('tabindex', '0');
    chip.setAttribute('role', 'button');
    chip.addEventListener('keydown', e => {
      if(e.key === 'Enter' || e.key === ' '){
        e.preventDefault();
        chip.click();
      } else if(e.key === 'ArrowRight' || e.key === 'ArrowDown'){
        e.preventDefault();
        const next = chips[i + 1] || chips[0];
        next.focus();
      } else if(e.key === 'ArrowLeft' || e.key === 'ArrowUp'){
        e.preventDefault();
        const prev = chips[i - 1] || chips[chips.length - 1];
        prev.focus();
      }
    });
  });
}

function buildWelcomeHTML(){
  // #1 Capability pills
  const caps = ['Điều khiển macOS','Duyệt web','Đọc/ghi file','Phân tích ảnh','Tự động hóa'];
  const capHtml = caps.map((c,i)=>
    `<span class="cap-pill" style="animation-delay:${i*0.08}s">${c}</span>`
  ).join('');

  // #12 Shuffle chips mỗi lần
  const chips = _shuffleChips();
  const chipsHtml = chips.map((c,i)=>
    `<div class="chip" style="animation-delay:${i*0.05}s" data-oculo="suggest" data-oculo-prompt="${encodeURIComponent(c.q)}"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${c.icon}</svg>${c.label}</div>`
  ).join('');

  return `<div id="welcome">
    <div class="wicon" id="welcome-icon">${EYE_AVATAR_HTML}</div>
    <h2>Oculo</h2>
    <p class="welcome-slogan">Nhìn thấu · Hiểu sâu · Làm được mọi việc bạn cần.</p>
    <div class="cap-pills">${capHtml}</div>
    <div class="chips">${chipsHtml}</div>
  </div>`;
}

// Configure marked with highlight.js
marked.setOptions({
  breaks:true, gfm:true,
  highlight:(code,lang)=>{
    if(lang && hljs.getLanguage(lang)){
      try{return hljs.highlight(code,{language:lang}).value}catch(e){}
    }
    return hljs.highlightAuto(code).value;
  }
});

// Safe markdown renderer — tắt HTML thô để tránh XSS từ model output
const _markedRenderer = new marked.Renderer();
const _markedOriginalCode = _markedRenderer.code.bind(_markedRenderer);
marked.use({
  renderer: _markedRenderer,
  hooks: {
    postprocess(html) {
      // Xóa thẻ script và on* attributes bất kể nguồn gốc
      return html
        .replace(/<script[\s\S]*?<\/script>/gi, '')
        .replace(/\son\w+\s*=\s*["'][^"']*["']/gi, '')
        .replace(/\son\w+\s*=\s*[^\s>]*/gi, '');
    }
  }
});

function safeMarkdown(text){
  try{ return marked.parse(text||''); }
  catch{ return esc(text||''); }
}

// ── Theme (HLJS URLs must exist before first applyTheme — TDZ if called above const) ──
const HLJS_DARK = 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css';
const HLJS_LIGHT = 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-light.min.css';

const htmlEl = document.documentElement;
let theme = localStorage.getItem('theme')||'dark';

function applyTheme(t){
  theme=t;htmlEl.setAttribute('data-theme',t);
  const tm = document.getElementById('theme-menu-label');
  if(tm) tm.textContent = t==='dark' ? 'Giao diện sáng' : 'Giao diện tối';
  const hl = document.getElementById('hljs-theme-link');
  if(hl) hl.href = t === 'light' ? HLJS_LIGHT : HLJS_DARK;
  const metaTheme = document.querySelector('meta[name="theme-color"]');
  if(metaTheme) metaTheme.setAttribute('content', t === 'light' ? '#f5f5f5' : '#0a0a0a');
  localStorage.setItem('theme',t);
}

applyTheme(theme);
function toggleThemeUI(){
  // #12 Thêm class để trigger transition đồng đều
  document.body.classList.add('theme-switching');
  applyTheme(theme==='dark'?'light':'dark');
  setTimeout(()=>document.body.classList.remove('theme-switching'), 400);
}

// Expose for data-oculo handlers / future UI buttons
window.openDownloadsForUpdate = openDownloadsForUpdate;

// ── Config ──
let cfg = {
  model: localStorage.getItem('cfg_model')||'claude-sonnet-4.6',
  temperature: parseFloat(localStorage.getItem('cfg_temp')||'1.0'),
  system_prompt: localStorage.getItem('cfg_system')||''
};

function uxFollowupsEnabled(){
  return localStorage.getItem('ux_followup_suggestions') !== '0';
}
function uxRiskToolWarn(){
  return localStorage.getItem('ux_warn_risk_tools') === '1';
}
function uxOllamaEnabled(){
  // Ưu tiên trạng thái checkbox trong UI để dropdown phản ánh ngay.
  // (Tránh trường hợp localStorage bị dính giá trị cũ do cache/service worker.)
  const el = document.getElementById('cfg-enable-ollama');
  if(el) return !!el.checked;
  return localStorage.getItem('ux_enable_ollama') === '1';
}

/** Khớp server.py MODEL / MODELS_EXCLUDE — sau fetchClientConfig */
let _serverDefaultModel = 'claude-sonnet-4.6';
let _excludeModelIds = new Set();
let _appVersion = '';
let _downloadsUrl = '';
let _updateFeedUrl = '';

async function fetchClientConfig(){
  try{
    const r = await fetch('/client-config', { cache: 'no-store' });
    if(!r.ok) return;
    const j = await r.json();
    if(typeof j.default_model === 'string' && j.default_model.trim())
      _serverDefaultModel = j.default_model.trim();
    if(Array.isArray(j.exclude_model_ids))
      _excludeModelIds = new Set(j.exclude_model_ids.map(String));
    if(typeof j.app_version === 'string') _appVersion = j.app_version.trim();
    if(typeof j.downloads_url === 'string') _downloadsUrl = j.downloads_url.trim();
    if(typeof j.update_feed_url === 'string') _updateFeedUrl = j.update_feed_url.trim();
  }catch(e){}
}

async function _checkForUpdateOnce(){
  // Minimal auto-update: show a banner/toast that links to downloads.
  // Enabled only when downloads_url is provided by server config.
  try{
    if(!_downloadsUrl) return;
    // If update feed exists, use it. Otherwise just show downloads shortcut.
    if(_updateFeedUrl){
      const r = await fetch(_updateFeedUrl, { cache: 'no-store' });
      if(!r.ok) return;
      const j = await r.json();
      const latest = String(j.version || '').trim();
      if(!latest) return;
      if(_appVersion && latest === _appVersion) return;
      showToast(`Có bản mới ${latest}. Nhấn để cập nhật.`, 5200);
    } else {
      // no feed → still provide a quick “Downloads” action if user wants
      return;
    }
  }catch(e){}
}

async function openDownloadsForUpdate(){
  const url = _downloadsUrl || '';
  if(!url) return;
  try{
    await fetch('/update/open', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ url }),
    });
  }catch(e){}
}

function migrateModelIfExcluded(){
  if(!_excludeModelIds.size || !_excludeModelIds.has(cfg.model)) return;
  cfg.model = _serverDefaultModel;
  localStorage.setItem('cfg_model', cfg.model);
  if(typeof showToast === 'function')
    showToast('Đã chuyển sang model mặc định (model trước không khả dụng với API key).', 3800);
}

/** Danh sách từ GET /models (object: id, display_name, provider_label, …) */
let _modelsCatalog = [];

/** Gợi ý nhãn prefix/model (khớp utils/model_display.py) */
const _PREFIX_LABELS = {
  csg:'chiasegpu', csgm:'chiasegpu · Gemini', anthropic:'Anthropic', openai:'OpenAI', openrouter:'OpenRouter',
  pplx:'Perplexity', perplexity:'Perplexity', groq:'Groq', xai:'xAI (Grok)', grok:'xAI (Grok)',
  gemini:'Google Gemini', google:'Google Gemini', vertex:'Google Vertex',
  glm:'GLM (Zhipu)', 'glm-cn':'GLM (China)', deepseek:'DeepSeek', mistral:'Mistral', cohere:'Cohere',
  nvidia:'NVIDIA NIM', together:'Together AI', fireworks:'Fireworks', nebius:'Nebius',
  siliconflow:'SiliconFlow', minimax:'MiniMax', kimi:'Kimi', ollama:'Ollama'
};
function _labelForModelPrefix(prefix){
  const p = String(prefix||'').toLowerCase();
  return _PREFIX_LABELS[p] || _PREFIX_LABELS[p.split('-')[0]] || prefix;
}

/** Gợi ý nhãn khi API chưa tải hoặc model nhập tay */
function deriveModelDisplay(modelId){
  const id = String(modelId||'').trim();
  if(!id) return {id:'', display_name:'—', provider_label:'—', route_hint:'', router_prefix:''};
  const slash = id.indexOf('/');
  if(slash>0){
    const prefix = id.slice(0, slash);
    const rest = id.slice(slash+1);
    const upstream = _labelForModelPrefix(prefix);
    return {
      id,
      display_name: rest,
      provider_label: 'Anthropic API · '+upstream,
      route_hint: 'Messages API · '+prefix,
      router_prefix: prefix,
    };
  }
  return {id, display_name: id, provider_label: 'Anthropic API', route_hint: '', router_prefix: ''};
}

function normalizeModelEntry(entry){
  const id = typeof entry === 'string' ? entry : entry.id;
  const base = deriveModelDisplay(id);
  if(typeof entry === 'string') return { id, ...base };
  return {
    id,
    display_name: entry.display_name ?? base.display_name,
    provider_label: entry.provider_label ?? base.provider_label,
    route_hint: entry.route_hint ?? base.route_hint,
    router_prefix: entry.router_prefix ?? base.router_prefix,
  };
}

function isOllamaModelEntry(entry){
  const meta = normalizeModelEntry(entry || { id: '' });
  const id = String(meta.id || '').toLowerCase();
  const prefix = String(meta.router_prefix || '').toLowerCase();
  const provider = String(meta.provider_label || '').toLowerCase();
  if(prefix === 'ollama') return true;
  if(id === 'ollama' || id.startsWith('ollama/') || id.startsWith('ollama:')) return true;
  return provider.includes('ollama');
}

function isOllamaModelId(modelId){
  const id = String(modelId || '').trim();
  const entry = _modelsCatalog.find(m => m.id === id);
  return isOllamaModelEntry(entry || { id });
}

function firstNonOllamaModelId(){
  const list = _modelsCatalog.length
    ? _modelsCatalog.map(e => normalizeModelEntry(e))
    : [normalizeModelEntry({ id: _serverDefaultModel })];
  const fallback = list.find(m => !isOllamaModelEntry(m));
  return (fallback && fallback.id) ? fallback.id : _serverDefaultModel;
}

function enforceOllamaPolicy(opts){
  if(uxOllamaEnabled()) return false;
  if(!isOllamaModelId(cfg.model)) return false;
  const nextModel = firstNonOllamaModelId();
  if(!nextModel || nextModel === cfg.model) return false;
  cfg.model = nextModel;
  localStorage.setItem('cfg_model', cfg.model);
  if(opts?.notify){
    showToast('Đang tắt Ollama nên đã tự chuyển sang model khác.', 3200);
  }
  return true;
}

async function ensureOllamaReadyForUi(opts){
  const silent = !!opts?.silent;
  try{
    const r = await fetch('/ollama/enable', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: '{}'
    });
    const d = await r.json().catch(()=>({}));
    if(r.ok && d?.ok){
      if(!silent) showToast('Ollama đã sẵn sàng.', 2200);
      // Refresh models ngay để UI thấy toàn bộ model local.
      await loadModelCatalog();
      syncCfgModelSelectIfOpen();
      updateHeaderModelDisplay();
      // Nếu panel picker đang mở, rerender để hiện nhóm Ollama.
      if(_modelPickerOpen){
        const search = document.getElementById('model-picker-search');
        renderModelPicker(search?.value || '');
      }
      return { ok: true, data: d };
    }
    const msg = d?.message || d?.error || `HTTP ${r.status}`;
    if(!silent) showToast(`Không bật được Ollama: ${msg}`, 4200);
    return { ok: false, message: msg, data: d };
  }catch(e){
    const msg = e?.message || 'Không kết nối được tới server.';
    if(!silent) showToast(`Không bật được Ollama: ${msg}`, 4200);
    return { ok: false, message: msg };
  }
}

function getUiModelsList(){
  enforceOllamaPolicy();
  let list = _modelsCatalog.length
    ? _modelsCatalog.map(e => normalizeModelEntry(e))
    : [normalizeModelEntry({ id: cfg.model })];
  if(!uxOllamaEnabled()){
    list = list.filter(m => !isOllamaModelEntry(m));
  }
  const ids = new Set(list.map(m => m.id));
  if(!ids.has(cfg.model) && (uxOllamaEnabled() || !isOllamaModelId(cfg.model))){
    list.push(normalizeModelEntry({ id: cfg.model }));
  }
  if(!list.length){
    list = [normalizeModelEntry({ id: firstNonOllamaModelId() })];
  }
  return list;
}

function fillCfgModelSelect(sel){
  if(!sel) return;
  sel.innerHTML = '';
  const models = getUiModelsList();
  const seen = new Set();
  models.forEach(entry => {
    const id = entry.id;
    if(seen.has(id)) return;
    seen.add(id);
    const meta = normalizeModelEntry(entry);
    const inRemote = _modelsCatalog.some(m => m.id === id);
    const o = document.createElement('option');
    o.value = id;
    o.textContent = inRemote
      ? `${meta.display_name} — ${meta.provider_label}`
      : `${meta.display_name} — ${meta.provider_label} (đã lưu cục bộ)`;
    o.title = meta.route_hint || id;
    o.dataset.providerLabel = meta.provider_label || '';
    o.dataset.routeHint = meta.route_hint || '';
    if(id === cfg.model) o.selected = true;
    sel.appendChild(o);
  });
}

function syncCfgModelSelectIfOpen(){
  const modal = document.getElementById('settings-modal');
  const sel = document.getElementById('cfg-model');
  if(!modal?.classList.contains('open') || !sel) return;
  fillCfgModelSelect(sel);
  sel.value = cfg.model;
  updateCfgModelDetail();
}

let _modelPickerOpen = false;

function groupModelsForPicker(list, filterQ){
  const q = (filterQ || '').trim().toLowerCase();
  function matches(m){
    if(!q) return true;
    return (
      m.id.toLowerCase().includes(q) ||
      (m.display_name || '').toLowerCase().includes(q) ||
      (m.provider_label || '').toLowerCase().includes(q) ||
      (m.router_prefix || '').toLowerCase().includes(q)
    );
  }
  const filtered = list.filter(matches);
  const groups = new Map();
  for(const m of filtered){
    const pref = m.router_prefix || (m.id.includes('/') ? m.id.split('/')[0] : '');
    const key = pref || '__none';
    const short = pref ? (_labelForModelPrefix(pref) || pref) : 'Khác';
    const label = pref ? `${short} · ${pref}` : short;
    if(!groups.has(key)) groups.set(key, { key, label, items: [] });
    groups.get(key).items.push(m);
  }
  const arr = [...groups.values()];
  arr.forEach(g => g.items.sort((a, b) => String(a.display_name || a.id).localeCompare(String(b.display_name || b.id), 'vi')));
  arr.sort((a, b) => a.label.localeCompare(b.label, 'vi'));
  return arr;
}

function renderModelPicker(filterQ){
  const root = document.getElementById('model-picker-groups');
  if(!root) return;
  const list = getUiModelsList();
  const groups = groupModelsForPicker(list, filterQ);
  if(!groups.length || groups.every(g => !g.items.length)){
    root.innerHTML = '<div class="model-picker-empty">Không có model khớp bộ lọc.</div>';
    return;
  }
  root.innerHTML = '';

  // #8 Recently used section (chỉ hiện khi không filter)
  if(!filterQ){
    const recent = _getRecentModels().filter(id => id !== cfg.model);
    if(recent.length){
      const sec = document.createElement('div');
      sec.className = 'model-picker-group';
      const h = document.createElement('div');
      h.className = 'model-picker-group-title';
      h.innerHTML = '⏱ Dùng gần đây';
      sec.appendChild(h);
      recent.forEach(id => {
        const ent = list.find(m => m.id === id);
        if(!ent) return;
        const btn = _makeModelPickerRow(ent);
        sec.appendChild(btn);
      });
      root.appendChild(sec);
      const sep = document.createElement('div');
      sep.style.cssText = 'height:1px;background:var(--border);margin:4px 10px';
      root.appendChild(sep);
    }
  }

  for(const g of groups){
    if(!g.items.length) continue;
    const section = document.createElement('div');
    section.className = 'model-picker-group';
    const h = document.createElement('div');
    h.className = 'model-picker-group-title';
    h.textContent = g.label;
    section.appendChild(h);
    for(const m of g.items){
      section.appendChild(_makeModelPickerRow(m));
    }
    root.appendChild(section);
  }
}

function _makeModelPickerRow(m){
  const btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'model-picker-row' + (m.id === cfg.model ? ' is-active' : '');
  btn.setAttribute('role', 'option');
  btn.setAttribute('aria-selected', m.id === cfg.model ? 'true' : 'false');
  btn.onclick = () => applyModelSelection(m.id);
  const name = document.createElement('div');
  name.className = 'model-picker-row-name';
  name.textContent = m.display_name || m.id;
  const sub = document.createElement('div');
  sub.className = 'model-picker-row-sub';
  sub.textContent = [m.provider_label, m.id].filter(Boolean).join(' · ');
  btn.appendChild(name);
  btn.appendChild(sub);
  return btn;
}

function filterModelPicker(value){
  renderModelPicker(value);
}

function _modelPickerOutside(ev){
  const wrap = document.getElementById('model-switcher-wrap');
  if(wrap && !wrap.contains(ev.target)) closeModelPicker();
}

async function toggleModelPicker(ev){
  if(ev) ev.stopPropagation();
  if(_modelPickerOpen){ closeModelPicker(); return; }
  await openModelPicker();
}

async function openModelPicker(){
  // #15 Hiện skeleton trước khi load
  const loading = document.getElementById('model-picker-loading');
  if(loading) loading.style.display = 'block';

  await loadModelCatalog();

  // #15 Ẩn skeleton sau khi load xong
  if(loading) loading.style.display = 'none';

  const panel = document.getElementById('model-picker-panel');
  const btn = document.getElementById('model-switcher-btn');
  const search = document.getElementById('model-picker-search');
  if(!panel || !btn) return;
  panel.hidden = false;
  btn.setAttribute('aria-expanded', 'true');
  _modelPickerOpen = true;
  if(search) search.value = '';
  renderModelPicker('');
  setTimeout(() => {
    search?.focus();
    // #6 Fix position nếu panel bị cắt ở cạnh phải
    _fixModelPickerPosition(panel, btn);
  }, 30);
  document.addEventListener('click', _modelPickerOutside, true);
  // #10 Keyboard navigation
  panel.addEventListener('keydown', _modelPickerKeyNav);
}

// #6 Điều chỉnh vị trí panel nếu bị cắt
function _fixModelPickerPosition(panel, btn){
  const btnRect = btn.getBoundingClientRect();
  const panelW = panel.offsetWidth || 320;
  // Nếu căn phải bị cắt bên trái → căn trái
  if(btnRect.right - panelW < 8){
    panel.style.right = 'auto';
    panel.style.left = '0';
  } else {
    panel.style.right = '0';
    panel.style.left = 'auto';
  }
}

// #10 Arrow key navigation trong model picker
function _modelPickerKeyNav(e){
  const rows = [...document.querySelectorAll('.model-picker-row')];
  if(!rows.length) return;
  const cur = document.activeElement;
  const idx = rows.indexOf(cur);
  if(e.key === 'ArrowDown'){
    e.preventDefault();
    const next = rows[idx + 1] || rows[0];
    next.focus();
  } else if(e.key === 'ArrowUp'){
    e.preventDefault();
    const prev = rows[idx - 1] || rows[rows.length - 1];
    prev.focus();
  } else if(e.key === 'Enter' && idx >= 0){
    e.preventDefault();
    rows[idx].click();
  } else if(e.key === 'Escape'){
    closeModelPicker();
    document.getElementById('model-switcher-btn')?.focus();
  }
}

function closeModelPicker(){
  if(!_modelPickerOpen) return false;
  const panel = document.getElementById('model-picker-panel');
  const btn = document.getElementById('model-switcher-btn');
  if(panel){ panel.hidden = true; panel.removeEventListener('keydown', _modelPickerKeyNav); }
  if(btn) btn.setAttribute('aria-expanded', 'false');
  _modelPickerOpen = false;
  document.removeEventListener('click', _modelPickerOutside, true);
  return true;
}

function applyModelSelection(modelId){
  const id = String(modelId || '').trim();
  if(!id) return;
  if(!uxOllamaEnabled() && isOllamaModelId(id)){
    showToast('Bạn đang tắt Ollama. Bật lại trong Cấu hình để dùng model này.', 3200);
    return;
  }
  const changed = id !== cfg.model;
  cfg.model = id;
  localStorage.setItem('cfg_model', cfg.model);
  // #8 Lưu recently used models
  _saveRecentModel(id);
  updateHeaderModelDisplay();
  syncCfgModelSelectIfOpen();
  closeModelPicker();
  if(changed) showToast('Đã chuyển model');
}

// #8 Recently used models — lưu tối đa 3
const _RECENT_MODELS_KEY = 'oculo_recent_models';
function _saveRecentModel(id){
  try{
    let recent = JSON.parse(localStorage.getItem(_RECENT_MODELS_KEY) || '[]');
    recent = [id, ...recent.filter(m => m !== id)].slice(0, 3);
    localStorage.setItem(_RECENT_MODELS_KEY, JSON.stringify(recent));
  }catch(e){}
}
function _getRecentModels(){
  try{ return JSON.parse(localStorage.getItem(_RECENT_MODELS_KEY) || '[]'); }
  catch(e){ return []; }
}

async function loadModelCatalog(){
  try{
    const _mRes = await fetch('/models', { cache: 'no-store' });
    if(!_mRes.ok){ _modelsCatalog = []; enforceOllamaPolicy(); return; }
    const raw = await _mRes.json();
    if(Array.isArray(raw) && raw.length && typeof raw[0]==='object')
      _modelsCatalog = raw;
    else if(Array.isArray(raw))
      _modelsCatalog = raw.map(mid=>({id: mid, ...deriveModelDisplay(mid)}));
    else
      _modelsCatalog = [];
  }catch{
    _modelsCatalog = [];
  }
  enforceOllamaPolicy();
}

function updateHeaderModelDisplay(){
  const nEl = document.getElementById('header-model-name');
  const pEl = document.getElementById('header-provider-name');
  const btn = document.getElementById('model-switcher-btn');
  if(!nEl || !pEl) return;
  const id = cfg.model;
  const ent = _modelsCatalog.find(m=>m.id===id);
  const meta = ent ? normalizeModelEntry(ent) : deriveModelDisplay(id);
  nEl.textContent = meta.display_name || id;
  pEl.textContent = meta.provider_label || '—';
  if(btn) btn.title = [meta.route_hint || '', meta.id || id, 'Chọn model · ⌥M'].filter(Boolean).join(' — ');
  // Dynamic hsub
  const hsub = document.getElementById('hsub-line');
  if(hsub){
    const modelShort = (meta.display_name || id).split('/').pop().split('-').slice(0,3).join('-');
    hsub.textContent = 'macOS · ' + modelShort;
  }
  // Cập nhật badge tier color theo model đang chọn
  const badge = document.getElementById('model-badge');
  if(badge){
    const m = id.toLowerCase();
    badge.classList.remove('badge-haiku','badge-sonnet','badge-opus','badge-gemini','badge-other','badge-streaming');
    if(m.includes('haiku'))       badge.classList.add('badge-haiku');
    else if(m.includes('sonnet')) badge.classList.add('badge-sonnet');
    else if(m.includes('opus'))   badge.classList.add('badge-opus');
    else if(m.includes('gemini') || m.includes('flash')) badge.classList.add('badge-gemini');
    else                          badge.classList.add('badge-other');
    const shortId = (meta.display_name || id).split('/').pop();
    badge.textContent = shortId.length > 14 ? shortId.slice(0,12)+'…' : shortId;
    badge.classList.remove('is-hidden');
    badge.title = `Model: ${id}`;
  }
}

function updateHeaderModelFromSSE(d){
  const nEl = document.getElementById('header-model-name');
  const pEl = document.getElementById('header-provider-name');
  const btn = document.getElementById('model-switcher-btn');
  if(nEl && d.display_name) nEl.textContent = d.display_name;
  if(pEl && d.provider_label) pEl.textContent = d.provider_label;
  if(btn) btn.title = [d.route_hint, d.model, d.reason].filter(Boolean).join(' · ');
}

function updateCfgModelDetail(){
  const sel = document.getElementById('cfg-model');
  const det = document.getElementById('cfg-model-detail');
  if(!det || !sel) return;
  const opt = sel.selectedOptions[0];
  if(!opt || !opt.value){
    det.hidden = true;
    return;
  }
  const prov = opt.dataset.providerLabel || '';
  const route = opt.dataset.routeHint || '';
  const vid = opt.value;
  det.style.whiteSpace = 'pre-wrap';
  det.textContent = [prov && ('Nhà cung cấp: '+prov), route && ('Đường đi: '+route), 'Model ID: '+vid].filter(Boolean).join('\n');
  det.hidden = false;
}

// ── DOM ──
const msgsEl   = document.getElementById('messages');
const inputEl  = document.getElementById('user-input');
const sendBtn  = document.getElementById('send-btn');
const abortBtn = document.getElementById('abort-btn');
const sdot     = document.getElementById('sdot');
const stext    = document.getElementById('stext');
const scrollBtn= document.getElementById('scroll-btn');
const filePrev = document.getElementById('file-preview');
const fileInput= document.getElementById('file-input');

// ── State ──
let history=[], busy=false, curBubble=null, curText='', rendered=[];
let pendingFiles=[];   // {name, type, data(base64), previewUrl}
let currentStreamId=null;
let currentViewMode = localStorage.getItem('ui_view_mode') || 'chat';
let streamRenderTimer = null;
let shouldStickToBottom = true;
let saveHistoryTimer = null;
let saveRenderedTimer = null;
let lastScreenshotTs = 0;
/** Undo toast gọi fetch.abort() — không hiển thị thanh "Đã dừng" trùng */
let _sendAbortedByUndoToast = false;

// ── Persist ──
const SK='ai_agent_history', RK='ai_agent_rendered';
const CONV_KEY='ai_agent_conversations';

function _lsSet(key, value){
  try{ localStorage.setItem(key, value); }
  catch(e){
    if(e && (e.name==='QuotaExceededError'||e.name==='NS_ERROR_DOM_QUOTA_REACHED')){
      showToast('Bộ nhớ trình duyệt đầy. Một số dữ liệu không được lưu.', 4000);
    }
  }
}

function saveHistory(){ _lsSet(SK, JSON.stringify(history)); }
function saveRendered(){ _lsSet(RK, JSON.stringify(rendered)); }
function saveHistoryDebounced(){
  clearTimeout(saveHistoryTimer);
  saveHistoryTimer = setTimeout(()=>{ saveHistory(); saveCurrentConv(); }, 600);
}
function saveRenderedDebounced(){
  clearTimeout(saveRenderedTimer);
  saveRenderedTimer = setTimeout(saveRendered, 600);
}

const LAZY_LOAD_SIZE = 20;
let _renderedStart = 0;

function loadHistory(){
  try{
    const h=JSON.parse(localStorage.getItem(SK)||'[]');
    const r=JSON.parse(localStorage.getItem(RK)||'[]');
    if(!h.length)return;
    removeWelcome(); history=h;
    rendered=stripEmptyAgentFromRendered(r);
    if(rendered.length!==r.length) saveRendered();

    // Chỉ render LAZY_LOAD_SIZE tin nhắn cuối
    const startIdx = Math.max(0, rendered.length - LAZY_LOAD_SIZE);
    _renderedStart = startIdx;

    if(startIdx > 0) {
      const w = document.createElement('div'); w.className='mwrap'; w.id='load-more-wrap';
      w.innerHTML=`<div style="text-align:center;padding:10px"><button type="button" data-oculo="loadMoreHistory" style="background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:6px 14px;font-size:12px;color:var(--soft);cursor:pointer">Tải ${startIdx} tin nhắn cũ hơn</button></div>`;
      msgsEl.appendChild(w);
    }

    rendered.slice(startIdx).forEach(item=>{
      if(item.role==='user') renderUser(item.text, item.ts, false, item.images);
      else if(item.role==='agent') renderAgent(item.text,item.ts,false);
    });
    removeEmptyAgentMessageWraps();
    scrollEnd(false);
  }catch(e){}
}

function loadMoreHistory(){
  try{
    const r=JSON.parse(localStorage.getItem(RK)||'[]');
    const loadCount = Math.min(LAZY_LOAD_SIZE, _renderedStart);
    const newStart = _renderedStart - loadCount;
    const toLoad = r.slice(newStart, _renderedStart);

    document.getElementById('load-more-wrap')?.remove();

    const firstMsg = msgsEl.firstChild;
    toLoad.slice().reverse().forEach(item=>{
      if(item.role==='agent' && !String(item.text||'').trim()) return;
      const w = document.createElement('div'); w.className='mwrap';
      if(item.role==='user') w.innerHTML=`<div class="mrow user"><div class="av user">${ICON_USER}</div><div class="bubble user-bubble-rich">${buildUserBubbleContent(item.text, item.images)}</div></div><div class="ts mrow user">${item.ts}</div>`;
      else w.innerHTML=`<div class="mrow agent"><div class="av agent">${ICON_AGENT}</div><div class="bubble">${safeMarkdown(item.text)}</div></div><div class="ts mrow agent">${item.ts}</div>`;
      msgsEl.insertBefore(w, firstMsg);
    });

    _renderedStart = newStart;
    if(newStart > 0) {
      const w = document.createElement('div'); w.className='mwrap'; w.id='load-more-wrap';
      w.innerHTML=`<div style="text-align:center;padding:10px"><button type="button" data-oculo="loadMoreHistory" style="background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:6px 14px;font-size:12px;color:var(--soft);cursor:pointer">Tải ${newStart} tin nhắn cũ hơn</button></div>`;
      msgsEl.insertBefore(w, msgsEl.firstChild);
    }
  }catch(e){}
}

// ── Clear ──
function executeClearChatHistory(){
  if(_activeConvId){
    _conversations = _conversations.filter(c=>c.id!==_activeConvId);
    saveConversations();
    _activeConvId = null;
  }
  history=[];rendered=[];
  localStorage.removeItem(SK);localStorage.removeItem(RK);localStorage.removeItem('chat_draft');
  msgsEl.innerHTML='';
  const w=document.createElement('div');w.className='mwrap';
  w.innerHTML=buildWelcomeHTML();
  msgsEl.appendChild(w);
  renderConvList();
}
const clearBtnEl = document.getElementById('clear-btn');
if(clearBtnEl) clearBtnEl.addEventListener('click', ()=>{
  toggleMoreMenu();
  openConfirmModal({
    title: 'Xóa toàn bộ lịch sử chat?',
    message: 'Cuộc trò chuyện hiện tại sẽ bị xóa khỏi thiết bị này.',
    okText: 'Xóa',
    danger: true,
    onConfirm: executeClearChatHistory
  });
});


// ── Scroll + new-msg badge ──
let newMsgCount = 0;
const newMsgBadge = document.getElementById('new-msg-badge');

msgsEl.addEventListener('scroll',()=>{
  const atBottom=msgsEl.scrollHeight-msgsEl.scrollTop-msgsEl.clientHeight<80;
  shouldStickToBottom = atBottom;
  scrollBtn.classList.toggle('visible',!atBottom);
  if(atBottom){ newMsgCount=0; if(newMsgBadge){ newMsgBadge.textContent=''; newMsgBadge.classList.remove('visible'); } }
});
function scrollEnd(smooth=true,force=false){
  if(!force && !shouldStickToBottom) return;
  newMsgCount=0; if(newMsgBadge){ newMsgBadge.textContent=''; newMsgBadge.classList.remove('visible'); }
  msgsEl.scrollTo({top:msgsEl.scrollHeight,behavior:smooth?'smooth':'instant'});
}
function scrollToChatBottom(){
  scrollEnd(true,true);
}
function openFilePicker(){
  document.getElementById('file-input')?.click();
}
function notifyNewMsg(){
  if(shouldStickToBottom) return;
  newMsgCount++;
  newMsgBadge.textContent = newMsgCount + ' tin mới';
  newMsgBadge.classList.add('visible');
  scrollBtn.classList.add('visible');
}

// ── Input resize ──
let _suppressDraft = false;
inputEl.addEventListener('input',()=>{
  inputEl.style.height='auto';
  inputEl.style.height=Math.min(inputEl.scrollHeight,140)+'px';
  if(!_suppressDraft){
    if(inputEl.value.trim()){
      localStorage.setItem('chat_draft', inputEl.value);
    } else {
      localStorage.removeItem('chat_draft');
    }
  }
  // @ mention detection
  const val = inputEl.value;
  const pos = inputEl.selectionStart;
  const atIdx = val.lastIndexOf('@', pos - 1);
  if(atIdx >= 0 && (atIdx === 0 || /\s/.test(val[atIdx - 1]))){
    const query = val.slice(atIdx + 1, pos);
    if(!/\s/.test(query)) _updateAtMentionPicker(query);
    else _closeAtMentionPicker();
  } else {
    _closeAtMentionPicker();
  }
  // #2 Character count
  _updateCharCount();
  // #3 Send button glow khi có content
  const hasContent = inputEl.value.trim().length > 0;
  sendBtn.classList.toggle('has-content', hasContent);
});
// #2 Character count — hiện khi > 200 ký tự
function _updateCharCount(){
  const len = inputEl.value.length;
  let el = document.getElementById('char-count');
  if(!el){
    el = document.createElement('span');
    el.id = 'char-count';
    el.className = 'char-count';
    document.getElementById('iwrap')?.appendChild(el);
  }
  if(len > 200){
    el.textContent = len.toLocaleString();
    el.classList.toggle('warn', len > 1000);
    el.style.display = 'block';
  } else {
    el.style.display = 'none';
  }
}

// Enter gửi, Shift+Enter xuống dòng — tránh newline/IME dư khi bộ gõ đang gõ dở
let _enterSendHandled = false;
/** keydown đã gọi send — tránh gửi trùng ở keyup (một số trình duyệt/IME) */
let _enterHandledByKeydown = false;
function _isEnterKey(e){
  return e.key === 'Enter' || e.code === 'Enter' || e.code === 'NumpadEnter';
}
if (inputEl){
  inputEl.addEventListener('keydown', e => {
    _enterSendHandled = false;

    // ↑ Arrow — edit last user message (chỉ khi input rỗng)
    if(e.key === 'ArrowUp' && !e.shiftKey && !e.ctrlKey && !e.metaKey && !busy){
      if(inputEl.value === '' || inputEl.selectionStart === 0){
        const lastUser = [...rendered].reverse().find(r => r.role === 'user');
        if(lastUser && lastUser.text){
          e.preventDefault();
          inputEl.value = lastUser.text;
          inputEl.dispatchEvent(new Event('input'));
          setTimeout(() => inputEl.setSelectionRange(lastUser.text.length, lastUser.text.length), 0);
          return;
        }
      }
    }

    // @ mention — mở file picker
    if(e.key === '@' && !e.ctrlKey && !e.metaKey){
      // Delay nhỏ để ký tự @ được gõ vào trước
      setTimeout(() => _openAtMentionPicker(), 10);
    }

    // Đóng @ picker khi Escape
    if(e.key === 'Escape'){
      _closeAtMentionPicker();
    }

    if (!_isEnterKey(e) || e.shiftKey) return;
    if (e.repeat) return;
    if (e.isComposing || e.key === 'Process' || e.keyCode === 229) return;
    e.preventDefault();
    _enterSendHandled = true;
    _enterHandledByKeydown = true;
    send();
  });
  /** Một số trình duyệt/IME gửi tốt hơn qua keyup khi keydown bị nuốt */
  inputEl.addEventListener('keyup', e => {
    if (!_isEnterKey(e) || e.shiftKey) return;
    if (e.isComposing) return;
    if (_enterHandledByKeydown){ _enterHandledByKeydown = false; return; }
    e.preventDefault();
    send();
  });
  inputEl.addEventListener('beforeinput', e => {
    if (_enterSendHandled) return;
    if (e.inputType !== 'insertLineBreak' && e.inputType !== 'insertParagraph') return;
    if (typeof e.getModifierState === 'function' && e.getModifierState('Shift')) return;
    if (e.isComposing) return;
    e.preventDefault();
    send();
  });
}

// ── Draft restore ──
const savedDraft = localStorage.getItem('chat_draft');
if(savedDraft && inputEl){ inputEl.value=savedDraft; inputEl.dispatchEvent(new Event('input')); }

// ── Drag & drop ──
const dropOverlay = document.getElementById('drop-overlay');
let dragCounter = 0;
document.addEventListener('dragenter', e=>{
  if(!e.dataTransfer?.types?.includes('Files')) return;
  dragCounter++;
  dropOverlay.classList.add('active');
});
document.addEventListener('dragleave', e=>{
  dragCounter--;
  if(dragCounter<=0){ dragCounter=0; dropOverlay.classList.remove('active'); }
});
document.addEventListener('dragover', e=>{ e.preventDefault(); });
document.addEventListener('drop', e=>{
  e.preventDefault();
  dragCounter=0; dropOverlay.classList.remove('active');
  const files = Array.from(e.dataTransfer?.files||[]);
  if(!files.length) return;
  files.forEach(file=>{
    const allowed = file.type.startsWith('image/') || /\.(txt|md|py|js|ts|json|csv|html|css)$/i.test(file.name);
    if(!allowed) return;
    const reader = new FileReader();
    reader.onload = ev=>{
      const data = ev.target.result.split(',')[1];
      const previewUrl = file.type.startsWith('image/') ? ev.target.result : null;
      pendingFiles.push({name:file.name, type:file.type||'text/plain', data, previewUrl});
      renderFilePreviews();
    };
    reader.readAsDataURL(file);
  });
  inputEl.focus();
});

// ── Timestamp ──
function nowTs(){return new Date().toLocaleTimeString('vi-VN',{hour:'2-digit',minute:'2-digit'})}

// ── DOM helpers ──
function wrap(){const d=document.createElement('div');d.className='mwrap';msgsEl.appendChild(d);return d}
function removeWelcome(){const w=document.getElementById('welcome');if(w)w.closest('.mwrap')?.remove()||w.remove()}

function buildUserBubbleContent(text, images){
  const imgs = Array.isArray(images) ? images.filter(x => x && x.dataUrl) : [];
  const imgHtml = imgs.length
    ? '<div class="user-bubble-media">' + imgs.map(img =>
        `<img class="user-msg-img" src="${img.dataUrl}" alt="${esc(img.name || '')}" loading="lazy">`
      ).join('') + '</div>'
    : '';
  const t = text != null ? String(text) : '';
  const textPart = t.trim() !== '' ? `<div class="user-bubble-text">${esc(t)}</div>` : '';
  return imgHtml + textPart;
}

function renderUser(text,ts,animate=true,images){
  const w=wrap();if(!animate)w.style.animation='none';
  w.innerHTML=`<div class="mrow user"><div class="av user">${ICON_USER}</div><div class="bubble user-bubble-rich">${buildUserBubbleContent(text, images)}</div></div><div class="ts mrow user">${ts}</div>`;
  // #8 Message grouping
  _applyMessageGrouping(w, 'user');
  scrollEnd(true,true);
  return w;
}
function renderAgent(text,ts,animate=true){
  if(!String(text||'').trim()) return;
  const w=wrap();if(!animate)w.style.animation='none';
  w.innerHTML=`<div class="mrow agent"><div class="av agent">${ICON_AGENT}</div><div class="bubble">${safeMarkdown(text)}</div></div><div class="ts mrow agent">${ts}</div>`;
  addCopyBtns(w);
  addMsgActions(w, text);
  // #8 Message grouping
  _applyMessageGrouping(w, 'agent');
  scrollEnd(true,true);
}

// #8 — Áp dụng grouping: ẩn avatar nếu tin nhắn liên tiếp cùng role
function _applyMessageGrouping(newWrap, role){
  const allWraps = [...msgsEl.querySelectorAll('.mwrap:not(#typing):not(#load-more-wrap)')];
  const idx = allWraps.indexOf(newWrap);
  if(idx <= 0) return;

  // Tìm wrap trước đó có message thực (bỏ qua tool cards, event pills)
  let prevWrap = null;
  for(let i = idx - 1; i >= 0; i--){
    const w = allWraps[i];
    if(w.querySelector('.mrow.agent') || w.querySelector('.mrow.user')){
      prevWrap = w; break;
    }
  }
  if(!prevWrap) return;

  const prevRole = prevWrap.querySelector('.mrow.agent') ? 'agent' : 'user';
  if(prevRole !== role) return;

  // Cùng role liên tiếp → group
  // Xóa group-end khỏi wrap trước
  prevWrap.classList.remove(`group-end-${role}`);
  prevWrap.classList.add(`grouped-${role}`);

  // Wrap mới là grouped (ẩn avatar) và là group-end (hiện timestamp)
  newWrap.classList.add(`grouped-${role}`, `group-end-${role}`);
}

function addUser(text, images){
  removeWelcome();const ts=nowTs();
  const imgs = Array.isArray(images) && images.length ? images : undefined;
  const w = renderUser(text, ts, true, imgs);
  rendered.push({role:'user', text, ts, ...(imgs ? { images: imgs } : {})});saveRenderedDebounced();
  return w;
}

const TOOL_STATUS_HINTS={
  browser_navigate:'Đang mở trang web…',browser_click:'Đang tương tác trang…',browser_fill:'Đang điền form…',
  browser_evaluate:'Đang phân tích trang…',browser_new_tab:'Đang mở tab…',read_file:'Đang đọc file…',
  write_file:'Đang ghi file…',run_shell:'Đang chạy lệnh…',run_applescript:'Đang chạy AppleScript…',
  screenshot_and_analyze:'Đang phân tích màn hình…',open_app:'Đang mở ứng dụng…',extract_data:'Đang trích xuất dữ liệu…',
  remember:'Đang lưu bộ nhớ…',recall:'Đang tìm trong bộ nhớ…',schedule_task:'Đang xử lý lịch…',
};
function formatToolStatusHint(name){
  if(name==null||name==='')return'';
  const t=String(name);
  if(/Đang suy nghĩ/i.test(t))return'Đang suy nghĩ…';
  if(t==='Đang xử lý...'||t.includes('Đang xử lý'))return'Đang xử lý tiếp…';
  return TOOL_STATUS_HINTS[name]||`Đang chạy: ${t.replace(/_/g,' ')}`;
}

/** Phân tầng UI: kết nối / suy nghĩ / gọi tool / chờ model sau tool */
const TYPING_PHASE = {
  CONNECTING: 'connecting',
  THINKING: 'thinking',
  TOOL: 'tool',
  AWAIT_MODEL: 'await_model',
};

function _typingAnimHtml(phase){
  if(phase === TYPING_PHASE.CONNECTING){
    return '<div class="typing-anim-dots" aria-hidden="true"><span></span><span></span><span></span></div>';
  }
  if(phase === TYPING_PHASE.TOOL){
    return '<div class="typing-anim-nodes" aria-hidden="true"><span></span><span></span><span></span><span></span></div>';
  }
  if(phase === TYPING_PHASE.AWAIT_MODEL){
    return '<div class="typing-anim-awaitbars" aria-hidden="true"><span></span><span></span><span></span><span></span></div>';
  }
  return '<div class="thinking-wave" aria-hidden="true"><div class="thinking-wave-bar"></div><div class="thinking-wave-bar"></div><div class="thinking-wave-bar"></div><div class="thinking-wave-bar"></div><div class="thinking-wave-bar"></div></div>';
}

function _phaseToLabel(phase, toolName){
  if(phase === TYPING_PHASE.CONNECTING) return 'Đang kết nối máy chủ…';
  if(phase === TYPING_PHASE.THINKING) return 'Đang suy nghĩ…';
  if(phase === TYPING_PHASE.AWAIT_MODEL) return 'Đang chờ phản hồi từ model…';
  if(phase === TYPING_PHASE.TOOL) return formatToolStatusHint(toolName) || ('Đang gọi: ' + String(toolName || '').replace(/_/g, ' '));
  return 'Đang xử lý…';
}

// Status bar (stext) — chỉ hiện thông tin có giá trị thêm, không lặp bubble
function _phaseToFooter(phase, toolName){
  if(phase === TYPING_PHASE.TOOL){
    return formatToolStatusHint(toolName) || ('Đang chạy: ' + String(toolName || '').replace(/_/g, ' '));
  }
  return 'Đang xử lý…';
}

function _syncBusyFooterForPhase(phase, toolName){
  if(busy && stext) stext.textContent = _phaseToFooter(phase, toolName);
  // stext may be null if status-bar was removed from DOM — safe to ignore
}

// agent-status-line (trên input) — chỉ hiện khi có tool cụ thể đang chạy
function setAgentStatusLine(text, phase){
  const el=document.getElementById('agent-status-line');
  if(!el) return;
  const isGeneric = !text || phase === TYPING_PHASE.THINKING || phase === TYPING_PHASE.AWAIT_MODEL;
  if(isGeneric){ el.textContent=''; el.setAttribute('hidden',''); }
  else { el.textContent=text; el.removeAttribute('hidden'); }
}

let _retrySnapshot=null;
let _lastErrorPlain='';
let _lastRetryPayload=null;

function addTyping(phase, toolName){
  removeTyping();
  const ph = phase != null ? phase : TYPING_PHASE.THINKING;
  const label = _phaseToLabel(ph, toolName);
  setAgentStatusLine(label, ph);
  _syncBusyFooterForPhase(ph, toolName);
  const w=wrap();w.id='typing';
  w.setAttribute('data-typing-phase', ph);
  const startTs = Date.now();
  w.innerHTML='<div class="thinking-row"><div class="av agent">' + ICON_AGENT + '</div>'
    + '<div class="thinking-bub thinking-bub--phase-' + ph + '">'
    + _typingAnimHtml(ph)
    + '<span class="thinking-label" id="thinking-label">' + esc(label) + '</span>'
    + '<span class="thinking-timer" id="thinking-timer">0s</span>'
    + '</div></div>';
  const timerInterval = setInterval(() => {
    const el = document.getElementById('thinking-timer');
    if(!el){ clearInterval(timerInterval); return; }
    const sec = Math.floor((Date.now() - startTs) / 1000);
    el.textContent = sec + 's';
  }, 1000);
  w._timerInterval = timerInterval;
  scrollEnd();
}

function setTypingPhase(phase, toolName){
  const ph = phase != null ? phase : TYPING_PHASE.THINKING;
  const label = _phaseToLabel(ph, toolName);
  setAgentStatusLine(label, ph);
  _syncBusyFooterForPhase(ph, toolName);
  // Orb sync với phase
  if(ph === TYPING_PHASE.TOOL && toolName) _orbSetTool(toolName);
  else if(ph === TYPING_PHASE.AWAIT_MODEL || ph === TYPING_PHASE.THINKING) _orbSetThinking();
  const t = document.getElementById('typing');
  if(!t){
    addTyping(ph, toolName);
    return;
  }
  t.setAttribute('data-typing-phase', ph);
  const bub = t.querySelector('.thinking-bub');
  if(bub){
    bub.className = 'thinking-bub thinking-bub--phase-' + ph;
    const lab = document.getElementById('thinking-label');
    if(lab && lab.previousElementSibling){
      lab.previousElementSibling.outerHTML = _typingAnimHtml(ph);
    }
  }
  const el = document.getElementById('thinking-label');
  if(el){
    el.style.opacity = '0.65';
    el.textContent = label;
    requestAnimationFrame(()=>{ el.style.opacity = '1'; });
  }
}

/** @deprecated dùng setTypingPhase(TYPING_PHASE.TOOL, name) hoặc AWAIT_MODEL */
function updateThinkingLabel(toolName){
  if(toolName === 'Đang xử lý...' || toolName === 'Đang xử lý…'){
    setTypingPhase(TYPING_PHASE.AWAIT_MODEL);
    return;
  }
  setTypingPhase(TYPING_PHASE.TOOL, toolName);
}

function _snippetFromReply(text, maxLen){
  if(!text || !String(text).trim()) return '';
  let s = String(text).replace(/\s+/g, ' ').trim();
  s = s.replace(/^#{1,6}\s+/gm, '').replace(/\*\*([^*]+)\*\*/g, '$1').replace(/`+/g, '');
  if(s.length <= maxLen) return s;
  const cut = s.slice(0, maxLen);
  const sp = cut.lastIndexOf(' ');
  return (sp > 40 ? cut.slice(0, sp) : cut) + '…';
}

function appendStoppedNoticeAndFocus(){
  removeTyping();
  const w = wrap();
  w.classList.add('chat-stopped-mwrap');
  w.innerHTML =
    '<div class="chat-stopped-notice" role="status">' +
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/></svg>' +
    '<span>Đã dừng — bạn có thể chỉnh lại yêu cầu và gửi tiếp.</span></div>';
  msgsEl.appendChild(w);
  scrollEnd(true);
  requestAnimationFrame(() => {
    try {
      inputEl.focus({ preventScroll: true });
    } catch(_) {
      inputEl.focus();
    }
  });
}
function removeTyping(){
  const t=document.getElementById('typing');
  if(t){
    if(t._timerInterval) clearInterval(t._timerInterval);
    t.remove();
  }
}

function showChatError(errMsg,userText,replySoFar){
  const full=String(errMsg||'Lỗi không xác định').replace(/^Lỗi:\s*/i,'').trim();
  _lastErrorPlain=full;
  _lastRetryPayload=_retrySnapshot;
  removeTyping();
  let hadPartial=false;
  const prevReply=typeof replySoFar==='string'?replySoFar:'';
  if(curBubble){
    if(String(curText||'').trim()){
      finalizeBubble();
      hadPartial=true;
    } else {
      document.querySelector('.streaming-agent-wrap')?.remove();
      curBubble=null;curText='';
    }
  }
  const combined=(prevReply&&prevReply.trim()?prevReply.trim()+'\n\n---\n':'')+'Lỗi: '+full;
  history.push({role:'user',content:userText});
  history.push({role:'assistant',content:combined});
  saveHistoryDebounced();
  const ts=nowTs();
  rendered.push({role:'agent',text:'Lỗi: '+full,ts});
  saveRenderedDebounced();
  const w=wrap();
  w.classList.add('chat-error-row');
  w.innerHTML=`<div class="mrow agent"><div class="av agent">${ICON_AGENT}</div><div class="bubble chat-error-bubble"><div class="chat-error-text">${esc('Lỗi: '+full)}</div><div class="chat-error-actions"><button type="button" class="btn-retry" data-oculo="retryLastFailedSend">Thử lại</button><button type="button" class="btn-copy-err" data-oculo="copyLastChatError">Sao chép lỗi</button></div></div></div><div class="ts mrow agent">${ts}</div>`;
  scrollEnd(true,true);
  hideTodoPanel();
  saveCurrentConv();
}
function retryLastFailedSend(){
  const p=_lastRetryPayload;
  if(!p||!p.text){showToast('Không có gì để thử lại');return;}
  document.querySelectorAll('.chat-error-row').forEach(el=>el.remove());
  if(history.length>=2){
    if(history[history.length-1].role==='assistant') history.pop();
    if(history[history.length-1].role==='user') history.pop();
  }
  saveHistoryDebounced();
  if(rendered.length&&rendered[rendered.length-1].role==='agent'&&String(rendered[rendered.length-1].text||'').startsWith('Lỗi:')){
    rendered.pop();
  }
  if(rendered.length&&rendered[rendered.length-1].role==='user'){
    rendered.pop();
    const users=[...msgsEl.querySelectorAll('.mwrap')].filter(w=>w.querySelector('.mrow.user'));
    users[users.length-1]?.remove();
  }
  saveRenderedDebounced();
  inputEl.value=p.text;
  pendingFiles=Array.isArray(p.files)?p.files.map(f=>({...f})):[];
  renderFilePreviews();
  inputEl.dispatchEvent(new Event('input'));
  inputEl.focus();
  send();
}
function copyLastChatError(){
  const t=_lastErrorPlain||'';
  if(!t){showToast('Không có nội dung');return;}
  navigator.clipboard.writeText(t).then(()=>showToast('Đã sao chép lỗi')).catch(()=>showToast('Không sao chép được'));
}

function startBubble(){
  removeTyping();curText='';
  const w=wrap();
  w.classList.add('streaming-agent-wrap');
  w.innerHTML=`<div class="mrow agent"><div class="av agent thinking">${ICON_AGENT}</div><div class="bubble streaming"></div></div>`;
  curBubble=w.querySelector('.bubble.streaming');
  scrollEnd(true);
}
function flushBubbleRender(forceScroll=false){
  if(!curBubble) return;
  curBubble.innerHTML = safeMarkdown(curText);
  if(forceScroll) scrollEnd(false);
}
let _textBatch = '';
let _batchTimer = null;
function appendText(t){
  if(!t) return;  // bỏ qua chunk rỗng
  if(!curBubble)startBubble();
  _textBatch += t;
  curText += t;
  if(_batchTimer) return;
    _batchTimer = setTimeout(()=>{
    _batchTimer = null;
    if(curBubble) {
      curBubble.innerHTML = safeMarkdown(curText);
      scrollEnd(false);
    }
    _textBatch = '';
  }, 30); // batch 30ms — nhanh hơn 80ms cũ
}
function finalizeBubble(){
  // Dọn timer trước
  if(streamRenderTimer){ clearTimeout(streamRenderTimer); streamRenderTimer=null; }
  if(_batchTimer){ clearTimeout(_batchTimer); _batchTimer=null; }

  const wrap = document.querySelector('.streaming-agent-wrap');
  if(curBubble) curBubble.classList.remove('streaming');
  if(wrap) wrap.querySelectorAll('.av.agent').forEach(a=>a.classList.remove('thinking'));

  if(!String(curText||'').trim()){
    if(wrap) wrap.remove();
    curBubble=null; curText='';
    return;
  }

  flushBubbleRender(true);
  const ts=nowTs();
  if(wrap){
    wrap.classList.remove('streaming-agent-wrap');
    wrap.insertAdjacentHTML('beforeend',`<div class="ts mrow agent">${ts}</div>`);
    addCopyBtns(wrap);
    addMsgActions(wrap, curText);
  }
  rendered.push({role:'agent',text:curText,ts});saveRenderedDebounced();
  notifyNewMsg();
  curBubble=null;curText='';
}

function removeEmptyAgentMessageWraps(){
  msgsEl.querySelectorAll('.mwrap').forEach(w=>{
    if(w.id==='typing'||w.id==='load-more-wrap') return;
    if(w.classList.contains('chat-error-row')) return;
    if(w.querySelector('.thinking-row,.tcard,.agent-event,.token-bar,.followup-wrap,.continue-wrap')) return;
    const row=w.querySelector('.mrow.agent');
    if(!row) return;
    const bub=row.querySelector('.bubble');
    if(!bub) { w.remove(); return; }
    const raw=bub.textContent.replace(/\u200b/g,'').trim();
    if(raw) return;
    if(bub.querySelector('pre,img,video,table,blockquote,ul,ol,iframe')) return;
    w.remove();
  });
}

function stripEmptyAgentFromRendered(arr){
  return arr.filter(m=>m.role!=='agent'||String(m.text||'').trim()!=='');
}

// ── Copy buttons + language label (data-oculo: runCmdFromPre, copyCodeBlock) ──
function runCmdFromPre(btn){
  const pre = btn.closest('pre');
  if(!pre) return;
  const code = pre.querySelector('code')?.innerText || pre.innerText;
  const firstLine = code.trim().split('\n')[0];
  inputEl.value = firstLine;
  inputEl.dispatchEvent(new Event('input'));
  inputEl.focus();
  showToast('Đã paste lệnh vào input');
}

function copyCodeBlock(btn){
  const pre = btn.closest('pre');
  if(!pre) return;
  const code = pre.querySelector('code')?.innerText || pre.innerText;
  navigator.clipboard.writeText(code).then(()=>{
    const orig = btn.innerHTML;
    btn.innerHTML = '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg> Đã chép';
    btn.classList.add('copied');
    showToast('✓ Đã sao chép code');
    setTimeout(()=>{ btn.textContent = 'Sao chép'; btn.classList.remove('copied'); }, 2000);
  });
}

function addCopyBtns(container){
  container.querySelectorAll('pre').forEach(pre=>{
    if(pre.querySelector('.copy-btn'))return;

    // Language label (mục 11)
    const codeEl = pre.querySelector('code');
    if(codeEl){
      const langClass = Array.from(codeEl.classList).find(c=>c.startsWith('language-'));
      if(langClass){
        const lang = langClass.replace('language-','');
        if(lang && lang !== 'plaintext' && lang !== 'text'){
          const label = document.createElement('span');
          label.className = 'code-lang-label';
          label.textContent = lang;
          pre.appendChild(label);
          pre.classList.add('has-lang');
        }
      }
    }

    // #12 Run command button for shell code blocks
    const lang = pre.querySelector('code')?.className?.match(/language-(\w+)/)?.[1] || '';
    if(['bash','sh','shell','zsh'].includes(lang)){
      const runBtn = document.createElement('button');
      runBtn.type = 'button';
      runBtn.className = 'run-cmd-btn';
      runBtn.setAttribute('data-oculo', 'runCmdFromPre');
      runBtn.innerHTML = '<svg viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3" fill="currentColor"/></svg>Chạy';
      runBtn.title = 'Chạy lệnh này';
      pre.appendChild(runBtn);
    }

    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'copy-btn';
    btn.textContent = 'Sao chép';
    btn.setAttribute('data-oculo', 'copyCodeBlock');
    pre.appendChild(btn);
  });
}

// ── Message actions (copy all, retry, pin) ──
// Store text by index to avoid HTML injection
const _msgTextStore = [];
function addMsgActions(container, text){
  const mrow = container.querySelector('.mrow.agent');
  if(!mrow) return;
  const idx = _msgTextStore.push(text) - 1;
  const div = document.createElement('div');
  div.className = 'msg-actions';
  div.innerHTML = `
    <button type="button" class="msg-act-btn" title="Sao chép toàn bộ" data-oculo="copyMsgText" data-oculo-msg-idx="${idx}">
      <svg viewBox="0 0 24 24"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
    </button>
    <button type="button" class="msg-act-btn" title="Gửi lại" data-oculo="retryMsg">
      <svg viewBox="0 0 24 24"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 .49-3.5"/></svg>
    </button>
    <button type="button" class="msg-act-btn" title="Ghim vào bộ nhớ" data-oculo="pinToMemory" data-oculo-msg-idx="${idx}">
      <svg viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
    </button>`;
  mrow.appendChild(div);
}

function copyMsgText(btn, idx){
  const text = _msgTextStore[idx] || '';
  navigator.clipboard.writeText(text).then(()=>{
    const orig = btn.innerHTML;
    btn.innerHTML='<svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>';
    setTimeout(()=>btn.innerHTML=orig, 1500);
  });
}

function retryMsg(btn){
  const mwrap = btn.closest('.mwrap');
  let prev = mwrap?.previousElementSibling;
  while(prev && !prev.querySelector('.mrow.user')) prev = prev.previousElementSibling;
  const userBubble = prev?.querySelector('.mrow.user .bubble');
  if(!userBubble) return;
  inputEl.value = userBubble.textContent;
  inputEl.dispatchEvent(new Event('input'));
  inputEl.focus();
}

async function pinToMemory(btn, idx){
  const text = _msgTextStore[idx] || '';
  try{
    const _pinRes = await fetch('/memory',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({content:text.slice(0,500), metadata:{category:'pinned'}})});
    if(!_pinRes.ok){ showToast('Lỗi khi ghim: ' + _pinRes.status); return; }
    // #9 Persistent pin indicator
    btn.classList.add('pinned');
    btn.title = 'Đã ghim vào bộ nhớ';
    // Add badge next to timestamp
    const mwrap = btn.closest('.mwrap');
    if(mwrap && !mwrap.querySelector('.msg-pinned-badge')){
      const ts = mwrap.querySelector('.ts');
      if(ts){
        const badge = document.createElement('span');
        badge.className = 'msg-pinned-badge';
        badge.innerHTML = '<svg viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg> Đã ghim';
        ts.appendChild(badge);
      }
    }
    showToast('✓ Đã ghim vào bộ nhớ');
  }catch(e){ showToast('Lỗi khi ghim'); }
}

// Tools ẩn - chạy ngầm không hiển thị card
// run_shell KHÔNG ẩn vì cần hiện streaming output
const HIDDEN_TOOLS = new Set(['run_applescript', 'notify', 'remember', 'recall', 'schedule_task']);

// Lấy preview 1-dòng thông minh theo từng tool
function toolInputSummary(name, input){
  if(typeof input === 'string') return input.slice(0,70);
  const pick = {
    browser_evaluate:'js', screenshot_and_analyze:'question',
    browser_navigate:'url', browser_fill:'value',
    browser_click:'selector', read_file:'path',
    write_file:'path', open_app:'app_name',
    extract_data:'query', remember:'content', recall:'query',
  };
  const key = pick[name];
  if(key && input[key]) return String(input[key]).replace(/\n/g,' ').slice(0,70);
  for(const v of Object.values(input)){
    if(typeof v==='string') return v.replace(/\n/g,' ').slice(0,70);
  }
  return JSON.stringify(input).slice(0,70);
}

// Phát hiện markdown thật sự (có heading, bullet, bold)
function looksLikeMarkdown(s){
  return /^#{1,3} |^\*{1,2}|^- |\*\*|`{1,3}|\[.+\]\(/.test(s);
}

// ── Tool cards (collapsed by default) ──
function addToolCard(name,input){
  if(HIDDEN_TOOLS.has(name)) return null;
  const w = wrap();
  const preview = esc(toolInputSummary(name, input));
  const inputStr = typeof input==='object' ? JSON.stringify(input,null,2) : input;
  const isShell = name === 'run_shell';
  const bodyClass = isShell ? 'tbody expanded' : 'tbody';
  const startTs = Date.now(); // #4 elapsed time
  const card = document.createElement('div');
  card.className = 'tcard' + (isShell ? ' tcard-shell' : '');
  card.dataset.start = startTs;
  const thead = document.createElement('div');
  thead.className = 'thead';
  thead.onclick = function(){ toggleCard(this); };
  thead.innerHTML = ICON_TOOL
    + '<span class="tname">' + esc(name) + '</span>'
    + '<span class="tsep">·</span>'
    + '<span class="tpreview">' + preview + '</span>'
    + '<span class="tchev">' + (isShell ? ICON_CHEVRON_DOWN : ICON_CHEVRON_RIGHT) + '</span>'
    + '<span class="tbadge">chạy...</span>';
  const tbody = document.createElement('div');
  tbody.className = bodyClass;
  if(!isShell){
    tbody.innerHTML = '<div class="tinput-label">Input</div><div class="tinput">' + esc(inputStr) + '</div>';
  }
  card.appendChild(thead);
  card.appendChild(tbody);
  if(isShell) thead.querySelector('.tchev').classList.add('open');
  w.appendChild(card);
  scrollEnd(false);
  return card;
}

const QUIET_TOOL_LABELS = {
  run_applescript: 'AppleScript',
  notify: 'Thông báo',
  remember: 'Ghi nhớ',
  recall: 'Truy vấn bộ nhớ',
  schedule_task: 'Lên lịch',
};

function addQuietToolRow(name, input){
  const w = wrap();
  const title = QUIET_TOOL_LABELS[name] || name.replace(/_/g, ' ');
  const hint = toolInputSummary(name, input).slice(0, 120);
  w.innerHTML = `<div class="quiet-tool-line">
    <span class="quiet-tool-dot" aria-hidden="true"></span>
    <span class="quiet-tool-title">${esc(title)}</span>
    <span class="quiet-tool-hint">${esc(hint)}</span>
    <span class="quiet-tool-status">…</span>
  </div>`;
  scrollEnd(false);
  return w;
}

function finishQuietToolLine(wrap, result, maskedFlag){
  const st = wrap.querySelector('.quiet-tool-status');
  if(st){
    const err = _toolResultLooksLikeError(result);
    st.textContent = err ? 'Lỗi' : 'Xong';
    st.classList.toggle('quiet-tool-status--err', err);
  }
  if(maskedFlag){
    wrap.insertAdjacentHTML('beforeend', '<div class="quiet-tool-mask" role="status">Đã ẩn một phần dữ liệu nhạy cảm trên màn hình</div>');
  }
}

function toggleCard(header){
  const body = header.nextElementSibling;
  const chev = header.querySelector('.tchev');
  const isOpen = body.classList.contains('expanded');
  body.classList.toggle('expanded', !isOpen);
  chev.classList.toggle('open', !isOpen);
  chev.innerHTML = !isOpen ? ICON_CHEVRON_DOWN : ICON_CHEVRON_RIGHT;
}

function _toolResultLooksLikeError(result){
  const s = String(result || '').trim();
  return /^(Error|Lỗi)\s*:/i.test(s);
}

function finishCard(card, result, maskedFlag){
  const b = card.querySelector('.tbadge');
  const isErr = _toolResultLooksLikeError(result);
  // #4 Elapsed time
  const startTs = parseInt(card.dataset.start || '0');
  const elapsed = startTs ? ((Date.now() - startTs) / 1000).toFixed(1) + 's' : '';
  if(b){
    if(isErr){
      b.textContent = elapsed ? 'lỗi · ' + elapsed : 'lỗi';
      b.className = 'tbadge tbadge--error';
    } else {
      b.textContent = elapsed ? 'xong · ' + elapsed : 'xong';
      b.className = 'tbadge done';
    }
  }

  const short = (result||'').replace(/\s+/g,' ').trim().slice(0,60);
  const previewEl = card.querySelector('.tpreview');
  if(previewEl && short && short!=='None'){
    previewEl.textContent = '› ' + short + (result.length>60?'…':'');
  }

  const body = card.querySelector('.tbody');
  // #8 Add copy button to result
  const copyResultBtn = document.createElement('button');
  copyResultBtn.className = 'tcopy-btn';
  copyResultBtn.textContent = 'Sao chép';
  copyResultBtn.onclick = () => {
    navigator.clipboard.writeText(result||'').then(()=>{
      copyResultBtn.textContent = '✓ Đã chép';
      setTimeout(()=>copyResultBtn.textContent='Sao chép', 1500);
    });
  };
  body.style.position = 'relative';
  body.appendChild(copyResultBtn);
  const resultHtml = looksLikeMarkdown(result)
    ? '<div class="tresult-label tresult-label--pad">Kết quả</div><div class="tresult-md">' + safeMarkdown(result) + '</div>'
    : '<div class="tresult-label tresult-label--pad">Kết quả</div><div class="tresult-raw">' + esc(result) + '</div>';
  body.insertAdjacentHTML('beforeend', resultHtml);
  if(maskedFlag){
    body.insertAdjacentHTML('beforeend', '<div class="tresult-mask-note" role="status">Một phần nội dung có thể đã được ẩn (khóa API, v.v.) trước khi hiển thị</div>');
  }
}

// ── Tool execution timeline (một block / lượt trả lời tới khi done) ──
let _execBlockState = null;
let _pendingShellToolUseId = null;

function execToolCategory(name){
  if(name === 'run_shell') return 'shell';
  if(/^browser_/.test(name)) return 'browser';
  if(name === 'read_file' || name === 'write_file') return 'file';
  if(name === 'remember' || name === 'recall') return 'memory';
  return 'system';
}

const EXEC_ICON_SVG = {
  shell: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/></svg>`,
  browser: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>`,
  file: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>`,
  memory: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>`,
  system: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>`,
};

function execFormatToolDetail(name, input){
  if(name === 'run_shell'){
    const cmd = (input && input.cmd) ? String(input.cmd) : '';
    return '<div class="exec-detail-label">Lệnh</div><pre class="exec-code-wrap"><code class="language-bash exec-cmd-code">' + esc(cmd) + '</code></pre>';
  }
  if(name === 'write_file'){
    const path = input && input.path ? String(input.path) : '';
    const content = input && input.content != null ? String(input.content) : '';
    const lines = content ? content.split('\n').length : 0;
    return '<div class="exec-detail-label">File</div><div class="exec-file-meta"><span class="exec-mono">' + esc(path) + '</span>'
      + (lines ? '<span class="exec-file-lines"> · ' + lines + ' dòng</span>' : '') + '</div>'
      + '<div class="exec-detail-label">Input (JSON)</div><pre class="exec-json-pre exec-mono">' + esc(JSON.stringify(input, null, 2)) + '</pre>';
  }
  if(/^browser_/.test(name)){
    const u = input && input.url != null ? String(input.url) : '';
    const sel = input && input.selector != null ? String(input.selector) : '';
    const js = input && input.js != null ? String(input.js) : '';
    let extra = '';
    if(u) extra += '<div class="exec-browser-line"><span class="exec-detail-label">URL</span><span class="exec-mono">' + esc(u) + '</span></div>';
    if(sel) extra += '<div class="exec-browser-line"><span class="exec-detail-label">Selector</span><span class="exec-mono">' + esc(sel) + '</span></div>';
    if(js && name === 'browser_evaluate') extra += '<div class="exec-browser-line"><span class="exec-detail-label">JS</span><span class="exec-mono">' + esc(js.slice(0, 400)) + (js.length > 400 ? '…' : '') + '</span></div>';
    if(!extra) extra = '<pre class="exec-json-pre exec-mono">' + esc(JSON.stringify(input, null, 2)) + '</pre>';
    return extra;
  }
  return '<pre class="exec-json-pre exec-mono">' + esc(JSON.stringify(input, null, 2)) + '</pre>';
}

function execHighlightDetail(rootEl){
  if(!rootEl || typeof hljs === 'undefined') return;
  rootEl.querySelectorAll('pre code.exec-cmd-code').forEach(el => {
    try{ hljs.highlightElement(el); }catch(_){}
  });
}

function execEnsureBlock(){
  if(_execBlockState) return _execBlockState;
  const w = wrap();
  w.classList.add('exec-mwrap');
  const root = document.createElement('div');
  root.className = 'execution-block';
  root.dataset.execDone = '0';
  root.dataset.execOpen = '1';
  root.innerHTML = ''
    + '<button type="button" class="exec-block-header" aria-expanded="true">'
    + '<span class="exec-block-hicon">' + ICON_TOOL + '</span>'
    + '<span class="exec-block-title">Agent đang thực thi</span>'
    + '<span class="exec-block-count"></span>'
    + '<span class="exec-block-status"></span>'
    + '<span class="exec-block-chev">' + ICON_CHEVRON_DOWN + '</span>'
    + '</button>'
    + '<div class="exec-block-panel">'
    +   '<div class="exec-timeline">'
    +     '<div class="exec-items"></div>'
    +   '</div>'
    + '</div>'
    + '<div class="exec-block-footer" hidden>'
    +   '<div class="exec-footer-summary"></div>'
    +   '<button type="button" class="exec-footer-err-btn" hidden>Xem chi tiết lỗi</button>'
    +   '<div class="exec-footer-err-body"></div>'
    + '</div>';

  w.appendChild(root);
  const header = root.querySelector('.exec-block-header');
  header.addEventListener('click', (ev) => {
    ev.preventDefault();
    const collapsed = root.classList.toggle('execution-block--collapsed');
    root.dataset.execOpen = collapsed ? '0' : '1';
    header.setAttribute('aria-expanded', collapsed ? 'false' : 'true');
    const chev = header.querySelector('.exec-block-chev');
    if(chev) chev.innerHTML = collapsed ? ICON_CHEVRON_RIGHT : ICON_CHEVRON_DOWN;
  });

  const footer = root.querySelector('.exec-block-footer');
  const errBtn = root.querySelector('.exec-footer-err-btn');
  const errBody = root.querySelector('.exec-footer-err-body');
  if(errBtn && errBody){
    errBtn.addEventListener('click', () => {
      const open = errBody.classList.toggle('exec-footer-err-body--open');
      errBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  _execBlockState = {
    wrap: w,
    root,
    itemsEl: root.querySelector('.exec-items'),
    toolMap: new Map(),
    order: [],
    blockStartMs: null,
    lastEndMs: null,
    errors: [],
    footerEl: footer,
    errBtn,
    errBody,
  };
  execRefreshHeader();
  scrollEnd(false);
  return _execBlockState;
}

function execRefreshHeader(){
  const st = _execBlockState;
  if(!st) return;
  const n = st.toolMap.size;
  const ce = st.root.querySelector('.exec-block-count');
  const se = st.root.querySelector('.exec-block-status');
  if(ce) ce.textContent = n ? '· ' + n + ' công cụ' : '';
  if(se){
    let running = 0, err = 0, ok = 0;
    st.toolMap.forEach(row => {
      const s = row.dataset.status;
      if(s === 'running') running++;
      else if(s === 'error') err++;
      else if(s === 'ok') ok++;
    });
    if(st.root.dataset.execDone === '1'){
      se.textContent = err ? 'Hoàn tất · có lỗi' : 'Hoàn tất';
      se.classList.toggle('exec-block-status--err', err > 0);
    } else {
      se.textContent = running ? 'Đang chạy' : 'Đang xử lý';
      se.classList.remove('exec-block-status--err');
    }
  }
}

function execAddToolItem(toolUseId, name, input){
  const st = execEnsureBlock();
  const id = String(toolUseId);
  if(st.blockStartMs == null) st.blockStartMs = Date.now();

  const row = document.createElement('div');
  row.className = 'exec-tool-item';
  row.dataset.status = 'running';
  row.dataset.toolId = id;
  row.dataset.toolName = name;

  const cat = execToolCategory(name);
  const summaryRaw = toolInputSummary(name, input || {});
  const summary = esc(summaryRaw);
  const dangerous = name === 'run_shell' || name === 'write_file' || name === 'run_applescript';
  const iconSvg = EXEC_ICON_SVG[cat] || EXEC_ICON_SVG.system;

  row.innerHTML = ''
    + '<div class="exec-tool-head" role="button" tabindex="0">'
    +   '<span class="exec-tool-track" aria-hidden="true">'
    +     '<span class="exec-tool-connector"></span>'
    +     '<span class="exec-tool-spine-dot" data-state="running"></span>'
    +   '</span>'
    +   '<span class="exec-tool-ico">' + iconSvg + '</span>'
    +   '<span class="exec-tool-name">' + esc(name) + '</span>'
    +   (dangerous ? '<span class="exec-tool-warn-badge">Thực thi hệ thống</span>' : '')
    +   '<span class="exec-tool-sum" title="' + summary + '">' + summary + '</span>'
    + '</div>'
    + '<div class="exec-tool-detail" hidden>'
    +   '<div class="exec-tool-io">'
    +     '<div class="exec-detail-label">Input</div>'
    +     '<div class="exec-tool-input-block">' + execFormatToolDetail(name, input || {}) + '</div>'
    +     (name === 'run_shell' ? '<div class="exec-detail-label exec-stream-label">Output (stream)</div><div class="exec-tool-stream"></div>' : '')
    +     '<div class="exec-detail-label">Kết quả</div>'
    +     '<div class="exec-tool-out"></div>'
    +   '</div>'
    + '</div>';

  // Tự động mở detail cho các tool có output đáng xem
  const AUTO_EXPAND_TOOLS = new Set([
    'run_shell', 'read_file', 'write_file',
    'browser_navigate', 'browser_analyze_page',
    'browser_vision_click', 'browser_vision_type',
    'recall', 'extract_data',
  ]);
  if(AUTO_EXPAND_TOOLS.has(name)){
    row.classList.add('exec-tool-item--open');
    const det = row.querySelector('.exec-tool-detail');
    if(det) det.hidden = false;
  }

  const head = row.querySelector('.exec-tool-head');
  head.addEventListener('click', (ev) => {
    ev.stopPropagation();
    row.classList.toggle('exec-tool-item--open');
    const det = row.querySelector('.exec-tool-detail');
    if(det) det.hidden = !row.classList.contains('exec-tool-item--open');
  });
  head.addEventListener('keydown', (ev) => {
    if(ev.key === 'Enter' || ev.key === ' '){
      ev.preventDefault();
      head.click();
    }
  });

  st.itemsEl.appendChild(row);
  st.toolMap.set(id, row);
  st.order.push({ id, name });
  execHighlightDetail(row);
  execRefreshHeader();
  scrollEnd(false);
  if(name === 'run_shell') _pendingShellToolUseId = id;
  // Orb: tool running
  _orbSetTool(name);
  // Screenshot: hiện shimmer placeholder
  if(name === 'screenshot_and_analyze'){
    const out = row.querySelector('.exec-tool-out');
    if(out){
      out.innerHTML = `<div class="exec-screenshot-loading">
        <svg viewBox="0 0 24 24"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
        Đang chụp màn hình…
      </div>`;
    }
  }
}

function execAppendShellStream(toolUseId, line){
  const st = _execBlockState;
  if(!st) return;
  const id = String(toolUseId);
  const row = st.toolMap.get(id);
  if(!row) return;
  const sw = row.querySelector('.exec-tool-stream');
  if(!sw) return;
  const ln = document.createElement('div');
  ln.className = 'exec-stream-line';
  ln.textContent = line;
  sw.appendChild(ln);
  sw.scrollTop = sw.scrollHeight;
  scrollEnd(false);
}

// ── Write-file diff map: tid → {path, before} ──
const _writeFileBeforeMap = new Map();

/** Tạo diff HTML đơn giản (line-level) giữa before và after */
function _buildDiffHtml(before, after){
  const bLines = before.split('\n');
  const aLines = after.split('\n');
  const maxLen = Math.max(bLines.length, aLines.length);
  let html = '<div class="diff-view">';
  let added = 0, removed = 0;
  for(let i = 0; i < maxLen; i++){
    const b = bLines[i]; const a = aLines[i];
    if(b === undefined){
      html += `<div class="diff-line diff-add"><span class="diff-gutter">+</span><span class="diff-code">${esc(a)}</span></div>`;
      added++;
    } else if(a === undefined){
      html += `<div class="diff-line diff-del"><span class="diff-gutter">−</span><span class="diff-code">${esc(b)}</span></div>`;
      removed++;
    } else if(b !== a){
      html += `<div class="diff-line diff-del"><span class="diff-gutter">−</span><span class="diff-code">${esc(b)}</span></div>`;
      html += `<div class="diff-line diff-add"><span class="diff-gutter">+</span><span class="diff-code">${esc(a)}</span></div>`;
      removed++; added++;
    } else {
      html += `<div class="diff-line diff-ctx"><span class="diff-gutter"> </span><span class="diff-code">${esc(b)}</span></div>`;
    }
  }
  html += '</div>';
  const summary = `<div class="diff-summary"><span class="diff-add-count">+${added}</span><span class="diff-del-count">−${removed}</span></div>`;
  return summary + html;
}

function execFindRowForResult(d){
  const st = _execBlockState;
  if(!st) return null;
  const tid = d.tool_use_id != null ? String(d.tool_use_id) : '';
  if(tid && st.toolMap.has(tid)) return st.toolMap.get(tid);
  for(let i = st.order.length - 1; i >= 0; i--){
    const o = st.order[i];
    const r = st.toolMap.get(o.id);
    if(r && r.dataset.status === 'running' && o.name === d.name) return r;
  }
  return null;
}

function execApplyToolResult(d){
  const st = _execBlockState;
  if(!st) return;
  const row = execFindRowForResult(d);
  if(!row) return;
  const result = d.result != null ? String(d.result) : '';
  const masked = !!d.masked;
  const toolName = d.name || row.dataset.toolName || '';
  const isErr = typeof d.is_error === 'boolean' ? d.is_error : _toolResultLooksLikeError(result);
  row.dataset.status = isErr ? 'error' : 'ok';
  const dot = row.querySelector('.exec-tool-spine-dot');
  if(dot){
    dot.dataset.state = isErr ? 'error' : 'ok';
  }
  if(isErr){
    row.classList.add('exec-tool-item--err');
    st.errors.push({ name: toolName, message: result.slice(0, 2000) });
    _orbSetError();
  } else {
    // Orb: back to thinking (waiting for next model response)
    _orbSetThinking();
  }
  const out = row.querySelector('.exec-tool-out');
  if(out){
    // Screenshot tool: hiện thumbnail thay vì raw text
    if(toolName === 'screenshot_and_analyze' && d.screenshot_b64){
      const ts = new Date().toLocaleTimeString('vi-VN',{hour:'2-digit',minute:'2-digit',second:'2-digit'});
      out.innerHTML = `<div class="exec-screenshot-thumb-wrap">
        <img class="exec-screenshot-thumb" src="data:image/png;base64,${d.screenshot_b64}" alt="Screenshot" title="Click để phóng to">
        <span class="exec-screenshot-badge">${ts}</span>
      </div>`;
      const thumb = out.querySelector('.exec-screenshot-thumb');
      if(thumb){
        thumb.addEventListener('click', () => {
          const lb = document.createElement('div');
          lb.className = 'browser-frame-lightbox';
          const full = document.createElement('img');
          full.src = thumb.src; full.alt = 'Screenshot full';
          lb.appendChild(full);
          lb.addEventListener('click', () => lb.remove());
          document.body.appendChild(lb);
        });
      }
      // Vẫn hiện text analysis bên dưới
      if(result){
        out.insertAdjacentHTML('beforeend',
          '<div class="exec-tool-out-md" style="margin-top:8px">' + safeMarkdown(result) + '</div>');
      }
    } else {
      const html = looksLikeMarkdown(result)
        ? '<div class="exec-tool-out-md">' + safeMarkdown(result) + '</div>'
        : '<pre class="exec-tool-out-raw exec-mono">' + esc(result) + '</pre>';
      out.innerHTML = html;
      // Diff view cho write_file
      if(toolName === 'write_file' && !isErr){
        const tid = d.tool_use_id != null ? String(d.tool_use_id) : '';
        const diffData = _writeFileBeforeMap.get(tid);
        if(diffData && diffData.newContent){
          if(diffData.before !== null){
            const diffHtml = _buildDiffHtml(diffData.before, diffData.newContent);
            out.insertAdjacentHTML('beforeend',
              `<details class="diff-details" open>
                <summary class="diff-toggle">Thay đổi trong <code>${esc(diffData.path.split('/').pop())}</code></summary>
                ${diffHtml}
              </details>`);
          } else {
            // File mới — hiện toàn bộ nội dung như "added"
            const lines = diffData.newContent.split('\n');
            const addedHtml = lines.map(l =>
              `<div class="diff-line diff-add"><span class="diff-gutter">+</span><span class="diff-code">${esc(l)}</span></div>`
            ).join('');
            out.insertAdjacentHTML('beforeend',
              `<details class="diff-details" open>
                <summary class="diff-toggle">File mới: <code>${esc(diffData.path.split('/').pop())}</code></summary>
                <div class="diff-summary"><span class="diff-add-count">+${lines.length}</span></div>
                <div class="diff-view">${addedHtml}</div>
              </details>`);
          }
          _writeFileBeforeMap.delete(tid);
        }
      }
    }
    if(masked){
      out.insertAdjacentHTML('beforeend', '<div class="exec-tool-mask" role="status">Một phần nội dung có thể đã được ẩn trước khi hiển thị</div>');
    }
  }
  st.lastEndMs = Date.now();
  execRefreshHeader();
  if(toolName === 'run_shell' || String(d.tool_use_id) === _pendingShellToolUseId){
    _pendingShellToolUseId = null;
  }
}

function execApplyToolError(d){
  const st = _execBlockState;
  if(!st) return;
  const tid = d.tool_use_id != null ? String(d.tool_use_id) : _pendingShellToolUseId;
  const row = tid ? st.toolMap.get(tid) : null;
  if(!row) return;
  row.dataset.status = 'error';
  row.classList.add('exec-tool-item--err');
  const dot = row.querySelector('.exec-tool-spine-dot');
  if(dot){ dot.dataset.state = 'error'; }
  const msg = (d.error != null ? String(d.error) : 'Lỗi');
  st.errors.push({ name: d.name || 'run_shell', message: msg });
  const out = row.querySelector('.exec-tool-out');
  if(out){
    out.innerHTML = '<pre class="exec-tool-out-raw exec-mono exec-tool-out-err">' + esc(msg) + '</pre>';
  }
  st.lastEndMs = Date.now();
  execRefreshHeader();
  _pendingShellToolUseId = null;
  _orbSetError();
}

// ── Browser Live View Panel ──
const _blp = {
  panel:    null,
  screen:   null,
  placeholder: null,
  urlEl:    null,
  stepEl:   null,
  tsEl:     null,
  lightbox: null,
  lbImg:    null,
  lbUrl:    null,
  lastB64:  null,
  _manuallyHidden: false,

  init(){
    this.panel       = document.getElementById('browser-live-panel');
    this.screen      = document.getElementById('blp-screen');
    this.placeholder = document.getElementById('blp-placeholder');
    this.urlEl       = document.getElementById('blp-url');
    this.stepEl      = document.getElementById('blp-step');
    this.tsEl        = document.getElementById('blp-ts');
    this.lightbox    = document.getElementById('blp-lightbox');
    this.lbImg       = document.getElementById('blp-lightbox-img');
    this.lbUrl       = document.getElementById('blp-lightbox-url');

    document.getElementById('blp-expand-btn')?.addEventListener('click', () => this.openLightbox());
    document.getElementById('blp-close-btn')?.addEventListener('click', () => this.hide(true));
    document.getElementById('blp-lightbox-close')?.addEventListener('click', () => this.closeLightbox());
    document.getElementById('blp-screen-wrap')?.addEventListener('click', () => this.openLightbox());
    document.getElementById('blp-lightbox')?.addEventListener('click', (e) => {
      if(e.target === this.lightbox) this.closeLightbox();
    });
  },

  show(){
    if(!this.panel) return;
    this._manuallyHidden = false;
    this.panel.hidden = false;
  },

  hide(manual = false){
    if(!this.panel) return;
    if(manual) this._manuallyHidden = true;
    this.panel.hidden = true;
    this.closeLightbox();
  },

  update(b64, url, stepText){
    if(!this.panel) return;
    this.lastB64 = b64;
    if(!this._manuallyHidden) this.show();
    // Screen
    if(this.screen){
      this.screen.src = 'data:image/png;base64,' + b64;
      this.screen.hidden = false;
    }
    if(this.placeholder) this.placeholder.style.display = 'none';
    // URL
    if(url && this.urlEl){
      const short = url.replace(/^https?:\/\//, '').slice(0, 60);
      this.urlEl.textContent = short;
      this.urlEl.title = url;
    }
    // Step
    if(stepText && this.stepEl) this.stepEl.textContent = stepText;
    // Timestamp
    if(this.tsEl){
      this.tsEl.textContent = new Date().toLocaleTimeString('vi-VN', {hour:'2-digit', minute:'2-digit', second:'2-digit'});
    }
    // Sync lightbox nếu đang mở
    if(this.lightbox && !this.lightbox.hidden && this.lbImg){
      this.lbImg.src = 'data:image/png;base64,' + b64;
    }
  },

  setStep(text){
    if(this.stepEl) this.stepEl.textContent = text;
  },

  openLightbox(){
    if(!this.lightbox || !this.lastB64) return;
    if(this.lbImg) this.lbImg.src = 'data:image/png;base64,' + this.lastB64;
    if(this.lbUrl && this.urlEl) this.lbUrl.textContent = this.urlEl.title || this.urlEl.textContent;
    this.lightbox.classList.add('open');
  },

  closeLightbox(){
    if(this.lightbox) this.lightbox.classList.remove('open');
  },

  reset(){
    this._manuallyHidden = false;
    this.lastB64 = null;
    if(this.screen){ this.screen.src = ''; this.screen.hidden = true; }
    if(this.placeholder) this.placeholder.style.display = '';
    if(this.urlEl){ this.urlEl.textContent = 'about:blank'; this.urlEl.title = ''; }
    if(this.stepEl) this.stepEl.textContent = '';
    this.hide();
    this.closeLightbox();
  },
};

// Init sau DOM ready — chỉ gọi 1 lần
if(document.readyState === 'loading'){
  document.addEventListener('DOMContentLoaded', () => _blp.init(), {once:true});
} else {
  _blp.init();
}

function _renderBrowserFrame(d){
  // 1. Cập nhật live panel (ưu tiên)
  if(d.base64){
    const st = _execBlockState;
    const toolName = (() => {
      if(!st) return '';
      const tid = d.tool_use_id != null ? String(d.tool_use_id) : null;
      const row = tid ? st.toolMap.get(tid) : (st.order.length ? st.toolMap.get(st.order[st.order.length-1].id) : null);
      return row ? (row.dataset.toolName || '') : '';
    })();
    const stepLabel = formatToolStatusHint(toolName) || toolName.replace(/_/g,' ') || 'Đang điều khiển…';
    _blp.update(d.base64, d.url || '', stepLabel);
  }

  // 2. Cũng render nhỏ trong tool card (giữ nguyên)
  const st = _execBlockState;
  if(!st) return;
  const tid = d.tool_use_id != null ? String(d.tool_use_id) : null;
  let row = tid ? st.toolMap.get(tid) : null;
  if(!row && st.order.length){
    const last = st.order[st.order.length - 1];
    row = st.toolMap.get(last.id);
  }
  if(!row) return;

  row.classList.add('exec-tool-item--open');
  const det = row.querySelector('.exec-tool-detail');
  if(det) det.hidden = false;

  const out = row.querySelector('.exec-tool-out');
  if(!out) return;

  const existing = out.querySelector('.browser-preview-frame');
  if(existing){ existing.remove(); }

  const img = document.createElement('img');
  img.className = 'browser-preview-frame';
  img.alt = 'Browser preview';
  img.src = 'data:image/png;base64,' + d.base64;
  img.title = 'Click để phóng to';
  img.addEventListener('click', () => _blp.openLightbox());

  out.appendChild(img);
  scrollEnd(false);
}

function execResetBlockState(){
  _execBlockState = null;
  _pendingShellToolUseId = null;
}

function execFinalizeBlock(opts){
  const opt = opts || {};
  const st = _execBlockState;
  if(!st) return;
  st.toolMap.forEach(row => {
    if(row.dataset.status === 'running'){
      row.dataset.status = 'error';
      row.classList.add('exec-tool-item--err');
      const dot = row.querySelector('.exec-tool-spine-dot');
      if(dot) dot.dataset.state = 'error';
      const out = row.querySelector('.exec-tool-out');
      if(out && !out.innerHTML.trim()){
        out.innerHTML = '<pre class="exec-tool-out-raw exec-mono exec-tool-out-err">' + esc(opt.interrupted ? 'Đã dừng' : 'Không nhận được kết quả') + '</pre>';
      }
      if(opt.interrupted) st.errors.push({ name: row.dataset.toolName || '', message: 'Đã dừng' });
    }
  });

  const total = st.toolMap.size;
  let ok = 0, err = 0;
  st.toolMap.forEach(row => {
    if(row.dataset.status === 'ok') ok++;
    else if(row.dataset.status === 'error') err++;
  });
  const t0 = st.blockStartMs || Date.now();
  const t1 = st.lastEndMs || Date.now();
  const sec = Math.max(0, (t1 - t0) / 1000);
  const sumEl = st.footerEl && st.footerEl.querySelector('.exec-footer-summary');
  if(sumEl){
    sumEl.innerHTML = ''
      + '<span>Tổng <strong>' + total + '</strong> công cụ</span>'
      + '<span class="exec-footer-sep">·</span>'
      + '<span class="exec-footer-ok">' + ok + ' thành công</span>'
      + '<span class="exec-footer-sep">·</span>'
      + '<span class="exec-footer-bad">' + err + ' lỗi</span>'
      + '<span class="exec-footer-sep">·</span>'
      + '<span>' + (sec >= 10 ? sec.toFixed(1) : sec.toFixed(2)) + 's</span>';
  }
  if(st.footerEl) st.footerEl.hidden = total === 0;
  if(st.errBtn && st.errBody){
    const hasErr = st.errors.length > 0;
    st.errBtn.hidden = !hasErr;
    if(hasErr){
      st.errBody.innerHTML = st.errors.map(e =>
        '<div class="exec-footer-err-item"><strong>' + esc(e.name) + '</strong><pre class="exec-mono">' + esc(e.message) + '</pre></div>'
      ).join('');
    }
  }

  st.root.dataset.execDone = '1';
  execRefreshHeader();
  st.root.classList.add('execution-block--collapsed');
  st.root.dataset.execOpen = '0';
  const header = st.root.querySelector('.exec-block-header');
  if(header){
    header.setAttribute('aria-expanded', 'false');
    const chev = header.querySelector('.exec-block-chev');
    if(chev) chev.innerHTML = ICON_CHEVRON_RIGHT;
  }

  execResetBlockState();
}

function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}

// ── Agent event pills ──
function addEventPill(cls, iconSvg, text){
  const w = wrap();
  w.innerHTML = `<div class="agent-event ${cls}">${iconSvg}<span>${esc(text)}</span></div>`;
  scrollEnd(false);
  return w;
}

// ── Recovery notices — inline trong thread ──
function renderRetryNotice({tool, attempt, maxAttempts, delaySec, reason}){
  const w = wrap();
  w.innerHTML = `<div class="recovery-notice recovery-notice--retry">
    <span class="recovery-dot recovery-dot--amber"></span>
    <span>Retry <strong>${esc(tool)}</strong> lần ${attempt}/${maxAttempts} sau ${delaySec}s</span>
    <span class="recovery-reason">${esc(reason||'')}</span>
    <span class="recovery-countdown" style="--duration:${delaySec}s"></span>
  </div>`;
  scrollEnd(false);
}

function renderFallbackNotice({tool, message}){
  const w = wrap();
  w.innerHTML = `<div class="recovery-notice recovery-notice--fallback">
    <span class="recovery-dot recovery-dot--blue"></span>
    <span>${esc(message||('Fallback: ' + tool))}</span>
  </div>`;
  scrollEnd(false);
}

const EV_ICONS = {
  model:    `<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/></svg>`,
  decompose:`<svg viewBox="0 0 24 24"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>`,
  compress: `<svg viewBox="0 0 24 24"><polyline points="4 14 10 14 10 20"/><polyline points="20 10 14 10 14 4"/><line x1="10" y1="14" x2="21" y2="3"/><line x1="3" y1="21" x2="14" y2="10"/></svg>`,
  retry:    `<svg viewBox="0 0 24 24"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 .49-3.5"/></svg>`,
  verifyOk: `<svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>`,
  verifyFail:`<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>`,
  parallel: `<svg viewBox="0 0 24 24"><line x1="17" y1="10" x2="3" y2="10"/><line x1="21" y1="6" x2="3" y2="6"/><line x1="21" y1="14" x2="3" y2="14"/><line x1="17" y1="18" x2="3" y2="18"/></svg>`,
  risk: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`,
};

// ── Task checklist ──
let _subtaskListEl = null;
let _subtaskItems = [];
let _currentSubtaskIdx = 0;

function addSubtaskList(subtasks){
  _subtaskItems = subtasks;
  _currentSubtaskIdx = 0;
  const w = wrap();
  const checkSvg = `<svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>`;
  const items = subtasks.map((t,i)=>
    `<div class="subtask-item" id="subtask-${i}">
      <div style="position:relative;display:flex;align-items:center">
        <div class="subtask-check">${checkSvg}</div>
        <div class="subtask-spinner"></div>
      </div>
      <span class="subtask-text">${esc(t)}</span>
    </div>`
  ).join('');
  w.innerHTML = `<div class="subtask-list" id="subtask-list-wrap">
    <div class="subtask-list-title">
      <svg viewBox="0 0 24 24"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>
      Kế hoạch thực hiện
    </div>
    ${items}
  </div>`;
  _subtaskListEl = w;
  // Đánh dấu task đầu tiên là running
  setTimeout(()=>setSubtaskRunning(0), 100);
  scrollEnd(false);
}

function setSubtaskRunning(idx){
  if(!_subtaskListEl || idx >= _subtaskItems.length) return;
  // Done tất cả task trước
  for(let i=0; i<idx; i++){
    const el = document.getElementById(`subtask-${i}`);
    if(el){ el.classList.remove('running'); el.classList.add('done'); }
  }
  const el = document.getElementById(`subtask-${idx}`);
  if(el){ el.classList.remove('done'); el.classList.add('running'); }
  _currentSubtaskIdx = idx;
}

function advanceSubtask(){
  if(!_subtaskListEl) return;
  const next = _currentSubtaskIdx + 1;
  if(next < _subtaskItems.length){
    setSubtaskRunning(next);
  } else {
    // Tất cả done
    for(let i=0; i<_subtaskItems.length; i++){
      const el = document.getElementById(`subtask-${i}`);
      if(el){ el.classList.remove('running'); el.classList.add('done'); }
    }
    _subtaskListEl = null;
  }
}

function resetSubtasks(){
  _subtaskListEl = null;
  _subtaskItems = [];
  _currentSubtaskIdx = 0;
}

// ── Tool stream lines ──
let _streamCard = null;
let _streamWrap = null;

function ensureStreamWrap(card){
  if(_streamCard === card && _streamWrap) return _streamWrap;
  _streamCard = card;
  const body = card.querySelector('.tbody');
  const sw = document.createElement('div');
  sw.className = 'tstream-wrap';
  body.appendChild(sw);
  _streamWrap = sw;
  return sw;
}

function appendStreamLine(card, line){
  if(!card) return;
  const sw = ensureStreamWrap(card);
  const d = document.createElement('div');
  d.className = 'tstream-line';
  d.textContent = line;
  sw.appendChild(d);
  sw.scrollTop = sw.scrollHeight;
  scrollEnd(false);
}

// ── Token usage bar ──
function addTokenBar(usage){
  const w = wrap();
  const cost = typeof usage.estimated_cost_usd === 'number' ? usage.estimated_cost_usd : 0;
  const costStr = cost < 0.001 ? '<$0.001' : '$' + cost.toFixed(4);
  const cacheHit = usage.cache_read_tokens > 0;
  const cachePct = usage.input_tokens > 0
    ? Math.round(usage.cache_read_tokens / (usage.input_tokens + usage.cache_read_tokens) * 100)
    : 0;
  const cacheHtml = cacheHit
    ? '<span class="token-seg token-cache-hit"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>' + cachePct + '% cached</span>'
    : '';
  const CTX_MAX = 128000;
  const totalIn = (usage.input_tokens||0) + (usage.cache_read_tokens||0);
  const ctxPct = Math.min(100, Math.round(totalIn / CTX_MAX * 100));
  const ctxClass = ctxPct >= 80 ? 'danger' : ctxPct >= 60 ? 'warn' : '';
  const inTok = (usage.input_tokens||0).toLocaleString();
  const outTok = (usage.output_tokens||0).toLocaleString();
  w.innerHTML = '<div class="token-bar">'
    + '<svg viewBox="0 0 24 24" title="Token usage"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>'
    + '<div class="token-ctx-bar" title="Cửa sổ ngữ cảnh: ' + ctxPct + '% đã dùng (' + totalIn.toLocaleString() + ' / ' + CTX_MAX.toLocaleString() + ' tokens)">'
    + '<div class="token-ctx-fill ' + ctxClass + '" style="width:' + ctxPct + '%"></div></div>'
    + '<span class="token-seg" title="Tokens đầu vào (câu hỏi + lịch sử)"><span>in</span>' + inTok + '</span>'
    + '<span class="token-seg" title="Tokens đầu ra (câu trả lời)"><span>out</span>' + outTok + '</span>'
    + cacheHtml
    + '<span class="token-cost" title="Chi phí ước tính (USD)">' + costStr + '</span>'
    + '</div>';
  scrollEnd(false);
}

// ── File upload ──
const _MAX_FILE_BYTES = 10 * 1024 * 1024; // 10MB
fileInput.addEventListener('change',()=>{
  Array.from(fileInput.files).forEach(file=>{
    if(file.size > _MAX_FILE_BYTES){ showToast(`File "${file.name}" vượt quá 10MB`); return; }
    const reader=new FileReader();
    reader.onload=e=>{
      const data=e.target.result.split(',')[1];
      const previewUrl=file.type.startsWith('image/')?e.target.result:null;
      pendingFiles.push({name:file.name,type:file.type,data,previewUrl});
      renderFilePreviews();
    };
    reader.readAsDataURL(file);
  });
  fileInput.value='';
});

// Dán ảnh từ clipboard vào đính kèm (trước đây không có handler → ảnh “biến mất”)
inputEl.addEventListener('paste', e=>{
  const cd = e.clipboardData;
  if(!cd || !cd.items || !cd.items.length) return;
  let hasImage = false;
  for(let i = 0; i < cd.items.length; i++){
    const it = cd.items[i];
    if(it.kind === 'file' && it.type && it.type.startsWith('image/')){ hasImage = true; break; }
  }
  if(!hasImage) return;
  e.preventDefault();
  const textExtra = cd.getData('text/plain');
  if(textExtra){
    const s = inputEl.selectionStart ?? inputEl.value.length;
    const end = inputEl.selectionEnd ?? inputEl.value.length;
    const v = inputEl.value;
    inputEl.value = v.slice(0, s) + textExtra + v.slice(end);
    const pos = s + textExtra.length;
    try{ inputEl.setSelectionRange(pos, pos); }catch(_){}
    inputEl.dispatchEvent(new Event('input'));
  }
  for(let i = 0; i < cd.items.length; i++){
    const it = cd.items[i];
    if(it.kind !== 'file' || !it.type || !it.type.startsWith('image/')) continue;
    const file = it.getAsFile();
    if(!file) continue;
    const reader = new FileReader();
    reader.onload = ev=>{
      const data = ev.target.result.split(',')[1];
      const previewUrl = ev.target.result;
      pendingFiles.push({
        name: file.name || ('clipboard-' + (file.type || 'image/png').replace(/\//g,'-') + '.png'),
        type: file.type || 'image/png',
        data,
        previewUrl
      });
      renderFilePreviews();
    };
    reader.readAsDataURL(file);
  }
});

function renderFilePreviews(){
  filePrev.innerHTML='';
  if(!pendingFiles.length)return;
  const row=document.createElement('div');row.className='file-chips';
  row.style.cssText='display:flex;flex-wrap:wrap;gap:6px;padding:6px 18px 2px;max-width:820px;margin:0 auto';
  pendingFiles.forEach((f,i)=>{
    const chip=document.createElement('div');chip.className='fchip';
    chip.innerHTML=f.previewUrl
      ?`<img class="fimg" src="${f.previewUrl}"><span>${esc(f.name)}</span><span class="rm" data-oculo="removeFile" data-oculo-arg="${i}"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></span>`
      :`${ICON_FILE}<span>${esc(f.name)}</span><span class="rm" data-oculo="removeFile" data-oculo-arg="${i}"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></span>`;
    row.appendChild(chip);
  });
  filePrev.appendChild(row);
}
function removeFile(i){pendingFiles.splice(i,1);renderFilePreviews()}

function setViewMode(mode){
  currentViewMode = mode === 'control' ? 'control' : 'chat';
  document.body.classList.toggle('control-mode', currentViewMode === 'control');
  const mc = document.getElementById('mode-chat');
  const mo = document.getElementById('mode-control');
  if(mc){ mc.classList.toggle('active', currentViewMode === 'chat'); mc.setAttribute('aria-pressed', currentViewMode === 'chat' ? 'true' : 'false'); }
  if(mo){ mo.classList.toggle('active', currentViewMode === 'control'); mo.setAttribute('aria-pressed', currentViewMode === 'control' ? 'true' : 'false'); }
  localStorage.setItem('ui_view_mode', currentViewMode);
  updateModeIndicator(true);  // animate=true → spring squish
  if(currentViewMode==='control'&&!localStorage.getItem('ux_control_tip_shown')){
    localStorage.setItem('ux_control_tip_shown','1');
    showToast('Chế độ Điều khiển: panel bên phải điều khiển máy thật. ⌘1 = Chat · ⌘2 = Điều khiển.', 7000);
  }
}

// ── Mode indicator — spring squish engine ──
// Uses left+right (not width) so leading/trailing edges animate independently.
// Result: pill "stretches" in the direction of travel, then snaps — like iOS.
let _modeLastLeft = -1;  // track last position to detect direction
let _modeShimmerTimer = null;

function updateModeIndicator(animate){
  const sw  = document.getElementById('mode-switch');
  const ind = document.getElementById('mode-indicator');
  const activeBtn = sw?.querySelector('.mode-btn.active');
  if(!activeBtn || !ind) return;

  const swRect  = sw.getBoundingClientRect();
  const btnRect = activeBtn.getBoundingClientRect();

  // Target values for left and right (both in px relative to switch)
  const PAD    = 3;
  const newLeft  = btnRect.left  - swRect.left  - PAD;
  const newRight = swRect.right  - btnRect.right - PAD;

  // No animation on first render or explicit disable
  if(!animate || _modeLastLeft < 0){
    ind.style.transition = 'none';
    ind.style.left  = newLeft  + 'px';
    ind.style.right = newRight + 'px';
    ind.style.width = '';
    _modeLastLeft = newLeft;
    // force reflow so next transition doesn't jump
    void ind.offsetWidth;
    return;
  }

  _modeLastLeft = newLeft;

  // Một đường cong, hai cạnh cùng duration → chuyển động mượt (kiểu segmented iOS)
  const EASE = 'cubic-bezier(0.4, 0, 0.2, 1)';
  const DUR  = '0.34s';
  ind.style.transition = `left ${DUR} ${EASE}, right ${DUR} ${EASE}`;

  ind.style.left  = newLeft  + 'px';
  ind.style.right = newRight + 'px';
  ind.style.width = '';

  // Shimmer sweep on each switch
  clearTimeout(_modeShimmerTimer);
  ind.classList.remove('sweeping');
  void ind.offsetWidth; // reflow
  ind.classList.add('sweeping');
  _modeShimmerTimer = setTimeout(()=>ind.classList.remove('sweeping'), 400);
}

// ══════════════════════════════════════════
// ── MODE SWITCH — ADVANCED INTERACTIONS ──
// ══════════════════════════════════════════
(function initModeSwitchFX(){
  const sw   = document.getElementById('mode-switch');
  const ind  = document.getElementById('mode-indicator');
  if(!sw || !ind) return;

  let _magneticActive = false; // true while magnetic preview is showing
  let _tiltRAF = null;

  // ── 1. Magnetic hover: pill leans 28% toward hovered inactive button ──
  sw.querySelectorAll('.mode-btn').forEach(btn => {
    btn.addEventListener('mouseenter', () => {
      if(btn.classList.contains('active')) return;
      _magneticActive = true;

      const swRect   = sw.getBoundingClientRect();
      const actBtn   = sw.querySelector('.mode-btn.active');
      if(!actBtn) return;
      const actRect  = actBtn.getBoundingClientRect();
      const hovRect  = btn.getBoundingClientRect();
      const PAD = 3, PULL = 0.28;

      const fromLeft  = actRect.left  - swRect.left  - PAD;
      const fromRight = swRect.right  - actRect.right - PAD;
      const toLeft    = hovRect.left  - swRect.left  - PAD;
      const toRight   = swRect.right  - hovRect.right - PAD;

      ind.style.transition = 'left .28s cubic-bezier(0.4, 0, 0.2, 1), right .28s cubic-bezier(0.4, 0, 0.2, 1)';
      ind.style.left  = (fromLeft  + (toLeft  - fromLeft)  * PULL) + 'px';
      ind.style.right = (fromRight + (toRight - fromRight) * PULL) + 'px';
    });

    btn.addEventListener('mouseleave', () => {
      if(!_magneticActive) return;
      _magneticActive = false;
      const swRect  = sw.getBoundingClientRect();
      const actBtn  = sw.querySelector('.mode-btn.active');
      if(!actBtn) return;
      const actRect = actBtn.getBoundingClientRect();
      const PAD = 3;
      ind.style.transition = 'left .32s cubic-bezier(0.4, 0, 0.2, 1), right .32s cubic-bezier(0.4, 0, 0.2, 1)';
      ind.style.left  = (actRect.left  - swRect.left  - PAD) + 'px';
      ind.style.right = (swRect.right  - actRect.right - PAD) + 'px';
    });
  });

  // ── 2. Ripple on click inside the pill ──
  sw.addEventListener('mousedown', e => {
    const rect = ind.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height) * 2.2;
    const r = document.createElement('span');
    r.className = 'mode-ripple';
    r.style.cssText = `width:${size}px;height:${size}px;`
      + `left:${e.clientX - rect.left - size/2}px;`
      + `top:${e.clientY  - rect.top  - size/2}px`;
    ind.appendChild(r);
    setTimeout(() => r.remove(), 600);
  });

  // ── 3. 3D tilt on hover (subtle perspective) ──
  const MAX_TILT_Y = 5, MAX_TILT_X = 3;
  sw.addEventListener('mousemove', e => {
    if(_tiltRAF) return; // throttle to rAF
    _tiltRAF = requestAnimationFrame(() => {
      _tiltRAF = null;
      const rect = sw.getBoundingClientRect();
      const cx = (e.clientX - rect.left) / rect.width  - 0.5; // -0.5 … 0.5
      const cy = (e.clientY - rect.top)  / rect.height - 0.5;
      sw.style.transform = `perspective(280px) rotateY(${cx*MAX_TILT_Y*2}deg) rotateX(${-cy*MAX_TILT_X*2}deg) scale(1.01)`;
    });
  });
  sw.addEventListener('mouseleave', () => {
    if(_tiltRAF){ cancelAnimationFrame(_tiltRAF); _tiltRAF=null; }
    sw.style.transition = 'transform .5s cubic-bezier(.34,1.56,.64,1)';
    sw.style.transform  = '';
    setTimeout(() => sw.style.transition = '', 500);
  });
  sw.addEventListener('mousedown', () => {
    sw.style.transform = 'perspective(280px) scale(.96)';
  });
  sw.addEventListener('mouseup', () => {
    sw.style.transform = '';
  });
})();

// ── Voice input ──
let recognition=null, isRecording=false;
const voiceBtn=document.getElementById('voice-btn');

function toggleVoice(){
  if(!('webkitSpeechRecognition' in window||'SpeechRecognition' in window)){
    showToast('Trình duyệt không hỗ trợ nhập giọng. Dùng Chrome hoặc Edge.', 4500);
    return;
  }
  if(isRecording){recognition?.stop();return}
  const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
  recognition=new SR();
  recognition.lang='vi-VN';recognition.continuous=false;recognition.interimResults=true;
  recognition.onstart=()=>{isRecording=true;voiceBtn.classList.add('recording');voiceBtn.innerHTML=ICON_MIC_OFF};
  recognition.onresult=e=>{
    const transcript=Array.from(e.results).map(r=>r[0].transcript).join('');
    inputEl.value=transcript;inputEl.dispatchEvent(new Event('input'));
  };
  recognition.onend=()=>{isRecording=false;voiceBtn.classList.remove('recording');voiceBtn.innerHTML=ICON_MIC};
  recognition.onerror=()=>{isRecording=false;voiceBtn.classList.remove('recording');voiceBtn.innerHTML=ICON_MIC};
  recognition.start();
}

// ── Abort ──
let _currentSendAbort = null;

async function abortStream(){
  if(!currentStreamId)return;
  // Hủy fetch ngay lập tức từ client
  if(_currentSendAbort){ try{ _currentSendAbort.abort(); }catch{} _currentSendAbort=null; }
  // Đồng thời báo server dừng
  fetch(`/abort/${currentStreamId}`,{method:'POST'}).catch(()=>{});
}

// ═══════════════════════════════════════════════════════════════
// ACTIVITY SIDEBAR — monitors, streams, schedules
// ═══════════════════════════════════════════════════════════════
const ActivitySidebar = {
  isOpen: false,
  pollInterval: null,
  pollDelay: 10000,
  elapsedInterval: null,
  pollCount: 0,
  streamStartTimes: Object.create(null),
  lastData: { streams: [], monitors: {}, schedules: {}, events: [] },
  lastSig: { streams: '', monitors: '', schedules: '', events: '' },

  init(){
    const open = localStorage.getItem('oculo_sidebar_open') === '1';
    if(open) this.applyOpenState(true, false);
    document.getElementById('activity-sidebar')?.addEventListener('click', (ev) => {
      const btn = ev.target.closest('[data-as-action]');
      if(!btn) return;
      const raw = btn.getAttribute('data-as-id');
      let id = raw || '';
      if(raw) try { id = decodeURIComponent(raw); } catch(_) { id = raw; }
      const act = btn.getAttribute('data-as-action');
      if(act === 'abort' && id) this.abortStream(id);
      else if(act === 'del-mon' && id) this.deleteMonitor(id);
      else if(act === 'del-sched' && id) this.deleteScheduleJob(id);
    });
  },

  applyOpenState(open, persist){
    this.isOpen = !!open;
    document.body.classList.toggle('activity-sidebar-open', this.isOpen);
    const panel = document.getElementById('activity-sidebar');
    if(panel) panel.setAttribute('aria-hidden', this.isOpen ? 'false' : 'true');
    const t = document.getElementById('activity-sidebar-toggle');
    if(t){
      t.setAttribute('aria-expanded', this.isOpen ? 'true' : 'false');
    }
    if(persist) localStorage.setItem('oculo_sidebar_open', this.isOpen ? '1' : '0');
    if(this.isOpen){
      this.startPolling();
      this.startElapsedTicker();
    } else {
      this.stopPolling();
      this.stopElapsedTicker();
    }
    if(!this.isOpen) this.updateBadge();
  },

  toggle(){
    this.applyOpenState(!this.isOpen, true);
  },

  startPolling(){
    this.stopPolling();
    this.poll();
    this.pollInterval = setInterval(() => this.poll(), this.pollDelay);
  },

  stopPolling(){
    if(this.pollInterval){ clearInterval(this.pollInterval); this.pollInterval = null; }
  },

  startElapsedTicker(){
    this.stopElapsedTicker();
    this.elapsedInterval = setInterval(() => this._tickElapsed(), 1000);
  },

  stopElapsedTicker(){
    if(this.elapsedInterval){ clearInterval(this.elapsedInterval); this.elapsedInterval = null; }
  },

  _tickElapsed(){
    if(!this.isOpen) return;
    const list = document.getElementById('as-list-streams');
    if(!list) return;
    list.querySelectorAll('.as-item[data-stream-id]').forEach((row) => {
      const sid = row.getAttribute('data-stream-id');
      const el = row.querySelector('[data-as-elapsed]');
      if(sid && el) el.textContent = this.getElapsed(sid);
    });
  },

  async _fetchJsonOk(url){
    try{
      const r = await fetch(url);
      if(!r.ok) return null;
      return await r.json();
    } catch(e){
      console.warn('ActivitySidebar fetch', url, e);
      return null;
    }
  },

  async poll(){
    this.pollCount++;
    const fetchSched = (this.pollCount % 3) === 1;
    const health = await this._fetchJsonOk('/health');
    const monitors = await this._fetchJsonOk('/monitors');
    const evList = await this._fetchJsonOk('/monitors/events');
    let schedules = this.lastData.schedules;
    if(fetchSched){
      const z = await this._fetchJsonOk('/schedules');
      if(z && typeof z === 'object') schedules = z;
    }
    const hadAny = !!(health || monitors || evList !== null);
    const h = health && typeof health === 'object' ? health : { open_streams: [] };
    const streams = Array.isArray(h.open_streams) ? h.open_streams : [];
    for(const sid of streams){
      if(!this.streamStartTimes[sid]) this.streamStartTimes[sid] = Date.now();
    }
    Object.keys(this.streamStartTimes).forEach((sid) => {
      if(!streams.includes(sid)) delete this.streamStartTimes[sid];
    });
    this.render({
      streams,
      monitors: monitors && typeof monitors === 'object' ? monitors : {},
      schedules: schedules && typeof schedules === 'object' ? schedules : {},
      events: Array.isArray(evList) ? evList : [],
    });
    this.updateLastUpdate(hadAny);
  },

  updateLastUpdate(ok){
    const el = document.getElementById('as-last-update');
    if(!el) return;
    el.classList.toggle('as-last-update--error', !ok);
    if(ok){
      const now = new Date();
      el.textContent = 'Cập nhật lúc ' + now.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' });
      el.removeAttribute('title');
    } else {
      el.textContent = 'Chưa tải được dữ liệu — nhấn Refresh';
      el.title = 'Không kết nối được /health hoặc /monitors (kiểm tra server Oculo đang chạy)';
    }
  },

  updateBadge(){
    const badge = document.getElementById('activity-sidebar-badge');
    if(!badge) return;
    const streamSet = new Set(this.lastData.streams || []);
    Object.keys(this.streamStartTimes).forEach((id) => streamSet.add(id));
    const nStr = streamSet.size;
    const mons = this.lastData.monitors || {};
    const scheds = this.lastData.schedules || {};
    const nMon = Object.keys(mons).length;
    const nSched = Object.keys(scheds).length;
    const total = nStr + nMon + nSched;
    if(total < 1){
      badge.hidden = true;
      return;
    }
    badge.hidden = false;
    badge.textContent = String(Math.min(99, total));
    const hasStream = (this.lastData.streams || []).length > 0 || Object.keys(this.streamStartTimes).length > 0;
    badge.classList.toggle('is-stream', hasStream);
  },

  render(data){
    this.lastData = {
      streams: data.streams || [],
      monitors: data.monitors || {},
      schedules: data.schedules || {},
      events: data.events || [],
    };
    const sigS = (this.lastData.streams || []).slice().sort().join('\n');
    const sigM = JSON.stringify(this.lastData.monitors);
    const sigZ = JSON.stringify(this.lastData.schedules);
    const sigE = JSON.stringify(this.lastData.events);
    if(sigS !== this.lastSig.streams) this.renderStreams(this.lastData.streams);
    if(sigM !== this.lastSig.monitors || sigE !== this.lastSig.events) this.renderMonitors(this.lastData.monitors);
    if(sigZ !== this.lastSig.schedules) this.renderSchedules(this.lastData.schedules);
    this.lastSig = { streams: sigS, monitors: sigM, schedules: sigZ, events: sigE };
    this.updateBadge();
  },

  _monitorLabel(type){
    if(type === 'file') return 'Theo dõi file';
    if(type === 'calendar') return 'Theo dõi lịch';
    if(type === 'system') return 'Theo dõi hệ thống';
    return String(type || 'Monitor');
  },

  _monitorTarget(m){
    if(!m || typeof m !== 'object') return '—';
    if(m.type === 'file') return m.path || '—';
    if(m.type === 'calendar') return `Mỗi ${m.interval_minutes || 5} phút`;
    if(m.type === 'system') return `CPU/RAM · ngưỡng ${m.cpu_threshold ?? '—'}/${m.mem_threshold ?? '—'}%`;
    return '—';
  },

  _eventsForWatch(events, wid){
    return events.filter((e) => {
      const d = e && e.data;
      return d && (d.watch_id === wid || (typeof d === 'object' && d.watch_id === wid));
    });
  },

  renderStreams(streams){
    const list = document.getElementById('as-list-streams');
    const countEl = document.getElementById('as-count-streams');
    if(countEl) countEl.textContent = String(streams.length);
    if(!list) return;
    if(!streams.length){
      list.innerHTML = '<div class="as-empty">Không có gì đang chạy</div>';
      return;
    }
    list.innerHTML = streams.map((sid) => {
      const short = sid.length > 8 ? sid.slice(0, 8) + '…' : sid;
      const el = this.getElapsed(sid);
      const enc = encodeURIComponent(sid);
      return `<div class="as-item" data-stream-id="${esc(sid)}">`
        + `<div class="as-item-main">`
        + `<div class="as-item-title">Stream ${esc(short)}</div>`
        + `<div class="as-item-sub">Đang chạy · <span data-as-elapsed>${esc(el)}</span></div>`
        + `</div>`
        + `<div class="as-item-actions">`
        + `<button type="button" class="btn btn-ghost btn--compact" data-as-action="abort" data-as-id="${enc}">Dừng</button>`
        + `</div></div>`;
    }).join('');
  },

  renderMonitors(monitors){
    const list = document.getElementById('as-list-monitors');
    const countEl = document.getElementById('as-count-monitors');
    const keys = Object.keys(monitors);
    if(countEl) countEl.textContent = String(keys.length);
    if(!list) return;
    if(!keys.length){
      list.innerHTML = '<div class="as-empty">Không có gì đang chạy</div>';
      return;
    }
    const events = this.lastData.events || [];
    list.innerHTML = keys.map((id) => {
      const m = monitors[id];
      const label = this._monitorLabel(m && m.type);
      const target = esc(this._monitorTarget(m));
      const evs = this._eventsForWatch(events, id);
      let line2 = '— · 0 sự kiện';
      if(evs.length){
        const last = evs[evs.length - 1];
        const ts = last.ts ? new Date(last.ts) : null;
        let ago = '—';
        if(ts && !isNaN(ts.getTime())){
          const sec = Math.max(0, Math.floor((Date.now() - ts.getTime()) / 1000));
          ago = sec < 60 ? `${sec}s trước` : sec < 3600 ? `${Math.floor(sec / 60)}p trước` : `${Math.floor(sec / 3600)}h trước`;
        }
        line2 = `${ago} · ${evs.length} sự kiện`;
      }
      return `<div class="as-item" data-monitor-id="${esc(id)}">`
        + `<div class="as-item-main">`
        + `<div class="as-item-title">${esc(label)} · ${target}</div>`
        + `<div class="as-item-sub">${esc(line2)}</div>`
        + `</div>`
        + `<div class="as-item-actions">`
        + `<button type="button" class="btn btn-ghost btn--compact" data-as-action="del-mon" data-as-id="${encodeURIComponent(id)}">Xóa</button>`
        + `</div></div>`;
    }).join('');
  },

  renderSchedules(schedules){
    const list = document.getElementById('as-list-schedules');
    const countEl = document.getElementById('as-count-schedules');
    const keys = Object.keys(schedules);
    if(countEl) countEl.textContent = String(keys.length);
    if(!list) return;
    if(!keys.length){
      list.innerHTML = '<div class="as-empty">Không có gì đang chạy</div>';
      return;
    }
    list.innerHTML = keys.map((id) => {
      const job = schedules[id] || {};
      const title = esc(_schedTitle(job.task || ''));
      const { label, countdown } = _schedTimeInfo(job);
      const sub = countdown
        ? `Chạy lúc ${esc(label)} · ${esc(countdown)}`
        : `Chạy lúc ${esc(label)}`;
      return `<div class="as-item" data-schedule-id="${esc(id)}">`
        + `<div class="as-item-main">`
        + `<div class="as-item-title">${title || esc(id)}</div>`
        + `<div class="as-item-sub">${sub}</div>`
        + `</div>`
        + `<div class="as-item-actions">`
        + `<button type="button" class="btn btn-ghost btn--compact" data-as-action="del-sched" data-as-id="${encodeURIComponent(id)}">Hủy</button>`
        + `</div></div>`;
    }).join('');
  },

  async abortStream(streamId){
    if(!confirm('Dừng stream này?')) return;
    await fetch(`/abort/${encodeURIComponent(streamId)}`, { method: 'POST' });
    delete this.streamStartTimes[streamId];
    await this.poll();
  },

  async deleteMonitor(monitorId){
    if(!confirm('Xóa monitor này?')) return;
    await fetch(`/monitors/${encodeURIComponent(monitorId)}`, { method: 'DELETE' });
    await this.poll();
  },

  async deleteScheduleJob(jobId){
    if(!confirm('Hủy lịch này?')) return;
    await fetch(`/schedules/${encodeURIComponent(jobId)}`, { method: 'DELETE' });
    await this.poll();
  },

  trackStream(streamId){
    if(streamId) this.streamStartTimes[streamId] = Date.now();
    this.updateBadge();
  },

  untrackStream(streamId){
    if(streamId) delete this.streamStartTimes[streamId];
    this.updateBadge();
  },

  getElapsed(streamId){
    const start = this.streamStartTimes[streamId];
    if(!start) return '—';
    const s = Math.floor((Date.now() - start) / 1000);
    return Math.floor(s / 60) + ':' + String(s % 60).padStart(2, '0');
  },
};

function toggleActivitySidebar(){ ActivitySidebar.toggle(); }
function activitySidebarRefresh(){ ActivitySidebar.poll(); }

// ── Ambient floating widget (task dài / tab khác) ──
const AmbientWidget = {
  // Widget này hữu ích khi chạy dạng native window, nhưng với web UI nhiều người thấy thừa.
  // Mặc định tắt hoàn toàn. Nếu muốn bật lại, set localStorage: ux_ambient_widget=1 rồi reload.
  disabled: (localStorage.getItem('ux_ambient_widget') !== '1'),
  el: null,
  streamId: null,
  sseActive: false,
  state: 'hidden',
  toolCallCount: 0,
  startTime: null,
  lastTool: null,
  timerInterval: null,
  autoTriggerTimer: null,
  minimizeAfterFocusTimer: null,
  doneHideTimer: null,
  wasEverVisible: false,
  minimized: false,
  dragging: false,
  dragStart: null,
  lastErrorMessage: '',
  heavyTools: ['run_shell', 'browser_navigate', 'browser_evaluate', 'screenshot_and_analyze', 'extract_data'],
  CORNER_MARGIN: 24,
  LS_POS: 'oculo_widget_pos',
  SS_MIN: 'oculo_ambient_min',

  ensureDom(){
    if(this.disabled) return;
    if(this.el) return;
    const w = document.createElement('div');
    w.id = 'ambient-widget';
    w.className = 'ambient-widget ambient-hidden';
    w.setAttribute('role', 'status');
    w.innerHTML = ''
      + '<div class="ambient-widget-inner">'
      +   '<div class="ambient-widget-drag">'
      +     '<button type="button" class="ambient-min-btn" aria-label="Thu gọn">−</button>'
      +     '<span class="ambient-dot" data-role="dot"></span>'
      +     '<span class="ambient-title" data-role="title">Oculo</span>'
      +   '</div>'
      +   '<div class="ambient-body" data-role="body">'
      +     '<div class="ambient-step" data-role="step">Chờ agent...</div>'
      +     '<div class="ambient-timer" data-role="timer">0:00</div>'
      +     '<div class="ambient-actions" data-role="actions">'
      +       '<button type="button" class="ambient-btn ambient-btn-back">Quay lại</button>'
      +       '<button type="button" class="ambient-btn ambient-btn-stop">Dừng</button>'
      +     '</div>'
      +     '<div class="ambient-done-line" data-role="doneLine" hidden></div>'
      +     '<div class="ambient-err-line" data-role="errLine" hidden></div>'
      +     '<button type="button" class="ambient-btn ambient-btn-detail" data-role="detailBtn" hidden>Xem chi tiết</button>'
      +   '</div>'
      + '</div>'
      + '<div class="ambient-minimized-view" data-role="minView" hidden>'
      +   '<span class="ambient-dot ambient-dot--sm" data-role="minDot"></span>'
      +   '<span class="ambient-min-timer" data-role="minTimer">0:00</span>'
      + '</div>';
    document.body.appendChild(w);
    this.el = w;

    w.querySelector('.ambient-min-btn').addEventListener('click', (e) => {
      e.stopPropagation();
      this.toggleMinimize(true);
    });
    w.querySelector('.ambient-btn-back').addEventListener('click', () => this.focusMain());
    w.querySelector('.ambient-btn-stop').addEventListener('click', () => this.abort());
    w.querySelector('[data-role="detailBtn"]').addEventListener('click', () => this.focusError());
    w.querySelector('[data-role="minView"]').addEventListener('click', () => this.toggleMinimize(false));
    w.addEventListener('transitionend', (e) => {
      if(e.propertyName === 'opacity' && this.state === 'hidden' && w.classList.contains('ambient-hidden')){
        w.setAttribute('aria-hidden', 'true');
      }
    });
    w.addEventListener('click', (e) => {
      if(AmbientWidget.state !== 'done') return;
      if(e.target.closest('button')) return;
      AmbientWidget.focusMain();
    });

    this._bindDrag();
    if(sessionStorage.getItem(this.SS_MIN) === '1') this.minimized = true;
  },

  _bindDrag(){
    const h = this.el.querySelector('.ambient-widget-drag');
    if(!h || h.dataset.dragBound) return;
    h.dataset.dragBound = '1';
    let ox = 0, oy = 0, sl = 0, st = 0, rw = 0, rh = 0;
    const onMove = (e) => {
      if(!this.dragging || !this.el) return;
      e.preventDefault();
      let nx = sl + (e.clientX - ox);
      let ny = st + (e.clientY - oy);
      const vw = window.innerWidth, vh = window.innerHeight;
      nx = Math.max(4, Math.min(nx, vw - rw - 4));
      ny = Math.max(4, Math.min(ny, vh - rh - 4));
      this.el.style.left = nx + 'px';
      this.el.style.top = ny + 'px';
      this.el.style.right = 'auto';
      this.el.style.bottom = 'auto';
    };
    const onUp = () => {
      if(!this.dragging) return;
      this.dragging = false;
      document.removeEventListener('mousemove', onMove);
      document.removeEventListener('mouseup', onUp);
      this._snapToNearestCorner();
    };
    h.addEventListener('mousedown', (e) => {
      if(e.target.closest('.ambient-min-btn')) return;
      if(this.state !== 'running' && this.state !== 'error') return;
      if(this.minimized) return;
      const r = this.el.getBoundingClientRect();
      ox = e.clientX; oy = e.clientY;
      sl = r.left; st = r.top;
      rw = r.width; rh = r.height;
      this.dragging = true;
      document.addEventListener('mousemove', onMove);
      document.addEventListener('mouseup', onUp);
      e.preventDefault();
    });
  },

  _snapToNearestCorner(){
    if(!this.el) return;
    const r = this.el.getBoundingClientRect();
    const cx = r.left + r.width / 2;
    const cy = r.top + r.height / 2;
    const vw = window.innerWidth, vh = window.innerHeight;
    const m = this.CORNER_MARGIN;
    const corners = [
      { id: 'tl', x: m + r.width / 2, y: m + r.height / 2 },
      { id: 'tr', x: vw - m - r.width / 2, y: m + r.height / 2 },
      { id: 'bl', x: m + r.width / 2, y: vh - m - r.height / 2 },
      { id: 'br', x: vw - m - r.width / 2, y: vh - m - r.height / 2 },
    ];
    let best = corners[0], bestD = Infinity;
    for(const c of corners){
      const d = Math.hypot(cx - c.x, cy - c.y);
      if(d < bestD){ bestD = d; best = c; }
    }
    localStorage.setItem(this.LS_POS, best.id);
    this._applyCorner(best.id);
  },

  _applyCorner(cornerId){
    if(!this.el) return;
    const el = this.el;
    el.style.left = el.style.right = el.style.top = el.style.bottom = 'auto';
    const m = this.CORNER_MARGIN;
    if(cornerId === 'br'){ el.style.bottom = m + 'px'; el.style.right = m + 'px'; }
    else if(cornerId === 'bl'){ el.style.bottom = m + 'px'; el.style.left = m + 'px'; }
    else if(cornerId === 'tr'){ el.style.top = m + 'px'; el.style.right = m + 'px'; }
    else { el.style.top = m + 'px'; el.style.left = m + 'px'; }
  },

  _loadCorner(){
    this.ensureDom();
    const c = localStorage.getItem(this.LS_POS) || 'br';
    this._applyCorner(['tl','tr','bl','br'].includes(c) ? c : 'br');
  },

  _clearTimers(){
    if(this.autoTriggerTimer){ clearTimeout(this.autoTriggerTimer); this.autoTriggerTimer = null; }
    if(this.minimizeAfterFocusTimer){ clearTimeout(this.minimizeAfterFocusTimer); this.minimizeAfterFocusTimer = null; }
    if(this.doneHideTimer){ clearTimeout(this.doneHideTimer); this.doneHideTimer = null; }
    if(this.timerInterval){ clearInterval(this.timerInterval); this.timerInterval = null; }
  },

  reset(){
    if(this.disabled) return;
    this._clearTimers();
    this.streamId = null;
    this.sseActive = false;
    this.toolCallCount = 0;
    this.startTime = null;
    this.lastTool = null;
    this.wasEverVisible = false;
    this.lastErrorMessage = '';
    if(this.el){
      this.el.className = 'ambient-widget ambient-hidden';
      this.el.classList.remove('ambient-state-running','ambient-state-done','ambient-state-error','ambient-animate-done','ambient-minimized');
      this.el.querySelector('[data-role="body"]').hidden = false;
      this.el.querySelector('[data-role="minView"]').hidden = true;
      this.el.querySelector('[data-role="doneLine"]').hidden = true;
      this.el.querySelector('[data-role="errLine"]').hidden = true;
      this.el.querySelector('[data-role="detailBtn"]').hidden = true;
      this.el.querySelector('[data-role="actions"]').hidden = false;
    }
    this.state = 'hidden';
    this.minimized = false;
  },

  beginStream(sid){
    if(this.disabled) return;
    this.ensureDom();
    this._clearTimers();
    this.stopTicker();
    this.toolCallCount = 0;
    this.lastTool = null;
    this.wasEverVisible = false;
    this.lastErrorMessage = '';
    if(this.el){
      this.el.className = 'ambient-widget ambient-hidden';
      this.el.classList.remove('ambient-state-running','ambient-state-done','ambient-state-error','ambient-animate-done','ambient-minimized');
      const body = this.el.querySelector('[data-role="body"]');
      if(body) body.hidden = false;
      this.el.querySelector('[data-role="minView"]').hidden = true;
      this.el.querySelector('[data-role="doneLine"]').hidden = true;
      this.el.querySelector('[data-role="errLine"]').hidden = true;
      this.el.querySelector('[data-role="detailBtn"]').hidden = true;
      this.el.querySelector('[data-role="actions"]').hidden = false;
    }
    this.state = 'hidden';
    this.streamId = sid;
    this.sseActive = true;
    this.startTime = Date.now();
    this.autoTriggerTimer = setTimeout(() => {
      if(this.sseActive && this.state === 'hidden'){
        this.setState('running');
      }
    }, 8000);
    this._loadCorner();
  },

  endStreamCleanup(){
    if(this.disabled) return;
    this.sseActive = false;
    if(this.autoTriggerTimer){ clearTimeout(this.autoTriggerTimer); this.autoTriggerTimer = null; }
  },

  onToolUse(toolName){
    if(this.disabled) return;
    this.toolCallCount++;
    this.lastTool = toolName;
    if(!this.sseActive) return;
    const heavy = this.heavyTools.includes(toolName);
    const second = this.toolCallCount >= 2;
    if(heavy || second){
      if(this.autoTriggerTimer){ clearTimeout(this.autoTriggerTimer); this.autoTriggerTimer = null; }
      if(this.state === 'hidden') this.setState('running');
    }
    if(this.state === 'running') this.updateRunningUI();
  },

  updateRunningUI(){
    if(this.disabled) return;
    this.ensureDom();
    const step = this.el.querySelector('[data-role="step"]');
    const name = this.lastTool || 'agent';
    if(step) step.textContent = name + ' · bước ' + this.toolCallCount + '/?';
    const title = this.el.querySelector('[data-role="title"]');
    if(title) title.textContent = 'Oculo đang chạy...';
  },

  updateTimerLabel(){
    if(this.disabled) return;
    if(!this.startTime) return;
    const sec = Math.floor((Date.now() - this.startTime) / 1000);
    const mm = Math.floor(sec / 60);
    const ss = sec % 60;
    const s = mm + ':' + (ss < 10 ? '0' : '') + ss;
    const t = this.el && this.el.querySelector('[data-role="timer"]');
    const mt = this.el && this.el.querySelector('[data-role="minTimer"]');
    if(t) t.textContent = s;
    if(mt) mt.textContent = s;
  },

  startTicker(){
    if(this.disabled) return;
    if(this.timerInterval) clearInterval(this.timerInterval);
    this.updateTimerLabel();
    this.timerInterval = setInterval(() => this.updateTimerLabel(), 1000);
  },

  stopTicker(){
    if(this.disabled) return;
    if(this.timerInterval){ clearInterval(this.timerInterval); this.timerInterval = null; }
  },

  setState(next, extra){
    if(this.disabled) return;
    this.ensureDom();
    this.el.classList.remove('ambient-hidden','ambient-state-running','ambient-state-done','ambient-state-error','ambient-animate-done');
    this.el.removeAttribute('aria-hidden');
    if(next === 'running'){
      this.el.classList.remove('ambient-hidden');
      this.state = 'running';
      this.wasEverVisible = true;
      this.el.classList.add('ambient-state-running');
      const dot = this.el.querySelector('[data-role="dot"]');
      if(dot){ dot.className = 'ambient-dot ambient-dot--running'; }
      const minDot = this.el.querySelector('[data-role="minDot"]');
      if(minDot){ minDot.className = 'ambient-dot ambient-dot--sm ambient-dot--running'; }
      const title = this.el.querySelector('[data-role="title"]');
      if(title) title.textContent = 'Oculo đang chạy...';
      this.el.querySelector('[data-role="body"]').hidden = false;
      this.el.querySelector('[data-role="actions"]').hidden = false;
      this.el.querySelector('[data-role="doneLine"]').hidden = true;
      this.el.querySelector('[data-role="errLine"]').hidden = true;
      this.el.querySelector('[data-role="detailBtn"]').hidden = true;
      this.updateRunningUI();
      this.startTicker();
      if(sessionStorage.getItem(this.SS_MIN) === '1') this.applyMinimizeClass(true);
      else this.applyMinimizeClass(false);
    } else if(next === 'done'){
      this.state = 'done';
      this.stopTicker();
      this.el.classList.remove('ambient-hidden');
      this.el.classList.add('ambient-state-done');
      const dot = this.el.querySelector('[data-role="dot"]');
      if(dot){ dot.className = 'ambient-dot ambient-dot--done'; }
      const title = this.el.querySelector('[data-role="title"]');
      if(title) title.textContent = 'Oculo xong rồi';
      const dur = extra && extra.durationSec != null ? extra.durationSec : 0;
      const cnt = extra && extra.toolCount != null ? extra.toolCount : this.toolCallCount;
      const line = this.el.querySelector('[data-role="doneLine"]');
      if(line){
        line.hidden = false;
        line.textContent = cnt + ' tool · ' + dur;
      }
      this.el.querySelector('[data-role="step"]').textContent = '';
      this.el.querySelector('[data-role="timer"]').textContent = '';
      this.el.querySelector('[data-role="actions"]').hidden = true;
      this.el.querySelector('[data-role="body"]').hidden = false;
      this.applyMinimizeClass(false);
      this.el.classList.add('ambient-animate-done');
      this.doneHideTimer = setTimeout(() => this.hide(), 4400);
    } else if(next === 'error'){
      this.state = 'error';
      this.stopTicker();
      this.el.classList.remove('ambient-hidden');
      this.el.classList.add('ambient-state-error');
      const dot = this.el.querySelector('[data-role="dot"]');
      if(dot){ dot.className = 'ambient-dot ambient-dot--error'; }
      const title = this.el.querySelector('[data-role="title"]');
      if(title) title.textContent = 'Oculo gặp lỗi';
      const errLine = this.el.querySelector('[data-role="errLine"]');
      if(errLine){
        errLine.hidden = false;
        errLine.textContent = (extra && extra.tool ? extra.tool + ' — ' : '') + (extra && extra.message ? String(extra.message).slice(0, 80) : 'Lỗi');
      }
      this.el.querySelector('[data-role="actions"]').hidden = true;
      this.el.querySelector('[data-role="detailBtn"]').hidden = false;
      this.el.querySelector('[data-role="doneLine"]').hidden = true;
    }
  },

  applyMinimizeClass(on){
    if(this.disabled) return;
    this.minimized = !!on;
    if(!this.el) return;
    this.el.classList.toggle('ambient-minimized', this.minimized);
    this.el.querySelector('[data-role="body"]').hidden = this.minimized;
    this.el.querySelector('[data-role="minView"]').hidden = !this.minimized;
    if(this.minimized) sessionStorage.setItem(this.SS_MIN, '1');
    else sessionStorage.removeItem(this.SS_MIN);
  },

  toggleMinimize(forceMin){
    if(this.disabled) return;
    if(this.state !== 'running' && this.state !== 'error') return;
    const next = forceMin === true ? true : forceMin === false ? false : !this.minimized;
    this.applyMinimizeClass(next);
  },

  minimize(){
    this.toggleMinimize(true);
  },

  hide(){
    if(this.disabled) return;
    this._clearTimers();
    this.stopTicker();
    if(!this.el) return;
    this.el.classList.add('ambient-hidden');
    this.el.classList.remove('ambient-state-running','ambient-state-done','ambient-state-error','ambient-animate-done','ambient-minimized');
    this.state = 'hidden';
    this.el.querySelector('[data-role="minView"]').hidden = true;
    this.el.querySelector('[data-role="body"]').hidden = false;
  },

  focusMain(){
    this.hide();
    msgsEl && msgsEl.lastElementChild && msgsEl.lastElementChild.scrollIntoView({ behavior: 'smooth', block: 'end' });
    inputEl && inputEl.focus({ preventScroll: true });
  },

  focusError(){
    const row = document.querySelector('.chat-error-row:last-of-type') || document.querySelector('.chat-error-bubble');
    if(row) row.scrollIntoView({ behavior: 'smooth', block: 'center' });
    this.hide();
    inputEl && inputEl.focus({ preventScroll: true });
  },

  async abort(){
    const sid = this.streamId || currentStreamId;
    if(sid){
      try{
        await fetch('/abort/' + encodeURIComponent(sid), { method: 'POST' });
      }catch(_){}
    }
    showToast('■ Đã dừng agent');
    this.hide();
  },

  onDone(){
    this.endStreamCleanup();
    if(!this.wasEverVisible){
      this.reset();
      return;
    }
    const durSec = this.startTime ? Math.max(0, (Date.now() - this.startTime) / 1000) : 0;
    const dStr = durSec >= 10 ? durSec.toFixed(1) : durSec.toFixed(2);
    this.setState('done', { toolCount: this.toolCallCount, durationSec: dStr });
    fetch('/notify-client', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: 'Oculo xong rồi',
        body: 'Đã chạy ' + this.toolCallCount + ' tool trong ' + dStr + ' giây',
      }),
    }).catch(() => {});
  },

  onStreamError(message){
    this.endStreamCleanup();
    this.lastErrorMessage = String(message || '');
    if(!this.wasEverVisible && this.toolCallCount === 0){
      this.reset();
      return;
    }
    this.setState('error', { tool: this.lastTool || '', message: this.lastErrorMessage });
  },

  onInterrupted(){
    this.endStreamCleanup();
    if(this.state === 'hidden' && !this.wasEverVisible){
      this.reset();
      return;
    }
    this.hide();
  },
};

(function initAmbientWidgetChrome(){
  function onVis(){
    if(AmbientWidget.minimizeAfterFocusTimer){
      clearTimeout(AmbientWidget.minimizeAfterFocusTimer);
      AmbientWidget.minimizeAfterFocusTimer = null;
    }
    if(document.hidden) return;
    if(AmbientWidget.state !== 'running' || !AmbientWidget.wasEverVisible) return;
    AmbientWidget.minimizeAfterFocusTimer = setTimeout(() => {
      if(AmbientWidget.state === 'running' && !document.hidden){
        AmbientWidget.minimize();
      }
    }, 3000);
  }
  document.addEventListener('visibilitychange', onVis);
  window.addEventListener('resize', () => {
    if(AmbientWidget.el && !AmbientWidget.dragging) AmbientWidget._loadCorner();
  });
})();

// ── Send ──


// #3 Resume from interrupted point
function _resumeFromHere(btn){
  btn.closest('.mwrap')?.remove();
  inputEl.value = '[CONTINUE]';
  inputEl.dispatchEvent(new Event('input'));
  send();
}

// ── #1 Undo send toast ──
let _undoTimer = null;

function _hideUndoToast(){
  const el = document.getElementById('undo-send-toast');
  if(el) el.classList.remove('show');
  clearTimeout(_undoTimer);
  _undoTimer = null;
}

function _undoSendRevert(userWrap, savedText, filesBackup){
  _hideUndoToast();
  removeTyping();
  document.querySelectorAll('.streaming-agent-wrap').forEach(el => el.remove());
  curBubble = null;
  curText = '';
  userWrap?.remove();
  if(rendered.length && rendered[rendered.length - 1].role === 'user'){
    rendered.pop();
    saveRenderedDebounced();
  }
  _suppressDraft = true;
  inputEl.value = savedText;
  inputEl.dispatchEvent(new Event('input'));
  _suppressDraft = false;
  pendingFiles = filesBackup.map(f => ({ ...f }));
  renderFilePreviews();
  setStatus(false);
  currentStreamId = null;
  todoReset();
  document.querySelectorAll('.followup-wrap,.continue-wrap').forEach(el => el.remove());
  removeEmptyAgentMessageWraps();
  const hasMsg = [...msgsEl.querySelectorAll('.mwrap')].some(w =>
    w.id !== 'typing' && w.id !== 'load-more-wrap' && (w.querySelector('.mrow.user') || w.querySelector('.mrow.agent'))
  );
  if(!hasMsg){
    const w = document.createElement('div');
    w.className = 'mwrap';
    w.innerHTML = buildWelcomeHTML();
    msgsEl.appendChild(w);
  }
}

function _showUndoToast(onUndo) {
  let el = document.getElementById('undo-send-toast');
  if (!el) {
    el = document.createElement('div');
    el.id = 'undo-send-toast';
    el.className = 'undo-toast';
    el.innerHTML =
      '<span>Đã gửi</span>' +
      '<div class="undo-toast-countdown">' +
        '<svg viewBox="0 0 20 20" width="20" height="20" aria-hidden="true">' +
        '<circle class="undo-track" cx="10" cy="10" r="8" fill="none" stroke-width="2"/>' +
        '<circle class="progress" cx="10" cy="10" r="8" fill="none" stroke-width="2" transform="rotate(-90 10 10)"/>' +
        '</svg>' +
      '</div>' +
      '<button type="button" class="undo-btn" id="undo-send-btn">Hủy</button>';
    document.body.appendChild(el);
  }
  const progressEl = el.querySelector('.progress');
  const undoBtn = el.querySelector('#undo-send-btn');
  const DURATION = 3000;
  const CIRCUMFERENCE = 50.27;

  clearTimeout(_undoTimer);
  el.classList.add('show');
  progressEl.style.transition = 'none';
  progressEl.style.strokeDashoffset = '0';
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      progressEl.style.transition = 'stroke-dashoffset ' + DURATION + 'ms linear';
      progressEl.style.strokeDashoffset = String(CIRCUMFERENCE);
    });
  });

  undoBtn.onclick = () => {
    clearTimeout(_undoTimer);
    el.classList.remove('show');
    onUndo();
  };

  _undoTimer = setTimeout(() => {
    el.classList.remove('show');
  }, DURATION);
}

async function send(){
  if(!inputEl) return;
  const text=inputEl.value.trim();
  if((!text&&!pendingFiles.length)||busy){
    if(busy && (text || pendingFiles.length)) showToast('Đang chờ phản hồi trước đó…', 2200);
    return;
  }
  // Blur sau khi chắc chắn sẽ gửi — tránh mất focus khi gõ Enter lúc đang busy / ô trống
  inputEl.blur();
  localStorage.removeItem('chat_draft');
  _suppressDraft = true;
  inputEl.value='';
  inputEl.dispatchEvent(new Event('input')); // reset height
  _suppressDraft = false;

  _lastQuestion = text;
  _lastAnswer   = '';
  const displayText=text||(pendingFiles.length?`[Gửi ${pendingFiles.length} file]`:'');
  const imageAttachments = pendingFiles.filter(f => f.previewUrl).map(f => ({ name: f.name, dataUrl: f.previewUrl }));
  const files=[...pendingFiles];
  const filesBackupForUndo = files.map(f=>({name:f.name,type:f.type||'',data:f.data,previewUrl:f.previewUrl||null}));

  currentStreamId=randomStreamId();
  ActivitySidebar.trackStream(currentStreamId);
  AmbientWidget.beginStream(currentStreamId);
  _retrySnapshot={text,files:files.map(f=>({name:f.name,type:f.type||'',data:f.data,previewUrl:f.previewUrl||null}))};
  pendingFiles=[];renderFilePreviews();

  const userTurnWrap = addUser(displayText, imageAttachments.length ? imageAttachments : undefined);
  const sendAbort = new AbortController();
  _currentSendAbort = sendAbort;
  const allowUndo = text !== '[CONTINUE]' && (!!String(text).trim() || filesBackupForUndo.length > 0);
  if(allowUndo){
    _showUndoToast(()=>{
      _sendAbortedByUndoToast = true;
      sendAbort.abort();
      _currentSendAbort = null;
      _undoSendRevert(userTurnWrap, text, filesBackupForUndo);
    });
  }

  setStatus(true);
  addTyping(TYPING_PHASE.CONNECTING);
  curBubble=null;
  todoReset();
  // Remove stale follow-ups from previous turn
  document.querySelectorAll('.followup-wrap,.continue-wrap').forEach(el=>el.remove());

  let reply='',_turnCollapsibles=[],_turnToolNames=[],turnToolCalls=[],turnToolResults=[];
  let undoToastDismissed = false;
  const activityStreamId = currentStreamId;
  execResetBlockState();
  try{
    const res=await fetch('/chat',{
      method:'POST',headers:{'Content-Type':'application/json'},
      signal: sendAbort.signal,
      body:JSON.stringify({message:text,files,history,stream_id:currentStreamId,
        model:cfg.model,temperature:cfg.temperature,
        use_ollama: uxOllamaEnabled(),
        system_prompt: (getActiveSkillPrompt() ? getActiveSkillPrompt() + '\n\n' : '') + (cfg.system_prompt||'') || undefined})
    });
    if(!res.ok){
      _hideUndoToast();
      let err=`Lỗi HTTP ${res.status}`;
      try{ const t=await res.text(); if(t) err=t.slice(0,1200); }catch{}
      AmbientWidget.reset();
      showChatError(err,text,'');
      removeEmptyAgentMessageWraps();
      ActivitySidebar.untrackStream(activityStreamId);
      setStatus(false);currentStreamId=null;
      return;
    }
    setTypingPhase(TYPING_PHASE.THINKING);
    const reader=res.body.getReader();
    const dec=new TextDecoder();
    let sseBuffer='',sseFatal=false;
    while(true){
      const{done,value}=await reader.read();
      if(value) sseBuffer += dec.decode(value,{stream:!done});
      const lines = sseBuffer.split('\n');
      sseBuffer = done ? '' : (lines.pop() || '');
      for(const line of lines){
        await waitIfPaused();
        if(!line.startsWith('data: '))continue;
        let d;try{d=JSON.parse(line.slice(6))}catch{continue}
        if(!undoToastDismissed){
          undoToastDismissed = true;
          _hideUndoToast();
        }
        if(d.type==='text'){appendText(d.content);reply+=d.content;_lastAnswer=reply}
        else if(d.type==='tool_call'){
          if(curBubble) finalizeBubble();
          AmbientWidget.onToolUse(d.name);
          _turnToolNames.push(d.name);
          const tid = d.id != null ? String(d.id) : ('gen-' + Date.now() + '-' + Math.random().toString(36).slice(2, 8));
          execAddToolItem(tid, d.name, d.input || {});
          // Lưu tool_call để lượt sau model biết đã gọi tool gì
          try{
            turnToolCalls.push({
              type: 'tool_use',
              id: tid,
              name: d.name,
              input: d.input || {}
            });
          }catch{}
          // Lưu before_content cho diff
          if(d.name === 'write_file' && d.before_content != null){
            _writeFileBeforeMap.set(tid, { path: (d.input||{}).path||'', before: d.before_content, newContent: (d.input||{}).content||'' });
          } else if(d.name === 'write_file'){
            _writeFileBeforeMap.set(tid, { path: (d.input||{}).path||'', before: null, newContent: (d.input||{}).content||'' });
          }
          // Live panel: hiện khi browser tool bắt đầu
          if(/^browser_/.test(d.name)){
            const stepLabel = formatToolStatusHint(d.name) || d.name.replace(/_/g,' ');
            const url = (d.input && d.input.url) ? d.input.url : '';
            if(!_blp.lastB64) _blp.show(); // hiện panel ngay cả khi chưa có frame
            _blp.setStep(stepLabel);
            if(url && _blp.urlEl){ _blp.urlEl.textContent = url.replace(/^https?:\/\//,'').slice(0,60); _blp.urlEl.title = url; }
            document.body.classList.add('browser-running');
          }
          setTypingPhase(TYPING_PHASE.TOOL, d.name);
          _streamCard=null; _streamWrap=null;
          if((!_todoItems.length || _todoAutoMode) && !HIDDEN_TOOLS.has(d.name)){
            todoAutoAddTool(d.name, d.input);
          }
        }
        else if(d.type==='tool_stream'){
          const sid = d.tool_use_id != null ? String(d.tool_use_id) : _pendingShellToolUseId;
          if(sid) execAppendShellStream(sid, d.line);
        }
        else if(d.type==='tool_result'){
          // Lưu tool output vào history để lượt sau model "biết agent đã làm gì"
          // Format theo Anthropic tool_result block: {type:"tool_result", tool_use_id, content}
          try{
            turnToolResults.push({
              type: 'tool_result',
              tool_use_id: d.tool_use_id != null ? String(d.tool_use_id) : '',
              content: d.result != null ? String(d.result) : (d.content != null ? String(d.content) : '')
            });
          }catch{}
          const masked = !!d.masked;
          execApplyToolResult({ ...d, masked });
          curBubble=null;
          setTypingPhase(TYPING_PHASE.AWAIT_MODEL);
          _streamCard=null; _streamWrap=null;
          advanceSubtask();
          todoMarkCurrentDone();
          document.body.classList.remove('browser-running');
        }
        else if(d.type==='tool_error'){
          execApplyToolError(d);
        }
        else if(d.type==='error_recovery'){
          const w=addEventPill('ev-retry', EV_ICONS.retry, `Recovery ${d.tool}: ${(d.suggestion||'').slice(0,80)}`);
          _turnCollapsibles.push({el:w, name:'retry'});
        }
        else if(d.type==='tool_retry'){
          const w=addEventPill('ev-retry', EV_ICONS.retry, `Retry ${d.name} (lần ${d.attempt}/3): ${(d.reason||'').slice(0,60)}`);
          _turnCollapsibles.push({el:w, name:'retry'});
        }
        else if(d.type==='retry_attempt'){
          renderRetryNotice({tool:d.tool, attempt:d.attempt, maxAttempts:d.max_attempts, delaySec:d.delay_sec, reason:d.reason});
        }
        else if(d.type==='fallback_attempt'){
          renderFallbackNotice({tool:d.tool, message:d.message});
        }
        else if(d.type==='model_selected'){
          const badge = document.getElementById('model-badge');
          if(badge){
            const dn = d.display_name || (d.model && d.model.includes('/') ? d.model.split('/').pop() : d.model) || '';
            const short = dn ? (dn.length>14 ? dn.slice(0,12)+'…' : dn) : (d.model && d.model.includes('haiku') ? 'haiku' : d.model && d.model.includes('sonnet') ? 'sonnet' : (d.model||'').slice(0,16));
            badge.textContent = short;
            badge.classList.remove('is-hidden');
            badge.title = [d.provider_label, d.route_hint, d.model, d.reason].filter(Boolean).join(' · ');
            // Màu theo tier model
            badge.classList.remove('badge-haiku','badge-sonnet','badge-opus','badge-gemini','badge-other');
            const m = (d.model||'').toLowerCase();
            if(m.includes('haiku'))       badge.classList.add('badge-haiku');
            else if(m.includes('sonnet')) badge.classList.add('badge-sonnet');
            else if(m.includes('opus'))   badge.classList.add('badge-opus');
            else if(m.includes('gemini') || m.includes('flash')) badge.classList.add('badge-gemini');
            else                          badge.classList.add('badge-other');
            badge.classList.add('badge-streaming');
            // Routing reason tooltip
            if(d.reason && d.complexity){
              const tierLabel = d.complexity === 'simple' ? '⚡ Haiku (tiết kiệm)' : d.complexity === 'complex' ? '🧠 Sonnet (đầy đủ)' : '👤 Bạn chọn';
              badge.title = `${tierLabel}\nModel: ${d.model}\nLý do: ${d.reason}`;
            }
          }
          updateHeaderModelFromSSE(d);
        }
        else if(d.type==='decomposition' && d.subtasks?.length){
          addSubtaskList(d.subtasks);
          todoSetFromDecomposition(d.subtasks);
        }
        else if(d.type==='history_compressed'){
          addEventPill('ev-compress', EV_ICONS.compress, `Đã nén ${d.compressed_count} tin nhắn cũ → ${d.summary_length} từ`);
        }
        else if(d.type==='parallel_tools'){
          const w=addEventPill('ev-parallel', EV_ICONS.parallel, `Chạy song song ${d.count} tools`);
          _turnCollapsibles.push({el:w, name:'parallel'});
        }
        else if(d.type==='verification_passed'){
          const w=addEventPill('ev-verify-ok', EV_ICONS.verifyOk, `Xác minh OK: ${d.tool}`);
          _turnCollapsibles.push({el:w, name:'verify'});
        }
        else if(d.type==='verification_failed'){
          const w=addEventPill('ev-verify-fail', EV_ICONS.verifyFail, `Xác minh thất bại: ${d.tool} — ${d.detail?.reason||''}`);
          _turnCollapsibles.push({el:w, name:'verify'});
        }
        else if(d.type==='page_intent'){
          const intent=d.intent||'unknown';
          const pillClass = intent==='captcha'||intent==='blocked' ? 'ev-verify-fail'
            : intent==='login_wall'||intent==='auth_expired'||intent==='rate_limited' ? 'ev-risk'
            : intent==='modal_open' ? 'ev-parallel' : 'ev-model';
          const w=addEventPill(pillClass, '◉', `Trang: ${intent} — ${(d.message||'').slice(0,140)}`);
          _turnCollapsibles.push({el:w, name:'page_intent'});
        }
        else if(d.type==='browser_frame' && d.base64){
          _renderBrowserFrame(d);
        }
        else if(d.type==='screenshot_captured' && d.b64){
          // Hiện thumbnail inline trong tool card screenshot_and_analyze
          const st = _execBlockState;
          if(st){
            const tid = d.tool_use_id != null ? String(d.tool_use_id) : null;
            const row = tid ? st.toolMap.get(tid) : null;
            if(row){
              const out = row.querySelector('.exec-tool-out');
              if(out){
                // Xóa shimmer nếu còn
                const shimmer = out.querySelector('.exec-screenshot-loading');
                if(shimmer) shimmer.remove();
                // Thêm thumbnail nếu chưa có
                if(!out.querySelector('.exec-screenshot-thumb-wrap')){
                  const ts = new Date().toLocaleTimeString('vi-VN',{hour:'2-digit',minute:'2-digit',second:'2-digit'});
                  const wrap = document.createElement('div');
                  wrap.className = 'exec-screenshot-thumb-wrap';
                  wrap.innerHTML = `<img class="exec-screenshot-thumb" src="data:image/png;base64,${d.b64}" alt="Screenshot" title="Click để phóng to"><span class="exec-screenshot-badge">${ts}</span>`;
                  const thumb = wrap.querySelector('.exec-screenshot-thumb');
                  thumb.addEventListener('click', () => {
                    const lb = document.createElement('div');
                    lb.className = 'browser-frame-lightbox';
                    const full = document.createElement('img');
                    full.src = thumb.src; full.alt = 'Screenshot full';
                    lb.appendChild(full);
                    lb.addEventListener('click', () => lb.remove());
                    document.body.appendChild(lb);
                  });
                  out.insertBefore(wrap, out.firstChild);
                }
              }
            }
          }
        }
        else if(d.type==='token_usage'){
          addTokenBar(d);
          updateCtxMeter(d.input_tokens||0);
        }
        else if(d.type==='done'){
          AmbientWidget.onDone();
          execFinalizeBlock();
          document.body.classList.remove('browser-running');
          // Ẩn live panel sau 2s khi agent xong
          setTimeout(() => _blp.hide(), 2000);
          _retrySnapshot=null;
          _lastRetryPayload=null;
          history.push({role:'user',content:text});
          if(turnToolCalls.length){
            history.push({role:'assistant',content:turnToolCalls});
          }
          if(turnToolResults.length){
            history.push({role:'user',content:turnToolResults});
          }
          if(reply)history.push({role:'assistant',content:reply});
          saveHistoryDebounced();finalizeBubble();
          // Cleanup: xóa toàn bộ streaming cursor còn sót (safety net)
          document.querySelectorAll('.bubble.streaming').forEach(b=>b.classList.remove('streaming'));
          document.querySelectorAll('.av.agent.thinking').forEach(a=>a.classList.remove('thinking'));
          removeEmptyAgentMessageWraps();
          // Collapse tool cards sau 400ms (để user thấy response trước)
          if(_turnCollapsibles.length){
            const toCollapse=[..._turnCollapsibles];
            _turnCollapsibles=[];
            setTimeout(()=>_collapseToolWraps(toCollapse), 400);
          }
          // Mark all remaining todo items done, then auto-hide
          _todoItems.forEach(t => { if(t.status !== 'done') t.status = 'done'; });
          _renderTodoItems();
          _autoHideTodoPanel();
          // Auto-generate title sau khi có câu trả lời từ assistant
          const assistantReplyCount = history.filter(m => m && m.role === 'assistant' && typeof m.content === 'string').length;
          if(assistantReplyCount === 1 && text){
            const words = text.trim().split(/\s+/).slice(0, 5).join(' ');
            const clientTitle = words.length > 3 ? words + (text.split(/\s+/).length > 5 ? '…' : '') : text.slice(0, 40);
            saveConvTitle(clientTitle);
          }
          if(assistantReplyCount === 2){
            fetch('/generate-title',{method:'POST',headers:{'Content-Type':'application/json'},
              body:JSON.stringify({messages:history})})
              .then(r=>r.ok ? r.json() : null).then(d=>{
                if(d && d.title) saveConvTitle(d.title);
              }).catch(()=>{});
          }
          // Hide model badge after done — giữ hiển thị, chỉ bỏ animation
          setTimeout(()=>{
            const b=document.getElementById('model-badge');
            if(b){ b.classList.remove('badge-streaming'); }
          }, 1200);
          // Auto-continue if response was cut off
          if(d.stop_reason === 'max_tokens' && reply.length > 200){
            setTimeout(_showContinueBtn, 400);
          } else if(reply.length > 80 && text && text !== '[CONTINUE]'){
            // Show follow-up suggestions (non-blocking)
            setTimeout(()=>_fetchFollowups(_lastQuestion, _lastAnswer.slice(0,600), _turnToolNames), 600);
          }
        }
        else if(d.type==='interrupted'){
          AmbientWidget.onInterrupted();
          execFinalizeBlock({ interrupted: true });
          setAgentStatusLine('');
          finalizeBubble();
          removeEmptyAgentMessageWraps();
          appendStoppedNoticeAndFocus();
          // #3 Continue from here button
          if(reply && reply.trim().length > 20){
            const rw = wrap();
            rw.innerHTML = '<button type="button" class="resume-btn" data-oculo="_resumeFromHere">' +
              '<svg viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3" fill="currentColor"/></svg>' +
              'Tiếp tục từ đây</button>';
          }
          hideTodoPanel();
        }
        else if(d.type==='error'){
          AmbientWidget.onStreamError(d.content);
          execFinalizeBlock();
          showChatError(d.content,text,reply);
          sseFatal=true;
          break;
        }
      }
      if(sseFatal)break;
      if(done)break;
    }
  }catch(e){
    if(e && e.name === 'AbortError'){
      ActivitySidebar.untrackStream(activityStreamId);
      AmbientWidget.onInterrupted();
      if(!_sendAbortedByUndoToast){
        finalizeBubble();
        removeEmptyAgentMessageWraps();
        appendStoppedNoticeAndFocus();
      }
      _sendAbortedByUndoToast = false;
    } else {
      AmbientWidget.onStreamError(e.message||String(e));
      showChatError(e.message||String(e),text,reply);
    }
  }
  _resumePauseIfHanging();
  _hideUndoToast();
  removeEmptyAgentMessageWraps();
  AmbientWidget.endStreamCleanup();
  ActivitySidebar.untrackStream(activityStreamId);
  _currentSendAbort = null;
  setStatus(false);currentStreamId=null;
}

// Đảm bảo data-oculo="send" luôn gọi được (một số môi trường không gắn async function lên window)
window.send = send;

function suggest(t, autoSend = true){
  inputEl.value=t;
  inputEl.dispatchEvent(new Event('input'));
  // #13 Smooth scroll xuống input trước khi focus
  inputEl.scrollIntoView({behavior:'smooth', block:'nearest'});
  setTimeout(()=>{
    inputEl.focus();
    if(autoSend) send();
  }, 150);
}

// ── Export ──
// #9 Copy conversation to clipboard
function copyConversation(){
  const text = rendered.map(m=>{
    const role = m.role === 'user' ? 'Bạn' : 'Oculo';
    return `${role} (${m.ts||''})\n${m.text||''}\n`;
  }).join('\n---\n\n');
  if(!text.trim()){ showToast('Không có nội dung để sao chép'); return; }
  navigator.clipboard.writeText(text)
    .then(()=>showToast('✓ Đã sao chép toàn bộ hội thoại'))
    .catch(()=>showToast('Không sao chép được'));
}

function exportObsidian(){
  const now = new Date();
  const dateStr = now.toISOString().slice(0,10);
  const title = _conversations.find(c=>c.id===_activeConvId)?.title || 'Oculo Chat';
  const frontmatter = '---\ntitle: ' + title + '\ndate: ' + dateStr + '\ntags: [oculo, ai-chat]\n---\n\n';
  const body = rendered.map(m=>{
    const role = m.role === 'user' ? '**Bạn**' : '**Oculo**';
    return role + ' (' + (m.ts||'') + ')\n\n' + (m.text||'') + '\n';
  }).join('\n---\n\n');
  const content = frontmatter + body;
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([content], {type:'text/markdown'}));
  a.download = dateStr + '-' + title.slice(0,30).replace(/[^a-zA-Z0-9\u00C0-\u024F\s]/g,'').trim().replace(/\s+/g,'-') + '.md';
  a.click();
  showToast('✓ Đã xuất Obsidian/Notion Markdown');
}

function exportChat(){
  const fmt=prompt('Chọn định dạng xuất: markdown, json, hoặc obsidian','markdown');
  if(!fmt)return;
  let content,filename,mime;
  if(fmt && fmt.toLowerCase()==='obsidian'){ exportObsidian(); return; }
  if(fmt && fmt.toLowerCase()==='json'){
    content=JSON.stringify({history,rendered},null,2);
    filename='chat-export.json';mime='application/json';
  }else{
    content=rendered.map(m=>`**${m.role==='user'?'Bạn':'Agent'}** (${m.ts})\n\n${m.text}\n\n---\n`).join('\n');
    filename='chat-export.md';mime='text/markdown';
  }
  const a=document.createElement('a');
  a.href=URL.createObjectURL(new Blob([content],{type:mime}));
  a.download=filename;a.click();
}

function exportPDF(){
  window.print();
}

// ══════════════════════════════════════════
// ── MULTI-CONVERSATION SIDEBAR ──
// ══════════════════════════════════════════
let _conversations = [];
let _activeConvId = null;

function loadConversations(){
  try{
    _conversations = JSON.parse(localStorage.getItem(CONV_KEY)||'[]');
  }catch(e){ _conversations=[]; }
  renderConvList();
}

function saveConversations(){
  _lsSet(CONV_KEY, JSON.stringify(_conversations));
}

function getCurrentConvId(){
  return _activeConvId;
}

// Xóa markdown khỏi title (**, *, #, `...)
function _cleanTitle(t){
  return (t||'')
    .replace(/\*{1,3}([^*]+)\*{1,3}/g,'$1')  // **bold**, *italic*
    .replace(/#{1,6}\s*/g,'')                  // headings
    .replace(/`[^`]*`/g,m=>m.replace(/`/g,''))
    .replace(/\[([^\]]+)\]\([^)]+\)/g,'$1')   // links
    .trim();
}

function saveConvTitle(title){
  if(!_activeConvId) return;
  const conv = _conversations.find(c=>c.id===_activeConvId);
  if(conv){ conv.title=_cleanTitle(title); conv.updatedAt=Date.now(); saveConversations(); renderConvList(); }
}

function saveCurrentConv(){
  if(!_activeConvId) return;
  const conv = _conversations.find(c=>c.id===_activeConvId);
  if(conv){
    const rClean = stripEmptyAgentFromRendered(rendered);
    if(rClean.length !== rendered.length){
      rendered = rClean;
      saveRenderedDebounced();
    }
    conv.history = JSON.parse(JSON.stringify(history));
    conv.rendered = JSON.parse(JSON.stringify(rendered));
    conv.updatedAt = Date.now();
    saveConversations();
  }
}

function newConversation(){
  // Save current before switching
  saveCurrentConv();
  const id = 'conv_'+Date.now();
  const conv = {id, title:'Cuộc hội thoại mới', history:[], rendered:[], createdAt:Date.now(), updatedAt:Date.now()};
  _conversations.unshift(conv);
  saveConversations();
  _activeConvId = id;
  // Clear UI
  history=[]; rendered=[];
  _msgTextStore.length = 0;
  localStorage.removeItem(SK); localStorage.removeItem(RK);
  msgsEl.innerHTML='';
  const w=document.createElement('div');w.className='mwrap';
  w.innerHTML=buildWelcomeHTML();
  msgsEl.appendChild(w);
  inputEl.value=''; inputEl.style.height='auto'; inputEl.focus();
  renderConvList();
}

// #4 Skeleton loader khi switch conversation
function _showConvSkeleton(){
  const skels = [
    {role:'agent', lines:[75,55,65]},
    {role:'user',  lines:[60]},
    {role:'agent', lines:[80,50]},
  ];
  skels.forEach(s=>{
    const w = document.createElement('div');
    w.className = 'mwrap';
    const linesHtml = s.lines.map(pct=>
      `<div class="msg-skeleton-line" style="width:${pct}%"></div>`
    ).join('');
    w.innerHTML = `<div class="msg-skeleton ${s.role}">
      <div class="msg-skeleton-av"></div>
      <div class="msg-skeleton-lines">${linesHtml}</div>
    </div>`;
    msgsEl.appendChild(w);
  });
}

async function switchConversation(id){
  if(id===_activeConvId) return;
  saveCurrentConv();
  const conv = _conversations.find(c=>c.id===id);
  if(!conv) return;
  _activeConvId = id;
  _msgTextStore.length = 0;

  // #13 Fade out current content
  msgsEl.classList.add('conv-switching');
  await new Promise(r => setTimeout(r, 150));
  msgsEl.classList.remove('conv-switching');
  // #4 Hiện skeleton loader ngay lập tức
  msgsEl.innerHTML = '';
  _showConvSkeleton();

  history = JSON.parse(JSON.stringify(conv.history||[]));
  {
    const rawR = JSON.parse(JSON.stringify(conv.rendered||[]));
    rendered = stripEmptyAgentFromRendered(rawR);
    if(rendered.length !== rawR.length) saveCurrentConv();
  }

  if(!rendered.length && history.length){
    history.forEach(m=>{
      let text = '';
      if(typeof m.content === 'string'){
        text = m.content;
      } else if(Array.isArray(m.content)){
        // Extract text blocks từ array content (tool_use, tool_result, etc.)
        text = m.content
          .filter(p => p?.type === 'text')
          .map(p => p.text||'')
          .join('\n').trim();
      }
      if(!text) return;
      if(m.role==='user')           rendered.push({role:'user',  text, ts:''});
      else if(m.role==='assistant') rendered.push({role:'agent', text, ts:''});
    });
    if(rendered.length) saveCurrentConv();
  }

  // Safety-net B: kiểm tra per-conv backup key (lưu lúc beforeunload)
  if(!rendered.length){
    try{
      const bak = JSON.parse(localStorage.getItem(`conv_bak_${id}`)||'null');
      if(bak?.rendered?.length){
        const rawB = bak.rendered;
        rendered = stripEmptyAgentFromRendered(rawB);
        if(!history.length && bak.history?.length) history = bak.history;
        saveCurrentConv();
        console.log('[conv] Restored from backup key');
      }
    }catch(e){}
  }

  // Safety-net C: SK/RK legacy (trước khi có multi-conv)
  if(!rendered.length && !history.length){
    try{
      const legacyH = JSON.parse(localStorage.getItem(SK)||'[]');
      const legacyR = JSON.parse(localStorage.getItem(RK)||'[]');
      if(legacyR.length){
        rendered=stripEmptyAgentFromRendered(legacyR);
        history=legacyH;
        saveCurrentConv();
        if(rendered.length!==legacyR.length) saveRendered();
      }
      else if(legacyH.length){
        // Có history nhưng không có rendered → rebuild
        legacyH.forEach(m=>{
          const text = typeof m.content==='string' ? m.content : '';
          if(!text) return;
          if(m.role==='user')      rendered.push({role:'user', text, ts:''});
          else if(m.role==='assistant' && String(text).trim()) rendered.push({role:'agent', text, ts:''});
        });
        if(rendered.length){ history=legacyH; saveCurrentConv(); }
      }
    }catch(e){}
  }

  // Re-render messages
  msgsEl.innerHTML='';
  if(!rendered.length){
    const w=document.createElement('div');w.className='mwrap';
    w.innerHTML=buildWelcomeHTML();
    msgsEl.appendChild(w);
  } else {
    const startIdx = Math.max(0, rendered.length - LAZY_LOAD_SIZE);
    _renderedStart = startIdx;
    if(startIdx > 0){
      const w=document.createElement('div');w.className='mwrap';w.id='load-more-wrap';
      w.innerHTML=`<div style="text-align:center;padding:10px"><button type="button" data-oculo="loadMoreHistory" style="background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:6px 14px;font-size:12px;color:var(--soft);cursor:pointer">Tải ${startIdx} tin nhắn cũ hơn</button></div>`;
      msgsEl.appendChild(w);
    }
    rendered.slice(startIdx).forEach(item=>{
      if(item.role==='user') renderUser(item.text, item.ts, false, item.images);
      else if(item.role==='agent') renderAgent(item.text,item.ts,false);
    });
  }
  removeEmptyAgentMessageWraps();
  // #13 Fade in
  msgsEl.classList.add('conv-switching-in');
  setTimeout(()=>msgsEl.classList.remove('conv-switching-in'), 200);
  scrollEnd(false);
  renderConvList();
  // Close sidebar on mobile
  if(window.innerWidth < 768) toggleSidebar();
}

function deleteConversation(id, e){
  e.stopPropagation();
  openConfirmModal({
    title: 'Xóa cuộc hội thoại?',
    message: 'Cuộc trò chuyện này sẽ bị xóa khỏi danh sách trên thiết bị này.',
    okText: 'Xóa',
    danger: true,
    onConfirm: ()=>{_executeDeleteConversation(id);}
  });
}
function _executeDeleteConversation(id){
  _conversations = _conversations.filter(c=>c.id!==id);
  saveConversations();
  if(_activeConvId===id){
    _activeConvId=null;
    if(_conversations.length) switchConversation(_conversations[0].id);
    else newConversation();
  } else {
    renderConvList();
  }
}

// ── Conv preview: lấy text tin nhắn cuối
function _convLastMsg(conv){
  const r = conv.rendered||[];
  if(!r.length) return '';
  const last = r[r.length-1];
  return (last.text||'').replace(/[#*`>\-]/g,'').replace(/\s+/g,' ').trim().slice(0,55);
}

// ── Date grouping
function _convDateGroup(conv){
  const d = new Date(conv.updatedAt||conv.createdAt||0);
  const now = new Date();
  const diffDays = Math.floor((now - d) / 86400000);
  if(diffDays < 1) return 'Hôm nay';
  if(diffDays < 2) return 'Hôm qua';
  if(diffDays < 7) return 'Tuần này';
  if(diffDays < 30) return 'Tháng này';
  return 'Cũ hơn';
}

// ── Build one conv-item HTML
function _convItemHTML(c){
  const isActive  = c.id === _activeConvId;
  const isPinned  = c.pinned || false;
  const preview   = _convLastMsg(c);
  const title     = _cleanTitle(c.title) || 'Cuộc hội thoại';
  // #7 Message count badge
  const msgCount  = (c.rendered||c.history||[]).length;
  const countBadge = msgCount > 0
    ? `<span class="conv-count-badge" title="${msgCount} tin nhắn">${msgCount}</span>`
    : '';
  const S = `width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"`;
  const pinSvg   = `<svg ${S}><line x1="12" y1="17" x2="12" y2="22"/><path d="M5 17h14v-1.76a2 2 0 0 0-1.11-1.79l-1.78-.9A2 2 0 0 1 15 10.76V6h1a2 2 0 0 0 0-4H8a2 2 0 0 0 0 4h1v4.76a2 2 0 0 1-1.11 1.79l-1.78.9A2 2 0 0 0 5 15.24Z"/></svg>`;
  const trashSvg = `<svg ${S}><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/></svg>`;
  const editSvg  = `<svg ${S}><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4z"/></svg>`;

  const cid = encodeURIComponent(c.id);
  return `<div class="conv-item ${isActive?'active':''} ${isPinned?'pinned':''}"
    data-oculo="switchConversation"
    data-conv-id="${cid}"
    title="${esc(title)} — nhấp đôi để đổi tên">
    <span class="conv-pin-icon">${pinSvg}</span>
    <div class="conv-content">
      <div class="conv-title-row">
        <span class="conv-title">${esc(title)}</span>
        ${countBadge}
      </div>
      ${preview ? `<span class="conv-preview">${esc(preview)}</span>` : ''}
    </div>
    <div class="conv-actions">
      <button type="button" class="conv-act pin-btn" data-oculo="togglePinConv" data-conv-id="${cid}" data-oculo-stop title="${isPinned?'Bỏ ghim':'Ghim'}">
        ${pinSvg}
      </button>
      <button type="button" class="conv-act" data-oculo="startRenameConv" data-conv-id="${cid}" data-oculo-stop title="Đổi tên">
        ${editSvg}
      </button>
      <button type="button" class="conv-act del-btn" data-oculo="deleteConversation" data-conv-id="${cid}" data-oculo-stop title="Xóa">
        ${trashSvg}
      </button>
    </div>
  </div>`;
}

let _convSearchQuery = '';

function filterConvList(q){
  _convSearchQuery = q.toLowerCase().trim();
  // Toggle clear button visibility
  const clr = document.getElementById('conv-search-clear');
  if(clr) clr.hidden = !q;
  renderConvList();
}

function renderConvList(){
  const list = document.getElementById('conv-list');
  if(!list) return;

  if(!_conversations.length){
    list.innerHTML=`<div class="conv-empty-hint">
      <div class="conv-empty-orb">${EYE_AVATAR_HTML}</div>
      <div class="conv-empty-title">Chưa có hội thoại nào</div>
      <div class="conv-empty-sub">Nhấn <b>+</b> hoặc <b>⌘N</b> để bắt đầu cuộc trò chuyện mới.</div>
    </div>`;
    return;
  }

  // Filter by search
  let convs = _conversations;
  if(_convSearchQuery){
    convs = convs.filter(c=>
      (c.title||'').toLowerCase().includes(_convSearchQuery) ||
      _convLastMsg(c).toLowerCase().includes(_convSearchQuery)
    );
    if(!convs.length){
      list.innerHTML=`<div class="conv-no-results">Không tìm thấy "${esc(_convSearchQuery)}"</div>`;
      return;
    }
    // Search mode: no grouping, show flat
    list.innerHTML = convs.map(_convItemHTML).join('');
    return;
  }

  // Sort: pinned first, then by updatedAt desc
  const sorted = [...convs].sort((a,b)=>{
    if((b.pinned||false) !== (a.pinned||false)) return (b.pinned?1:0) - (a.pinned?1:0);
    return (b.updatedAt||0) - (a.updatedAt||0);
  });

  // Group by date
  const groups = {};
  const groupOrder = [];
  sorted.forEach(c=>{
    const g = c.pinned ? 'Đã ghim' : _convDateGroup(c);
    if(!groups[g]){ groups[g]=[]; groupOrder.push(g); }
    groups[g].push(c);
  });

  list.innerHTML = groupOrder.map(g=>`
    <div class="conv-group-label">${g}</div>
    ${groups[g].map(_convItemHTML).join('')}
  `).join('');
}

// ── Pin / Unpin
function togglePinConv(id, e){
  e.stopPropagation();
  const conv = _conversations.find(c=>c.id===id);
  if(!conv) return;
  conv.pinned = !conv.pinned;
  conv.updatedAt = Date.now();
  saveConversations();
  renderConvList();
}

// ── Rename (double-click)
function startRenameConv(id, e){
  e.stopPropagation();
  const conv = _conversations.find(c=>c.id===id);
  if(!conv) return;

  let target = null;
  document.querySelectorAll('.conv-item[data-conv-id]').forEach(el=>{
    try{
      if(decodeURIComponent(el.getAttribute('data-conv-id')||'')===id) target = el;
    }catch{
      if(el.getAttribute('data-conv-id')===id) target = el;
    }
  });
  if(!target) return;

  const titleEl = target.querySelector('.conv-title');
  if(!titleEl) return;

  const inp = document.createElement('input');
  inp.className = 'conv-rename-input';
  inp.value = conv.title || '';
  inp.maxLength = 60;
  titleEl.replaceWith(inp);
  inp.focus(); inp.select();
  target.onclick = null; // disable switch while renaming

  const save = ()=>{
    const newTitle = inp.value.trim() || conv.title || 'Cuộc hội thoại';
    conv.title = newTitle;
    conv.updatedAt = Date.now();
    saveConversations();
    renderConvList();
  };
  inp.addEventListener('blur', save);
  inp.addEventListener('keydown', e2=>{
    if(e2.key==='Enter') inp.blur();
    if(e2.key==='Escape'){ inp.value=conv.title||''; inp.blur(); }
  });
}

function syncSidebarToggleA11y(){
  const tb = document.getElementById('sidebar-toggle');
  if(tb) tb.setAttribute('aria-expanded', document.body.classList.contains('sidebar-open') ? 'true' : 'false');
}
function closeSidebar(){
  if(!document.body.classList.contains('sidebar-open')) return;
  document.body.classList.remove('sidebar-open');
  const si = document.getElementById('conv-search');
  if(si) si.value='';
  filterConvList('');
  syncSidebarToggleA11y();
}
function toggleSidebar(){
  document.body.classList.toggle('sidebar-open');
  if(!document.body.classList.contains('sidebar-open')){
    const si = document.getElementById('conv-search');
    if(si) si.value='';
    filterConvList('');
  }
  syncSidebarToggleA11y();
}
function updateSidebarLayout(){
  document.body.classList.toggle('sidebar-overlay', window.innerWidth < 900);
}
function syncHeaderHeight(){
  const hEl = document.querySelector('header');
  if(!hEl) return;
  const h = Math.ceil(hEl.getBoundingClientRect().height);
  document.documentElement.style.setProperty('--header-h', `${h}px`);
}
let _headerResizeObs;
function initHeaderHeightSync(){
  const hEl = document.querySelector('header');
  if(!hEl) return;
  syncHeaderHeight();
  if(typeof ResizeObserver !== 'undefined' && !_headerResizeObs){
    _headerResizeObs = new ResizeObserver(syncHeaderHeight);
    _headerResizeObs.observe(hEl);
  }
}

// ── Settings ──
async function openSettings(){
  await loadModelCatalog();
  fillCfgModelSelect(document.getElementById('cfg-model'));
  document.getElementById('cfg-temp').value=cfg.temperature;
  document.getElementById('temp-display').textContent=cfg.temperature;
  document.getElementById('cfg-system').value=cfg.system_prompt;
  const eo = document.getElementById('cfg-enable-ollama');
  const fu = document.getElementById('cfg-followups');
  const rw = document.getElementById('cfg-risk-warn');
  if(eo) eo.checked = uxOllamaEnabled();
  if(fu) fu.checked = uxFollowupsEnabled();
  if(rw) rw.checked = uxRiskToolWarn();
  updateCfgModelDetail();
  _openModalWithFocus('settings-modal');
}
document.getElementById('cfg-temp').addEventListener('input',function(){
  document.getElementById('temp-display').textContent=parseFloat(this.value).toFixed(2);
});
const _cfgModelEl = document.getElementById('cfg-model');
if(_cfgModelEl) _cfgModelEl.addEventListener('change', updateCfgModelDetail);
const _cfgEnableOllamaEl = document.getElementById('cfg-enable-ollama');
if(_cfgEnableOllamaEl){
  _cfgEnableOllamaEl.addEventListener('change', async function(){
    // Sync flag ngay để dropdown phản ánh đúng (saveSettings sẽ ghi lại lần nữa)
    try{
      localStorage.setItem('ux_enable_ollama', this.checked ? '1' : '0');
    }catch{}
    if(this.checked){
      await ensureOllamaReadyForUi({ silent: false });
      await loadModelCatalog();
    }
    enforceOllamaPolicy({ notify: !this.checked });
    fillCfgModelSelect(document.getElementById('cfg-model'));
    const sel = document.getElementById('cfg-model');
    if(sel) sel.value = cfg.model;
    updateCfgModelDetail();
    updateHeaderModelDisplay();
  });
}
async function saveSettings(){
  const eo = document.getElementById('cfg-enable-ollama');
  const prevOllama = uxOllamaEnabled();
  if(eo) localStorage.setItem('ux_enable_ollama', eo.checked ? '1' : '0');
  if(!prevOllama && uxOllamaEnabled()){
    await ensureOllamaReadyForUi({ silent: true });
    await loadModelCatalog();
  }
  enforceOllamaPolicy({ notify: true });
  cfg.model=document.getElementById('cfg-model').value;
  if(!uxOllamaEnabled() && isOllamaModelId(cfg.model)){
    cfg.model = firstNonOllamaModelId();
  }
  cfg.temperature=parseFloat(document.getElementById('cfg-temp').value);
  cfg.system_prompt=document.getElementById('cfg-system').value;
  localStorage.setItem('cfg_model',cfg.model);
  localStorage.setItem('cfg_temp',cfg.temperature);
  localStorage.setItem('cfg_system',cfg.system_prompt);
  const fu = document.getElementById('cfg-followups');
  const rw = document.getElementById('cfg-risk-warn');
  if(fu) localStorage.setItem('ux_followup_suggestions', fu.checked ? '1' : '0');
  if(rw) localStorage.setItem('ux_warn_risk_tools', rw.checked ? '1' : '0');
  updateHeaderModelDisplay();
  closeModal('settings-modal');
}

// ── Schedules ──
// Trích title ngắn từ task description (bỏ commands, URL, bước số)
function _schedTitle(task){
  return task
    .split(/\n|Bước\s*\d+[:.]/i)[0]   // dòng đầu, trước "Bước 1:"
    .replace(/curl\s+[^\s]+.*/gi,'')   // bỏ curl command
    .replace(/https?:\/\/\S+/g,'')     // bỏ URL
    .replace(/\s{2,}/g,' ')
    .trim()
    .slice(0,120) || task.slice(0,120);
}

// Tính thời gian chạy và countdown (không dùng toLocale* cho giờ — tránh ký tự ▯ do NBSP/U+202F)
function _schedTimeInfo(job){
  try{
    const created   = new Date(job.created);
    const scheduled = new Date(created.getTime() + (job.delay||0)*1000);
    const now       = new Date();
    const diffMs    = scheduled - now;
    const hh = String(scheduled.getHours()).padStart(2,'0');
    const mm = String(scheduled.getMinutes()).padStart(2,'0');
    const timeStr = `${hh}:${mm}`;
    const sameCalDay = scheduled.getFullYear() === now.getFullYear()
      && scheduled.getMonth() === now.getMonth()
      && scheduled.getDate() === now.getDate();
    const dd = String(scheduled.getDate()).padStart(2,'0');
    const mo = String(scheduled.getMonth() + 1).padStart(2,'0');
    const dateStr = sameCalDay ? 'hôm nay' : `${dd}/${mo}`;
    const label = `${timeStr} ${dateStr}`;
    if(diffMs <= 0) return { label, countdown:'Đã chạy', cls:'done' };
    const sec = Math.ceil(diffMs/1000);
    const countdownText = sec < 60 ? `còn ${sec}s` : sec < 3600 ? `còn ${Math.ceil(sec/60)}p` : `còn ${Math.ceil(sec/3600)}h`;
    const cls = sec < 120 ? 'soon' : 'waiting';
    return { label, countdown:countdownText, cls };
  }catch{ return { label:'—', countdown:'', cls:'waiting' }; }
}

/** Cùng API /schedules với bảng Hoạt động — mở sidebar và cuộn tới mục Lịch đã đặt. */
async function openSchedules(){
  ActivitySidebar.applyOpenState(true, true);
  const z = await ActivitySidebar._fetchJsonOk('/schedules');
  if(z && typeof z === 'object'){
    ActivitySidebar.lastData.schedules = z;
    ActivitySidebar.renderSchedules(z);
    ActivitySidebar.lastSig.schedules = JSON.stringify(z);
    ActivitySidebar.updateBadge();
  }
  requestAnimationFrame(() => {
    document.getElementById('as-section-schedules')?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  });
}

let _confirmAction = null;
let _modalFocusTrapHandler = null;
let _modalPrevFocus = null;

function closeModal(id){
  const el = document.getElementById(id);
  if(!el) return;
  el.classList.remove('open');
  if(id==='confirm-modal') _confirmAction = null;
  // Restore focus trap
  if(_modalFocusTrapHandler){
    document.removeEventListener('keydown', _modalFocusTrapHandler);
    _modalFocusTrapHandler = null;
  }
  if(_modalPrevFocus){ _modalPrevFocus.focus(); _modalPrevFocus = null; }
}

function _trapFocus(modalEl){
  const focusable = modalEl.querySelectorAll(
    'button:not([disabled]),input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])'
  );
  if(!focusable.length) return;
  const first = focusable[0], last = focusable[focusable.length - 1];
  _modalFocusTrapHandler = (e) => {
    if(e.key !== 'Tab') return;
    if(e.shiftKey){ if(document.activeElement === first){ e.preventDefault(); last.focus(); } }
    else { if(document.activeElement === last){ e.preventDefault(); first.focus(); } }
  };
  document.addEventListener('keydown', _modalFocusTrapHandler);
  // Focus first focusable element
  setTimeout(() => first.focus(), 50);
}

function _openModalWithFocus(id){
  _modalPrevFocus = document.activeElement;
  const el = document.getElementById(id);
  if(!el) return;
  el.classList.add('open');
  _trapFocus(el);
}
function openConfirmModal(opts){
  document.getElementById('confirm-title').textContent = opts.title || 'Xác nhận';
  document.getElementById('confirm-message').textContent = opts.message || '';
  const ok = document.getElementById('confirm-ok-btn');
  ok.textContent = opts.okText || 'Xác nhận';
  ok.classList.toggle('btn-danger', !!opts.danger);
  _confirmAction = opts.onConfirm;
  _openModalWithFocus('confirm-modal');
}
function confirmModalExecute(){
  const fn = _confirmAction;
  _confirmAction = null;
  closeModal('confirm-modal');
  if(typeof fn === 'function'){
    try{
      const r = fn();
      if(r && typeof r.then === 'function') r.catch(()=>{});
    }catch(e){}
  }
}
function confirmModalCancel(){
  _confirmAction = null;
  closeModal('confirm-modal');
}
function openClearMemoryConfirm(){
  openConfirmModal({
    title: 'Xóa toàn bộ bộ nhớ?',
    message: 'Hành động này không thể hoàn tác. Tất cả ghi nhớ dài hạn sẽ bị xóa.',
    okText: 'Xóa tất cả',
    danger: true,
    onConfirm: ()=>{ clearAllMemories(); }
  });
}
document.querySelectorAll('.modal-overlay').forEach(el=>el.addEventListener('click',e=>{
  if(e.target !== el) return;
  closeModal(el.id);
}));

// ── New Chat ──
function _doNewChat(){
  resetSubtasks();
  newConversation();
}
function newChat(){
  if(busy){
    openConfirmModal({
      title: 'Agent đang chạy',
      message: 'Tạo cuộc hội thoại mới? Tiến trình hiện tại sẽ dừng.',
      okText: 'Tạo mới',
      danger: true,
      onConfirm: ()=>{ _doNewChat(); }
    });
    return;
  }
  _doNewChat();
}
// ── @ Mention file picker ──
let _atMentionOpen = false;
let _atMentionFiles = [];
let _atMentionIdx = 0;

const _RECENT_FILES_KEY = 'oculo_recent_files';
function _saveRecentFile(name, path){
  try{
    let list = JSON.parse(localStorage.getItem(_RECENT_FILES_KEY) || '[]');
    list = [{name, path}, ...list.filter(f => f.path !== path)].slice(0, 10);
    localStorage.setItem(_RECENT_FILES_KEY, JSON.stringify(list));
  }catch(e){}
}
function _getRecentFiles(){
  try{ return JSON.parse(localStorage.getItem(_RECENT_FILES_KEY) || '[]'); }
  catch(e){ return []; }
}

async function _fetchDesktopFiles(query){
  try{
    const r = await fetch('/list-files?q=' + encodeURIComponent(query || ''), { cache: 'no-store' });
    if(!r.ok) return [];
    return await r.json();
  }catch(e){ return []; }
}

function _getOrCreateAtPicker(){
  let el = document.getElementById('at-mention-picker');
  if(!el){
    el = document.createElement('div');
    el.id = 'at-mention-picker';
    el.className = 'at-mention-picker';
    el.setAttribute('role', 'listbox');
    el.setAttribute('aria-label', 'Chọn file');
    document.getElementById('input-area').appendChild(el);
  }
  return el;
}

async function _openAtMentionPicker(){
  _atMentionOpen = true;
  await _updateAtMentionPicker('');
}

async function _updateAtMentionPicker(query){
  const picker = _getOrCreateAtPicker();
  picker.innerHTML = '<div class="at-mention-loading">Đang tìm…</div>';
  picker.classList.add('open');
  _atMentionOpen = true;

  // Lấy recent + desktop files
  const recent = _getRecentFiles().filter(f =>
    !query || f.name.toLowerCase().includes(query.toLowerCase())
  ).slice(0, 5);
  const desktop = await _fetchDesktopFiles(query);
  const all = [...recent, ...desktop.filter(f => !recent.find(r => r.path === f.path))].slice(0, 8);

  if(!all.length){
    picker.innerHTML = '<div class="at-mention-empty">Không tìm thấy file</div>';
    return;
  }
  _atMentionFiles = all;
  _atMentionIdx = 0;
  _renderAtMentionItems(picker, all, query);
}

function _renderAtMentionItems(picker, files, query){
  picker.innerHTML = '';
  files.forEach((f, i) => {
    const item = document.createElement('div');
    item.className = 'at-mention-item' + (i === _atMentionIdx ? ' at-mention-item--active' : '');
    item.setAttribute('role', 'option');
    item.setAttribute('aria-selected', i === _atMentionIdx ? 'true' : 'false');
    const ext = f.name.split('.').pop().toLowerCase();
    const icon = ['png','jpg','jpeg','gif','webp'].includes(ext) ? '🖼' :
                 ['py','js','ts','json','md','txt','csv'].includes(ext) ? '📄' : '📁';
    item.innerHTML = `<span class="at-mention-icon">${icon}</span><span class="at-mention-name">${esc(f.name)}</span><span class="at-mention-path">${esc((f.path||'').replace(/^.*\/([^/]+\/[^/]+)$/, '…/$1'))}</span>`;
    item.addEventListener('mousedown', (e) => {
      e.preventDefault();
      _selectAtMentionFile(f);
    });
    picker.appendChild(item);
  });
}

function _selectAtMentionFile(f){
  // Thay @ + query bằng tên file trong input
  const val = inputEl.value;
  const pos = inputEl.selectionStart;
  const atIdx = val.lastIndexOf('@', pos - 1);
  if(atIdx >= 0){
    const before = val.slice(0, atIdx);
    const after = val.slice(pos);
    inputEl.value = before + after;
    inputEl.setSelectionRange(atIdx, atIdx);
  }
  _closeAtMentionPicker();
  // Attach file qua fetch
  _attachFileByPath(f.path, f.name);
  _saveRecentFile(f.name, f.path);
}

async function _attachFileByPath(path, name){
  try{
    const r = await fetch('/read-file-b64', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({path})
    });
    if(!r.ok) return;
    const d = await r.json();
    const isImg = /\.(png|jpg|jpeg|gif|webp)$/i.test(name);
    const dataUrl = isImg ? `data:${d.mime||'image/png'};base64,${d.b64}` : null;
    pendingFiles.push({ name, type: d.mime || 'text/plain', data: d.b64, previewUrl: dataUrl });
    renderFilePreviews();
    showToast(`Đã đính kèm: ${name}`);
  }catch(e){
    showToast('Không thể đọc file: ' + name, 2500);
  }
}

function _closeAtMentionPicker(){
  _atMentionOpen = false;
  const picker = document.getElementById('at-mention-picker');
  if(picker) picker.classList.remove('open');
}

// Arrow navigation trong @ picker
if(inputEl){
  inputEl.addEventListener('keydown', e => {
    if(!_atMentionOpen) return;
    if(e.key === 'ArrowDown'){
      e.preventDefault();
      _atMentionIdx = Math.min(_atMentionIdx + 1, _atMentionFiles.length - 1);
      _renderAtMentionItems(document.getElementById('at-mention-picker'), _atMentionFiles, '');
    } else if(e.key === 'ArrowUp' && _atMentionOpen){
      e.preventDefault();
      _atMentionIdx = Math.max(_atMentionIdx - 1, 0);
      _renderAtMentionItems(document.getElementById('at-mention-picker'), _atMentionFiles, '');
    } else if(e.key === 'Enter' && _atMentionOpen){
      e.preventDefault();
      e.stopImmediatePropagation();
      if(_atMentionFiles[_atMentionIdx]) _selectAtMentionFile(_atMentionFiles[_atMentionIdx]);
    }
  }, true); // capture để chạy trước handler Enter
}

function toggleMoreMenu(){
  const menu = document.getElementById('hmore-menu');
  const btn  = document.getElementById('hmore-btn');
  const open = menu.classList.toggle('open');
  btn.classList.toggle('open', open);
  btn.setAttribute('aria-expanded', open ? 'true' : 'false');
}
// Close on outside click
document.addEventListener('click', e=>{
  const wrap = document.getElementById('hmore-wrap');
  if(wrap && !wrap.contains(e.target)){
    document.getElementById('hmore-menu')?.classList.remove('open');
    const b = document.getElementById('hmore-btn');
    if(b){ b.classList.remove('open'); b.setAttribute('aria-expanded','false'); }
  }
});

// ── Automation Panel ──
function toggleAutoPanel(){
  document.body.classList.contains('auto-panel-open') ? closeAutoPanel() : openAutoPanel();
}
function openAutoPanel(){
  document.body.classList.add('auto-panel-open');
  const panel = document.getElementById('auto-panel');
  const btn   = document.getElementById('auto-panel-btn');
  if(panel){ panel.setAttribute('aria-hidden','false'); panel.removeAttribute('hidden'); }
  if(btn)  btn.setAttribute('aria-expanded','true');
  // close more menu if open
  document.getElementById('hmore-menu')?.classList.remove('open');
  const hb = document.getElementById('hmore-btn');
  if(hb){ hb.classList.remove('open'); hb.setAttribute('aria-expanded','false'); }
}
function closeAutoPanel(){
  document.body.classList.remove('auto-panel-open');
  const panel = document.getElementById('auto-panel');
  const btn   = document.getElementById('auto-panel-btn');
  if(panel) panel.setAttribute('aria-hidden','true');
  if(btn)  btn.setAttribute('aria-expanded','false');
}

// ══════════════════════════════════════════
// ── SKILLS ──
// ══════════════════════════════════════════
const SKILLS_KEY = 'ai_agent_skills';
const SKILL_ACTIVE_KEY = 'ai_agent_active_skill';

const SKILL_ICONS = ['🤖','💻','🐍','🌐','📊','✍️','🔍','🎨','📱','🔧','🧠','📝','🚀','🔐','📈','🎯','🗂️','⚡','🌍','🎓'];

const DEFAULT_SKILLS = [
  {
    id: 'python-dev', icon: '🐍', name: 'Python Dev',
    desc: 'Viết code Python sạch, có type hints, docstring',
    prompt: 'Bạn là chuyên gia Python. Luôn viết code với type hints, docstring, và PEP8. Giải thích code bằng tiếng Việt. Ưu tiên readability và best practices.'
  },
  {
    id: 'content-writer', icon: '✍️', name: 'Viết Content SEO',
    desc: 'Viết bài chuẩn SEO + Internal Linking chiến lược',
    prompt: `Bạn là Senior SEO Content Strategist với 10+ năm kinh nghiệm thực chiến, chuyên về Content Marketing và Technical SEO. Mỗi bài viết bạn tạo ra phải đạt chuẩn để rank Top 3 Google và tối ưu toàn bộ hệ thống internal linking.

═══════════════════════════════════════
## PHẦN 1 — CẤU TRÚC BÀI VIẾT CHUẨN SEO
═══════════════════════════════════════

### 1. Title Tag (Thẻ tiêu đề)
- Đặt từ khóa chính ở vị trí đầu (Power Position)
- Độ dài: 50-60 ký tự (tránh bị cắt trên SERP)
- Công thức hiệu quả: [Từ khóa chính] + [Lợi ích/Số liệu] + [Năm nếu cần]
- Ví dụ: "Học SEO từ A-Z: Lộ trình 90 ngày cho người mới 2025"
- Tránh: Keyword stuffing, Click-bait quá mức, Trùng với trang khác

### 2. Meta Description
- Độ dài: 150-158 ký tự (Google thường cắt ở đây)
- Phải chứa: từ khóa chính + 1 từ khóa phụ + CTA rõ ràng
- Công thức: [Hook câu hỏi/vấn đề] + [Giải pháp bài viết cung cấp] + [CTA]
- Ví dụ: "Chưa biết SEO bắt đầu từ đâu? Hướng dẫn chi tiết từng bước từ keyword research đến link building. Đọc ngay để tránh sai lầm phổ biến!"

### 3. Cấu trúc Heading (Phân cấp nội dung)
- **H1**: Duy nhất 1 thẻ, chứa từ khóa chính, khác với Title Tag 15-20%
- **H2**: 3-6 mục chính, mỗi mục chứa 1 từ khóa LSI hoặc từ khóa phụ
- **H3**: Mục con chi tiết, dùng long-tail keyword hoặc câu hỏi người dùng hay tìm
- **H4-H6**: Phân cấp sâu hơn nếu nội dung phức tạp
- Quy tắc: Không nhảy cấp (H2 → H4), mỗi heading phải standalone có nghĩa

### 4. Nội dung (Body Content)
- **Đoạn mở đầu (Introduction)**: Từ khóa chính trong 100 từ đầu tiên; nêu vấn đề → hứa hẹn giải pháp; hook mạnh trong 2 câu đầu
- **Mật độ từ khóa**: 1.0-1.5% (không nhồi nhét); từ khóa chính xuất hiện tự nhiên ở intro, 1-2 heading, kết luận
- **LSI Keywords**: Rải đều toàn bài; dùng công cụ: Google "People Also Ask", "Related Searches"
- **Cấu trúc đoạn văn**: 2-4 câu/đoạn; câu ngắn 15-20 từ; 1 ý chính/đoạn
- **Visual elements**: Bullet lists, numbered lists, bold text, table so sánh khi phù hợp
- **External linking**: 2-3 link đến nguồn uy tín (.gov, .edu, nghiên cứu, báo lớn); mở tab mới (target="_blank")

### 5. E-E-A-T (Experience · Expertise · Authoritativeness · Trustworthiness)
- **Experience**: Chia sẻ kinh nghiệm thực tế, case study cụ thể, số liệu thực
- **Expertise**: Giải thích chuyên sâu, dùng thuật ngữ chuyên ngành đúng chỗ
- **Authority**: Trích dẫn chuyên gia, nghiên cứu có nguồn gốc rõ ràng
- **Trust**: Cập nhật thông tin mới nhất, nêu rõ ngày viết/cập nhật, tránh thông tin sai lệch

### 6. Search Intent Alignment
- **Informational**: Giải thích toàn diện, định nghĩa rõ, ví dụ cụ thể → bài hướng dẫn dài
- **Navigational**: Focus vào brand/sản phẩm cụ thể → trang landing page
- **Commercial Investigation**: So sánh ưu/nhược, bảng so sánh, rating → review bài
- **Transactional**: CTA mạnh, nút hành động, giá trị đề nghị rõ ràng → trang dịch vụ/sản phẩm

### 7. Featured Snippet Optimization
- **Paragraph snippet**: Định nghĩa trả lời trực tiếp trong 40-60 từ, ngay sau H2 liên quan
- **List snippet**: Numbered list cho how-to (tối đa 8 bước); bullet list cho "top X" (6-8 items)
- **Table snippet**: Bảng so sánh với header rõ ràng (ít nhất 3 cột, 4+ hàng)
- **FAQ schema**: 4-6 câu hỏi thường gặp cuối bài với câu trả lời ngắn 50-80 từ

### 8. Readability & UX
- Flesch Reading Ease score: 50-70 (phù hợp người Việt đọc nội dung chuyên môn)
- Transition words: "Tuy nhiên", "Vì vậy", "Ngoài ra", "Cụ thể hơn", "Quan trọng hơn"
- Sử dụng active voice >80% câu
- Tránh jargon không giải thích, viết tắt phải có chú thích lần đầu

═══════════════════════════════════════
## PHẦN 2 — INTERNAL LINKING STRATEGY (CHIẾN LƯỢC LIÊN KẾT NỘI BỘ)
═══════════════════════════════════════

### A. Mô hình Topic Cluster & Pillar Page

**Pillar Page (Trang trụ cột)**:
- 1 bài viết dài 3.000-5.000+ từ về chủ đề rộng (broad topic)
- Bao quát toàn bộ chủ đề ở mức tổng quan
- Nhận link từ TẤT CẢ cluster pages liên quan
- Ví dụ: "Hướng dẫn SEO toàn diện A-Z"

**Cluster Pages (Trang vệ tinh)**:
- Các bài viết chuyên sâu về subtopic cụ thể
- Đều link về Pillar Page của chủ đề
- Cross-link với nhau khi liên quan
- Ví dụ: "Keyword Research", "On-page SEO", "Link Building", "Technical SEO"

**Silo Structure**:
- Nhóm content theo chủ đề rõ ràng
- Link chỉ đi trong cùng silo (giữ link juice tập trung)
- Tránh link chéo giữa các silo không liên quan

### B. Quy tắc Mật độ Internal Link
- **Bài 1.000-1.500 từ**: 3-5 internal links
- **Bài 1.500-2.500 từ**: 5-8 internal links
- **Bài 2.500-4.000 từ**: 8-12 internal links
- **Pillar Page 4.000+ từ**: 12-20 internal links (link đến toàn bộ cluster)
- Quy tắc vàng: **1 internal link per 200-300 từ**
- Không link quá 2 lần đến cùng 1 URL trong 1 bài

### C. Chiến lược Anchor Text (Văn bản neo)

**5 loại anchor text cần đa dạng hóa**:

1. **Exact Match (Khớp chính xác)**: 5-10% tổng links
   - Anchor text = từ khóa chính của trang đích
   - Ví dụ: anchor "học SEO" → link đến trang "Hướng dẫn học SEO"
   - ⚠️ Dùng nhiều quá sẽ bị Google phạt

2. **Partial Match (Khớp một phần)**: 30-40% tổng links
   - Anchor chứa từ khóa nhưng có thêm từ bổ sung
   - Ví dụ: "cách học SEO hiệu quả", "kiến thức SEO cơ bản"
   - ✅ An toàn nhất, tự nhiên nhất

3. **LSI/Semantic Match (Ngữ nghĩa)**: 20-30% tổng links
   - Anchor là từ đồng nghĩa hoặc liên quan về ngữ nghĩa
   - Ví dụ: "tối ưu tìm kiếm", "kỹ thuật lên top Google"

4. **Branded (Thương hiệu)**: 10-15% tổng links
   - Dùng tên website/brand làm anchor
   - Ví dụ: "theo VnExpress", "nguồn từ Neil Patel"

5. **Generic/Navigational**: 10-15% tổng links
   - "tại đây", "xem thêm", "đọc tiếp", "tham khảo"
   - ⚠️ Không nên dùng quá nhiều vì không có giá trị SEO

**QUY TẮC VÀNG Anchor Text**:
- Anchor text phải mô tả ĐÚNG nội dung trang đích
- Không dùng anchor trùng nhau cho 2 URL khác nhau (confusing signals)
- Không dùng anchor quá chung chung cho link quan trọng ("click here", "link này")
- Anchor phải đọc tự nhiên trong câu văn, không gượng ép

### D. Nguyên tắc đặt Internal Link trong bài

**VỊ TRÍ đặt link**:
- ✅ **Trong body text** (contextual link): giá trị SEO cao nhất
- ✅ **Introduction** (200 từ đầu): link đến pillar page hoặc trang category
- ✅ **Sau H2/H3 quan trọng**: link đến bài chuyên sâu hơn về subtopic đó
- ✅ **Kết luận (Conclusion)**: link đến bài "bước tiếp theo" hoặc related content
- ⚠️ **Sidebar/Footer**: ít giá trị SEO hơn, Google ưu tiên contextual links

**LUỒNG Link Juice (Phân phối sức mạnh)**:
- Trang có PageRank cao (Homepage, Category page) → link xuống bài mới
- Bài mới → link về Pillar Page (đẩy authority lên pillar)
- Cluster pages → cross-link với nhau khi tự nhiên
- Orphan pages (trang cô đơn, không được link đến) = trang chết về SEO → PHẢI có ít nhất 1-2 link đến

**ƯU TIÊN link đến**:
1. Pillar Page của chủ đề (luôn link về trang trụ cột)
2. Trang category/tag liên quan
3. Bài viết chuyên sâu về subtopic vừa đề cập
4. Trang sản phẩm/dịch vụ nếu relevant
5. Bài viết mới cần được crawl (giúp Google discover nhanh hơn)

### E. Internal Link cho từng loại bài viết

**Bài Informational (Hướng dẫn, Giải thích)**:
- Link đến Pillar Page của chủ đề chính: 1-2 links
- Link đến bài chuyên sâu hơn về subtopic: 2-3 links
- Link đến bài ví dụ/case study liên quan: 1-2 links
- Link đến trang công cụ/tài nguyên: 1 link

**Bài Commercial/Review (So sánh, Đánh giá)**:
- Link đến trang sản phẩm/dịch vụ được đề cập: 1-2 links mỗi sản phẩm
- Link đến bài hướng dẫn sử dụng chi tiết: 1-2 links
- Link đến bài so sánh khác liên quan: 1-2 links

**Bài Transactional (Landing Page)**:
- Link đến trang FAQ: 1 link
- Link đến case study/testimonial: 1-2 links
- Link đến bài related products/services: 2-3 links

### F. Kiểm tra & Audit Internal Link

Khi đề xuất internal links, luôn xem xét:
- [ ] Anchor text có mô tả đúng trang đích không?
- [ ] Link có contextually relevant không?
- [ ] Mật độ link có vượt quá 1 link/200 từ không?
- [ ] Trang đích có bị noindex/nofollow không?
- [ ] Có broken link nào không?
- [ ] Trang đích có đang được crawl không (orphan check)?

═══════════════════════════════════════
## PHẦN 3 — QUY TRÌNH THỰC HIỆN
═══════════════════════════════════════

**Bước 1 — Keyword Research & Clustering**
- Xác định: Focus keyword (1) + Secondary keywords (2-4) + LSI keywords (8-15)
- Map search intent cho từng từ khóa
- Xác định bài này là Pillar Page hay Cluster Page

**Bước 2 — SERP Analysis**
- Xem 5 bài đang rank Top 5 cho từ khóa chính
- Phân tích: Độ dài trung bình, cấu trúc heading, loại nội dung (text/video/image)
- Tìm content gap: Thông tin họ chưa cover

**Bước 3 — Outline (Phải confirm trước khi viết)**
Cung cấp outline dạng:
\`\`\`
[Title Tag]: ...
[H1]: ...
[H2-1]: ... → Link đến: [trang liên quan]
  [H3-1a]: ...
  [H3-1b]: ...
[H2-2]: ...
...
[Internal links dự kiến]: 
  - "[anchor text]" → [URL/slug gợi ý] (vị trí: H2-2, paragraph 2)
\`\`\`

**Bước 4 — Viết nội dung**

**Bước 5 — SEO Checklist trước khi giao**

═══════════════════════════════════════
## PHẦN 4 — OUTPUT FORMAT CHUẨN
═══════════════════════════════════════

Mỗi bài viết phải xuất ra ĐẦY ĐỦ theo format sau:

---
**📌 SEO METADATA**
- **Title Tag** (≤60 ký tự): [...]
- **Meta Description** (150-158 ký tự): [...]
- **Slug URL** (lowercase, dashes, có từ khóa chính): /[...]
- **Focus Keyword**: [...]
- **Secondary Keywords**: [...], [...], [...]
- **LSI Keywords**: [...], [...], [...], [...], [...]
- **Search Intent**: [Informational/Commercial/Transactional/Navigational]
- **Loại trang**: [Pillar Page / Cluster Page / Landing Page]

---
**🔗 KẾ HOẠCH INTERNAL LINKING**

| # | Vị trí trong bài | Anchor Text | URL đích | Loại anchor | Ghi chú |
|---|---|---|---|---|---|
| 1 | Intro, câu 3 | [anchor] | /slug-trang-dich | Partial match | Link đến Pillar Page |
| 2 | Sau H2 "..." | [anchor] | /slug | LSI | Link đến bài chuyên sâu |
| 3 | ... | ... | ... | ... | ... |

- **Tổng internal links**: X links / Y từ ≈ Z từ/link ✅
- **Phân bổ anchor text**: X% exact · X% partial · X% LSI · X% generic

---
**📝 NỘI DUNG BÀI VIẾT**

[Full content ở đây — với internal links được đánh dấu dạng [[anchor text → /url]]]

---
**❓ FAQ SECTION** (cho FAQ schema)

**Q1**: [Câu hỏi liên quan đến từ khóa]
**A1**: [Trả lời ngắn 50-80 từ, tự nhiên, có thể chứa featured snippet]

[3-6 cặp Q&A]

---
**✅ SEO CHECKLIST**
- [ ] Từ khóa chính trong Title, H1, 100 từ đầu, kết luận
- [ ] Mật độ từ khóa 1-1.5%
- [ ] LSI keywords rải đều
- [ ] Internal links: X links, đa dạng anchor text
- [ ] External links: X links đến nguồn uy tín
- [ ] Ảnh có alt text chứa từ khóa
- [ ] Meta description ≤158 ký tự
- [ ] Không có keyword stuffing
- [ ] Readability: câu ngắn, đoạn văn 2-4 câu

═══════════════════════════════════════
## PHẦN 5 — NGUYÊN TẮC VÀNG
═══════════════════════════════════════

1. **People First, SEO Second**: Viết cho người đọc trước, sau đó tối ưu cho bot
2. **Context is King**: Internal link chỉ có giá trị khi thực sự liên quan đến nội dung xung quanh
3. **Anchor Diversity**: Không bao giờ dùng cùng 1 anchor text cho 2 URL khác nhau
4. **Link to Value**: Mỗi link phải đưa người đọc đến nơi có giá trị hơn, không chỉ để có link
5. **Orphan Page = Dead Page**: Mọi trang quan trọng phải được link đến ít nhất từ 1-3 trang khác
6. **Pillar First**: Bài nào cũng phải có ít nhất 1 link về Pillar Page của chủ đề
7. **Tiếng Việt tự nhiên**: Không viết gượng ép, anchor text phải chảy tự nhiên trong câu văn`
  },
  {
    id: 'data-analyst', icon: '📊', name: 'Phân tích dữ liệu',
    desc: 'Phân tích, visualize, insights từ data',
    prompt: 'Bạn là data analyst. Phân tích dữ liệu chi tiết, đưa ra insights có giá trị. Dùng Python/pandas khi cần. Trình bày kết quả rõ ràng bằng bảng và biểu đồ.'
  },
  {
    id: 'macos-expert', icon: '🖥️', name: 'macOS Expert',
    desc: 'Tối ưu thao tác máy: shell, AppleScript, GUI, tự động hóa an toàn và có thể kiểm chứng',
    prompt: `Bạn là chuyên gia điều khiển và tự động hóa macOS cấp cao. Nhiệm vụ: giúp người dùng thao tác nhanh hơn, ít lỗi hơn, dễ lặp lại và dễ gỡ lỗi — không chỉ “chạy được lệnh”.

## Triết lý
- Ưu tiên **một lần đúng**: suy nghĩ trạng thái hệ thống (phiên bản macOS, shell mặc định, quyền file, Full Disk Access / Automation nếu chạm GUI) trước khi đề xuất lệnh.
- **An toàn trước**: với xóa/sửa hàng loạt, sửa plist, launchd, cấu hình hệ thống — nêu rủi ro, gợi ý sao lưu (copy file, Time Machine, export cấu hình), tránh lệnh phá hoại không cần thiết.
- **Có thể kiểm chứng**: mỗi bước nên có tiêu chí thành công (exit code, file tồn tại, output mong đợi, process đang chạy).
- **Tối thiểu quyền**: chỉ dùng \`sudo\` khi thật sự cần; giải thích vì sao.

## Chọn công cụ (khi agent có tools)
- **run_shell**: file, process, mạng, \`defaults\`, \`plutil\`, \`osascript -e\` ngắn, \`log show\`, \`diskutil\`, \`networkQuality\`, v.v. — ưu tiên lệnh có sẵn trên macOS/BSD.
- **open_app** / **open -a**: mở app hoặc file bằng ứng dụng đích.
- **run_applescript**: điều khiển UI (System Events), Mail, Finder, Safari khi shell không đủ; viết script **có timeout ý niệm** (tránh vòng lặp vô hạn); xử lý “button không tìm thấy”.
- **browser_***: khi tác vụ là web; **screenshot_and_analyze** khi cần nhìn màn hình.
- **read_file** / **write_file**: script, plist, log — luôn xác định đường dẫn tuyệt đối hoặc \`~/\` rõ ràng.
- **notify**: thông báo kết quả tác vụ dài hoặc hẹn giờ (**schedule_task**).

## Shell & script
- Dùng **\`#!/usr/bin/env bash\` hoặc zsh** phù hợp; quote biến (\`"$var"\`), tránh word-splitting và pathname expansion không chủ ý.
- Kiểm tra lỗi: \`set -euo pipefail\` cho script dài; với lệnh đơn, đọc exit code và stderr.
- **Đường dẫn**: \`/usr/local\` vs Apple Silicon; \`which\`, \`command -v\`; tránh hard-code kiến trúc nếu có thể dùng \`uname -m\`.
- **Hiệu năng**: tránh subshell/pipeline thừa; \`find\` kết hợp \`-print0\` + \`xargs -0\` cho tên file lạ; cân nhắc song song chỉ khi an toàn (không ghi cùng file).

## AppleScript / tự động hóa GUI
- Dùng **tell application "System Events"** khi cần; chờ cửa sổ/menu xuất hiện; ưu tiên **accessibility** ổn định (AX) thay vì tọa độ click nếu được.
- Nếu AppleScript quá dài/khó bảo trì, tách bước hoặc kết hợp shell + \`osascript\`.

## Trình bày cho người dùng
- Trả lời bằng **tiếng Việt** rõ ràng; với lệnh/đường dẫn/code giữ nguyên ký tự kỹ thuật.
- Cấu trúc: **Mục tiêu → Các bước đánh số → Kết quả mong đợi → Cách kiểm tra / rollback ngắn**.
- Sau khi đề xuất lệnh, nêu **cách xác nhận** (ví dụ: \`echo $?\`, mở file log, kiểm tra process).
- Không bịa tên menu/button thực tế: nếu không chắc UI, nói rõ và đề xuất cách xác minh (screenshot, mô tả cửa sổ).

Luôn tối ưu để người dùng **làm ít thao tác thủ công hơn** trong khi vẫn kiểm soát được rủi ro.`
  },
];

let skills = [];
let activeSkill = null;

// Version stamp — tăng số này khi muốn force-reset default skills
const SKILLS_VERSION = '2';
const SKILLS_VER_KEY = 'ai_agent_skills_ver';

function loadSkills() {
  try {
    const saved = localStorage.getItem(SKILLS_KEY);
    const savedVersion = localStorage.getItem(SKILLS_VER_KEY);
    const savedSkills = saved ? JSON.parse(saved) : null;

    if(savedSkills && savedVersion === SKILLS_VERSION) {
      // Merge: luôn dùng DEFAULT_SKILLS mới nhất, giữ custom skills do user tạo
      const defaultIds = new Set(DEFAULT_SKILLS.map(s => s.id));
      const customSkills = savedSkills.filter(s => !defaultIds.has(s.id));
      skills = [...DEFAULT_SKILLS, ...customSkills];
    } else {
      // Version mới hoặc lần đầu — reset về default
      skills = [...DEFAULT_SKILLS];
      localStorage.setItem(SKILLS_VER_KEY, SKILLS_VERSION);
    }
    localStorage.setItem(SKILLS_KEY, JSON.stringify(skills));
  } catch(e) { skills = [...DEFAULT_SKILLS]; }
  try {
    const activeId = localStorage.getItem(SKILL_ACTIVE_KEY);
    activeSkill = activeId ? skills.find(s => s.id === activeId) || null : null;
  } catch(e) { activeSkill = null; }
  renderSkillBadge();
}

function saveSkillsToStorage() {
  localStorage.setItem(SKILLS_KEY, JSON.stringify(skills));
}

function setActiveSkill(skill) {
  activeSkill = skill;
  if(skill) localStorage.setItem(SKILL_ACTIVE_KEY, skill.id);
  else localStorage.removeItem(SKILL_ACTIVE_KEY);
  renderSkillBadge();
  renderSkillsGrid();
}

function renderSkillBadge() {
  const badge = document.getElementById('skill-active-badge');
  if(!badge) return;
  if(!activeSkill) { badge.classList.add('is-hidden'); return; }
  badge.classList.remove('is-hidden');
  badge.className='skill-badge active';
  badge.innerHTML=`
    <span class="skill-badge-icon">${activeSkill.icon}</span>
    <span class="skill-badge-name">${esc(activeSkill.name)}</span>
    <span class="skill-badge-clear" data-oculo="setActiveSkill" data-oculo-arg="null" data-oculo-stop title="Bỏ chọn kỹ năng">
      <svg viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
    </span>`;
}

function openSkills() {
  renderSkillsGrid();
  _openModalWithFocus('skills-modal');
}

function renderSkillsGrid() {
  const grid = document.getElementById('skills-grid');
  if(!grid) return;
  grid.innerHTML = skills.map(s => `
    <div class="skill-card ${activeSkill?.id===s.id?'selected':''}" data-oculo="selectSkillAndClose" data-oculo-arg="${encodeURIComponent(s.id)}">
      <div class="skill-card-actions">
        <button type="button" class="skill-card-btn" data-oculo="editSkill" data-oculo-arg="${encodeURIComponent(s.id)}" data-oculo-stop title="Sửa">
          <svg viewBox="0 0 24 24"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
        </button>
        <button type="button" class="skill-card-btn" data-oculo="deleteSkill" data-oculo-arg="${encodeURIComponent(s.id)}" data-oculo-stop title="Xóa" style="color:var(--red)">
          <svg viewBox="0 0 24 24"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/></svg>
        </button>
      </div>
      <div class="skill-card-icon">${s.icon}</div>
      <div class="skill-card-name">${esc(s.name)}</div>
      <div class="skill-card-desc">${esc(s.desc)}</div>
    </div>`).join('') +
    `<div class="skill-add-card" data-oculo="openSkillEditor" role="button" tabindex="0">
      <svg viewBox="0 0 24 24"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
      <span class="skill-add-label">Tạo kỹ năng mới</span>
    </div>`;
}

function selectSkillAndClose(id) {
  const skill = skills.find(s => s.id === id);
  setActiveSkill(skill || null);
  closeModal('skills-modal');
  // Thông báo nhỏ
  const badge = document.getElementById('skill-active-badge');
  if(badge){ badge.style.transform='scale(1.08)'; setTimeout(()=>badge.style.transform='',200); }
}

function openSkillEditor(id) {
  const skill = id ? skills.find(s => s.id === id) : null;
  document.getElementById('skill-editor-title').textContent = skill ? 'Sửa kỹ năng' : 'Tạo kỹ năng mới';
  document.getElementById('skill-editor-id').value = skill?.id || '';
  document.getElementById('skill-name').value = skill?.name || '';
  document.getElementById('skill-desc').value = skill?.desc || '';
  document.getElementById('skill-prompt').value = skill?.prompt || '';

  // Render icon picker
  const picker = document.getElementById('skill-icon-picker');
  picker.innerHTML = SKILL_ICONS.map(icon =>
    `<div class="skill-icon-opt ${skill?.icon===icon?'selected':''}" data-oculo="selectSkillIcon" data-oculo-arg="${encodeURIComponent(icon)}" role="button" tabindex="0">${icon}</div>`
  ).join('');
  if(!skill) picker.querySelector('.skill-icon-opt')?.classList.add('selected');

  _openModalWithFocus('skill-editor-modal');
}

function editSkill(id) {
  closeModal('skills-modal');
  setTimeout(() => openSkillEditor(id), 150);
}

function selectSkillIcon(el, icon) {
  el.closest('.skill-icon-picker').querySelectorAll('.skill-icon-opt').forEach(e=>e.classList.remove('selected'));
  el.classList.add('selected');
}

function saveSkill() {
  const id = document.getElementById('skill-editor-id').value;
  const name = document.getElementById('skill-name').value.trim();
  const desc = document.getElementById('skill-desc').value.trim();
  const prompt = document.getElementById('skill-prompt').value.trim();
  const iconEl = document.querySelector('.skill-icon-opt.selected');
  const icon = iconEl ? iconEl.textContent : '🤖';

  if(!name || !prompt) { showToast('Vui lòng nhập tên và system prompt.', 3500); return; }

  if(id) {
    const idx = skills.findIndex(s => s.id === id);
    if(idx >= 0) skills[idx] = {id, icon, name, desc, prompt};
    if(activeSkill?.id === id) activeSkill = skills[idx];
  } else {
    skills.push({id: 'skill_'+Date.now(), icon, name, desc, prompt});
  }
  saveSkillsToStorage();
  renderSkillBadge();
  closeModal('skill-editor-modal');
  setTimeout(() => openSkills(), 150);
}

function deleteSkill(id) {
  openConfirmModal({
    title: 'Xóa skill này?',
    message: 'Kỹ năng sẽ bị xóa khỏi danh sách. Bạn có thể tạo lại sau.',
    okText: 'Xóa',
    danger: true,
    onConfirm: ()=>{
      skills = skills.filter(s => s.id !== id);
      if(activeSkill?.id === id) setActiveSkill(null);
      saveSkillsToStorage();
      renderSkillsGrid();
    }
  });
}

function getActiveSkillPrompt() {
  return activeSkill?.prompt || '';
}

// ══════════════════════════════════════════
// ── TODO PANEL (Cursor-style) ──
// ══════════════════════════════════════════
const _todoPanel = document.getElementById('todo-panel');
const _todoBody  = document.getElementById('todo-body');
const _todoCount = document.getElementById('todo-count');

// [{id, label, status: 'pending'|'running'|'done'|'error'}]
let _todoItems = [];
let _todoAutoMode = false; // true = auto-tracking tool calls (no decomposition)
let _todoCurrentAutoIdx = -1;
let _todoHideTimer = null;

function showTodoPanel(){
  clearTimeout(_todoHideTimer);
  _todoPanel.classList.add('visible');
}
function hideTodoPanel(){
  _todoPanel.classList.remove('visible');
}
function _autoHideTodoPanel(){
  _todoHideTimer = setTimeout(hideTodoPanel, 2800);
}

function _renderTodoItems(){
  const doneCount = _todoItems.filter(t => t.status === 'done').length;
  const total = _todoItems.length;
  _todoCount.textContent = total ? `${doneCount}/${total}` : '';

  _todoBody.innerHTML = _todoItems.map((item, idx) => {
    let iconHtml = '';
    if(item.status === 'pending'){
      iconHtml = `<div class="todo-icon"><div class="todo-icon-pending"></div></div>`;
    } else if(item.status === 'running'){
      iconHtml = `<div class="todo-icon"><div class="todo-icon-running"></div></div>`;
    } else if(item.status === 'done'){
      iconHtml = `<div class="todo-icon todo-icon-done"><svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg></div>`;
    } else {
      iconHtml = `<div class="todo-icon todo-icon-error"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg></div>`;
    }
    return `<div class="todo-item ${item.status}" id="todo-item-${idx}">${iconHtml}<span class="todo-label">${esc(item.label)}</span></div>`;
  }).join('');
}

// Called when decomposition event fires (subtask list from AI)
function todoSetFromDecomposition(subtasks){
  _todoAutoMode = false;
  _todoItems = subtasks.map((t, i) => ({ id: i, label: t, status: 'pending' }));
  if(_todoItems.length > 0) _todoItems[0].status = 'running';
  _renderTodoItems();
  showTodoPanel();
}

// Called on tool_call when no decomposition — auto-build task list
function todoAutoAddTool(toolName, inputSummary){
  _todoAutoMode = true;
  const label = _makeToolLabel(toolName, inputSummary);
  // Gộp nhiều lần chụp màn hình liên tiếp thành một dòng (×N) — tránh list 15/16 toàn chụp ảnh
  if(toolName === 'screenshot_and_analyze' && _todoItems.length){
    const last = _todoItems[_todoItems.length - 1];
    if(last && last.toolName === 'screenshot_and_analyze'){
      last.repeatCount = (last.repeatCount || 1) + 1;
      last.label = `Chụp & phân tích màn hình (×${last.repeatCount})`;
      last.status = 'running';
      _todoCurrentAutoIdx = _todoItems.length - 1;
      _renderTodoItems();
      showTodoPanel();
      const el = document.getElementById(`todo-item-${_todoCurrentAutoIdx}`);
      el?.scrollIntoView({ block: 'nearest' });
      return;
    }
  }
  // Mark previous running as done
  if(_todoCurrentAutoIdx >= 0 && _todoItems[_todoCurrentAutoIdx]){
    _todoItems[_todoCurrentAutoIdx].status = 'done';
  }
  const newIdx = _todoItems.length;
  _todoItems.push({ id: newIdx, label, status: 'running', toolName });
  _todoCurrentAutoIdx = newIdx;
  _renderTodoItems();
  // Scroll to new item
  const el = document.getElementById(`todo-item-${newIdx}`);
  el?.scrollIntoView({ block: 'nearest' });
  showTodoPanel();
}

// Called on tool_result
function todoMarkCurrentDone(){
  if(_todoAutoMode){
    if(_todoCurrentAutoIdx >= 0 && _todoItems[_todoCurrentAutoIdx]){
      _todoItems[_todoCurrentAutoIdx].status = 'done';
      _renderTodoItems();
    }
  } else {
    // Find current running item and mark done, advance to next
    const runIdx = _todoItems.findIndex(t => t.status === 'running');
    if(runIdx >= 0){
      _todoItems[runIdx].status = 'done';
      if(runIdx + 1 < _todoItems.length){
        _todoItems[runIdx + 1].status = 'running';
      }
      _renderTodoItems();
    }
  }
}

// Reset panel state
function todoReset(){
  clearTimeout(_todoHideTimer);
  _todoItems = [];
  _todoAutoMode = false;
  _todoCurrentAutoIdx = -1;
  _renderTodoItems();
}

function _makeToolLabel(toolName, input){
  // Rút gọn URL thành "domain/path" dễ đọc
  function _fmtUrl(url){
    try{
      const u = new URL(url);
      const q = u.searchParams.get('q') || u.searchParams.get('query') || u.searchParams.get('search');
      if(q) return `Tìm "${decodeURIComponent(q).slice(0,35)}"`;
      const path = u.pathname.replace(/\/$/, '').slice(0,30);
      return u.hostname.replace('www.','') + (path && path!=='/' ? path : '');
    }catch{ return decodeURIComponent(url).slice(0,45); }
  }

  // Rút gọn đường dẫn file thành tên file
  function _fmtPath(p){
    return p.replace(/^.*[/\\]/, '').slice(0,40) || p.slice(0,40);
  }

  // Rút gọn lệnh shell
  function _fmtCmd(cmd){
    const c = cmd.trim().replace(/\s+/g,' ');
    const kw = c.split(' ')[0];
    const kwMap = {
      ls:'Liệt kê thư mục', curl:'Tải dữ liệu', python3:'Chạy Python',
      python:'Chạy Python', node:'Chạy Node.js', brew:'Homebrew',
      echo:'In ra', cat:'Đọc file', mkdir:'Tạo thư mục', rm:'Xóa file',
      cp:'Sao chép', mv:'Di chuyển', open:'Mở', grep:'Tìm kiếm',
      ps:'Xem tiến trình', kill:'Dừng tiến trình', df:'Dung lượng đĩa',
      top:'Tài nguyên hệ thống', ifconfig:'Mạng', ping:'Ping',
    };
    return kwMap[kw] || `Thực thi: ${c.slice(0,35)}`;
  }

  if(!input || typeof input === 'string'){
    const s = (input||'').slice(0,45);
    return toolName + (s ? `: ${s}` : '');
  }

  switch(toolName){
    case 'run_shell':           return _fmtCmd(input.cmd||'');
    case 'browser_navigate':    return `Mở ${_fmtUrl(input.url||'')}`;
    case 'browser_evaluate':    return 'Phân tích nội dung trang';
    case 'browser_fill':        return `Điền "${(input.value||'').slice(0,30)}"`;
    case 'browser_click':       return `Nhấn nút trên trang`;
    case 'browser_new_tab':     return input.url ? `Tab mới: ${_fmtUrl(input.url)}` : 'Mở tab mới';
    case 'read_file':           return `Đọc ${_fmtPath(input.path||'')}`;
    case 'write_file':          return `Lưu ${_fmtPath(input.path||'')}`;
    case 'screenshot_and_analyze': return `Chụp & phân tích màn hình`;
    case 'open_app':            return `Mở ${input.app_name||'ứng dụng'}`;
    case 'extract_data':        return 'Trích xuất dữ liệu có cấu trúc';
    default:                    return toolName.replace(/_/g,' ');
  }
}

// ══════════════════════════════════════════
// ── CONTEXT WINDOW METER ──
// ══════════════════════════════════════════
const CTX_LIMIT = 190000; // Claude Sonnet usable context (~200k)
let _ctxTokensTotal = 0;

function updateCtxMeter(inputTokens){
  _ctxTokensTotal = inputTokens;
  const pct = Math.min(100, Math.round(_ctxTokensTotal / CTX_LIMIT * 100));
  const meter = document.getElementById('ctx-meter');
  const fill  = document.getElementById('ctx-fill');
  const pctEl = document.getElementById('ctx-pct');
  const tokEl = document.getElementById('ctx-tokens');
  if(!meter) return;
  if(pct < 2){ meter.style.display='none'; return; }
  meter.style.display='flex';
  fill.style.width = pct + '%';
  fill.className = 'ctx-fill' + (pct > 80 ? ' danger' : pct > 50 ? ' warn' : '');
  pctEl.textContent = pct + '%';
  pctEl.className = 'ctx-pct' + (pct > 80 ? ' danger' : pct > 50 ? ' warn' : '');
  tokEl.textContent = `${(_ctxTokensTotal/1000).toFixed(1)}k / ${(CTX_LIMIT/1000).toFixed(0)}k`;
}

// ══════════════════════════════════════════
// ── FOLLOW-UP SUGGESTIONS ──
// ══════════════════════════════════════════
let _lastQuestion = '';
let _lastAnswer   = '';

/**
 * suggestions: array of string hoặc {text, type}
 * type: 'question' | 'action' — server trả về prefix để phân biệt
 * Prefix quy ước: "→ " = action, còn lại = question
 */
function _showFollowups(suggestions){
  if(!suggestions?.length) return;
  const wraps = [...msgsEl.querySelectorAll('.mwrap')].filter(w => w.querySelector('.mrow.agent'));
  const lastWrap = wraps[wraps.length - 1];
  if(!lastWrap) return;

  lastWrap.querySelectorAll('.followup-wrap').forEach(el => el.remove());
  _followupStore.clear();

  const div = document.createElement('div');
  div.className = 'followup-wrap';

  // Label — không cần nữa, chips tự nói lên ý nghĩa
  // Chips
  // Chips — phân biệt action (→) vs question (?)
  suggestions.forEach((s, i) => {
    const raw = typeof s === 'string' ? s : (s.text || '');
    const isAction = raw.startsWith('→ ') || raw.startsWith('> ');
    const displayText = isAction ? raw.replace(/^[→>]\s*/, '') : raw;
    const id = `fu_${++_followupIdCounter}`;
    _followupStore.set(id, displayText);
    const btn = document.createElement('button');
    btn.className = 'followup-chip' + (isAction ? ' followup-chip--action' : '');
    btn.style.animationDelay = `${i * 0.08}s`;
    // Icon: action = ⚡, question = ?
    const iconHtml = isAction
      ? `<svg class="fu-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>`
      : `<svg class="fu-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`;
    const span = document.createElement('span');
    span.innerHTML = iconHtml;
    btn.appendChild(span);
    btn.appendChild(document.createTextNode(displayText));
    btn.addEventListener('click', () => {
      suggest(_followupStore.get(id) || displayText, false);
      _followupStore.delete(id);
      div.remove();
    });
    div.appendChild(btn);
  });

  lastWrap.appendChild(div);
  scrollEnd(false);
}

// Store followup texts indexed to avoid onclick/HTML escaping issues
const _followupStore = new Map();
let _followupIdCounter = 0;

async function _fetchFollowups(question, answer, toolNames){
  if(!uxFollowupsEnabled()) return;
  if(!question || !answer) return;
  try{
    const _sfRes = await fetch('/suggest-followups',{
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({question, answer, tool_names: toolNames || []})
    });
    if(!_sfRes.ok) return;
    const d = await _sfRes.json();
    if(d.suggestions?.length) _showFollowups(d.suggestions);
  }catch(e){}
}

// ══════════════════════════════════════════
// ── AUTO-CONTINUE ──
// ══════════════════════════════════════════
function _showContinueBtn(){
  const wraps = [...msgsEl.querySelectorAll('.mwrap')].filter(w => w.querySelector('.mrow.agent'));
  const lastWrap = wraps[wraps.length - 1];
  if(!lastWrap) return;
  const div = document.createElement('div');
  div.className = 'continue-wrap';
  div.innerHTML = `<button type="button" class="continue-btn" data-oculo="_autoContinue">
    <svg viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3"/></svg>
    Tiếp tục tạo...
  </button>`;
  lastWrap.appendChild(div);
  scrollEnd(false);
}

function _autoContinue(btn){
  btn.closest('.continue-wrap').remove();
  // Remove followups too if present
  document.querySelectorAll('.followup-wrap').forEach(el=>el.remove());
  _suppressDraft = true;
  inputEl.value = '';
  _suppressDraft = false;
  // Send empty message to continue — backend will see conversation and continue
  const origText = inputEl.value;
  inputEl.value = '[CONTINUE]';
  send();
  inputEl.value = origText;
}

// ══════════════════════════════════════════
// ── SHORTCUTS PANEL ──
// ══════════════════════════════════════════
function openShortcuts(){
  _openModalWithFocus('shortcuts-modal');
}

// ══════════════════════════════════════════
// ── COLLAPSE TOOL CARDS AFTER DONE ──
// ══════════════════════════════════════════
// #9 Expand collapsed tool cards khi user click "Xem lại"
// Lưu items đã collapse để có thể restore
const _collapsedToolStore = new WeakMap();

function _collapseToolWraps(items){
  // Lọc các element còn trong DOM và chưa bị xóa
  const valid = items.filter(it => it?.el?.parentNode);
  if(!valid.length) return;

  // Lấy tên các công cụ đã dùng (không trùng)
  const toolNames = [...new Set(
    valid
      .filter(it => it.name && !['error','retry','parallel','verify','risk'].includes(it.name))
      .map(it => {
        const nameMap = {
          browser_navigate:'Tìm kiếm', browser_evaluate:'Phân tích',
          screenshot_and_analyze:'Chụp màn hình', browser_fill:'Điền form',
          browser_click:'Nhấp chuột', read_file:'Đọc file',
          write_file:'Lưu file', run_shell:'Terminal', open_app:'Mở app',
          extract_data:'Trích xuất',
        };
        return nameMap[it.name] || null;
      })
      .filter(Boolean)
  )].slice(0, 4);

  const toolCount = valid.filter(it => !['error','retry','parallel','verify','risk'].includes(it.name)).length;
  const hasError  = valid.some(it => it.name === 'error');

  // Lấy reference để insert summary sau
  const lastEl   = valid[valid.length - 1].el;
  const insertRef = lastEl.nextSibling;
  const parent   = lastEl.parentNode;

  // Animate collapse — dùng rAF để browser commit initial state trước khi animate
  valid.forEach(it => {
    const el = it.el;
    const h = el.scrollHeight;
    // Snapshot height + freeze
    el.style.overflow  = 'hidden';
    el.style.maxHeight = h + 'px';
    el.style.transition= 'none';
    // rAF: browser paints the snapshot, then we start transition to 0
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        el.style.transition = 'max-height .28s cubic-bezier(.4,0,.2,1), opacity .2s ease, margin .28s ease';
        el.style.maxHeight  = '0';
        el.style.opacity    = '0';
        el.style.marginTop  = '0';
        el.style.marginBottom = '0';
      });
    });
  });

  // Sau animation: clone → xóa wraps → chèn summary (clone để có thể mở lại)
  setTimeout(() => {
    const clones = valid.map(it => it.el.cloneNode(true));
    valid.forEach(it => it.el?.parentNode && it.el.remove());

    if(!toolCount && !hasError) return;

    const summary = document.createElement('div');
    summary.className = 'mwrap';
    const icon = hasError
      ? `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="var(--yellow)" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>`
      : `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>`;

    summary.innerHTML = `<div class="tool-summary-line">
      ${icon}
      <span>Đã gộp ${toolCount} bước</span>
      ${toolNames.length ? `<span class="tool-summary-names">· ${toolNames.join(' · ')}</span>` : ''}
      <button type="button" class="tool-summary-expand" data-oculo="_expandCollapsedTools" title="Mở lại chi tiết công cụ">
        <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
        Mở lại
      </button>
    </div>`;

    if(insertRef && insertRef.parentNode === parent){
      parent.insertBefore(summary, insertRef);
    } else if(parent){
      parent.appendChild(summary);
    }
    _collapsedToolStore.set(summary, { clones, insertRef, parent });
  }, 300);
}

function _expandCollapsedTools(btn){
  const summaryWrap = btn.closest('.mwrap');
  if(!summaryWrap) return;
  const stored = _collapsedToolStore.get(summaryWrap);
  if(!stored?.clones?.length || !stored.parent) return;
  const { clones, insertRef, parent } = stored;
  let ref = insertRef;
  for(let i = clones.length - 1; i >= 0; i--){
    parent.insertBefore(clones[i], ref);
    ref = clones[i];
  }
  summaryWrap.remove();
  scrollEnd(false);
}


// #7 Sidebar resize handle
(function initSidebarResize(){
  const sidebar = document.getElementById('sidebar');
  if(!sidebar) return;
  const handle = document.createElement('div');
  handle.id = 'sidebar-resize';
  sidebar.appendChild(handle);

  const MIN_W = 200, MAX_W = 420;
  let dragging = false, startX = 0, startW = 0;

  handle.addEventListener('mousedown', e => {
    dragging = true;
    startX = e.clientX;
    startW = sidebar.offsetWidth;
    document.body.style.cursor = 'col-resize';
    document.body.style.userSelect = 'none';
    e.preventDefault();
  });

  document.addEventListener('mousemove', e => {
    if(!dragging) return;
    const newW = Math.min(MAX_W, Math.max(MIN_W, startW + e.clientX - startX));
    sidebar.style.width = newW + 'px';
    // Update margin for content
    if(document.body.classList.contains('sidebar-open')){
      document.getElementById('messages').style.marginLeft = newW + 'px';
      document.getElementById('input-area').style.marginLeft = newW + 'px';
    }
    localStorage.setItem('sidebar_width', newW);
  });

  document.addEventListener('mouseup', () => {
    if(!dragging) return;
    dragging = false;
    document.body.style.cursor = '';
    document.body.style.userSelect = '';
  });

  // Restore saved width
  const saved = parseInt(localStorage.getItem('sidebar_width') || '0');
  if(saved >= MIN_W && saved <= MAX_W) sidebar.style.width = saved + 'px';
})();

// ── Keyboard shortcuts ──
document.addEventListener('keydown',e=>{
  if(e.key==='/'&&document.activeElement!==inputEl&&!e.ctrlKey&&!e.metaKey){e.preventDefault();inputEl.focus()}
  if((e.ctrlKey||e.metaKey)&&e.key==='k'){e.preventDefault();document.getElementById('clear-btn')?.click()}
  if((e.ctrlKey||e.metaKey)&&e.key==='1'){e.preventDefault();setViewMode('chat');inputEl.focus()}
  if((e.ctrlKey||e.metaKey)&&e.key==='2'){e.preventDefault();setViewMode('control');document.getElementById('cu-task').focus()}
  if((e.ctrlKey||e.metaKey)&&e.key==='f'){e.preventDefault();openSearch()}
  if((e.ctrlKey||e.metaKey)&&e.key==='n'){e.preventDefault();newChat()}
  if(e.altKey&&e.code==='Slash'){e.preventDefault();openShortcuts()}
  if(e.altKey && !e.ctrlKey && !e.metaKey && (e.key === 'm' || e.key === 'M')){
    e.preventDefault();
    toggleModelPicker();
  }
  if(e.key==='Escape'){
    if(closeModelPicker()){ e.preventDefault(); return; }
    closeSearch();
    if(document.getElementById('confirm-modal')?.classList.contains('open')){
      confirmModalCancel();
      return;
    }
    const opens = [...document.querySelectorAll('.modal-overlay.open')].filter(x=>x.id!=='confirm-modal');
    if(opens.length) closeModal(opens[opens.length-1].id);
  }
  if(e.key==='Enter'){
    const sb = document.getElementById('search-bar');
    const inSearch = document.activeElement && document.activeElement.closest && document.activeElement.closest('#search-bar');
    if(sb && sb.classList.contains('open') && inSearch){
      e.preventDefault();
      searchNav(e.shiftKey?-1:1);
    }
  }
});

// ══════════════════════════════════════════
// ── SEARCH ──
// ══════════════════════════════════════════
let searchMatches=[], searchIdx=0;

function openSearch(){
  const bar = document.getElementById('search-bar');
  bar.classList.add('open');
  document.getElementById('search-input').focus();
  document.getElementById('search-input').select();
}
function closeSearch(){
  document.getElementById('search-bar').classList.remove('open');
  clearSearchHighlights();
  document.getElementById('search-input').value='';
  document.getElementById('search-count').textContent='';
  searchMatches=[];
}
function clearSearchHighlights(){
  msgsEl.querySelectorAll('mark.sh').forEach(m=>{
    m.replaceWith(document.createTextNode(m.textContent));
  });
  // Normalize text nodes
  msgsEl.querySelectorAll('.bubble').forEach(b=>b.normalize());
}
function doSearch(query){
  clearSearchHighlights();
  searchMatches=[]; searchIdx=0;
  if(!query.trim()){ document.getElementById('search-count').textContent=''; return; }
  const q = query.toLowerCase();
  // #5 Search trong cả bubble và tool results, bỏ qua code blocks để tránh noise
  msgsEl.querySelectorAll('.bubble, .tresult-raw, .tresult-md').forEach(el=>{
    // Bỏ qua pre/code để tránh highlight trong code
    const skipTags = new Set(['PRE','CODE','SCRIPT','STYLE','BUTTON','MARK']);
    function _highlight(node){
      if(node.nodeType===3){
        const text=node.textContent, lower=text.toLowerCase();
        let idx=0, result='', found=false;
        while(true){
          const i=lower.indexOf(q,idx);
          if(i===-1){result+=esc(text.slice(idx));break;}
          result+=esc(text.slice(idx,i))+`<mark class="sh">${esc(text.slice(i,i+q.length))}</mark>`;
          idx=i+q.length; found=true;
        }
        if(found){
          const span=document.createElement('span');
          span.innerHTML=result;
          node.replaceWith(span);
        }
      } else if(node.nodeType===1 && !skipTags.has(node.tagName)){
        Array.from(node.childNodes).forEach(c=>_highlight(c));
      }
    }
    _highlight(el);
  });
  searchMatches = Array.from(msgsEl.querySelectorAll('mark.sh'));
  document.getElementById('search-count').textContent = searchMatches.length ? `1 / ${searchMatches.length}` : 'Không tìm thấy';
  if(searchMatches.length){ setActiveMatch(0); }
}
function setActiveMatch(i){
  searchMatches.forEach((m,j)=>m.classList.toggle('active',j===i));
  searchMatches[i]?.scrollIntoView({behavior:'smooth',block:'center'});
  document.getElementById('search-count').textContent=`${i+1} / ${searchMatches.length}`;
}
function searchNav(dir){
  if(!searchMatches.length) return;
  searchIdx=(searchIdx+dir+searchMatches.length)%searchMatches.length;
  setActiveMatch(searchIdx);
}
let _searchTimer = null;
document.getElementById('search-input').addEventListener('input',e=>{
  clearTimeout(_searchTimer);
  _searchTimer = setTimeout(()=>doSearch(e.target.value), 200);
});

// ══════════════════════════════════════════
// ── PAUSE / RESUME ──
// ══════════════════════════════════════════
let isPaused = false;
let pauseResolve = null;
const pauseBtn = document.getElementById('pause-btn');
const pauseIcon = document.getElementById('pause-icon');

function togglePause(){
  isPaused = !isPaused;
  pauseBtn.classList.toggle('paused', isPaused);
  pauseIcon.innerHTML = isPaused
    ? '<polygon points="5 3 19 12 5 21 5 3" fill="currentColor"/>'
    : '<rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/>';
  pauseBtn.title = isPaused
    ? 'Tiếp tục nhận sự kiện SSE'
    : 'Tạm dừng xử lý phía trình duyệt (hàng đợi sự kiện; không hủy yêu cầu trên server)';
  if(!isPaused && pauseResolve){ pauseResolve(); pauseResolve=null; }
}

function waitIfPaused(){
  if(!isPaused) return Promise.resolve();
  return new Promise(res=>{ pauseResolve=res; });
}

function _resumePauseIfHanging(){
  isPaused = false;
  if(pauseResolve){ pauseResolve(); pauseResolve=null; }
  if(pauseBtn) pauseBtn.classList.remove('paused');
  if(pauseIcon) pauseIcon.innerHTML = '<rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/>';
}

// ── Orb state management ──
const ORB_LABELS = {
  idle:     'Sẵn sàng',
  thinking: 'Đang suy nghĩ…',
  tool:     'Đang thực thi…',
  error:    'Có lỗi xảy ra',
};
function _setOrbLabel(state, toolName){
  const logo = document.getElementById('header-logo');
  if(!logo) return;
  const label = toolName
    ? (formatToolStatusHint(toolName) || ('Đang chạy: ' + toolName.replace(/_/g,' ')))
    : (ORB_LABELS[state] || '');
  logo.setAttribute('data-orb-label', label);
  logo.setAttribute('aria-label', 'Oculo — ' + label);
}
function _orbSetTool(toolName){
  document.body.classList.add('agent-tool');
  document.body.classList.remove('agent-error');
  _setOrbLabel('tool', toolName);
}
function _orbSetError(){
  document.body.classList.add('agent-error');
  document.body.classList.remove('agent-tool');
  _setOrbLabel('error');
}
function _orbSetThinking(){
  document.body.classList.remove('agent-tool','agent-error');
  _setOrbLabel('thinking');
}

function setStatus(on){
  busy=on;sendBtn.disabled=on;
  if(sdot) sdot.className='sdot'+(on?' busy':'');
  if(stext) stext.textContent=on?'Đang xử lý...':'Sẵn sàng';
  document.body.classList.toggle('agent-busy',!!on);
  if(!on){
    // Reset orb về idle khi xong
    document.body.classList.remove('agent-tool','agent-error');
    _setOrbLabel('idle');
  } else {
    _setOrbLabel('thinking');
  }
  const iArea=document.getElementById('input-area');
  if(iArea) iArea.classList.toggle('agent-active',!!on);
  if(!on) setAgentStatusLine('');
  abortBtn.classList.toggle('visible',on);
  pauseBtn.classList.toggle('visible',on);
  if(!on){ isPaused=false; pauseBtn.classList.remove('paused');
    pauseIcon.innerHTML='<rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/>'; }
  // Avatar thinking animation
  document.querySelectorAll('.av.agent').forEach(el=>el.classList.toggle('thinking',on));
  // #14 Eye gaze: thinking = look up, done = blink then center
  const root14 = document.documentElement;
  if(on){
    root14.classList.add('eye-thinking');
    root14.classList.remove('eye-done-blink');
  } else {
    root14.classList.remove('eye-thinking');
    root14.classList.add('eye-done-blink');
    setTimeout(()=>root14.classList.remove('eye-done-blink'), 300);
  }
  // #7 Sync input area height cho toast position
  _syncInputAreaHeight();
}

// ── Toast ──
// #7 Sync input area height để toast không bị che
function _syncInputAreaHeight(){
  const iArea = document.getElementById('input-area');
  if(iArea){
    const h = iArea.getBoundingClientRect().height;
    document.documentElement.style.setProperty('--input-area-h', h + 'px');
  }
}
// Sync khi resize
window.addEventListener('resize', _syncInputAreaHeight);
// Sync lần đầu sau load
requestAnimationFrame(_syncInputAreaHeight);

let toastTimer=null;
function showToast(msg,duration=2000){
  const t=document.getElementById('toast');
  if(!t) return;
  t.textContent=msg;t.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer=setTimeout(()=>t.classList.remove('show'),duration);
}

// ── PWA Service Worker ──
if('serviceWorker' in navigator){
  window.addEventListener('load', ()=>{
    navigator.serviceWorker.register('/static/sw.js', {scope: '/'})
      .catch(()=>{}); // fail silently
  });
}

// ── Send: gọi trực tiếp send() (không chỉ data-oculo — tránh môi trường không delegate được)
// ── Send button ripple ──
if(sendBtn){
  sendBtn.addEventListener('click',function(e){
    const rect=this.getBoundingClientRect();
    const r=document.createElement('span');
    r.className='ripple-wave';
    const size=Math.max(rect.width,rect.height)*2;
    r.style.cssText=`width:${size}px;height:${size}px;left:${e.clientX-rect.left-size/2}px;top:${e.clientY-rect.top-size/2}px`;
    this.appendChild(r);
    setTimeout(()=>r.remove(),500);
    send();
  },{passive:true});
}

// ── Init ──
loadHistory();   // sets history & rendered from localStorage SK/RK
loadSkills();
loadConversations();

// Initialize first conversation if none exist
if(!_conversations.length){
  const id='conv_'+Date.now();
  _conversations=[{
    id, title:'Cuộc hội thoại',
    history: history.slice(),    // dùng data đã load từ SK
    rendered: rendered.slice(),  // dùng data đã load từ RK
    createdAt:Date.now(), updatedAt:Date.now()
  }];
  saveConversations();
  _activeConvId=id;
} else {
  _activeConvId=_conversations[0].id;

  // Sync: conv object trong localStorage có thể có rendered/history cũ/rỗng
  // → merge với data thực đang có trong SK/RK (loadHistory đã load rồi)
  const _initConv = _conversations.find(c=>c.id===_activeConvId);
  if(_initConv){
    const convRenderedLen = (_initConv.rendered||[]).length;
    const convHistoryLen  = (_initConv.history||[]).length;
    // Nếu SK/RK có nhiều hơn trong conv → conv bị stale, overwrite
    if(rendered.length > convRenderedLen || history.length > convHistoryLen){
      _initConv.history  = JSON.parse(JSON.stringify(history));
      _initConv.rendered = JSON.parse(JSON.stringify(rendered));
      _initConv.updatedAt = Date.now();
      saveConversations();
    } else {
      // Load data từ conv object vào biến active
      history  = JSON.parse(JSON.stringify(_initConv.history||[]));
      rendered = stripEmptyAgentFromRendered(JSON.parse(JSON.stringify(_initConv.rendered||[])));
    }
  }

  // Render messages của conversation đầu tiên ra DOM
  msgsEl.innerHTML = '';
  if(!rendered.length){
    const w = document.createElement('div'); w.className = 'mwrap';
    w.innerHTML = buildWelcomeHTML();
    msgsEl.appendChild(w);
  } else {
    const startIdx = Math.max(0, rendered.length - LAZY_LOAD_SIZE);
    _renderedStart = startIdx;
    if(startIdx > 0){
      const w = document.createElement('div'); w.className = 'mwrap'; w.id = 'load-more-wrap';
      w.innerHTML = `<div style="text-align:center;padding:10px"><button type="button" data-oculo="loadMoreHistory" style="background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:6px 14px;font-size:12px;color:var(--soft);cursor:pointer">Tải ${startIdx} tin nhắn cũ hơn</button></div>`;
      msgsEl.appendChild(w);
    }
    rendered.slice(startIdx).forEach(item => {
      if(item.role==='user') renderUser(item.text, item.ts, false, item.images);
      else if(item.role==='agent') renderAgent(item.text, item.ts, false);
    });
    removeEmptyAgentMessageWraps();
    scrollEnd(false);
  }
}
setViewMode(currentViewMode);
updateSidebarLayout();
initHeaderHeightSync();
fetchClientConfig()
  .then(() => { migrateModelIfExcluded(); return loadModelCatalog(); })
  .then(() => { enforceOllamaPolicy(); updateHeaderModelDisplay(); })
  .then(() => _checkForUpdateOnce())
  .catch(() => updateHeaderModelDisplay());
ActivitySidebar.init();
// Init mode indicator — no animation on first render
requestAnimationFrame(()=>requestAnimationFrame(()=>updateModeIndicator(false)));
window.addEventListener('resize', ()=>{
  updateModeIndicator(false);
  updateSidebarLayout();
  syncHeaderHeight();
});
window.addEventListener('load', ()=>{
  syncHeaderHeight();
  // Track input area height for toast positioning
  const inputArea = document.getElementById('input-area');
  if(inputArea && window.ResizeObserver){
    new ResizeObserver(entries => {
      for(const entry of entries){
        const h = Math.round(entry.contentRect.height);
        document.documentElement.style.setProperty('--input-area-h', h + 'px');
      }
    }).observe(inputArea);
    // Initial value
    document.documentElement.style.setProperty('--input-area-h', inputArea.offsetHeight + 'px');
  }
});
window.addEventListener('beforeunload', ()=>{
  if(saveHistoryTimer) { clearTimeout(saveHistoryTimer); saveHistory(); }
  if(saveRenderedTimer){ clearTimeout(saveRenderedTimer); saveRendered(); }
  // Always save current conv on exit — regardless of debounce timer
  saveCurrentConv();
  // Per-conv backup: lưu dữ liệu vào key riêng cho từng conv
  // (dùng để recover khi conv object bị mất data)
  if(_activeConvId && (history.length || rendered.length)){
    try{
      localStorage.setItem(
        `conv_bak_${_activeConvId}`,
        JSON.stringify({ history, rendered, ts: Date.now() })
      );
    }catch(e){}
  }
  // Gửi shutdown đến server khi đóng tab
  try {
    navigator.sendBeacon('/shutdown', new Blob(['{}'], {type:'application/json'}));
  } catch(e) {}
});

// ── Offline / Online indicator ──
(function initOfflineIndicator(){
  const banner = document.getElementById('offline-banner');
  if(!banner) return;
  function updateOnlineStatus(){
    const isOnline = navigator.onLine;
    banner.hidden = !!isOnline;
    // Đẩy header xuống khi banner hiện
    document.documentElement.style.setProperty('--offline-banner-h', isOnline ? '0px' : '36px');
  }
  window.addEventListener('online',  updateOnlineStatus);
  window.addEventListener('offline', updateOnlineStatus);
  updateOnlineStatus();
})();

// ══════════════════════════════════════════
// ── MULTI-AGENT PIPELINE ──
// ══════════════════════════════════════════
function openPipeline(){
  const out = document.getElementById('pipeline-output');
  out.hidden = true;
  out.innerHTML='';
  _openModalWithFocus('pipeline-modal');
}

async function runPipeline(){
  const task = document.getElementById('pipeline-task').value.trim();
  if(!task) return;
  const out = document.getElementById('pipeline-output');
  out.hidden = false;
  out.innerHTML='';
  document.getElementById('pipeline-run-btn').disabled=true;

  const stageInfo = {
    research: {label:'Agent Nghiên cứu', color:'research'},
    executor: {label:'Agent Thực thi',   color:'executor'},
    reviewer: {label:'Agent Đánh giá',   color:'reviewer'},
    error:    {label:'Lỗi',              color:'error'},
  };

  const stages = {};

  try {
    const res = await fetch('/pipeline', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({task})
    });
    if(!res.ok){
      const errText = await res.text().catch(()=>'');
      out.insertAdjacentHTML('beforeend', `<div class="pipeline-stage"><div class="ps-header error">Lỗi server ${res.status}: ${esc(errText.slice(0,200))}</div></div>`);
      document.getElementById('pipeline-run-btn').disabled=false;
      return;
    }
    if(!res.body){ out.insertAdjacentHTML('beforeend','<div class="pipeline-stage"><div class="ps-header error">Không nhận được dữ liệu từ server</div></div>'); document.getElementById('pipeline-run-btn').disabled=false; return; }
    const reader = res.body.getReader();
    const dec = new TextDecoder();
    let sseBuffer = '';

    while(true){
      const {done, value} = await reader.read();
      if(done) break;
      sseBuffer += dec.decode(value, {stream: true});
      const lines = sseBuffer.split('\n');
      sseBuffer = lines.pop() || '';
      for(const line of lines){
        if(!line.startsWith('data: ')) continue;
        let d; try{d=JSON.parse(line.slice(6))}catch{continue}

        const info = stageInfo[d.stage] || {label:d.stage, color:'executor'};

        if(d.status === 'running'){
          const el = document.createElement('div');
          el.className = 'pipeline-stage';
          el.id = `ps-${d.stage}`;
          el.innerHTML = `<div class="ps-header ${info.color}"><div class="ps-spinner"></div>${info.label}</div>`;
          out.appendChild(el);
          stages[d.stage] = el;
        } else if(d.status === 'done' && stages[d.stage]){
          const el = stages[d.stage];
          const header = el.querySelector('.ps-header');
          header.innerHTML = `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>${info.label}`;
          el.insertAdjacentHTML('beforeend', `<div class="ps-body">${safeMarkdown(d.content||'')}</div>`);
          if(d.tool_log && d.tool_log.length){
            const chips = d.tool_log.map(t=>`<span class="ps-tool-chip">${esc(t.tool)}</span>`).join('');
            el.insertAdjacentHTML('beforeend', `<div class="ps-tools">${chips}</div>`);
          }
        }
      }
    }
  } catch(e) {
    out.insertAdjacentHTML('beforeend', `<div class="pipeline-stage"><div class="ps-header error">Lỗi: ${esc(e.message)}</div></div>`);
  }
  document.getElementById('pipeline-run-btn').disabled=false;
}

function _flattenCheckpointMessages(msgs){
  const out = [];
  (msgs||[]).forEach(m=>{
    let text = '';
    if(typeof m.content === 'string') text = m.content;
    else if(Array.isArray(m.content)){
      text = m.content.filter(p=>p?.type==='text').map(p=>p.text||'').join('\n').trim();
    }
    if(!text) return;
    if(m.role==='user') out.push({role:'user', text, ts:''});
    else if(m.role==='assistant') out.push({role:'agent', text, ts:''});
  });
  return out;
}

async function openCheckpoints(){
  const list = document.getElementById('cp-list');
  if(list) list.innerHTML = '<p class="modal-loading-text">Đang tải...</p>';
  _openModalWithFocus('checkpoint-modal');
  try{
    const _cpRes = await fetch('/checkpoints');
    if(!_cpRes.ok){ if(list) list.innerHTML = '<p class="modal-error-text">Lỗi tải danh sách</p>'; return; }
    const rows = await _cpRes.json();
    if(!list) return;
    if(!rows.length){
      list.innerHTML = '<p class="modal-muted-text">Chưa có checkpoint. Checkpoint được tạo trước mỗi lần agent gọi công cụ (lưu trong RAM server, tối đa 20, TTL ~1 giờ).</p>';
      return;
    }
    list.innerHTML = rows.map(cp=>{
      const t = new Date((cp.ts||0)*1000);
      const label = esc(cp.label||cp.id||'');
      return `<div class="cp-row">
        <div class="cp-row-meta"><span class="cp-time">${esc(t.toLocaleString('vi-VN'))}</span><span class="cp-label">${label}</span></div>
        <button type="button" class="btn btn-primary btn--compact" data-oculo="restoreCheckpoint" data-oculo-arg="${encodeURIComponent(cp.id)}">Khôi phục</button>
      </div>`;
    }).join('');
  }catch(e){
    if(list) list.innerHTML = '<p class="modal-error-text">Lỗi tải danh sách</p>';
  }
}

async function restoreCheckpoint(cpId){
  if(!cpId) return;
  if(busy){
    showToast('Đợi agent xong rồi mới khôi phục');
    return;
  }
  try{
    const res = await fetch('/checkpoints/'+encodeURIComponent(cpId)+'/restore', { method:'POST' });
    const data = await res.json().catch(()=>({}));
    if(!res.ok || data.error){
      showToast(typeof data.error === 'string' ? data.error : 'Không khôi phục được');
      return;
    }
    closeModal('checkpoint-modal');
    history = data.messages || [];
    rendered = _flattenCheckpointMessages(history);
    msgsEl.innerHTML = '';
    _renderedStart = 0;
    if(!rendered.length){
      const w=document.createElement('div'); w.className='mwrap'; w.innerHTML=buildWelcomeHTML(); msgsEl.appendChild(w);
    } else {
      rendered.forEach(item=>{
        if(item.role==='user') renderUser(item.text, item.ts||nowTs(), false);
        else renderAgent(item.text, item.ts||nowTs(), false);
      });
    }
    removeEmptyAgentMessageWraps();
    saveCurrentConv();
    saveHistoryDebounced();
    saveRenderedDebounced();
    showToast('Đã khôi phục checkpoint');
    scrollEnd(false);
  }catch(e){
    showToast('Lỗi: '+(e.message||String(e)));
  }
}

// ══════════════════════════════════════════
// ── LONG-TERM MEMORY ──
// ══════════════════════════════════════════
async function openMemory(){
  const list = document.getElementById('mem-list');
  if(list){
    list.innerHTML = `<div class="mem-skel-wrap" aria-busy="true">
      <div class="mem-skel"></div><div class="mem-skel mem-skel--short"></div><div class="mem-skel"></div>
    </div>`;
  }
  _openModalWithFocus('memory-modal');
  await loadMemories();
}

async function loadMemories(){
  const list = document.getElementById('mem-list');
  try {
    const mems = await fetch('/memory').then(r=>r.json());
    if(!mems.length){
      list.innerHTML = `<div class="mem-empty">
        <div class="conv-empty-orb">${EYE_AVATAR_HTML}</div>
        <div class="conv-empty-title">Chưa có ghi nhớ nào</div>
        <div class="conv-empty-sub">Agent sẽ tự lưu thông tin quan trọng trong quá trình trò chuyện.</div>
      </div>`;
      return;
    }
    list.innerHTML = mems.map(m=>`
      <div class="mem-item">
        <button type="button" class="mem-del" data-oculo="deleteMemory" data-oculo-arg="${encodeURIComponent(String(m.id||m.metadata?.id||''))}"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></button>
        <div class="mem-content">${esc(m.content)}</div>
        <div class="mem-meta">${m.metadata?.timestamp?.slice(0,16)||''} · ${m.metadata?.category||'chung'}</div>
      </div>`).join('');
  } catch(e){ list.innerHTML=`<p class="modal-error-text">Lỗi: ${esc(e.message)}</p>`; }
}

async function searchMemories(query){
  if(!query.trim()){ await loadMemories(); return; }
  const list = document.getElementById('mem-list');
  try {
    const _srRes = await fetch('/memory/search',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({query})});
    if(!_srRes.ok){ if(list) list.innerHTML=`<p class="modal-error-text">Lỗi tìm kiếm: ${_srRes.status}</p>`; return; }
    const results = await _srRes.json();
    if(!results.length){ if(list) list.innerHTML='<p class="modal-muted-text">Không tìm thấy kết quả.</p>'; return; }
    if(list) list.innerHTML = results.map(r=>`
      <div class="mem-item">
        <button type="button" class="mem-del" data-oculo="deleteMemory" data-oculo-arg="${encodeURIComponent(String(r.id||r.metadata?.id||''))}"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></button>
        <div class="mem-content">${esc(r.content)}</div>
        <div class="mem-meta">${r.metadata?.timestamp?.slice(0,16)||''} · độ liên quan: ${(1-(r.distance||0)).toFixed(2)}</div>
      </div>`).join('');
  } catch(e){ if(list) list.innerHTML=`<p class="modal-error-text">Lỗi: ${esc(e.message)}</p>`; }
}

async function addMemoryManual(){
  const input = document.getElementById('mem-add-input');
  const content = input?.value.trim();
  if(!content) return;
  try {
    const r = await fetch('/memory',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({content,metadata:{category:'manual'}})});
    if(!r.ok){ showToast('Lỗi khi thêm bộ nhớ: ' + r.status); return; }
    if(input) input.value='';
    await loadMemories();
  } catch(e){ showToast('Lỗi khi thêm bộ nhớ'); }
}

async function deleteMemory(id, btn){
  if(!id) return;
  try {
    const r = await fetch(`/memory/${id}`,{method:'DELETE'});
    if(!r.ok){ showToast('Lỗi khi xóa: ' + r.status); return; }
    btn?.closest('.mem-item')?.remove();
  } catch(e){ showToast('Lỗi khi xóa bộ nhớ'); }
}

async function clearAllMemories(){
  try {
    await fetch('/memory/clear',{method:'POST'});
    await loadMemories();
  } catch(e){ showToast('Lỗi khi xóa bộ nhớ'); }
}

// ══════════════════════════════════════════
// ── PROACTIVE MONITORS ──
// ══════════════════════════════════════════
async function openMonitor(){
  _openModalWithFocus('monitor-modal');
  await loadMonitors();
  await loadMonitorEvents();
}

async function loadMonitors(){
  const list = document.getElementById('mon-list');
  try {
    const _monRes = await fetch('/monitors');
    if(!_monRes.ok){ if(list) list.innerHTML=`<p style="color:var(--error);font-size:13px">Lỗi tải monitor: ${_monRes.status}</p>`; return; }
    const mons = await _monRes.json();
    const keys = Object.keys(mons);
    if(!list) return;
    if(!keys.length){ list.innerHTML='<p style="color:var(--soft);font-size:13px">Chưa có monitor nào đang chạy.</p>'; return; }
    list.innerHTML = keys.map(id=>`
      <div class="mon-item">
        <span class="mon-type">${esc(mons[id].type)}</span>
        <span class="mon-path">${esc(mons[id].path||mons[id].type+' monitor')}</span>
        <button type="button" class="mon-del" data-oculo="stopMonitor" data-oculo-arg="${encodeURIComponent(id)}">
          <svg viewBox="0 0 24 24"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/></svg>
        </button>
      </div>`).join('');
  } catch(e){ if(list) list.innerHTML=`<p style="color:var(--error);font-size:13px">Lỗi: ${esc(e.message)}</p>`; }
}

async function loadMonitorEvents(){
  const list = document.getElementById('mon-events-list');
  try {
    const events = await fetch('/monitors/events').then(r=>r.json());
    if(!events.length){ list.textContent='Chưa có sự kiện nào.'; return; }
    list.innerHTML = events.slice(-10).reverse().map(e=>
      `<div style="padding:2px 0;border-bottom:1px solid var(--border)">[${e.ts?.slice(11,19)||''}] ${esc(e.type)}: ${esc(JSON.stringify(e.data).slice(0,80))}</div>`
    ).join('');
  } catch(e){}
}

async function addMonitor(){
  const type = document.getElementById('mon-type').value;
  const path = document.getElementById('mon-path').value;
  const id = 'mon_' + Date.now();
  let url, body;
  if(type==='file')     { url='/monitors/file';     body={id,path}; }
  else if(type==='calendar'){ url='/monitors/calendar'; body={id,interval_minutes:5}; }
  else                  { url='/monitors/system';   body={id,cpu_threshold:85,mem_threshold:85,interval:30}; }
  try {
    const r = await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}).then(r=>r.json());
    if(r.ok) await loadMonitors();
    else showToast('Lỗi: '+(r.error||'Không thêm được monitor'), 4500);
  } catch(e){ showToast('Lỗi: '+(e.message||e), 4500); }
}

async function stopMonitor(id){
  try {
    const r = await fetch(`/monitors/${id}`,{method:'DELETE'});
    if(!r.ok){ showToast('Lỗi khi dừng monitor: ' + r.status); }
  } catch(e){ showToast('Lỗi khi dừng monitor'); }
  await loadMonitors();
}

// ── Task History ──
const CU_HISTORY_KEY = 'cu_task_history';
let cuTaskHistory = (()=>{ try{ return JSON.parse(localStorage.getItem(CU_HISTORY_KEY)||'[]'); }catch{ return []; } })();
renderTaskHistory();

function cuSaveToHistory(task){
  cuTaskHistory = cuTaskHistory.filter(t => t !== task);
  cuTaskHistory.unshift(task);
  if(cuTaskHistory.length > 20) cuTaskHistory = cuTaskHistory.slice(0, 20);
  localStorage.setItem(CU_HISTORY_KEY, JSON.stringify(cuTaskHistory));
  renderTaskHistory();
}

function renderTaskHistory(){
  const wrap = document.getElementById('cu-history-wrap');
  const list = document.getElementById('cu-history-list');
  if(!wrap || !list) return;
  if(!cuTaskHistory.length){ wrap.style.display='none'; return; }
  wrap.style.display='block';
  list.innerHTML = cuTaskHistory.map((t,i) => `
    <div class="cu-history-item" data-oculo="cuSuggest" data-oculo-prompt="${encodeURIComponent(t)}">
      <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 8 12 12 14 14"/></svg>
      <span class="cu-history-text">${esc(t)}</span>
      <button type="button" class="cu-history-del" data-oculo="cuDeleteHistory" data-oculo-arg="${i}" data-oculo-stop title="Xóa">
        <svg viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
    </div>`).join('');
}

function cuDeleteHistory(i){
  cuTaskHistory.splice(i, 1);
  localStorage.setItem(CU_HISTORY_KEY, JSON.stringify(cuTaskHistory));
  renderTaskHistory();
}

function toggleTaskHistory(){
  const list = document.getElementById('cu-history-list');
  const chev = document.getElementById('cu-history-chev');
  const open = list.classList.toggle('open');
  chev.classList.toggle('open', open);
}

// ── Computer Use ──
// ══════════════════════════════════════════
let cuAbortCtrl = null;
let cuStep = 0;
let cuLastScreenshot = null;
let _cuElapsedTimer = null;
let _cuStartTs = 0;

function openComputerUse(){
  setViewMode('control');
  document.getElementById('cu-task').focus();
}

function cuSetStatus(state, text){
  const dot  = document.getElementById('cu-sdot');
  const stxt = document.getElementById('cu-status-text');
  if(dot) dot.className = 'cu-sdot' + (state==='busy'?' busy': state==='error'?' error':'');
  if(stxt) stxt.textContent = text;
}

function cuSetProgress(running){
  const bar = document.getElementById('cu-progress');
  if(running){ bar.className='cu-progress-bar indeterminate'; }
  else { bar.className='cu-progress-bar'; bar.style.width='0%'; }
}

function _cuStartElapsed(){
  _cuStartTs = Date.now();
  const el = document.getElementById('cu-elapsed');
  if(el) el.hidden = false;
  _cuElapsedTimer = setInterval(() => {
    const sec = Math.floor((Date.now() - _cuStartTs) / 1000);
    const el2 = document.getElementById('cu-elapsed');
    if(el2) el2.textContent = sec < 60 ? sec + 's' : Math.floor(sec/60) + 'm' + (sec%60) + 's';
  }, 1000);
}
function _cuStopElapsed(){
  clearInterval(_cuElapsedTimer);
  _cuElapsedTimer = null;
  const el = document.getElementById('cu-elapsed');
  if(el) el.hidden = true;
}

function cuSetRunning(running){
  const runBtn   = document.getElementById('cu-run-btn');
  const abortBtn = document.getElementById('cu-abort-btn');
  runBtn.disabled = running;
  abortBtn.classList.toggle('visible', running);
  cuSetProgress(running);
  if(running){ _cuStartElapsed(); }
  else { _cuStopElapsed(); }
  // Step counter overlay
  const stepEl = document.getElementById('cu-screen-step');
  if(stepEl) stepEl.hidden = !running;
}

function clearCuLog(){
  const log = document.getElementById('cu-log');
  log.innerHTML=`<div class="cu-empty-state" id="cu-log-empty">
    <div class="cu-empty-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg></div>
    <div class="cu-empty-title">Chưa có thao tác nào</div>
    <div class="cu-empty-sub">Nhập yêu cầu và nhấn Bắt đầu</div>
  </div>`;
  cuStep=0;
  const badge = document.getElementById('cu-step-badge');
  badge.hidden=true; badge.textContent='0';
}

function abortComputerUse(){
  if(cuAbortCtrl){ cuAbortCtrl.abort(); cuAbortCtrl=null; }
  cuSetRunning(false);
  cuSetStatus('', 'Đã dừng');
  cuAddEntry('error', CU_ICON.abort, 'Người dùng dừng');
}

function cuSuggest(text){
  document.getElementById('cu-task').value = text;
  document.getElementById('cu-task').focus();
}

function cuOpenLightbox(){
  if(!cuLastScreenshot) return;
  const lb = document.getElementById('cu-lightbox');
  document.getElementById('cu-lightbox-img').src = 'data:image/png;base64,' + cuLastScreenshot;
  lb.classList.add('open');
}
function cuCloseLightbox(){
  document.getElementById('cu-lightbox').classList.remove('open');
}
document.addEventListener('keydown', e=>{ if(e.key==='Escape') cuCloseLightbox(); });

// ── Fullscreen button ──
document.getElementById('cu-fullscreen-btn')?.addEventListener('click', () => cuOpenLightbox());

// ── Resize handle ──
(function initCuResize(){
  const handle = document.getElementById('cu-resize-handle');
  const dock   = document.getElementById('cu-dock');
  if(!handle || !dock) return;
  let startX = 0, startW = 0;
  handle.addEventListener('mousedown', e => {
    e.preventDefault();
    startX = e.clientX;
    startW = dock.offsetWidth;
    handle.classList.add('dragging');
    document.addEventListener('mousemove', onMove);
    document.addEventListener('mouseup', onUp);
  });
  function onMove(e){
    const delta = startX - e.clientX;
    const newW = Math.min(Math.max(startW + delta, 320), window.innerWidth * 0.7);
    dock.style.width = newW + 'px';
  }
  function onUp(){
    handle.classList.remove('dragging');
    document.removeEventListener('mousemove', onMove);
    document.removeEventListener('mouseup', onUp);
  }
})();

// ── Char count for cu-task ──
(function initCuCharCount(){
  const ta = document.getElementById('cu-task');
  const cc = document.getElementById('cu-char-count');
  if(!ta || !cc) return;
  ta.addEventListener('input', () => {
    const len = ta.value.length;
    cc.textContent = len > 50 ? len : '';
  });
  // Auto-resize
  ta.addEventListener('input', () => {
    ta.style.height = 'auto';
    ta.style.height = Math.min(ta.scrollHeight, 110) + 'px';
  });
  // Enter to submit (without shift)
  ta.addEventListener('keydown', e => {
    if(e.key === 'Enter' && !e.shiftKey && !e.isComposing){
      e.preventDefault();
      document.getElementById('cu-run-btn')?.click();
    }
  });
})();

// ── Computer Use SVG icons ──
const CU_ICON = {
  click:      `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 3l14 9-7 1-3 7z"/></svg>`,
  move:       `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="5 9 2 12 5 15"/><polyline points="9 5 12 2 15 5"/><polyline points="15 19 12 22 9 19"/><polyline points="19 9 22 12 19 15"/><line x1="2" y1="12" x2="22" y2="12"/><line x1="12" y1="2" x2="12" y2="22"/></svg>`,
  type:       `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 7 4 4 20 4 20 7"/><line x1="9" y1="20" x2="15" y2="20"/><line x1="12" y1="4" x2="12" y2="20"/></svg>`,
  key:        `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 2l-4 5-4-5"/></svg>`,
  scroll:     `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><polyline points="19 12 12 19 5 12"/></svg>`,
  screenshot: `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>`,
  wait:       `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>`,
  drag:       `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="5 9 2 12 5 15"/><polyline points="19 9 22 12 19 15"/><line x1="2" y1="12" x2="22" y2="12"/></svg>`,
  text:       `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>`,
  done:       `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>`,
  error:      `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>`,
  abort:      `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/></svg>`,
  action:     `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/></svg>`,
};

// Chuyển action type → class + icon + label gọn
function cuActionMeta(a){
  const t = a.action || a.type || '';
  const coord = a.coordinate ? `(${a.coordinate[0]},${a.coordinate[1]})` : '';
  const txt   = a.text ? `"${a.text.slice(0,40)}"` : '';
  if(t==='left_click'||t==='right_click'||t==='double_click'){
    const label = t==='double_click'?'DoubleClick': t==='right_click'?'RightClick':'Click';
    return {cls:'type-click', icon:CU_ICON.click, label:`${label} ${coord}`};
  }
  if(t==='mouse_move') return {cls:'type-move',       icon:CU_ICON.move,       label:`Move ${coord}`};
  if(t==='type')       return {cls:'type-type',       icon:CU_ICON.type,       label:`Type ${txt}`};
  if(t==='key')        return {cls:'type-key',        icon:CU_ICON.key,        label:`Key ${txt}`};
  if(t==='scroll')     return {cls:'type-scroll',     icon:CU_ICON.scroll,     label:`Scroll ${a.direction||''} ${coord}`};
  if(t==='screenshot') return {cls:'type-screenshot', icon:CU_ICON.screenshot, label:'Screenshot'};
  if(t==='wait')       return {cls:'type-screenshot', icon:CU_ICON.wait,       label:`Wait ${a.duration||1}s`};
  if(t==='left_click_drag') return {cls:'type-click', icon:CU_ICON.drag,       label:`Drag → ${coord}`};
  return {cls:'type-move', icon:CU_ICON.action, label:t||'action'};
}

function cuAddEntry(type, icon, text, step, thumbData){
  const log = document.getElementById('cu-log');
  // Remove empty state
  log.querySelector('.cu-empty-state')?.remove();

  const timeStr = new Date().toLocaleTimeString('vi-VN',{hour:'2-digit',minute:'2-digit',second:'2-digit'});
  const stepHtml = step ? `<span class="cu-step-badge">#${step}</span>` : '';
  const thumbHtml = thumbData
    ? `<img class="cu-thumb" src="data:image/png;base64,${thumbData}" alt="screenshot" data-oculo="cuShowThumb" data-oculo-thumb="${thumbData}" data-oculo-stop>`
    : '';

  log.insertAdjacentHTML('beforeend',
    `<div class="cu-entry type-${type}">
      <span class="cu-entry-icon">${icon}</span>
      <div class="cu-entry-body">
        <div class="cu-entry-text">${esc(text)}</div>
        <div class="cu-entry-meta">
          <span class="cu-entry-time">${timeStr}</span>
          ${stepHtml}
        </div>
        ${thumbHtml}
      </div>
    </div>`
  );
  log.scrollTop = log.scrollHeight;

  // Update step counter overlay on screen
  if(step){
    const stepNumEl = document.getElementById('cu-screen-step-num');
    if(stepNumEl) stepNumEl.textContent = step;
  }
}

function cuShowThumb(data){
  cuLastScreenshot = data;
  cuOpenLightbox();
}

async function runComputerUse(){
  const task = document.getElementById('cu-task').value.trim();
  if(!task) return;
  cuSaveToHistory(task);
  clearCuLog();
  cuSetRunning(true);
  cuSetStatus('busy','Đang khởi động...');

  const screenWrap = document.getElementById('cu-screen-wrap');
  const screen     = document.getElementById('cu-screenshot');
  const placeholder= document.getElementById('cu-screen-placeholder');
  const stepBadge  = document.getElementById('cu-step-badge');

  cuAbortCtrl = new AbortController();
  let lastScreenshotTs = 0;

  try {
    const res = await fetch('/computer-use',{
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({task}),
      signal: cuAbortCtrl.signal
    });
    if(!res.ok){
      const errText = await res.text().catch(()=>'');
      cuAddEntry('error', CU_ICON.error, `Lỗi server ${res.status}: ${errText.slice(0,200)}`);
      cuSetStatus('error','Có lỗi xảy ra');
      return;
    }
    if(!res.body){ cuAddEntry('error', CU_ICON.error, 'Không nhận được dữ liệu từ server'); cuSetStatus('error','Có lỗi xảy ra'); return; }
    const reader = res.body.getReader();
    const dec = new TextDecoder();
    let sseBuffer = '';

    while(true){
      const {done,value} = await reader.read();
      if(done) break;
      sseBuffer += dec.decode(value,{stream:true});
      const lines = sseBuffer.split('\n');
      sseBuffer = lines.pop() || '';

      for(const line of lines){
        if(!line.startsWith('data: ')) continue;
        let d; try{d=JSON.parse(line.slice(6))}catch{continue}

        if(d.type==='text' && d.content){
          cuAddEntry('text', CU_ICON.text, d.content);

        } else if(d.type==='action'){
          cuStep++;
          stepBadge.hidden=false;
          stepBadge.textContent = cuStep;
          const {cls,icon,label} = cuActionMeta(d.action||{});
          cuAddEntry(cls.replace('type-',''), icon, label, cuStep);
          cuSetStatus('busy',`Bước ${cuStep}: ${label}`);

        } else if(d.type==='screenshot'){
          const now = Date.now();
          cuLastScreenshot = d.data;
          // Update live preview (throttled)
          if(now - lastScreenshotTs > 500){
            lastScreenshotTs = now;
            screen.src = 'data:image/png;base64,' + d.data;
            if(!screen.classList.contains('visible')){
              screen.classList.add('visible');
              if(placeholder) placeholder.style.display='none';
              screenWrap.classList.remove('empty');
            }
          }

        } else if(d.type==='done'){
          cuAddEntry('done', CU_ICON.done, d.content||'Hoàn thành');
          cuSetStatus('', `Xong · ${cuStep} bước`);

        } else if(d.type==='error'){
          cuAddEntry('error', CU_ICON.error, d.content||'Lỗi không xác định');
          cuSetStatus('error','Có lỗi xảy ra');
        }
      }
    }
  } catch(e){
    if(e.name!=='AbortError'){
      cuAddEntry('error', CU_ICON.error, 'Lỗi kết nối: ' + e.message);
      cuSetStatus('error','Lỗi kết nối');
    }
  }
  cuSetRunning(false);
  cuAbortCtrl = null;
}

// ── Avatar agent: mắt — bám mục tiêu theo dt (mượt, không giật) + dao động sin liên tục ──
(function initAgentEyeRandom(){
  const root = document.documentElement;
  root.classList.add('agent-eye-random');
  let tx = 0;
  let ty = 0;
  let cx = 0;
  let cy = 0;
  let last = performance.now();
  /** Hướng nhìn chính: tốc độ bám (càng lớn càng “dứt khoát”, vẫn mượt) */
  const FOLLOW = 10.5;
  const SCALE = 3.48;
  const CONV = 0.052;
  /** Dao động nhỏ liên tục (sin) — không đổi random mỗi vài trăm ms (tránh lag / đuổi không kịp) */
  let drift = Math.random() * Math.PI * 2;

  function rand(a, b){ return a + Math.random() * (b - a); }

  function pickGazeTarget(){
    tx = (Math.random() * 2 - 1) * rand(0.22, 0.78);
    ty = (Math.random() * 2 - 1) * rand(0.22, 0.78);
    setTimeout(pickGazeTarget, rand(1700, 5400));
  }

  function scheduleBlink(){
    setTimeout(() => {
      root.classList.add('agent-eye-blink-on');
      setTimeout(() => root.classList.remove('agent-eye-blink-on'), 160);
      scheduleBlink();
    }, rand(2800, 9200));
  }

  const favLink = document.getElementById('app-favicon');
  const favCanvas = document.createElement('canvas');
  favCanvas.width = 32;
  favCanvas.height = 32;
  const favCtx = favCanvas.getContext('2d');
  let faviconFrame = 0;

  function paintDynamicFavicon(lx, ly, rx, ry, blink){
    if(!favLink || !favCtx) return;
    const W = 32;
    const ctx = favCtx;
    ctx.clearRect(0, 0, W, W);
    const st = getComputedStyle(root);
    const c1 = (st.getPropertyValue('--accent') || '#7c9fff').trim();
    const c2 = (st.getPropertyValue('--accent2') || '#a78bfa').trim();
    const rad = ((152 - 90) * Math.PI) / 180;
    const cx0 = W / 2;
    const cy0 = W / 2;
    const R = W * 0.72;
    const orbGrd = ctx.createLinearGradient(
      cx0 - Math.cos(rad) * R, cy0 - Math.sin(rad) * R,
      cx0 + Math.cos(rad) * R, cy0 + Math.sin(rad) * R
    );
    orbGrd.addColorStop(0, c1);
    orbGrd.addColorStop(0.42, '#5c6cf0');
    orbGrd.addColorStop(1, c2);
    ctx.fillStyle = orbGrd;
    ctx.beginPath();
    ctx.arc(cx0, cy0, W / 2 - 1, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = 'rgba(255,255,255,.14)';
    ctx.lineWidth = 1;
    ctx.stroke();

    const S = W / 34;
    const eyeY = 17 * S;
    const leftCx = 10 * S;
    const rightCx = 22 * S;
    const rScl = 5 * S;
    const rIris = 3 * S;
    const rPupil = 1.375 * S;

    function drawEye(cx, cy, ox, oy){
      if(blink){
        ctx.strokeStyle = 'rgba(255,255,255,.9)';
        ctx.lineWidth = Math.max(1, 1.15 * S);
        ctx.beginPath();
        ctx.moveTo(cx - rScl * 0.82, cy);
        ctx.lineTo(cx + rScl * 0.82, cy);
        ctx.stroke();
        return;
      }
      const sg = ctx.createRadialGradient(cx - rScl * 0.18, cy - rScl * 0.22, 0, cx, cy, rScl);
      sg.addColorStop(0, '#ffffff');
      sg.addColorStop(0.55, '#f0f3fb');
      sg.addColorStop(1, '#dce2f2');
      ctx.fillStyle = sg;
      ctx.beginPath();
      ctx.arc(cx, cy, rScl, 0, Math.PI * 2);
      ctx.fill();

      const ix = cx + ox * S;
      const iy = cy + oy * S;
      const ig = ctx.createRadialGradient(ix - rIris * 0.25, iy - rIris * 0.22, 0, ix, iy, rIris);
      ig.addColorStop(0, '#a8b8ff');
      ig.addColorStop(0.45, '#6b7fff');
      ig.addColorStop(1, '#2e3878');
      ctx.fillStyle = ig;
      ctx.beginPath();
      ctx.arc(ix, iy, rIris, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = '#0c0e18';
      ctx.beginPath();
      ctx.arc(ix, iy, rPupil, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = 'rgba(255,255,255,.82)';
      ctx.beginPath();
      ctx.arc(ix + rPupil * 0.28, iy - rPupil * 0.32, rPupil * 0.32, 0, Math.PI * 2);
      ctx.fill();
    }

    drawEye(leftCx, eyeY, lx, ly);
    drawEye(rightCx, eyeY, rx, ry);

    try{
      favLink.type = 'image/png';
      favLink.href = favCanvas.toDataURL('image/png');
    }catch(_){ /* ignore */ }
  }

  function frame(now){
    const dt = Math.min(0.045, Math.max(0.001, (now - last) / 1000));
    last = now;
    const a = 1 - Math.exp(-FOLLOW * dt);
    cx += (tx - cx) * a;
    cy += (ty - cy) * a;

    drift += dt * 1.05;
    const oxL = Math.sin(drift) * 0.052 + Math.sin(drift * 1.71 + 0.9) * 0.028;
    const oyL = Math.cos(drift * 0.89) * 0.045 + Math.sin(drift * 1.33 + 0.4) * 0.022;
    const oxR = Math.sin(drift * 1.03 + 1.1) * 0.05 + Math.sin(drift * 1.67) * 0.03;
    const oyR = Math.cos(drift * 0.92 + 0.5) * 0.044 + Math.sin(drift * 1.4 + 1.2) * 0.024;

    const lx = (cx + oxL - CONV) * SCALE;
    const ly = (cy + oyL) * SCALE * 0.91;
    const rx = (cx + oxR + CONV) * SCALE;
    const ry = (cy + oyR) * SCALE * 0.91;

    root.style.setProperty('--agent-eye-lx', lx + 'px');
    root.style.setProperty('--agent-eye-ly', ly + 'px');
    root.style.setProperty('--agent-eye-rx', rx + 'px');
    root.style.setProperty('--agent-eye-ry', ry + 'px');

    faviconFrame++;
    if(faviconFrame % 5 === 0){
      paintDynamicFavicon(lx, ly, rx, ry, root.classList.contains('agent-eye-blink-on'));
    }
    requestAnimationFrame(frame);
  }

  pickGazeTarget();
  scheduleBlink();
  requestAnimationFrame(frame);
})();

// ── data-oculo — gán sự kiện từ HTML (thay onclick / oninput inline) ──
(function oculoUiActions(){
  function decAttr(s){
    if(s==null||s==='') return '';
    try { return decodeURIComponent(s); } catch(_) { return s; }
  }
  function runStep(step, el, ev){
    const ix = step.indexOf(':');
    const fnName = ix === -1 ? step : step.slice(0, ix);
    const arg = ix === -1 ? undefined : step.slice(ix + 1);
    const fn = typeof window[fnName] === 'function' ? window[fnName] : null;
    if(!fn) return;
    if(fnName === 'toggleModelPicker' && ev) return void fn(ev);
    if(fnName === 'searchNav') return void fn(parseInt(arg, 10));
    if(arg !== undefined && arg !== '') return void fn(arg);
    fn();
  }
  document.addEventListener('click', (ev) => {
    const el = ev.target.closest('[data-oculo]');
    if(!el) return;
    if(el.hasAttribute('data-oculo-stop')) ev.stopPropagation();
    const spec = el.getAttribute('data-oculo');
    if(!spec) return;
    const promptEnc = el.getAttribute('data-oculo-prompt');
    if(promptEnc !== null && spec === 'suggest'){
      let p = (() => { try { return decodeURIComponent(promptEnc); } catch(_) { return promptEnc; } })();
      suggest(p, false);
      ev.preventDefault();
      return;
    }
    if(promptEnc !== null && spec === 'cuSuggest'){
      let p = (() => { try { return decodeURIComponent(promptEnc); } catch(_) { return promptEnc; } })();
      if(p.length >= 2 && ((p[0] === "'" && p[p.length - 1] === "'") || (p[0] === '"' && p[p.length - 1] === '"')))
        p = p.slice(1, -1);
      cuSuggest(p);
      ev.preventDefault();
      return;
    }
    const msgIdx = el.getAttribute('data-oculo-msg-idx');
    if(spec === 'copyMsgText' && msgIdx !== null){
      copyMsgText(el, parseInt(msgIdx, 10));
      ev.preventDefault();
      return;
    }
    if(spec === 'retryMsg'){
      retryMsg(el);
      ev.preventDefault();
      return;
    }
    if(spec === 'pinToMemory' && msgIdx !== null){
      pinToMemory(el, parseInt(msgIdx, 10));
      ev.preventDefault();
      return;
    }
    const convAttr = el.getAttribute('data-conv-id');
    const convId = convAttr !== null ? decAttr(convAttr) : null;
    if(spec === 'switchConversation' && convId !== null && convId !== ''){
      switchConversation(convId);
      ev.preventDefault();
      return;
    }
    if(spec === 'togglePinConv' && convId !== null && convId !== ''){
      togglePinConv(convId, ev);
      ev.preventDefault();
      return;
    }
    if(spec === 'startRenameConv' && convId !== null && convId !== ''){
      startRenameConv(convId, ev);
      ev.preventDefault();
      return;
    }
    if(spec === 'deleteConversation' && convId !== null && convId !== ''){
      deleteConversation(convId, ev);
      ev.preventDefault();
      return;
    }
    const rawArg = el.getAttribute('data-oculo-arg');
    if(spec === 'removeFile' && rawArg !== null){
      removeFile(parseInt(rawArg, 10));
      ev.preventDefault();
      return;
    }
    if(spec === '_resumeFromHere'){ _resumeFromHere(el); ev.preventDefault(); return; }
    if(spec === '_autoContinue'){ _autoContinue(el); ev.preventDefault(); return; }
    if(spec === '_expandCollapsedTools'){ _expandCollapsedTools(el); ev.preventDefault(); return; }
    if(spec === 'deleteMemory' && rawArg !== null){
      deleteMemory(decAttr(rawArg), el);
      ev.preventDefault();
      return;
    }
    if(spec === 'restoreCheckpoint' && rawArg !== null){
      restoreCheckpoint(decAttr(rawArg));
      ev.preventDefault();
      return;
    }
    if(spec === 'cuDeleteHistory' && rawArg !== null){
      cuDeleteHistory(parseInt(rawArg, 10));
      ev.preventDefault();
      return;
    }
    if(spec === 'cuShowThumb'){
      const td = el.getAttribute('data-oculo-thumb') || '';
      cuShowThumb(td);
      ev.preventDefault();
      return;
    }
    if(spec === 'setActiveSkill'){
      const v = rawArg === 'null' ? null : (rawArg != null ? decAttr(rawArg) : null);
      setActiveSkill(v);
      ev.preventDefault();
      return;
    }
    if(spec === 'selectSkillIcon' && rawArg !== null){
      selectSkillIcon(el, decAttr(rawArg));
      ev.preventDefault();
      return;
    }
    if(spec === 'selectSkillAndClose' && rawArg !== null){
      selectSkillAndClose(decAttr(rawArg));
      ev.preventDefault();
      return;
    }
    if(spec === 'editSkill' && rawArg !== null){
      editSkill(decAttr(rawArg));
      ev.preventDefault();
      return;
    }
    if(spec === 'deleteSkill' && rawArg !== null){
      deleteSkill(decAttr(rawArg));
      ev.preventDefault();
      return;
    }
    if(spec === 'openSkillEditor'){
      if(rawArg != null && rawArg !== '') openSkillEditor(decAttr(rawArg));
      else openSkillEditor();
      ev.preventDefault();
      return;
    }
    if(spec === 'stopMonitor' && rawArg !== null){
      stopMonitor(decAttr(rawArg));
      ev.preventDefault();
      return;
    }
    if(spec === 'loadMoreHistory'){ loadMoreHistory(); ev.preventDefault(); return; }
    if(spec === 'clearConvSearch'){
      const inp = document.getElementById('conv-search');
      if(inp){ inp.value=''; inp.focus(); }
      filterConvList('');
      ev.preventDefault();
      return;
    }
    if(spec === 'retryLastFailedSend'){ retryLastFailedSend(); ev.preventDefault(); return; }
    if(spec === 'copyLastChatError'){ copyLastChatError(); ev.preventDefault(); return; }
    if(spec === 'runCmdFromPre'){ runCmdFromPre(el); ev.preventDefault(); return; }
    if(spec === 'copyCodeBlock'){ copyCodeBlock(el); ev.preventDefault(); return; }

    for(const part of spec.split('|').map(s => s.trim()).filter(Boolean)){
      runStep(part, el, ev);
    }
  });
  document.addEventListener('dblclick', (ev) => {
    const row = ev.target.closest('.conv-item[data-conv-id]');
    if(!row || ev.target.closest('.conv-actions')) return;
    const id = decAttr(row.getAttribute('data-conv-id') || '');
    if(!id) return;
    startRenameConv(id, ev);
  });
  document.addEventListener('input', (ev) => {
    const t = ev.target;
    if(!(t instanceof HTMLInputElement) && !(t instanceof HTMLTextAreaElement)) return;
    if(t.id === 'conv-search') filterConvList(t.value);
    else if(t.id === 'mem-search') searchMemories(t.value);
    else if(t.id === 'model-picker-search') filterModelPicker(t.value);
  });

  // ── Oculo Eye Interaction (Pupil tracking cursor) ──
  document.addEventListener('mousemove', (e) => {
    const irises = document.querySelectorAll('.agent-eye-iris');
    if (!irises.length) return;
    irises.forEach(iris => {
      const rect = iris.parentElement.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;
      const angle = Math.atan2(e.clientY - centerY, e.clientX - centerX);
      const distance = Math.min(rect.width / 4, Math.hypot(e.clientX - centerX, e.clientY - centerY) / 12);
      const x = Math.cos(angle) * distance;
      const y = Math.sin(angle) * distance;
      iris.style.transform = `translate(${x}px, ${y}px)`;
    });
  });
})();
