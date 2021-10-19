"""
Some of the shots are in manim. Maybe eventually all of the shots will be.
"""

from manim import *

background="#e0e0ff"

class LHopitalsRule(Scene):
    def construct(self):
        def poly_result(order=5,max_order=5):
            product=max_order
            if order!=max_order:
                for coef in range(max_order-1,order,-1):
                    product*=coef
            result=(r"\infty" if order>0 else str(product))
            return result
        def poly_tex(name='f',order=5,max_order=5):
            if order==max_order:
                coefs=""
                primes=""
            else:
                coefs="{{%d}}"%max_order
                primes = "'"
                for coef in range(max_order-1,order,-1):
                    primes += "'"
                    coefs=r"{{%d}}{{\cdot}}"%coef+coefs
            tex=(r"{{"+name+r"}}"+primes+r"{{(x)}} &= "+
                 coefs+((r"{{x}}^{{%d}}"%order if order>1 else r"{{x}}") if order>0 else "")+r"\\"+
                 r" &= "+poly_result(order=order,max_order=max_order))
            return tex
        iftex=r"\lim_{x\rightarrow \infty}f(x)=\infty"
        formulaif = MathTex("{{\mbox{if } }}"+iftex, color=BLACK)
        formulaifY = MathTex(iftex, color=BLACK,tex_to_color_map={"\checkmark":"#008000"}).shift(LEFT*3.5+UP*3.5)
        position_list=reversed([RIGHT,RIGHT*0.5,RIGHT*0.5+DOWN,LEFT*0.5+DOWN,LEFT*0.5,LEFT,UP])
        octagonif=RegularPolygon(n=8,color=BLACK,fill_color='#cc0000',fill_opacity=1.0,stroke_width=6).rotate(22.5*DEGREES).scale(0.3).next_to(formulaifY,LEFT)
        arrowif=Polygon(*position_list,color=BLACK,fill_color="#00cc00",fill_opacity=1.0).scale(0.3).rotate(-90*DEGREES).next_to(formulaifY,LEFT)
        andtex=r"\lim_{x\rightarrow \infty}g(x)=\infty"
        formulaand = MathTex("{{\mbox{and } }}"+andtex, color=BLACK)
        formulaandY = MathTex(andtex, color=BLACK,tex_to_color_map={"\checkmark":"#008000"}).shift(LEFT*3.5+DOWN*0.5)
        position_list=reversed([RIGHT,RIGHT*0.5,RIGHT*0.5+DOWN,LEFT*0.5+DOWN,LEFT*0.5,LEFT,UP])
        octagonand=RegularPolygon(n=8,color=BLACK,fill_color='#cc0000',fill_opacity=1.0,stroke_width=6).rotate(22.5*DEGREES).scale(0.3).next_to(formulaandY,LEFT)
        arrowand=Polygon(*position_list,color=BLACK,fill_color="#00cc00",fill_opacity=1.0).scale(0.3).rotate(-90*DEGREES).next_to(formulaandY,LEFT)
        formulathen = MathTex(r"\mbox{then }\lim_{x\rightarrow \infty}{ f(x)\over g(x) }", r"={ f'(x) \over g'(x) }", color=BLACK)
        self.camera.background_color=background
        formulaif.next_to(formulaand,UP)
        formulathen.next_to(formulaand,DOWN)
        self.play(FadeIn(formulaif))
        self.play(FadeIn(formulaand))
        self.play(FadeIn(formulathen))
        self.wait()
        self.camera.background_color=background
        self.play(TransformMatchingTex(formulaif,formulaifY),
                  TransformMatchingTex(formulaand,formulaandY),
                  FadeIn(arrowif),FadeIn(arrowand),
                  FadeOut(formulathen))
        self.wait(0.5)
        vline=Line(start=UP*4,end=DOWN*4,color=BLACK)
        hline1=Line(start=ORIGIN,end=LEFT*7,color=BLACK)
        self.play(Create(vline,run_time=0.5))
        self.play(Create(hline1,run_time=0.5))
        self.wait()
        lh=MathTex(r'\frac{f(x)}{g(x)}&=\frac{'+poly_result(4,4)+"}{"+poly_result(5,5)+r"}\\&=???",color=BLACK).shift(RIGHT*3.5)
        fx=MathTex(poly_tex('f',4,max_order=4),color=BLACK).shift(UP*2+LEFT*3.5)
        gx=MathTex(poly_tex('g',5,max_order=5),color=BLACK).shift(DOWN*2+LEFT*3.5)
        signf=arrowif
        signg=arrowand
        self.play(FadeIn(fx),FadeIn(gx),FadeIn(lh))
        self.wait(1)
        dfx = MathTex(poly_tex('f', 3, max_order=4), color=BLACK).next_to(fx,ORIGIN)
        self.play(TransformMatchingTex(fx, dfx, path_arc=90 * DEGREES))
        self.wait(1)
        fx=dfx
        dgx = MathTex(poly_tex('g', 4, max_order=5), color=BLACK).next_to(gx,ORIGIN)
        self.play(TransformMatchingTex(gx, dgx, path_arc=90 * DEGREES))
        self.wait(1)
        gx=dgx

        for i in range(2,4+1):
            dfx=MathTex(poly_tex('f',4-i,max_order=4),color=BLACK).next_to(fx,ORIGIN)
            dgx=MathTex(poly_tex('g',5-i,max_order=5),color=BLACK).next_to(gx,ORIGIN)
            result4=poly_result(4-i, 4)
            dsignf=arrowif if result4=="\infty" else octagonif
            result5=poly_result(5-i, 5)
            dsigng=arrowand if result5=="\infty" else octagonand
            dlh = MathTex(
                r'\frac{f(x)}{g(x)}&=\frac{' + result4 + "}{" + result5 + r"}\\&="+("???" if i<4 else "0"),color=BLACK).next_to(lh,ORIGIN)
            self.play(TransformMatchingTex(fx,dfx,path_arc=90 * DEGREES),
                      TransformMatchingTex(gx,dgx,path_arc=90 * DEGREES),
                      FadeOut(lh),FadeIn(dlh),
                      FadeOut(signf),FadeIn(dsignf),
                      FadeOut(signg),FadeIn(dsigng))
            fx=dfx
            gx=dgx
            signf=dsignf
            signg=dsigng
            lh=dlh
        self.wait(1)



class Title(Scene):
    def construct(self):
        self.camera.background_color = background
        text = Text("Exponential Beats All", font_size=48, font="Decker")
        text.set_color('#1a5fb4')
        text.shift(UP + LEFT)
        subtitle = Text("(polynomials)", font_size=32, font="Decker")
        subtitle.next_to(text, DOWN)
        subtitle.set_color('#1a5fb4')

        axes = Axes(x_range=[0, 20, 1], y_range=[0, 500, 100])
        x2 = axes.get_graph(lambda x: (x / 2) ** 2, color='#800000')
        x3 = axes.get_graph(lambda x: (x / 3) ** 3, color='#C00000')
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
        thinktwice=SVGMobject("clipart/ThinkTwice.svg").next_to(kwanlogo,LEFT)
        python=SVGMobject("clipart/python.svg").next_to(kwanlogo,RIGHT)
        self.play(Write(kwanlogo))
        self.wait(1)
        self.play(Write(thinktwice))
        self.wait(1)
        self.play(Write(python))
        self.wait(1)
        logo_green = "#87c2a5"
        logo_blue = "#525893"
        logo_red = "#e07a5f"
        logo_black = "#343434"
        ds_m = MathTex(r"\mathbb{M}", fill_color=logo_black).scale(7)
        ds_m.shift(2.25 * LEFT + 1.5 * UP)
        circle = Circle(color=logo_green, fill_opacity=1).shift(LEFT)
        square = Square(color=logo_blue, fill_opacity=1).shift(UP)
        triangle = Triangle(color=logo_red, fill_opacity=1).shift(RIGHT)
        logo = VGroup(triangle, square, circle, ds_m)  # order matters
        logo.scale(0.4).next_to(kwanlogo,DOWN)
        self.play(Create(logo))