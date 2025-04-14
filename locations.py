import json
import os
import pygame
from datetime import datetime
import random

import variables
import widgets

class Location_Ustawienia():
    def __init__(self):
        self.surface = pygame.Surface((variables.ustawienia['Szerokość'] - 60 * variables.ustawienia['Skalowanie'], variables.ustawienia['Wysokość'] - 94 * variables.ustawienia['Skalowanie']))
        self.slider_y = widgets.Slider_Y(variables.window, (variables.ustawienia['Szerokość'] - 50 * variables.ustawienia['Skalowanie'], 84 * variables.ustawienia['Skalowanie']), (30 * variables.ustawienia['Skalowanie'], self.surface.get_height() - 10 * variables.ustawienia['Skalowanie']), (100, 100, 100), 5 * variables.ustawienia['Skalowanie'], (0, 0, 0), (50, 50, 50))

        self.jezyk_label = widgets.Label(self.surface, (0, 0), None, f'{variables.jezyk["Ustawienia"]["Język"]}: {variables.ustawienia["Język"]}', 50, (255, 255, 255))
        self.jezyki = []
        self.maksymalne_miejsca = int(self.surface.get_width() / (74 * variables.ustawienia['Skalowanie']))
        for index, nazwa in enumerate(os.listdir('languages')):
            self.jezyki.append((widgets.Button(self.surface, (74 * (index % self.maksymalne_miejsca), 50 + 74 * (index // self.maksymalne_miejsca)), (f'languages/{nazwa}/icon.png', (64, 64)), real_pos=(10 * variables.ustawienia['Skalowanie'] + 74 * (index % self.maksymalne_miejsca), 134 + 74 * (index // self.maksymalne_miejsca))), nazwa))

        self.glosnosc_ogolna_label = widgets.Label(self.surface, (0, self.jezyki[-1][0].y + 74 * variables.ustawienia['Skalowanie']), None, f'{variables.jezyk["Ustawienia"]["Głośność ogólna"]} ({variables.ustawienia["Głośność"]["Ogólne"]})', 50, (255, 255, 255))
        self.glosnosc_ogolna_slider = widgets.Slider(self.surface, (0, self.glosnosc_ogolna_label.y + 50 * variables.ustawienia['Skalowanie']), (self.surface.get_width() - 20 * variables.ustawienia['Skalowanie'], 30 * variables.ustawienia['Skalowanie']), (100, 100, 100), 5, (0, 0, 0), (50, 50, 50), real_pos=(10, 0), init_value=variables.ustawienia["Głośność"]["Ogólne"])
        self.glosnosc_ogolna_slider.real_y = self.glosnosc_ogolna_slider.y + 84
        self.glosnosc_muzyka_label = widgets.Label(self.surface, (0, self.glosnosc_ogolna_slider.y + 50 * variables.ustawienia['Skalowanie']), None, f'{variables.jezyk["Ustawienia"]["Głośność muzyki"]} ({variables.ustawienia["Głośność"]["Muzyka"]})', 50, (255, 255, 255))
        self.glosnosc_muzyka_slider = widgets.Slider(self.surface, (0, self.glosnosc_muzyka_label.y + 50 * variables.ustawienia['Skalowanie']), (self.surface.get_width() - 20 * variables.ustawienia['Skalowanie'], 30 * variables.ustawienia['Skalowanie']), (100, 100, 100), 5, (0, 0, 0), (50, 50, 50), real_pos=(10, 0), init_value=variables.ustawienia["Głośność"]["Muzyka"])
        self.glosnosc_muzyka_slider.real_y = self.glosnosc_muzyka_slider.y + 84
        self.slider_y.max = self.glosnosc_muzyka_slider.y - self.surface.get_height()
        if self.slider_y.max < 1:
            self.slider_y.max = 1

    def draw(self):
        if variables.Locations.Location_Lista.ustawienia_button.draw():
            variables.lokalizacja = 'Ustawienia'
        if variables.Locations.Location_Lista.info_button.draw():
            variables.lokalizacja = 'Informacje'
        if variables.Locations.Location_Lista.lista_quizow_button.draw():
            variables.lokalizacja = 'Lista'
        if variables.Locations.Location_Lista.stworz_quiz_button.draw():
            variables.lokalizacja = 'Stwórz quiz'

        self.surface.fill((30, 30, 30))

        self.jezyk_label.y = -self.slider_y.value * variables.ustawienia['Skalowanie']
        self.jezyk_label.draw()
        for index, (button, jezyk) in enumerate(self.jezyki):
            button.y = (50 + 74 * (index // self.maksymalne_miejsca) - round(self.slider_y.value)) * variables.ustawienia['Skalowanie']
            button.real_y = (134 + 74 * (index // self.maksymalne_miejsca) - round(self.slider_y.value)) * variables.ustawienia['Skalowanie']
            if button.draw():
                variables.ustawienia['Język'] = jezyk
                widgets.zapisz_ustawienia()
                variables.run = 0

        self.glosnosc_ogolna_label.y = self.jezyki[-1][0].y + 74 * variables.ustawienia['Skalowanie']
        self.glosnosc_ogolna_label.draw()
        self.glosnosc_ogolna_slider.y = self.glosnosc_ogolna_label.y + 50 * variables.ustawienia['Skalowanie']
        self.glosnosc_ogolna_slider.real_y = self.glosnosc_ogolna_slider.y + 84 * variables.ustawienia['Skalowanie']
        if self.glosnosc_ogolna_slider.draw():
            variables.ustawienia['Głośność']['Ogólne'] = round(self.glosnosc_ogolna_slider.value)
            self.glosnosc_ogolna_label.edit_text(f'Głośność ogólna ({variables.ustawienia["Głośność"]["Ogólne"]})')
            widgets.zapisz_ustawienia()
        self.glosnosc_muzyka_label.y = self.glosnosc_ogolna_slider.y + 50 * variables.ustawienia['Skalowanie']
        self.glosnosc_muzyka_label.draw()
        self.glosnosc_muzyka_slider.y = self.glosnosc_muzyka_label.y + 50 * variables.ustawienia['Skalowanie']
        self.glosnosc_muzyka_slider.real_y = self.glosnosc_muzyka_slider.y + 84 * variables.ustawienia['Skalowanie']
        if self.glosnosc_muzyka_slider.draw():
            variables.ustawienia['Głośność']['Muzyka'] = round(self.glosnosc_muzyka_slider.value)
            self.glosnosc_muzyka_label.edit_text(f'Głośność muzyki ({variables.ustawienia["Głośność"]["Muzyka"]})')
            widgets.zapisz_ustawienia()

        variables.window.blit(self.surface, (10 * variables.ustawienia['Skalowanie'], 84 * variables.ustawienia['Skalowanie']))
        if self.slider_y.max != 1:
            self.slider_y.draw()

class Location_Inforamcje():
    def __init__(self):
        self.surface = pygame.Surface((variables.ustawienia['Szerokość'] - 60 * variables.ustawienia['Skalowanie'], variables.ustawienia['Wysokość'] - 94 * variables.ustawienia['Skalowanie']))

        tekst = f'''{variables.jezyk["Informacje"]["Autor"]}: czarchmA8
{variables.jezyk["Informacje"]["Data powstania"]}: 07-02-2025 r.
{variables.jezyk["Informacje"]["Ostatnia aktualizacja"]}: {datetime.strptime(variables.data_aktualizacji, "%Y-%m-%d, %H:%M:%S").strftime("%d-%m-%Y")} r.
{variables.jezyk["Informacje"]["Wersja"]}: {variables.wersja}

{variables.jezyk["Informacje"]["Opis"]}'''

        self.label = widgets.Label(self.surface, (0, 0), None, tekst, 40, (255, 255, 255), max_width=variables.ustawienia['Szerokość'] - 75 * variables.ustawienia['Skalowanie'])
        max_y = self.label.text_surface.get_height() - self.surface.get_height() + 40 * variables.ustawienia['Skalowanie']
        if max_y < 1:
            max_y = 1
        self.slider_y = widgets.Slider_Y(variables.window, (variables.ustawienia['Szerokość'] - 50 * variables.ustawienia['Skalowanie'], 84 * variables.ustawienia['Skalowanie']), (30 * variables.ustawienia['Skalowanie'], self.surface.get_height() - 10 * variables.ustawienia['Skalowanie']), (100, 100, 100), 5, (0, 0, 0), (50, 50, 50), 0, max_y)

    def draw(self):
        if variables.Locations.Location_Lista.ustawienia_button.draw():
            variables.lokalizacja = 'Ustawienia'
        if variables.Locations.Location_Lista.info_button.draw():
            variables.lokalizacja = 'Informacje'
        if variables.Locations.Location_Lista.lista_quizow_button.draw():
            variables.lokalizacja = 'Lista'
        if variables.Locations.Location_Lista.stworz_quiz_button.draw():
            variables.lokalizacja = 'Stwórz quiz'

        self.surface.fill((30, 30, 30))
        self.label.y = -self.slider_y.value
        self.label.draw()
        variables.window.blit(self.surface, (10 * variables.ustawienia['Skalowanie'], 84 * variables.ustawienia['Skalowanie']))
        if self.slider_y.max != 1:
            self.slider_y.draw()

class Location_Lista():
    def __init__(self):
        self.ustawienia_button = widgets.Button(variables.window, (10 * variables.ustawienia['Skalowanie'], 10 * variables.ustawienia['Skalowanie']), ('assets/Buttons/settings.png', (64, 64)))
        self.info_button = widgets.Button(variables.window, (84 * variables.ustawienia['Skalowanie'], 10 * variables.ustawienia['Skalowanie']), ('assets/Buttons/info.png', (64, 64)))
        self.lista_quizow_button = widgets.Button(variables.window, (168 * variables.ustawienia['Skalowanie'], 10 * variables.ustawienia['Skalowanie']), ('assets/Buttons/list.png', (64, 64)))
        self.stworz_quiz_button = widgets.Button(variables.window, (242 * variables.ustawienia['Skalowanie'], 10 * variables.ustawienia['Skalowanie']), ('assets/Buttons/create.png', (64, 64)))
        self.surface = pygame.Surface((variables.ustawienia['Szerokość'] - 60 * variables.ustawienia['Skalowanie'], variables.ustawienia['Wysokość'] - 204 * variables.ustawienia['Skalowanie']))
        self.slider_y = widgets.Slider_Y(variables.window, (variables.ustawienia['Szerokość'] - 50 * variables.ustawienia['Skalowanie'], 84 * variables.ustawienia['Skalowanie']), (30 * variables.ustawienia['Skalowanie'], self.surface.get_height()), (100, 100, 100), 5, (0, 0, 0), (50, 50, 50))
        self.slider_x = widgets.Slider(variables.window, (10 * variables.ustawienia['Skalowanie'], variables.ustawienia['Wysokość'] - 120 * variables.ustawienia['Skalowanie']), (self.surface.get_width() + 30 * variables.ustawienia['Skalowanie'], 30 * variables.ustawienia['Skalowanie']), (100, 100, 100), 5, (0, 0, 0), (50, 50, 50))
        self.mouse_motion = None

        self.widoczne_checkbox = widgets.CheckBox(self.surface, (0, 0), [(('assets/Buttons/not_visible.png', (48, 48)), None, None, None, None), (('assets/Buttons/visible2.png', (48, 48)), None, None, None, None)])
        self.dodaj_checkbox = widgets.CheckBox(self.surface, (0, 0), [(('assets/Buttons/close.png', (48, 48)), None, None, None, None), (('assets/Buttons/accept.png', (48, 48)), None, None, None, None)])

        self.widoczne_quizy: list = []
        self.dodane_quizy: dict = {}
        self.ustawienia_quizow: dict = {}
        self.all_folders: dict = {'Quizzes': []}
        for root, dirs, files in os.walk('Quizzes'):
            if dirs == ['Obrazy'] and files == ['ustawienia.json']:
                self.all_folders[root] = None
            else:
                for directory in dirs:
                    full_path = os.path.join(root, directory)
                    if root in self.all_folders:
                        self.all_folders[root].append(full_path)
                    else:
                        self.all_folders[root] = [full_path]
        self.widoczne_quizy.append('Quizzes')
        self.ustawienia_quizow['Quizzes'] = {
            "Widoczne": False,
            "Label": widgets.Label(self.surface, (0, 0), None, 'Quizzes', 45, (255, 255, 255))
        }

        self.ilosc_pytan: int = 0
        self.zaznaczono_pytan_label = widgets.Label(variables.window, (15 * variables.ustawienia['Skalowanie'], variables.ustawienia['Wysokość'] - 60 * variables.ustawienia['Skalowanie']), None, f'{variables.jezyk["Lista pytań"]["Zaznaczono"]} 0 {variables.jezyk["Lista pytań"]["Pytań"]}', 50, (255, 255, 255))
        self.dalej_button = widgets.Button(variables.window, (variables.ustawienia['Szerokość'] - 74 * variables.ustawienia['Skalowanie'], variables.ustawienia['Wysokość'] - 74 * variables.ustawienia['Skalowanie']), ('assets/Buttons/play.png', (64, 64)))

        self.zapisz_button = widgets.Button(variables.window, (variables.ustawienia['Szerokość'] - 138 * variables.ustawienia['Skalowanie'], 10 * variables.ustawienia['Skalowanie']), ('assets/Buttons/save.png', (64, 64)))
        self.wczytaj_button = widgets.Button(variables.window, (variables.ustawienia['Szerokość'] - 74 * variables.ustawienia['Skalowanie'], 10 * variables.ustawienia['Skalowanie']), ('assets/Buttons/load.png', (64, 64)))

    def draw(self):
        if self.ustawienia_button.draw():
            variables.lokalizacja = 'Ustawienia'
        if self.info_button.draw():
            variables.lokalizacja = 'Informacje'
        if self.lista_quizow_button.draw():
            variables.lokalizacja = 'Lista'
        if self.stworz_quiz_button.draw():
            variables.lokalizacja = 'Stwórz quiz'
        if self.zapisz_button.draw():
            variables.lokalizacja = 'Zapisywanie'
        if self.wczytaj_button.draw():
            variables.lokalizacja = 'Wczytywanie'

        pygame.draw.rect(variables.window, (0, 0, 0), (10 * variables.ustawienia['Skalowanie'], 84 * variables.ustawienia['Skalowanie'], variables.ustawienia['Szerokość'] - 60 * variables.ustawienia['Skalowanie'], variables.ustawienia['Wysokość'] - 194 * variables.ustawienia['Skalowanie']))
        self.surface.fill((80, 80, 80))
        max_szerokosc = 0
        for index, lokalizacja in enumerate(self.widoczne_quizy):
            self.dodaj_checkbox.x, self.dodaj_checkbox.y = (55 + 20 * lokalizacja.count(os.sep)) * variables.ustawienia['Skalowanie'] - self.slider_x.value, (5 + 50 * index) * variables.ustawienia['Skalowanie'] - self.slider_y.value
            self.dodaj_checkbox.real_x, self.dodaj_checkbox.real_y = (70 + 20 * lokalizacja.count(os.sep)) * variables.ustawienia['Skalowanie'] - self.slider_x.value, (94 + 50 * index) * variables.ustawienia['Skalowanie'] - self.slider_y.value
            self.dodaj_checkbox.value = True if lokalizacja in self.dodane_quizy else False
            self.ustawienia_quizow[lokalizacja]['Label'].x, self.ustawienia_quizow[lokalizacja]['Label'].y = (105 + 20 * lokalizacja.count(os.sep)) * variables.ustawienia['Skalowanie'] - self.slider_x.value, (5 + 50 * index) * variables.ustawienia['Skalowanie'] - self.slider_y.value
            szerokosc = self.ustawienia_quizow[lokalizacja]['Label'].x + self.slider_x.value + self.ustawienia_quizow[lokalizacja]['Label'].text_surface.get_width()
            if szerokosc > max_szerokosc:
                max_szerokosc = szerokosc

            klikniety_checkbox_lokalizacja = None
            if self.all_folders[lokalizacja] is not None:
                self.widoczne_checkbox.x, self.widoczne_checkbox.y = (5 + 20 * lokalizacja.count(os.sep)) * variables.ustawienia['Skalowanie'] - self.slider_x.value, (5 + 50 * index) * variables.ustawienia['Skalowanie'] - self.slider_y.value
                self.widoczne_checkbox.real_x, self.widoczne_checkbox.real_y = (20 + 20 * lokalizacja.count(os.sep)) * variables.ustawienia['Skalowanie'] - self.slider_x.value, (94 + 50 * index) * variables.ustawienia['Skalowanie'] - self.slider_y.value
                self.widoczne_checkbox.value = self.ustawienia_quizow[lokalizacja]['Widoczne']
                if self.widoczne_checkbox.draw():
                    klikniety_checkbox_lokalizacja = lokalizacja

            if klikniety_checkbox_lokalizacja:
                self.ustawienia_quizow[lokalizacja]['Widoczne'] = not self.ustawienia_quizow[lokalizacja]['Widoczne']
                if self.ustawienia_quizow[lokalizacja]['Widoczne']:
                    for index2, pelna_lokalizacja in enumerate(self.all_folders[lokalizacja]):
                        self.widoczne_quizy.insert(index+index2+1, pelna_lokalizacja)
                        self.ustawienia_quizow[pelna_lokalizacja] = {
                            "Widoczne": False,
                            "Label": widgets.Label(self.surface, (0, 0), None, os.path.basename(pelna_lokalizacja), 45, (255, 255, 255))
                        }
                else:
                    for pelna_lokalizacja in self.all_folders:
                        if lokalizacja in pelna_lokalizacja and pelna_lokalizacja != lokalizacja:
                            if pelna_lokalizacja in self.widoczne_quizy:
                                del self.ustawienia_quizow[pelna_lokalizacja]
                                self.widoczne_quizy.remove(pelna_lokalizacja)

            if self.dodaj_checkbox.draw():
                if self.dodaj_checkbox.value:
                    self.dodane_quizy[lokalizacja] = None
                else:
                    del self.dodane_quizy[lokalizacja]

                for pelna_lokalizacja in self.all_folders:
                    if lokalizacja+os.sep in pelna_lokalizacja:
                        if self.dodaj_checkbox.value:
                            self.dodane_quizy[pelna_lokalizacja] = None
                        elif pelna_lokalizacja in self.dodane_quizy:
                            del self.dodane_quizy[pelna_lokalizacja]

                if lokalizacja in self.dodane_quizy:
                    for pelna_lokalizacja in self.all_folders:
                        if pelna_lokalizacja+os.sep in lokalizacja:
                            self.dodane_quizy[pelna_lokalizacja] = None
                else:
                    while variables.run:
                        lokalizacja_rodzica = os.path.dirname(lokalizacja)
                        if lokalizacja_rodzica != '':
                            wszystkie_false = True
                            for pelna_lokalizacja in self.all_folders:
                                if lokalizacja_rodzica in pelna_lokalizacja and pelna_lokalizacja != lokalizacja_rodzica:
                                    if pelna_lokalizacja in self.dodane_quizy:
                                        wszystkie_false = False

                            if wszystkie_false:
                                del self.dodane_quizy[lokalizacja_rodzica]
                                lokalizacja = lokalizacja_rodzica
                            else:
                                break
                        else:
                            break
            self.ustawienia_quizow[lokalizacja]['Label'].draw()

        variables.window.blit(self.surface, (15 * variables.ustawienia['Skalowanie'], 89 * variables.ustawienia['Skalowanie']))
        max = (len(self.widoczne_quizy) * 50 + 50) * variables.ustawienia['Skalowanie'] - self.surface.get_height()
        if max < 1:
            max = 1
        if max != self.slider_y.max:
            v = self.slider_y.value
            self.slider_y.max = max
            self.slider_y.set_value(v)
        self.slider_y.draw()

        max = max_szerokosc - self.surface.get_width() + 20 * variables.ustawienia['Skalowanie']
        if max < 1:
            max = 1
        if max != self.slider_x.max:
            v = self.slider_x.value
            self.slider_x.max = max
            self.slider_x.set_value(v)
        self.slider_x.draw()

        if variables.mouse_scroll != 0:
            if 'left shift' in variables.pressed_keys:
                self.slider_x.set_value(self.slider_x.value - variables.mouse_scroll * 25 * variables.ustawienia['Skalowanie'])
            else:
                self.slider_y.set_value(self.slider_y.value - variables.mouse_scroll * 25 * variables.ustawienia['Skalowanie'])

        if variables.mouse_pressed[0] == 2:
            rect = self.surface.get_rect()
            rect.x, rect.y = 15 * variables.ustawienia['Skalowanie'], 89 * variables.ustawienia['Skalowanie']
            if rect.collidepoint(variables.mouse_x, variables.mouse_y):
                self.mouse_motion = None, variables.mouse_x, variables.mouse_y
        elif self.mouse_motion is not None and variables.mouse_pressed[0] == 1:
            if self.mouse_motion[0] is None:
                if abs(self.mouse_motion[2] - variables.mouse_y) - 5 * variables.ustawienia['Skalowanie'] > abs(self.mouse_motion[1] - variables.mouse_x):
                    self.mouse_motion = 'y', self.slider_y.value + self.mouse_motion[2]
                elif abs(self.mouse_motion[1] - variables.mouse_x) - 5 * variables.ustawienia['Skalowanie'] > abs(self.mouse_motion[2] - variables.mouse_y):
                    self.mouse_motion = 'x', self.slider_x.value + self.mouse_motion[1]
            elif self.mouse_motion[0] == 'y':
                self.slider_y.set_value(self.mouse_motion[1] - variables.mouse_y)
            elif self.mouse_motion[0] == 'x':
                self.slider_x.set_value(self.mouse_motion[1] - variables.mouse_x)
        elif variables.mouse_pressed[0] == 3:
            self.mouse_motion = None

        self.ilosc_pytan = sum(self.all_folders[lokalizacja] is None for lokalizacja in self.dodane_quizy)
        self.zaznaczono_pytan_label.edit_text(f'{variables.jezyk["Lista pytań"]["Zaznaczono"]} {self.ilosc_pytan} {variables.jezyk["Lista pytań"]["Pytań"]}')
        self.zaznaczono_pytan_label.draw()
        if self.dalej_button.draw() and self.ilosc_pytan > 0:
            variables.lokalizacja = 'Kolejność'
            variables.Locations.Location_Kolejnosc.widoczne_quizy = ['Quizzes']
            variables.Locations.Location_Kolejnosc.ustawienia_quizow = {}
            for lokalizacja in variables.Locations.Location_Lista.dodane_quizy:
                if lokalizacja == 'Quizzes':
                    variables.Locations.Location_Kolejnosc.ustawienia_quizow['Quizzes'] = {
                        "Widoczne": False,
                        "Kolejność": "Losowa",
                        "Label": widgets.Label(variables.Locations.Location_Kolejnosc.surface, (0, 0), None, 'Quizzes', 45, (255, 255, 255))
                    }
                else:
                    if self.all_folders[lokalizacja] is None:
                        ustawienia = {"Kolejność": None}
                    else:
                        with open(os.path.join(lokalizacja, 'ustawienia.json'), 'r', encoding='utf-8') as f:
                            ustawienia = json.load(f)
                    variables.Locations.Location_Kolejnosc.ustawienia_quizow[lokalizacja] = {
                        "Widoczne": False,
                        "Kolejność": ustawienia["Kolejność"],
                        "Label": None
                    }

class Location_Kolejnosc():
    def __init__(self):
        self.powrot_button = widgets.Button(variables.window, (10 * variables.ustawienia['Skalowanie'], 10 * variables.ustawienia['Skalowanie']), ('assets/Buttons/back.png', (64, 64)))

        self.zapisz_button = widgets.Button(variables.window, (variables.ustawienia['Szerokość'] - 74 * variables.ustawienia['Skalowanie'], 10 * variables.ustawienia['Skalowanie']), ('assets/Buttons/save.png', (64, 64)))

        self.surface = pygame.Surface((variables.ustawienia['Szerokość'] - 60 * variables.ustawienia['Skalowanie'], variables.ustawienia['Wysokość'] - 204 * variables.ustawienia['Skalowanie']))
        self.slider_y = widgets.Slider_Y(variables.window, (variables.ustawienia['Szerokość'] - 50 * variables.ustawienia['Skalowanie'], 84 * variables.ustawienia['Skalowanie']), (30 * variables.ustawienia['Skalowanie'], self.surface.get_height()), (100, 100, 100), 5, (0, 0, 0), (50, 50, 50))
        self.slider_x = widgets.Slider(variables.window, (10 * variables.ustawienia['Skalowanie'], variables.ustawienia['Wysokość'] - 120 * variables.ustawienia['Skalowanie']), (self.surface.get_width() + 30 * variables.ustawienia['Skalowanie'], 30 * variables.ustawienia['Skalowanie']), (100, 100, 100), 5, (0, 0, 0), (50, 50, 50))
        self.mouse_motion = None

        self.widoczne_checkbox = widgets.CheckBox(self.surface, (0, 0), [(('assets/Buttons/not_visible.png', (48, 48)), None, None, None, None), (('assets/Buttons/visible2.png', (48, 48)), None, None, None, None)])
        self.losowe_checkbox = widgets.CheckBox(self.surface, (0, 0), [(('assets/Buttons/not_random.png', (48, 48)), None, None, None, None), (('assets/Buttons/random.png', (48, 48)), None, None, None, None), (('assets/Buttons/unimportant.png', (48, 48)), None, None, None, None)])

        self.widoczne_quizy: list = []
        self.ustawienia_quizow: dict = {}

        self.rozpocznij_button = widgets.Button(variables.window, (variables.ustawienia['Szerokość'] - 74 * variables.ustawienia['Skalowanie'], variables.ustawienia['Wysokość'] - 74 * variables.ustawienia['Skalowanie']), ('assets/Buttons/play.png', (64, 64)))

    def draw(self):
        if self.powrot_button.draw():
            variables.lokalizacja = 'Lista'
        if self.zapisz_button.draw():
            variables.lokalizacja = 'Zapisywanie_Kolejności'

        pygame.draw.rect(variables.window, (0, 0, 0), (10 * variables.ustawienia['Skalowanie'], 84 * variables.ustawienia['Skalowanie'], variables.ustawienia['Szerokość'] - 60 * variables.ustawienia['Skalowanie'], variables.ustawienia['Wysokość'] - 194 * variables.ustawienia['Skalowanie']))
        self.surface.fill((80, 80, 80))
        max_szerokosc = 0
        for index, lokalizacja in enumerate(self.widoczne_quizy):
            klikniety_checkbox_lokalizacja = None
            if variables.Locations.Location_Lista.all_folders[lokalizacja] is not None:
                self.losowe_checkbox.x, self.losowe_checkbox.y = (55 + 20 * lokalizacja.count(os.sep)) * variables.ustawienia['Skalowanie'] - self.slider_x.value, (5 + 50 * index) * variables.ustawienia['Skalowanie'] - self.slider_y.value
                self.losowe_checkbox.real_x, self.losowe_checkbox.real_y = (70 + 20 * lokalizacja.count(os.sep)) * variables.ustawienia['Skalowanie'] - self.slider_x.value, (94 + 50 * index) * variables.ustawienia['Skalowanie'] - self.slider_y.value
                self.losowe_checkbox.value = ("Uporządkowana", "Losowa", "Ignorowana").index(self.ustawienia_quizow[lokalizacja]['Kolejność'])
                if self.losowe_checkbox.draw():
                    self.ustawienia_quizow[lokalizacja]['Kolejność'] = "Losowa" if self.ustawienia_quizow[lokalizacja]['Kolejność'] == "Uporządkowana" else ("Ignorowana" if self.ustawienia_quizow[lokalizacja]['Kolejność'] == "Losowa" and lokalizacja != 'Quizzes' else "Uporządkowana")

                self.widoczne_checkbox.x, self.widoczne_checkbox.y = (5 + 20 * lokalizacja.count(os.sep)) * variables.ustawienia['Skalowanie'] - self.slider_x.value, (5 + 50 * index) * variables.ustawienia['Skalowanie'] - self.slider_y.value
                self.widoczne_checkbox.real_x, self.widoczne_checkbox.real_y = (20 + 20 * lokalizacja.count(os.sep)) * variables.ustawienia['Skalowanie'] - self.slider_x.value, (94 + 50 * index) * variables.ustawienia['Skalowanie'] - self.slider_y.value
                self.widoczne_checkbox.value = self.ustawienia_quizow[lokalizacja]['Widoczne']
                if self.widoczne_checkbox.draw():
                    klikniety_checkbox_lokalizacja = lokalizacja

            if klikniety_checkbox_lokalizacja:
                self.ustawienia_quizow[lokalizacja]['Widoczne'] = not self.ustawienia_quizow[lokalizacja]['Widoczne']
                if self.ustawienia_quizow[lokalizacja]['Widoczne']:
                    minus = 0
                    for index2, pelna_lokalizacja in enumerate(variables.Locations.Location_Lista.all_folders[lokalizacja]):
                        if pelna_lokalizacja in variables.Locations.Location_Lista.dodane_quizy:
                            self.widoczne_quizy.insert(index+index2-minus+1, pelna_lokalizacja)
                            self.ustawienia_quizow[pelna_lokalizacja]['Widoczne'] = False
                            self.ustawienia_quizow[pelna_lokalizacja]['Label'] = widgets.Label(self.surface, (0, 0), None, os.path.basename(pelna_lokalizacja), 45, (255, 255, 255))
                        else:
                            minus += 1
                else:
                    for pelna_lokalizacja in variables.Locations.Location_Lista.all_folders:
                        if lokalizacja in pelna_lokalizacja and pelna_lokalizacja != lokalizacja:
                            if pelna_lokalizacja in self.widoczne_quizy:
                                self.ustawienia_quizow[pelna_lokalizacja]['Label'] = None
                                self.widoczne_quizy.remove(pelna_lokalizacja)

            self.ustawienia_quizow[lokalizacja]['Label'].x, self.ustawienia_quizow[lokalizacja]['Label'].y = (105 + 20 * lokalizacja.count(os.sep)) * variables.ustawienia['Skalowanie'] - self.slider_x.value, (5 + 50 * index) * variables.ustawienia['Skalowanie'] - self.slider_y.value
            self.ustawienia_quizow[lokalizacja]['Label'].draw()
            szerokosc = self.ustawienia_quizow[lokalizacja]['Label'].x + self.slider_x.value + self.ustawienia_quizow[lokalizacja]['Label'].text_surface.get_width()
            if szerokosc > max_szerokosc:
                max_szerokosc = szerokosc

        variables.window.blit(self.surface, (15 * variables.ustawienia['Skalowanie'], 89 * variables.ustawienia['Skalowanie']))
        max = (len(self.widoczne_quizy) * 50 + 50) * variables.ustawienia['Skalowanie'] - self.surface.get_height()
        if max < 1:
            max = 1
        if max != self.slider_y.max:
            v = self.slider_y.value
            self.slider_y.max = max
            self.slider_y.set_value(v)
        self.slider_y.draw()

        max = max_szerokosc - self.surface.get_width() + 20 * variables.ustawienia['Skalowanie']
        if max < 1:
            max = 1
        if max != self.slider_x.max:
            v = self.slider_x.value
            self.slider_x.max = max
            self.slider_x.set_value(v)
        self.slider_x.draw()

        if variables.mouse_scroll != 0:
            if 'left shift' in variables.pressed_keys:
                self.slider_x.set_value(self.slider_x.value - variables.mouse_scroll * 25 * variables.ustawienia['Skalowanie'])
            else:
                self.slider_y.set_value(self.slider_y.value - variables.mouse_scroll * 25 * variables.ustawienia['Skalowanie'])

        if variables.mouse_pressed[0] == 2:
            rect = self.surface.get_rect()
            rect.x, rect.y = 15 * variables.ustawienia['Skalowanie'], 89 * variables.ustawienia['Skalowanie']
            if rect.collidepoint(variables.mouse_x, variables.mouse_y):
                self.mouse_motion = None, variables.mouse_x, variables.mouse_y
        elif self.mouse_motion is not None and variables.mouse_pressed[0] == 1:
            if self.mouse_motion[0] is None:
                if abs(self.mouse_motion[2] - variables.mouse_y) - 5 * variables.ustawienia['Skalowanie'] > abs(self.mouse_motion[1] - variables.mouse_x):
                    self.mouse_motion = 'y', self.slider_y.value + self.mouse_motion[2]
                elif abs(self.mouse_motion[1] - variables.mouse_x) - 5 * variables.ustawienia['Skalowanie'] > abs(self.mouse_motion[2] - variables.mouse_y):
                    self.mouse_motion = 'x', self.slider_x.value + self.mouse_motion[1]
            elif self.mouse_motion[0] == 'y':
                self.slider_y.set_value(self.mouse_motion[1] - variables.mouse_y)
            elif self.mouse_motion[0] == 'x':
                self.slider_x.set_value(self.mouse_motion[1] - variables.mouse_x)
        elif variables.mouse_pressed[0] == 3:
            self.mouse_motion = None

        variables.Locations.Location_Lista.zaznaczono_pytan_label.edit_text(f'{variables.Locations.Location_Lista.ilosc_pytan} {variables.jezyk["Lista pytań"]["Pytań"]}')
        variables.Locations.Location_Lista.zaznaczono_pytan_label.draw()

        if self.rozpocznij_button.draw():
            self.rozpocznij_quiz()

    def rozpocznij_quiz(self):
        variables.lokalizacja = 'Quiz_Pytanie'

        # print("All folders:", variables.Locations.Location_Lista.all_folders) # "lokalizacja": ["lokalizacja"...]
        # print("Dodane quizy:", variables.Locations.Location_Lista.dodane_quizy) # "lokalizacja": None
        # print("Ustawienia quizów:", self.ustawienia_quizow) # "lokalizacja": {ustawienia}

        # Ignorowanie folderów z pytaniami
        for lokalizacja in variables.Locations.Location_Lista.dodane_quizy:
            if self.ustawienia_quizow[lokalizacja]["Kolejność"] == "Ignorowana":
                nadfolder = os.path.dirname(lokalizacja)
                while variables.run:
                    if self.ustawienia_quizow[nadfolder]["Kolejność"] == "Ignorowana":
                        nadfolder = os.path.dirname(nadfolder)
                    else:
                        break

                for l in variables.Locations.Location_Lista.all_folders[lokalizacja]:
                    if l in variables.Locations.Location_Lista.dodane_quizy:
                        if variables.Locations.Location_Lista.dodane_quizy[nadfolder] is None:
                            variables.Locations.Location_Lista.dodane_quizy[nadfolder] = []
                        variables.Locations.Location_Lista.dodane_quizy[nadfolder].append(l)
        # print('Zignorowane:', variables.Locations.Location_Lista.dodane_quizy)

        # Mieszanie pytań
        for lokalizacja in variables.Locations.Location_Lista.dodane_quizy:
            if self.ustawienia_quizow[lokalizacja]['Kolejność'] == "Losowa":
                if variables.Locations.Location_Lista.dodane_quizy[lokalizacja] is None:
                    cos = []
                    for l in variables.Locations.Location_Lista.all_folders[lokalizacja]:
                        if l in variables.Locations.Location_Lista.dodane_quizy:
                            cos.append(l)
                    variables.Locations.Location_Lista.dodane_quizy[lokalizacja] = random.sample(cos, len(cos))
                else:
                    variables.Locations.Location_Lista.dodane_quizy[lokalizacja] = random.sample(variables.Locations.Location_Lista.dodane_quizy[lokalizacja], len(variables.Locations.Location_Lista.dodane_quizy[lokalizacja]))

            elif self.ustawienia_quizow[lokalizacja]['Kolejność'] == "Uporządkowana" and variables.Locations.Location_Lista.dodane_quizy[lokalizacja] is None:
                variables.Locations.Location_Lista.dodane_quizy[lokalizacja] = []
                for l in variables.Locations.Location_Lista.all_folders[lokalizacja]:
                    if l in variables.Locations.Location_Lista.dodane_quizy:
                        variables.Locations.Location_Lista.dodane_quizy[lokalizacja].append(l)
        # print('Wymieszane:', variables.Locations.Location_Lista.dodane_quizy)

        pytania = []
        dokoncz = ['Quizzes']
        while variables.run:
            if variables.Locations.Location_Lista.dodane_quizy[dokoncz[0]] is not None:
                for lokalizacja in variables.Locations.Location_Lista.dodane_quizy[dokoncz[0]]:
                    dokoncz.append(lokalizacja)
            elif self.ustawienia_quizow[dokoncz[0]]['Kolejność'] is None:
                pytania.append(dokoncz[0])
            dokoncz.pop(0)
            if dokoncz == []:
                break
        # print('Pytania:', pytania)

        # Restartowanie listy dodane_quizy
        for lokalizacja in variables.Locations.Location_Lista.dodane_quizy:
            variables.Locations.Location_Lista.dodane_quizy[lokalizacja] = None

        variables.Locations.Location_Quiz_Pytanie.pytania = pytania
        variables.Locations.Location_Quiz_Pytanie.pytanie = -1
        variables.Locations.Location_Quiz_Pytanie.poprawne_odpowiedzi = 0
        variables.Locations.Location_Quiz_Pytanie.zdobyte_punkty = 0
        variables.Locations.Location_Quiz_Pytanie.odpowiedzi = []
        variables.Locations.Location_Quiz_Pytanie.czas_rozpoczecia = datetime.now()
        variables.Locations.Location_Quiz_Pytanie.nastepne_pytanie()

class Location_Quiz_Pytanie():
    def __init__(self):
        self.pytania: list = []
        self.pytanie: int = 0
        self.zdjecia: list = []
        self.zdjecie: int = 0
        self.zdjecie_y: int = 0
        self.ustawienia_pytania: dict = {}
        self.zdobyte_punkty: int = 0
        self.poprawne_odpowiedzi: int = 0
        self.odpowiedzi: list = []
        self.czas_rozpoczecia = None
        self.czas_odpowiedzi = None

        self.ilosc_pytan_label: widgets.Label = widgets.Label(variables.window, (84 * variables.ustawienia['Skalowanie'], 22 * variables.ustawienia['Skalowanie']), None, '', 40, (255, 255, 255))
        self.pytanie_label: widgets.Label = widgets.Label(variables.window, (10 * variables.ustawienia['Skalowanie'], 84 * variables.ustawienia['Skalowanie']), None, '', 50, (255, 255, 255), max_width=variables.ustawienia['Szerokość'] - 20 * variables.ustawienia['Skalowanie'], wyrownaj_do='middle')

        self.nastepne_zdjecie_button = widgets.Button(variables.window, (variables.ustawienia['Szerokość'] - 74 * variables.ustawienia['Skalowanie'], 0), ('assets/Buttons/not_visible.png', (64, 64)))
        self.poprzednie_zdjecie_button = widgets.Button(variables.window, (10 * variables.ustawienia['Skalowanie'], 0), ('assets/Buttons/smaller_than.png', (64, 64)))

        self.odpowiedz_entry = widgets.Entry(variables.window, (10 * variables.ustawienia['Skalowanie'], 0), (variables.ustawienia['Szerokość'] - 30 * variables.ustawienia['Skalowanie'], 40 * variables.ustawienia['Skalowanie']), None, (255, 255, 255), (100, 100, 100), 5, (0, 0, 0), None, f'{variables.jezyk["Pytanie"]["Typ odpowiedzi"]["Wpisz odpowiedz"]}', (120, 120, 120), (80, 80, 80), (0, 0, 0), (50, 50, 50), (0, 0, 0))

        self.minutnik_progressbar = widgets.ProgressBar(variables.window, (10 * variables.ustawienia['Skalowanie'], 0), (variables.ustawienia['Szerokość'] - 30 * variables.ustawienia['Skalowanie'], 40 * variables.ustawienia['Skalowanie']), (100, 100, 100), 5, (0, 0, 0), (50, 50, 240))
        self.minutnik = 0

    def draw(self):
        if variables.Locations.Location_Kolejnosc.powrot_button.draw():
            variables.lokalizacja = 'Lista'

        self.ilosc_pytan_label.draw()
        self.pytanie_label.draw()

        if type(self.zdjecia[self.zdjecie]) is str:
            obraz = pygame.image.load(os.path.join(self.pytania[self.pytanie], 'Obrazy', self.zdjecia[self.zdjecie]))
            szerokosc, wysokosc = obraz.get_size()
            wspolczynnik = self.pytanie_label.max_width / szerokosc
            if wysokosc * wspolczynnik > variables.ustawienia['Wysokość'] / 2.5:
                szerokosc, wysokosc = szerokosc * (variables.ustawienia['Wysokość'] / 2.5 / wysokosc), variables.ustawienia['Wysokość'] / 2.5
            else:
                szerokosc, wysokosc = self.pytanie_label.max_width - 40 * variables.ustawienia['Skalowanie'], wysokosc * wspolczynnik
            self.zdjecia[self.zdjecie] = pygame.transform.scale(obraz, (szerokosc, wysokosc)).convert_alpha()

        variables.window.blit(self.zdjecia[self.zdjecie], ((variables.ustawienia['Szerokość'] - 20 * variables.ustawienia['Skalowanie'] - self.zdjecia[self.zdjecie].get_width()) / 2 + 10 * variables.ustawienia['Skalowanie'], self.pytanie_label.text_surface.get_height() + 94 * variables.ustawienia['Skalowanie']))
        if self.zdjecie <= len(self.zdjecia) - 2:
            self.nastepne_zdjecie_button.y = self.zdjecie_y
            self.nastepne_zdjecie_button.real_y = self.zdjecie_y
            if self.nastepne_zdjecie_button.draw() or (not self.odpowiedz_entry.clicked and 'right' in variables.pressed_keys and variables.pressed_keys['right'][1] == 1):
                self.zdjecie += 1
        if self.zdjecie > 0:
            self.poprzednie_zdjecie_button.y = self.zdjecie_y
            self.poprzednie_zdjecie_button.real_y = self.zdjecie_y
            if self.poprzednie_zdjecie_button.draw() or (not self.odpowiedz_entry.clicked and 'left' in variables.pressed_keys and variables.pressed_keys['left'][1] == 1):
                self.zdjecie -= 1

        if self.minutnik < self.minutnik_progressbar.max:
            self.minutnik += 1
            if self.minutnik == self.minutnik_progressbar.max:
                self.czas_odpowiedzi = datetime.now()
            self.minutnik_progressbar.set_value(self.minutnik)

            self.minutnik_progressbar.y = self.zdjecie_y + 74 * variables.ustawienia['Skalowanie']
            self.minutnik_progressbar.real_y = self.minutnik_progressbar.y
            self.minutnik_progressbar.draw()
        else:
            zatwierdz = False
            if self.ustawienia_pytania['Typ odpowiedzi'] == 'Wpisz tekst':
                self.odpowiedz_entry.y = self.zdjecie_y + 74 * variables.ustawienia['Skalowanie']
                self.odpowiedz_entry.real_y = self.odpowiedz_entry.y
                self.odpowiedz_entry.draw()
                zatwierdz = variables.Locations.Location_Lista.dalej_button.draw() or 'return' in variables.pressed_keys and variables.pressed_keys['return'][1] == 3

            if zatwierdz:
                if self.ustawienia_pytania['Typ odpowiedzi'] == 'Wpisz tekst':
                    self.poprawna_odpowiedz = False
                    for poprawna_odpowiedz, punkty in self.ustawienia_pytania['Poprawne odpowiedzi']:
                        if self.ustawienia_pytania['Rozróżnianie wielkości liter'] == False:
                            if self.odpowiedz_entry.text.lower() == poprawna_odpowiedz.lower():
                                self.poprawna_odpowiedz = True
                                break
                        else:
                            if self.odpowiedz_entry.text == poprawna_odpowiedz:
                                self.poprawna_odpowiedz = True
                                break
                    self.odpowiedzi.append({"Odpowiedź": self.odpowiedz_entry.text})
                self.odpowiedzi[-1]["Punkty"] = punkty
                self.odpowiedzi[-1]["Max punkty"] = max([p for _, p in self.ustawienia_pytania['Poprawne odpowiedzi']])
                self.odpowiedzi[-1]["Czas odpowiedzi"] = (datetime.now() - self.czas_odpowiedzi).total_seconds()

                self.zdjecie_y = self.pytanie_label.text_surface.get_height() + variables.ustawienia['Wysokość'] / 2.5
                self.pytanie_label.x = 0
                self.pytanie_label.surface = variables.Locations.Location_Quiz_Odpowiedz.surface
                self.poprzednie_zdjecie_button.surface = variables.Locations.Location_Quiz_Odpowiedz.surface
                self.poprzednie_zdjecie_button.x = 0
                self.poprzednie_zdjecie_button.real_x = 10 * variables.ustawienia['Skalowanie']
                self.nastepne_zdjecie_button.surface = variables.Locations.Location_Quiz_Odpowiedz.surface
                self.nastepne_zdjecie_button.x = variables.ustawienia['Szerokość'] - 134 * variables.ustawienia['Skalowanie']
                self.nastepne_zdjecie_button.real_x = variables.ustawienia['Szerokość'] - 124 * variables.ustawienia['Skalowanie']
                variables.Locations.Location_Quiz_Odpowiedz.slider_y.set_value(0)

                if self.poprawna_odpowiedz:
                    self.zdobyte_punkty += punkty
                    self.poprawne_odpowiedzi += 1
                    self.ilosc_pytan_label.edit_text(f'{variables.jezyk["Pytanie"]["Pytanie"]} {self.pytanie + 1}/{len(self.pytania)} | {variables.jezyk["Pytanie"]["Punkty"]}: {self.zdobyte_punkty} | {variables.jezyk["Pytanie"]["Poprawne odpowiedzi"]}: {self.poprawne_odpowiedzi}/{self.pytanie + 1}')

                variables.lokalizacja = 'Quiz_Odpowiedź'

    def nastepne_pytanie(self):
        self.pytanie += 1
        if self.pytanie >= len(self.pytania):
            variables.lokalizacja = 'Quiz_Wynik'
            max_punkty = sum([dict['Max punkty'] for dict in self.odpowiedzi])
            czas_ukonczenia = datetime.now() - self.czas_rozpoczecia
            hours, remainder = divmod(czas_ukonczenia.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            hours = f"{int(hours)}h" if hours > 0 else ""
            minutes = f"{int(minutes)}m" if minutes > 0 else ""
            sredni_czas_odpowiedzi = round(sum([dict['Czas odpowiedzi'] for dict in self.odpowiedzi]) / self.pytanie, 1)
            variables.Locations.Location_Quiz_wynik.informacje_label.edit_text(
                f'''{variables.jezyk["Wyniki"]["Zdobyte punkty"]}: {self.zdobyte_punkty} / {max_punkty} ({round(self.zdobyte_punkty / max_punkty * 100, 1)}%)
                {variables.jezyk["Wyniki"]["Poprawne odpowiedzi"]}: {self.poprawne_odpowiedzi} / {self.pytanie} ({round(self.poprawne_odpowiedzi / self.pytanie * 100, 1)}%)
                {variables.jezyk["Wyniki"]["Czas ukończenia"]}: {hours} {minutes} {int(seconds)}s
                {variables.jezyk["Wyniki"]["Średni czas odpowiedzi"]}: {sredni_czas_odpowiedzi}s''')
            return
        self.czas_odpowiedzi = datetime.now()
        self.ilosc_pytan_label.edit_text(f'{variables.jezyk["Pytanie"]["Pytanie"]} {self.pytanie + 1}/{len(self.pytania)} | {variables.jezyk["Pytanie"]["Punkty"]}: {self.zdobyte_punkty} | {variables.jezyk["Pytanie"]["Poprawne odpowiedzi"]}: {self.poprawne_odpowiedzi}/{self.pytanie}')
        with open(os.path.join(self.pytania[self.pytanie], 'ustawienia.json'), 'r', encoding='utf-8') as f:
            self.ustawienia_pytania = json.load(f)
        self.pytanie_label.edit_text(self.ustawienia_pytania['Pytanie'])
        self.zdjecia: list = os.listdir(os.path.join(self.pytania[self.pytanie], 'Obrazy'))
        self.zdjecie: int = 0
        self.zdjecie_y: int = self.pytanie_label.text_surface.get_height() + variables.ustawienia['Wysokość'] / 2.5 + 104 * variables.ustawienia['Skalowanie']

        self.pytanie_label.x = 10 * variables.ustawienia['Skalowanie']
        self.pytanie_label.y = 84 * variables.ustawienia['Skalowanie']
        self.pytanie_label.surface = variables.window
        self.poprzednie_zdjecie_button.surface = variables.window
        self.poprzednie_zdjecie_button.x = 10 * variables.ustawienia['Skalowanie']
        self.poprzednie_zdjecie_button.real_x = self.poprzednie_zdjecie_button.x
        self.nastepne_zdjecie_button.surface = variables.window
        self.nastepne_zdjecie_button.x = variables.ustawienia['Szerokość'] - 74 * variables.ustawienia['Skalowanie']
        self.nastepne_zdjecie_button.real_x = self.nastepne_zdjecie_button.x

        self.odpowiedz_entry.edit_text('')
        if self.ustawienia_pytania['Czas na reakcje (s)'] > 0:
            self.minutnik = 0
            self.minutnik_progressbar.max = self.ustawienia_pytania['Czas na reakcje (s)'] * 60
        else:
            self.minutnik = 0
            self.minutnik_progressbar.max = 0

class Location_Quiz_Odpowiedz():
    def __init__(self):
        self.surface = pygame.Surface((variables.ustawienia['Szerokość'] - 60 * variables.ustawienia['Skalowanie'], variables.ustawienia['Wysokość'] - 218 * variables.ustawienia['Skalowanie']))
        self.slider_y = widgets.Slider_Y(variables.window, (variables.ustawienia['Szerokość'] - 50 * variables.ustawienia['Skalowanie'], 144 * variables.ustawienia['Skalowanie']), (30 * variables.ustawienia['Skalowanie'], self.surface.get_height() - 10 * variables.ustawienia['Skalowanie']), (100, 100, 100), 5, (0, 0, 0), (50, 50, 50))

        self.odpowiedz_poprawna_label = widgets.Label(variables.window, (10 * variables.ustawienia['Skalowanie'], 84 * variables.ustawienia['Skalowanie']), None, f'{variables.jezyk["Odpowiedź"]["Poprawna odpowiedź"]}', 50, (100, 255, 100))
        self.odpowiedz_poprawna_label.x = (variables.ustawienia['Szerokość'] - self.odpowiedz_poprawna_label.text_surface.get_width()) / 2
        self.odpowiedz_nie_poprawna_label = widgets.Label(variables.window, (10 * variables.ustawienia['Skalowanie'], 84 * variables.ustawienia['Skalowanie']), None, f'{variables.jezyk["Odpowiedź"]["Zła odpowiedź"]}', 50, (255, 100, 100))
        self.odpowiedz_nie_poprawna_label.x = (variables.ustawienia['Szerokość'] - self.odpowiedz_nie_poprawna_label.text_surface.get_width()) / 2
        self.twoja_odpowiedz_label = widgets.Label(self.surface, (0, 0), None, 'Twoja odpowiedź: ', 40, (255, 255, 255), max_width=self.surface.get_width())

    def draw(self):
        if variables.Locations.Location_Kolejnosc.powrot_button.draw():
            variables.lokalizacja = 'Lista'

        variables.Locations.Location_Quiz_Pytanie.ilosc_pytan_label.draw()

        self.surface.fill((30, 30, 30))

        variables.Locations.Location_Quiz_Pytanie.pytanie_label.y = -self.slider_y.value
        variables.Locations.Location_Quiz_Pytanie.pytanie_label.draw()

        if type(variables.Locations.Location_Quiz_Pytanie.zdjecia[variables.Locations.Location_Quiz_Pytanie.zdjecie]) is str:
            obraz = pygame.image.load(os.path.join(variables.Locations.Location_Quiz_Pytanie.pytania[variables.Locations.Location_Quiz_Pytanie.pytanie], 'Obrazy', variables.Locations.Location_Quiz_Pytanie.zdjecia[variables.Locations.Location_Quiz_Pytanie.zdjecie]))
            szerokosc, wysokosc = obraz.get_size()
            wspolczynnik = variables.Locations.Location_Quiz_Pytanie.pytanie_label.max_width / szerokosc
            if wysokosc * wspolczynnik > variables.ustawienia['Wysokość'] / 2.5:
                szerokosc, wysokosc = szerokosc * (variables.ustawienia['Wysokość'] / 2.5 / wysokosc), variables.ustawienia['Wysokość'] / 2.5
            else:
                szerokosc, wysokosc = variables.Locations.Location_Quiz_Pytanie.pytanie_label.max_width, wysokosc * wspolczynnik
            variables.Locations.Location_Quiz_Pytanie.zdjecia[variables.Locations.Location_Quiz_Pytanie.zdjecie] = pygame.transform.scale(obraz, (szerokosc, wysokosc)).convert_alpha()

        self.surface.blit(variables.Locations.Location_Quiz_Pytanie.zdjecia[variables.Locations.Location_Quiz_Pytanie.zdjecie], ((self.surface.get_width() - variables.Locations.Location_Quiz_Pytanie.zdjecia[variables.Locations.Location_Quiz_Pytanie.zdjecie].get_width()) / 2, variables.Locations.Location_Quiz_Pytanie.pytanie_label.text_surface.get_height() - self.slider_y.value))
        if variables.Locations.Location_Quiz_Pytanie.zdjecie <= len(variables.Locations.Location_Quiz_Pytanie.zdjecia) - 2:
            variables.Locations.Location_Quiz_Pytanie.nastepne_zdjecie_button.y = variables.Locations.Location_Quiz_Pytanie.zdjecie_y - self.slider_y.value
            variables.Locations.Location_Quiz_Pytanie.nastepne_zdjecie_button.real_y = variables.Locations.Location_Quiz_Pytanie.zdjecie_y + 144 * variables.ustawienia['Skalowanie'] - self.slider_y.value
            if variables.Locations.Location_Quiz_Pytanie.nastepne_zdjecie_button.draw() or ('right' in variables.pressed_keys and variables.pressed_keys['right'][1] == 1):
                variables.Locations.Location_Quiz_Pytanie.zdjecie += 1
        if variables.Locations.Location_Quiz_Pytanie.zdjecie > 0:
            variables.Locations.Location_Quiz_Pytanie.poprzednie_zdjecie_button.y = variables.Locations.Location_Quiz_Pytanie.zdjecie_y - self.slider_y.value
            variables.Locations.Location_Quiz_Pytanie.poprzednie_zdjecie_button.real_y = variables.Locations.Location_Quiz_Pytanie.zdjecie_y + 144 * variables.ustawienia['Skalowanie'] - self.slider_y.value
            if variables.Locations.Location_Quiz_Pytanie.poprzednie_zdjecie_button.draw() or ('left' in variables.pressed_keys and variables.pressed_keys['left'][1] == 1):
                variables.Locations.Location_Quiz_Pytanie.zdjecie -= 1

        if variables.Locations.Location_Quiz_Pytanie.ustawienia_pytania['Typ odpowiedzi'] == 'Wpisz tekst':
            self.twoja_odpowiedz_label.y = variables.Locations.Location_Quiz_Pytanie.zdjecie_y + 74 * variables.ustawienia['Skalowanie'] - self.slider_y.value
            p = "".join([f"\n - {p[0]} ({p[1]})" for p in variables.Locations.Location_Quiz_Pytanie.ustawienia_pytania["Poprawne odpowiedzi"]])
            self.twoja_odpowiedz_label.edit_text(f'{variables.jezyk["Odpowiedź"]["Twoja odpowiedź"]}: {variables.Locations.Location_Quiz_Pytanie.odpowiedz_entry.text}\n\n{variables.jezyk["Odpowiedź"]["Poprawne odpowiedzi"]}: {p}')
            self.twoja_odpowiedz_label.draw()

        variables.window.blit(self.surface, (10 * variables.ustawienia['Skalowanie'], 144 * variables.ustawienia['Skalowanie']))
        self.slider_y.max = variables.Locations.Location_Quiz_Pytanie.zdjecie_y + 124 * variables.ustawienia['Skalowanie'] + self.twoja_odpowiedz_label.text_surface.get_height() - self.surface.get_height()
        if self.slider_y.max < 1:
            self.slider_y.max = 1
        self.slider_y.draw()

        if variables.Locations.Location_Quiz_Pytanie.poprawna_odpowiedz:
            self.odpowiedz_poprawna_label.draw()
        else:
            self.odpowiedz_nie_poprawna_label.draw()

        if variables.Locations.Location_Lista.dalej_button.draw() or 'return' in variables.pressed_keys and variables.pressed_keys['return'][1] == 3:
            variables.lokalizacja = 'Quiz_Pytanie'
            variables.Locations.Location_Quiz_Pytanie.nastepne_pytanie()

class Location_Quiz_wynik():
    def __init__(self):
        self.zakoncz_button = widgets.Button(variables.window, (20 * variables.ustawienia['Skalowanie'], variables.ustawienia['Wysokość'] - 116 * variables.ustawienia['Skalowanie']), ('assets/Buttons/close.png', (96, 96)))
        self.powtorz_button = widgets.Button(variables.window, (variables.ustawienia['Szerokość'] - 116 * variables.ustawienia['Skalowanie'], variables.ustawienia['Wysokość'] - 116 * variables.ustawienia['Skalowanie']), ('assets/Buttons/restart.png', (96, 96)))
        self.ukonczyles_quiz_label = widgets.Label(variables.window, (10 * variables.ustawienia['Skalowanie'], 20 * variables.ustawienia['Skalowanie']), None, f'{variables.jezyk["Wyniki"]["Ukończono quiz"]}', 60, (50, 230, 50), max_width=variables.ustawienia['Szerokość'] - 20 * variables.ustawienia['Skalowanie'], wyrownaj_do='middle')
        self.informacje_label = widgets.Label(variables.window, (10 * variables.ustawienia['Skalowanie'], 30 * variables.ustawienia['Skalowanie'] + self.ukonczyles_quiz_label.text_surface.get_height()), None, '', 40, (255, 255, 255), max_width=variables.ustawienia['Szerokość'] - 20 * variables.ustawienia['Skalowanie'], wyrownaj_do='middle')
        # self.slider_y = widgets.Slider_Y(variables.window, (variables.ustawienia['Szerokość'] - 50 * variables.ustawienia['Skalowanie'], self.informacje_label.y + self.informacje_label.text_surface.get_height() + 10 * variables.ustawienia['Skalowanie']), (30, variables.ustawienia['Wysokość'] - 146 * variables.ustawienia['Skalowanie'] - self.informacje_label.y - self.informacje_label.text_surface.get_height()), (100, 100, 100), 5, (0, 0, 0), (50, 50, 50))
        # self.odpowiedzi_surface = pygame.Surface((variables.ustawienia['Szerokość'] - 65 * variables.ustawienia['Skalowanie'], self.slider_y.size[1]))

    def draw(self):
        self.ukonczyles_quiz_label.draw()
        self.informacje_label.draw()

        # pygame.draw.rect(variables.window, (0, 0, 0), (10 * variables.ustawienia['Skalowanie'], self.slider_y.y, self.odpowiedzi_surface.get_width() + 10 * variables.ustawienia['Skalowanie'], self.slider_y.size[1] + 10 * variables.ustawienia['Skalowanie']))
        # self.odpowiedzi_surface.fill((80, 80, 80))
        #
        # variables.window.blit(self.odpowiedzi_surface, (15 * variables.ustawienia['Skalowanie'], self.slider_y.y + 5 * variables.ustawienia['Skalowanie']))
        # self.slider_y.draw()

        if self.zakoncz_button.draw():
            variables.lokalizacja = 'Lista'
        if self.powtorz_button.draw():
            variables.Locations.Location_Kolejnosc.rozpocznij_quiz()

class Location_Stworz_gre():
    def __init__(self):
        self.surface = pygame.Surface((variables.ustawienia['Szerokość'] - 60 * variables.ustawienia['Skalowanie'], variables.ustawienia['Wysokość'] - 94 * variables.ustawienia['Skalowanie']))
        self.slider_y = widgets.Slider_Y(variables.window, (variables.ustawienia['Szerokość'] - 50 * variables.ustawienia['Skalowanie'], 84 * variables.ustawienia['Skalowanie']), (30 * variables.ustawienia['Skalowanie'], self.surface.get_height() - 10 * variables.ustawienia['Skalowanie']), (100, 100, 100), 5, (0, 0, 0), (50, 50, 50))
        self.label = widgets.Label(self.surface, (0, 0), None, f'{variables.jezyk["Stwórz quiz"]["Niedostępne"]}', 40, (255, 255, 255), max_width=self.surface.get_width())

    def draw(self):
        if variables.Locations.Location_Lista.ustawienia_button.draw():
            variables.lokalizacja = 'Ustawienia'
        if variables.Locations.Location_Lista.info_button.draw():
            variables.lokalizacja = 'Informacje'
        if variables.Locations.Location_Lista.lista_quizow_button.draw():
            variables.lokalizacja = 'Lista'
        if variables.Locations.Location_Lista.stworz_quiz_button.draw():
            variables.lokalizacja = 'Stwórz quiz'

        self.surface.fill((30, 30, 30))
        self.label.draw()
        variables.window.blit(self.surface, (10 * variables.ustawienia['Skalowanie'], 84 * variables.ustawienia['Skalowanie']))
        if self.slider_y.max != 1:
            self.slider_y.draw()

class Location_Zapisywanie():
    def __init__(self):
        self.label = widgets.Label(variables.window, (10 * variables.ustawienia['Skalowanie'], 84 * variables.ustawienia['Skalowanie']), None, f'{variables.jezyk["Zapisywanie"]["Niedostępne"]}', 40, (255, 255, 255), max_width=variables.ustawienia['Szerokość'] - 20 * variables.ustawienia['Skalowanie'])

    def draw(self):
        self.label.draw()
        if variables.Locations.Location_Kolejnosc.powrot_button.draw():
            variables.lokalizacja = 'Lista'

class Location_Wczytywanie():
    def __init__(self):
        self.label = widgets.Label(variables.window, (10 * variables.ustawienia['Skalowanie'], 84 * variables.ustawienia['Skalowanie']), None, f'{variables.jezyk["Wczytywanie"]["Niedostępne"]}', 40, (255, 255, 255), max_width=variables.ustawienia['Szerokość'] - 20 * variables.ustawienia['Skalowanie'])

    def draw(self):
        self.label.draw()
        if variables.Locations.Location_Kolejnosc.powrot_button.draw():
            variables.lokalizacja = 'Lista'

class Locations():
    def __init__(self):
        self.FPS = widgets.FPS()
        self.Music = widgets.Music(True)
        self.Music.zmien_liste_odtwarzania(['uplifting-loop-cheerful-happiness-297034.mp3', 'sneaky-world-middle-eastern-loop-291260.mp3'])

        self.Location_Ustawienia = Location_Ustawienia()
        self.Location_Inforamcje = Location_Inforamcje()
        self.Location_Lista = Location_Lista()
        self.Location_Kolejnosc = Location_Kolejnosc()
        self.Location_Quiz_Pytanie = Location_Quiz_Pytanie()
        self.Location_Quiz_Odpowiedz = Location_Quiz_Odpowiedz()
        self.Location_Quiz_wynik = Location_Quiz_wynik()
        self.Location_Stworz_gre = Location_Stworz_gre()
        self.Location_Zapisywanie = Location_Zapisywanie()
        self.Location_Wczytywanie = Location_Wczytywanie()


    def draw(self):
        if variables.lokalizacja == 'Ustawienia':
            self.Location_Ustawienia.draw()
        elif variables.lokalizacja == 'Informacje':
            self.Location_Inforamcje.draw()
        elif variables.lokalizacja == 'Lista':
            self.Location_Lista.draw()
        elif variables.lokalizacja == 'Kolejność':
            self.Location_Kolejnosc.draw()
        elif variables.lokalizacja == 'Quiz_Pytanie':
            self.Location_Quiz_Pytanie.draw()
        elif variables.lokalizacja == 'Quiz_Odpowiedź':
            self.Location_Quiz_Odpowiedz.draw()
        elif variables.lokalizacja == 'Quiz_Wynik':
            self.Location_Quiz_wynik.draw()
        elif variables.lokalizacja == 'Stwórz quiz':
            self.Location_Stworz_gre.draw()
        elif variables.lokalizacja in ('Zapisywanie', 'Zapisywanie_Kolejności'):
            self.Location_Zapisywanie.draw()
        elif variables.lokalizacja == 'Wczytywanie':
            self.Location_Wczytywanie.draw()

        self.FPS.draw()
        self.Music.graj_muzyke()
