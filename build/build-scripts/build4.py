import json
comps = open('comps_min.json').read()

# ---- SAMPLE learning catalog (CURATION POINT: replace/extend later) ----
LEARNING = {
  "_meta": {"note":"Sample content - to be curated. Keyed by competency area; add ref-level overrides as needed."},
  "Syniti Platform: Technical (ADM)": [
    {"p":"degreed","t":"Syniti ADM Fundamentals","m":"Pathway · 3h · Foundational"},
    {"p":"linkedin","t":"SQL Essential Training","m":"Course · 4h 30m · Beginner"}
  ],
  "Syniti Platform: Technical (ADM-M)": [
    {"p":"degreed","t":"Syniti Migrate (ADM-M) Essentials","m":"Pathway · 4h · Intermediate"},
    {"p":"linkedin","t":"Data Migration Best Practices","m":"Course · 1h 45m · Intermediate"}
  ],
  "DQ-Specific Technical": [
    {"p":"linkedin","t":"Learning Data Profiling","m":"Course · 2h · Intermediate"},
    {"p":"degreed","t":"Root Cause Analysis for Data Quality","m":"Pathway · 2h 30m · Intermediate"}
  ],
  "DQ-Specific Functional": [
    {"p":"linkedin","t":"Data Governance Foundations","m":"Course · 1h 30m · Beginner"},
    {"p":"degreed","t":"Defining Data Quality KPIs","m":"Article set · 1h · Foundational"}
  ],
  "SAP Data Functional": [
    {"p":"degreed","t":"SAP Master Data Essentials","m":"Pathway · 5h · Intermediate"},
    {"p":"linkedin","t":"SAP Business Process Fundamentals","m":"Course · 2h 15m · Beginner"}
  ],
  "Delivery & Consulting": [
    {"p":"linkedin","t":"Consulting Foundations","m":"Course · 1h 20m · Beginner"},
    {"p":"linkedin","t":"Stakeholder Management Fundamentals","m":"Course · 55m · Intermediate"},
    {"p":"degreed","t":"Facilitating Effective Workshops","m":"Pathway · 2h · Intermediate"}
  ],
  "Squad-Delivery Excellence": [
    {"p":"degreed","t":"Writing Statements of Work","m":"Pathway · 1h 30m · Intermediate"},
    {"p":"linkedin","t":"Project Risk & RAID Management","m":"Course · 1h · Intermediate"}
  ],
  "Squad-dqOps": [
    {"p":"degreed","t":"DQ Operations Methodology (dqOps)","m":"Pathway · 2h · Intermediate"},
    {"p":"linkedin","t":"Quality Assurance Fundamentals","m":"Course · 1h 10m · Beginner"}
  ],
  "Squad-Harmonization": [
    {"p":"degreed","t":"Data Harmonization Techniques","m":"Pathway · 2h 30m · Advanced"},
    {"p":"linkedin","t":"Master Data Consolidation","m":"Course · 1h 30m · Intermediate"}
  ],
  "Squad-Source Cleansing": [
    {"p":"degreed","t":"Source Data Cleansing Methodology","m":"Pathway · 2h · Intermediate"},
    {"p":"linkedin","t":"Cleaning Data with Advanced Techniques","m":"Course · 2h · Intermediate"}
  ],
  "Squad-Cloud Data Quality": [
    {"p":"degreed","t":"Cloud Data Quality Foundations","m":"Pathway · 2h 30m · Intermediate"},
    {"p":"linkedin","t":"Data Quality in the Cloud","m":"Course · 1h 40m · Intermediate"}
  ],
  "Squad-Dashboarding & Analytics": [
    {"p":"linkedin","t":"Power BI Data Modeling","m":"Course · 3h · Intermediate"},
    {"p":"linkedin","t":"Advanced SQL for Data Analysts","m":"Course · 2h 30m · Advanced"}
  ],
  "Squad-Specialized and AI Driven": [
    {"p":"linkedin","t":"Generative AI & LLM Foundations","m":"Course · 1h 30m · Beginner"},
    {"p":"degreed","t":"Applied AI for Data Professionals","m":"Pathway · 3h · Intermediate"}
  ]
}
learning_json = open('learning.json').read()

HTML = r'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Syniti · Consultant Performance Assessment</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root{
    --navy:#1E2761; --blue:#2563CC; --violet:#8B5CF6; --teal:#0E9F6E; --amber:#E08A0B; --red:#DC5A54;
    --ink:#1E2440; --muted:#6B7492; --slate:#64748B;
    --hair:rgba(255,255,255,.65); --glass:rgba(255,255,255,.55); --glass-2:rgba(255,255,255,.42);
    --shadow:0 24px 60px -34px rgba(30,40,90,.4);
    --grad:linear-gradient(120deg,#2563CC,#8B5CF6);
    --li:#0A66C2; --dg:#E08A0B;
    --maxw:1360px;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  html{scroll-behavior:smooth}
  body{font-family:'Inter',-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--ink);
    background:#F6F8FE;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;min-height:100vh;
    position:relative;overflow-x:hidden;line-height:1.5}
  .aurora{position:fixed;inset:0;z-index:0;overflow:hidden;pointer-events:none}
  .blob{position:absolute;border-radius:50%;filter:blur(90px);opacity:.55}
  .blob.b1{width:660px;height:660px;top:-240px;left:-170px;background:radial-gradient(circle,#DBEAFE 0%,rgba(219,234,254,0) 70%)}
  .blob.b2{width:740px;height:740px;top:-180px;right:-230px;background:radial-gradient(circle,#EDE7FD 0%,rgba(237,231,253,0) 70%)}
  .blob.b3{width:700px;height:700px;bottom:-300px;left:26%;background:radial-gradient(circle,#D6F2E6 0%,rgba(214,242,230,0) 70%)}

  .shell{position:relative;z-index:1;max-width:var(--maxw);margin:0 auto;padding:32px 40px 120px}

  .topbar{display:flex;align-items:center;gap:16px;margin-bottom:30px;flex-wrap:wrap}
  .wordmark{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:21px;letter-spacing:.01em;
    background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
  .eyebrow-now{color:var(--slate);text-transform:uppercase;font-size:11px;letter-spacing:.2em;font-weight:600;
    font-family:'JetBrains Mono',monospace}
  .spacer{flex:1}
  .actbtns{display:flex;gap:9px;flex-wrap:wrap}

  .btn{appearance:none;cursor:pointer;font-family:'Inter',sans-serif;font-size:12.5px;font-weight:600;
    padding:9px 15px;border-radius:12px;transition:.16s;display:inline-flex;align-items:center;gap:7px;
    border:1px solid rgba(37,99,204,.22);background:var(--glass);color:var(--blue);
    -webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px)}
  .btn:hover{background:rgba(255,255,255,.75)}
  .btn:focus-visible{outline:2px solid var(--violet);outline-offset:2px}
  .btn.primary{background:var(--grad);border-color:transparent;color:#fff;box-shadow:0 10px 24px -14px rgba(85,60,180,.6)}
  .btn.primary:hover{filter:brightness(1.06)}
  .btn .ic{font-size:14px;line-height:1}

  .eyebrow{font-family:'JetBrains Mono',monospace;font-size:11.5px;letter-spacing:.2em;text-transform:uppercase;
    color:var(--slate);font-weight:600;margin-bottom:14px;display:flex;align-items:center;gap:12px}
  .eyebrow::before{content:"";width:28px;height:1px;background:var(--violet);opacity:.6}

  h1{font-family:'Space Grotesk',sans-serif;font-weight:700;line-height:1.03;letter-spacing:-.02em;
    font-size:clamp(30px,5vw,50px);color:var(--navy)}
  h1 .grad{background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
  .lead{color:var(--muted);line-height:1.6;font-size:16px;max-width:72ch;margin-top:16px}

  .card{background:var(--glass);border:1px solid var(--hair);border-radius:22px;box-shadow:var(--shadow);
    -webkit-backdrop-filter:blur(26px) saturate(150%);backdrop-filter:blur(26px) saturate(150%);
    padding:26px 28px;margin-top:22px}
  .panel-h{font-family:'Space Grotesk',sans-serif;font-weight:600;font-size:19px;margin-bottom:4px;color:var(--navy);
    display:flex;align-items:center;gap:11px}
  .panel-h .n{font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--blue);border:1px solid rgba(37,99,204,.25);
    border-radius:8px;padding:3px 8px;background:rgba(37,99,204,.06)}
  .panel-sub{color:var(--muted);font-size:13.5px;margin-bottom:20px;line-height:1.55}

  .fgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));gap:16px}
  .field label{display:block;font-family:'JetBrains Mono',monospace;font-size:10.5px;letter-spacing:.1em;
    text-transform:uppercase;color:var(--slate);font-weight:600;margin-bottom:7px}
  .field input,.field select,.field textarea{width:100%;background:rgba(255,255,255,.6);border:1px solid var(--hair);
    color:var(--ink);border-radius:12px;padding:11px 13px;font-family:'Inter',sans-serif;font-size:14px;transition:.16s;
    -webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}
  .field textarea{resize:vertical;min-height:82px;line-height:1.55}
  .field input:focus,.field select:focus,.field textarea:focus{outline:none;border-color:var(--violet);
    background:#fff;box-shadow:0 0 0 3px rgba(139,92,246,.12)}
  .field input::placeholder,.field textarea::placeholder{color:#A7AEC4}
  .field select{cursor:pointer;appearance:none;
    background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'><path d='M2 4l4 4 4-4' stroke='%2364748B' stroke-width='1.5' fill='none' stroke-linecap='round' stroke-linejoin='round'/></svg>");
    background-repeat:no-repeat;background-position:right 13px center;padding-right:34px}
  .field.wide{grid-column:1/-1}

  .legend{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}
  .legchip{border:1px solid var(--hair);border-radius:11px;padding:9px 12px;background:rgba(255,255,255,.5);min-width:98px;
    -webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}
  .legchip .lv{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:16px;color:var(--navy)}
  .legchip .nm{font-size:11.5px;color:var(--muted);margin-top:2px}

  .scoperow{display:grid;grid-template-columns:repeat(auto-fit,minmax(235px,1fr));gap:10px}
  .scopetile{border:1px solid var(--hair);border-radius:14px;padding:13px 15px;background:rgba(255,255,255,.45);
    cursor:pointer;display:flex;align-items:center;gap:12px;transition:.16s;text-align:left;font-family:inherit;color:inherit;
    -webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px)}
  .scopetile:hover{background:rgba(255,255,255,.7)}
  .scopetile.on{border-color:rgba(139,92,246,.4);background:rgba(255,255,255,.8);box-shadow:0 8px 20px -16px rgba(85,60,180,.5)}
  .scopetile .box{width:20px;height:20px;border-radius:6px;border:1.5px solid #B4BAD0;flex:none;display:grid;place-items:center;
    font-size:12px;color:#fff;transition:.16s}
  .scopetile.on .box{background:var(--grad);border-color:transparent}
  .scopetile .st{flex:1}
  .scopetile .st b{font-family:'Space Grotesk',sans-serif;font-weight:600;font-size:13.5px;display:block;color:var(--ink)}
  .scopetile .st span{font-size:11.5px;color:var(--slate);font-family:'JetBrains Mono',monospace}

  .areablock{border:1px solid var(--hair);border-radius:16px;margin-top:12px;overflow:hidden;background:rgba(255,255,255,.35)}
  .areahead{display:flex;align-items:center;gap:14px;padding:14px 18px;background:rgba(255,255,255,.5);cursor:pointer;
    border-bottom:1px solid transparent;transition:.16s}
  .areahead:hover{background:rgba(255,255,255,.7)}
  .areahead .at{font-family:'Space Grotesk',sans-serif;font-weight:600;font-size:15px;flex:1;color:var(--navy)}
  .areahead .chev{color:var(--slate);transition:.25s;font-size:12px}
  .areablock.open .areahead{border-bottom-color:var(--hair)}
  .areablock.open .chev{transform:rotate(90deg)}
  .areastat{font-family:'JetBrains Mono',monospace;font-size:11px;padding:4px 10px;border-radius:20px;
    border:1px solid var(--hair);color:var(--slate);white-space:nowrap;background:rgba(255,255,255,.5)}
  .areastat.pos{color:var(--teal);border-color:rgba(14,159,110,.35);background:rgba(14,159,110,.1)}
  .areastat.neg{color:var(--red);border-color:rgba(220,90,84,.35);background:rgba(220,90,84,.1)}
  .arearows{display:none}
  .areablock.open .arearows{display:block}

  .mgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(400px,1fr));gap:12px;padding:14px}
  .ctile{border:1px solid var(--hair);border-radius:14px;padding:13px 15px;background:rgba(255,255,255,.5);
    display:flex;flex-direction:column;gap:9px;transition:.16s}
  .ctile:hover{background:rgba(255,255,255,.72)}
  .ctile-top{display:flex;align-items:flex-start;justify-content:space-between;gap:10px}
  .ct{font-family:'Space Grotesk',sans-serif;font-weight:600;font-size:13.5px;color:var(--ink);line-height:1.3}
  .cref{font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--slate);
    border:1px solid var(--hair);border-radius:5px;padding:1px 6px;margin-right:8px;background:rgba(255,255,255,.6)}
  .ct-right{display:flex;flex-direction:column;align-items:flex-end;gap:4px;flex:none}
  .cd{color:var(--muted);font-size:12px;line-height:1.4;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
  .ctile-rate{display:flex;align-items:center;gap:10px;margin-top:auto}
  .expbadge{font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--slate);white-space:nowrap;flex:none}
  .expbadge b{color:var(--blue);font-weight:600}

  .seg{display:inline-flex;border:1px solid var(--hair);border-radius:11px;overflow:hidden;background:rgba(255,255,255,.5);
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
  .seg.full button.na{flex:0 0 46px}

  .deltapill{font-family:'JetBrains Mono',monospace;font-size:11px;padding:3px 9px;border-radius:20px;
    border:1px solid var(--hair);color:var(--slate);white-space:nowrap;min-width:66px;text-align:center;background:rgba(255,255,255,.5)}
  .deltapill.met{color:var(--teal);border-color:rgba(14,159,110,.35);background:rgba(14,159,110,.1)}
  .deltapill.under{color:var(--amber);border-color:rgba(224,138,11,.35);background:rgba(224,138,11,.1)}
  .deltapill.gap{color:var(--red);border-color:rgba(220,90,84,.4);background:rgba(220,90,84,.12)}
  .prevtag{font-family:'JetBrains Mono',monospace;font-size:10.5px;color:var(--slate);white-space:nowrap}
  .prevtag .up{color:var(--teal)} .prevtag .dn{color:var(--red)} .prevtag .eq{color:var(--slate)}

  .sumgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(165px,1fr));gap:14px;margin-top:4px}
  .stat{border:1px solid var(--hair);border-radius:16px;padding:18px 20px;background:rgba(255,255,255,.5);
    -webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);box-shadow:0 14px 34px -30px rgba(30,40,90,.5)}
  .stat .v{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:32px;line-height:1;
    background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
  .stat .v.plain{background:none;-webkit-text-fill-color:var(--ink);color:var(--ink)}
  .stat .k{color:var(--muted);font-size:12.5px;margin-top:7px;line-height:1.35}
  .stat .chg{font-family:'JetBrains Mono',monospace;font-size:11px;margin-top:6px}
  .chg.up{color:var(--teal)} .chg.dn{color:var(--red)} .chg.eq{color:var(--slate)}

  .bandbadge{display:inline-flex;align-items:center;gap:9px;font-family:'Space Grotesk',sans-serif;font-weight:600;
    font-size:15px;padding:10px 17px;border-radius:13px;border:1px solid var(--hair);margin-top:4px;background:rgba(255,255,255,.5)}
  .bandbadge.exceeds{color:var(--teal);border-color:rgba(14,159,110,.4);background:rgba(14,159,110,.1)}
  .bandbadge.meets{color:var(--blue);border-color:rgba(37,99,204,.35);background:rgba(37,99,204,.09)}
  .bandbadge.partial{color:var(--amber);border-color:rgba(224,138,11,.4);background:rgba(224,138,11,.1)}
  .bandbadge.below{color:var(--red);border-color:rgba(220,90,84,.4);background:rgba(220,90,84,.12)}
  .dotm{width:9px;height:9px;border-radius:50%;background:currentColor}

  .barwrap{margin-top:18px}
  .bar{display:flex;align-items:center;gap:12px;margin-bottom:9px}
  .bar .lbl{width:220px;font-size:12px;color:var(--muted);flex:none;line-height:1.25}
  .bar .track{flex:1;height:22px;border-radius:7px;background:rgba(100,116,139,.12);overflow:hidden;position:relative;
    border:1px solid var(--hair)}
  .bar .fill{height:100%;width:0;border-radius:7px;transition:width .5s cubic-bezier(.4,0,.2,1)}
  .bar .val{position:absolute;right:8px;top:50%;transform:translateY(-50%);font-family:'JetBrains Mono',monospace;
    font-size:10.5px;color:var(--ink);opacity:.85}
  .bar .exp-mark{position:absolute;top:-2px;bottom:-2px;width:2px;background:var(--navy);opacity:.55}

  .note{margin-top:18px;border-left:2px solid var(--violet);padding-left:15px;font-size:13.5px;color:var(--muted);line-height:1.6}
  .note b{color:var(--ink);font-weight:600}

  .importbanner{display:none;align-items:center;gap:12px;border:1px dashed var(--blue);border-radius:14px;
    padding:12px 16px;margin-top:16px;background:rgba(37,99,204,.06);font-size:13px;color:var(--ink)}
  .importbanner.show{display:flex}
  .importbanner .clr{margin-left:auto}

  /* learning */
  .toolbar{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-bottom:6px}
  .segmented{display:inline-flex;gap:2px;padding:5px;border-radius:14px;background:rgba(255,255,255,.5);
    border:1px solid var(--hair);-webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px);
    box-shadow:0 10px 30px -24px rgba(30,40,90,.5)}
  .segmented button{appearance:none;border:0;background:transparent;font-family:'Inter',sans-serif;font-size:12.5px;
    font-weight:600;color:var(--muted);padding:8px 15px;border-radius:10px;cursor:pointer;transition:.15s}
  .segmented button:hover{color:var(--navy)}
  .segmented button.on{color:var(--navy);background:rgba(255,255,255,.9);box-shadow:0 6px 16px -10px rgba(30,40,90,.5)}
  .learnfilter{margin-left:auto;font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--slate)}
  .learnfilter button{appearance:none;border:1px solid var(--hair);background:rgba(255,255,255,.5);cursor:pointer;
    font-family:inherit;font-size:11px;color:var(--slate);padding:6px 11px;border-radius:9px;transition:.15s}
  .learnfilter button.on{color:var(--navy);background:rgba(255,255,255,.85)}

  .learnarea{margin-top:16px}
  .learnarea .lah{font-family:'JetBrains Mono',monospace;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
    color:var(--slate);font-weight:600;margin-bottom:10px;display:flex;align-items:center;gap:10px}
  .learnarea .lah .gapdot{font-family:'JetBrains Mono',monospace;font-size:10px;padding:2px 8px;border-radius:20px;
    background:rgba(220,90,84,.12);color:var(--red);border:1px solid rgba(220,90,84,.3);text-transform:none;letter-spacing:0}
  .learngrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px}
  .lcard{border:1px solid var(--hair);border-radius:14px;padding:15px 16px;background:rgba(255,255,255,.55);
    -webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);display:flex;flex-direction:column;gap:9px;transition:.16s}
  .lcard:hover{background:rgba(255,255,255,.78)}
  .lcard .prov{display:inline-flex;align-items:center;gap:7px;font-family:'JetBrains Mono',monospace;font-size:10px;
    font-weight:600;letter-spacing:.04em;text-transform:uppercase;padding:3px 9px;border-radius:7px;align-self:flex-start}
  .lcard .prov.linkedin{color:var(--li);background:rgba(10,102,194,.1);border:1px solid rgba(10,102,194,.25)}
  .lcard .prov.degreed{color:var(--dg);background:rgba(224,138,11,.1);border:1px solid rgba(224,138,11,.28)}
  .lcard .prov.coursera{color:#0056D2;background:rgba(0,86,210,.09);border:1px solid rgba(0,86,210,.25)}
  .lcard .lt{font-family:'Space Grotesk',sans-serif;font-weight:600;font-size:14px;color:var(--ink);line-height:1.3}
  .lcard .lm{font-size:11.5px;color:var(--slate);font-family:'JetBrains Mono',monospace}
  .lcard .lact{display:flex;align-items:center;gap:10px;margin-top:auto;padding-top:4px}
  .lcard .lopen{font-size:12px;font-weight:600;color:var(--blue);text-decoration:none;display:inline-flex;align-items:center;gap:5px}
  .lcard .lopen:hover{text-decoration:underline}
  .lplan{margin-left:auto;display:inline-flex;align-items:center;gap:6px;font-size:11.5px;color:var(--slate);cursor:pointer;user-select:none}
  .lplan input{width:15px;height:15px;accent-color:var(--violet)}
  .samplebadge{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.08em;text-transform:uppercase;
    color:var(--amber);border:1px solid rgba(224,138,11,.35);background:rgba(224,138,11,.08);border-radius:7px;padding:3px 9px;font-weight:600}
  .planbox{margin-top:18px;border:1px solid var(--hair);border-radius:14px;padding:16px 18px;background:rgba(255,255,255,.4)}
  .planbox .pbh{font-family:'JetBrains Mono',monospace;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
    color:var(--slate);font-weight:600;margin-bottom:10px}
  .planitem{display:flex;align-items:center;gap:10px;font-size:12.5px;color:var(--ink);padding:6px 0;border-top:1px dashed rgba(100,116,139,.16)}
  .planitem:first-of-type{border-top:none}
  .planitem .x{margin-left:auto;cursor:pointer;color:var(--slate);font-size:14px}
  .emptyplan{font-size:12.5px;color:var(--slate)}

  .disc{margin-top:20px;padding:14px 18px;border-radius:14px;background:rgba(255,255,255,.4);border:1px solid var(--hair);
    font-size:11.5px;color:var(--muted);line-height:1.6}
  .disc b{color:var(--ink);font-weight:600}

  .footer{margin-top:38px;padding-top:20px;border-top:1px solid var(--hair);display:flex;gap:14px;flex-wrap:wrap;
    align-items:center;color:var(--slate);font-family:'JetBrains Mono',monospace;font-size:11.5px}
  .toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%) translateY(80px);z-index:99;
    background:#fff;border:1px solid var(--violet);border-radius:12px;padding:12px 20px;font-size:13.5px;color:var(--ink);
    transition:.3s;box-shadow:0 18px 50px -18px rgba(30,40,90,.5);opacity:0;font-weight:500}
  .toast.show{transform:translateX(-50%) translateY(0);opacity:1}

  .toprow{display:grid;grid-template-columns:1.15fr 1fr;gap:22px;align-items:start;margin-top:22px}
  .toprow > .card{margin-top:0}
  .revgrid{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:14px}
  .revlabel{font-family:'JetBrains Mono',monospace;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--slate);font-weight:600;margin-bottom:8px}
  .promptbox{width:100%;min-height:210px;border:1px solid var(--hair);border-radius:12px;padding:12px 13px;
    font-family:'JetBrains Mono',monospace;font-size:11.5px;line-height:1.5;color:var(--ink);background:rgba(255,255,255,.6);resize:vertical}
  .promptbox:focus{outline:none;border-color:var(--violet);background:#fff}
  @media(max-width:1080px){ .toprow{grid-template-columns:1fr} }
  @media(max-width:820px){ .revgrid{grid-template-columns:1fr} }
  @media(max-width:720px){
    .shell{padding:26px 20px 100px}
    .mgrid{grid-template-columns:1fr}
    .bar .lbl{width:120px}
  }
  @media print{
    body{background:#fff}
    .aurora,.actbtns,.scopewrap,.importbanner,.seg,.segmented,.learnfilter,.lplan{display:none!important}
    .card{break-inside:avoid;box-shadow:none;background:#fff;border-color:#ddd;-webkit-backdrop-filter:none;backdrop-filter:none}
    .areablock .arearows{display:block!important}
  }
</style>
</head>
<body>
<div class="aurora"><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div></div>
<div class="shell">

  <div class="topbar">
    <span class="wordmark">Syniti</span>
    <span class="eyebrow-now">Delivery Services</span>
    <span class="spacer"></span>
    <div class="actbtns">
      <button class="btn" id="importBtn"><span class="ic">&#8681;</span> Import previous</button>
      <button class="btn" id="printBtn"><span class="ic">&#128424;</span> Save / Print</button>
      <button class="btn primary" id="exportBtn"><span class="ic">&#8682;</span> Download form (.json)</button>
    </div>
    <input type="file" id="importFile" accept="application/json,.json" style="display:none">
  </div>

  <div class="eyebrow">Consultant Performance Assessment</div>
  <h1>Rate the work. See the <span class="grad">gap to level.</span> Close it.</h1>
  <p class="lead">A short, structured review that scores a consultant against the competency expectations for their C-level, classifies overall performance, captures project feedback, and suggests targeted Degreed and LinkedIn Learning to close each gap. Rate only what the engagement exercised, then download the form or import a prior review to track change.</p>

  <div class="toprow">
  <div class="card">
    <div class="panel-h"><span class="n">01</span> Assessment details</div>
    <div class="panel-sub">Who is being reviewed, on what engagement, and against which level.</div>
    <div class="fgrid">
      <div class="field"><label>Consultant name</label><input id="f_name" placeholder="First Last"></div>
      <div class="field"><label>Project / engagement</label><input id="f_project" placeholder="Project name"></div>
      <div class="field"><label>Reviewing lead</label><input id="f_lead" placeholder="Your name"></div>
      <div class="field"><label>C-Level (drives expectations)</label><select id="f_level"></select></div>
      <div class="field"><label>Assessment type</label>
        <select id="f_type"><option>Regular</option><option>Mid-project</option><option>End of assignment</option><option>Promotion review</option></select></div>
      <div class="field"><label>Assessment date</label><input id="f_date" type="date"></div>
    </div>
    <div style="margin-top:18px">
      <label style="font-family:'JetBrains Mono',monospace;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--slate);font-weight:600">Rating scale (0-5)</label>
      <div class="legend" id="legend"></div>
    </div>
    <div class="importbanner" id="cmpBanner">
      <span class="ic" style="color:var(--blue)">&#8644;</span>
      <span id="cmpText">Comparison loaded.</span>
      <button class="btn clr" id="clearCmp">Clear comparison</button>
    </div>
  </div>

  <div class="card">
    <div class="panel-h"><span class="n">02</span> Live summary</div>
    <div class="panel-sub">A running read-out of the assessment - it fills in as you rate the matrix below.</div>
    <div class="bandbadge meets" id="bandBadge"><span class="dotm"></span><span id="bandLabel">Awaiting ratings</span></div>
    <div class="sumgrid" id="sumGrid" style="margin-top:16px"></div>
    <div class="barwrap" id="barWrap"></div>
    <div class="note" id="sumNote"></div>
  </div>
  </div>

  <div class="card scopewrap">
    <div class="panel-h"><span class="n">03</span> Scope the assessment</div>
    <div class="panel-sub">Turn on only the competency areas relevant to this project. Core areas are on by default - squads are optional.</div>
    <div class="scoperow" id="scopeRow"></div>
  </div>

  <div class="card">
    <div class="panel-h"><span class="n">04</span> Guided review with AI <span class="samplebadge" style="color:var(--blue);border-color:rgba(37,99,204,.3);background:rgba(37,99,204,.08)">Optional</span></div>
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

  <div class="card" id="matrixCard">
    <div class="panel-h"><span class="n">05</span> Skills matrix</div>
    <div class="panel-sub">Score each competency 0-5. The expectation for the selected level is shown, and the delta flags where the consultant is at, above, or below level. Use N/A where not exercised on this project.</div>
    <div id="matrix"></div>
  </div>

  <div class="card">
    <div class="panel-h"><span class="n">06</span> Project feedback &amp; classification</div>
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

  <div class="card">
    <div class="panel-h"><span class="n">07</span> Recommended learning <span class="samplebadge">Starter set</span></div>
    <div class="panel-sub">Real LinkedIn Learning and Coursera courses mapped to each gap found above. A starter set for now - built to be deconstructed and curated (including Degreed) later.</div>
    <div class="toolbar">
      <div class="segmented" id="provSeg">
        <button data-p="both" class="on">Both sources</button>
        <button data-p="linkedin">LinkedIn Learning</button>
        <button data-p="coursera">Coursera</button>
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
    <div class="disc"><b>Links:</b> entries marked as a course open a verified LinkedIn Learning or Coursera page; entries marked <b>search</b> open that provider's live results for the topic. <b>Degreed:</b> Degreed is an enterprise LXP - its course URLs sit behind your organisation's SSO, so there are no public deep links. When you curate, either point each item's link at your Degreed tenant or let Degreed surface these same LinkedIn/Coursera items. The whole catalog is one structured object in this file (keyed by competency area, with room for competency-level overrides), so it lifts out cleanly for curation.</div>
  </div>


  <div class="footer">
    <span>Syniti Consulting Career Framework</span><span>·</span>
    <span>Competency scale 0-5</span><span>·</span>
    <span id="footMeta">Not saved yet</span>
    <span class="spacer" style="flex:1"></span>
    <button class="btn primary" onclick="doExport()"><span class="ic">&#8682;</span> Download form</button>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
const COMPS = __COMPS__;
const LEARNING = __LEARNING__;
const PROV_NAME = {linkedin:"LinkedIn Learning", coursera:"Coursera"};

const LEVELS = ["C1","C2","C3","C4-S","C4-M","C5-S","C5-M","C6-S","C6-M"];
const LEVEL_LABEL = {"C1":"C1 · Associate","C2":"C2 · Consultant","C3":"C3 · Senior Consultant",
  "C4-S":"C4 · Lead (Solution)","C4-M":"C4 · Lead (Managing)","C5-S":"C5 · Solution Architect",
  "C5-M":"C5 · Managing Consultant","C6-S":"C6 · Principal Sol. Architect","C6-M":"C6 · Principal Consultant"};
const SCALE = [{lv:0,nm:"None"},{lv:1,nm:"Awareness"},{lv:2,nm:"Working"},{lv:3,nm:"Competent"},{lv:4,nm:"Proficient"},{lv:5,nm:"Expert"}];

let state = {level:"C3", ratings:{}, na:{}, scope:{}, cmp:null, prov:"both", onlyGaps:true, plan:{}, reviewMode:"interview"};
const CORE_ON = ["DQ-Specific Technical","DQ-Specific Functional","SAP Data Functional","Delivery & Consulting"];
const AREAS = [...new Set(COMPS.map(c=>c.area))];
AREAS.forEach(a=> state.scope[a] = CORE_ON.includes(a));

const $ = s=>document.querySelector(s);
const el = (t,c,h)=>{const e=document.createElement(t); if(c)e.className=c; if(h!=null)e.innerHTML=h; return e;};

(function(){
  const sel=$("#f_level");
  LEVELS.forEach(l=>{const o=el("option"); o.value=l; o.textContent=LEVEL_LABEL[l]; sel.appendChild(o);});
  sel.value=state.level;
  const lg=$("#legend");
  SCALE.forEach(s=>lg.appendChild(el("div","legchip",`<div class="lv">${s.lv}</div><div class="nm">${s.nm}</div>`)));
  $("#f_date").value = new Date().toISOString().slice(0,10);
})();

function renderScope(){
  const row=$("#scopeRow"); row.innerHTML="";
  AREAS.forEach(a=>{
    const n=COMPS.filter(c=>c.area===a).length;
    const t=el("button","scopetile"+(state.scope[a]?" on":""));
    t.innerHTML=`<span class="box">${state.scope[a]?"&#10003;":""}</span><span class="st"><b>${a}</b><span>${n} competencies</span></span>`;
    t.onclick=()=>{state.scope[a]=!state.scope[a]; renderScope(); renderMatrix(); recompute();};
    row.appendChild(t);
  });
}
function expFor(c){ return c.e[state.level]; }
function deltaClass(r,e){ if(r>=e) return "met"; if(r<=e-2) return "gap"; return "under"; }

function renderMatrix(){
  const m=$("#matrix"); m.innerHTML="";
  const activeAreas=AREAS.filter(a=>state.scope[a]);
  if(!activeAreas.length){ m.appendChild(el("div","panel-sub","No areas selected. Turn on at least one area in step 03.")); return; }
  activeAreas.forEach((a,idx)=>{
    const items=COMPS.filter(c=>c.area===a);
    const block=el("div","areablock"+(idx===0?" open":""));
    const head=el("div","areahead");
    head.innerHTML=`<span class="chev">&#9654;</span><span class="at">${a}</span><span class="areastat" data-area="${a}">-</span>`;
    head.onclick=(e)=>{ if(e.target.tagName==="BUTTON")return; block.classList.toggle("open"); };
    block.appendChild(head);
    const rows=el("div","arearows");
    const grid=el("div","mgrid");
    items.forEach(c=>{
      const e=expFor(c);
      const tile=el("div","ctile");
      const top=el("div","ctile-top",`<div class="ct"><span class="cref">${c.ref}</span>${c.t}</div>`);
      const right=el("div","ct-right");
      const dp=el("div","deltapill","-"); dp.dataset.ref=c.ref;
      const pv=el("div","prevtag"); pv.dataset.prev=c.ref;
      right.appendChild(dp); right.appendChild(pv); top.appendChild(right);
      tile.appendChild(top);
      if(c.d){ const d=el("div","cd",c.d); d.title=c.d; tile.appendChild(d); }
      const rate=el("div","ctile-rate");
      rate.appendChild(el("div","expbadge",`Exp ${state.level}: <b>${e}</b>`));
      const seg=el("div","seg full");
      for(let v=0;v<=5;v++){
        const b=el("button",null,v); b.dataset.v=v; b.dataset.ref=c.ref;
        if(state.ratings[c.ref]===v && !state.na[c.ref]) b.classList.add("sel");
        b.onclick=()=>{ state.ratings[c.ref]=v; state.na[c.ref]=false; paintRow(c); recompute(); };
        seg.appendChild(b);
      }
      const naB=el("button","na"+(state.na[c.ref]?" sel":""),"N/A"); naB.dataset.ref=c.ref;
      naB.onclick=()=>{ state.na[c.ref]=!state.na[c.ref]; if(state.na[c.ref]) delete state.ratings[c.ref]; paintRow(c); recompute(); };
      seg.appendChild(naB);
      rate.appendChild(seg);
      tile.appendChild(rate);
      grid.appendChild(tile);
    });
    rows.appendChild(grid); block.appendChild(rows); m.appendChild(block);
  });
  activeAreas.forEach(a=>COMPS.filter(c=>c.area===a).forEach(paintRow));
}

function paintRow(c){
  const e=expFor(c);
  document.querySelectorAll(`.seg button[data-ref="${c.ref}"]`).forEach(b=>{
    if(b.classList.contains("na")) b.classList.toggle("sel", !!state.na[c.ref]);
    else b.classList.toggle("sel", state.ratings[c.ref]===Number(b.dataset.v) && !state.na[c.ref]);
  });
  const dp=document.querySelector(`.deltapill[data-ref="${c.ref}"]`);
  if(dp){
    if(state.na[c.ref] || state.ratings[c.ref]==null){ dp.className="deltapill"; dp.textContent="-"; }
    else{ const r=state.ratings[c.ref]; const d=r-e; dp.className="deltapill "+deltaClass(r,e); dp.textContent=(d>0?"+":"")+d+" vs level"; }
  }
  const pv=document.querySelector(`.prevtag[data-prev="${c.ref}"]`);
  if(pv){
    if(state.cmp&&state.cmp.ratings&&state.cmp.ratings[c.ref]!=null&&!state.na[c.ref]&&state.ratings[c.ref]!=null){
      const p=state.cmp.ratings[c.ref], cur=state.ratings[c.ref], ch=cur-p;
      const cls=ch>0?"up":(ch<0?"dn":"eq"); const arw=ch>0?"&#9650;":(ch<0?"&#9660;":"=");
      pv.innerHTML=`was ${p} <span class="${cls}">${arw}${ch!==0?(ch>0?"+"+ch:ch):""}</span>`;
    } else pv.innerHTML="";
  }
}

function stats(){
  const active=COMPS.filter(c=>state.scope[c.area]&&!state.na[c.ref]&&state.ratings[c.ref]!=null);
  let deltas=[],met=0,gaps=[];
  active.forEach(c=>{const e=expFor(c);const d=state.ratings[c.ref]-e;deltas.push(d);if(d>=0)met++;if(d<=-2)gaps.push(c);});
  const n=active.length;
  return {n, avgD:n?deltas.reduce((a,b)=>a+b,0)/n:0, avgScore:n?active.reduce((a,c)=>a+state.ratings[c.ref],0)/n:0,
    pctMet:n?Math.round(met/n*100):0, gaps, met};
}
function band(s){
  if(s.n===0) return {k:"meets",l:"Awaiting ratings"};
  if(s.avgD>=0.5) return {k:"exceeds",l:"Exceeds expectations"};
  if(s.avgD>=-0.25&&s.gaps.length===0) return {k:"meets",l:"Meets expectations"};
  if(s.avgD>=-1) return {k:"partial",l:"Partially meets - development needed"};
  return {k:"below",l:"Below expectations"};
}
let bandTouched=false;
$("#f_band").addEventListener("change",()=>bandTouched=true);

// areas that are below level (any rated competency under expectation)
function belowAreas(){
  const res={};
  AREAS.filter(a=>state.scope[a]).forEach(a=>{
    const items=COMPS.filter(c=>c.area===a&&!state.na[c.ref]&&state.ratings[c.ref]!=null);
    const below=items.filter(c=>state.ratings[c.ref]<expFor(c));
    const gaps=items.filter(c=>state.ratings[c.ref]<=expFor(c)-2);
    if(below.length) res[a]={below:below.length, gaps:gaps.length};
  });
  return res;
}

function renderLearning(){
  const wrap=$("#learning"); wrap.innerHTML="";
  const below=belowAreas();
  let areas = state.onlyGaps ? Object.keys(below) : AREAS.filter(a=>state.scope[a]);
  // sort: gap areas first
  areas.sort((a,b)=> (below[b]?below[b].gaps:0)-(below[a]?below[a].gaps:0));
  if(!areas.length){
    wrap.appendChild(el("div","panel-sub", state.onlyGaps
      ? "No below-level competencies in scope yet. Rate the matrix, or switch to \"All scoped areas\" to browse the full sample catalog."
      : "No areas in scope. Turn areas on in step 03."));
    return;
  }
  areas.forEach(a=>{
    let items=(LEARNING[a]||[]).filter(x=> state.prov==="both" || x.p===state.prov);
    if(!items.length) return;
    const sec=el("div","learnarea");
    const b=below[a];
    sec.appendChild(el("div","lah",`${a}${b?`<span class="gapdot">${b.below} below level${b.gaps?` · ${b.gaps} gap`:""}</span>`:""}`));
    const grid=el("div","learngrid");
    items.forEach(x=>{
      const key=a+"::"+x.t;
      const card=el("div","lcard");
      const url=x.u;
      card.innerHTML=`<span class="prov ${x.p}">${PROV_NAME[x.p]}${x.d?"":" · search"}</span>
        <div class="lt">${x.t}</div><div class="lm">${x.m||""}</div>
        <div class="lact"><a class="lopen" href="${url}" target="_blank" rel="noopener">Open &#8599;</a>
        <label class="lplan"><input type="checkbox" ${state.plan[key]?"checked":""}> Add to plan</label></div>`;
      card.querySelector("input").onchange=(ev)=>{
        if(ev.target.checked) state.plan[key]={area:a,provider:x.p,title:x.t,meta:x.m||"",url};
        else delete state.plan[key];
        renderPlan();
      };
      grid.appendChild(card);
    });
    sec.appendChild(grid); wrap.appendChild(sec);
  });
}
function renderPlan(){
  const box=$("#planList"); const keys=Object.keys(state.plan);
  if(!keys.length){ box.innerHTML='<div class="emptyplan">Tick "Add to plan" on any suggestion to build a development plan for this consultant.</div>'; return; }
  box.innerHTML="";
  keys.forEach(k=>{
    const it=state.plan[k];
    const row=el("div","planitem",`<span class="prov ${it.provider}" style="font-size:9px;padding:2px 7px">${PROV_NAME[it.provider]}</span> <b style="font-weight:600">${it.title}</b> <span style="color:var(--slate);font-family:'JetBrains Mono',monospace;font-size:11px">${it.area}</span><span class="x" title="Remove">&#10005;</span>`);
    row.querySelector(".x").onclick=()=>{ delete state.plan[k]; renderPlan(); renderLearning(); };
    box.appendChild(row);
  });
}

// prov + gap toggles
$("#provSeg").querySelectorAll("button").forEach(btn=>{
  btn.onclick=()=>{ state.prov=btn.dataset.p; $("#provSeg").querySelectorAll("button").forEach(x=>x.classList.toggle("on",x===btn)); renderLearning(); };
});
$("#onlyGaps").onclick=()=>{ state.onlyGaps=true; $("#onlyGaps").classList.add("on"); $("#allAreas").classList.remove("on"); renderLearning(); };
$("#allAreas").onclick=()=>{ state.onlyGaps=false; $("#allAreas").classList.add("on"); $("#onlyGaps").classList.remove("on"); renderLearning(); };

function recompute(){
  const s=stats();
  AREAS.filter(a=>state.scope[a]).forEach(a=>{
    const items=COMPS.filter(c=>c.area===a&&!state.na[c.ref]&&state.ratings[c.ref]!=null);
    const pill=document.querySelector(`.areastat[data-area="${a}"]`); if(!pill)return;
    if(!items.length){ pill.className="areastat"; pill.textContent="not rated"; return; }
    const d=items.reduce((x,c)=>x+(state.ratings[c.ref]-expFor(c)),0)/items.length;
    pill.className="areastat "+(d>=0?"pos":(d<=-1?"neg":""));
    pill.textContent=`${items.length}/${COMPS.filter(c=>c.area===a).length} · ${(d>=0?"+":"")}${d.toFixed(1)} vs level`;
  });
  const b=band(s);
  if(!bandTouched) $("#f_band").value=b.k;
  const curBand=$("#f_band").value;
  const labels={exceeds:"Exceeds expectations",meets:"Meets expectations",partial:"Partially meets - development needed",below:"Below expectations"};
  $("#bandBadge").className="bandbadge "+curBand; $("#bandLabel").textContent=labels[curBand];
  const g=$("#sumGrid"); g.innerHTML="";
  const cmpS=state.cmp?state.cmp.summary:null;
  function card(v,k,chg,plain){
    let ch="";
    if(chg!=null){const cls=chg>0?"up":(chg<0?"dn":"eq"); ch=`<div class="chg ${cls}">${chg>0?"&#9650; +":(chg<0?"&#9660; ":"")}${chg!==0?chg.toFixed(2):"no change"} vs prev</div>`;}
    return el("div","stat",`<div class="v ${plain?"plain":""}">${v}</div><div class="k">${k}</div>${ch}`);
  }
  g.appendChild(card(s.avgScore.toFixed(2),"Average competency score",cmpS?+(s.avgScore-cmpS.avgScore).toFixed(2):null));
  g.appendChild(card((s.avgD>=0?"+":"")+s.avgD.toFixed(2),"Average delta to level",cmpS?+(s.avgD-cmpS.avgD).toFixed(2):null,true));
  g.appendChild(card(s.pctMet+"%","At or above expectation",cmpS?s.pctMet-cmpS.pctMet:null));
  g.appendChild(card(s.gaps.length,"Material gaps (2+ below)",null,true));
  g.appendChild(card(s.n,"Competencies rated",null,true));
  const bw=$("#barWrap"); bw.innerHTML="";
  AREAS.filter(a=>state.scope[a]).forEach(a=>{
    const items=COMPS.filter(c=>c.area===a&&!state.na[c.ref]&&state.ratings[c.ref]!=null);
    if(!items.length)return;
    const avg=items.reduce((x,c)=>x+state.ratings[c.ref],0)/items.length;
    const expAvg=items.reduce((x,c)=>x+expFor(c),0)/items.length; const d=avg-expAvg;
    const fillCol=d>=0?"linear-gradient(90deg,#0E9F6E,#3FCB98)":(d<=-1?"linear-gradient(90deg,#DC5A54,#EE8A85)":"linear-gradient(120deg,#2563CC,#8B5CF6)");
    const bar=el("div","bar");
    bar.innerHTML=`<div class="lbl">${a}</div><div class="track"><div class="fill" style="background:${fillCol}"></div><div class="exp-mark" style="left:${expAvg/5*100}%"></div><div class="val">${avg.toFixed(1)} / exp ${expAvg.toFixed(1)}</div></div>`;
    bw.appendChild(bar);
    requestAnimationFrame(()=>bar.querySelector(".fill").style.width=(avg/5*100)+"%");
  });
  let note="";
  if(s.n===0) note="Start rating competencies to build the summary.";
  else{
    const gapNames=s.gaps.slice(0,4).map(c=>c.t).join(", ");
    note=`<b>${s.met} of ${s.n}</b> rated competencies are at or above the ${state.level} expectation (${s.pctMet}%). `;
    note+= s.gaps.length ? `Focus development on <b>${s.gaps.length}</b> material gap${s.gaps.length>1?"s":""}: ${gapNames}${s.gaps.length>4?"...":""}.` : `No material gaps against level - a solid profile for the scoped areas.`;
    if(cmpS){const dd=s.avgScore-cmpS.avgScore; note+= dd>0?` Since the previous review the average score is up ${dd.toFixed(2)}.`:(dd<0?` Since the previous review the average score is down ${Math.abs(dd).toFixed(2)}.`:` No change in average score since the previous review.`);}
  }
  $("#sumNote").innerHTML=note;
  $("#footMeta").textContent=($("#f_name").value||"Unnamed")+" · "+state.level+" · "+s.n+" rated";
  renderLearning();
  refreshPrompt();
}

$("#f_level").addEventListener("change",e=>{ state.level=e.target.value; COMPS.forEach(paintRow); recompute(); });
$("#f_name").addEventListener("input",recompute);

function collect(){
  const s=stats(); const b=$("#f_band").value;
  return {schema:"syniti-perf-assessment",version:2,
    meta:{consultant:$("#f_name").value,project:$("#f_project").value,lead:$("#f_lead").value,level:state.level,type:$("#f_type").value,date:$("#f_date").value,learningSource:state.prov},
    scope:state.scope, ratings:state.ratings, na:state.na,
    feedback:{classification:b,recommendation:$("#f_reco").value,projectRating:$("#f_proj").value,strengths:$("#f_str").value,development:$("#f_dev").value,projectFeedback:$("#f_pf").value},
    learningPlan:Object.values(state.plan),
    summary:{avgScore:+s.avgScore.toFixed(3),avgD:+s.avgD.toFixed(3),pctMet:s.pctMet,gaps:s.gaps.length,n:s.n}};
}
function doExport(){
  const data=collect(); const blob=new Blob([JSON.stringify(data,null,2)],{type:"application/json"});
  const url=URL.createObjectURL(blob); const a=document.createElement("a");
  const safe=(data.meta.consultant||"consultant").replace(/[^a-z0-9]+/gi,"_");
  a.href=url; a.download=`Assessment_${safe}_${data.meta.date||"draft"}.json`; a.click(); URL.revokeObjectURL(url); toast("Form downloaded");
}
$("#exportBtn").onclick=doExport;
$("#printBtn").onclick=()=>window.print();
$("#importBtn").onclick=()=>$("#importFile").click();
$("#importFile").onchange=e=>{
  const f=e.target.files[0]; if(!f)return; const rd=new FileReader();
  rd.onload=()=>{ try{ const d=JSON.parse(rd.result); if(d.schema!=="syniti-perf-assessment")throw 0;
      state.cmp=d; $("#cmpBanner").classList.add("show");
      $("#cmpText").innerHTML=`Comparing against <b>${d.meta.consultant||"previous"}</b> · ${d.meta.level||"?"} · ${d.meta.date||"no date"}. Each row shows the change; the summary shows deltas.`;
      COMPS.forEach(paintRow); recompute(); toast("Previous assessment loaded for comparison");
    }catch(err){ toast("Could not read that file - expected an exported assessment (.json)"); } e.target.value=""; };
  rd.readAsText(f);
};
$("#clearCmp").onclick=()=>{ state.cmp=null; $("#cmpBanner").classList.remove("show"); COMPS.forEach(paintRow); recompute(); };
function toast(m){const t=$("#toast");t.textContent=m;t.classList.add("show");clearTimeout(t._t);t._t=setTimeout(()=>t.classList.remove("show"),2600);}


// ===== Guided AI review: prompt build + paste-back =====
function scopedComps(){ return COMPS.filter(c=>state.scope[c.area]); }
function buildPrompt(){
  const sc=scopedComps(); const L=[];
  L.push("You are helping a Syniti delivery lead assess a consultant for a project performance review.");
  L.push("");
  L.push("CONSULTANT LEVEL: "+state.level+" ("+LEVEL_LABEL[state.level]+"). Judge performance against the expectation for THIS level, not against perfection.");
  L.push("");
  L.push("RATING SCALE (integers 0-5):");
  SCALE.forEach(x=>L.push("  "+x.lv+" = "+x.nm));
  L.push("");
  L.push("COMPETENCIES TO ASSESS  (ref | competency | expected level | meaning):");
  sc.forEach(c=>L.push("  "+c.ref+" | "+c.t+" | expected "+expFor(c)+" | "+(c.d||"")));
  L.push("");
  if(state.reviewMode==="notes"){
    L.push("MY NOTES ON THE CONSULTANT:");
    L.push('"""');
    L.push(($("#f_notes")&&$("#f_notes").value)?$("#f_notes").value:"(type or paste your observations in the notes box before copying)");
    L.push('"""');
    L.push("");
    L.push("TASK: Using only my notes, rate each competency above. Where my notes give no evidence for a competency, put its ref in \"na\" rather than guessing.");
  } else {
    L.push("TASK: Interview me to gather evidence. Ask a short, focused set of questions (about 6-10, grouped by theme) covering the competencies above - keep it a quick back-and-forth. When you have enough to judge, produce the assessment.");
  }
  L.push("");
  L.push("OUTPUT: when ready, reply with ONLY this JSON inside a single code block, no other text:");
  L.push('```json');
  L.push("{");
  L.push('  "ratings": { "'+(sc[0]?sc[0].ref:"A1")+'": 3 },   // ONE integer 0-5 for EACH ref listed above');
  L.push('  "na": [],                                  // refs with no evidence');
  L.push('  "classification": "meets",                 // exceeds | meets | partial | below');
  L.push('  "recommendation": "On track at level",');
  L.push('  "strengths": "",');
  L.push('  "development": "",                          // focus on the gaps to expected level');
  L.push('  "projectFeedback": ""');
  L.push("}");
  L.push('```');
  L.push("Rules: use ONLY the refs listed; ratings are integers 0-5; be evidence-based and do not inflate; when writing development, compare each rating to its expected level.");
  return L.join("\n");
}
function refreshPrompt(){ const t=$("#promptBox"); if(t) t.value=buildPrompt(); }
function copyPrompt(){
  const ta=$("#promptBox"); if(!ta) return; ta.focus(); ta.select();
  let ok=false; try{ ok=document.execCommand("copy"); }catch(e){}
  if(navigator.clipboard){ navigator.clipboard.writeText(ta.value).then(()=>{}).catch(()=>{}); ok=true; }
  toast(ok?"Prompt copied - paste it into your assistant":"Select the prompt and copy manually");
}
function applyAI(){
  const raw=($("#pasteBox")&&$("#pasteBox").value||"").trim();
  if(!raw){ toast("Paste the assistant's response first"); return; }
  let obj=null;
  const m=raw.match(/```(?:json)?\s*([\s\S]*?)```/i);
  let cand=m?m[1]:raw;
  try{ obj=JSON.parse(cand); }catch(e){
    const i=cand.indexOf("{"), j=cand.lastIndexOf("}");
    if(i>=0&&j>i){ try{ obj=JSON.parse(cand.slice(i,j+1)); }catch(e2){} }
  }
  if(!obj || typeof obj!=="object"){ toast("Could not find valid JSON in that response"); return; }
  applyObj(obj);
}
function applyObj(o){
  const valid=new Set(COMPS.map(c=>c.ref));
  const areaOf={}; COMPS.forEach(c=>areaOf[c.ref]=c.area);
  let n=0;
  if(o.ratings && typeof o.ratings==="object"){
    Object.keys(o.ratings).forEach(ref=>{
      if(!valid.has(ref)) return;
      let v=Math.round(Number(o.ratings[ref])); if(isNaN(v)) return;
      v=Math.max(0,Math.min(5,v));
      state.ratings[ref]=v; state.na[ref]=false; state.scope[areaOf[ref]]=true; n++;
    });
  }
  if(Array.isArray(o.na)){
    o.na.forEach(ref=>{ if(valid.has(ref)){ state.na[ref]=true; delete state.ratings[ref]; state.scope[areaOf[ref]]=true; } });
  }
  if(o.strengths) $("#f_str").value=o.strengths;
  if(o.development) $("#f_dev").value=o.development;
  if(o.projectFeedback) $("#f_pf").value=o.projectFeedback;
  if(o.classification && ["exceeds","meets","partial","below"].includes(String(o.classification))){ $("#f_band").value=o.classification; bandTouched=true; }
  if(o.recommendation){ const sel=$("#f_reco"); Array.from(sel.options).forEach(op=>{ if(op.value.toLowerCase()===String(o.recommendation).toLowerCase()) sel.value=op.value; }); }
  renderScope(); renderMatrix(); recompute();
  toast("Applied "+n+" ratings from the assistant");
  const mc=document.getElementById("matrixCard"); if(mc) mc.scrollIntoView({behavior:"smooth",block:"start"});
}
if($("#modeSeg")) $("#modeSeg").querySelectorAll("button").forEach(btn=>{
  btn.onclick=()=>{ state.reviewMode=btn.dataset.m; $("#modeSeg").querySelectorAll("button").forEach(x=>x.classList.toggle("on",x===btn));
    $("#notesWrap").style.display = state.reviewMode==="notes" ? "block":"none"; refreshPrompt(); };
});
if($("#f_notes")) $("#f_notes").addEventListener("input",refreshPrompt);
if($("#copyPrompt")) $("#copyPrompt").onclick=copyPrompt;
if($("#applyAI")) $("#applyAI").onclick=applyAI;

renderScope(); renderMatrix(); renderPlan(); recompute();
</script>
</body>
</html>'''

HTML = HTML.replace("__COMPS__", comps).replace("__LEARNING__", learning_json)
open('/mnt/user-data/outputs/Syniti_Performance_Assessment.html','w').write(HTML)
print("written", len(HTML), "bytes")
