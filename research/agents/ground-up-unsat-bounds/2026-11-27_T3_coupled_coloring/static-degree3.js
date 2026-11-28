const fs=require('node:fs');
const mac=function mac(x,cap=3000000){
 const A=(t,m)=>{if(!t)throw Error(m)},F=x.raw.trimEnd().split("\n").slice(1).map(c=>c.split(" ").map(Number).slice(0,-1)),n=x.vertices,r=2*n,K=c=>c.slice().sort((a,b)=>a-b).join(","),db=new Set(F.map(K)),B=r+1;
 function mono(v){v=[...new Set(v)].sort((a,b)=>a-b);let id=v.length===0?0:v.length===1?v[0]:v.length===2?B+v[0]*B+v[1]:B+B*B+v[0]*B*B+v[1]*B+v[2];return [id,v]}
 function poly(terms){let m=new Map();for(let t of terms){let [id,v]=mono(t);if(m.has(id))m.delete(id);else m.set(id,v)}return [...m.values()]}
 let rows=[],edges=[],sourceTests=0;for(let v=0;v<n;v++){let a=3*v+1,b=a+1,c=a+2;for(let t of [[a,b,c],[-a,-b],[-a,-c],[-b,-c]]){sourceTests++;A(db.delete(K(t)),"group")}rows.push([[2*v+1,2*v+2]])}
 for(let s of [...db]){if(!db.has(s))continue;let [l,m]=s.split(",").map(Number),u=Math.floor((-l-1)/3),v=Math.floor((-m-1)/3);A(l<0&&m<0&&u!==v&&(-l-1)%3===(-m-1)%3,"edge");for(let c=1;c<=3;c++){sourceTests++;A(db.delete(K([-(3*u+c),-(3*v+c)])),"triple")}edges.push([u,v]);let a=2*u+1,b=a+1,c=2*v+1,d=c+1;rows.push([[a,c]],[[b,d]],poly([[],[a],[b],[c],[d],[a,c],[a,d],[b,c],[b,d]]))}
 A(!db.size,"extra source");let basis=new Map(),work=0,xors=0,generated=0,constant=false,peakTerms=0,stored=0,status="COMPLETE_NO_CONSTANT";
 function add(t){generated++;let s=new Set(poly(t).map(v=>mono(v)[0]));while(s.size){let p=-1;for(let z of s){work++;if(z>p)p=z}if(work>cap)throw Error("cap");if(!basis.has(p)){basis.set(p,s);stored+=s.size;peakTerms=Math.max(peakTerms,stored);if(p===0)constant=true;return}let b=basis.get(p);xors++;for(let z of b){work++;if(s.has(z))s.delete(z);else s.add(z)}}}
 try{for(let p of rows)add(p);for(let p of rows)for(let v=1;v<=r;v++){add(p.map(t=>[...t,v]));if(constant)break}if(constant)status="CONSTANT_FOUND"}catch(e){if(e.message!=="cap")throw e;status="CAP_UNKNOWN"}
 return {k:x.k,sha:x.sha,variables:r,baseRows:rows.length,candidateRows:rows.length*(r+1),generated,rank:basis.size,constant,status,work,xors,storedTerms:stored,peakTerms,sourceTests,degree3Pivots:[...basis.keys()].filter(i=>i>=B+B*B).length}
};
const d=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));console.log(JSON.stringify(d.families.filter(x=>x.label==='NO'&&x.k<=6).map(x=>mac(x)),null,2));
