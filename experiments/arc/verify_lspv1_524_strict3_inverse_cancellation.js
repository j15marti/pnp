/* Independent LSPV-1/524 proof replay (ES2020); historical R_mix341 NOT certified. */
"use strict";
function chk(x,msg){if(!x)throw Error(msg)}
function cl(a){chk(Array.isArray(a)&&a.every(x=>Number.isInteger(x)&&x!==0),"bad literal");let z=[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);chk(!z.some(x=>z.includes(-x)),"tautology");return z}
function eq(a,b){return JSON.stringify(cl(a))===JSON.stringify(cl(b))}
function bit(l,v){return l>0?v[l]:!v[-l]}
function check(P){
const q=P.proof,L=q.lines,G=q.definitions;
const S=[[1,2,3],[-1,-2,4],[-1,-2,-4],[-1,-3,4],[-1,-3,-4],[-2,-3,4],[-2,-3,-4]];
chk(L.length===118&&G.length===19&&q.paid_resolution_nodes===54&&q.paid_work_unit===73,"counts");
let F=new Map,prev=4,checks=0,nres=0,nfacet=0,nsource=0,depth=Array(L.length).fill(0);
for(const g of G){
 chk(g.id===prev+1&&Math.abs(g.a)!==Math.abs(g.b)&&Math.abs(g.a)<=prev&&Math.abs(g.b)<=prev,"gate IDs/ports");
 prev=g.id;
 [[-g.id,g.a],[-g.id,g.b],[g.id,-g.a,-g.b]].forEach((c,k)=>F.set(g.facets[k],{c,owner:g.owner,tag:["left","right","back"][k]}));checks++;
}
for(const l of L){
 chk(l.id===nres+nfacet+nsource,"line id");
 let c=cl(l.clause);chk(c.length===l.clause.length,"noncanonical record");
 if(l.kind==="SOURCE"){chk(l.id<7&&eq(c,S[l.id]),"original source");nsource++;}
 else if(l.kind==="FACET"){let t=F.get(l.id);chk(t&&l.owner===t.owner&&l.tag===t.tag&&eq(c,t.c),"facet owner");nfacet++;}
 else if(l.kind==="RES"){chk(l.left<l.id&&l.right<l.id&&l.pivot>0,"parents");
 const a=L[l.left].clause,b=L[l.right].clause,p=l.pivot;chk(a.includes(p)&&b.includes(-p),"pivot");
 chk(eq(c,[...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]),"RES result");
 depth[l.id]=1+Math.max(depth[l.left],depth[l.right]);nres++;
 }else throw Error("invalid record type");
 checks++;
}
chk(nsource===7&&nfacet===57&&nres===54,"kinds");
const wanted=[[6,7,8],[-6,-7],[-6,-8],[-7,-8],[-19],[21],[23]];
chk(q.targets.length===7,"goals");
q.targets.forEach((g,i)=>{chk(eq(g.clause,wanted[i])&&eq(L[g.id].clause,wanted[i]),"target");checks++;});
let sat=0,invalid=0;
for(let mask=0;mask<16;mask++){
 let v={};for(let j=1;j<=4;j++)v[j]=!!(mask&(1<<(j-1)));
 for(const g of G)v[g.id]=bit(g.a,v)&&bit(g.b,v);
 for(const g of G)for(const f of g.facets)chk(L[f].clause.some(x=>bit(x,v)),"facet semantics");
 if(S.every(c=>c.some(x=>bit(x,v)))){sat++;chk(wanted.every(c=>c.some(x=>bit(x,v))),"output semantics");
 let i=[1,2,3].findIndex(x=>v[x]),j=[6,7,8].findIndex(x=>v[x]);chk(j===(3-i)%3,"inverse semantics");
 }else invalid++; checks++;
}
chk(sat===6&&invalid===10,"original models");
function syntaxTest(v){let z=v.proof;
for(let i=0;i<7;i++)chk(eq(z.lines[i].clause,S[i]),"source mutation");
for(const g of z.definitions){chk(Math.abs(g.a)!==Math.abs(g.b),"duplicate port");[[-g.id,g.a],[-g.id,g.b],[g.id,-g.a,-g.b]].forEach((c,k)=>chk(eq(z.lines[g.facets[k]].clause,c),"facet mutation"));}
for(const l of z.lines)if(l.kind==="RES"){let a=z.lines[l.left].clause,b=z.lines[l.right].clause,p=l.pivot;chk(a.includes(p)&&b.includes(-p),"pivot mutation");chk(eq(l.clause,[...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]),"RES mutation");}
wanted.forEach((c,i)=>chk(eq(z.lines[z.targets[i].id].clause,c),"goal mutation"));
}
let corrupt=0;
for(const mutation of [z=>z.proof.lines.find(x=>x.kind==="RES").pivot=999,z=>z.proof.lines.find(x=>x.kind==="FACET").clause=[999],z=>z.proof.lines[0].clause=[-1,2,3],z=>z.proof.definitions[0].b=z.proof.definitions[0].a,z=>z.proof.targets[4].id=0]){
 let cp=JSON.parse(JSON.stringify(P));mutation(cp);try{syntaxTest(cp)}catch(e){corrupt++}
}
chk(corrupt===5,"mutation accepted");
const dimacs="p cnf 4 7\n"+S.map(c=>c.join(" ")+" 0").join("\n")+"\n";
function parse(s){let a=s.trim().split("\n");chk(a[0]==="p cnf 4 7"&&a.length===8,"dimacs header/count");return a.slice(1).map(r=>{let v=r.trim().split(/\s+/).map(Number);chk(v.at(-1)===0,"terminator");v.pop();chk(v.every(l=>l&&Math.abs(l)<=4),"range");return cl(v)})}
chk(parse(dimacs).every((c,i)=>eq(c,S[i])),"dimacs invalid");
let bad=0;for(const s of [dimacs.replace("p cnf 4 7","p cnf 3 7"),dimacs.replace(" 0\n"," 9\n"),dimacs+"1 0\n"]){try{parse(s)}catch(e){bad++}}
chk(bad===3,"malformed accepted");
return {status:"PASS",counts:{original_sources:nsource,def_facets:nfacet,paid_definitions:G.length,paid_resolution:nres,paid_logical_work:q.paid_work_unit,total_clauses:L.length,checks,valid_source_assignments:sat,invalid_source_assignments:invalid,corruptions_rejected:corrupt,malformed_rejected:bad,maximum_RES_depth:Math.max(...depth)},scope:"independent original-source/facet-owner/RES/semantic replay; historical R_mix341 open"};
}
function main(packet){return check(packet)}

if(typeof module!=="undefined"&&require.main===module){const f=require("fs");console.log(JSON.stringify(main(JSON.parse(f.readFileSync(process.argv[2],"utf8"))),null,2));}
