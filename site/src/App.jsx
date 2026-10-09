import React, { useMemo, useState } from "react";
import example from "../../examples/receipt_example.json";
import {
  FIELDS, CONSTRAINT, COHERENCE, DIMENSIONS, SCALES, ARCHETYPES, CLASSIFICATIONS,
  C_STAR, PHI, calculate, coordinateKey, scenarioDocument,
} from "./engine.js";

const REPO="https://github.com/MichaelWave369/DCL";
const INITIAL=example.scores;
const CLOSE=(v,digits=3)=>Number(v).toFixed(digits);
const COORDS=[
  ["dimension_id","DIMENSION",DIMENSIONS],
  ["field_variable_id","FIELD VARIABLE",FIELDS.map(f=>f.key+" / "+f.name)],
  ["scale_id","SCALE",SCALES],
  ["archetype_id","ARCHETYPE",ARCHETYPES],
];
const LABELS={
  D_score:"Constraint index",Phi_score:"Coherence index",DCR:"Constraint ratio",CMI:"Matrix index",
};
function Icon({name,size=18}) {
  const common={width:size,height:size,viewBox:"0 0 24 24",fill:"none",stroke:"currentColor",strokeWidth:1.6,strokeLinecap:"round",strokeLinejoin:"round","aria-hidden":"true"};
  if(name==="arrow")return <svg {...common}><path d="M5 12h14m-7-7 7 7-7 7"/></svg>;
  if(name==="github")return <svg {...common}><path d="M9 19c-4.8 1.3-4.8-2.8-6.7-3.2m13.4 6v-3.7c0-1.1.1-1.5-.5-2.2 1.8-.2 3.7-.8 3.7-4.6 0-1-.3-2-1-2.7.1-.5.4-2-.1-2.7 0 0-1.3-.3-2.8 1.2a9.6 9.6 0 0 0-5.2 0C8.3 5.6 7 5.9 7 5.9c-.5.7-.2 2.2-.1 2.7-.7.7-1 1.7-1 2.7 0 3.8 1.9 4.4 3.7 4.6-.5.6-.5 1.3-.5 2.2v3.7"/><path d="M12 22c5.5 0 10-4.5 10-10S17.5 2 12 2 2 6.5 2 12s4.5 10 10 10Z"/></svg>;
  if(name==="download")return <svg {...common}><path d="M12 3v12m-4-4 4 4 4-4M4 17v4h16v-4"/></svg>;
  if(name==="rotate")return <svg {...common}><path d="M3 12a9 9 0 1 0 3-6.7L3 8m0-5v5h5"/></svg>;
  return <svg {...common}><circle cx="12" cy="12" r="9"/><path d="M12 7v5m0 4h.01"/></svg>;
}
function FieldControl({field,value,onChange}) {
  return <label className="field-control">
    <span className="field-head"><span className="field-key">{field.key}</span><span className="field-name">{field.name}</span><output>{CLOSE(value,2)}</output></span>
    <input type="range" min="0" max="1" step=".01" value={value}
      onChange={e=>onChange(field.key,Number(e.target.value))}
      aria-label={field.name} title={field.hint}
      style={{"--fill":(value*100)+"%"}} />
    <span className="field-ends"><span>LOW</span><span>HIGH</span></span>
  </label>;
}
function Orbital() {
  return <div className="orbital" aria-hidden="true">
    <div className="orbital-fog"/>
    <div className="orbital-ring orbital-ring-1"/>
    <div className="orbital-ring orbital-ring-2"/>
    <div className="orbital-ring orbital-ring-3"/>
    <div className="orbital-inner"><span className="orbital-glyph">Φ</span><span className="orbital-inner-label">DCL / Ω</span></div>
    <span className="orbit-signal signal-1">D / CONSTRAINT</span>
    <span className="orbit-signal signal-2">Φ / COHERENCE</span>
    <span className="orbit-signal signal-3">OBSERVATION 001</span>
    <div className="orbital-crosshair"/>
  </div>;
}
function CardMetric({overline,value,note,tone}) {
  return <div className={"metric-card "+tone}>
    <span>{overline}</span><strong>{value}</strong><small>{note}</small>
  </div>;
}
function Band({cmi,classification}) {
  return <div className="band-wrap"><div className="band-track">
    {CLASSIFICATIONS.map((item,index)=><div key={item.key}
      className={"band-part "+(item.key===classification?"selected":"")}
      title={item.label}><span>{index+1}</span></div>)}
    <div className="band-needle" style={{left:(cmi*100)+"%"}}><b/></div>
  </div>
  <div className="band-ends"><span>0.0 / LOW CONSTRAINT</span><span>1.0 / HIGH CONSTRAINT</span></div></div>;
}
function LatticeAxis({id,label,options,value,onChange}) {
  return <label className="axis"><span>{label} / {String(value).padStart(2,"0")}</span>
    <select aria-label={label.toLowerCase()} value={value} onChange={e=>onChange(id,Number(e.target.value))}>
      {options.map((name,i)=><option key={i+1} value={i+1}>{String(i+1).padStart(2,"0")} / {name}</option>)}
    </select>
  </label>;
}

export default function App() {
  const [scores,setScores]=useState({...INITIAL});
  const [coordinate,setCoordinate]=useState({...example.coordinate});
  const [showFormula,setShowFormula]=useState(false);
  const [exportMessage,setExportMessage]=useState("");
  const computed=useMemo(()=>calculate(scores),[scores]);
  const initial=useMemo(()=>calculate(INITIAL),[]);
  const coordKey=coordinateKey(coordinate);
  const setScore=(key,value)=>{setScores(prev=>({...prev,[key]:value}));setExportMessage("")};
  const setCoord=(key,value)=>setCoordinate(prev=>({...prev,[key]:value}));
  const reset=()=>{setScores({...INITIAL});setCoordinate({...example.coordinate});setExportMessage("Sample scenario restored.");};
  function exportScenario(){
    const payload=scenarioDocument(scores,coordinate);
    const url=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)+"\n"],{type:"application/json"}));
    const element=document.createElement("a");element.href=url;element.download="dcl-observatory-scenario.json";
    document.body.appendChild(element);element.click();element.remove();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
    setExportMessage("Scenario downloaded. This is NOT a canonical DCL observation receipt.");
  }
  const dominantConstraint=FIELDS.find(f=>f.key===computed.dominant_constraint);
  const dominantCoherence=FIELDS.find(f=>f.key===computed.dominant_coherence);
  const thresholdClass=computed.phi369_threshold_met?"threshold-yes":"threshold-no";
  return <div className="app-shell" id="home">
    <header className="site-header">
      <a href="#home" className="wordmark"><span className="mark"><span>⌘</span></span><span className="wordmark-text"><b>DCL<span className="wordmark-dot">.</span></b><small>DEMIURGIC COSMOLOGY LATTICE</small></span></a>
      <nav aria-label="Site navigation"><a href="#lab">Signal lab</a><a href="#lattice">Lattice</a><a href="#receipt">Receipt</a><a href="#method">Method</a></nav>
      <a className="header-repo" href={REPO} target="_blank" rel="noopener noreferrer"><Icon name="github" size={17}/> Source ↗</a>
    </header>
    <main>
      <section className="hero">
        <div className="hero-left">
          <div className="eyebrow"><span className="signal-dot"/> OBSERVATORY / RUNTIME v0.1 / PUBLIC RESEARCH</div>
          <h1>Observe the pattern.<br/><em>Test the structure.</em></h1>
          <p className="hero-description">A transparent, local-first instrument for exploring <strong>constraint, coherence and observation receipts</strong> using the Demiurgic Cosmology Lattice model.</p>
          <div className="hero-actions"><a href="#lab" className="action-primary">Enter the signal lab <Icon name="arrow"/></a><a href="#receipt" className="action-secondary">Inspect sample receipt ↗</a></div>
          <div className="truth-strip"><span className="tiny-square"/> MODEL COHERENCE ≠ METAPHYSICAL PROOF</div>
        </div>
        <Orbital/>
      </section>
      <section className="system-strip" aria-label="DCL research model overview">
        <div><b>12</b><span>FIELD VARIABLES</span></div>
        <div><b>04</b><span>LATTICE AXES</span></div>
        <div><b>20,736</b><span>CONCEPTUAL CELLS</span></div>
        <div><b>LOCAL</b><span>NO DATA UPLOADS</span></div>
      </section>

      <section id="lab" className="lab-section">
        <div className="section-heading"><div><p className="section-kicker">01 / INTERACTIVE RESEARCH INSTRUMENT</p><h2>Constraint × coherence</h2><p>Adjust the twelve bounded variables to explore how DCL v0.1 transforms observations into internal model scores.</p></div><span className="section-status"><span className="signal-dot"/> LOCAL SIMULATION</span></div>
        <div className="lab-toolbar"><span><span className="cross">＋</span> SAMPLE SCENARIO LOADED</span><div className="tool-buttons"><button type="button" onClick={reset}><Icon name="rotate" size={15}/> Reset</button><button type="button" className="export" onClick={exportScenario}><Icon name="download" size={15}/> Export scenario</button></div></div>
        {exportMessage&&<p className="export-note" role="status">{exportMessage}</p>}
        <div className="lab-grid">
          <div className="variable-area">
            <div className="variable-card constraint-card"><div className="variable-card-head"><span><i className="square yellow"/> D / CONSTRAINT</span><strong>01—06</strong></div><p>Pressure toward restriction, recurrence and extraction.</p>
              <div className="field-list">{CONSTRAINT.map(f=><FieldControl key={f.key} field={f} value={scores[f.key]} onChange={setScore}/>)}</div>
            </div>
            <div className="variable-card coherence-card"><div className="variable-card-head"><span><i className="square teal"/> Φ / COHERENCE</span><strong>07—12</strong></div><p>Clarity, integration, agency and life-value in the model.</p>
              <div className="field-list">{COHERENCE.map(f=><FieldControl key={f.key} field={f} value={scores[f.key]} onChange={setScore}/>)}</div>
            </div>
          </div>
          <aside className="results-panel">
            <div className="results-title"><span>COMPUTED OUTPUT</span><span>LIVE / NON-CANONICAL</span></div>
            <div className="score-meter"><div className="score-meter-row"><div><span>CONSTRAINT / D</span><strong>{CLOSE(computed.D_score)}</strong></div><div className="meter-track"><i className="meter-fill amber" style={{width:(computed.D_score*100)+"%"}}/></div></div>
              <div className="score-meter-row"><div><span>COHERENCE / Φ</span><strong>{CLOSE(computed.Phi_score)}</strong></div><div className="meter-track"><i className="meter-fill cyan" style={{width:(computed.Phi_score*100)+"%"}}/></div></div>
            </div>
            <div className="result-tiles">
              <CardMetric overline="DCR / RATIO" value={CLOSE(computed.DCR)} note="D / (Φ + ε)" tone="ratio"/>
              <CardMetric overline="CMI / INDEX" value={CLOSE(computed.CMI)} note="sigmoid(5 × (D−Φ))" tone="index"/>
            </div>
            <div className="class-section"><p>FIELD CLASSIFICATION</p><h3>{computed.classification_label}</h3><Band cmi={computed.CMI} classification={computed.classification}/>
              <span className="class-footnote">Classification is a rule of the DCL model, not a diagnosis or external finding.</span></div>
            <div className="dominants"><div><span>DOMINANT CONSTRAINT</span><strong>{dominantConstraint?.name}</strong><small>{computed.dominant_constraint} · {CLOSE(scores[computed.dominant_constraint],2)}</small></div><div><span>DOMINANT COHERENCE</span><strong>{dominantCoherence?.name}</strong><small>{computed.dominant_coherence} · {CLOSE(scores[computed.dominant_coherence],2)}</small></div></div>
            <div className={"threshold "+thresholdClass}><span>Φ369 HEURISTIC THRESHOLD</span><strong>{computed.phi369_threshold_met?"MET":"NOT MET"}</strong><small>Φ ≥ {CLOSE(C_STAR,4)} and DCR &lt; 1.0</small></div>
            <p className="comparison-note">Change from bundled example · ΔD {computed.D_score-initial.D_score>=0?"+":""}{CLOSE(computed.D_score-initial.D_score)} · ΔΦ {computed.Phi_score-initial.Phi_score>=0?"+":""}{CLOSE(computed.Phi_score-initial.Phi_score)}</p>
            <button className="formula-toggle" type="button" aria-expanded={showFormula} onClick={()=>setShowFormula(v=>!v)}>See exact formulas <span>{showFormula?"−":"+"}</span></button>
            {showFormula&&<div className="formula-details"><p><b>D</b> = (B + R + I_g + S + E_x + D_c) / 6</p><p><b>Φ</b> = (C_o + K + A + M + L_v + R_s) / 6</p><p><b>DCR</b> = D / (Φ + 0.000001)</p><p><b>CMI</b> = 1 / (1 + exp(−5(D−Φ)))</p><p><b>Φ threshold</b> = φ / 2, where φ = {PHI}</p></div>}
          </aside>
        </div>
      </section>

      <section className="lattice-section" id="lattice">
        <div className="section-heading"><div><p className="section-kicker">02 / COORDINATE INDEX</p><h2>The 12⁴ lattice</h2><p>Browse DCL's four conceptual classification axes. Selecting a coordinate changes its index, not the measured world.</p></div><div className="lattice-stamp">12 × 12 × 12 × 12</div></div>
        <div className="lattice-grid"><div className="lattice-form"><div className="lattice-form-head">COORDINATE EXPLORER <span>04 AXES</span></div>
          {COORDS.map(([key,title,options])=><LatticeAxis key={key} id={key} label={title} options={options} value={coordinate[key]} onChange={setCoord}/>)}
        </div><div className="lattice-output"><p>SELECTED LATTICE ADDRESS</p><h3>{coordKey}</h3><div className="lattice-visual" aria-hidden="true"><div className="lattice-mesh"/><span className="lattice-center">⌖</span></div><span className="lattice-note">20,736 possible addresses · 1 selected</span><p className="lattice-caution">These axes form a conceptual taxonomy. They are not claims of 12 observed physical dimensions.</p></div></div>
      </section>

      <section className="receipt-section" id="receipt">
        <div className="section-heading"><div><p className="section-kicker">03 / INSPECTABLE SOURCE OBJECT</p><h2>Observation receipt</h2><p>Trace the publicly committed sample, including its evidence and counter-evidence.</p></div><span className="section-status amber-status">DEMO FIXTURE / NOT VERIFIED HERE</span></div>
        <div className="receipt-grid">
          <article className="receipt-main"><div className="receipt-top"><span>OBSERVATION / {example.schema_version}</span><span>EXAMPLE DATA</span></div><h3>{example.claim}</h3>
            <div className="receipt-details"><div><span>RECEIPT ID</span><code>{example.receipt_id}</code></div><div><span>OBSERVER</span><strong>{example.observer_anchor.observer_role}</strong></div><div><span>EVIDENCE GRADE</span><strong>{example.evidence.grade} / 5 · Behavioral evidence</strong></div><div><span>MODEL CLASS</span><strong>{initial.classification_label}</strong></div></div>
            <div className="evidence-pair"><div><span>EVIDENCE SUMMARY</span><p>{example.evidence.summary}</p></div><div><span>COUNTER-EVIDENCE</span><p>{example.evidence.counter_evidence}</p></div></div>
            <p className="fixture-warning">This fixture is illustrative. Its receipt ID and computed values are copied from the repository. The browser displays the record but does not independently verify its canonical SHA-256 identity or external claims.</p>
          </article>
          <aside className="receipt-side"><p className="side-heading">AUDIT CHAIN</p><div className="audit-steps">{["Observation","Structured scores","Model computations","Receipt hash","Python verification"].map((step,i)=><div key={step}><b>{String(i+1).padStart(2,"0")}</b><span>{step}</span><small>{i===4?"CLI ONLY":"SAMPLE STAGE"}</small></div>)}</div>
            <a href={REPO+"/blob/main/examples/receipt_example.json"} target="_blank" rel="noopener noreferrer">View original sample JSON <Icon name="arrow" size={16}/></a>
          </aside>
        </div>
      </section>

      <section className="method-section" id="method"><div className="method-copy"><p className="section-kicker">04 / INTERPRETATION BOUNDARY</p><h2>Prove the structure.<br/><em>Not the myth.</em></h2><p>Deterministic scoring and receipt verification can assess <b>internal consistency under the DCL model</b>. They cannot demonstrate a literal demiurge, prison universe, simulation, or twelve-dimensional physics model.</p><p>The reference Python runtime handles validation, canonical hashes, deterministic snapshots, before/after comparisons, recapture-tax analysis and ranked intervention proposals. This website is a static, client-only exploratory interface.</p><a href={REPO+"#receipt-verification-workflow"} target="_blank" rel="noopener noreferrer">Explore the Python verification workflow <Icon name="arrow" size={16}/></a></div><div className="method-art" aria-hidden="true"><span className="method-symbol">Φ</span><span className="method-equation">STRUCTURE ≠ ONTOLOGY</span></div></section>
    </main>
    <footer><a href="#home" className="footer-brand">DCL <span>OBSERVATORY</span></a><p>Local-first · Model-defined scores · MIT open-source software</p><a href={REPO} target="_blank" rel="noopener noreferrer">GitHub source ↗</a></footer>
  </div>;
}
