#!/usr/bin/env node
// LSPV-2/410 independent public-DEF facet Resolution certificate checker.
// node lspv2_410_independent_checker.mjs path/to/raw.json[.gz.b64]
import fs from 'node:fs';
import zlib from 'node:zlib';
let checks=0;function ok(c,msg){checks++;if(!c)throw Error(msg);}
function norm(c){let v=[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||b-a);return v.some(x=>v.includes(-x))?null:v;}
const key=x=>JSON.stringify(x),gate=(op,a,b)=>(op>>(2*a+b))&1;
function evals(gs,base){const v={1:base[0],2:base[1],3:base[2]};for(const [out,a,b,f] of gs){ok(Object.hasOwn(v,a)&&Object.hasOwn(v,b),'gate topological');ok(!Object.hasOwn(v,out),'gate fresh');v[out]=gate(f,v[a],v[b]);}return v;}
function facets(gs){let res=[];for(let [out,a,b,f] of gs)for(let u=0;u<2;u++)for(let v=0;v<2;v++){let y=1-gate(f,u,v),c=norm([u?-a:a,v?-b:b,y?-out:out]);if(c&&!res.some(t=>key(t)===key(c)))res.push(c);}return res;}
function models(cs,v){return cs.every(c=>c.some(x=>v[Math.abs(x)]===(x>0?1:0)));}
function verify(rec){
  ok(rec.scope.includes('NOT certified native'),'correct restricted scope');
  const oldF=facets(rec.old_gates),newF=facets(rec.new_gates);
  ok(key(oldF)===key(rec.old_facets),'old facets');
  ok(key(newF)===key(rec.new_facets),'new facets');
  for(let a=0;a<8;a++){
    let bits=[a>>2&1,a>>1&1,a&1],old=evals(rec.old_gates,bits),neu=evals(rec.new_gates,bits);
    for(let w of [4,5,6])ok(old[w]===neu[w],'public vector');
    ok(models(oldF,old)&&models(newF,neu),'defining relation');
  }
  let behavior=[],costB=0,costF=0;
  for(const [pi,p] of rec.proofs.entries()){
    ok(p.stage===(pi<24?'behavior':'facet'),'stage');
    const target=norm(p.target);ok(target!==null&&key(target)===key(p.target),'target syntax');
    let ax=p.axioms;ok(ax.every(x=>norm(x)!==null&&key(norm(x))===key(x)),'premise syntax');
    if(pi<24){
      let reach=new Set(),ng=Object.fromEntries(rec.new_gates.map(x=>[x[0],x]));
      const walk=z=>{if(z<=3)return;if(!reach.has(z)){let h=ng[z];ok(!!h,'missing new gate');walk(h[1]);walk(h[2]);reach.add(z);}};
      walk(p.gate);let expected=facets(rec.new_gates.filter(x=>reach.has(x[0])));
      ok(key(ax)===key(expected),'wrong behavior premises');
      ok(p.target.length===4&&p.target.some(x=>Math.abs(x)===p.gate),'behavior target');
      for(let a=0;a<8;a++){
        let bits=[a>>2&1,a>>1&1,a&1],v=evals(rec.new_gates,bits);
        ok(models(ax,v),'cone model');ok(p.target.some(x=>v[Math.abs(x)]===(x>0?1:0)),'behavior not valid');
      }
    }else{
      let expected=behavior.filter(x=>p.target.some(y=>Math.abs(y)===x.g)).map(x=>x.c);
      let uniq=[...new Map(expected.map(x=>[key(x),x])).values()];
      ok(key(ax)===key(uniq),'premise not previously derived behavior');
      ok(oldF.some(x=>key(x)===key(p.target)),'facet not old');
      for(let a=0;a<8;a++){
        let bits=[a>>2&1,a>>1&1,a&1],v=evals(rec.old_gates,bits);
        ok(models(ax,v),'behavior does not imply old output');
        ok(p.target.some(x=>v[Math.abs(x)]===(x>0?1:0)),'old facet invalid');
      }
    }
    let nodes=[];const ref=p=>{ok(Array.isArray(p)&&p.length===2,'ref shape');let [tag,i]=p;ok(Number.isInteger(i),'ref index');if(tag==='axiom'){ok(i>=0&&i<ax.length,'axiom bounds');return ax[i];}ok(tag==='res'&&i>=0&&i<nodes.length,'res bounds');return nodes[i];};
    for(let n of p.nodes){
      let a=ref(n.left),b=ref(n.right),piv=n.pivot;
      ok(a.includes(piv)&&b.includes(-piv),'bad pivot');
      let r=norm([...a.filter(x=>x!==piv),...b.filter(x=>x!==-piv)]);
      ok(r!==null&&key(r)===key(n.clause),'bad resolvent');nodes.push(r);
    }
    ok(p.root.every(x=>target.includes(x)),'root not subclause');
    ok([...ax,...nodes].some(x=>key(x)===key(p.root)),'root not derived');
    let vars=new Set(ax.flat().map(Math.abs)),tv=new Set(target.map(Math.abs));
    let deficit=[...vars].filter(x=>!tv.has(x)).length;
    ok(deficit<=3&&p.nodes.length<=2**deficit-1,'cost bound');
    if(pi<24){behavior.push({g:p.gate,c:p.root});costB+=p.nodes.length;}
    else costF+=p.nodes.length;
  }
  let c=rec.counts;
  ok(costB===c.behavior_res&&costF===c.facet_res,'stage cost');
  ok(costB+costF===c.total_res,'total inference cost');
  ok(c.new_defs+c.total_res===c.q_new&&c.q_new===44,'paid cost');
  ok(models([[1],[1,2]],{1:1,2:0,3:0}),'SAT control');
  ok(!models([[1],[-1]],{1:1,2:0,3:0}),'UNSAT control 1');
  ok(!models([[1],[-1]],{1:0,2:0,3:0}),'UNSAT control 2');
}
const path=process.argv[2];if(!path)throw Error('Supply raw.json or raw.json.gz.b64');
let input=fs.readFileSync(path);
const raw=JSON.parse(path.endsWith('.b64')?zlib.gunzipSync(Buffer.from(input.toString().trim(),'base64')).toString():input.toString());
verify(raw);
function reject(b,what){let threw=false;try{verify(b);}catch{threw=true;}ok(threw,'failed to reject '+what);}
const clone=()=>structuredClone(raw);
let b=clone();b.proofs.find(x=>x.nodes.length).nodes[0].pivot=999;reject(b,'pivot');
b=clone();b.new_gates[3][3]=6;reject(b,'gate');
b=clone();b.proofs[2].target=[1,1,2,3,-4];reject(b,'literal');
b=clone();b.proofs[24].axioms[0]=[99];reject(b,'invented axiom');
b=clone();b.proofs[0].root=[100];reject(b,'invented result');
console.log(JSON.stringify({status:'PASS',checks,proofs:raw.proofs.length,resolution:raw.counts.total_res,paid:raw.counts.q_new,mutants_rejected:5}));
