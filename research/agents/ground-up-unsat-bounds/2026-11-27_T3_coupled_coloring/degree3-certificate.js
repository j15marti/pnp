const fs=require('node:fs'),crypto=require('node:crypto');
const proof=function proof(x,cap=3000000){
 const A=(t,m)=>{if(!t)throw Error(m)},F=x.raw.trimEnd().split("\n").slice(1).map(c=>c.split(" ").map(Number).slice(0,-1)),n=x.vertices,r=2*n,K=c=>c.slice().sort((a,b)=>a-b).join(","),db=new Set(F.map(K)),B=r+1;
 function mono(v){v=[...new Set(v)].sort((a,b)=>a-b);let id=v.length===0?0:v.length===1?v[0]:v.length===2?B+v[0]*B+v[1]:B+B*B+v[0]*B*B+v[1]*B+v[2];return [id,v]}
 function poly(terms){let m=new Map();for(let t of terms){let [id,v]=mono(t);if(m.has(id))m.delete(id);else m.set(id,v)}return [...m.values()]}
 let rows=[],ids=[],sourceTests=0;for(let v=0;v<n;v++){let a=3*v+1,b=a+1,c=a+2;for(let t of [[a,b,c],[-a,-b],[-a,-c],[-b,-c]]){sourceTests++;A(db.delete(K(t)),"group")}rows.push([[2*v+1,2*v+2]]);ids.push(["V",v])}
 for(let s of [...db]){if(!db.has(s))continue;let [l,m]=s.split(",").map(Number),u=Math.floor((-l-1)/3),v=Math.floor((-m-1)/3);A(l<0&&m<0&&u!==v&&(-l-1)%3===(-m-1)%3,"edge");for(let c=1;c<=3;c++){sourceTests++;A(db.delete(K([-(3*u+c),-(3*v+c)])),"triple")}let a=2*u+1,b=a+1,c=2*v+1,d=c+1;rows.push([[a,c]],[[b,d]],poly([[],[a],[b],[c],[d],[a,c],[a,d],[b,c],[b,d]]));ids.push(["E",u,v,0],["E",u,v,1],["E",u,v,2])}
 A(!db.size,"extra");let basis=new Map(),records=[],work=0,xors=0,generated=0,root=null,stored=0,depArcs=0;
 function add(i,v){generated++;let s=new Set(poly(v?rows[i].map(t=>[...t,v]):rows[i]).map(v=>mono(v)[0])),parents=[];while(s.size){let p=-1;for(let z of s){work++;if(z>p)p=z}if(work>cap)throw Error("cap");if(!basis.has(p)){let node={s,i,v,parents,index:records.length};records.push(node);basis.set(p,node);stored+=s.size;depArcs+=parents.length;if(p===0)root=node.index;return}let b=basis.get(p);xors++;parents.push(b.index);for(let z of b.s){work++;if(s.has(z))s.delete(z);else s.add(z)}}}
 outer:{for(let i=0;i<rows.length;i++){add(i,0);if(root!==null)break outer}for(let i=0;i<rows.length;i++)for(let v=1;v<=r;v++){add(i,v);if(root!==null)break outer}}
 A(root!==null,"no constant");
 let active=new Set([root]),terms=new Map(),extraction=0;
 for(let j=root;j>=0;j--){extraction++;if(!active.has(j))continue;let q=records[j],k=q.i*(r+1)+q.v;if(terms.has(k))terms.delete(k);else terms.set(k,[ids[q.i],q.v]);for(let p of q.parents){extraction++;if(active.has(p))active.delete(p);else active.add(p)}}
 return {k:x.k,sha:x.sha,N:x.N,variables:r,terms:[...terms.values()],generated,rank:basis.size,work,xors,stored,depArcs,extraction,sourceTests}
};
const verify=function verify(x,c){
 const A=(t,m)=>{if(!t)throw Error(m)},F=x.raw.trimEnd().split("\n").slice(1).map(c=>c.split(" ").map(Number).slice(0,-1)),n=x.vertices,K=c=>c.slice().sort((a,b)=>a-b).join(","),db=new Set(F.map(K)),S=new Set(),counts={sourceChecks:0,products:0,terms:0};
 const toggle=t=>{let k=[...new Set(t)].sort((a,b)=>a-b).join(":");if(S.has(k))S.delete(k);else S.add(k);counts.terms++};
 const colors=(v,c)=>c===0?[[2*v+1]]:c===1?[[2*v+2]]:[[],[2*v+1],[2*v+2]];
 for(let [id,m] of c.terms){A(Number.isInteger(m)&&m>=0&&m<=2*n,"multiplier");let row;if(id[0]==="V"){let v=id[1],a=3*v+1,b=a+1,d=a+2;A(v>=0&&v<n,"vertex");for(let t of [[a,b,d],[-a,-b],[-a,-d],[-b,-d]]){counts.sourceChecks++;A(db.has(K(t)),"onehot source")}row=[[2*v+1,2*v+2]]}
 else{let [tag,u,v,col]=id;A(tag==="E"&&u!==v&&u>=0&&u<n&&v>=0&&v<n&&col>=0&&col<3,"edge");counts.sourceChecks++;A(db.has(K([-(3*u+col+1),-(3*v+col+1)])),"edge source");row=[];for(let a of colors(u,col))for(let b of colors(v,col)){counts.products++;row.push([...a,...b])}}
 for(let t of row)toggle(m?[...t,m]:t)}
 A(S.size===1&&S.has(""),"not constant");return {...counts,constant:true,proofTerms:c.terms.length}
};
const d=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));const out=d.families.filter(x=>x.label==='NO'&&x.k<=6).map(x=>{if(crypto.createHash('sha256').update(x.raw).digest('hex')!==x.sha||Buffer.byteLength(x.raw)*8!==x.N)throw Error('source hash');let c=proof(x);return {...c,verification:verify(x,c)}});console.log(JSON.stringify(out,null,2));
