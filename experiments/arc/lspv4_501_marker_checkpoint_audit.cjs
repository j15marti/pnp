// LSPV-4/501: standalone exact-state marker replay verifier (V8/Node).
function audit() {
 const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],bit=(x,w)=>x.toString(2).padStart(w,"0");
 function core(c){const out=[];for(let v=0;v<4;v++){const ids=edges.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);for(let a=0;a<8;a++){let signs=[0,1,2].map(t=>(a>>t)&1);if((signs[0]+signs[1]+signs[2])%2!==c[v])out.push(ids.map((id,k)=>signs[k]?-id:id));}}return out;}
 function f(r,j,c){const n=6+4*r,w=n.toString(2).length,cs=[];for(let i=0;i<r;i++)cs.push([7+4*i,8+4*i+((j>>(r-i-1))&1),10+4*i]);cs.push(...core(c));let s="11010010"+bit(n,16)+bit(cs.length,16);for(const cl of cs)for(const l of cl)s+=(l<0?"1":"0")+bit(Math.abs(l),w);return {s,cs,n,w};}
 function parse(s){if(s.length<40||s.slice(0,8)!=="11010010")return null;const n=parseInt(s.slice(8,24),2),m=parseInt(s.slice(24,40),2),w=n.toString(2).length;if(s.length!==40+m*3*(w+1))return null;let cs=[],p=40;for(let i=0;i<m;i++){let c=[],ids=[];for(let k=0;k<3;k++){let neg=s[p++]==="1",id=parseInt(s.slice(p,p+w),2);p+=w;if(!(id>=1&&id<=n))return null;ids.push(id);c.push(neg?-id:id);}if(new Set(ids).size!==3||ids.some((x,k)=>k>0&&x<=ids[k-1]))return null;cs.push(c);}return new Set(cs.map(c=>c.join(","))).size===cs.length?cs:null;}
 function count(cs){let n=0;for(let a=0;a<64;a++)if(cs.every(c=>c.some(l=>Boolean(a&(1<<(Math.abs(l)-1)))===(l>0))))n++;return n;}
 const check=(x,m)=>{if(!x)throw Error("LSPV4/501 "+m);};
 check(count(core([1,0,0,0]))===0,"odd UNSAT");check(count(core([0,0,0,0]))===8,"even SAT");
 let rows=[];
 for(const [r,K] of [[3,33],[5,129],[7,257]]){
  const q=1<<r,first=f(r,0,[1,0,0,0]),trie=new Set([""]),suffix=new Set(),sources=new Set();let even=0;
  for(let j=0;j<q;j++){const v=f(r,j,[1,0,0,0]);check(JSON.stringify(parse(v.s))===JSON.stringify(v.cs),"valid original");sources.add(v.s);check(v.s.length===first.s.length,"fixed bits");check(8*v.cs.length-2*v.n===116,"decode H");check(v.cs.length-16===r,"decode r");let tag=0;for(let i=0;i<r;i++){let p=40+i*3*(v.w+1)+2*v.w+1;tag=(tag<<1)+Number(v.s[p]!==first.s[p]);trie.add(j.toString(2).padStart(r,"0").slice(0,i+1));}check(tag===j,"tag");for(let t=0;t<=K;t++)suffix.add(j+":"+t);if(j<2||j===q-1){let e=f(r,j,[0,0,0,0]);check(JSON.stringify(parse(e.s))===JSON.stringify(e.cs),"even");even++;}}
  check(sources.size===q&&trie.size===2*q-1&&suffix.size===q*(K+1),"trie/suffix state counts");
  const sz=3*(first.w+1),dup=first.s.slice(0,40+sz)+first.s.slice(40,40+sz)+first.s.slice(40+2*sz);
  const bad=[(first.s[0]==="1"?"0":"1")+first.s.slice(1),first.s.slice(0,-1),dup,first.s.slice(0,41)+"0".repeat(first.w)+first.s.slice(41+first.w)];
  check(bad.every(s=>parse(s)===null),"malformed");
  rows.push({r,q,K,bits:first.s.length,valid_odd:q,valid_even:even,malformed:4,prefix_nodes:trie.size,prefix_edges:trie.size-1,naive_prefix_reads:q*r,suffix_states:suffix.size,unshared_paid_suffix:q*K,early_savings:q*r-(trie.size-1)});
 }
 return {scope:"finite hosted exact-state model; NOT a native FLMV machine",rows};
}
if(typeof console!=="undefined")console.log(JSON.stringify(audit(),null,2));
