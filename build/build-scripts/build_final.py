import json
LOGO = open('logo_b64.txt').read().strip()
s = open('build4.py').read()

def rep(a,b):
    global s
    assert a in s, "MISS: "+a[:110]
    s = s.replace(a,b)

# ================= CSS =================
rep("<title>Syniti · Consultant Performance Assessment</title>",
    "<title>Syniti · Skills Evaluation &amp; Enablement</title>")

rep('''  .legchip{border:1px solid var(--hair);border-radius:11px;padding:9px 12px;background:rgba(255,255,255,.5);min-width:98px;
    -webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}
  .legchip .lv{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:16px;color:var(--navy)}
  .legchip .nm{font-size:11.5px;color:var(--muted);margin-top:2px}''',
'''  .legend{gap:6px}
  .legchip{border:1px solid var(--hair);border-radius:9px;padding:5px 9px;background:rgba(255,255,255,.6);
    display:flex;align-items:baseline;gap:6px}
  .legchip .lv{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:13px;color:var(--navy)}
  .legchip .nm{font-size:10.5px;color:var(--muted)}''')

rep('''  .seg{display:inline-flex;border:1px solid var(--hair);border-radius:11px;overflow:hidden;background:rgba(255,255,255,.5);
    -webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}
  .seg button{appearance:none;border:0;background:transparent;color:var(--muted);cursor:pointer;
    font-family:'JetBrains Mono',monospace;font-size:12.5px;width:34px;height:32px;transition:.14s;
    border-right:1px solid rgba(100,116,139,.14)}
  .seg button:last-child{border-right:0}
  .seg button:hover{background:rgba(37,99,204,.08);color:var(--navy)}
  .seg button.sel{background:var(--grad);color:#fff;font-weight:600}
  .seg button.na{width:40px;font-size:10.5px}
  .seg button.na.sel{background:#8891AE;color:#fff}
  .seg.full{flex:1}
  .seg.full button{flex:1;width:auto}
  .seg.full button.na{flex:0 0 46px}''',
'''  .seg{display:inline-flex;gap:5px;background:transparent}
  .seg button{appearance:none;cursor:pointer;font-family:'JetBrains Mono',monospace;font-size:11.5px;font-weight:600;
    width:30px;height:28px;border-radius:8px;transition:.13s;color:var(--slate);
    background:rgba(255,255,255,.9);border:1px solid rgba(100,116,139,.24);box-shadow:0 1px 2px rgba(30,40,90,.06)}
  .seg button:hover{border-color:var(--violet);color:var(--navy);box-shadow:0 3px 8px -3px rgba(85,60,180,.35);transform:translateY(-1px)}
  .seg button.sel{background:var(--grad);color:#fff;border-color:transparent;box-shadow:0 4px 10px -4px rgba(85,60,180,.55)}
  .seg button.na{width:38px;font-size:10px;color:var(--muted)}
  .seg button.na.sel{background:#8891AE;color:#fff;border-color:transparent}
  .seg.full{flex:1;gap:6px}
  .seg.full button{flex:1;width:auto}
  .seg.full button.na{flex:0 0 46px}''')

rep('''  @media print{
    body{background:#fff}
    .aurora,.actbtns,.scopewrap,.importbanner,.seg,.segmented,.learnfilter,.lplan{display:none!important}''',
'''  .brandlogo{height:30px;width:auto;display:block}
  .topbar{padding-left:52px}
  .panel-h .sic{display:inline-flex;color:var(--blue)}
  .panel-h .sic svg{width:18px;height:18px;stroke:currentColor;fill:none;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
  .hchip{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.06em;text-transform:uppercase;color:var(--slate);font-weight:600;border:1px solid var(--hair);background:rgba(255,255,255,.55);border-radius:7px;padding:3px 9px}
  .minilab{font-family:'JetBrains Mono',monospace;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--slate);font-weight:600}
  .ovgrid{display:grid;grid-template-columns:1.12fr 1fr;gap:26px;align-items:start}
  .ovcol{min-width:0}
  .ovsub{font-family:'JetBrains Mono',monospace;font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--blue);font-weight:600;margin-bottom:12px}
  #sec-overview,#sec-scope,#sec-ai,#sec-skills,#sec-learning{scroll-margin-top:16px}
  .navtoggle{position:fixed;top:18px;left:18px;z-index:60;width:40px;height:40px;border-radius:11px;border:1px solid var(--hair);
    background:var(--glass);-webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px);cursor:pointer;display:grid;place-items:center;
    box-shadow:0 10px 24px -16px rgba(30,40,90,.5);transition:.16s}
  .navtoggle:hover{background:rgba(255,255,255,.9)}
  .navtoggle span{display:block;width:16px;height:2px;border-radius:2px;background:var(--navy);position:relative}
  .navtoggle span::before,.navtoggle span::after{content:"";position:absolute;left:0;width:16px;height:2px;border-radius:2px;background:var(--navy)}
  .navtoggle span::before{top:-5px}.navtoggle span::after{top:5px}
  .sidenav{position:fixed;top:0;left:0;bottom:0;width:226px;z-index:55;padding:72px 14px 22px;
    background:rgba(255,255,255,.74);-webkit-backdrop-filter:blur(24px) saturate(150%);backdrop-filter:blur(24px) saturate(150%);
    border-right:1px solid var(--hair);transform:translateX(-100%);transition:transform .28s cubic-bezier(.4,0,.2,1);overflow-y:auto}
  body.nav-open .sidenav{transform:translateX(0)}
  .sidenav .navttl{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--slate);font-weight:600;padding:0 12px 10px}
  .navlink{display:flex;align-items:center;gap:11px;padding:10px 12px;border-radius:11px;cursor:pointer;color:var(--muted);
    font-size:13px;font-weight:500;transition:.14s;text-decoration:none;margin-bottom:2px}
  .navlink:hover{background:rgba(255,255,255,.85);color:var(--navy)}
  .navlink.active{background:var(--grad);color:#fff;box-shadow:0 8px 18px -12px rgba(85,60,180,.6)}
  .navlink svg{width:17px;height:17px;flex:none;stroke:currentColor;fill:none;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
  .navlink .idx{font-family:'JetBrains Mono',monospace;font-size:10.5px;opacity:.65;margin-left:auto}
  .navbackdrop{position:fixed;inset:0;z-index:50;background:rgba(20,25,50,.28);opacity:0;pointer-events:none;transition:.28s}
  body.nav-open .navbackdrop{opacity:1;pointer-events:auto}
  @media(min-width:1180px){
    body.nav-open .navbackdrop{opacity:0;pointer-events:none}
    body.nav-open .shell{margin-left:236px}
  }
  @media(max-width:1080px){ .ovgrid{grid-template-columns:1fr} }
  @media print{
    body{background:#fff}
    .aurora,.navtoggle,.sidenav,.navbackdrop,.actbtns,.importbanner,.seg,.segmented,.learnfilter,.lplan{display:none!important}
    body.nav-open .shell{margin-left:0}''')

# ================= NAV insert (before shell) =================
IC_LAYOUT='<svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M9 9v11"/></svg>'
IC_SCOPE='<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/></svg>'
IC_AI='<svg viewBox="0 0 24 24"><path d="M12 3l1.7 4.5L18 9l-4.3 1.5L12 15l-1.7-4.5L6 9l4.3-1.5z"/><path d="M18.5 14.5l.8 2 .7.8-2 .7-.8 2-.7-2-2-.7 2-.7z"/></svg>'
IC_GRID='<svg viewBox="0 0 24 24"><rect x="4" y="4" width="7" height="7" rx="1.5"/><rect x="13" y="4" width="7" height="7" rx="1.5"/><rect x="4" y="13" width="7" height="7" rx="1.5"/><rect x="13" y="13" width="7" height="7" rx="1.5"/></svg>'
IC_CAP='<svg viewBox="0 0 24 24"><path d="M12 4l9 5-9 5-9-5z"/><path d="M6 11v5c0 1 2.7 2.5 6 2.5s6-1.5 6-2.5v-5"/></svg>'
IC_DOC='<svg viewBox="0 0 24 24"><path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4"/><path d="M9 13h6M9 16.5h6"/></svg>'

NAV=('<button class="navtoggle" id="navToggle" aria-label="Toggle sections"><span></span></button>\n'
'<div class="navbackdrop" id="navBackdrop"></div>\n'
'<nav class="sidenav" id="sidenav">\n'
'  <div class="navttl">Sections</div>\n'
'  <a class="navlink" href="#sec-overview">'+IC_LAYOUT+'<span>Details &amp; summary</span><span class="idx">01</span></a>\n'
'  <a class="navlink" href="#sec-scope">'+IC_SCOPE+'<span>Scope</span><span class="idx">02</span></a>\n'
'  <a class="navlink" href="#sec-ai">'+IC_AI+'<span>Guided review</span><span class="idx">03</span></a>\n'
'  <a class="navlink" href="#sec-skills">'+IC_GRID+'<span>Skills evaluation</span><span class="idx">04</span></a>\n'
'  <a class="navlink" href="#sec-learning">'+IC_CAP+'<span>Learning plan</span><span class="idx">05</span></a>\n'
'</nav>\n')
rep('<div class="aurora"><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div></div>\n<div class="shell">',
    '<div class="aurora"><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div></div>\n'+NAV+'<div class="shell">')

# ================= BODY replace (topbar .. learning card) =================
head='  <div class="topbar">'
disc_tail='so it lifts out cleanly for curation.</div>'
i=s.index(head)
j=s.index(disc_tail)+len(disc_tail)
k=s.index('</div>', j); j2=k+len('</div>')

NEWBODY='''  <div class="topbar">
    <img class="brandlogo" src="data:image/png;base64,__LOGO__" alt="Syniti">
    <span class="eyebrow-now">Syniti EMEA Data Quality</span>
    <span class="spacer"></span>
    <div class="actbtns">
      <button class="btn" id="importBtn"><span class="ic">&#8681;</span> Import previous</button>
      <button class="btn" id="printBtn"><span class="ic">&#128424;</span> Save / Print</button>
      <button class="btn primary" id="exportBtn"><span class="ic">&#8682;</span> Download form (.json)</button>
    </div>
    <input type="file" id="importFile" accept="application/json,.json" style="display:none">
  </div>

  <div class="eyebrow">Skills Evaluation &amp; Enablement</div>
  <h1>Rate the work. See the <span class="grad">gap to level.</span> Close it.</h1>
  <p class="lead">A structured evaluation that scores a consultant against the competency expectations for their C-level, classifies overall performance, captures feedback, and maps targeted learning to close each gap. Rate only what the engagement exercised - or generate the review with AI - then download the form or import a prior evaluation to track change.</p>

  <div class="card" id="sec-overview">
    <div class="panel-h"><span class="sic">__IC_DOC__</span><span class="n">01</span> Evaluation details &amp; summary</div>
    <div class="ovgrid">
      <div class="ovcol">
        <div class="ovsub">Details</div>
        <div class="fgrid">
          <div class="field"><label>Consultant name</label><input id="f_name" placeholder="First Last"></div>
          <div class="field"><label>Project / engagement</label><input id="f_project" placeholder="Project name"></div>
          <div class="field"><label>Reviewing lead</label><input id="f_lead" placeholder="Your name"></div>
          <div class="field"><label>C-Level (drives expectations)</label><select id="f_level"></select></div>
          <div class="field"><label>Evaluation type</label>
            <select id="f_type"><option>Regular</option><option>Mid-project</option><option>End of assignment</option><option>Promotion review</option></select></div>
          <div class="field"><label>Evaluation date</label><input id="f_date" type="date"></div>
        </div>
        <div style="margin-top:16px">
          <label class="minilab">Rating scale (0-5)</label>
          <div class="legend" id="legend"></div>
        </div>
        <div class="importbanner" id="cmpBanner">
          <span class="ic" style="color:var(--blue)">&#8644;</span>
          <span id="cmpText">Comparison loaded.</span>
          <button class="btn clr" id="clearCmp">Clear comparison</button>
        </div>
      </div>
      <div class="ovcol">
        <div class="ovsub">Live summary</div>
        <div class="bandbadge meets" id="bandBadge"><span class="dotm"></span><span id="bandLabel">Awaiting ratings</span></div>
        <div class="sumgrid" id="sumGrid" style="margin-top:14px"></div>
        <div class="barwrap" id="barWrap"></div>
        <div class="note" id="sumNote"></div>
      </div>
    </div>
  </div>

  <div class="card" id="sec-scope">
    <div class="panel-h"><span class="sic">__IC_SCOPE__</span><span class="n">02</span> Scope of evaluation</div>
    <div class="panel-sub">Turn on only the competency areas relevant to this project. Core areas are on by default - squads are optional.</div>
    <div class="scoperow" id="scopeRow"></div>
  </div>

  <div class="card" id="sec-ai">
    <div class="panel-h"><span class="sic">__IC_AI__</span><span class="n">03</span> Guided review <span class="samplebadge" style="color:var(--blue);border-color:rgba(37,99,204,.3);background:rgba(37,99,204,.08)">AI assistance</span></div>
    <div class="panel-sub">Prefer to talk it through? Generate a prompt, paste it into Copilot, Claude or ChatGPT, then bring the assistant's answer back to auto-fill the ratings. It uses only the areas you scoped above.</div>
    <div class="toolbar">
      <div class="segmented" id="modeSeg">
        <button data-m="interview" class="on">Interview me (Q&amp;A)</button>
        <button data-m="notes">Rate from my notes</button>
      </div>
    </div>
    <div id="notesWrap" class="field wide" style="display:none;margin-top:12px">
      <label>Your notes about the consultant</label>
      <textarea id="f_notes" placeholder="Write in plain language - what they did on the project, where they were strong, where they struggled. The assistant turns this into ratings."></textarea>
    </div>
    <div class="revgrid">
      <div class="revcol">
        <div class="revlabel">1 &middot; Copy this prompt</div>
        <textarea id="promptBox" class="promptbox" readonly></textarea>
        <button class="btn primary" id="copyPrompt" style="margin-top:10px"><span class="ic">&#9112;</span> Copy prompt</button>
      </div>
      <div class="revcol">
        <div class="revlabel">2 &middot; Paste the assistant's answer</div>
        <textarea id="pasteBox" class="promptbox" placeholder="Paste the JSON the assistant returns here, then apply..."></textarea>
        <button class="btn" id="applyAI" style="margin-top:10px"><span class="ic">&#10003;</span> Apply AI ratings</button>
      </div>
    </div>
    <div class="disc"><b>How it works:</b> the prompt lists your scoped competencies and the expected level for each, and asks the assistant for a small JSON block. Paste that block above and the matrix, classification and feedback fill in automatically - you can still adjust anything by hand. Nothing leaves your browser; you choose what to paste.</div>
  </div>

  <div class="card" id="sec-skills">
    <div class="panel-h"><span class="sic">__IC_GRID__</span><span class="n">04</span> Skills evaluation <span class="hchip">by competency area</span></div>
    <div class="panel-sub">Score each competency 0-5. The expectation for the level is shown, and the delta flags where the consultant is at, above, or below level. Use N/A where not exercised on this project.</div>
    <div class="toolbar" style="margin-bottom:4px">
      <div class="learnfilter" style="margin-left:0">
        <button id="collapseAll">Collapse all</button>
        <button id="expandAll">Expand all</button>
      </div>
    </div>
    <div id="matrix"></div>
    <div class="ovsub" style="margin-top:24px">Evaluation feedback &amp; classification</div>
    <div class="panel-sub">The classification is suggested from the ratings - adjust if your judgement differs, then add narrative feedback.</div>
    <div class="fgrid">
      <div class="field"><label>Overall classification</label>
        <select id="f_band">
          <option value="exceeds">Exceeds expectations</option>
          <option value="meets">Meets expectations</option>
          <option value="partial">Partially meets - development needed</option>
          <option value="below">Below expectations</option>
        </select></div>
      <div class="field"><label>Recommendation</label>
        <select id="f_reco">
          <option>On track at level</option>
          <option>Ready / near ready for promotion</option>
          <option>Solid contributor - keep developing</option>
          <option>Needs focused support</option>
          <option>Performance concern - action plan</option>
        </select></div>
      <div class="field"><label>Project rating (1-5)</label>
        <select id="f_proj"><option value="">-</option><option>5 - Outstanding</option><option>4 - Strong</option><option>3 - Solid</option><option>2 - Mixed</option><option>1 - Below par</option></select></div>
      <div class="field wide"><label>Key strengths</label><textarea id="f_str" placeholder="What the consultant did well on this engagement..."></textarea></div>
      <div class="field wide"><label>Development areas</label><textarea id="f_dev" placeholder="Where to focus to close the gap to level..."></textarea></div>
      <div class="field wide"><label>Project-specific feedback</label><textarea id="f_pf" placeholder="Context, standout moments, client feedback, notable deliverables..."></textarea></div>
    </div>
  </div>

  <div class="card" id="sec-learning">
    <div class="panel-h"><span class="sic">__IC_CAP__</span><span class="n">05</span> Learning plan <span class="samplebadge">Starter set</span></div>
    <div class="panel-sub">LinkedIn Learning, Coursera and Degreed mapped to each gap found above. A starter set for now - the catalog is a structured repo you can curate and extend later.</div>
    <div class="toolbar">
      <div class="segmented" id="provSeg">
        <button data-p="both" class="on">All sources</button>
        <button data-p="linkedin">LinkedIn</button>
        <button data-p="coursera">Coursera</button>
        <button data-p="degreed">Degreed</button>
      </div>
      <div class="learnfilter">
        <button id="onlyGaps" class="on">Only gap areas</button>
        <button id="allAreas">All scoped areas</button>
      </div>
    </div>
    <div id="learning"></div>
    <div class="planbox">
      <div class="pbh">Development plan (added to the downloaded form)</div>
      <div id="planList"><div class="emptyplan">Tick "Add to plan" on any suggestion to build a development plan for this consultant.</div></div>
    </div>
    <div class="disc"><b>Links &amp; repo:</b> items marked as a course open a verified LinkedIn Learning or Coursera page; items marked <b>search</b> open that provider's live results. <b>Degreed</b> links resolve inside your organisation's Degreed tenant (there are no public Degreed URLs). The whole catalog is one structured object keyed by competency area - update titles, links and providers there to curate over time, including pinning learning to individual competency refs.</div>
  </div>'''

NEWBODY=(NEWBODY.replace("__LOGO__",LOGO).replace("__IC_DOC__",IC_DOC).replace("__IC_SCOPE__",IC_SCOPE)
         .replace("__IC_AI__",IC_AI).replace("__IC_GRID__",IC_GRID).replace("__IC_CAP__",IC_CAP))
s = s[:i] + NEWBODY + s[j2:]

# ================= JS =================
rep('const PROV_NAME = {linkedin:"LinkedIn Learning", coursera:"Coursera"};',
    'const PROV_NAME = {linkedin:"LinkedIn Learning", coursera:"Coursera", degreed:"Degreed"};')
rep('const mc=document.getElementById("matrixCard"); if(mc) mc.scrollIntoView({behavior:"smooth",block:"start"});',
    'const mc=document.getElementById("sec-skills"); if(mc) mc.scrollIntoView({behavior:"smooth",block:"start"});')
rep('return {schema:"syniti-perf-assessment",version:2,',
    'return {schema:"syniti-skills-eval",version:3,')
rep('try{ const d=JSON.parse(rd.result); if(d.schema!=="syniti-perf-assessment")throw 0;',
    'try{ const d=JSON.parse(rd.result); if(!["syniti-skills-eval","syniti-perf-assessment"].includes(d.schema))throw 0;')
rep('a.href=url; a.download=`Assessment_${safe}_${data.meta.date||"draft"}.json`; a.click();',
    'a.href=url; a.download=`Evaluation_${safe}_${data.meta.date||"draft"}.json`; a.click();')

# append nav + collapse-all JS before init
init='renderScope(); renderMatrix(); renderPlan(); recompute();'
extra='''
// collapse / expand competency areas
if($("#collapseAll")) $("#collapseAll").onclick=()=>document.querySelectorAll("#matrix .areablock").forEach(b=>b.classList.remove("open"));
if($("#expandAll")) $("#expandAll").onclick=()=>document.querySelectorAll("#matrix .areablock").forEach(b=>b.classList.add("open"));
// side nav
const body=document.body;
function setNav(o){ body.classList.toggle("nav-open",o); }
if($("#navToggle")) $("#navToggle").onclick=()=>setNav(!body.classList.contains("nav-open"));
if($("#navBackdrop")) $("#navBackdrop").onclick=()=>setNav(false);
document.querySelectorAll(".navlink").forEach(a=>a.addEventListener("click",()=>{ if(window.innerWidth<1180) setNav(false); }));
if(window.innerWidth>=1180) setNav(true);
try{
  const secIds=["sec-overview","sec-scope","sec-ai","sec-skills","sec-learning"];
  const io=new IntersectionObserver((es)=>{es.forEach(e=>{ if(e.isIntersecting){ const id=e.target.id; document.querySelectorAll(".navlink").forEach(a=>a.classList.toggle("active",a.getAttribute("href")==="#"+id)); }});},{rootMargin:"-45% 0px -50% 0px",threshold:0});
  secIds.forEach(id=>{const el2=document.getElementById(id); if(el2) io.observe(el2);});
}catch(e){}

'''
rep(init, extra+init)

out='/mnt/user-data/outputs/Syniti_Skills_Evaluation_and_Enablement.html'
open(out,'w').write(s)
open('/home/claude/final.html','w').write(s)
print("built", len(s), "bytes ->", out)
