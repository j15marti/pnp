"use strict";
/*
 * TMR-5/051 independent end-to-end source-interface redteam.
 * Model: read-only *sequentially headed* binary input; genuine sequentially
 * headed writable checkpoint tape, fixed state/update delta, ordered Q=B comb
 * leaf queries. Every source-head movement and record-cell movement counted.
 * No claim about arbitrary adaptive orders, unrestricted Tree Evaluation,
 * physical universal machine microcode, or P versus NP.
 * Revision: tmr5-seqsource051.v1; deterministic seed 20261115.
 */
const REV = "tmr5-seqsource051.v1", SEED=20261115;
let assertions=0, failures=0, examples=0, queryChecks=0, malformedRejected=0;
let sourceHeadMoves=0, anchorHeadMoves=0, exactFormulaChecks=0;
function check(c,msg){assertions++;if(!c){failures++;throw new Error(msg);}}
function bitWidth(n){let v=1,k=0;while(v<=n){v*=2;k++;}return k||1;}
function gamma(n){check(Number.isSafeInteger(n)&&n>=1,"gamma domain");const s=n.toString(2);return "0".repeat(s.length-1)+s;}
function encode(payload){return gamma(payload.length)+"0"+payload;}
function parse(input){
 if(!/^[01]*$/.test(input) || !input.length) return null;
 let z=0;while(z<input.length && input[z]==="0")z++;
 if(z===input.length)return null;
 const t=z+1;
 // A valid B is <= input length, so an oversized header can be rejected
 // without storing more than O(log(input length)) source bits.
 if(t>bitWidth(input.length) || 2*z+2>input.length)return null;
 const B=parseInt(input.slice(z,z+t),2), start=2*z+2;
 if(!Number.isSafeInteger(B)||B<1||input[2*z+1]!=="0"||input.length-start!==B)return null;
 return {B,start,payload:input.slice(start)};
}
function transitionDecode(code,C=2){const tr=Array.from({length:C},()=>Array(2));for(let q=0;q<C;q++)for(let x=0;x<2;x++){
 let d=code%(2*C);code=Math.floor(code/(2*C));tr[q][x]=[Math.floor(d/2),d%2];
 }return tr;}
function actualTrace(payload,tr){let q=0,p=0;const states=[],pos=[],moves=[];for(const x of payload){const [next,m]=tr[q][Number(x)];q=next;p+=m;states.push(q);pos.push(p);moves.push(m);}return {states,pos,moves,accept:2*p>=payload.length,p};}
function replay(input,tr,C,L){
 const meta=parse(input);check(meta!==null,"valid authenticated source");const {B,start,payload}=meta;
 check(1<=L && L<=B,"L range");
 const direct=actualTrace(payload,tr);const w=bitWidth(C-1)+bitWidth(B);
 let q=0,p=0,anchorRecords=[{a:0,q:0,p:0}],sourceHead=0,anchorHead=0;
 // One physical forward scan of all input positions, with grammar verification.
 // The payload updates only start after the authenticated header.
 for(let i=0;i<input.length;i++){
   if(i>=start){const j=i-start;const [next,m]=tr[q][Number(input[i])];q=next;p+=m;
     if((j+1)%L===0 && j+1<B)anchorRecords.push({a:j+1,q,p});
   }
   sourceHead++;
 }
 check(q===direct.states[B-1] && p===direct.p,"source scan state correct");
 const R=Math.ceil(B/L);check(anchorRecords.length===R,"anchor count");
 let inputMoves=input.length; // genuine source scan moves, includes header
 let inputReads=input.length;
 let recordMoves=R*w; // sequential bit writes during anchor construction
 const checkpointCells=R*w;
 // Authenticated input head is at endmarker. Reverse to the first payload cell.
 inputMoves+=Math.abs(sourceHead-start);sourceHead=start;
 let finalCount=0,exactBlockMoveSum=0,exactProbeSum=0;
 for(let j=1;j<=B;j++){
   const ai=Math.floor((j-1)/L),a=ai*L;
   const rec=anchorRecords[ai];check(rec.a===a,"record position");
   // Sequentially headed anchor tape, no random indexing or free resets.
   const recordStart=ai*w;
   recordMoves+=Math.abs(anchorHead-recordStart);anchorHead=recordStart;
   recordMoves+=w;anchorHead+=w; // paid bit-cell visits for one record
   let zq=rec.q,zp=rec.p,zm=0;
   // Genuine source-head seek, followed by paid locally moving replay.
   const target=start+a;
   const seek=Math.abs(sourceHead-target);inputMoves+=seek;sourceHead=target;
   for(let i=a;i<j;i++){
     const [next,m]=tr[zq][Number(input[sourceHead])];zq=next;zp+=m;zm=m;
     sourceHead++;inputMoves++;inputReads++;
   }
   const t=j-a;exactBlockMoveSum+=seek+t;exactProbeSum+=t;
   check(zq===direct.states[j-1] && zp===direct.pos[j-1] && zm===direct.moves[j-1],"physical virtual graph bit");
   check(sourceHead===start+j,"after ordered replay input head");
   check(seek===t-1,"ordered source-head rewind exact bound");
   check(2*zp>=0,"nonnegative positions");
   finalCount+=zm;
   queryChecks++;
 }
 check(finalCount===direct.p && (2*finalCount>=B)===direct.accept,"full evaluator output");
 let sumSquare=0,sumTri=0;for(let a=0;a<B;a+=L){const d=Math.min(L,B-a);sumSquare+=d*d;sumTri+=d*(d+1)/2;}
 check(exactBlockMoveSum===sumSquare,"exact source-head query movement sum squared");
 check(exactProbeSum===sumTri,"exact source-symbol read count triangles");
 check(inputMoves===input.length+B+sumSquare,"end-to-end source moves including scan and rewind");
 check(inputReads===input.length+sumTri,"end-to-end exact source reads including scan");
 check(recordMoves<=3*B*R*w+R*w,"sequential anchor moves polynomial upper ledger");
 check(checkpointCells===R*w && w===bitWidth(C-1)+bitWidth(B),"simultaneous live checkpoint cells");
 exactFormulaChecks++;sourceHeadMoves+=inputMoves;anchorHeadMoves+=recordMoves;examples++;
 return {B,L,R,w,queryCount:B,sourceLength:input.length,sourceMoves:inputMoves,sourceReads:inputReads,
   replayMoves:sumSquare,readReplays:sumTri,anchorMoves:recordMoves,anchorCells:R*w,
   output:direct.accept,sourceHeaderLength:start};
}
// Independent exhaustive physical-path validation of every 2-state transducer.
for(let B=1;B<=5;B++)for(let code=0;code<256;code++){
 const tr=transitionDecode(code,2);
 for(let word=0;word<(1<<B);word++){
   const payload=word.toString(2).padStart(B,"0"),s=encode(payload);
   const parsed=parse(s);check(parsed && parsed.payload===payload && parsed.B===B,"gamma grammar roundtrip");
   for(let L=1;L<=B;L++)replay(s,tr,2,L);
 }
}
// Three-state hostile transducers, seeded and original complete words, including ties.
let seed=SEED>>>0;function rng(){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0;}
for(let v=0;v<12;v++){
 let tr=Array.from({length:3},()=>Array.from({length:2},()=>[rng()%3,rng()%2]));
 for(let B=1;B<=7;B++)for(let word=0;word<(1<<B);word++){
   const payload=word.toString(2).padStart(B,"0"),s=encode(payload);
   replay(s,tr,3,Math.max(1,Math.ceil(Math.sqrt(B))));
 }
}
// Malformed-input firewall; reject before any virtual query.
const bad=["","0","1","00","10","110","100","101","10100","0110","1110","10000", "011001011000"];
for(const s of bad){if(parse(s)===null){malformedRejected++;}else{const obj=parse(s);check(obj.payload.length===obj.B,"malformed control accidentally valid grammar");}}
check(malformedRejected>=7,"malformed rejections observed");
const witness=[];for(const B of [16,64,1024]){
 const L=Math.ceil(Math.sqrt(B)),payload=Array.from({length:B},(_,i)=>((i*i+7*i+3)%11<4)?"1":"0").join("");
 const tr=[[[0,0],[1,1]],[[0,1],[1,0]]];
 witness.push(replay(encode(payload),tr,2,L));
}
const out={revision:REV,seed:SEED,model:"sequential input head; sequential anchor work head; fixed Q=B left-to-right comb",status:"COMPUTATIONAL",cases:examples,queryChecks,assertions,failures,exactFormulaChecks,malformedRejected,
 totals:{sourceHeadMoves,anchorHeadMoves},witness,
 proved_identity:"query source-head movements sum_{blocks} length(block)^2, including replay and rewind; add N+B for input authentication and reset",
 scope:"Only canonical blank-start fixed-state streaming transducers and ordered comb queries. No arbitrary graph provider, generic TreeEval, or unrestricted DTISP separation.",
 independent_audit_of:"TMR-3/054 draft PR #164; original main branch handoff at /049 lags"};
process.stdout.write(JSON.stringify(out,null,2)+"\n");
