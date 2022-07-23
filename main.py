from kivy.properties import StringProperty, BooleanProperty, Clock, NumericProperty, ListProperty
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import Screen, ScreenManager
from random import choice
from kivy.core.window import Window
from kivymd.app import MDApp

Window.clearcolor = (192 / 255, 192 / 255, 192 / 255, 192 / 255)


class Menu(Screen):
    pass


class Wiek(Screen):
    wiek_gracza = StringProperty("Wskaż swój wiek")
    pelnoletni = BooleanProperty(False)
    t = StringProperty("Grajmy!")

    def Wybor_wieku(self, widget):
        self.wiek_gracza = str(widget.value)
        if widget.value >= 18:
            self.pelnoletni = True
            self.t = "Grajmy!"
        else:
            self.pelnoletni = False
            if widget.value == 17:
                self.t = f"Nie masz wymaganego wieku. \nWróć do nas za {18 - widget.value} rok"
            elif widget.value >= 14:
                self.t = f"Nie masz wymaganego wieku. \nWróć do nas za {18 - widget.value} lata"
            else:
                self.t = f"Nie masz wymaganego wieku. \nWróć do nas za {18 - widget.value} lat"


class Imiona(Screen):
    imie1 = StringProperty("")
    s1 = BooleanProperty(False)
    imie2 = StringProperty("")
    s2 = BooleanProperty(False)

    def wpisanie_imienia1(self, widget):
        self.imie1 = widget.text
        self.s1 = True

    def wpisanie_imienia2(self, widget):
        self.imie2 = widget.text
        self.s2 = True


class Pytania_pf(Screen):
    lp1pf = []  # lista pytań 1 butelka prawda/fałsz
    with open("pytania/1pf.txt", encoding="utf8") as f:
        for l in f:
            l = l.strip()
            lp1pf.append(l)
    lp2pf = []  # lista pytań 2 butelka prawda/fałsz
    with open("pytania/2pf.txt", encoding="utf8") as f:
        for l in f:
            l = l.strip()
            lp2pf.append(l)
    lp3pf = []  # lista pytań 3 butelka prawda/fałsz
    with open("pytania/3pf.txt", encoding="utf8") as f:
        for l in f:
            l = l.strip()
            lp3pf.append(l)

    r = NumericProperty(0)  # runda dla pf
    n = NumericProperty(0)  # runda dla tj
    pb = ProgressBar(max=100, value=100)
    pf = ListProperty(lp1pf)
    pytanko = StringProperty(choice(lp1pf))
    c = NumericProperty(0)  # counter
    p1 = NumericProperty(0)  # punkty osoby 1
    p2 = NumericProperty(0)  # punkty osoby 2

    def ukryj(self):
        self.remove_widget(self.ids.instrukcja)
        self.remove_widget(self.ids.butelka)
        self.pb.value = 100
        self.c = 0
        self.r = 0
        self.n = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 10)

    def zmiana_imienia(self):
        if self.r % 2 == 0:
            self.ids.ktogra.text = self.manager.get_screen("imiona").ids.pierwsza.text + " odpowiada:"
        elif self.r % 2 == 1:
            self.ids.ktogra.text = self.manager.get_screen("imiona").ids.druga.text + " odpowiada:"

    def update(self, dt):
        if self.manager.current == 'pytania_pf':
            if self.pb.value > 0:
                self.pb.value -= 1
            else:
                self.pytanko = choice(self.pf)
                self.pf.remove(self.pytanko)
                self.pb.value = 100
                self.c += 1
                if self.c >= 10:
                    if self.r % 2 == 0:
                        self.manager.current = 'pytania_tj'
                    elif self.r % 2 == 1:
                        self.add_widget(self.ids.butelka)
                    self.c = 0
                    self.r += 1
                    self.zmiana_imienia()

    def p_click(self):
        self.pytanko = choice(self.pf)
        self.pf.remove(self.pytanko)
        self.pb.value = 100
        self.c += 1
        if self.r % 2 != 0:  # w nieparzystych rundach osoba 1 dostaje punkt
            self.p2 += 1
        if self.r % 2 == 0:  # w parzystych rundach osoba 2 dostaje punkt
            self.p1 += 1
        if self.c >= 10:
            if self.r % 2 == 0:
                self.manager.current = 'pytania_tj'
            elif self.r % 2 == 1:
                self.add_widget(self.ids.butelka)
            self.c = 0
            self.r += 1
            self.zmiana_imienia()

    def f_click(self):
        self.pytanko = choice(self.pf)
        self.pf.remove(self.pytanko)
        self.pb.value = 100
        self.c += 1
        if self.c >= 10:
            if self.r % 2 == 0:
                self.manager.current = 'pytania_tj'
            elif self.r % 2 == 1:
                self.add_widget(self.ids.butelka)
            self.r += 1
            self.c = 0
            self.zmiana_imienia()

    def jeszcze(self):
        self.remove_widget(self.ids.butelka)
        self.pytanko = choice(self.pf)
        self.pb.value = 100
        self.c = 0
        if len(self.pf) < 20:
            if self.n == 0:
                lp1pf = []
                with open("pytania/1pf.txt", encoding="utf8") as f:
                    for l in f:
                        l = l.strip()
                        lp1pf.append(l)
                self.pf = lp1pf
            if self.n == 1:
                lp2pf = []
                with open("pytania/2pf.txt", encoding="utf8") as f:
                    for l in f:
                        l = l.strip()
                        lp2pf.append(l)
                self.pf = lp2pf
            if self.n == 2:
                lp3pf = []
                with open("pytania/3pf.txt", encoding="utf8") as f:
                    for l in f:
                        l = l.strip()
                        lp3pf.append(l)
                self.pf = lp3pf

    def nastepna(self):
        self.remove_widget(self.ids.butelka)
        if self.n == 0:
            self.pf = self.lp2pf
        elif self.n == 1:
            self.pf = self.lp3pf
        else:
            print("koniec gry")
        self.n += 1
        Pytania_tj.n = self.n
        self.c = 0


class Pytania_tj(Screen):
    lp1tj = []  # lista pytań 1 butelka ty/ja
    with open("pytania/1tj.txt", encoding="utf8") as f:
        for l in f:
            l = l.strip()
            lp1tj.append(l)
    lp2tj = []  # lista pytań 2 butelka ty/ja
    with open("pytania/2tj.txt", encoding="utf8") as f:
        for l in f:
            l = l.strip()
            lp2tj.append(l)
    lp3tj = []  # lista pytań 3 butelka ty/ja
    with open("pytania/3tj.txt", encoding="utf8") as f:
        for l in f:
            l = l.strip()
            lp3tj.append(l)

    n = Pytania_pf.n  # runda
    c = NumericProperty(0)  # counter
    ea1 = BooleanProperty(True)
    ea2 = BooleanProperty(True)
    ea3 = BooleanProperty(True)
    ea4 = BooleanProperty(True)
    pz = NumericProperty(0)  # punkty zgodności
    pytanko = StringProperty(choice(lp1tj))
    pb = ProgressBar(max=100, value=100)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 10)

    def ukryj(self):
        self.remove_widget(self.ids.instrukcja)
        self.pb.value = 100

    def update(self, dt):
        if self.manager.current == 'pytania_tj':
            if self.pb.value > 0 and self.ea1 == True and self.ea2 == True or self.pb.value > 0 and self.ea3 == True and self.ea4 == True:
                self.pb.value -= 1
            else:
                if self.ids.tb1.state == "down" and self.ids.tb3.state == "down":
                    self.pz += 1
                if self.ids.tb2.state == "down" and self.ids.tb4.state == "down":
                    self.pz += 1
                self.pb.value = 100
                self.ids.tb1.state = "normal"
                self.ids.tb2.state = "normal"
                self.ids.tb3.state = "normal"
                self.ids.tb4.state = "normal"
                self.ea1 = True
                self.ea2 = True
                self.ea3 = True
                self.ea4 = True
                if self.n == 0:
                    self.pytanko = choice(self.lp1tj)
                    self.lp1tj.remove(self.pytanko)
                    if len(self.lp1tj) == 0:
                        with open("pytania/1tj.txt", encoding="utf8") as f:
                            for l in f:
                                l = l.strip()
                                self.lp1tj.append(l)
                elif self.n == 1:
                    self.pytanko = choice(self.lp2tj)
                    self.lp2tj.remove(self.pytanko)
                    if len(self.lp2tj) == 0:
                        with open("pytania/2tj.txt", encoding="utf8") as f:
                            for l in f:
                                l = l.strip()
                                self.lp2tj.append(l)
                elif self.n == 2:
                    self.pytanko = choice(self.lp3tj)
                    self.lp3tj.remove(self.pytanko)
                    if len(self.lp3tj) == 0:
                        with open("pytania/3tj.txt", encoding="utf8") as f:
                            for l in f:
                                l = l.strip()
                                self.lp3tj.append(l)
                self.c += 1
                if self.c >= 10:
                    self.manager.current = 'pytania_pf'
                    self.c = 0

    def da1(self):
        self.ea1 = False

    def da2(self):
        self.ea2 = False

    def da3(self):
        self.ea3 = False

    def da4(self):
        self.ea4 = False


class gdpApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Menu(name="menu"))
        sm.add_widget(Wiek(name="wiek"))
        sm.add_widget(Imiona(name="imiona"))
        sm.add_widget(Pytania_pf(name="pytania_pf"))
        sm.add_widget(Pytania_tj(name="pytania_tj"))
        # sm = ScreenManager(transition=NoTransition())
        return sm


gdpApp().run()
