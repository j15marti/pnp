'use strict';
// ARC-STREAM-DICT132: finite semantic and operation-count reference.
// This JavaScript is NOT an FLMV indexed-tape timing/space emulator.
function audit() {
  const W = '-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14';
  const W1 = W.split(';').map(s=>s.trim().split(/\s+/).map(Number));
  const G = [[1,2,3],[1,-2,-3],[-1,2,-3],[-1,-2,3]];
  let assertions = 0;
  function check(p, message) { assertions++; if (!p) throw Error(message || 'assertion '+assertions); }
  function encode(clauses, n) {
    let src = 'p cnf '+n+' '+clauses.length+'\n', offsets=[];
    for(const c of clauses) { offsets.push(src.length);src += c.join(' ')+' 0\n'; }
    return {src, offsets, clauses, n};
  }
  function sourceAt(src, p) {
    if(!Number.isInteger(p) || p<=0 || p>=src.length || src[p-1]!=='\n') return null;
    const e=src.indexOf('\n',p); if(e<0) return null;
    const row=src.slice(p,e).trim().split(/\s+/).map(Number);
    if(row.length!==4 || row[3]!==0 || !row.slice(0,3).every(Number.isInteger))return null;
    if(new Set(row.slice(0,3).map(Math.abs)).size!==3)return null;
    return row.slice(0,3);
  }
  function residue(c, assignment) {
    let r=[];
    for(const lit of c){const v=assignment.get(Math.abs(lit));if(v!==undefined) {if(v===(lit>0))return null;} else r.push(lit);}
    return r;
  }
  function edges(r) {
    if(r===null) return [];
    if(r.length===1)return [[-r[0],r[0]]];
    if(r.length===2)return [[-r[0],r[1]],[-r[1],r[0]]];
    return [];
  }
  // A fully deterministic AVL dictionary supporting insertion, update,
  // search and erasure; key comparison and rotations are instrumented.
  class AVL {
    constructor() {this.root=null;this.size=0;this.compares=0;this.rotations=0;this.maxHeight=0;}
    ht(x){return x?x.h:0;}
    update(x){x.h=1+Math.max(this.ht(x.l),this.ht(x.r));return x;}
    right(a){let b=a.l;a.l=b.r;b.r=this.update(a);this.rotations++;return this.update(b);}
    left(a){let b=a.r;a.r=b.l;b.l=this.update(a);this.rotations++;return this.update(b);}
    balance(x){if(!x)return null;this.update(x);let d=this.ht(x.l)-this.ht(x.r);
      if(d>1){if(this.ht(x.l.l)<this.ht(x.l.r))x.l=this.left(x.l);return this.right(x);}
      if(d< -1){if(this.ht(x.r.r)<this.ht(x.r.l))x.r=this.right(x.r);return this.left(x);}
      return x;
    }
    get(key){let x=this.root;while(x){this.compares++;if(key===x.k)return x.v;x=key<x.k?x.l:x.r;}return undefined;}
    put(key,value){let added=false;const f=x=>{if(!x){added=true;return {k:key,v:value,h:1,l:null,r:null};}
      this.compares++;if(key===x.k){x.v=value;return x;}
      if(key<x.k)x.l=f(x.l);else x.r=f(x.r);return this.balance(x);
    };this.root=f(this.root);if(added)this.size++;this.maxHeight=Math.max(this.maxHeight,this.ht(this.root));return added;}
    del(key){let found=false;const min=x=>{while(x.l)x=x.l;return x;};
      const remove=(x,k)=>{if(!x)return null;this.compares++;
        if(k<x.k)x.l=remove(x.l,k);else if(k>x.k)x.r=remove(x.r,k);
        else{found=true;if(!x.l)return x.r;if(!x.r)return x.l;
          const y=min(x.r);x.k=y.k;x.v=y.v;x.r=dropMin(x.r);}
        return this.balance(x);
      };
      const dropMin=x=>{if(!x.l)return x.r;x.l=dropMin(x.l);return this.balance(x);};
      this.root=remove(this.root,key);if(found)this.size--;return found;
    }
    verify(){const visit=x=>{if(!x)return {h:0,count:0,min:Infinity,max:-Infinity};
        const l=visit(x.l),r=visit(x.r);check(l.max<x.k && x.k<r.min,'AVL ordering');
        check(x.h===Math.max(l.h,r.h)+1 && Math.abs(l.h-r.h)<=1,'AVL balance');
        return {h:x.h,count:l.count+r.count+1,min:Math.min(l.min,x.k),max:Math.max(r.max,x.k)};};
      const out=visit(this.root);check(out.count===this.size,'AVL size');return out.h;
    }
  }
  function pathFrom(g,from,to){let Q=[from],prev=new Map([[from,null]]);for(let i=0;i<Q.length;i++){
      let u=Q[i];for(const [v,p] of (g.get(u)||[]))if(!prev.has(v)){prev.set(v,[u,p]);Q.push(v);}
    }if(!prev.has(to))return null;let ans=[];for(let v=to;prev.get(v)!==null;){let [u,p]=prev.get(v);ans.push([p,u,v]);v=u;}return ans.reverse();}
  function leafFor(f,as){let g=new Map();for(let i=0;i<f.clauses.length;i++){
      const r=residue(f.clauses[i],as),p=f.offsets[i];if(r!==null&&r.length===0)return {type:'empty',p};
      for(const [u,v] of edges(r)){if(!g.has(u))g.set(u,[]);g.get(u).push([v,p]);}
    }for(let x=1;x<=15;x++)if(as.get(x)===undefined){let plus=pathFrom(g,x,-x),minus=pathFrom(g,-x,x);
      if(plus&&minus)return {type:'paths',x,plus,minus};}
    return null;}
  function baseline(f,vars,i,as){let leaf=leafFor(f,as);if(leaf)return {type:'leaf',w:leaf};
    if(i===vars.length)return null;let v=vars[i];as.set(v,false);let a=baseline(f,vars,i+1,as);
    as.set(v,true);let b=baseline(f,vars,i+1,as);as.delete(v);
    return {type:'branch',v,a,b};}
  function cloneLeaf(t){return JSON.parse(JSON.stringify(t));}
  function skew(leaf,vars,i){if(i===vars.length)return cloneLeaf(leaf);
    return {type:'branch',v:vars[i],a:cloneLeaf(leaf),b:skew(leaf,vars,i+1)};}
  function appendSkew(t,vars){if(t.type==='leaf')return skew(t,vars,0);
    return {type:'branch',v:t.v,a:appendSkew(t.a,vars),b:appendSkew(t.b,vars)};}
  function treeStats(t){if(t.type==='leaf')return {B:0,L:1,E:t.w.type==='paths'?t.w.plus.length+t.w.minus.length:0,h:0};
    const a=treeStats(t.a),b=treeStats(t.b);
    return {B:a.B+b.B+1,L:a.L+b.L,E:a.E+b.E,h:1+Math.max(a.h,b.h)};}
  function validate(f,t,mode){let A=new AVL(),stack=[],naiveChecks=0,records=0,sourceReads=0,peakDepth=0;
    function value(x){if(mode==='naive'){for(let i=stack.length-1;i>=0;i--){naiveChecks++;if(stack[i].v===x)return stack[i].val;}return undefined;}
      return A.get(x);}
    function validSource(p){sourceReads++;return sourceAt(f.src,p);}
    function checkLeaf(w){records++;if(w.type==='empty'){
        let c=validSource(w.p);return !!c&&residue(c,{get:value})?.length===0;}
      if(w.type!=='paths'||!Number.isInteger(w.x)||w.x<1||w.x>f.n||value(w.x)!==undefined)return false;
      for(const [route,start,end] of [[w.plus,w.x,-w.x],[w.minus,-w.x,w.x]]){
        if(route.length>2*f.n-1)return false;let cur=start;
        for(const [p,u,v] of route){records++;let c=validSource(p);
          if(!c||cur!==u||value(Math.abs(u))!==undefined||value(Math.abs(v))!==undefined)return false;
          const r=residue(c,{get:value});if(!edges(r).some(([a,b])=>a===u&&b===v))return false;
          cur=v;
        }if(cur!==end)return false;
      }return true;}
    function run(node){if(!node)return false;if(node.type==='leaf')return checkLeaf(node.w);
      if(node.type!=='branch'||!Number.isInteger(node.v)||node.v<1||node.v>f.n||value(node.v)!==undefined)return false;
      records++;A.put(node.v,false);stack.push({v:node.v,val:false});peakDepth=Math.max(peakDepth,stack.length);
      const left=run(node.a);A.put(node.v,true);stack[stack.length-1].val=true;
      const right=left&&run(node.b);stack.pop();A.del(node.v);
      return left&&right;}
    let valid=run(t);let height=A.verify();check(height===0&&A.size===0,'AVL rollback');
    return {valid,records,sourceReads,comparisons:A.compares,naiveChecks,rotations:A.rotations,maxAVLHeight:A.maxHeight,peakDepth};}
  const base=encode(W1,15);const baseProof=baseline(base,[2,4,7,14,15],0,new Map());
  check(!!baseProof && validate(base,baseProof,'tree').valid,'base W1 proof');
  const sizes=[0,1,2,4,8,12];let cases=[];
  for(const k of sizes){let clauses=W1.slice(),vars=[];
    for(let j=0;j<k;j++){let shift=15+3*j;clauses.push(...G.map(c=>c.map(x=>Math.sign(x)*(Math.abs(x)+shift))));vars.push(shift+1);}
    const f=encode(clauses,15+3*k),cert=appendSkew(baseProof,vars),stats=treeStats(cert);
    let balanced=validate(f,cert,'tree'),naive=validate(f,cert,'naive');
    check(balanced.valid&&naive.valid,'both validate W1 plus G');
    check(balanced.records===naive.records && balanced.peakDepth===stats.h,'records and depth');
    check(balanced.sourceReads===naive.sourceReads,'source records');
    check(balanced.maxAVLHeight<=2*Math.ceil(Math.log2(stats.h+2)),'AVL height');
    cases.push({G_copies:k,N:f.src.length,stats,...balanced,naiveAncestorChecks:naive.naiveChecks});
    let tampered=JSON.parse(JSON.stringify(cert));
    function mutate(t){if(t.type==='leaf' && t.w.type==='paths' && t.w.plus.length){t.w.plus[0][0]+=1;return true;}
      if(t.type==='branch')return mutate(t.a)||mutate(t.b);return false;}
    check(mutate(tampered),'found source-attested path');
    check(!validate(f,tampered,'tree').valid,'forged offset rejected');
    let duplicate=JSON.parse(JSON.stringify(cert));
    duplicate={type:'branch',v:2,a:duplicate,b:duplicate};
    check(!validate(f,duplicate,'tree').valid,'repeated branch rejected');
  }
  const sat=encode(G,3);check(leafFor(sat,new Map())===null,'SAT gadget has no contradictory leaf');
  const f=encode(W1,15);let malformed=JSON.parse(JSON.stringify(baseProof));
  malformed.a={type:'leaf',w:{type:'empty',p:1}};
  check(!validate(f,malformed,'tree').valid,'header spoof rejected');
  const comparisons=cases.map(c=>({k:c.G_copies,naive:c.naiveAncestorChecks,avl:c.comparisons,ratio:c.naiveAncestorChecks/Math.max(1,c.comparisons)}));
  return {run:'ARC-STREAM-DICT132',model:'semantic AVL reference, NOT physical indexed Turing time',seed:null,assertions,cases,comparisons,
    status:{balanced_lookup:'PROVED/EXACT abstract RAM data-structure conditional on canonical grammar',coNTIME:'CONDITIONAL all-UNSAT capped coverage',ARC:'OPEN',P_versus_NP:'OPEN'}};
}
if(typeof module!=='undefined' && require.main===module)console.log(JSON.stringify(audit(),null,2));