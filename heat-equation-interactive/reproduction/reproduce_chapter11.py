"""Recompute Chapter 11 V3.3 data. Python 3 with NumPy and Numba.
Usage: python reproduce_chapter11.py [output.json]
The original finite-box settings follow revised thesis Ch. 9; benchmark and domain runs are supplementary.
"""
import numpy as np, json, math
from numba import njit
from pathlib import Path
import sys
OUTPUT=Path(sys.argv[1]) if len(sys.argv)>1 else Path("numerical_investigations_v3_3.json")
@njit(cache=True)
def solve(h,dt,T,lam,eps,p,R=2.):
 n=round(2*R/h)+1; nz=round(R/h)+1; steps=round(T/dt); dt=T/steps
 a=np.zeros((n,n,nz)); b=a.copy(); f=dt/h**2
 for i in range(1,n-1):
  for j in range(1,n-1):
   for k in range(nz-1): a[i,j,k]=math.exp(-((i*h-R-.15)**2+(j*h-R)**2)/.5**2-(k*h-.45)**2/.35**2)
 rec=np.empty((21,5)); sl=np.zeros((21,3,n,n)); times=np.empty(21); pos=0
 for step in range(steps+1):
  t=step*dt; center=0. if p==0 else .42*(t/T)**p
  if step==round(pos*steps/20):
   m=0.; l2=0.; full=0.; peak=0.; bp=0.
   for i in range(n):
    for j in range(n):
     for k in range(nz):
      q=a[i,j,k]; w=.5 if k==0 else 1.; m+=w*q; l2+=w*q*q;full+=q;peak=max(peak,q)
      if k==0: bp=max(bp,q)
   rec[pos]=np.array([m*h**3,l2*h**3,peak,full*h**3,bp]); times[pos]=t
   sl[pos,0,:,:]=a[:,:,0]; sl[pos,1,:,:nz]=a[:,n//2,:];sl[pos,2,:,:nz]=a[n//2,:,:];pos+=1
  if step==steps: break
  for i in range(1,n-1):
   for j in range(1,n-1):
    V=lam/math.sqrt((i*h-R-center)**2+(j*h-R)**2+eps**2)
    b[i,j,0]=(1-6*f+2*dt*V/h)*a[i,j,0]+f*(a[i-1,j,0]+a[i+1,j,0]+a[i,j-1,0]+a[i,j+1,0]+2*a[i,j,1])
    for k in range(1,nz-1): b[i,j,k]=(1-6*f)*a[i,j,k]+f*(a[i-1,j,k]+a[i+1,j,k]+a[i,j-1,k]+a[i,j+1,k]+a[i,j,k-1]+a[i,j,k+1])
  a,b=b,a
 return times,rec,sl,a

def package(t,r,s): return {'t':t.tolist(),'d':r.tolist(),'s':np.round(s,7).tolist()}
if __name__=='__main__':
 T=.28; lc=2*(math.gamma(.75)/math.gamma(.25))**2
 data={'lambda3':lc,'original':{},'sensitivity':[],'trajectory':[],'refine':[],'domain':[]}
 for name,p in [('Fixed',0.),('Moving',1.)]:
  t,r,s,a=solve(.1,.0007,T,.55,.2,p);data['original'][name]=package(t,r,s);print(name,r[-1],flush=True)
 for ratio in [.5,1,2]:
  for eps in [.2,.1]:
   t,r,_,_=solve(.1,.0007,T,ratio*lc,eps,1.);data['sensitivity'].append({'label':f'{ratio:g} λ₃, ε={eps:g}','t':t.tolist(),'d':r.tolist()})
 for p in [0.,1.,.75,.5,.3]:
  t,r,_,_=solve(.1,.0007,T,lc,.2,p);data['trajectory'].append({'label':'Fixed' if p==0 else f'p={p:g}','t':t.tolist(),'d':r.tolist()})
 for h,dt in [(.2,.0007),(.1,.0007),(.1,.00035),(.05,.000175)]:
  t,r,_,_=solve(h,dt,T,lc,.2,1.);data['refine'].append({'label':f'h={h:g}, Δt={dt:g}','h':h,'dt':dt,'t':t.tolist(),'d':r.tolist()});print('refine',h,dt,r[-1],flush=True)
 for R in [1.,2.,3.]:
  t,r,_,a=solve(.1,.0007,T,.55,.2,1.,R);data['domain'].append({'label':f'R={R:g}','t':t.tolist(),'d':r.tolist(),'probe':float(a[round((R+.4)/.1),round(R/.1),1])});print('domain',R,r[-1],flush=True)
 OUTPUT.write_text(json.dumps(data,separators=(',',':')))

 b=.7;T=.28;R=2
 exact=lambda z,t: np.exp(b*b*t-b*z)
 def run(h,dt):
  z=np.linspace(0,R,round(R/h)+1);u=exact(z,0);n=round(T/dt);dt=T/n;F=dt/h**2
  for k in range(n):
   v=u.copy();v[1:-1]=u[1:-1]+F*(u[2:]+u[:-2]-2*u[1:-1]);v[0]=u[0]+2*F*(u[1]-u[0])+2*dt*b/h*u[0];v[-1]=exact(R,(k+1)*dt);u=v
  return z,u,float(np.max(np.abs(u-exact(z,T))))
 d=json.loads(OUTPUT.read_text());d['bench']=[]
 for h,dt in [(.2,.0028),(.1,.0007),(.05,.000175),(.025,.00004375),(.1,.00035),(.1,.000175)]:
  z,u,e=run(h,dt);d['bench'].append(dict(h=h,dt=dt,z=z.tolist(),u=u.tolist(),error=e));print(h,dt,e)
 rng=np.random.default_rng(20261127);n=20000;w=rng.normal(0,math.sqrt(2*T),n);U=rng.uniform(np.finfo(float).tiny,1,n);z=np.linspace(0,R,21);res=[]
 for x in z:
  a=x;c=x+w;minimum=(a+c-np.sqrt((a-c)**2-4*T*np.log(U)))/2;L=np.maximum(0,-minimum);X=c+L;Y=np.exp(b*L-b*X);res.append([float(x),float(Y.mean()),float(Y.std(ddof=1)/np.sqrt(n)),float(exact(x,T))])
 d['matched']={'n':n,'seed':20261127,'b':b,'T':T,'values':res};OUTPUT.write_text(json.dumps(d,separators=(',',':')))
 # Supplementary V3.3 studies.
 import platform
 d['metadata']={'version':'3.3','python':platform.python_version(),'numpy':np.__version__,'seed':20261127,'dtype':'float64','T':T}
 def budget(p):
  h=.1;dt=.0007;x=np.linspace(-2,2,41);z=np.linspace(0,2,21);a=np.exp(-((x[:,None,None]-.15)**2+x[None,:,None]**2)/.25-(z[None,None,:]-.45)**2/.35**2)
  a[[0,-1],:,:]=0;a[:,[0,-1],:]=0;a[:,:,-1]=0
  weights=np.ones(21);weights[0]=.5
  def mass(a):return h**3*np.sum(a*weights)
  def norm(a):return h**3*np.sum(a*a*weights)
  rows=[]
  for k in range(400):
   V=.55/np.sqrt((x[1:-1,None]-p*1.5*k*dt)**2+x[None,1:-1]**2+.2**2)
   g=np.zeros_like(a);g[1:-1,1:-1,1:-1]=(a[2:,1:-1,1:-1]+a[:-2,1:-1,1:-1]+a[1:-1,2:,1:-1]+a[1:-1,:-2,1:-1]+a[1:-1,1:-1,2:]+a[1:-1,1:-1,:-2]-6*a[1:-1,1:-1,1:-1])/h**2
   g[1:-1,1:-1,0]=(a[2:,1:-1,0]+a[:-2,1:-1,0]+a[1:-1,2:,0]+a[1:-1,:-2,0]+2*a[1:-1,1:-1,1]-6*a[1:-1,1:-1,0])/h**2+2*V*a[1:-1,1:-1,0]/h
   J=h*h*np.sum(V*a[1:-1,1:-1,0]);loss=h*(np.sum((a[1,1:-1,:]+a[-2,1:-1,:]+a[1:-1,1,:]+a[1:-1,-2,:])*weights)+np.sum(a[1:-1,1:-1,-2]))
   E=h*(np.sum(np.diff(a,axis=0)**2*weights)+np.sum(np.diff(a,axis=1)**2*weights)+np.sum(np.diff(a,axis=2)**2)); Q=h*h*np.sum(V*a[1:-1,1:-1,0]**2); v=a+dt*g
   mr=abs((mass(v)-mass(a))/dt-(J-loss));er=abs((norm(v)-norm(a))/dt-(-2*E+2*Q+dt*norm(g)))
   rows.append([k*dt,J,loss,E,Q,dt*norm(g),mass(a),norm(a),mr,er]);a=v
  return {'rows':rows,'max_mass_residual':max(r[8] for r in rows),'max_energy_residual':max(r[9] for r in rows)}
 d['balance']={name:budget(p) for name,p in [('Fixed',0),('Moving',1)]}
 d['joint']=[];fields={}
 for eps in [.2,.1,.05]:
  for h in [.2,.1,.05]:
   dt=.07*h*h;_,r,_,a=solve(h,dt,T,lc,eps,1.);fields[eps,h]=a;d['joint'].append(dict(eps=eps,h=h,ratio=eps/h,mass=float(r[-1,0]),peak=float(r[-1,2]),boundary=float(r[-1,4])))
 for r in d['joint']:
  h,eps=r['h'],r['eps'];stride=round(h/.05);fine=fields[eps,.05][::stride,::stride,::stride];r['common_max_diff']=float(np.max(np.abs(fields[eps,h]-fine)))
 dom={}
 for R in [1.,2.,3.]:
  _,_,_,a=solve(.1,.0007,T,.55,.2,1.,R);i=round((R-.8)/.1);j=round((R+.8)/.1);dom[R]=a[i:j+1,i:j+1,:9].copy()
 d['domain_common']=[]
 for a,bx in [(1.,2.),(2.,3.)]:
  diff=dom[bx]-dom[a];w=np.ones(17);w[[0,-1]]=.5;wz=np.ones(9);wz[[0,-1]]=.5;d['domain_common'].append(dict(pair=f'{a:g} → {bx:g}',max=float(np.max(np.abs(diff))),l2=float(np.sqrt(.001*np.sum(diff**2*w[:,None,None]*w[None,:,None]*wz[None,None,:]))),min=float(diff.min()),slice=diff[:,8,:].tolist()))
 d['temporal']=[]
 for i,j in [(1,4),(4,5)]:
  a,c=d['bench'][i],d['bench'][j];d['temporal'].append(dict(dt=a['dt'],fine_dt=c['dt'],difference=float(np.max(np.abs(np.array(a['u'])-c['u'])))))
 d['spatial']=[]
 for h in [.2,.1,.05,.025]:
  z,u,e=run(h,.00004375/4);d['spatial'].append(dict(h=h,dt=.00004375/4,error=e,z=z.tolist(),u=u.tolist()))
 def m(b,z,t):
  z=np.asarray(z);return np.vectorize(math.erf)(z/(2*math.sqrt(t)))+np.exp(b*b*t-b*z)*np.vectorize(math.erfc)(z/(2*math.sqrt(t))-b*math.sqrt(t))
 b=.7;t0=.1;T=.28;n=20000;rng=np.random.default_rng(20261128);Z=rng.normal(0,math.sqrt(2*T),n);U=rng.uniform(np.finfo(float).tiny,1,n)
 z=np.linspace(0,2,21);u=m(b,z,t0);dt=.0007;F=dt/.01
 for k in range(400):
  v=u.copy();v[1:-1]=u[1:-1]+F*(u[2:]+u[:-2]-2*u[1:-1]);v[0]=u[0]+2*F*(u[1]-u[0])+2*dt*b/.1*u[0];v[-1]=m(b,2,t0+(k+1)*dt);u=v
 rows=[]
 for i,x in enumerate(z):
  end=x+Z;minimum=(x+end-np.sqrt((x-end)**2-4*T*np.log(U)))/2;L=np.maximum(0,-minimum);X=end+L;Y=np.exp(b*L)*m(b,X,t0);Y1=np.exp(b*L);var=float(m(2*b,x,T)-m(b,x,T)**2)
  rows.append([float(x),float(m(b,x,t0+T)),float(u[i]),float(Y.mean()),float(Y.std(ddof=1)/np.sqrt(n)),float(Y1.mean()),float(m(b,x,T)),float(np.sqrt(max(0,var)/n))])
 d['localtime']={'n':n,'seed':20261128,'b':b,'t0':t0,'T':T,'rows':rows}
 for r in d['matched']['values']:r.append(float(r[3]*math.sqrt(math.expm1(2*b*b*T)/n)))
 OUTPUT.write_text(json.dumps(d,separators=(',',':')),encoding='utf-8')
 print('balance residuals',[(k,v['max_mass_residual'],v['max_energy_residual']) for k,v in d['balance'].items()]);print('domain',[(r['pair'],r['max'],r['l2']) for r in d['domain_common']]);print('local time',rows[0]);print('wrote',OUTPUT)
