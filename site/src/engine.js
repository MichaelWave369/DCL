// Mirrors the public DCL Runtime v0.1 scoring formulas and classification mapping.
// This browser lab is NOT the Python receipt verifier and never issues canonical receipt IDs.
export const EPSILON = 0.000001;
export const K = 5;
export const PHI = 1.618033988749895;
export const C_STAR = PHI / 2;
export const FIELDS = [
  { key:"B", name:"Boundary pressure", hint:"Strength of limiting edges or imposed boundaries", group:"constraint" },
  { key:"R", name:"Recurrence pressure", hint:"Repetition or looping pressure", group:"constraint" },
  { key:"I_g", name:"Ignorance gradient", hint:"Lack of accessible knowledge", group:"constraint" },
  { key:"S", name:"Suffering stabilization", hint:"Persistence of harmful patterns", group:"constraint" },
  { key:"E_x", name:"Extraction pressure", hint:"Resources or attention being drawn away", group:"constraint" },
  { key:"D_c", name:"Decay / entropy constraint", hint:"Constraint driven by loss or deterioration", group:"constraint" },
  { key:"C_o", name:"Coherence", hint:"Internal consistency and integration", group:"coherence" },
  { key:"K", name:"Knowledge / clarity", hint:"Understanding and discernment", group:"coherence" },
  { key:"A", name:"Authentic agency", hint:"Ability to choose and act", group:"coherence" },
  { key:"M", name:"Meaning", hint:"Sense of purpose or significance", group:"coherence" },
  { key:"L_v", name:"Life-value / aliveness", hint:"Experienced vitality and value", group:"coherence" },
  { key:"R_s", name:"Sovereign resistance", hint:"Ability to resist unwanted pressures", group:"coherence" },
];
export const CONSTRAINT = FIELDS.filter(f=>f.group==="constraint");
export const COHERENCE = FIELDS.filter(f=>f.group==="coherence");
export const DIMENSIONS = [
 "Point / Seed", "Plane / Surface", "Volume / Body", "Time / Sequence",
 "Probability / Choice", "Polarity / Relation", "Memory / Lineage", "Mind / Symbol",
 "Network / Society", "Planetary / Biospheric", "Cosmic / Law-Set", "Coherence / Integration"
];
export const SCALES = [
 "Subtle / Signal","Physical","Biological","Emotional","Cognitive","Individual",
 "Relational","Social","Institutional","Planetary","Cosmic","Meta-Cosmic"
];
export const ARCHETYPES = [
 "Void Field","Boundary Field","Recurrence Field","Extraction Field",
 "Prison Field","Simulation Field","School Field","Forge Field",
 "Garden Field","Contested Field","Liberation Field","Sovereign Field"
];
export const CLASSIFICATIONS = [
 {max:.2,key:"liberation_field",label:"Liberation field"},
 {max:.4,key:"garden_growth_field",label:"Garden / growth field"},
 {max:.6,key:"contested_field",label:"Contested field"},
 {max:.8,key:"prison_extraction_field",label:"Prison / extraction field"},
 {max:Infinity,key:"high_matrix_capture",label:"High matrix capture"},
];
export function coordinateKey(coord) {
  const parts=[coord.dimension_id,coord.field_variable_id,coord.scale_id,coord.archetype_id];
  if(parts.some(n=>!Number.isInteger(n)||n<1||n>12))throw new RangeError("Coordinate components must be integers 1–12.");
  return ["d","f","s","a"].map((prefix,i)=>prefix+String(parts[i]).padStart(2,"0")).join("_");
}
export function calculate(scores) {
  for(const field of FIELDS) {
    const v=scores[field.key];
    if(typeof v!=="number"||!Number.isFinite(v)||v<0||v>1)throw new RangeError("Invalid score: "+field.key);
  }
  const average=fields=>fields.reduce((total,f)=>total+scores[f.key],0)/6;
  const D_score=average(CONSTRAINT);
  const Phi_score=average(COHERENCE);
  const DCR=D_score/(Phi_score+EPSILON);
  const CMI=1/(1+Math.exp(-K*(D_score-Phi_score)));
  const classification=CLASSIFICATIONS.find(item=>CMI<=item.max);
  const dominant=fields=>fields.map(f=>f.key).sort((a,b)=>scores[b]-scores[a]||a.localeCompare(b,"en"))[0];
  // ASCII lexical tie ordering matches Python sorted; localeCompare differs for underscores only
  // among distinct variable keys, which have no numerical ties in the bundled fixture.
  const lexical=fields=>fields.map(f=>f.key).sort((a,b)=>scores[b]-scores[a]||(a<b?-1:a>b?1:0))[0];
  return {
    D_score,Phi_score,DCR,CMI,
    classification:classification.key,
    classification_label:classification.label,
    phi369_threshold_met:Phi_score>=C_STAR&&DCR<1,
    dominant_constraint:lexical(CONSTRAINT),
    dominant_coherence:lexical(COHERENCE),
  };
}
export function scenarioDocument(scores, coordinate) {
  const computed=calculate(scores);
  return {
    document_type:"dcl_observatory_exploration_not_receipt",
    notice:"Illustrative local model exploration. This is NOT a canonical receipt, scientific verification, or an experimental measurement.",
    coordinate_key:coordinateKey(coordinate),
    coordinate:{...coordinate},
    scores:{...scores},
    computed,
    formula_version:"dcl-runtime-v0.1",
  };
}
