const pin=(F,v)=>F.map(f=>{let i=f.vs.indexOf(v);if(i<0)return f;return{...f,vs:f.vs.filter(x=>x!==v),ok:f.ok.filter(w=>!(w>>i&1)).map(w=>(w&((1<<i)-1))|((w>>(i+1))<<i))}})
;
function replayRUP(F,proof){
 let db=[],scans=0,lits=0;
 for(let f of F)for(let w=0;w<2**f.vs.length;w++)if(!f.ok.includes(w))db.push(f.vs.map((v,i)=>(w>>i&1)?-v:v));
 function conflict(assumptions){let a=new Map();for(let l of assumptions){let v=Math.abs(l),b=l>0;if(a.has(v)&&a.get(v)!==b)return true;a.set(v,b)}for(;;){let n=a.size;for(let c of db){scans++;if(scans>10000000)throw Error("CAP");let u=[],sat=false;for(let l of c){lits++;if(a.get(Math.abs(l))===(l>0)){sat=true;break}if(!a.has(Math.abs(l)))u.push(l)}if(sat)continue;if(!u.length)return true;if(u.length===1)a.set(Math.abs(u[0]),u[0]>0)}if(n===a.size)return false}}
 for(let z of proof){if(z.kind!=="UP"||!conflict(z.clause.map(l=>-l)))return{verified:false,scans,lits,failed:z};db.push(z.clause)}
 return{verified:proof.at(-1).clause.length===0,scans,lits}
}
module.exports={pin,replayRUP};
