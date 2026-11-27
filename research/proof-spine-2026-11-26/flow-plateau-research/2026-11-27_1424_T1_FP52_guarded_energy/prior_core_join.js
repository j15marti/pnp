function priorCoreJoin(F,previous,projected,E){
 const S=new Set(previous.expected),Fs=F.filter((f,i)=>S.has(i)||!f.cost.includes(2));const proof=E.proofSearch(E.asCNF(Fs).clauses,100000);if(proof.status!=="UNSAT")return {proof,status:"UNKNOWN"};
 const check=E.checkTree(Fs,proof.tree,500000);const candidates=projected.globalCandidates.filter(i=>S.has(i));return {status:"VERIFIED",priorCandidates:S.size,coreFactorCount:Fs.length,priorCoreOwners:Fs.flatMap(f=>f.ids).sort((a,b)=>a-b),priorCoreProof:proof,independentCheck:check,newCandidates:candidates,globalCandidateCount:candidates.length,afterGuardProjection:projected.globalCandidates.length};
}
module.exports={priorCoreJoin};
