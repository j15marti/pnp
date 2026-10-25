/* ARC-MARKER-PROBE-FUSION114: independent ordinary-CNF SAT/UNSAT
   two-level indexed-bit experiment. Node 18+, no dependencies and no seeds.
   This counts logical input-bit reads, NOT FLMV physical tape work or space.
   Usage: node 2026-10-25_0250_ARC_MARKER_PROBE_FUSION114_repro.js
*/
"use strict";
function bin(x,w){return x.toString(2).padStart(w,"0");}
function bitWidth(v,m){return Math.max(3,Math.ceil(Math.log2(Math.max(v,m)+1)));}
function encode(clauses,arity){
 const v=Math.max(...clauses.flatMap(c=>c.map(x=>Math.abs(x))));
 const m=clauses.length,w=bitWidth(v,m);
 const header=(arity===2?"0010":"0011")+"1".repeat(w)+"0"+bin(v,w)+bin(m,w);
 return {text:header+clauses.map(c=>c.map(x=>(x<0?"1":"0")+bin(Math.abs(x),w)).join("")).join(""),v,m,w,headerLen:header.length,arity,clauses};
}
function parent(q,odd){
 const clauses=[];
 for(let i=0;i<q;i++){const u=i+1,v=(i+1)%q+1,b=(odd&&i===0)?1:0;
  if(b){clauses.push([u,v]);clauses.push([-u,-v]);}
  else{clauses.push([-u,v]);clauses.push([u,-v]);}}
 return encode(clauses,2);
}
function childSpec(baseLength){
 const nPad=Math.max(2,Math.floor(Math.sqrt(baseLength)/Math.log2(baseLength+2)));
 const v=6+3*nPad,m=8+nPad,w=bitWidth(v,m);
 const header="0011"+"1".repeat(w)+"0"+bin(v,w)+bin(m,w);
 return {nPad,v,m,w,header,headerLen:header.length,length:header.length+3*(w+1)*m,marker:header.length+7*3*(w+1)};
}
function litAt(c,j,unsat){
 if(c<7){const sign=(c>>(2-j))&1;return sign?-(j+1):(j+1);}
 if(c===7)return unsat?-(j+1):(j+4);
 return 7+3*(c-8)+j;
}
function childBit(sp,pos,unsat){
 if(pos<0||pos>=sp.length)throw Error("out of range");
 if(pos<sp.headerLen)return sp.header[pos];
 let local=pos-sp.headerLen,clause=Math.floor(local/(3*(sp.w+1)));
 local%=3*(sp.w+1);
 const j=Math.floor(local/(sp.w+1)),k=local%(sp.w+1);
 const lit=litAt(clause,j,unsat);
 return k===0?(lit<0?"1":"0"):bin(Math.abs(lit),sp.w)[k-1];
}
function childClauses(sp,unsat){
 let clauses=[];
 for(let c=0;c<sp.m;c++)clauses.push([litAt(c,0,unsat),litAt(c,1,unsat),litAt(c,2,unsat)]);
 return clauses;
}
function dpll(clauses,assignment={}){
 const a={...assignment};
 while(true){
  let changed=false,pending=[];
  for(const c of clauses){
   let satisfied=false,unbound=[];
   for(const lit of c){const v=Math.abs(lit),val=a[v];
    if(val===undefined)unbound.push(lit);
    else if(val===(lit>0)){satisfied=true;break;}
   }
   if(satisfied)continue;
   if(!unbound.length)return false;
   if(unbound.length===1){
    const lit=unbound[0],v=Math.abs(lit),value=lit>0;
    if(a[v]!==undefined&&a[v]!==value)return false;
    if(a[v]===undefined){a[v]=value;changed=true;}
   }else pending.push(unbound);
  }
  if(changed)continue;
  if(!pending.length)return true;
  const v=Math.abs(pending[0][0]);
  return dpll(clauses,{...a,[v]:true})||dpll(clauses,{...a,[v]:false});
 }
}
function sat2(clauses,n){
 const g=Array.from({length:2*n},()=>[]),r=Array.from({length:2*n},()=>[]);
 function node(l){return 2*(Math.abs(l)-1)+(l<0?1:0);}
 for(const [a,b] of clauses){
  const na=node(-a),nb=node(-b),A=node(a),B=node(b);
  g[na].push(B);r[B].push(na);g[nb].push(A);r[A].push(nb);
 }
 const seen=new Uint8Array(2*n),order=[];
 function dfs(x){seen[x]=1;for(const v of g[x])if(!seen[v])dfs(v);order.push(x);}
 for(let i=0;i<2*n;i++)if(!seen[i])dfs(i);
 let comps=new Int32Array(2*n).fill(-1),cc=0;
 function rev(x){comps[x]=cc;for(const v of r[x])if(comps[v]===-1)rev(v);}
 for(let i=order.length-1;i>=0;i--){const v=order[i];if(comps[v]===-1){rev(v);cc++;}}
 for(let i=0;i<n;i++)if(comps[2*i]===comps[2*i+1])return false;
 return true;
}
function readSourceStatus(src,stats){
 /* Full literal source scan; inspect first literal of each pair.
    The cycle-grammar promise is separately checked by the fixture
    construction and SCC solver, not all ordinary input encodings. */
 let parity=0,observed=0;
 const stride=4*(src.w+1);
 for(let i=0;i<src.text.length;i++){
  const ch=src.text.charAt(i);stats.rootReads++;
  if(i>=src.headerLen && (i-src.headerLen)%stride===0){
   parity^=(ch==="0"?1:0);observed++;
  }
 }
 if(observed!==src.v)throw Error("source grammar mismatch");
 return parity===1;
}
function run(){
 let assertions=0,fullOldScans=0,fullMarkerScans=0,aggregateRootReads=0;
 function check(ok,msg){assertions++;if(!ok)throw Error("ASSERT "+msg);}
 const cases=[];
 for(const q of [3,4,5,6,8,12,24,48,96]){
  for(const odd of [false,true]){
   const src=parent(q,odd),first=childSpec(src.text.length),second=childSpec(first.length),bad=odd;
   const e1=encode(childClauses(first,bad),3),e2=encode(childClauses(second,bad),3);
   check(e1.text.length===first.length,"first length");
   check(e2.text.length===second.length,"second length");
   check(first.marker<first.length,"marker range");
   check(childBit(first,first.marker,false)==="0","SAT marker");
   check(childBit(first,first.marker,true)==="1","UNSAT marker");
   check(sat2(src.clauses,q)===!bad,"source SCC");
   check(dpll(e1.clauses)===!bad,"first DPLL");
   check(dpll(e2.clauses)===!bad,"second DPLL");
   const probe={rootReads:0};
   for(let i=0;i<second.length;i++){
    const p=readSourceStatus(src,probe);
    const firstMarker=childBit(first,first.marker,p);
    const x=childBit(second,i,firstMarker==="1");
    check(x===e2.text[i],"marker nested bit "+q+":"+odd+":"+i);
   }
   const markerReads=probe.rootReads;
   check(markerReads===src.text.length*second.length,"marker source reads");
   fullMarkerScans++;aggregateRootReads+=markerReads;
   const cheap={rootReads:0};
   const one=readSourceStatus(src,cheap);
   check(one===bad,"summary status");
   for(let i=0;i<second.length;i++)check(childBit(second,i,one)===e2.text[i],"summary bit");
   check(cheap.rootReads===src.text.length,"summary once");
   let oldExecuted=false,oldReads=0;
   if(q===3){
    const old={rootReads:0};
    for(let i=0;i<second.length;i++){
     let firstMarker="!";
     for(let j=0;j<first.length;j++){
      const p=readSourceStatus(src,old);
      const bit=childBit(first,j,p);
      if(j===first.marker)firstMarker=bit;
     }
     check(childBit(second,i,firstMarker==="1")===e2.text[i],"old scan bit");
    }
    oldExecuted=true;oldReads=old.rootReads;fullOldScans++;
    check(oldReads===src.text.length*first.length*second.length,"old scan exact");
   }
   cases.push({q,label:bad?"UNSAT":"SAT",N:src.text.length,L1:first.length,L2:second.length,
    actual_marker_root_reads:markerReads,predicted_old_full_scan_root_reads:src.text.length*first.length*second.length,
    actual_old_full_scan_root_reads:oldExecuted?oldReads:null,summary_root_reads:cheap.rootReads,
    peak_generator_index_bits_estimate:Math.ceil(Math.log2(src.text.length+1))+Math.ceil(Math.log2(first.length+1))+Math.ceil(Math.log2(second.length+1))});
  }
 }
 const hornSat=dpll([[1],[-1,2]]),hornUnsat=dpll([[1],[-1]]);
 check(hornSat&&(!hornUnsat),"horn control");
 return {id:"ARC-MARKER-PROBE-FUSION114",mode:"deterministic exhaustive per indexed child bit, SAT/SCC checks",seed:null,
  source_case_count:cases.length,actual_marker_full_scans:fullMarkerScans,actual_old_full_scans:fullOldScans,
  assertions,failed_assertions:0,total_actual_marker_source_reads:aggregateRootReads,
  cases,hostile_controls:["all source cycle 2SAT SCC","first and second ordinary child DPLL SAT and UNSAT","one-pass source parity direct recognizer","Horn SAT/UNSAT","cached summary","literal full virtual input scan"],
  caveats:["No physical FLMV TM trace","Only promised affine/2SAT cycle source; not all ordinary SAT","Source marker discloses SAT label","Bit-count proxy excludes physical index tape transition count","No unconditional SAT hardness"]};
}
if(typeof module!=="undefined" && require.main===module)console.log(JSON.stringify(run(),null,2));
