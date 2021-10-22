"""
Some of the shots are in manim. Maybe eventually all of the shots will be.
"""

from manim import *
import numpy as np
from poly import *

background="#e0e0ff"
eqn_color='#1a5fb4'




stop = RegularPolygon(n=8, color=BLACK, fill_color='#cc0000', fill_opacity=1.0, stroke_width=6).rotate(
    22.5 * DEGREES).scale(0.3)
go_points = reversed([RIGHT, RIGHT * 0.5, RIGHT * 0.5 + DOWN, LEFT * 0.5 + DOWN, LEFT * 0.5, LEFT, UP])
go = Polygon(*go_points, color=BLACK, fill_color="#00cc00", fill_opacity=1.0).scale(0.3).rotate(-90 * DEGREES)

formulaif = MathTex(r"\mbox{if }\lim_{x\rightarrow \infty}f(x)=\infty", color=eqn_color)
formulaand = MathTex(r"\mbox{and }\lim_{x\rightarrow \infty}g(x)=\infty", color=eqn_color)
formulathen = MathTex(r"\mbox{then }\lim_{x\rightarrow \infty}{ f(x)\over g(x) }", r"={ f'(x) \over g'(x) }",
                      color=eqn_color)
formulaif.next_to(formulaand, UP)
formulathen.next_to(formulaand, DOWN)

class LHopitalsRule(Scene):
    def construct(self):
        self.camera.background_color=background
        self.play(FadeIn(formulaif))
        self.play(FadeIn(formulaand))
        self.play(FadeIn(formulathen))
        self.wait()
        self.play(FadeOut(formulaif),
                  FadeOut(formulaand),
                  FadeOut(formulathen))
        self.wait(0.5)
        vline=Line(start=UP*4,end=DOWN*4,color=eqn_color)
        hline1=Line(start=ORIGIN,end=LEFT*8,color=eqn_color)
        self.play(Create(vline,run_time=0.5))
        self.play(Create(hline1,run_time=0.5))
        self.wait()
        lh=MathTex(r'\frac{f(x)}{g(x)}&=\frac{'+poly_result(4,4)+"}{"+poly_result(5,5)+r"}\\&=???",color=eqn_color).shift(RIGHT*3.5)
        fx=MathTex(lhpoly_tex('f', 4, d=0), color=eqn_color).shift(UP * 2 + LEFT * 3.5)
        gx=MathTex(lhpoly_tex('g', 5, d=0), color=eqn_color).shift(DOWN * 2 + LEFT * 3.5)
        fsign=go.copy().next_to(fx,RIGHT)
        gsign=go.copy().next_to(gx,RIGHT)
        self.play(FadeIn(fx),FadeIn(gx),FadeIn(lh),FadeIn(fsign),FadeIn(gsign))
        self.wait(1)
        dfx = MathTex(lhpoly_tex('f', 4, d=1), color=eqn_color).next_to(fx, ORIGIN)
        self.play(TransformMatchingTex(fx, dfx, path_arc=90 * DEGREES))
        self.wait(1)
        fx=dfx
        dgx = MathTex(lhpoly_tex('g', 5, d=1), color=eqn_color).next_to(gx, ORIGIN)
        self.play(TransformMatchingTex(gx, dgx, path_arc=90 * DEGREES))
        self.wait(1)
        gx=dgx

        #Do the rest of the derivatives simultaneously. Also update result.
        for d in range(2,4+1):
            dfx=MathTex(lhpoly_tex('f', 4, d=d), color=eqn_color).next_to(fx, ORIGIN)
            dgx=MathTex(lhpoly_tex('g', 5, d=d), color=eqn_color).next_to(gx, ORIGIN)
            result4=poly_result(4, d)
            dsignf=go.copy() if result4 == "\infty" else stop.copy()
            dsignf.next_to(dfx,RIGHT)
            result5=poly_result(5, d)
            dsigng=go.copy() if result5 == "\infty" else stop.copy()
            dsigng.next_to(dgx,RIGHT)
            dlh = MathTex(
                r'\frac{f(x)}{g(x)}&=\frac{' + result4 + "}{" + result5 + r"}\\&="+("???" if i<4 else "0"),color=eqn_color).next_to(lh,ORIGIN)
            self.play(TransformMatchingTex(fx,dfx,path_arc=90 * DEGREES),
                      TransformMatchingTex(gx,dgx,path_arc=90 * DEGREES),
                      FadeOut(lh),FadeIn(dlh),
                      FadeOut(fsign),FadeIn(dsignf),
                      FadeOut(gsign),FadeIn(dsigng))
            fx=dfx
            gx=dgx
            fsign=dsignf
            gsign=dsigng
            lh=dlh
        self.wait(1)

class LHopitalsFlip(Scene):
    def construct(self):
        vline=Line(start=UP*4,end=DOWN*4,color=eqn_color)
        hline1=Line(start=ORIGIN,end=LEFT*8,color=eqn_color)
        self.add(vline)
        self.add(hline1)
        lh=MathTex(r'\frac{f(x)}{g(x)}&={ {{'+poly_result(4,d=4)+"}} \over {{"+poly_result(5,d=4)+r"}} }\\&= {{0}}",color=eqn_color).shift(RIGHT*3.5)
        lh2=MathTex(r'\frac{f(x)}{g(x)}&={ {{'+poly_result(5,d=4)+"}} \over {{"+poly_result(4,d=4)+r"}} }\\&= {{\infty}}",color=eqn_color).shift(RIGHT*3.5)
        fx=MathTex(lhpoly_tex('f', 4, d=4, mark_coef=False, mark_poly=True), color=eqn_color).shift(UP * 2 + LEFT * 3.5)
        gx=MathTex(lhpoly_tex('g', 5, d=4, mark_coef=False, mark_poly=True), color=eqn_color).shift(DOWN * 2 + LEFT * 3.5)
        fsign=stop.copy().next_to(fx,RIGHT)
        gsign=go.copy().next_to(gx,RIGHT)
        self.add(lh)
        self.add(fx)
        self.add(gx)
        self.add(fsign,gsign)
        self.play(Swap(fx[4],gx[4]),
                  Swap(fx[6],gx[6]),
                  Swap(fsign,gsign))
        self.wait(1)
        self.play(Swap(lh[1],lh[3]),
                  Transform(lh[5],lh2[5]))
        self.wait(1)

class DynPresDerivation(Scene):
    def construct(self):
        self.camera.background_color=background
        q=MathTex(r'q &=w( {{ v }} )\rho( {{ h }} )\\',color=eqn_color).shift(UP*3.2)
        w=MathTex(r'w({{v}})&\propto {{v}}^2 \\',color='#ff0000').shift(UP*2+LEFT*5)
        w_axes = Axes(x_range=[0, 5.00001, 1], y_range=[0, 25.00001, 5],x_length=6,axis_config={"color":eqn_color},tips=False).shift(LEFT*3.5)
        w_plot=w_axes.get_graph(lambda x: x ** 2, color='#ff0000')
        rho=MathTex(r'\rho( {{ h }} )&\propto e^{-k {{ h }} }',color='#0000ff').shift(UP*2+RIGHT*3)
        rho_axes = Axes(x_range=[0, 5.00001, 1], y_range=[0, 25.00001, 5],x_length=6,axis_config={"color":eqn_color},tips=False).shift(RIGHT*3.5)
        rho_plot=rho_axes.get_graph(lambda x: 25*np.exp(-x), color='#0000ff')
        self.play(FadeIn(q))
        self.wait()
        self.play(AnimationGroup(FadeIn(w),Create(w_axes),Create(w_plot),lag_ratio=0.5))
        self.wait()
        self.play(AnimationGroup(FadeIn(rho),Create(rho_axes),Create(rho_plot),lag_ratio=0.5))
        self.wait()
        q2=MathTex(r'q &=w( {{ t }} )\rho( {{ t }} )\\',color=eqn_color).next_to(q,ORIGIN)
        w2=MathTex(r'w({{t}})&\propto {{t}}^2 \\',color='#ff0000').next_to(w,ORIGIN)
        rho2=MathTex(r'\rho( {{ t }} )&\propto e^{-k {{ t }} }',color='#0000ff').next_to(rho,ORIGIN)
        self.play(TransformMatchingTex(q,q2),
                  TransformMatchingTex(w, w2),
                  TransformMatchingTex(rho, rho2))
        self.wait()

class Title(Scene):
    def construct(self):
        self.camera.background_color = background
        text = Text("Exponential Beats All", font_size=48, font="Decker",color=eqn_color)
        text.shift(UP + LEFT)
        subtitle = Text("(polynomials)", font_size=32, font="Decker",color=eqn_color)
        subtitle.next_to(text, DOWN)

        axes = Axes(x_range=[0, 20, 1], y_range=[0, 500, 100])
        x2 = axes.get_graph(lambda x: (x / 2) ** 2, color='#990000')
        x3 = axes.get_graph(lambda x: (x / 3) ** 3, color='#CC0000')
        x4 = axes.get_graph(lambda x: (x / 4) ** 4, color='#FF0000')
        ex = axes.get_graph(lambda x: np.exp(x / 2) / 10, color='#0000FF')
        group = LaggedStart(Write(x2, run_time=10),
                            Write(x3, run_time=10),
                            Write(x4, run_time=10),
                            Write(ex, run_time=10),
                            Succession(AddTextLetterByLetter(text, run_time=2),Wait(run_time=8)),
                            Succession(AddTextLetterByLetter(subtitle, run_time=2),Wait(run_time=8)), lag_ratio=0.1)
        group.build_animations_with_timings()
        print(group.anims_with_timings)
        self.play(group)
        self.wait()
        self.play(*[FadeOut(x) for x in [x2, x3, x4, ex, text, subtitle]])

class ExpTaylor(Scene):
    def construct(self):
        def factorial(n):
            result=1
            for i in range(1,n+1):
                result*=i
            return result
        def taylor_term(n):
            return lambda x:x**n/factorial(n)+(0 if n==0 else taylor_term(n-1)(x))
        self.camera.background_color = background
        axes = Axes(x_range=[0, 10, 1], y_range=[0, 200, 100])
        resistor_code=[
            '#000000', #black
            '#804000', #brown
            '#ff0000', #red
            '#ff8000', #orange
            '#c0c000', #Yellow
            '#00c000', #Green
            '#0000ff', #blue
            '#8000ff', #Purple
            '#808080', #Gray
            '#ffffff', #white
        ]
        x=[axes.get_graph(taylor_term(i), color=resistor_code[i]) for i in range(8)]
        group = LaggedStart(*[Write(x[i], run_time=10) for i in range(8)],lag_ratio=0.1)
        #self.add(axes.get_graph(lambda x:np.exp(x),color='#ffffff'))
        self.play(group)
        self.play(*[FadeOut(x[i]) for i in range(8)])

class Shoutout(Scene):
    def construct(self):
        self.camera.background_color=background
        kwanlogo=SVGMobject("clipart/KwanLogo.svg")
        tb1b_logo=VGroup(
            Arc(radius=0.75,start_angle=PI,angle=3*PI/2,color="#89b2da",stroke_width=40),
            Arc(radius=0.75, start_angle=PI/2, angle=PI / 2, color="#69401a", stroke_width=40)
        ).next_to(kwanlogo,LEFT)
        thinktwice=SVGMobject("clipart/ThinkTwice.svg").next_to(kwanlogo,RIGHT)
        kdenlive=SVGMobject("clipart/Kdenlive-logo.svg").next_to(kwanlogo,UP)
        git=SVGMobject("clipart/Git-logo.svg").next_to(kwanlogo,UP+RIGHT)
        tux=SVGMobject("clipart/Tux.svg").next_to(kwanlogo,UP+LEFT)
        python=SVGMobject("clipart/python.svg").next_to(kwanlogo,DOWN)
        github=SVGMobject("clipart/Github.svg").next_to(kwanlogo,DOWN+RIGHT)
        manim_logo = VGroup(Triangle(color="#e07a5f", fill_opacity=1).shift(RIGHT),   # order matters
                            Square  (color="#525893", fill_opacity=1).shift(UP),
                            Circle  (color="#87c2a5", fill_opacity=1).shift(LEFT),
                            MathTex (r"\mathbb{M}",   fill_color="#343434").scale(7).shift(2.25 * LEFT + 1.5 * UP)).scale(0.4).next_to(kwanlogo,DOWN+LEFT)
        for logo in [kwanlogo,tb1b_logo,thinktwice,python,manim_logo,git,tux,kdenlive,github]:
            self.play(Write(logo))
            self.wait(1)

