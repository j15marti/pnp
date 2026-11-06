// LSPV-4/434 compact independent source-port test; no libraries.
const output=(()=>{let n=0,visits=0;
const eq=(a,b)=>{if(JSON.stringify(a)!==JSON.stringify(b))throw Error("FAIL");++n;};
class Bank{constructor(H){this.e=0;this.t=Array(H).fill(0);this.v=Array(H).fill(0)}
 enter(ed){this.e++;ed.forEach(x=>{if(x<0||x>=this.t.length)throw Error("bad ID");if(this.t[x]!==this.e){this.t[x]=this.e;this.v[x]=0;}this.v[x]^=1;});}
 get(x){return this.t[x]===this.e?this.v[x]:0;}}
const graphs={K4:[4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]],Cube:[8,Array.from({length:8},(_,u)=>[1,2,4].map(k=>[u,u^k]).filter(([a,b])=>a<b)).flat()],Petersen:[10,[...Array.from({length:5},(_,i)=>[i,(i+1)%5]),...Array.from({length:5},(_,i)=>[i,i+5]),...Array.from({length:5},(_,i)=>[i+5,(i+2)%5+5])]]};
let rows=[];for(const [name,[H,E]] of Object.entries(graphs)){let A=Array.from({length:H},()=>[]);E.forEach(([u,v],id)=>{A[u].push(id);A[v].push(id)});A.forEach(x=>eq(x.length,3));A=A.map(x=>x.sort((a,b)=>a-b));
const clause=c=>{let x=[];for(let v=0;v<H;v++)for(let p=0;p<2;p++)for(let r=0;r<2;r++)x.push([[A[v][0],p],[A[v][1],r],[A[v][2],p^r^1^c[v]]]);return x;};
const base=Array.from({length:H},(_,i)=>i%2),banks=Array.from({length:3},()=>new Bank(H)),st=[base.slice()];let seq=19,seen=0;
function audit(d){const c=base.map((b,v)=>{for(let i=0;i<d;i++)b^=banks[i].get(v);return b;});eq(c,st[st.length-1]);eq(clause(c),clause(st[st.length-1]));seen++;visits++;}
function dfs(d){audit(d);if(d===3)return;for(let j=0;j<3;j++){let ed=[];for(let k=0;k<8+j;k++){seq=(Math.imul(seq,1664525)+1013904223)>>>0;ed.push(seq%H);}ed.push(0,0);banks[d].enter(ed);let c=st[st.length-1].slice();ed.forEach(v=>c[v]^=1);st.push(c);dfs(d+1);st.pop();audit(d);}}
dfs(0);rows.push({name,seen,epochs:banks.map(b=>b.e)});}
let b=new Bank(4);b.enter([0]);eq(b.get(0),1);b.enter([0]);eq(b.t[0]===1?b.v[0]:0,0);
return {status:"PASS",assertions:n,snapshots:visits,rows,parent_lifetime_counterexample:true,
limits:"finite source checks, not native FLMV"};
})();if(typeof console!=="undefined")console.log(JSON.stringify(output));output;