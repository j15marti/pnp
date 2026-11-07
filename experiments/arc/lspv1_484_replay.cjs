'use strict';
// Replay the exact previously published standalone finite syntactic Res(XOR) checker.
const {run}=require('./lspv1_484_affine_bool_syntactic.cjs');
const result=run();
if(result.status!=='PASS')process.exitCode=1;
console.log(JSON.stringify(result,null,2));
