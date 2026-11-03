"use strict";
// Deterministic strict-3CNF matching-merger proof source, LSPV-1 363.
function bit(x){let p=0;while(x){p^=1;x&=x-1n;}return p;}
function edges(k){let a=[];for(let i=0;i<k;i++)a.push([i,(i+1)%k]);for(let i=0;i<k;i++)a.push([k+i,k+(i+1)%k]);for(let i=0;i<k;i++)a.push([i,k+i]);return a;}
function solve(E,b,n){let piv={};for(let i=0;i<E.length;i++){let m=E[i],v=b[i];while(m){let j=0;while(!(m&(1n<<BigInt(j))))j++;if(piv[j]){m^=piv[j][0];v^=piv[j][1];}else{piv[j]=[m,v];break;}}if(!m&&v)return null;}let x=0n;for(let j=n-1;j>=0;j--)if(piv[j]){let [m,v]=piv[j];if(v^bit((m&~(1n<<BigInt(j)))&x))x|=1n<<BigInt(j);}return x;}
function build(k){
 if(k<4||k%2)throw Error("k must be even >= 4");const h=2*k,ed=edges(k),matching=Array.from({length:k/2},(_,i)=>2*i);
 let n=1,cols=ed.map((_,i)=>matching.includes(i)?1:++n),rows=Array(h).fill(0n),rhs=Array(h).fill(0);rhs[0]=1;
 for(let i=0;i<ed.length;i++){let [u,v]=ed[i],m=1n<<BigInt(cols[i]-1);rows[u]^=m;rows[v]^=m;}
 for(let omit=0;omit<h;omit++){let q=[omit===0?1:0],seen=new Set(q);for(let a=0;a<q.length;a++)for(let i=0;i<ed.length;i++){if(matching.includes(i))continue;let[u,v]=ed[i],to=u===q[a]?v:v===q[a]?u:-1;if(to>=0&&to!==omit&&!seen.has(to)){seen.add(to);q.push(to);}}if(seen.size!==h-1)throw Error("not two-vertex-connected after deletion");}
 let supports=[],sources=[],groups=[];
 for(let r=0;r<h;r++){let vs=[];for(let v=1;v<=n;v++)if(rows[r]&(1n<<BigInt(v-1)))vs.push(v);if(vs.length!==3)throw Error("width not three");supports.push(vs);let ids=[];for(let tuple=0;tuple<8;tuple++)if(bit(BigInt(tuple))!==rhs[r]){ids.push(sources.length);sources.push({eq:r,tuple,lits:vs.map((v,j)=>tuple>>j&1?-v:v)});}groups.push(ids);}
 function table(id,vs){let mask=0;for(let a=0;a<8;a++)if(sources[id].lits.some(l=>(l>0)===Boolean(a>>vs.indexOf(Math.abs(l))&1)))mask|=1<<a;return mask;}
 let proof=[],last=[];
 for(let i=0;i<h;i++){let p="S"+groups[i][0],mask=table(groups[i][0],supports[i]);for(let j=1;j<4;j++){mask&=table(groups[i][j],supports[i]);let id=proof.length;proof.push({op:"AND3",parents:[p,"S"+groups[i][j]],support:supports[i],table:mask});p="D"+id;}last.push(p);}
 let row=rows[0],b=rhs[0],prev=last[0];for(let i=1;i<h;i++){row^=rows[i];b^=rhs[i];let id=proof.length;proof.push({op:"XOR",parents:[prev,last[i]],coeff:row.toString(16),rhs:b});prev="D"+id;}
 if(row!==0n||b!==1||proof.length!==4*h-1)throw Error("bad proof terminal");
 let witnesses=[];for(let s of sources){let eqs=[],bs=[];for(let j=0;j<h;j++)if(j!==s.eq){eqs.push(rows[j]);bs.push(rhs[j]);}for(let j=0;j<3;j++){eqs.push(1n<<BigInt(supports[s.eq][j]-1));bs.push(s.tuple>>j&1);}let x=solve(eqs,bs,n);if(x===null)throw Error("missing deletion witness");witnesses.push(x.toString(16));}
 let dimacs="p cnf "+n+" "+sources.length+"\n"+sources.map(s=>s.lits.join(" ")+" 0\n").join("");
 return {k,h,n,edges:ed,matching,columns:cols,rows:rows.map(x=>x.toString(16)),rhs,supports,sources,proof,witnesses,encodedBits:8*dimacs.length};
}
function produce(){return {schema:"MATCHING_MERGER363",calculus:"Rmix341",generated:"2026-11-03_0600_PST",cases:[4,6,8,10,12].map(build)};}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(produce()));