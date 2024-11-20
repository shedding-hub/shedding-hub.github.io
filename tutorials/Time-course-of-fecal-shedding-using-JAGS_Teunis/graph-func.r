v0 <- function(ap,gp)
    return(((ap+gp)/gp)*((ap+gp)/ap)^(ap/gp));

logvir <- function(tm,ap,gp,cp,dp)
    return(cp+dp*log(exp(-ap*tm)*(1-exp(-gp*tm))*v0(ap,gp)));

quant.resp <- function(k.subj,time,t_offs,c_offs){
  t <-  time;
  if(t_offs) t <- time - offs.shed[k.subj,];
  tmp <- logvir(t,alpha[k.subj,],gamma[k.subj,],c[k.subj,],d[k.subj,]);
  if(c_offs) tmp <- tmp + c.offs;
  tmp <- as.numeric(na.omit(tmp));
  return(quantile(tmp,probs=c(0.025,0.5,0.975),na.rm=TRUE));
}

quant.subset <- function(subj.list,time,t_offs,c_offs){
  tmp <- array(NA,dim=c(length(subj.list),nmc));
  for(k.subj in 1:length(subj.list)){
    t <- time;
    if(t_offs) t <- time - offs.shed[subj.list[k.subj],];
    tmp[k.subj,] <- logvir(t,alpha[subj.list[k.subj],],gamma[subj.list[k.subj],],
                        c[subj.list[k.subj],],d[subj.list[k.subj],]);
    if(c_offs) tmp[k.subj,] <- tmp[k.subj,] + c.offs;
  }
  tmp <- as.numeric(na.omit(c(tmp)));
  return(quantile(tmp,probs=c(0.025,0.5,0.975),na.rm=TRUE));
}

graph.resp <- function(xrng,k.subj,color){
 x <- seq(from=xrng[1],to=xrng[2],by=0.01);
 y <- array(NA,dim=c(length(x),3));
 for(k in 1:length(x)){
  y[k,] <- log10(exp(quant.resp(k.subj,x[k],FALSE,FALSE)));
 }
 lines(x,y[,1],col=color,lty=2);
 lines(x,y[,2],col=color,lty=1);
 lines(x,y[,3],col=color,lty=2);
}

graph.subset <- function(xrng,subj.list,color,ltyp=1){
 x <- seq(from=xrng[1],to=xrng[2],by=0.01);
 y <- array(NA,dim=c(length(x),3));
 for(k in 1:length(x)){
  y[k,] <- log10(exp(quant.subset(subj.list,x[k],FALSE,FALSE)));
 }
 lines(x,y[,1],col=color,lty=ltyp);
 lines(x,y[,2],col=color,lty=ltyp);
 lines(x,y[,3],col=color,lty=ltyp);
}

graph.obs <- function(k.subj,colr="black"){
 cn <- log10(exp(logv.obs[k.subj,]));
 for(k.obs in 1:nobs[k.subj]){
   if(is.na(logv.obs[k.subj,k.obs]))
     cn[k.obs] <- log10(exp(logv.init[k.subj,k.obs]));
 }
 points(t.obs[k.subj,]-mean(offs.shed[k.subj,]),cn,cex=1.5,col=colr,pch=16);
 lines(t.obs[k.subj,]-mean(offs.shed[k.subj,]),cn,col=colr);
}
