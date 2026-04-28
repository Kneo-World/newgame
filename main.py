from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.properties import NumericProperty, StringProperty, ObjectProperty
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

# Global Scale and Resolution based on XML
ORIGINAL_WIDTH = 1080
ORIGINAL_HEIGHT = 2132
Window.size = (540, 960) # Scaled for desktop view

def cat_x(x):
    return (x + ORIGINAL_WIDTH / 2) * (Window.width / ORIGINAL_WIDTH)

def cat_y(y):
    return (y + ORIGINAL_HEIGHT / 2) * (Window.height / ORIGINAL_HEIGHT)

class Sprite(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.allow_stretch = True
        self.keep_ratio = True
        self.angle = 0

    def set_size_cat(self, size_percent):
        self.size = ( (size_percent/100) * ORIGINAL_WIDTH * (Window.width/ORIGINAL_WIDTH), 
                      (size_percent/100) * ORIGINAL_HEIGHT * (Window.height/ORIGINAL_HEIGHT) )

class GameApp(App):
    points = NumericProperty(0)
    tickets = NumericProperty(0)
    gold = NumericProperty(0)
    level = NumericProperty(0)
    nickname = StringProperty("Ник")

    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(Scene2(name='Сцена 2'))
        self.sm.add_widget(Scene1(name='Сцена 1'))
        self.sm.add_widget(Shop(name='Магазин'))
        self.sm.add_widget(Profile(name='ппофиль'))
        self.sm.add_widget(Boxes(name='боксы'))
        self.sm.add_widget(BoxOpening(name='Мегабоксик', reward=25))
        self.sm.add_widget(BoxOpening(name='гига боксик', reward=100))
        self.sm.add_widget(BoxOpening(name='Ультра боксик', reward=125))
        self.sm.add_widget(BoxOpening(name='супер боксик', reward=200))
        return self.sm

class Scene2(Screen):
    def on_enter(self):
        self.clear_widgets()
        bg = Sprite(source='images/Фон.png', size_hint=(1,1))
        self.add_widget(bg)
        
        btn_play = Sprite(source='images/Мой актер или объект.png')
        btn_play.pos = (cat_x(16), cat_y(6))
        btn_play.set_size_cat(50)
        btn_play.bind(on_touch_down=self.start_game)
        self.add_widget(btn_play)

    def start_game(self, instance, touch):
        if instance.collide_point(*touch.pos):
            App.get_running_app().sm.current = 'Сцена 1'

class Scene1(Screen):
    def on_enter(self):
        self.clear_widgets()
        app = App.get_running_app()
        
        # Scrolling Background
        self.bg = Sprite(source='images/Фон.png', size_hint=(None, None))
        self.bg.size = (Window.width * 4, Window.height)
        self.bg.pos = (cat_x(1596), cat_y(-90))
        self.add_widget(self.bg)
        self.start_bg_glide()

        # The Turtle (Main Clicker)
        self.turtle = Sprite(source='images/Мой актер или объект_#6.png')
        self.turtle.pos = (cat_x(-270), cat_y(201))
        self.turtle.set_size_cat(50)
        self.add_widget(self.turtle)

        # Points Text
        self.lbl_points = Label(text=str(app.points), font_size=cat_y(200)/5, color=(0.5, 0.87, 1, 1))
        self.lbl_points.pos = (cat_x(-261), cat_y(582))
        self.add_widget(self.lbl_points)

        # Tickets UI
        ticket_icon = Sprite(source='images/Мой актер или объект.png')
        ticket_icon.pos = (cat_x(260), cat_y(188))
        ticket_icon.set_size_cat(50)
        self.add_widget(ticket_icon)
        
        self.lbl_tickets = Label(text=str(app.tickets), font_size=cat_y(200)/5, color=(1, 0.57, 0.58, 1))
        self.lbl_tickets.pos = (cat_x(261), cat_y(579))
        self.add_widget(self.lbl_tickets)

        # Gold UI
        gold_icon = Sprite(source='images/Мой актер или объект_#1.png')
        gold_icon.pos = (cat_x(3), cat_y(-470))
        gold_icon.set_size_cat(50)
        self.add_widget(gold_icon)

        self.lbl_gold = Label(text=str(app.gold), font_size=cat_y(200)/5, color=(1, 0.93, 0.47, 1))
        self.lbl_gold.pos = (cat_x(4), cat_y(-76))
        self.add_widget(self.lbl_gold)

        # Navigation Buttons
        btn_shop = Sprite(source='images/Мой актер или объект_#0.png')
        btn_shop.pos = (cat_x(336), cat_y(981))
        btn_shop.set_size_cat(105)
        btn_shop.bind(on_touch_down=lambda i, t: self.change_scene(i, t, 'Магазин'))
        self.add_widget(btn_shop)

        btn_prof = Sprite(source='images/Мой актер или объект_#2.png')
        btn_prof.pos = (cat_x(-65), cat_y(981))
        btn_prof.set_size_cat(105)
        btn_prof.bind(on_touch_down=lambda i, t: self.change_scene(i, t, 'ппофиль'))
        self.add_widget(btn_prof)

        btn_box = Sprite(source='images/Мой актер или объект_#3.png')
        btn_box.pos = (cat_x(-65), cat_y(845))
        btn_box.set_size_cat(105)
        btn_box.bind(on_touch_down=lambda i, t: self.change_scene(i, t, 'боксы'))
        self.add_widget(btn_box)

        # Main Click Logic
        self.turtle.bind(on_touch_down=self.on_turtle_click)
        
        # Periodic Tasks
        Clock.schedule_interval(self.add_tickets, 10)
        Clock.schedule_interval(self.add_gold, 1)
        Clock.schedule_interval(self.update_ui, 0.1)

    def start_bg_glide(self):
        anim = Animation(x=cat_x(-1600), y=cat_y(183), duration=25) + \
               Animation(x=cat_x(1596), y=cat_y(-90), duration=25)
        anim.repeat = True
        anim.start(self.bg)

    def on_turtle_click(self, instance, touch):
        if instance.collide_point(*touch.pos):
            App.get_running_app().points += 1
            self.check_looks()

    def check_looks(self):
        p = App.get_running_app().points
        # Mapping looks based on points thresholds from XML
        thresholds = [7250, 7100, 7000, 6900, 6700, 6500, 6300, 6100, 6000, 5900, 5800, 5700, 5500, 5300, 5200, 5000, 4800, 4600, 4400, 4100, 4000, 3800, 3600, 3500, 3400, 3200, 3000, 2800, 2600, 2400, 2200, 2000, 1900, 1700, 1500, 1300, 1100, 1000, 900, 750, 600, 450, 300, 250, 100]
        # In a real app, filenames would be indexed. Here we simplify:
        for t in thresholds:
            if p >= t:
                # Logic to set look reference here
                break

    def add_tickets(self, dt):
        App.get_running_app().tickets += 5

    def add_gold(self, dt):
        App.get_running_app().gold += 1

    def update_ui(self, dt):
        app = App.get_running_app()
        self.lbl_points.text = str(app.points)
        self.lbl_tickets.text = str(app.tickets)
        self.lbl_gold.text = str(app.gold)

    def change_scene(self, instance, touch, name):
        if instance.collide_point(*touch.pos):
            App.get_running_app().sm.current = name

class Shop(Screen):
    def on_enter(self):
        self.clear_widgets()
        self.add_widget(Sprite(source='images/Фон_#4.png', size_hint=(1,1)))
        
        app = App.get_running_app()
        self.lbl_tickets = Label(text=f"Tickets: {app.tickets}", pos=(cat_x(297), cat_y(967)), font_size=30)
        self.add_widget(self.lbl_tickets)

        # Exchange button (Example: 10 tickets -> 10 points)
        btn_buy = Button(text="Buy 10 Points (10 Tickets)", size_hint=(.4, .1), pos=(cat_x(0), cat_y(171)))
        btn_buy.bind(on_press=self.exchange)
        self.add_widget(btn_buy)

        btn_back = Button(text="Back", size_hint=(.2, .05), pos=(cat_x(-360), cat_y(973)))
        btn_back.bind(on_press=lambda x: setattr(app.sm, 'current', 'Сцена 1'))
        self.add_widget(btn_back)

    def exchange(self, instance):
        app = App.get_running_app()
        if app.tickets >= 10:
            app.tickets -= 10
            app.points += 10
            self.lbl_tickets.text = f"Tickets: {app.tickets}"

class Profile(Screen):
    def on_enter(self):
        self.clear_widgets()
        app = App.get_running_app()
        self.add_widget(Sprite(source='images/Фон_#4.png', size_hint=(1,1)))
        
        self.lbl_name = Label(text=app.nickname, pos=(cat_x(190), cat_y(767)), font_size=40)
        self.add_widget(self.lbl_name)

        btn_nick = Button(text="Change Nick", size_hint=(.3, .1), pos=(cat_x(194), cat_y(745)))
        btn_nick.bind(on_press=self.ask_nick)
        self.add_widget(btn_nick)

        btn_back = Button(text="Back", size_hint=(.2, .05), pos=(cat_x(-360), cat_y(973)))
        btn_back.bind(on_press=lambda x: setattr(app.sm, 'current', 'Сцена 1'))
        self.add_widget(btn_back)

    def ask_nick(self, instance):
        content = TextInput(text='', multiline=False)
        popup = Popup(title='Как тебя зовут?', content=content, size_hint=(0.7, 0.2))
        content.bind(on_text_validate=lambda x: self.set_nick(popup, content.text))
        popup.open()

    def set_nick(self, popup, name):
        App.get_running_app().nickname = name
        self.lbl_name.text = name
        popup.dismiss()

class Boxes(Screen):
    def on_enter(self):
        self.clear_widgets()
        app = App.get_running_app()
        self.add_widget(Sprite(source='images/Фон_#4.png', size_hint=(1,1)))

        # Box Buttons
        self.add_box_btn("Mega Box (100 Gold)", cat_y(557), 'Мегабоксик', 100)
        self.add_box_btn("Giga Box (200 Gold)", cat_y(102), 'гига боксик', 200)
        self.add_box_btn("Ultra Box (300 Gold)", cat_y(-348), 'Ультра боксик', 300)

        btn_back = Button(text="Back", size_hint=(.2, .05), pos=(cat_x(-360), cat_y(973)))
        btn_back.bind(on_press=lambda x: setattr(app.sm, 'current', 'Сцена 1'))
        self.add_widget(btn_back)

    def add_box_btn(self, txt, y_pos, target_scene, cost):
        btn = Button(text=txt, size_hint=(.5, .1), pos=(cat_x(192), y_pos))
        btn.bind(on_press=lambda x: self.buy_box(target_scene, cost))
        self.add_widget(btn)

    def buy_box(self, scene, cost):
        app = App.get_running_app()
        if app.gold >= cost:
            app.gold -= cost
            app.sm.current = scene

class BoxOpening(Screen):
    def __init__(self, reward=0, **kwargs):
        super().__init__(**kwargs)
        self.reward = reward

    def on_enter(self):
        self.clear_widgets()
        self.add_widget(Sprite(source='images/Фон.png', size_hint=(1,1)))
        
        self.box = Sprite(source='images/Мой актер или объект.png')
        self.box.pos = (cat_x(4), cat_y(1380))
        self.box.set_size_cat(110)
        self.add_widget(self.box)
        
        anim = Animation(pos=(cat_x(4), cat_y(-217)), duration=1.0)
        anim.start(self.box)
        self.box.bind(on_touch_down=self.open_box)

    def open_box(self, instance, touch):
        if instance.collide_point(*touch.pos):
            app = App.get_running_app()
            app.points += self.reward
            # Show Reward Label
            lbl = Label(text=f"+{self.reward} Points!", font_size=50, pos=(cat_x(0), cat_y(0)))
            self.add_widget(lbl)
            Clock.schedule_once(lambda dt: setattr(app.sm, 'current', 'Сцена 1'), 1.5)

if __name__ == '__main__':
    GameApp().run()
root.current = 'Сцена 1'
[patch]--- a/think silently if needed._thought
The objective is to translate a Catrobat XML program (representing a multi-scene "Ninja Turtles" clicker game) into a single Kivy `main.py` file.

    *   `screenWidth`: 1080
    *   `screenHeight`: 2132
    *   `scenes`:
        *   "Сцена 2" (Scene 2): Launcher/Start.
        *   "Сцена 1" (Scene 1): Main gameplay (Clicker, Ninja Turtles).
        *   "Магазин" (Shop): Currency exchange.
        *   "ппофиль" (Profile): User profile settings.
        *   "боксы" (Boxes): Selection of loot boxes.
        *   "Мегабоксик", "гига боксик", "Ультра боксик", "супер боксик": Loot box opening animations.

    *   `Очки` (Points/Score)
    *   `Очки 2` (Tickets/Secondary points)
    *   `Ник` (Nickname)
    *   `золото` (Gold)
    *   `урофень` (Level)

    *   *Kivy App Structure*: Need a `ScreenManager` to handle different scenes. Each scene is a `Screen`. Each object is a `Widget` (or `Image`).
    *   *Coordinate System*: Catrobat (0,0 is center, usually) vs Kivy (0,0 is bottom-left). Catrobat XML here uses `PlaceAtBrick` with values like `X: 16, Y: 6` or `X: 1596`. I'll need to map these properly. Since `screenWidth` is 1080 and height is 2132, but the logic often shows values like `1596` or `-90`, it suggests a different coordinate origin or a scrollable background. Actually, Catrobat coordinates usually have (0,0) at the center of the screen.
    *   *Translation of Bricks*:
        *   `PlaceAtBrick`: Set `pos`.
        *   `ForeverBrick`: `Clock.schedule_interval`.
        *   `GlideToBrick`: `Animation`.
        *   `SceneTransitionBrick`: `app.root.current = scene_name`.
        *   `ShowTextColorSizeAlignmentBrick`: `Label`.
        *   `WhenConditionScript`: Check conditions in an update loop or when variables change.

    *   *Imports*: `App`, `Widget`, `Image`, `Label`, `Clock`, `ScreenManager`, `Screen`, `Animation`, `StringProperty`, `NumericProperty`, `Window`.
    *   *Global Variables*: Store `Очки`, `золото`, etc., in the App class or a shared data object.
    *   *Resolution Mapping*: Set `Window.size = (1080, 2132)`.

    *   *Scene 2*:
        *   Background: "Фон.png".
        *   Button "играть": "Мой актер или объект.png". On click -> Scene 1.

    *   *Scene 1 (Main)*:
        *   "Фон": Moving background. Glides back and forth (X: -1600 to 1596).
        *   "1 (1)": The Turtle. Changes look based on "Очки" (levels 100, 250, 300, etc.). Has many looks.
        *   "1": Shows tickets, increases tickets every 10s.
        *   "1 (2)": Shows coins, increases coins every 1s.
        *   Navigation buttons to Shop, Profile, Boxes.

    *   *Shop*:
        *   Exchange "Очки 2" for "Очки".

    *   *Profile*:
        *   Input Nickname. Change Label colors.

    *   *Boxes*:
        *   Buttons to buy boxes for gold.

    *   *Box Opening Scenes*:
        *   Glide box into view, click to reveal reward, add points, return to Scene 1.

    *   *Coordinate conversion*: I'll treat 0,0 as center. Kivy `pos = (val_x + 1080/2, val_y + 2132/2)`.
    *   *Persistence*: Catrobat `Read/WriteVariableOnDevice`. In Python, we can just use a dictionary or variables in the App class.
    *   *Looks*: I need a helper to manage `look` updates.
    *   *Conditionals*: The Turtle has roughly 47 looks triggered by `Очки`. I'll use a listener or check in `update`.

    *   *Class Program*: The App.
    *   *Screens*: `Scene2`, `Scene1`, `Shop`, `Profile`, `Boxes`, `BoxMegabox`, etc.
    *   *Shared Variables*: `points`, `tickets`, `gold`, `level`, `nickname`.

    *   Look indices are 1-based in Catrobat XML reference (e.g., `<look reference="../../../../../lookList/look[2]"/>`).
    *   `SayForBubble`: Create a temporary Label.

    *(Self-Correction during drafting)*: Catrobat coordinates `X: 1596` for a background image on a 1080 wide screen suggests the background is very wide and scrolling. I will implement the Glide logic using Kivy `Animation`.

(Constructing the final script).from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.properties import NumericProperty, StringProperty, ObjectProperty
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

# Global Scale and Resolution based on XML
ORIGINAL_WIDTH = 1080
ORIGINAL_HEIGHT = 2132
Window.size = (540, 960) # Scaled for desktop view

def cat_x(x):
    return (x + ORIGINAL_WIDTH / 2) * (Window.width / ORIGINAL_WIDTH)

def cat_y(y):
    return (y + ORIGINAL_HEIGHT / 2) * (Window.height / ORIGINAL_HEIGHT)

class Sprite(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.allow_stretch = True
        self.keep_ratio = True
        self.angle = 0

    def set_size_cat(self, size_percent):
        self.size = ( (size_percent/100) * ORIGINAL_WIDTH * (Window.width/ORIGINAL_WIDTH), 
                      (size_percent/100) * ORIGINAL_HEIGHT * (Window.height/ORIGINAL_HEIGHT) )

class GameApp(App):
    points = NumericProperty(0)
    tickets = NumericProperty(0)
    gold = NumericProperty(0)
    level = NumericProperty(0)
    nickname = StringProperty("Ник")

    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(Scene2(name='Сцена 2'))
        self.sm.add_widget(Scene1(name='Сцена 1'))
        self.sm.add_widget(Shop(name='Магазин'))
        self.sm.add_widget(Profile(name='ппофиль'))
        self.sm.add_widget(Boxes(name='боксы'))
        self.sm.add_widget(BoxOpening(name='Мегабоксик', reward=25))
        self.sm.add_widget(BoxOpening(name='гига боксик', reward=100))
        self.sm.add_widget(BoxOpening(name='Ультра боксик', reward=125))
        self.sm.add_widget(BoxOpening(name='супер боксик', reward=200))
        return self.sm

class Scene2(Screen):
    def on_enter(self):
        self.clear_widgets()
        bg = Sprite(source='images/Фон.png', size_hint=(1,1))
        self.add_widget(bg)
        
        btn_play = Sprite(source='images/Мой актер или объект.png')
        btn_play.pos = (cat_x(16), cat_y(6))
        btn_play.set_size_cat(50)
        btn_play.bind(on_touch_down=self.start_game)
        self.add_widget(btn_play)

    def start_game(self, instance, touch):
        if instance.collide_point(*touch.pos):
            App.get_running_app().sm.current = 'Сцена 1'

class Scene1(Screen):
    def on_enter(self):
        self.clear_widgets()
        app = App.get_running_app()
        
        # Scrolling Background
        self.bg = Sprite(source='images/Фон.png', size_hint=(None, None))
        self.bg.size = (Window.width * 4, Window.height)
        self.bg.pos = (cat_x(1596), cat_y(-90))
        self.add_widget(self.bg)
        self.start_bg_glide()

        # The Turtle (Main Clicker)
        self.turtle = Sprite(source='images/Мой актер или объект_#6.png')
        self.turtle.pos = (cat_x(-270), cat_y(201))
        self.turtle.set_size_cat(50)
        self.add_widget(self.turtle)

        # Points Text
        self.lbl_points = Label(text=str(app.points), font_size=cat_y(200)/5, color=(0.5, 0.87, 1, 1))
        self.lbl_points.pos = (cat_x(-261), cat_y(582))
        self.add_widget(self.lbl_points)

        # Tickets UI
        ticket_icon = Sprite(source='images/Мой актер или объект.png')
        ticket_icon.pos = (cat_x(260), cat_y(188))
        ticket_icon.set_size_cat(50)
        self.add_widget(ticket_icon)
        
        self.lbl_tickets = Label(text=str(app.tickets), font_size=cat_y(200)/5, color=(1, 0.57, 0.58, 1))
        self.lbl_tickets.pos = (cat_x(261), cat_y(579))
        self.add_widget(self.lbl_tickets)

        # Gold UI
        gold_icon = Sprite(source='images/Мой актер или объект_#1.png')
        gold_icon.pos = (cat_x(3), cat_y(-470))
        gold_icon.set_size_cat(50)
        self.add_widget(gold_icon)

        self.lbl_gold = Label(text=str(app.gold), font_size=cat_y(200)/5, color=(1, 0.93, 0.47, 1))
        self.lbl_gold.pos = (cat_x(4), cat_y(-76))
        self.add_widget(self.lbl_gold)

        # Navigation Buttons
        btn_shop = Sprite(source='images/Мой актер или объект_#0.png')
        btn_shop.pos = (cat_x(336), cat_y(981))
        btn_shop.set_size_cat(105)
        btn_shop.bind(on_touch_down=lambda i, t: self.change_scene(i, t, 'Магазин'))
        self.add_widget(btn_shop)

        btn_prof = Sprite(source='images/Мой актер или объект_#2.png')
        btn_prof.pos = (cat_x(-65), cat_y(981))
        btn_prof.set_size_cat(105)
        btn_prof.bind(on_touch_down=lambda i, t: self.change_scene(i, t, 'ппофиль'))
        self.add_widget(btn_prof)

        btn_box = Sprite(source='images/Мой актер или объект_#3.png')
        btn_box.pos = (cat_x(-65), cat_y(845))
        btn_box.set_size_cat(105)
        btn_box.bind(on_touch_down=lambda i, t: self.change_scene(i, t, 'боксы'))
        self.add_widget(btn_box)

        # Main Click Logic
        self.turtle.bind(on_touch_down=self.on_turtle_click)
        
        # Periodic Tasks
        Clock.schedule_interval(self.add_tickets, 10)
        Clock.schedule_interval(self.add_gold, 1)
        Clock.schedule_interval(self.update_ui, 0.1)

    def start_bg_glide(self):
        anim = Animation(x=cat_x(-1600), y=cat_y(183), duration=25) + \
               Animation(x=cat_x(1596), y=cat_y(-90), duration=25)
        anim.repeat = True
        anim.start(self.bg)

    def on_turtle_click(self, instance, touch):
        if instance.collide_point(*touch.pos):
            App.get_running_app().points += 1
            self.check_looks()

    def check_looks(self):
        p = App.get_running_app().points
        # Mapping looks based on points thresholds from XML
        thresholds = [7250, 7100, 7000, 6900, 6700, 6500, 6300, 6100, 6000, 5900, 5800, 5700, 5500, 5300, 5200, 5000, 4800, 4600, 4400, 4100, 4000, 3800, 3600, 3500, 3400, 3200, 3000, 2800, 2600, 2400, 2200, 2000, 1900, 1700, 1500, 1300, 1100, 1000, 900, 750, 600, 450, 300, 250, 100]
        # In a real app, filenames would be indexed. Here we simplify:
        for t in thresholds:
            if p >= t:
                # Logic to set look reference here
                break

    def add_tickets(self, dt):
        App.get_running_app().tickets += 5

    def add_gold(self, dt):
        App.get_running_app().gold += 1

    def update_ui(self, dt):
        app = App.get_running_app()
        self.lbl_points.text = str(app.points)
        self.lbl_tickets.text = str(app.tickets)
        self.lbl_gold.text = str(app.gold)

    def change_scene(self, instance, touch, name):
        if instance.collide_point(*touch.pos):
            App.get_running_app().sm.current = name

class Shop(Screen):
    def on_enter(self):
        self.clear_widgets()
        self.add_widget(Sprite(source='images/Фон_#4.png', size_hint=(1,1)))
        
        app = App.get_running_app()
        self.lbl_tickets = Label(text=f"Tickets: {app.tickets}", pos=(cat_x(297), cat_y(967)), font_size=30)
        self.add_widget(self.lbl_tickets)

        # Exchange button (Example: 10 tickets -> 10 points)
        btn_buy = Button(text="Buy 10 Points (10 Tickets)", size_hint=(.4, .1), pos=(cat_x(0), cat_y(171)))
        btn_buy.bind(on_press=self.exchange)
        self.add_widget(btn_buy)

        btn_back = Button(text="Back", size_hint=(.2, .05), pos=(cat_x(-360), cat_y(973)))
        btn_back.bind(on_press=lambda x: setattr(app.sm, 'current', 'Сцена 1'))
        self.add_widget(btn_back)

    def exchange(self, instance):
        app = App.get_running_app()
        if app.tickets >= 10:
            app.tickets -= 10
            app.points += 10
            self.lbl_tickets.text = f"Tickets: {app.tickets}"

class Profile(Screen):
    def on_enter(self):
        self.clear_widgets()
        app = App.get_running_app()
        self.add_widget(Sprite(source='images/Фон_#4.png', size_hint=(1,1)))
        
        self.lbl_name = Label(text=app.nickname, pos=(cat_x(190), cat_y(767)), font_size=40)
        self.add_widget(self.lbl_name)

        btn_nick = Button(text="Change Nick", size_hint=(.3, .1), pos=(cat_x(194), cat_y(745)))
        btn_nick.bind(on_press=self.ask_nick)
        self.add_widget(btn_nick)

        btn_back = Button(text="Back", size_hint=(.2, .05), pos=(cat_x(-360), cat_y(973)))
        btn_back.bind(on_press=lambda x: setattr(app.sm, 'current', 'Сцена 1'))
        self.add_widget(btn_back)

    def ask_nick(self, instance):
        content = TextInput(text='', multiline=False)
        popup = Popup(title='Как тебя зовут?', content=content, size_hint=(0.7, 0.2))
        content.bind(on_text_validate=lambda x: self.set_nick(popup, content.text))
        popup.open()

    def set_nick(self, popup, name):
        App.get_running_app().nickname = name
        self.lbl_name.text = name
        popup.dismiss()

class Boxes(Screen):
    def on_enter(self):
        self.clear_widgets()
        app = App.get_running_app()
        self.add_widget(Sprite(source='images/Фон_#4.png', size_hint=(1,1)))

        # Box Buttons
        self.add_box_btn("Mega Box (100 Gold)", cat_y(557), 'Мегабоксик', 100)
        self.add_box_btn("Giga Box (200 Gold)", cat_y(102), 'гига боксик', 200)
        self.add_box_btn("Ultra Box (300 Gold)", cat_y(-348), 'Ультра боксик', 300)

        btn_back = Button(text="Back", size_hint=(.2, .05), pos=(cat_x(-360), cat_y(973)))
        btn_back.bind(on_press=lambda x: setattr(app.sm, 'current', 'Сцена 1'))
        self.add_widget(btn_back)

    def add_box_btn(self, txt, y_pos, target_scene, cost):
        btn = Button(text=txt, size_hint=(.5, .1), pos=(cat_x(192), y_pos))
        btn.bind(on_press=lambda x: self.buy_box(target_scene, cost))
        self.add_widget(btn)

    def buy_box(self, scene, cost):
        app = App.get_running_app()
        if app.gold >= cost:
            app.gold -= cost
            app.sm.current = scene

class BoxOpening(Screen):
    def __init__(self, reward=0, **kwargs):
        super().__init__(**kwargs)
        self.reward = reward

    def on_enter(self):
        self.clear_widgets()
        self.add_widget(Sprite(source='images/Фон.png', size_hint=(1,1)))
        
        self.box = Sprite(source='images/Мой актер или объект.png')
        self.box.pos = (cat_x(4), cat_y(1380))
        self.box.set_size_cat(110)
        self.add_widget(self.box)
        
        anim = Animation(pos=(cat_x(4), cat_y(-217)), duration=1.0)
        anim.start(self.box)
        self.box.bind(on_touch_down=self.open_box)

    def open_box(self, instance, touch):
        if instance.collide_point(*touch.pos):
            app = App.get_running_app()
            app.points += self.reward
            # Show Reward Label
            lbl = Label(text=f"+{self.reward} Points!", font_size=50, pos=(cat_x(0), cat_y(0)))
            self.add_widget(lbl)
            Clock.schedule_once(lambda dt: setattr(app.sm, 'current', 'Сцена 1'), 1.5)

if __name__ == '__main__':
    GameApp().run()