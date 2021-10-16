"""
Animate "Exponential Beats All"
"""

from picturebox import *
from kwanmath.interp import linterp,trap
from collections.abc import Iterable
import numpy as np
from manim import *
import os

class LHopitalsRule(Scene):
    def construct(self):
        self.camera.background_color='#e0e0ff'
        formula1=MathTex(r"\lim_{x\rightarrow \infty}\frac{f(x)}{g(x)}=\frac{f'(x)}{g'(x)}")
        formula1.set_color(BLACK)
        formula2=MathTex(r"\mbox{if }\lim_{x\rightarrow \infty}f(x)=\infty")
        formula2.set_color(BLACK)
        formula3=MathTex(r"\mbox{and }\lim_{x\rightarrow \infty}g(x)=\infty")
        formula3.set_color(BLACK)
        formula1.next_to(formula2,UP)
        formula3.next_to(formula2,DOWN)
        self.play(FadeIn(formula1))
        self.play(FadeIn(formula2))
        self.play(FadeIn(formula3))
        self.play(FadeOut(formula1),
                  FadeOut(formula2),
                  FadeOut(formula3))

class PolyDerivative(Scene):
    def construct(self):
        self.camera.background_color='#e0e0ff'
        max_order=5
        x=MathTex("{{x^}}{{%d}}"%max_order)
        x.set_color(BLACK)
        self.play(FadeIn(x))
        self.wait(1)
        for i in range(max_order):
            order0=max_order-i #Polynomial order at start of transformation
            order1=order0-1    #Polynomial order at end of transformation
            #Build up coefficients -- should be from max order downto order1
            coefs="{{%d}}"%max_order
            for coef in range(max_order-1,order1-1,-1):
                coefs="{{%d}}{{\cdot}}"%coef+coefs
            ddx=MathTex(coefs+"{{x^}}{{%d}}"%order1)
            ddx.set_color(BLACK)
            self.play(TransformMatchingTex(x,ddx,path_arc=90 * DEGREES))
            self.wait(1)
            x=ddx
        self.play(FadeOut(x))

class Stage:
    w0 = 1280
    h0 = 720

    def __init__(self,w=None,h=None,f0=0,f1=100,shadow=False,facecolor='#e0e0ff'):
        self.actors=[]
        self.w=Stage.w0 if w is None else w
        self.h=Stage.h0 if h is None else h
        self.f0=f0
        self.f1=f1
        self.shadow=shadow
        self.facecolor=facecolor
    def setup(self,pb:PictureBox):
        pass
    def teardown(self,pb:PictureBox):
        pass
    def perform(self):
        digits=len(str(self.f1))
        oufn_pat=f"media/images/{os.path.basename(__file__)[:-3]}/{type(self).__name__}_%0{digits}d.png"
        with PictureBox(self.w,self.h,title=type(self).__name__,facecolor=self.facecolor) as pb:
            self.setup(pb)
            perform(pb,self.actors,self.f0,self.f1,shadow=self.shadow,oufn_pat=oufn_pat)
            self.teardown(pb)

class cpl:
    """
    Continuous Piecewise Linear function
    """
    def __init__(self,ys):
        """

        :param ys: Table of y values. Each value is the value of the
                   function at the beginning of the corresponding phase.
                   Must have at least one more value than intended phases.
        """
        self.ys=ys
    def __call__(self,phase,t):
        if phase<0:
            phase=len(self.ys)+phase-1
        return linterp(0,self.ys[phase],1,self.ys[phase+1],t)


class Ticks(EnterActor):
    def _enter(self,pb:PictureBox,tt:float,alpha:float=1.0,shadow:bool=False,
             u0:float=None,u1:float=None,du:float=1.0,
             px0:float=None,dx0:float=None,px1:float=None,dx1:float=None,tx0:float=None,tx1:float=None,
             py0:float=None,dy0:float=None,py1:float=None,dy1:float=None,ty0:float=None,ty1:float=None,
             lx:float=None,ly:float=None,lfmt:str=None,
             **kwargs)->None:
        """
        Draw a series of evenly spaced ticks along a straight line

        :param pb: PictureBox to draw on
        :param tt: Time parameter in this phase
        :param alpha: Transparency
        :param shadow: True if on the shadow pass
        :param u0: lowest numbered tick
        :param u1: highest numbered tick
        :param du: spacing between ticks in data space
        :param px0: Pixel horizontal coordinate of one end of the line
        :param dx0: Data horizontal coordinate of one end of the line
        :param px1: Pixel horizontal coordinate of the other end of the line
        :param dx1: Data horizontal coordinate of the other end of the line
        :param tx0: Horizontal Offset of one end of each tick in pixels from its spot
        :param tx1: Horizontal Offset of the other end of each tick in pixels from its spot
        :param py0: Pixel vertical coordinate of one end of the line
        :param dy0: Data vertical coordinate of one end of the line
        :param py1: Pixel vertical coordinate of the other end of the line
        :param dy1: Data vertical coordinate of the other end of the line
        :param ty0: Vertical offset of one end of each tick in pixels from its spot
        :param ty1: Vertical offset of the other end of each tick in pixels from its spot
        :param lx: if non-None, print numerical labels at each tick, offset this many pixels horizontally
        :param ly: if non-None, print numerical labels at each tick, offset this many pixels vertically
        :param fmt: If non-None, format the tick number with this % string
        :param kwargs: Passed to pb.line
        """
        if shadow:
            return
        if alpha==0:
            return
        for u in np.arange(u0,u1+0.00001,du):
            if linterp(u0,0,u1,1,u)>tt:
                continue
            #Data coordinates of tick
            dx=linterp(u0,dx0,u1,dx1,u)
            dy=linterp(u0,dy0,u1,dy1,u)
            #Pixel coordinates of tick
            px=px0 if px0==px1 else linterp(dx0,px0,dx1,px1,dx)
            py=py0 if py0==py1 else linterp(dy0,py0,dy1,py1,dy)
            if tx0 is not None:
                #Draw the line
                pb.line(px+tx0,py+ty0,px+tx1,py+ty1,alpha=alpha,**kwargs)
            if lx is not None:
                #Print the label
                pb.text(px+lx,py+ly,lfmt%u,alpha=alpha,**kwargs)

def LabeledAxis(ts:Iterable[float]=None,
                ticklen:float=20,size:float=15,color='k',alpha=1.0,
                px0:float=None,dx0:float=None,px1:float=None,dx1:float=None,dux:float=1.0,
                py0:float=None,dy0:float=None,py1:float=None,dy1:float=None,duy:float=1.0,
                lfmtx:str='%.0f',lfmty:str='%.0f'):
    denter = ts[1] - ts[0]
    return [
        Axis(x0=px0, x1=px1, y0=py1, y1=py0, color='k', ts=ts, alpha=alpha),
        # X axis ticks
        Ticks(ts=[ts[0]+denter*(1/6+1/3),ts[0]+denter*(1/6+3/3)]+ts[2:],
              u0=dx0, u1=dx1, du=dux,
              px0=px0, dx0=dx0, px1=px1, dx1=dx1, tx0=0, tx1=0,
              py0=py0, dy0=dy0, py1=py0, dy1=dy0, ty0=0, ty1=ticklen,
              color=color,alpha=alpha),
        Ticks(ts=[ts[0]+denter*(1/6+1/3),ts[0]+denter*(1/6+3/3)]+ts[2:],
                  u0=dx0, u1=dx1, du=dux,
                  px0=px0, dx0=dx0, px1=px1, dx1=dx1,
                  py0=py0, dy0=dy0, py1=py0, dy1=dy0,
                  lx=-3, ly=ticklen, size=size, lfmt=lfmtx, ha='right', va='baseline',
                  color=color,alpha=alpha),
        # Y axis ticks
        Ticks(ts=[ts[0]+denter*(1/6+0/3),ts[0]+denter*(1/6+2/3)]+ts[2:],
                   u0=dy0, u1=dy1, du=duy,
                   px0=px0, dx0=dx0, px1=px0, dx1=dx0, tx0=-ticklen, tx1=0,
                   py0=py0, dy0=dy0, py1=py1, dy1=dy1, ty0=0, ty1=0,
                   color=color,alpha=alpha),
        Ticks(ts=[ts[0]+denter*(1/6+0/3),ts[0]+denter*(1/6+2/3)]+ts[2:],
                   u0=dy0, u1=dy1, du=duy,
                   px0=px0, dx0=dx0, px1=px0, dx1=dx0,
                   py0=py0, dy0=dy0, py1=py1, dy1=dy1,
                   lx=-3, ly=ticklen, size=size, lfmt=lfmty, ha='right', va='baseline',
                   color=color,alpha=alpha)
    ]


def main():
    f=lambda x:x**2
    g=lambda x:np.exp(x)

    dx0=0
    dx1=5
    dy0=0
    dy1=np.ceil((f(dx1) if f(dx1)>g(dx1) else g(dx1))/25)*25
    px0=100
    px1=Stage.w0-100
    py0=Stage.h0-100
    py1=100
    if True:  #Fade in the competitors, f(x)=x**2 and g(x)=exp(x)
        class IntroduceFormulas(Stage):
            def __init__(self):
                super().__init__(f0=0,f1=100)
                self.actors.append(Text(ts=[0,30,100,100],x=300,y=300,size=30,s='$f(x)=x^2$',color='r',usetex=True))
                self.actors.append(Text(ts=[30,60,100,100],x=300,y=400,size=30,s='$g(x)=e^x$',color='b',usetex=True))
        IntroduceFormulas().perform()
    if True:  #Draw the formulas, and the curves.
        class IntroduceCurves(Stage):
            def __init__(self):
                super().__init__(f0=0,f1=100)
                self.actors.append(Text(ts=[0,0,100,100],x=300,y=300,size=30,s='$f(x)=x^2$',color='r',usetex=True))
                self.actors.append(Text(ts=[0,0,100,100],x=300,y=400,size=30,s='$g(x)=e^x$',color='b',usetex=True))
                self.actors=self.actors+LabeledAxis(ts=[0,30,100,100],
                                          px0=px0,dx0=dx0,px1=px1,dx1=dx1,dux=1,
                                          py0=py0,dy0=dy0,py1=py1,dy1=dy1,duy=25)
                self.actors.append(Function(ts=[20,70,100,100],px0=100,px1=self.w-100,dx0=dx0,dx1=dx1,py0=self.h-100,py1=100,dy0=dy0,dy1=dy1,f=lambda phase,tt:lambda x:f(x),color='r'))
                self.actors.append(Function(ts=[40,90,100,100],px0=100,px1=self.w-100,dx0=dx0,dx1=dx1,py0=self.h-100,py1=100,dy0=dy0,dy1=dy1,f=lambda phase,tt:lambda x:g(x),color='b'))
        IntroduceCurves().perform()
    if True: #Crank up the exponent on the x curve
        class CrankExponent(Stage):
            def __init__(self):
                super().__init__(f0=0,f1=100)
                self.actors.append(Text(ts=[0,0,100,100],x=300,y=300,size=30,s=lambda phase,t:'$f(x)=x^{'+"%.2f"%(2 if phase==0 else linterp(0,2,1,5,t) if phase==1 else 5)+"}$",color='r',usetex=True))
                self.actors.append(Text(ts=[0,0,100,100],x=300,y=400,size=30,s='$g(x)=e^x$',color='b',usetex=True))
                self.actors=self.actors+LabeledAxis(ts=[0,0,100,100],
                                          px0=px0,dx0=dx0,px1=px1,dx1=dx1,dux=1,
                                          py0=py0,dy0=dy0,py1=py1,dy1=dy1,duy=25)
                self.actors.append(Function(ts=[0,0,100,100],px0=100,px1=self.w-100,dx0=dx0,dx1=dx1,py0=self.h-100,py1=100,dy0=dy0,dy1=dy1,f=lambda phase,tt:lambda x: x**linterp(0,2,1,5,tt),color='r'))
                self.actors.append(Function(ts=[0,0,100,100],px0=100,px1=self.w-100,dx0=dx0,dx1=dx1,py0=self.h-100,py1=100,dy0=dy0,dy1=dy1,f=lambda phase,tt:lambda x: g(x),color='b'))
        CrankExponent().perform()
    dy1a=dy1
    dy1b=400000
    dy1=lambda phase,tt:np.exp(linterp(0,np.log(dy1a),1,np.log(dy1b),tt))
    if True:
        class VertScale(Stage):
            def __init__(self):
                super().__init__(f0=0,f1=100)
                self.actors.append(Text(ts=[0,0,100,100],x=300,y=300,size=30,s='$f(x)=x^5$',color='r',usetex=True))
                self.actors.append(Text(ts=[0,0,100,100],x=300,y=400,size=30,s='$g(x)=e^x$',color='b',usetex=True))
                self.actors=self.actors+LabeledAxis(ts=[0,0,100,100],
                                          px0=px0,dx0=dx0,px1=px1,dx1=dx1,dux=1,
                                          py0=py0,dy0=dy0,py1=py1,dy1=dy1,duy=25,alpha=lambda phase,tt:1 if phase==0 else 0 if phase==-1 else linterp(0,1,0.2,0,tt,bound=True) )
                self.actors=self.actors+LabeledAxis(ts=[0,0,100,100],
                                          px0=px0,dx0=dx0,px1=px1,dx1=dx1,dux=1,
                                          py0=py0,dy0=dy0,py1=py1,dy1=dy1,duy=dy1b+1,alpha=lambda phase,tt:0 if phase==0 else 0 if phase==-1 else trap(0,0.2,0.8,1,0,1,tt) )
                self.actors=self.actors+LabeledAxis(ts=[0,0,100,100],
                                          px0=px0,dx0=dx0,px1=px1,dx1=dx1,dux=1,
                                          py0=py0,dy0=dy0,py1=py1,dy1=dy1,duy=5e4,lfmty='%.1e',alpha=lambda phase,tt:0 if phase==0 else 0 if phase==-1 else linterp(0.8,0,1,1,tt,bound=True) )
                self.actors.append(Function(ts=[0,0,100,100],px0=100,px1=self.w-100,dx0=dx0,dx1=dx1,py0=self.h-100,py1=100,dy0=dy0,dy1=dy1,f=lambda phase,tt:lambda x: x**5,color='r'))
                self.actors.append(Function(ts=[0,0,100,100],px0=100,px1=self.w-100,dx0=dx0,dx1=dx1,py0=self.h-100,py1=100,dy0=dy0,dy1=dy1,f=lambda phase,tt:lambda x: g(x),color='b'))
        VertScale().perform()
    dy1=dy1b
    dx1a=dx1
    dx1b=13
    dx1=lambda phase, tt: linterp(0, dx1a, 1, dx1b, tt)
    if True:
        class HorizScale(Stage):
            def __init__(self):
                super().__init__(f0=0,f1=100)
                self.actors.append(Text(ts=[0,0,100,100],x=300,y=300,size=30,s='$f(x)=x^5$',color='r',usetex=True))
                self.actors.append(Text(ts=[0,0,100,100],x=300,y=400,size=30,s='$g(x)=e^x$',color='b',usetex=True))
                self.actors=self.actors+LabeledAxis(ts=[0,0,100,100],
                                          px0=px0,dx0=dx0,px1=px1,dx1=dx1,dux=1,
                                          py0=py0,dy0=dy0,py1=py1,dy1=dy1,duy=5e4,lfmty='%.1e')
                self.actors.append(Function(ts=[0,0,100,100],px0=100,px1=self.w-100,dx0=dx0,dx1=dx1,py0=self.h-100,py1=100,dy0=dy0,dy1=dy1,f=lambda phase,tt:lambda x: x**5,color='r'))
                self.actors.append(Function(ts=[0,0,100,100],px0=100,px1=self.w-100,dx0=dx0,dx1=dx1,py0=self.h-100,py1=100,dy0=dy0,dy1=dy1,f=lambda phase,tt:lambda x: g(x),color='b'))
        HorizScale().perform()
    dx1=13
    if True:
        class FadeCurves(Stage):
            def __init__(self):
                super().__init__(f0=0,f1=30)
                self.actors.append(Text(ts=[0,0,0,30],x=300,y=300,size=30,s='$f(x)=x^5$',color='r',usetex=True))
                self.actors.append(Text(ts=[0,0,0,30],x=300,y=400,size=30,s='$g(x)=e^x$',color='b',usetex=True))
                self.actors=self.actors+LabeledAxis(ts=[0,0,0,30],
                                          px0=px0,dx0=dx0,px1=px1,dx1=dx1,dux=1,
                                          py0=py0,dy0=dy0,py1=py1,dy1=dy1,duy=5e4,lfmty='%.1e')
                self.actors.append(Function(ts=[0,0,0,30],px0=100,px1=self.w-100,dx0=dx0,dx1=dx1,py0=self.h-100,py1=100,dy0=dy0,dy1=dy1,f=lambda phase,tt:lambda x: x**5,color='r'))
                self.actors.append(Function(ts=[0,0,0,30],px0=100,px1=self.w-100,dx0=dx0,dx1=dx1,py0=self.h-100,py1=100,dy0=dy0,dy1=dy1,f=lambda phase,tt:lambda x: g(x),color='b'))
        FadeCurves().perform()
    if True:
        class DrawTable(Stage):
            def __init__(self):
                super().__init__(f0=0,f1=100)
                self.actors.append(TableGrid  (ts=[0,30,100,130],x0=50,x1=570,yt=80,y0=102,yb=self.h-60,xs=[105,205,415],color='k'))
                self.actors.append(TableColumn(ts=[0,30,100,130],header="Time"     ,data=np.arange(37),x=100,y0=100,dy=15,horizontalalignment='right',color='k'))
                self.actors.append(TableColumn(ts=[15,45,100,130],header="$f(x)=x^5$" ,data=np.arange(37)**5,x=200,y0=100,dy=15,horizontalalignment='right',color='r'))
                self.actors.append(TableColumn(ts=[30,60,100,130],header="$g(x)=e^x$",data=np.round(np.exp(np.arange(37))),x=410,y0=100,dy=15,horizontalalignment='right',color='b'))
                self.actors.append(TableColumn(ts=[45,75,100,130],header="$f(x)/g(x)=x^5/e^x$",data=np.floor(1000*(np.arange(37)**5/np.exp(np.arange(37))))/1000,x=560,y0=100,dy=15,horizontalalignment='right',color='#8000ff'))
            def setup(self,pb:PictureBox):
                pb.translate(400,0)
            def teardown(self,pb:PictureBox):
                pb.resetM()
        DrawTable().perform()


if __name__ == "__main__":
    main()