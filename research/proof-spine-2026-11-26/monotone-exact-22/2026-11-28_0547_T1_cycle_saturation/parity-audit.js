// Source-only owner-mask parity certificate; node parity-audit.js syndrome-controls.json
function parityAudit(raw,sha){
 const enc=x=>JSON.stringify(x)+"\n",v=x=>BigInt("0x"+x),par=x=>{let p=0;while(x){p^=1;x&=x-1n}return p};const out=[];
 for(const z of raw){let c=z.cert,F=c.source;if(sha(enc(F))!==c.instance_id.split(":").at(-1)||c.N!==8*enc(F).length||"CERT-v1:sha256:"+sha(enc(c))!==z.certificate_id)throw Error("source");let L=F.labels.map(A=>A.map(v)),T=v(F.target),m=Math.max(T.toString(2).length,...L.flat().map(x=>x.toString(2).length)),counts={owner:0,proposals:0,labelParity:0,check:0};let groups=new Map();
  for(let b=0;b<m;b++){let owners=[];for(let i=0;i<L.length;i++){counts.owner+=L[i].length;if(L[i].some(x=>x&(1n<<BigInt(b))))owners.push(i)}let k=owners.join(",");if(!groups.has(k))groups.set(k,0n);groups.set(k,groups.get(k)|(1n<<BigInt(b)))}
  let proof=null;for(const [owners,H] of groups){counts.proposals++;let offsets=[],ok=true;for(let i=0;i<L.length;i++){let a=par(L[i][0]&H);for(const x of L[i]){counts.labelParity++;if(par(x&H)!==a)ok=false}offsets.push(a)}if(ok&&offsets.reduce((a,b)=>a^b,0)!==par(T&H)){proof={mask:H.toString(16),ownerGroup:owners,offsets,targetParity:par(T&H)};break}}
  if(proof){let H=v(proof.mask),s=0;for(let i=0;i<L.length;i++){let a=proof.offsets[i];for(const x of L[i]){counts.check++;if(par(H&x)!==a)throw Error("parity")};s^=a}if(s===proof.targetParity)throw Error("no contradiction")}
  const record={instance_id:c.instance_id,original_N_bits:c.N,guard_id:"EMPTY",residual_id:"ROOT",original_ids:c.original_ids,parents:[],source_pin:"b1bd8ec2b83f3b4f782ad7236da963d54a7b4e7e",status:proof?"NO":"NO_CERTIFICATE",proof,counts};out.push({certificate_id:"CERT-v1:sha256:"+sha(enc(record)),record})
 }
 return out;
}
const fs=require('node:fs'),crypto=require('node:crypto');console.log(JSON.stringify(parityAudit(JSON.parse(fs.readFileSync(process.argv[2],'utf8')),s=>crypto.createHash('sha256').update(s).digest('hex'))));
