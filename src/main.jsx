import React, {useState, useEffect, useRef} from 'react';
import {createRoot} from 'react-dom/client';
import './styles.css';

const bidders=[
 {name:'ABC Technologies Pvt. Ltd.',score:94,risk:'Low',issue:'Fully verified',state:'Verified'},
 {name:'Bharat Digital Systems',score:86,risk:'Medium',issue:'OEM authorization review',state:'Needs Review'},
 {name:'Nova Infotech Pvt. Ltd.',score:72,risk:'Medium',issue:'Turnover discrepancy',state:'Needs Review'},
 {name:'Vertex Solutions',score:61,risk:'High',issue:'Missing statutory documents',state:'Review'},
 {name:'SecureTech India',score:48,risk:'High',issue:'Multiple compliance issues',state:'Review'}
];
const nav=['Dashboard','Tenders','Bid Verification','Compliance Analysis','Risk Center','Reports','Audit Trail','Integrations','Settings'];
const icons=['▦','◇','✓','▤','◉','▱','◷','⌁','⚙'];
const requirements=[
 ['GST Registration','verified','GSTIN 09ABCDE1234F1Z5','Active registration · Last verified 2 min ago'],
 ['Udyam Registration','verified','UDYAM-UP-09-0023412','Micro enterprise · ABC Technologies Pvt. Ltd.'],
 ['PAN / Income Tax','verified','PAN ABCDE1234F','Name and PAN matched across submitted documents'],
 ['Turnover Requirement','review','Minimum turnover: ₹5 Crore','Extracted: ₹4.72 Crore · Officer review required'],
 ['OEM Authorization','failed','Authorization validity not detected','Required authorization needs manual verification']
];
function Badge({children,type}){return <span className={'badge '+(type||'')}>{children}</span>}

/* ---------------------------------------------------------------------- */
/* ROUTER                                                                  */
/* Lightweight History-API router — no external dependency required.      */
/* Handles: initial URL, browser back/forward, and programmatic navigate. */
/* ---------------------------------------------------------------------- */
function useRoute(){
 const [path,setPathState]=useState(window.location.pathname);
 useEffect(()=>{
  const onPop=()=>setPathState(window.location.pathname);
  window.addEventListener('popstate',onPop);
  return ()=>window.removeEventListener('popstate',onPop);
 },[]);
 const navigate=(to)=>{
  if(window.location.pathname!==to)window.history.pushState({},'',to);
  setPathState(to);
 };
 return [path,navigate];
}

/* ---------------------------------------------------------------------- */
/* SCROLL REVEAL                                                          */
/* Reusable, lightweight (no library) — observes every ".reveal-on-scroll"*/
/* element currently in the DOM and fades/slides it in the first time it  */
/* enters the viewport. Call inside any component's effect after its      */
/* content (re)renders, e.g. useScrollReveal() on mount, or               */
/* useScrollReveal([page]) to re-scan after a page/section swap.          */
/* ---------------------------------------------------------------------- */
function useScrollReveal(deps=[]){
 useEffect(()=>{
  const els=document.querySelectorAll('.reveal-on-scroll:not(.revealed)');
  if(!els.length)return;
  const reduceMotion=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(reduceMotion||typeof IntersectionObserver==='undefined'){
   els.forEach(el=>el.classList.add('revealed'));
   return;
  }
  const observer=new IntersectionObserver((entries)=>{
   entries.forEach(entry=>{
    if(entry.isIntersecting){
     entry.target.classList.add('revealed');
     observer.unobserve(entry.target);
    }
   });
  },{threshold:0.15,rootMargin:'0px 0px -40px 0px'});
  els.forEach(el=>observer.observe(el));
  return ()=>observer.disconnect();
  // eslint-disable-next-line react-hooks/exhaustive-deps
 },deps);
}


function AppRouter(){
 const [authenticated,setAuthenticated]=useState(false);
 const [path,navigate]=useRoute();

 const login=()=>{setAuthenticated(true);navigate('/dashboard')};
 const logout=()=>{setAuthenticated(false);navigate('/')};

 // Resolve which screen this path + auth state should show.
 let view;
 if(path==='/login')view=authenticated?'app':'login';
 else if(path==='/')view='landing';
 else view=authenticated?'app':'landing';

 // Keep the address bar consistent with what's actually rendered —
 // e.g. an authenticated user hitting /login lands on the dashboard URL,
 // and an unauthenticated user on an unknown/protected path is sent home.
 useEffect(()=>{
  if(view==='app'&&path==='/login')navigate('/dashboard');
  if(view==='landing'&&path!=='/'&&path!=='/login')navigate('/');
 },[view,path]);

 if(view==='login')return <Login onSignIn={login}/>;
 if(view==='app')return <App onLogout={logout}/>;
 return <Landing onLogin={()=>navigate('/login')}/>;
}

/* ---------------------------------------------------------------------- */
/* PAGE 1 — LANDING PAGE                                                   */
/* ---------------------------------------------------------------------- */
function Landing({onLogin}){
 const [navOpen,setNavOpen]=useState(false);
 useScrollReveal();
 const features=[
  ['✓','AI-Powered Verification','Documents are read and cross-checked against tender requirements automatically.'],
  ['◉','Multi-Portal Validation','Bidder claims are checked against GSTN, Udyam, MCA and other government sources.'],
  ['▤','Risk & Compliance Scoring','Every bidder gets a transparent score, backed by the evidence behind it.'],
  ['◷','Audit-Ready Evidence','Every verification and officer decision is logged for complete traceability.']
 ];
 const categories=['GST','PAN','Udyam / MSME','Make in India','EPFO / ESIC','Startup India','NSIC','OEM Authorization','MCA','BIS / DPIIT'];
 const security=[
  ['◇','Role-based access','Officers see only the tenders and bids their role permits.'],
  ['◉','Secure evidence storage','Submitted documents and extracted evidence are stored securely.'],
  ['◷','Complete audit traceability','Every AI assessment and officer action is recorded, end to end.'],
  ['✓','Officer-controlled final decisions','AI assists with evidence — the Procurement Officer decides.']
 ];
 return <div className="landing">
  <header className="landing-nav">
   <div className="landing-brand"><div className="logo">G</div><div><b>GeM Compliance AI</b><small>AI-POWERED PROCUREMENT VERIFICATION</small></div></div>
   <nav className={navOpen?'open':''}>
    <a href="#product">Product</a>
    <a href="#features">Features</a>
    <a href="#security">Security</a>
    <a href="#about">About</a>
    <button className="primary nav-login" onClick={onLogin}>Officer Login</button>
   </nav>
   <button className="nav-toggle" aria-label="Toggle navigation" onClick={()=>setNavOpen(!navOpen)}>{navOpen?'×':'☰'}</button>
  </header>

  <section className="landing-hero" id="product">
   <div className="landing-hero-copy">
    <p className="eyebrow">SECURE PROCUREMENT WORKSPACE</p>
    <h1>Intelligent Procurement Compliance</h1>
    <p className="landing-hero-sub">AI-powered verification and decision support for GeM procurement officers.</p>
    <p className="landing-hero-desc">GeM Compliance AI reads bidder documents, checks them against official government sources, and gives every procurement officer a clear, evidence-backed view of compliance — so qualification decisions are faster, and fully auditable.</p>
    <div className="landing-cta-row">
     <button className="primary hero-cta" onClick={onLogin}>Login to Officer Workspace →</button>
     <a className="secondary hero-cta" href="#features">Explore Platform</a>
    </div>
   </div>
   <div className="landing-hero-visual" aria-hidden="true">
    <div className="hero-panel">
     <div className="hero-panel-head"><span/><span/><span/><b>Bid Verification</b></div>
     <div className="hero-panel-score">
      <div className="hero-ring"><svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="42"/><circle className="hero-ring-fill" cx="50" cy="50" r="42"/></svg><div><b>94</b><span>/100</span></div></div>
      <div className="hero-panel-rows">
       <p><i className="hero-dot verified"/> GST Registration <b>Verified</b></p>
       <p><i className="hero-dot verified"/> Udyam Registration <b>Verified</b></p>
       <p><i className="hero-dot review"/> Turnover Requirement <b>Review</b></p>
      </div>
     </div>
    </div>
   </div>
  </section>

  <section className="landing-section" id="features">
   <div className="landing-section-head reveal-on-scroll"><p className="eyebrow">WHY GeM COMPLIANCE AI</p><h2>Built for procurement officers, not generic document review</h2></div>
   <div className="landing-feature-grid">
    {features.map((f,i)=><div className="landing-feature-card reveal-on-scroll" style={{transitionDelay:(i%4)*100+'ms'}} key={f[1]}><div className="landing-feature-icon">{f[0]}</div><h3>{f[1]}</h3><p>{f[2]}</p></div>)}
   </div>
  </section>

  <section className="landing-section landing-categories">
   <div className="landing-section-head reveal-on-scroll"><p className="eyebrow">COMPLIANCE COVERAGE</p><h2>Verification across the categories that matter</h2></div>
   <div className="landing-category-chips reveal-on-scroll">
    {categories.map(c=><span key={c}>{c}</span>)}
   </div>
  </section>

  <section className="landing-section landing-security" id="security">
   <div className="landing-security-copy reveal-on-scroll"><p className="eyebrow">SECURITY & GOVERNANCE</p><h2>Evidence you can trust, decisions you can defend</h2><p>Every part of the workflow is designed around one principle: the AI assists, and the Procurement Officer decides — with a full record behind every decision.</p></div>
   <div className="landing-security-grid">
    {security.map((s,i)=><div className="landing-security-item reveal-on-scroll" style={{transitionDelay:(i%4)*100+'ms'}} key={s[1]}><div className="landing-security-icon">{s[0]}</div><div><b>{s[1]}</b><p>{s[2]}</p></div></div>)}
   </div>
  </section>

  <section className="landing-final-cta reveal-on-scroll" id="about">
   <h2>Ready to verify procurement compliance?</h2>
   <p>Sign in to your officer workspace and continue where your verifications left off.</p>
   <button className="primary" onClick={onLogin}>Enter Officer Workspace →</button>
  </section>

  <footer className="landing-footer reveal-on-scroll">
   <div>
    <div className="landing-brand"><div className="logo">G</div><div><b>GeM Compliance AI</b><small>AI-powered procurement verification</small></div></div>
    <p>Authorized Procurement Personnel Only</p>
   </div>
   <div className="landing-footer-links"><a href="#">Privacy</a><a href="#">Security</a><a href="#">Contact</a></div>
  </footer>
 </div>
}

/* ---------------------------------------------------------------------- */
/* PAGE 2 — LOGIN PAGE (unchanged design, now its own route)              */
/* ---------------------------------------------------------------------- */
function Login({onSignIn}){
 const [showPassword,setShowPassword]=useState(false);
 return <div className="login-page login-page-solo"><form className="login-card" onSubmit={e=>{e.preventDefault();onSignIn()}}><div className="login-brand"><div className="logo">G</div><div><b>GeM Compliance AI</b><small>AI-POWERED PROCUREMENT VERIFICATION</small></div></div><div className="login-logo">G</div><h2>Welcome back</h2><p>Sign in to your authorized officer workspace.</p><label>Official email<input type="email" defaultValue="officer@cpse.gov.in" required/></label><label>Password<span className="password-field"><input type={showPassword?'text':'password'} defaultValue="Procurement@2026" required/><button type="button" className="password-toggle" aria-label={showPassword?'Hide password':'Show password'} title={showPassword?'Hide password':'Show password'} onClick={()=>setShowPassword(!showPassword)}>{showPassword?'◉':'◌'}</button></span></label><div className="remember"><label><input type="checkbox" defaultChecked/> Remember me</label><button type="button">Forgot password?</button></div><button className="primary sign-in">Sign in securely →</button><div className="authorized">⌾ Authorized Procurement Personnel Only</div></form></div>
}

/* ---------------------------------------------------------------------- */
/* AUTHENTICATED WORKSPACE (unchanged aside from onLogout wiring)         */
/* ---------------------------------------------------------------------- */
function App({onLogout}){
 const [page,setPage]=useState('Dashboard'),[collapsed,setCollapsed]=useState(false),[showWorkflow,setWorkflow]=useState(false),[step,setStep]=useState(1),[query,setQuery]=useState(''),[selected,setSelected]=useState('ABC Technologies Pvt. Ltd.'),[expanded,setExpanded]=useState(null),[decision,setDecision]=useState(null),[remark,setRemark]=useState(''),[toast,setToast]=useState(''),[profileOpen,setProfileOpen]=useState(false);
 const notify=m=>{setToast(m);setTimeout(()=>setToast(''),2600)};
 const [selectedTender,setSelectedTender]=useState(null);
 const shown=bidders.filter(b=>b.name.toLowerCase().includes(query.toLowerCase()));
 const selectPage=p=>{setPage(p); if(p==='Bid Verification')setSelected('ABC Technologies Pvt. Ltd.')};
 const profileRef=useRef(null);
 useEffect(()=>{
  if(!profileOpen)return;
  const onOutside=e=>{if(profileRef.current&&!profileRef.current.contains(e.target))setProfileOpen(false)};
  const onKey=e=>{if(e.key==='Escape')setProfileOpen(false)};
  document.addEventListener('mousedown',onOutside);
  document.addEventListener('keydown',onKey);
  return ()=>{document.removeEventListener('mousedown',onOutside);document.removeEventListener('keydown',onKey)};
 },[profileOpen]);
 useScrollReveal([page]);
 return <div className={'app '+(collapsed?'collapsed':'')}>
  <aside className="sidebar"><div className="brand"><div className="logo">G</div>{!collapsed&&<div><b>GeM Compliance AI</b><small>AI-POWERED PROCUREMENT</small></div>}</div>
   <button className="collapse" onClick={()=>setCollapsed(!collapsed)}>{collapsed?'›':'‹'}</button>
   <nav>{nav.map((n,i)=><button key={n} className={page===n?'active':''} onClick={()=>selectPage(n)}><i>{icons[i]}</i>{!collapsed&&n}</button>)}</nav>
   <div className="officer"><div className="avatar">PO</div>{!collapsed&&<div><b>Procurement Officer</b><small><em/> Online</small></div>}</div></aside>
  <main><header><div className="crumb">{page}</div><div className="header-actions"><div className="search"><span>⌕</span><input value={query} onChange={e=>setQuery(e.target.value)} placeholder="Search tender, bidder, GSTIN..."/></div>
   <div className="profile-wrap" ref={profileRef}><button className="profile" onClick={()=>setProfileOpen(!profileOpen)} aria-haspopup="true" aria-expanded={profileOpen}><div className="avatar">PO</div><span>Procurement Officer</span><b className={profileOpen?'flip':''}>⌄</b></button>
    {profileOpen&&<div className="profile-menu" role="menu">
     <div className="profile-menu-head"><div className="avatar">PO</div><div><b>Procurement Officer</b><small>Authorized Officer</small></div></div>
     <div className="profile-menu-group">
      <button role="menuitem" onClick={()=>{setProfileOpen(false);notify('Profile settings opened')}}><i>⚙</i>Profile settings</button>
      <button role="menuitem" onClick={()=>{setProfileOpen(false);notify('Account & security opened')}}><i>🔒</i>Account & Security</button>
     </div>
     <div className="profile-menu-group">
      <button role="menuitem" className="danger" onClick={()=>{setProfileOpen(false);onLogout()}}><i>↪</i>Log out</button>
     </div>
    </div>}
   </div>
   </div></header>
   <section className="content">
    {page==='Dashboard'&&<Dashboard onNew={()=>{setStep(1);setWorkflow(true)}} onPage={selectPage} shown={shown}/>} 
    {page==='Tenders'&&<Tenders query={query} onView={tender=>{setSelectedTender(tender);setPage('Tender Details')}} onNew={()=>{setStep(1);setWorkflow(true)}}/>}
    {page==='Tender Details'&&<TenderDetails tender={selectedTender} onBack={()=>setPage('Tenders')} onVerify={()=>selectPage('Bid Verification')}/>}
    {page==='Bid Verification'&&<Verification selected={selected} setSelected={setSelected} expanded={expanded} setExpanded={setExpanded} onDecision={setDecision} notify={notify}/>}
    {page==='Risk Center'&&<Risk shown={shown} onReview={b=>{setSelected(b.name);setPage('Bid Verification')}}/>}
    {page==='Integrations'&&<Integrations notify={notify}/>}
    {page==='Reports'&&<Reports notify={notify}/>}
    {page==='Audit Trail'&&<Audit/>}
    {!['Dashboard','Tenders','Tender Details','Bid Verification','Risk Center','Integrations','Reports','Audit Trail'].includes(page)&&<Placeholder title={page}/>} 
   </section>
  </main>
  {showWorkflow&&<Workflow step={step} setStep={setStep} close={()=>setWorkflow(false)} notify={notify}/>} 
  {decision&&<Decision type={decision} remark={remark} setRemark={setRemark} close={()=>setDecision(null)} notify={notify}/>} 
  <HelpChat />
  <WhyDetails />
  {toast&&<div className="toast">✓ {toast}</div>}
 </div>
}
function Dashboard({onNew,onPage,shown}){const kpis=[['◈','12','Active Tenders','+2 this month'],['◷','28','Bids Under Verification','6 due today'],['◉','8','Pending Reviews','Action needed'],['⚠','4','High Risk Bidders','2 new this week'],['✓','146','Verified Bids','+12.5%'],['◌','18 min','Avg. Verification Time','4 min faster']];return <>
 <div className="hero"><div><p className="eyebrow">PROCUREMENT COMMAND CENTER</p><h1>Good morning, Procurement Officer</h1><p>Here’s your procurement compliance overview.</p></div></div>
 <div className="kpis">{kpis.map((x,i)=><div className="kpi reveal-on-scroll" style={{transitionDelay:(i%6)*80+'ms'}} key={x[2]}><div className="kpi-icon">{x[0]}</div><small>{x[2]}</small><strong>{x[1]}</strong><span className={x[3].includes('Action')?'warn':'trend'}>{x[3]}</span></div>)}</div>
 <div className="analytics"><div className="card chart reveal-on-scroll"><div className="card-title"><div><h3>Compliance overview</h3><p>Verification outcomes across active tenders</p></div><button>Last 7 days⌄</button></div><div className="chart-body"><div className="donut"><div><b>186</b><small>Total bids</small></div></div><div className="legend"><p><i className="dot green"/> Compliant <b>146</b><span>78%</span></p><p><i className="dot amber"/> Needs review <b>28</b><span>15%</span></p><p><i className="dot red"/> Non-compliant <b>12</b><span>7%</span></p></div></div></div><div className="card activity reveal-on-scroll" style={{transitionDelay:'100ms'}}><div className="card-title"><div><h3>Verification activity</h3><p>Document processing & review trends</p></div><button>Weekly⌄</button></div><div className="line-chart"><div className="gridlines"/><svg viewBox="0 0 500 160" preserveAspectRatio="none"><polyline points="0,120 70,105 140,119 210,70 280,90 350,45 430,58 500,20" fill="none" stroke="#1976d2" strokeWidth="4"/><polyline points="0,145 70,135 140,140 210,115 280,130 350,95 430,110 500,78" fill="none" stroke="#14a28b" strokeWidth="3"/></svg><div className="axis"><span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Fri</span><span>Sat</span><span>Sun</span></div></div><div className="chart-key"><span><i className="dot blue"/>Documents verified</span><span><i className="dot teal"/>Issues detected</span></div></div></div>
 <div className="card table-card reveal-on-scroll"><div className="card-title"><div><h3>Recent tender verification</h3><p>Track the latest verification activity</p></div><button onClick={()=>onPage('Tenders')}>View all →</button></div><table><thead><tr><th>TENDER ID</th><th>TENDER TITLE</th><th>TOTAL BIDS</th><th>VERIFIED</th><th>PENDING</th><th>HIGH RISK</th><th>STATUS</th><th/></tr></thead><tbody><tr><td className="link">GEM/2026/B/10234</td><td><b>Supply of IT Equipment</b><small>Central Public Sector Enterprise</small></td><td>8</td><td className="positive">6</td><td className="warning">2</td><td className="danger">1</td><td><Badge type="progress">In Progress</Badge></td><td><button className="view" onClick={()=>onPage('Bid Verification')}>View →</button></td></tr><tr><td className="link">GEM/2026/B/09821</td><td><b>Network Infrastructure</b><small>National Informatics Centre</small></td><td>12</td><td className="positive">12</td><td>0</td><td>0</td><td><Badge type="verified">Completed</Badge></td><td><button className="view">View →</button></td></tr></tbody></table></div>
 </>}
function Tenders({query,onView,onNew}){const tenders=[['GEM/2026/B/10234','Supply of IT Equipment','Central Public Sector Enterprise','8','6','2','26 Aug 2026','In Progress'],['GEM/2026/B/09821','Network Infrastructure Modernization','National Informatics Centre','12','12','0','21 Aug 2026','Completed'],['GEM/2026/B/09718','Cybersecurity Software Licenses','Ministry of Electronics & IT','6','3','3','29 Aug 2026','In Progress'],['GEM/2026/B/09456','Desktop Computers & Peripherals','Department of Revenue','10','0','10','02 Sep 2026','Pending'],['GEM/2026/B/09102','Data Centre Maintenance Services','Central Warehousing Corporation','5','5','0','18 Aug 2026','Completed']];const visible=tenders.filter(t=>t.slice(0,3).join(' ').toLowerCase().includes(query.toLowerCase()));return <><div className="hero"><div><p className="eyebrow">PROCUREMENT MANAGEMENT</p><h1>Active tenders</h1><p>Monitor tender verification activity, bidder submissions, and compliance progress.</p></div></div><div className="tender-summary"><div><b>12</b><span>Active tenders</span></div><div><b>28</b><span>Bids under verification</span></div><div><b>8</b><span>Reviews pending</span></div></div><div className="card table-card"><div className="card-title"><div><h3>Tender register</h3><p>{visible.length} tenders shown · Search using the global search field</p></div><button className="secondary">Status: All ⌄</button></div><table><thead><tr><th>TENDER ID</th><th>TENDER TITLE</th><th>ORGANIZATION</th><th>BIDS</th><th>VERIFIED</th><th>PENDING</th><th>DEADLINE</th><th>STATUS</th><th/></tr></thead><tbody>{visible.map(t=><tr key={t[0]}><td className="link">{t[0]}</td><td><b>{t[1]}</b></td><td>{t[2]}</td><td>{t[3]}</td><td className="positive">{t[4]}</td><td className={t[5]==='0'?'':'warning'}>{t[5]}</td><td>{t[6]}</td><td><Badge type={t[7]==='Completed'?'verified':t[7]==='Pending'?'review':'progress'}>{t[7]}</Badge></td><td><button className="view" onClick={onView}>View →</button></td></tr>)}</tbody></table>{!visible.length&&<div className="filter-empty">No tenders match your search. <button onClick={()=>window.location.reload()}>Clear search</button></div>}</div></>}
function Verification({selected,setSelected,expanded,setExpanded,onDecision,notify}){const bidder=bidders.find(x=>x.name===selected)||bidders[0];return <><div className="verify-head"><div><button className="back">← Back to verifications</button><h1>{bidder.name}</h1><p>Supply of IT Equipment <span>•</span> GEM/2026/B/10234</p></div><div><button className="secondary" onClick={()=>notify('Compliance report prepared')}>⇩ Export report</button><button className="primary" onClick={()=>onDecision('Approve / Qualify')}>Final review →</button></div></div><div className="assessment"><div className="score"><svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="42"/><circle className="score-ring" cx="50" cy="50" r="42" style={{strokeDashoffset:264-(264*bidder.score/100)}}/></svg><div><b>{bidder.score}</b><span>/100</span><small>Compliance score</small></div></div><div className="assessment-copy"><p className="eyebrow">AI VERIFICATION COMPLETE</p><h2>{bidder.score>=85?'Strong compliance profile':'Review attention required'}</h2><p>Evidence has been analyzed against 12 tender-specific requirements.</p><div><Badge type={bidder.risk==='Low'?'verified':'review'}>{bidder.risk.toUpperCase()} RISK</Badge><Badge type="progress">{bidder.state}</Badge></div></div><div className="review-summary"><b>8 <small>Verified</small></b><b>2 <small>Needs review</small></b><b>2 <small>Not verified</small></b></div></div><div className="advisory">✦ <b>AI-generated assessment.</b> Final qualification/disqualification decision must be made by the Procurement Officer.</div>
<div className="split"><div><div className="section-title"><div><h2>Compliance requirements</h2><p>Evidence-based AI assessment for this bidder</p></div><button className="secondary">Filter: All⌄</button></div>{requirements.map((r,i)=><div className={'requirement '+(expanded===i?'open':'')} key={r[0]}><button className="req-top" onClick={()=>setExpanded(expanded===i?null:i)}><span className={'status-icon '+r[1]}>{r[1]==='verified'?'✓':r[1]==='review'?'!':'×'}</span><div><b>{r[0]}</b><small>{r[1]==='verified'?'VERIFIED':r[1]==='review'?'NEEDS REVIEW':'NOT VERIFIED'}</small></div><span className="chev">⌄</span></button>{expanded===i&&<div className="req-details"><div><small>{r[2]}</small><b>{r[3]}</b></div><p>{r[1]==='review'?'Submitted financial documents indicate turnover below the tender threshold. Officer review is required.':r[1]==='failed'?'Required document was not found or could not be verified. Request clarification or verify manually.':'Source verified through document extraction and cross-document matching.'}</p><div><button className="secondary" onClick={()=>notify('Evidence viewer opened for '+r[0])}>View evidence</button><button className="text-btn" onClick={()=>notify('Auditable reasoning summary opened')}>✦ Why?</button></div></div>}</div>)}</div><aside className="right-panel"><h3>Verification details</h3><div className="detail"><small>Verification ID</small><b>VRF-2026-08492</b></div><div className="detail"><small>Processed on</small><b>23 Aug 2026, 10:42 AM</b></div><div className="detail"><small>Documents analyzed</small><b>7 documents</b></div><hr/><h3>Consistency check</h3><p className="inconsistency">⚠ Potential mismatch requiring officer review.</p><div className="match"><span>Company name</span><Badge type="review">Variation</Badge></div><div className="match"><span>PAN</span><Badge type="verified">Match</Badge></div><div className="match"><span>GSTIN</span><Badge type="verified">Match</Badge></div><button className="full secondary" onClick={()=>notify('Consistency report opened')}>View consistency report</button></aside></div></>}
function Workflow({step,setStep,close,notify}){const steps=['Tender details','Tender document','Bidder documents','AI verification']; const complete=step===4;return <div className="modal-bg"><div className="workflow"><button className="close" onClick={close}>×</button><p className="eyebrow">NEW VERIFICATION</p><h2>{complete?'AI verification in progress':'Create a tender verification'}</h2><div className="steps">{steps.map((s,i)=><span key={s} className={step===i+1?'current':step>i+1?'done':''}><i>{step>i+1?'✓':i+1}</i>{s}</span>)}</div>{step===1&&<div className="form"><label>Tender ID<input defaultValue="GEM/2026/B/10234"/></label><label>Tender title<input defaultValue="Supply of IT Equipment"/></label><label>Department / organization<select><option>Central Public Sector Enterprise</option></select></label><label>Tender category<select><option>IT & Electronics</option></select></label></div>}{step===2&&<Upload title="Upload Tender Document" text="Drop a PDF or DOCX to extract tender requirements." file="IT_Equipment_Tender.pdf"/>}{step===3&&<Upload title="Upload Bid Documents" text="Upload documents received from GeM for verification." file="GST_Certificate.pdf  ·  Udyam_Certificate.pdf  ·  PAN.pdf"/>}{step===4&&<div className="processing"><div className="loader">✦</div><h3>Analyzing tender & bidder documents</h3><p>88% complete · This takes a moment</p>{['Document extraction','Tender requirement extraction','GST verification','Udyam verification','PAN verification','Cross-document consistency check','Risk assessment','Compliance report'].map((x,i)=><div className={'process '+(i<5?'done':i===5?'active':'')} key={x}><span>{i<5?'✓':i===5?'◉':'○'}</span>{x}<small>{i<5?'Complete':i===5?'In progress':''}</small></div>)}</div>}<div className="modal-footer"><button className="secondary" onClick={step===1?close:()=>setStep(step-1)}>Back</button><button className="primary" onClick={()=>complete?(close(),notify('Verification completed — report is ready')):setStep(step+1)}>{complete?'View compliance report':'Continue →'}</button></div></div></div>}
function Upload({title,text,file}){return <div className="upload"><div className="upload-icon">⇧</div><h3>{title}</h3><p>{text}</p><button className="secondary">Choose files</button><div className="uploaded">✓ <b>{file}</b><span>AI extraction ready</span></div></div>}
function Decision({type,remark,setRemark,close,notify}){return <div className="modal-bg"><div className="decision"><button className="close" onClick={close}>×</button><p className="eyebrow">FINAL PROCUREMENT REVIEW</p><h2>{type} bidder?</h2><div className="advisory">⚠ <b>AI recommendations are advisory only.</b> The Procurement Officer is solely responsible for the final procurement decision.</div><p>I have reviewed the available evidence and am making this decision based on my assessment.</p><label>Officer remarks <textarea value={remark} onChange={e=>setRemark(e.target.value)} placeholder="Add mandatory decision remarks..."/></label><div className="modal-footer"><button className="secondary" onClick={close}>Cancel</button><button className="primary" disabled={!remark} onClick={()=>{close();notify(type+' recorded in audit trail')}}>Confirm decision</button></div></div></div>}
function Risk({shown,onReview}){return <><div className="hero"><div><p className="eyebrow">RISK INTELLIGENCE</p><h1>Bidder risk center</h1><p>Prioritize evidence-based review across active tenders.</p></div></div><div className="risk-stats"><div><b>4</b><span>High risk bidders</span></div><div><b>11</b><span>Medium risk bidders</span></div><div><b>13</b><span>Low risk bidders</span></div></div><div className="card table-card"><div className="card-title"><div><h3>Risk queue</h3><p>Sorted by potential impact</p></div><button className="secondary">Filter risk⌄</button></div><table><thead><tr><th>BIDDER</th><th>TENDER</th><th>SCORE</th><th>RISK</th><th>MAIN ISSUE</th><th>ACTION</th></tr></thead><tbody>{shown.map(b=><tr key={b.name}><td><b>{b.name}</b></td><td className="link">GEM/2026/B/10234</td><td><b>{b.score}/100</b></td><td><Badge type={b.risk.toLowerCase()}>{b.risk}</Badge></td><td>{b.issue}</td><td><button className="view" onClick={()=>onReview(b)}>Review →</button></td></tr>)}</tbody></table></div></>}
const integrationWebsites={
 'GSTN':{primary:'https://www.gst.gov.in/'},
 'Udyam / MSME':{primary:'https://udyamregistration.gov.in/'},
 'PAN / Income Tax':{primary:'https://www.incometax.gov.in/'},
 'MCA21':{primary:'https://www.mca.gov.in/'},
 'Startup India':{primary:'https://www.startupindia.gov.in/'},
 'DigiLocker':{primary:'https://www.digilocker.gov.in/'},
 'BIS / DPIIT':{primary:'https://www.bis.gov.in/',secondary:{label:'DPIIT',url:'https://www.dpiit.gov.in/'}},
 'Blacklisting / Debarment':{primary:'https://gem.gov.in/'}
};
function Integrations({notify}){
 const [integrations,setIntegrations]=useState(()=>['GSTN','Udyam / MSME','PAN / Income Tax','MCA21','Startup India','DigiLocker','BIS / DPIIT','Blacklisting / Debarment'].map((name,i)=>({
  name,
  status:i===3?'Sandbox':'Demo connected',
  environment:i===3?'Sandbox':'Demo',
  lastSync:i===3?'1 day ago':'2 minutes ago',
  requests:1248-i*103,
  website:integrationWebsites[name].primary,
  secondary:integrationWebsites[name].secondary
 })));
 const [configFor,setConfigFor]=useState(null);
 const updateIntegration=(name,patch)=>setIntegrations(prev=>prev.map(it=>it.name===name?{...it,...patch}:it));
 return <><div className="hero"><div><p className="eyebrow">GOVERNMENT SOURCE VERIFICATION</p><h1>Integrations</h1><p>Connection status and verification activity for official data sources.</p></div></div><div className="integration-grid">{integrations.map(it=><div className="card integration" key={it.name}><div className="int-icon">{it.name.slice(0,2)}</div><div><h3><a className="integration-name-link" href={it.website} target="_blank" rel="noopener noreferrer" title={'Open the official '+it.name+' website'}>{it.name}<span className="ext-icon" aria-hidden="true">↗</span></a>{it.secondary&&<a className="integration-secondary-link" href={it.secondary.url} target="_blank" rel="noopener noreferrer" title={'Open the official '+it.secondary.label+' website'}>{it.secondary.label}<span className="ext-icon" aria-hidden="true">↗</span></a>}</h3><Badge type={it.status==='Sandbox'?'review':'verified'}>{it.status}</Badge></div><p>Last synchronized {it.lastSync}</p><b>{it.requests} <small>verification requests</small></b><button onClick={()=>setConfigFor(it)}>Configure →</button></div>)}</div><p className="demo-note">All integrations are clearly labelled Demo / Sandbox in this prototype; no live government system access is implied.</p>
  {configFor&&<IntegrationConfigModal integration={configFor} onClose={()=>setConfigFor(null)} onSave={patch=>{updateIntegration(configFor.name,patch);notify(configFor.name+' configuration saved successfully.');setConfigFor(null)}} onTestSuccess={()=>updateIntegration(configFor.name,{status:'Demo connected',environment:'Demo',lastSync:'just now'})}/>}
 </>}

function IntegrationConfigModal({integration,onClose,onSave,onTestSuccess}){
 const [environment,setEnvironment]=useState(integration.environment);
 const [testState,setTestState]=useState('idle');
 useEffect(()=>{
  const onKey=e=>{if(e.key==='Escape')onClose()};
  document.addEventListener('keydown',onKey);
  return ()=>document.removeEventListener('keydown',onKey);
 },[onClose]);
 const runTest=()=>{
  setTestState('testing');
  setTimeout(()=>{setTestState('success');onTestSuccess()},900);
 };
 const displayStatus=testState==='success'?'Demo connected':integration.status;
 return <div className="modal-bg" onMouseDown={e=>{if(e.target===e.currentTarget)onClose()}}>
  <div className="integration-modal" role="dialog" aria-modal="true" aria-label={'Configure '+integration.name}>
   <button className="close" onClick={onClose} aria-label="Close">×</button>
   <p className="eyebrow">INTEGRATION SETTINGS</p>
   <h2>Configure {integration.name}</h2>
   <div className="integration-modal-summary">
    <div><small>Integration</small><b>{integration.name}</b></div>
    <div><small>Connection status</small><Badge type={displayStatus==='Sandbox'?'review':'verified'}>{displayStatus}</Badge></div>
    <div><small>Last synchronized</small><b>{integration.lastSync}</b></div>
    <div><small>Verification requests</small><b>{integration.requests}</b></div>
   </div>
   <label>Environment<select value={environment} onChange={e=>setEnvironment(e.target.value)}><option value="Demo">Demo</option><option value="Sandbox">Sandbox</option></select></label>
   <label>API / Portal endpoint<input value={integration.website} readOnly/></label>
   <div className="integration-modal-fields">
    <label>Client ID<input placeholder="demo-client-id"/></label>
    <label>Client Secret<input type="password" placeholder="••••••••"/></label>
    <label>API Key<input placeholder="demo-api-key"/></label>
    <label>Access Token<input placeholder="demo-access-token"/></label>
   </div>
   <p className="integration-modal-note">This is a prototype. No real government credentials are stored or transmitted, and no live API requests are made — Test Connection simulates a result locally.</p>
   {testState!=='idle'&&<div className={'integration-test-result '+testState}>{testState==='testing'?'Testing connection...':'✓ Connection successful'}</div>}
   <div className="modal-footer">
    <button className="secondary" onClick={onClose}>Cancel</button>
    <button className="secondary" onClick={runTest} disabled={testState==='testing'}>{testState==='testing'?'Testing connection...':'Test Connection'}</button>
    <button className="primary" onClick={()=>onSave({environment,status:environment==='Demo'?'Demo connected':'Sandbox'})}>Save Configuration</button>
   </div>
  </div>
 </div>
}
function Reports({notify}){return <><div className="hero"><div><p className="eyebrow">AUDITABLE OUTPUTS</p><h1>Reports</h1><p>Generate procurement-ready compliance and risk reports.</p></div></div><div className="report-grid">{['Bid Compliance Report','Tender Compliance Summary','Risk Assessment Report','Audit Report','Government Verification Report'].map(x=><div className="card report" key={x}><div>▧</div><h3>{x}</h3><p>Exported with tender-specific evidence and officer review trail.</p><button className="primary" onClick={()=>notify(x+' generated')}>Generate Report</button></div>)}</div></>}
function Audit(){return <><div className="hero"><div><p className="eyebrow">EVIDENCE TRACEABILITY</p><h1>Audit trail</h1><p>Every verification and officer action in one immutable review log.</p></div><button className="secondary">⇩ Export logs</button></div><div className="card table-card"><table><thead><tr><th>TIMESTAMP</th><th>USER</th><th>TENDER</th><th>BIDDER</th><th>ACTION</th><th>RESULT</th></tr></thead><tbody>{[['10:21 AM','Procurement Officer','GEM/2026/B/10234','ABC Technologies','GST Verification','Completed'],['10:24 AM','AI Verification Engine','GEM/2026/B/10234','ABC Technologies','OEM Authorization','Issue detected'],['10:31 AM','Procurement Officer','GEM/2026/B/10234','ABC Technologies','Compliance reviewed','Recorded']].map(r=><tr key={r[0]}>{r.map((x,i)=><td key={i}>{i===5?<Badge type={x==='Completed'?'verified':'review'}>{x}</Badge>:x}</td>)}</tr>)}</tbody></table></div></>}
function Placeholder({title}){return <div className="empty"><div>◈</div><h1>{title}</h1><p>This working prototype is ready to be configured for your procurement process.</p></div>}

function HelpChat(){
 const [open,setOpen]=useState(false),[input,setInput]=useState('');
 const [messages,setMessages]=useState([{role:'bot',text:'Hello! I’m the GeM Compliance AI assistant. Ask me how to use any feature in this workspace.'}]);
 const answer=(question)=>{const q=question.toLowerCase();if(q.includes('report'))return 'Open Reports from the sidebar, choose a report type, then select Generate Report. The prototype prepares a tender-specific report with evidence and officer review context.';if(q.includes('verification')||q.includes('upload'))return 'Select New Verification on the dashboard. Add tender details, upload the tender and bidder documents, then follow the AI verification progress. The officer reviews the final results.';if(q.includes('risk'))return 'Risk Center prioritizes bidders by low, medium, or high risk. Open a bidder’s Review action to inspect the evidence and compliance requirements.';if(q.includes('decision')||q.includes('approve')||q.includes('reject'))return 'AI recommendations are advisory only. In Bid Verification, use Final Review, add mandatory officer remarks, and confirm your assessment to record it in the audit trail.';if(q.includes('evidence')||q.includes('document'))return 'Expand a compliance requirement and select View evidence to inspect the extracted document information. You can also use Why? for a concise, auditable AI reasoning summary.';return 'I can help with verification, bidder risk, evidence, reports, audit trail, and officer decisions. Try asking, “How do I generate a report?”';};
 const send=(value=input)=>{const text=value.trim();if(!text)return;setMessages(current=>[...current,{role:'user',text},{role:'bot',text:answer(text)}]);setInput('')};
 return <div className={'help-chat '+(open?'open':'')}><div className="chat-window"><div className="chat-head"><div><span>✦</span><div><b>GeM AI Assistant</b><small>Demo website help</small></div></div><button onClick={()=>setOpen(false)} aria-label="Close assistant">×</button></div><div className="chat-messages">{messages.map((message,index)=><div className={'chat-message '+message.role} key={index}>{message.text}</div>)}</div><div className="chat-prompts"><button onClick={()=>send('How do I start a verification?')}>Start verification</button><button onClick={()=>send('How do I generate a report?')}>Generate a report</button></div><form className="chat-input" onSubmit={e=>{e.preventDefault();send()}}><input value={input} onChange={e=>setInput(e.target.value)} placeholder="Ask about this website..."/><button aria-label="Send message">↑</button></form></div><button className="chat-launcher" onClick={()=>setOpen(!open)} aria-label="Open AI website help"><span>✦</span><b>Need help?</b></button></div>
}

function WhyDetails(){
 const [detail,setDetail]=useState(null);
 React.useEffect(()=>{const open=(event)=>{const button=event.target.closest('.text-btn');if(!button||!button.textContent.includes('Why?'))return;const card=button.closest('.requirement');const name=card?.querySelector('.req-top b')?.textContent||'Compliance requirement';const status=card?.querySelector('.req-top small')?.textContent||'REVIEW REQUIRED';setDetail({name,status})};document.addEventListener('click',open);return()=>document.removeEventListener('click',open)},[]);
 if(!detail)return null;
 const isVerified=detail.status==='VERIFIED';
 return <div className="why-overlay" role="dialog" aria-modal="true" aria-label="AI reasoning summary"><div className="why-card"><button className="close" onClick={()=>setDetail(null)} aria-label="Close explanation">×</button><p className="eyebrow">AI EXPLAINABILITY</p><h2>Why this result?</h2><div className="why-row"><small>Requirement</small><b>{detail.name}</b></div><div className="why-row"><small>Assessment</small><Badge type={isVerified?'verified':'review'}>{detail.status}</Badge></div><div className="why-row"><small>Evidence found</small><b>{isVerified?'Verified bidder document and matching registration details':'Submitted documents and tender-specific requirements'}</b></div><div className="why-row"><small>AI finding</small><p>{isVerified?'Information was extracted from the document and matched against related bidder information. No material inconsistency was detected.':'Available evidence needs officer review before a procurement decision is made.'}</p></div><div className="why-recommendation"><b>Recommended next step</b><p>{isVerified?'Review the linked evidence if needed, then continue with the procurement assessment.':'Inspect the linked evidence and add an officer remark after your review.'}</p></div><p className="why-note">This is a concise, auditable evidence summary—not hidden model reasoning. The Procurement Officer makes the final decision.</p><button className="primary" onClick={()=>setDetail(null)}>Understood</button></div></div>
}

function VerificationWithFilter({selected,setSelected,expanded,setExpanded,onDecision,notify}){
 const [filter,setFilter]=useState('all');
 const [filterOpen,setFilterOpen]=useState(false);
 const bidder=bidders.find(x=>x.name===selected)||bidders[0];
 const labels={all:'All',verified:'Verified',review:'Needs Review',failed:'Not Verified'};
 const shown=requirements.map((item,index)=>({item,index})).filter(({item})=>filter==='all'||item[1]===filter);
 return <>
  <div className="verify-head"><div><button className="back">← Back to verifications</button><h1>{bidder.name}</h1><p>Supply of IT Equipment <span>•</span> GEM/2026/B/10234</p></div><div><button className="secondary" onClick={()=>notify('Compliance report prepared')}>⇩ Export report</button><button className="primary" onClick={()=>onDecision('Approve / Qualify')}>Final review →</button></div></div>
  <div className="assessment"><div className="score"><svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="42"/><circle className="score-ring" cx="50" cy="50" r="42" style={{strokeDashoffset:264-(264*bidder.score/100)}}/></svg><div><b>{bidder.score}</b><span>/100</span><small>Compliance score</small></div></div><div className="assessment-copy"><p className="eyebrow">AI VERIFICATION COMPLETE</p><h2>{bidder.score>=85?'Strong compliance profile':'Review attention required'}</h2><p>Evidence has been analyzed against 12 tender-specific requirements.</p><Badge type={bidder.risk==='Low'?'verified':'review'}>{bidder.risk.toUpperCase()} RISK</Badge></div><div className="review-summary"><b>8 <small>Verified</small></b><b>2 <small>Needs review</small></b><b>2 <small>Not verified</small></b></div></div>
  <div className="advisory">✦ <b>AI-generated assessment.</b> Final qualification/disqualification decision must be made by the Procurement Officer.</div>
  <div className="split"><div><div className="section-title"><div><h2>Compliance requirements</h2><p>Evidence-based AI assessment for this bidder</p></div><div className="filter-control"><button className="secondary filter-button" onClick={()=>setFilterOpen(!filterOpen)} aria-expanded={filterOpen}>Filter: {labels[filter]} <span>⌄</span></button>{filterOpen&&<div className="filter-menu">{Object.entries(labels).map(([value,label])=><button key={value} className={filter===value?'selected':''} onClick={()=>{setFilter(value);setFilterOpen(false);setExpanded(null)}}><i>{filter===value?'✓':''}</i>{label}</button>)}</div>}</div></div>
   {shown.length?shown.map(({item:r,index:i})=><div className={'requirement '+(expanded===i?'open':'')} key={r[0]}><button className="req-top" onClick={()=>setExpanded(expanded===i?null:i)}><span className={'status-icon '+r[1]}>{r[1]==='verified'?'✓':r[1]==='review'?'!':'×'}</span><div><b>{r[0]}</b><small>{r[1]==='verified'?'VERIFIED':r[1]==='review'?'NEEDS REVIEW':'NOT VERIFIED'}</small></div><span className="chev">⌄</span></button>{expanded===i&&<div className="req-details"><div><small>{r[2]}</small><b>{r[3]}</b></div><p>{r[1]==='review'?'Submitted financial documents indicate turnover below the tender threshold. Officer review is required.':r[1]==='failed'?'Required document was not found or could not be verified. Request clarification or verify manually.':'Source verified through document extraction and cross-document matching.'}</p><div><button className="secondary" onClick={()=>notify('Evidence viewer opened for '+r[0])}>View evidence</button><button className="text-btn" onClick={()=>notify('Auditable reasoning summary opened')}>✦ Why?</button></div></div>}</div>):<div className="filter-empty">No requirements match this filter. <button onClick={()=>setFilter('all')}>Show all</button></div>}</div>
   <aside className="right-panel"><h3>Verification details</h3><div className="detail"><small>Verification ID</small><b>VRF-2026-08492</b></div><div className="detail"><small>Processed on</small><b>23 Aug 2026, 10:42 AM</b></div><div className="detail"><small>Documents analyzed</small><b>7 documents</b></div><hr/><h3>Consistency check</h3><p className="inconsistency">⚠ Potential mismatch requiring officer review.</p><div className="match"><span>Company name</span><Badge type="review">Variation</Badge></div><div className="match"><span>PAN</span><Badge type="verified">Match</Badge></div><div className="match"><span>GSTIN</span><Badge type="verified">Match</Badge></div><button className="full secondary" onClick={()=>notify('Consistency report opened')}>View consistency report</button></aside>
  </div>
 </>
}
function TenderList({query,onView,onNew}){
 const tenders=[
  {id:'GEM/2026/B/10234',title:'Supply of IT Equipment',organization:'Central Public Sector Enterprise',status:'In Progress',bids:8,deadline:'26 Aug 2026',category:'IT & Electronics'},
  {id:'GEM/2026/B/09821',title:'Network Infrastructure Modernization',organization:'National Informatics Centre',status:'Completed',bids:12,deadline:'21 Aug 2026',category:'Network Infrastructure'},
  {id:'GEM/2026/B/09718',title:'Cybersecurity Software Licenses',organization:'Ministry of Electronics & IT',status:'In Progress',bids:6,deadline:'29 Aug 2026',category:'Cybersecurity'},
  {id:'GEM/2026/B/09456',title:'Desktop Computers & Peripherals',organization:'Department of Revenue',status:'Pending',bids:10,deadline:'02 Sep 2026',category:'IT Hardware'},
  {id:'GEM/2026/B/09102',title:'Data Centre Maintenance Services',organization:'Central Warehousing Corporation',status:'Completed',bids:5,deadline:'18 Aug 2026',category:'Managed Services'}
 ];
 const visible=tenders.filter(t=>`${t.id} ${t.title}`.toLowerCase().includes(query.toLowerCase()));
 return <><div className="hero"><div><p className="eyebrow">PROCUREMENT MANAGEMENT</p><h1>Tenders</h1><p>Select a tender to view its complete verification workspace.</p></div></div><div className="tender-title-list">{visible.map((t,index)=><button className="tender-title-bar" onClick={()=>onView(t)} key={t.id}><span className="tender-index">{String(index+1).padStart(2,'0')}</span><span className="tender-title-copy"><b>{t.title}</b><small>{t.id} · {t.organization}</small></span><Badge type={t.status==='Completed'?'verified':t.status==='Pending'?'review':'progress'}>{t.status}</Badge><span className="tender-slider" aria-label={'Open '+t.title}>→</span></button>)}</div>{!visible.length&&<div className="filter-empty">No tenders match your search.</div>}</>
}
function TenderDetails({tender,onBack,onVerify}){
 const t=tender||{id:'GEM/2026/B/10234',title:'Supply of IT Equipment',organization:'Central Public Sector Enterprise',status:'In Progress',bids:8,deadline:'26 Aug 2026',category:'IT & Electronics'};
 return <><div className="verify-head"><div><button className="back" onClick={onBack}>← Back to tenders</button><h1>{t.title}</h1><p>{t.id} <span>•</span> {t.organization}</p></div><div><button className="secondary">⇩ Export tender summary</button><button className="primary" onClick={onVerify}>Open bid verification →</button></div></div><div className="tender-detail-banner"><div><small>TENDER STATUS</small><h2>{t.status}</h2><p>{t.category}</p></div><div><small>SUBMISSION DEADLINE</small><b>{t.deadline}</b><p>11:59 PM IST</p></div><div><small>BIDDER SUBMISSIONS</small><b>{t.bids}</b><p>Documents received through GeM</p></div><div><small>COMPLIANCE PROGRESS</small><b>75%</b><div className="tender-progress"><span/></div></div></div><div className="tender-detail-grid"><div className="card tender-info"><h3>Tender information</h3><div className="info-grid"><div><small>Tender ID</small><b>{t.id}</b></div><div><small>Organization</small><b>{t.organization}</b></div><div><small>Category</small><b>{t.category}</b></div><div><small>Evaluation method</small><b>Technical compliance review</b></div><div><small>Requirements extracted</small><b>12 compliance requirements</b></div><div><small>Document status</small><b>AI extraction complete</b></div></div></div><div className="card tender-info"><h3>Verification progress</h3><div className="progress-list"><p><span>✓</span> Tender document analyzed <b>Complete</b></p><p><span>✓</span> Bidder documents received <b>{t.bids} bidders</b></p><p><span>◉</span> Compliance verification <b>In progress</b></p><p><span>○</span> Final officer review <b>Pending</b></p></div></div></div><div className="card table-card"><div className="card-title"><div><h3>Bidder submissions</h3><p>Verification status for this tender</p></div></div><table><thead><tr><th>BIDDER</th><th>COMPLIANCE SCORE</th><th>RISK</th><th>STATUS</th><th>ACTION</th></tr></thead><tbody>{bidders.map(b=><tr key={b.name}><td><b>{b.name}</b></td><td>{b.score}/100</td><td><Badge type={b.risk.toLowerCase()}>{b.risk}</Badge></td><td><Badge type={b.state==='Verified'?'verified':'review'}>{b.state}</Badge></td><td><button className="view" onClick={onVerify}>Review →</button></td></tr>)}</tbody></table></div></>
}
Tenders = TenderList;
Verification = VerificationWithFilter;
createRoot(document.getElementById('root')).render(<AppRouter/>);