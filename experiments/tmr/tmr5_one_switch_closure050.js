#!/usr/bin/env node
"use strict";
// TMR-5 independent one-switch neighborhood-rank audit; no packages, no seed.
// Proof scope is restricted to deterministic acyclic shared binary branching programs.
function audit050(){
"use strict";
let checks=0, matrices=0, traces=0, rectangleChecks=0, groupedGraphs=0;
function eq(test,msg){checks++;if(!test)throw Error(msg)}
function rank(A,p){const m=A.length,n=A[0].length;let B=A.map(r=>r.slice()),r=0;function inv(a){let t=1,b=a,e=p-2;while(e){if(e&1)t=t*b%p;b=b*b%p;e>>=1}return t}for(let c=0;c<n&&r<m;c++){let j=r;while(j<m&&!B[j][c])j++;if(j===m)continue;[B[r],B[j]]=[B[j],B[r]];const u=inv(B[r][c]);for(let z=c;z<n;z++)B[r][z]=B[r][z]*u%p;for(let i=r+1;i<m;i++){const f=B[i][c];if(!f)continue;for(let z=c;z<n;z++)B[i][z]=(B[i][z]-f*B[r][z]%p+p)%p}r++}return r}
function graph(k,mask){let edges=[];for(let i=0;i<k;i++)for(let j=0;j<k;j++)if(mask&(1<<(k*i+j)))edges.push([i,j]);return edges}
function crossMatrix(k,edges){
 const m=1<<k,ng=Array(k).fill(0);for(const [i,j] of edges)ng[i]|=1<<j;
 const unions=[],D=[],C=[];for(let x=0;x<m;x++){let u=0;for(let i=0;i<k;i++)if(x&(1<<i))u|=ng[i];unions.push(u);let a=[],c=[];for(let y=0;y<m;y++){const v=+((u&y)===0);a.push(v);c.push(1-v)}D.push(a);C.push(c)}
 const r=new Set(unions).size;for(const p of [2,101]){eq(rank(D,p)===r,"rank D");eq(rank(C,p)===r-1,"rank complement");eq(rank(D.map((row,i)=>row.map((v,j)=>(v+C[i][j])%p)),p)===1,"selector collapse")}
 matrices++;return {r,D,ng};
}
class BP{
 constructor(){this.nodes=new Map;this.keys=new Map}
 add(v,l,h){if(l===h)return l;const key=v+":"+l+":"+h;if(this.keys.has(key))return this.keys.get(key);const id=this.nodes.size+2;this.keys.set(key,id);this.nodes.set(id,{v,l,h});return id}
 trace(root,x,y,k){let id=root,side=null,b=0,ts=[],s=0;while(id>=2){const nd=this.nodes.get(id);eq(!!nd,"missing node");const own=nd.v<k?"X":"Y";if(side&&side!==own){b++;ts.push(id)}side=own;const bit=nd.v<k?(x>>nd.v)&1:(y>>(nd.v-k))&1;id=bit?nd.h:nd.l;s++;eq(s<=this.nodes.size,"cycle")}traces++;return {value:id,b,ts:ts.join(",")}}
}
function matchInterleaved(k){const B=new BP;let root=1;for(let i=k-1;i>=0;i--){const testY=B.add(k+i,root,0);root=B.add(i,root,testY)}return {B,root}}
function grouped(k,ng){const B=new BP;let xm=new Map,ym=new Map;function Y(j,u){const key=j+":"+u;if(ym.has(key))return ym.get(key);let v=j===k?1:((u>>j)&1)?B.add(k+j,Y(j+1,u),0):Y(j+1,u);ym.set(key,v);return v}function X(j,u){const key=j+":"+u;if(xm.has(key))return xm.get(key);let v=j===k?Y(0,u):B.add(j,X(j+1,u),X(j+1,u|ng[j]));xm.set(key,v);return v}return {B,root:X(0,0)}}
function completeGrouped(k){const B=new BP;let Y=1;for(let i=k-1;i>=0;i--)Y=B.add(k+i,Y,0);let root=1;for(let i=k-1;i>=0;i--)root=B.add(i,root,Y);return {B,root}}
function testBP(name,k,model,D,r,rectangles=true){
 const {B,root}=model,m=1<<k;let b=0,accepted=new Map;
 for(let x=0;x<m;x++)for(let y=0;y<m;y++){const t=B.trace(root,x,y,k);eq(t.value===D[x][y],"incorrect BP "+name);b=Math.max(b,t.b);if(rectangles&&t.value){if(!accepted.has(t.ts))accepted.set(t.ts,[]);accepted.get(t.ts).push([x,y])}}
 if(rectangles)for(const pairs of accepted.values()){const xx=new Set(pairs.map(z=>z[0])),yy=new Set(pairs.map(z=>z[1]));eq(pairs.length===xx.size*yy.size,"nonrectangle");rectangleChecks++;const seen=new Set(pairs.map(z=>z.join(",")));for(const x of xx)for(const y of yy)eq(seen.has(x+","+y),"rectangle hole")}
 const V=B.nodes.size,VX=[...B.nodes.values()].filter(n=>n.v<k).length,VY=V-VX;
 if(b<=1){eq(V>=2*(r-1),"one-switch total lower bound");eq(VX>=r-1||V===0,"X-side lower bound");eq(VY>=r-1||V===0,"Y-side lower bound")}
 if(rectangles){let sum=0n;for(let j=0;j<=b;j++)sum+=BigInt(V)**BigInt(j);eq(BigInt(r)<=BigInt(accepted.size),"rank > transcripts");eq(BigInt(accepted.size)<=sum,"transcripts bound");eq(BigInt(r)<=BigInt(V+1)**BigInt(b+1),"uniform switching inequality")}
 return {name,k,V,VX,VY,b,r,transcripts:rectangles?accepted.size:null,tests:m*m};
}
let runs=[];for(let k=1;k<=6;k++){
 const match=Array.from({length:k},(_,i)=>[i,i]),full=Array.from({length:k*k},(_,z)=>[Math.floor(z/k),z%k]);
 const a=crossMatrix(k,match),c=crossMatrix(k,full);
 runs.push(testBP("MATCH_INTERLEAVED",k,matchInterleaved(k),a.D,a.r));
 runs.push(testBP("MATCH_GROUPED",k,grouped(k,a.ng),a.D,a.r));
 runs.push(testBP("COMPLETE_GROUPED",k,completeGrouped(k),c.D,c.r));
 eq(a.r===2**k,"matching closure");eq(c.r===2,"complete closure");
 eq(runs[runs.length-3].V===2*k,"interleaved size");
 eq(runs[runs.length-2].V===2*(2**k-1),"exact grouped minimum");
 eq(runs[runs.length-1].b<=1,"complete switches");
}
let exhaustive=0,dist={};for(let mask=0;mask<512;mask++){
 const a=crossMatrix(3,graph(3,mask)),model=grouped(3,a.ng);
 const result=testBP("ALL3x3_"+mask,3,model,a.D,a.r,false);
 eq(result.b<=1,"grouped one switch");dist[a.r]=(dist[a.r]||0)+1;exhaustive++;groupedGraphs++;
}
return {revision:"tmr5-one-switch-closure050.v1",seed:null,fields:[2,101],graphs_exhaustive_3by3:exhaustive,rank_histogram_3by3:dist,rank_matrices:matrices,independently_built_grouped_graphs:groupedGraphs,model:"shared deterministic acyclic binary branching programs with fixed X:Y; all input tests and source acquisition charged in ledgers",test_cases:runs.length,assignment_traces:traces,rectangle_groups_checked:rectangleChecks,assertions:checks,failures:0,cases:runs};
}
process.stdout.write(JSON.stringify(audit050(),null,2)+'\n');
