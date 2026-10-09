import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import { calculate, coordinateKey, scenarioDocument, C_STAR, FIELDS } from "../src/engine.js";

const fixture=JSON.parse(fs.readFileSync(new URL("../../examples/receipt_example.json",import.meta.url),"utf8"));

test("browser scoring matches Python example receipt numeric values",()=>{
  const actual=calculate(fixture.scores);
  for(const key of ["D_score","Phi_score","DCR","CMI"])
    assert.ok(Math.abs(actual[key]-fixture.computed[key])<1e-10,key);
  for(const key of ["classification","dominant_constraint","dominant_coherence","phi369_threshold_met"])
    assert.equal(actual[key],fixture.computed[key],key);
});
test("all 12 scoring fields are bounded and finite",()=>{
  assert.equal(FIELDS.length,12);
  assert.throws(()=>calculate({...fixture.scores,B:NaN}),/Invalid score/);
  assert.throws(()=>calculate({...fixture.scores,B:1.1}),/Invalid score/);
  assert.throws(()=>calculate({...fixture.scores,B:-1}),/Invalid score/);
});
test("threshold and classification boundaries reflect the documented model",()=>{
  const allZero=Object.fromEntries(FIELDS.map(f=>[f.key,0]));
  assert.equal(calculate(allZero).classification,"contested_field");
  const highPhi={...allZero,...Object.fromEntries(FIELDS.slice(6).map(f=>[f.key,1]))};
  assert.equal(calculate(highPhi).classification,"liberation_field");
  assert.ok(calculate(highPhi).phi369_threshold_met);
  assert.equal(C_STAR,1.618033988749895/2);
});
test("coordinate and exports are explicit, non-canonical scenario documents",()=>{
  assert.equal(coordinateKey(fixture.coordinate),"d06_f02_s06_a10");
  assert.throws(()=>coordinateKey({...fixture.coordinate,scale_id:13}),RangeError);
  const doc=scenarioDocument(fixture.scores,fixture.coordinate);
  assert.match(doc.document_type,/not_receipt/);
  assert.equal(doc.receipt_id,undefined);
});
