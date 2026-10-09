import test from "node:test";
import assert from "node:assert/strict";
import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { createServer } from "vite";

test("actual DCL React app renders on server, not just compiles",async()=>{
  const vite=await createServer({server:{middlewareMode:true},appType:"custom",logLevel:"error"});
  try{
    const {default:App}=await vite.ssrLoadModule("/src/App.jsx");
    const html=renderToStaticMarkup(React.createElement(App));
    assert.match(html,/OBSERVATORY/);
    assert.match(html,/Constraint/i);
    assert.match(html,/Coherence/i);
    assert.match(html,/Observation receipt/i);
    assert.match(html,/cannot demonstrate/i);
  }finally{await vite.close()}
});
