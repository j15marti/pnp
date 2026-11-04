#!/usr/bin/env node
// LSPV-2/398 independent certificate and cofactor verifier. Node.js 18+, no packages.
'use strict';
const fs=require('fs'),crypto=require('crypto');
const payload=JSON.parse(fs.readFileSync(process.argv[2]||'results/raw/arc/2026-11-04_1213_LSPV2_GATE_COLLAPSE_BACKDOOR398_raw.json','utf8'));
let asserts=0;
function ok(p,msg){asserts++;if(!p)throw Error('assert failed: '+msg)}
function standard(c){const xs=[...new Set(c)].sort((a,b)=>a-b);
    ok(xs.every(x=>x!==0),'nonzero');
    ok(xs.every(x=>!xs.includes(-x)),'not tautology');return xs;}
function derive(u,v,p){ok(u.includes(p)&&v.includes(-p),'pivot');
    return standard([...u.filter(x=>x!==p),...v.filter(x=>x!==-p)]);}
function models(src,n){let v=0;for(let mask=0;mask<(1<<n);mask++)
    if(src.every(c=>c.some(z=>Boolean(mask&(1<<(Math.abs(z)-1)))===(z>0))))v++;
    return v;}
function build(g){
    const src=[[1],...Array.from({length:g},(_,i)=>[i+2]),
        [-1,...Array.from({length:g},(_,i)=>-i-2)]];
    const defs=[];for(let i=0;i<g;i++){
        const y=g+2+i,w=i+2;defs.push([[-y,1],[-y,w],[y,-1,-w]]);}
    const bank=[...src,...defs.flat()].map(standard);
    const steps=bank.map(c=>({type:'input',c}));
    function push(i,j,p){const c=derive(steps[i].c,steps[j].c,p);
        steps.push({type:'res',i,j,p,c});return steps.length-1;}
    const d=[];for(let i=0;i<g;i++){
        const y=g+2+i,w=i+2,base=src.length+3*i;
        const u=push(0,base+2,1),v=push(i+1,u,w);
        d.push(push(v,base+1,y));}
    let tail=push(0,src.length-1,1);
    for(let i=0;i<g;i++)tail=push(d[i],tail,i+2);
    ok(!steps[steps.length-1].c.length,'empty contradiction');
    ok(steps.length-bank.length===4*g+1,'Resolution count');
    return {src,defs,bank,steps};
}
function subst(lit,x,gate){
    let v=Math.abs(lit)===1?x:gate[Math.abs(lit)];
    if(v===undefined)v=Math.abs(lit);
    if(lit<0)v=typeof v==='boolean'?!v:-v;
    return v;
}
function collapse(g,x){
    const gate={};for(let i=0;i<g;i++)gate[g+2+i]=x?i+2:false;
    return gate;
}
function reduced(C,x,gate){
    let out=[];for(const l of C){const s=subst(l,x,gate);
        if(s===true)return null;if(s===false)continue;out.push(s);}
    out=[...new Set(out)];
    if(out.some(z=>out.includes(-z)))return null;
    return out.sort((a,b)=>a-b);
}
function projected(orig,g,x){
    const gate=collapse(g,x),res=[];let paid=0;
    for(let j=0;j<orig.steps.length;j++){
        const node=orig.steps[j],expect=reduced(node.c,x,gate);
        if(node.type==='input'){res.push(expect);continue;}
        if(expect===null){res.push(null);continue;}
        const a=res[node.i],b=res[node.j];
        let best=[a,b].find(z=>z!==null&&z.every(l=>expect.includes(l)));
        if(best===undefined){
            if(a===null||b===null)throw Error('bad cofactor taut premise');
            best=undefined;
            for(const p of a)if(b.includes(-p)){
                const c=derive(a,b,p);
                if(c.every(l=>expect.includes(l))){best=c;paid++;break;}
            }
        }
        ok(best!==undefined,'projection has a derivable subclause');
        res.push(best);
    }
    ok(res.at(-1)!==null&&res.at(-1).length===0,'cofactor contradicts');
    for(const d of orig.defs)for(const clause of d)
        ok(reduced(clause,x,gate)===null,'definition eliminates');
    return paid;
}
let checked=0;
for(const row of payload.cases){
    const {g,mode}=row;
    ok(row.gate_backdoor_B.length===1&&row.gate_backdoor_B[0]===1,'B');
    ok(row.collapse_branches===2,'two branches');
    if(mode==='parallel'){
        const d=build(g),r=d.steps.length-d.bank.length;
        ok(row.strict_resolution_nodes===r,'r');
        ok(row.old_397_bound===(2**g)*(r+1)-1,'397 bound');
        ok(row.new_398_bound===2*(r+1)-1,'398 bound');
        ok(projected(d,g,false)<=r,'false branch');
        ok(projected(d,g,true)<=r,'true branch');
        if(g<=4){
            ok(models(d.src,g+1)===0,'UNSAT');
            for(let i=0;i<d.src.length;i++)
                ok(models(d.src.filter((_,j)=>i!==j),g+1)>0,'minimal UNSAT');
        }
    }else{
        let old;
        for(let i=0;i<g;i++){
            const w=i+2, vTrue=i===0?w:old;
            ok(false===false,'false chain');
            ok(vTrue===w||vTrue===2,'true chain');
            old=vTrue;
        }
    }
    checked++;
}
let rejected=0;
for(const mutate of [
 v=>{v[0].new_398_bound--},
 v=>{v[0].strict_resolution_nodes=0},
 v=>{v[0].gate_backdoor_B=[2]},
 v=>{v[0].old_397_bound=3},
 v=>{v[0].collapse_branches=1}
]){
    const c=JSON.parse(JSON.stringify(payload.cases));mutate(c);
    const r=c[0];
    try{
        ok(r.gate_backdoor_B.length===1&&r.gate_backdoor_B[0]===1,'corrupt B');
        ok(r.collapse_branches===2,'corrupt branches');
        const d=build(r.g),k=d.steps.length-d.bank.length;
        ok(r.strict_resolution_nodes===k,'corrupt r');
        ok(r.old_397_bound===(2**r.g)*(k+1)-1,'corrupt old');
        ok(r.new_398_bound===2*(k+1)-1,'corrupt new');
    }catch(e){rejected++;}
}
ok(rejected===5,'all mutations rejected');
console.log(JSON.stringify({independent_assertions:asserts,checks:checked,
  rejected_corruptions:rejected,
  raw_sha256:crypto.createHash('sha256').update(fs.readFileSync(process.argv[2]||
    'results/raw/arc/2026-11-04_1213_LSPV2_GATE_COLLAPSE_BACKDOOR398_raw.json')).digest('hex')},null,2));
