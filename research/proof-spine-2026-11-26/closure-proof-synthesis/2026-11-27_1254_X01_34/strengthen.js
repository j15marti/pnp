/* Native RUP-to-subclause compiler, source pins and replay instructions in results.json. */
function strengthen(base, trace, limit=1000000) {
 const rec=base.rec.map(r=>({...r,c:r.c.slice()})),ids=base.ids.slice(),seen=new Map(rec.map((r,i)=>[r.c.join(","),i]));let scans=0,resolutions=0,reused=0,accepted=0,refused=0,maxTrail=0,terminal=null;
 const norm=c=>[...new Set(c)].sort((a,b)=>a-b);
 function derive(a,b,v){const x=rec[a].c,y=rec[b].c;if(!(x.includes(v)&&y.includes(-v)||x.includes(-v)&&y.includes(v)))throw Error("pivot");const c=norm(x.concat(y).filter(l=>Math.abs(l)!==v));if(c.some(l=>c.includes(-l)))throw Error("tautological conflict resolvent");let k=c.join(",");resolutions++;if(seen.has(k)){reused++;return seen.get(k)}let i=rec.length;rec.push({c,p:[a,b,v]});seen.set(k,i);return i}
 for(const target0 of trace){let target=norm(target0);if(target.some(l=>target.includes(-l)))throw Error("taut target");let A=new Set(target.map(l=>-l)),trail=[],hit=null,changed=true;
 while(changed&&hit===null){changed=false;for(const i of ids){let c=rec[i].c,free=0,last=0,sat=false;for(const l of c){if(++scans>limit)return {status:"UNKNOWN",accepted,refused,scans,resolutions,reused,maxTrail};if(A.has(l)){sat=true;break}if(!A.has(-l)){free++;last=l}}if(sat)continue;if(!free){hit=i;break}if(free===1){A.add(last);trail.push([last,i]);changed=true}}}
 maxTrail=Math.max(maxTrail,trail.length);if(hit===null){refused++;continue}
 let p=hit;for(let t=trail.length-1;t>=0;t--){let [l,i]=trail[t];if(rec[p].c.includes(-l))p=derive(p,i,Math.abs(l))}
 if(rec[p].c.some(l=>!target.includes(l)))throw Error("not subclause");accepted++;if(!ids.includes(p))ids.push(p);if(!rec[p].c.length){terminal=p;break}
 }
 return {status:terminal===null?"UNKNOWN":"UNSAT",accepted,refused,scans,resolutions,reused,maxTrail,terminal,rec};
}
module.exports={strengthen};
