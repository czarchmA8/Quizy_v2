import json
from random import randrange
from threading import Thread
from math import sqrt, atan2
from PIL import Image
import pygame
from pyperclip import copy as clipboard_copy
from pyperclip import paste as clipboard_paste

import variables

def zapisz_ustawienia():
    with open('settings.json', 'w', encoding='utf-8') as f:
        json.dump(variables.ustawienia, f, indent=2)

def zaladuj_obraz(lokalizacja: str, rozdzielczosc: float | tuple, convert_alpha: bool=True, skalowanie: bool=True):
    obraz = pygame.image.load(lokalizacja)
    if skalowanie:
        obraz = pygame.transform.scale(obraz, (rozdzielczosc[0] * variables.ustawienia['Skalowanie'], rozdzielczosc[1] * variables.ustawienia['Skalowanie']))
    else:
        obraz = pygame.transform.scale(obraz, rozdzielczosc)
    if convert_alpha:
        obraz = obraz.convert_alpha()
    else:
        obraz = obraz.convert()
    return obraz

def graj_dzwiek(lokalizacja, glosnosc):
    def dzwiek():
        dzwiek = pygame.mixer.Sound(f'assets/Sounds/{lokalizacja}')
        dzwiek.set_volume(glosnosc)
        kanal = dzwiek.play()
        clock = pygame.time.Clock()
        while kanal.get_busy():
            clock.tick(5)

    Thread(target=dzwiek, daemon=True).start()

class Music():
    def __init__(self, losowo: bool):
        self.losowo: bool = losowo
        self.lista_muzyk: dict = {}
        self.lista_odtwarzania: list = []
        self.teraz_grana_muzyka = ''
        self.kanal = None

    def zmien_liste_odtwarzania(self, lista_lokalizacji: list):
        if self.lista_odtwarzania != lista_lokalizacji:
            self.lista_odtwarzania = lista_lokalizacji
            for lokalizacja in self.lista_odtwarzania:
                if lokalizacja not in self.lista_muzyk:
                    self.lista_muzyk[lokalizacja] = pygame.mixer.Sound(f'assets/Music/{lokalizacja}')
            self.teraz_grana_muzyka = self.lista_odtwarzania[randrange(0, len(self.lista_odtwarzania))]
            self.kanal = None

    def graj_muzyke(self):
        if not variables.running:
            self.kanal.stop()
        elif self.kanal and self.kanal.get_busy():
            self.kanal.set_volume(variables.ustawienia['Głośność']['Ogólne'] * variables.ustawienia['Głośność']['Muzyka'] / 10000)
        else:
            if len(self.lista_odtwarzania) > 1 and self.losowo:
                self.lista_odtwarzania.remove(self.teraz_grana_muzyka)
                wylosowana_muzyka = self.lista_odtwarzania[randrange(0, len(self.lista_odtwarzania))]
                self.lista_odtwarzania.append(self.teraz_grana_muzyka)
                self.teraz_grana_muzyka = wylosowana_muzyka
            else:
                self.teraz_grana_muzyka = self.lista_odtwarzania.index(self.teraz_grana_muzyka) + 1
                if self.teraz_grana_muzyka >= len(self.lista_odtwarzania):
                    self.teraz_grana_muzyka = 0
                self.teraz_grana_muzyka = self.lista_odtwarzania[self.teraz_grana_muzyka]

            self.kanal = self.lista_muzyk[self.teraz_grana_muzyka].play()
            self.kanal.set_volume(variables.ustawienia['Głośność']['Ogólne'] * variables.ustawienia['Głośność']['Muzyka'] / 10000)

class GIF():
    def __init__(self, surface, pos, lokalizacja: str, powieksz: float | tuple[int, int]=1):
        self.surface = surface
        self.pos = pos
        gif = Image.open(lokalizacja)
        gif_duration = gif.info.get('duration', 100)
        self.frames = []
        for frame in range(gif.n_frames):
            gif.seek(frame)
            frame_surface = pygame.image.fromstring(gif.tobytes(), gif.size, gif.mode)
            if isinstance(powieksz, tuple):
                frame_surface = pygame.transform.scale(frame_surface, powieksz).convert_alpha()
            else:
                frame_surface = pygame.transform.scale(frame_surface, (frame_surface.get_width() * powieksz, frame_surface.get_height() * powieksz)).convert_alpha()
            self.frames.append(frame_surface)
        self.ilosc_klatek_w_klatce_gry = 1 / (gif_duration / (1000 / 60))
        self.frame_index = 1

    def draw(self):
        self.frame_index += self.ilosc_klatek_w_klatce_gry
        if self.frame_index > len(self.frames):
            self.frame_index = 1 + self.frame_index - int(self.frame_index)
        self.surface.blit(self.frames[int(self.frame_index)], self.pos)

class Label():
    def __init__(self, surface, pos: tuple[int, int], font: str, text: str, text_size: int, text_color: tuple, text_bg: tuple=None, max_width: int=None, wyrownaj_do: str='left'):
        self.surface = surface
        self.x, self.y = pos
        self.text = None
        self.text_size = int(text_size * variables.ustawienia['Skalowanie'])
        self.text_color = text_color
        self.text_bg = text_bg
        self.font = pygame.font.Font(font, self.text_size)
        self.max_width = max_width
        self.wyrownaj_do = wyrownaj_do
        self.text_surface = pygame.Surface((1, 1))

        self.edit_text(text)

    def draw(self):
        self.surface.blit(self.text_surface, (self.x, self.y))

    def edit_text(self, text):
        if text == '':
            self.text = text
            self.text_surface = pygame.Surface((1, 1))
        elif self.text != text:
            self.text = text
            lines = []
            paragraphs = text.splitlines()

            for paragraph in paragraphs:
                words = paragraph.split(" ")
                current_line = ""
                for word in words:
                    # if word == "":
                        # Jeśli mamy kilka spacji z rzędu – pomijamy puste elementy
                        # continue

                    # Przygotowujemy testową linię – jeśli current_line nie jest puste, dodajemy spację
                    test_line = current_line + (" " if current_line else "") + word
                    if not self.max_width or self.font.size(test_line)[0] <= self.max_width:
                        current_line = test_line
                    else:
                        # Jeśli aktualna linia nie jest pusta, zapisujemy ją i rozpoczynamy nową
                        if current_line:
                            lines.append(current_line)
                            current_line = ""
                        # Sprawdzamy, czy samo słowo mieści się w limicie
                        if not self.max_width or self.font.size(word)[0] <= self.max_width:
                            current_line = word
                        else:
                            # Słowo jest za długie – dzielimy je na fragmenty
                            broken_parts = []
                            current_part = ""
                            for char in word:
                                test_part = current_part + char
                                if not self.max_width or self.font.size(test_part)[0] <= self.max_width:
                                    current_part = test_part
                                else:
                                    if current_part:  # Zapisujemy dotychczasowy fragment
                                        broken_parts.append(current_part)
                                    # Rozpoczynamy nowy fragment od aktualnego znaku
                                    current_part = char
                            if current_part:
                                broken_parts.append(current_part)

                            # Dodajemy wszystkie fragmenty poza ostatnim jako osobne linie
                            for part in broken_parts[:-1]:
                                lines.append(part)
                            # Ostatni fragment zapisujemy jako początek nowej linii
                            current_line = broken_parts[-1]
                # Dodajemy linię z akapitu (nawet jeśli jest pusta)
                lines.append(current_line)

            max_width = 0
            for index, line in enumerate(lines):
                lines[index] = self.font.render(line, False, self.text_color, self.text_bg)
                if lines[index].get_width() > max_width:
                    max_width = lines[index].get_width()

            self.text_surface = pygame.Surface((self.max_width if self.max_width else max_width, self.text_size * len(lines)), pygame.SRCALPHA)
            if self.text_bg:
                self.text_surface.fill(self.text_bg)
            for index, line in enumerate(lines):
                if self.wyrownaj_do == 'left':
                    x = 0
                elif self.wyrownaj_do == 'middle':
                    x = (self.text_surface.get_width() - line.get_width()) / 2
                elif self.wyrownaj_do == 'right':
                    x = self.text_surface.get_width() - line.get_width()
                self.text_surface.blit(line, (x, self.text_size * index + (self.text_size - line.get_height()) / 2))

class Button():
    def __init__(self, surface, pos: tuple, image: tuple=None, image2: tuple=None, spacing: int=0, font: str=None, text_size: int=None, text: str=None, text_color: tuple[int, int, int]=(255, 255, 255), text_bg_color: tuple=None, real_pos: tuple=None):
        self.surface = surface
        self.x, self.y = pos
        if real_pos:
            self.real_x, self.real_y = real_pos
        else:
            self.real_x, self.real_y = self.x, self.y
        self.text_bg_color = text_bg_color

        if image:
            button_image = zaladuj_obraz(image[0], image[1])
            if image2:
                button_image2 = zaladuj_obraz(image2[0], image2[1])
            elif image2 is False:
                button_image2 = button_image
            else:
                if isinstance(image[1], tuple):
                    button_image2 = zaladuj_obraz(image[0], (image[1][0] * 1.1, image[1][1] * 1.1))
                else:
                    button_image2 = zaladuj_obraz(image[0], image[1] * 1.1)

            if button_image.get_height() > button_image2.get_height():
                max_wysokosc = button_image.get_height()
            else:
                max_wysokosc = button_image2.get_height()
            if button_image.get_width() > button_image2.get_width():
                max_szerokosc = button_image.get_width()
            else:
                max_szerokosc = button_image2.get_width()
        else:
            max_szerokosc = 0

        if text:
            text = pygame.font.Font(font, text_size if text_size else max_wysokosc).render(text, False, text_color)
            if not image:
                max_wysokosc = text_size

        self.button_surface = pygame.Surface((max_szerokosc + (text.get_width() if text else 0) + spacing, max_wysokosc), pygame.SRCALPHA)
        if image:
            self.button_surface.blit(button_image, ((max_szerokosc - button_image.get_width()) / 2, (max_wysokosc - button_image.get_height()) / 2))
        if text:
            self.button_surface.blit(text, (max_szerokosc + spacing, (max_wysokosc - text.get_height()) / 2))

        self.button_surface2 = pygame.Surface((max_szerokosc + (text.get_width() if text else 0) + spacing, max_wysokosc), pygame.SRCALPHA)
        if image:
            self.button_surface2.blit(button_image2, ((max_szerokosc - button_image2.get_width()) / 2, (max_wysokosc - button_image2.get_height()) / 2))
        else:
            self.button_surface2.fill(text_bg_color)
        if text:
            self.button_surface2.blit(text, (max_szerokosc + spacing, (max_wysokosc - text.get_height()) / 2))

    def draw(self) -> bool:
        self.surface.blit(self.button_surface, (self.x, self.y))
        if pygame.Rect(self.real_x, self.real_y, self.button_surface.get_width(), self.button_surface.get_height()).collidepoint(variables.mouse_x, variables.mouse_y):
            self.surface.blit(self.button_surface2, (self.x, self.y))
            if variables.mouse_pressed[0] == 3:
                return True
        return False

class Entry():
    def __init__(self, surface, pos: tuple, size: tuple,
                 font: str | None, font_color: tuple, bg_color: tuple,
                 border_width: int, border_color: tuple,
                 placeholder_font: str | None, placeholder_text: str, placeholder_text_color: tuple,
                 touching_bg_color: tuple, touching_border_color: tuple,
                 clicked_bg_color: tuple, clicked_border_color: tuple,
                 max: int=-1, black_list=None, white_list=None, readonly: bool=False,
                 real_pos: tuple=None):
        self.surface = surface
        self.x, self.y = pos
        if real_pos:
            self.real_x, self.real_y = real_pos
        else:
            self.real_x, self.real_y = self.x, self.y
        self.size: tuple | list = int(size[0]), int(size[1])
        self.font = pygame.font.Font(font, self.size[1])
        self.font_color: tuple | list = font_color
        self.bg_color: tuple | list = bg_color
        self.border_width: int = border_width * variables.ustawienia["Skalowanie"]
        self.border_color: tuple | list = border_color
        self.placeholder_font: str = placeholder_font
        self.placeholder_text: str = placeholder_text
        self.placeholder_text_color: tuple | list = placeholder_text_color
        self.touching_bg_color: tuple | list = touching_bg_color
        self.touching_border_color: tuple | list = touching_border_color
        self.clicked_bg_color: tuple | list = clicked_bg_color
        self.clicked_border_color: tuple | list = clicked_border_color
        self.max: int = max
        self.black_list: list = black_list
        self.white_list: list = white_list
        self.readonly: bool = readonly

        self.clicked: bool = False
        self.text: str = ''
        self.text_changed: bool = False
        self.enter: bool = False
        self.zaznaczony_tekst: list = [0, 0]
        self.stary_zaznaczony_tekst: list = None
        self.zaznaczanie_tekstu: bool = False
        self.widoczny_tekst: int = 0
        self.miganie_czas = pygame.time.get_ticks()
        self.cursor_width: int = self.font.size((' '))[0] // 2
        if self.cursor_width < 1:
            self.cursor_width = 1

        self.update_placeholder()

        self.visible_text_surface = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)
        self.full_text_surface = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)
        self.zaznaczony_tekst_surface = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)

    def draw(self):
        self.text_changed = False
        self.enter = False
        clicked = self.clicked
        touching = pygame.Rect(self.real_x, self.real_y, self.size[0] + self.border_width * 2, self.size[1] + self.border_width * 2).collidepoint(variables.mouse_x, variables.mouse_y)

        # Wyświetlanie ramki i tła Entry
        if self.clicked:
            pygame.draw.rect(self.surface, self.clicked_border_color, (self.x, self.y, self.size[0] + self.border_width * 2, self.size[1] + self.border_width * 2))
            pygame.draw.rect(self.surface, self.clicked_bg_color, (self.x + self.border_width, self.y + self.border_width, self.size[0], self.size[1]))

            # Wyświetlanie zaznaczonego tekstu
            if self.text != '':
                if self.zaznaczony_tekst[0] != self.zaznaczony_tekst[1] or pygame.time.get_ticks() - self.miganie_czas < 500:
                    self.surface.blit(self.zaznaczony_tekst_surface, (self.x + self.border_width, self.y + self.border_width))
                elif pygame.time.get_ticks() - self.miganie_czas >= 1000:
                    self.miganie_czas = pygame.time.get_ticks()
        else:
            if touching:
                pygame.draw.rect(self.surface, self.touching_border_color, (self.x, self.y, self.size[0] + self.border_width * 2, self.size[1] + self.border_width * 2))
                pygame.draw.rect(self.surface, self.touching_bg_color, (self.x + self.border_width, self.y + self.border_width, self.size[0], self.size[1]))
            else:
                pygame.draw.rect(self.surface, self.border_color, (self.x, self.y, self.size[0] + self.border_width * 2, self.size[1] + self.border_width * 2))
                pygame.draw.rect(self.surface, self.bg_color, (self.x + self.border_width, self.y + self.border_width, self.size[0], self.size[1]))

        # Wyświetlanie tekstu lub tekstu podpowiedzi
        if self.text == '':
            self.surface.blit(self.placeholder_text_surface, (self.x + self.border_width, self.y + self.border_width))
        else:
            self.surface.blit(self.visible_text_surface, (self.x + self.border_width, self.y + self.border_width))

        if self.clicked:
            # Zaznaczanie tekstu za pomocą myszki
            if self.zaznaczanie_tekstu:
                if variables.mouse_pressed[0] == 2:
                    for index in range(len(self.text) + 1):
                        if self.widoczny_tekst + variables.mouse_x - self.real_x <= self.font.size(self.text[:index])[0]:
                            self.zaznaczony_tekst[1] = index - 1
                            break
                    else:
                        self.zaznaczony_tekst[1] = len(self.text) + 1
                elif variables.mouse_pressed[0] == 3:
                    self.zaznaczanie_tekstu = False
            elif touching and variables.mouse_pressed[0] == 1:
                self.zaznaczanie_tekstu = True
                self.miganie_czas = pygame.time.get_ticks()
                for index in range(len(self.text)):
                    if self.widoczny_tekst + variables.mouse_x - self.real_x <= self.font.size(self.text[:index])[0]:
                        self.zaznaczony_tekst[0] = index - 1
                        break
                else:
                    self.zaznaczony_tekst[0] = len(self.text) + 1
                self.zaznaczony_tekst[1] = self.zaznaczony_tekst[0]

            # Dodawanie znaków do tekstu
            for key in variables.TextInput:
                if ((not self.white_list or key in self.white_list) and
                    (not self.black_list or key not in self.black_list) and
                    (self.max == -1 or len(self.text) <= self.max)):
                    self.text = self.text[:min(self.zaznaczony_tekst)] + key + self.text[max(self.zaznaczony_tekst):]
                    self.text_changed = True
                    self.zaznaczony_tekst[0] = self.zaznaczony_tekst[1] = self.zaznaczony_tekst[0] + 1 if self.zaznaczony_tekst[0] == self.zaznaczony_tekst[1] else min(self.zaznaczony_tekst) + 1

            # Funkcjonalność klawiszy specjalnych
            for key in variables.pressed_keys:
                if variables.pressed_keys[key]["state"] == 1 or (variables.pressed_keys[key]["state"] == 2 and variables.pressed_keys[key]["key_held_triggered"]):
                    if key == 'backspace' or key == 'delete':
                        if self.zaznaczony_tekst[0] == self.zaznaczony_tekst[1]:
                            a = 0 if min(self.zaznaczony_tekst) - 1 < 0 else min(self.zaznaczony_tekst) - 1
                        else:
                            a = min(self.zaznaczony_tekst)
                        self.text = self.text[:a] + self.text[max(self.zaznaczony_tekst):]
                        self.text_changed = True
                        self.zaznaczony_tekst[0] = self.zaznaczony_tekst[1] = self.zaznaczony_tekst[0] - 1 if self.zaznaczony_tekst[0] == self.zaznaczony_tekst[1] else min(self.zaznaczony_tekst)
                    elif key == 'return':
                        self.enter = True
                        self.clicked = False
                        break
                    elif key == 'escape':
                        self.clicked = False
                        break
                    elif key == 'left':
                        if 'left shift' in variables.pressed_keys:
                            self.zaznaczony_tekst[1] -= 1
                        else:
                            if self.zaznaczony_tekst[0] == self.zaznaczony_tekst[1]:
                                self.zaznaczony_tekst[0] = self.zaznaczony_tekst[1] = self.zaznaczony_tekst[0] - 1
                            else:
                                self.zaznaczony_tekst[0] = self.zaznaczony_tekst[1] = min(self.zaznaczony_tekst)
                        self.miganie_czas = pygame.time.get_ticks()
                    elif key == 'right':
                        if 'left shift' in variables.pressed_keys:
                            self.zaznaczony_tekst[1] += 1
                        else:
                            if self.zaznaczony_tekst[0] == self.zaznaczony_tekst[1]:
                                self.zaznaczony_tekst[0] = self.zaznaczony_tekst[1] = self.zaznaczony_tekst[0] + 1
                            else:
                                self.zaznaczony_tekst[0] = self.zaznaczony_tekst[1] = max(self.zaznaczony_tekst)
                        self.miganie_czas = pygame.time.get_ticks()
                    elif key == 'a' and 'left ctrl' in variables.pressed_keys and 'right alt' not in variables.pressed_keys:
                        self.zaznaczony_tekst[0] = 0
                        self.zaznaczony_tekst[1] = len(self.text)
                    elif key == 'c' and 'left ctrl' in variables.pressed_keys and 'right alt' not in variables.pressed_keys:
                        clipboard_copy(self.text[min(self.zaznaczony_tekst):max(self.zaznaczony_tekst)])
                    elif key == 'v' and 'left ctrl' in variables.pressed_keys and 'right alt' not in variables.pressed_keys and isinstance(clipboard_paste(), str):
                        self.text = self.text[:min(self.zaznaczony_tekst)] + clipboard_paste() + self.text[max(self.zaznaczony_tekst):]
                        self.text_changed = True
                        self.zaznaczony_tekst[0] = self.zaznaczony_tekst[1] = self.zaznaczony_tekst[0] + len(clipboard_paste())

            self.update_selected_text()

            # Aktualizacja wyświetlania tekstu
            if self.text_changed:
                self.update_text()
                self.miganie_czas = pygame.time.get_ticks()

            if not touching and variables.mouse_pressed[0] == 1:
                self.clicked = False
        elif touching and variables.mouse_pressed[0] == 1:
            self.clicked = True

        if self.clicked != clicked: # Aktywowanie klawiatury ekranowej na telefonie
            if self.clicked:
                pygame.key.start_text_input()
            else:
                pygame.key.stop_text_input()

    def update_selected_text(self, check_changes: bool=True):
        if self.stary_zaznaczony_tekst != self.zaznaczony_tekst or not check_changes:
            self.stary_zaznaczony_tekst = self.zaznaczony_tekst[:]
            # regulacja zaznaczonego tekstu
            if self.zaznaczony_tekst[0] < 0:
                self.zaznaczony_tekst[0] = 0
            elif self.zaznaczony_tekst[0] > len(self.text):
                self.zaznaczony_tekst[0] = len(self.text)
            if self.zaznaczony_tekst[1] < 0:
                self.zaznaczony_tekst[1] = 0
            elif self.zaznaczony_tekst[1] > len(self.text):
                self.zaznaczony_tekst[1] = len(self.text)

            # Aktualizacja widzanego tekstu
            x_zaznaczonego_tekstu = self.font.size(self.text[:self.zaznaczony_tekst[1]])[0]
            if x_zaznaczonego_tekstu + self.cursor_width > self.widoczny_tekst + self.size[0]:
                self.widoczny_tekst = x_zaznaczonego_tekstu + self.cursor_width - self.size[0]
                self.update_text_position()
            elif x_zaznaczonego_tekstu < self.widoczny_tekst:
                self.widoczny_tekst = x_zaznaczonego_tekstu
                self.update_text_position()

            # Aktualizacja wyświetlania zaznaczonego tekstu
            x = self.font.size(self.text[:min(self.zaznaczony_tekst)])[0] - self.widoczny_tekst
            x = x if x > 0 else 0
            if self.zaznaczony_tekst[0] == self.zaznaczony_tekst[1]:
                szerokosc = self.cursor_width
            else:
                szerokosc = self.font.size(self.text[min(self.zaznaczony_tekst):max(self.zaznaczony_tekst)])[0]
                if szerokosc + x > self.size[0]:
                    szerokosc = self.size[0] - x
            self.zaznaczony_tekst_surface = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)
            pygame.draw.rect(self.zaznaczony_tekst_surface, (0, 0, 0), (x, 0, szerokosc, self.size[1]))

    def update_placeholder(self):
        self.placeholder_text_surface = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)
        placeholder_text = self.font.render(self.placeholder_text, False, self.placeholder_text_color)
        self.placeholder_text_surface.blit(placeholder_text, (0, (self.size[1] - placeholder_text.get_height()) / 2))

    def update_text(self, check_changes: bool=True):
        self.full_text = self.font.render(self.text, False, self.font_color)
        self.update_text_position()
        self.update_selected_text(check_changes)

    def update_text_position(self):
        self.visible_text_surface = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)
        self.visible_text_surface.blit(self.full_text, (-self.widoczny_tekst, (self.size[1] - self.full_text.get_height()) // 2))

    def set_text(self, text):
        if text != self.text:
            self.text = text
            self.zaznaczony_tekst[0] = self.zaznaczony_tekst[1] = len(self.text)
            self.widoczny_tekst = 0
            self.update_text(False)

    def size_changed(self):
        self.zaznaczony_tekst[0] = self.zaznaczony_tekst[1] = len(self.text)
        self.widoczny_tekst = 0
        self.update_text(False)

class Slider():
    def __init__(self, surface, pos: tuple, size: tuple, bg_color: tuple,
                 border_width: int, border_color: tuple,
                 button_color: tuple,
                 min: int=0, max: int=100, init_value: int=0, real_pos: tuple=None):
        self.surface = surface
        self.x, self.y = pos
        if real_pos:
            self.real_x, self.real_y = real_pos
        else:
            self.real_x, self.real_y = self.x, self.y
        self.size = size
        self.bg_color = bg_color
        self.border_width = border_width * variables.ustawienia['Skalowanie']
        self.border_color = border_color
        self.button_color = button_color
        self.min = min
        self.max = max
        self.value = init_value
        self.button_x = (self.value - self.min) / (self.max - self.min) * (self.size[0] - self.size[1])
        self.clicked = False

        self.bg_surface = pygame.Surface((self.size[0] + self.border_width*2, self.size[1] + self.border_width*2))
        self.bg_surface.fill(border_color)
        pygame.draw.rect(self.bg_surface, self.bg_color, (self.border_width, self.border_width, self.size[0], self.size[1]))

    def draw(self) -> bool:
        self.surface.blit(self.bg_surface, (self.x, self.y))

        if self.clicked:
            if variables.mouse_pressed[0] == 0:
                self.clicked = False
            self.button_x = variables.mouse_x - self.real_x - self.border_width - self.size[1] / 2
            if self.button_x < 0:
                self.button_x = 0
            elif self.button_x > self.size[0] - self.size[1]:
                self.button_x = self.size[0] - self.size[1]
            self.value = self.min + (self.button_x / (self.size[0] - self.size[1])) * (self.max - self.min)

        elif variables.mouse_pressed[0] == 1 and pygame.Rect(self.real_x + self.border_width + self.button_x, self.real_y + self.border_width, self.size[1], self.size[1]).collidepoint(variables.mouse_x, variables.mouse_y):
            self.clicked = True

        pygame.draw.rect(self.surface, self.button_color, (self.x + self.border_width + self.button_x, self.y + self.border_width, self.size[1], self.size[1]))
        return self.clicked

    def set_value(self, value):
        if value > self.max:
            value = self.max
        if value < self.min:
            value = self.min
        self.value = value
        self.button_x = (self.value - self.min) / (self.max - self.min) * (self.size[0] - self.size[1])

class Slider_Y():
    def __init__(self, surface, pos: tuple, size: tuple, bg_color: tuple,
                 border_width: int, border_color: tuple,
                 button_color: tuple,
                 min: int = 0, max: int = 100, init_value: int = 0, real_pos: tuple = None):
        self.surface = surface
        self.x, self.y = pos
        if real_pos:
            self.real_x, self.real_y = real_pos
        else:
            self.real_x, self.real_y = self.x, self.y
        self.size = size
        self.bg_color = bg_color
        self.border_width = border_width * variables.ustawienia['Skalowanie']
        self.border_color = border_color
        self.button_color = button_color
        self.min = min
        self.max = max
        self.value = init_value
        self.button_y = (self.value - self.min) / (self.max - self.min) * (self.size[1] - self.size[0])
        self.clicked = False

    def draw(self) -> bool:
        bg_surface = pygame.Surface((self.size[0] + self.border_width * 2, self.size[1] + self.border_width * 2))
        bg_surface.fill(self.border_color)
        pygame.draw.rect(bg_surface, self.bg_color, (self.border_width, self.border_width, self.size[0], self.size[1]))
        self.surface.blit(bg_surface, (self.x, self.y))

        if self.clicked:
            if variables.mouse_pressed[0] == 0:
                self.clicked = False
            self.button_y = variables.mouse_y - self.real_y - self.border_width - self.size[0] / 2
            if self.button_y < 0:
                self.button_y = 0
            elif self.button_y > self.size[1] - self.size[0]:
                self.button_y = self.size[1] - self.size[0]
            self.value = self.min + (self.button_y / (self.size[1] - self.size[0])) * (self.max - self.min)

        elif variables.mouse_pressed[0] == 1 and pygame.Rect(self.real_x + self.border_width, self.real_y + self.border_width + self.button_y, self.size[0], self.size[0]).collidepoint(variables.mouse_x, variables.mouse_y):
            self.clicked = True

        pygame.draw.rect(self.surface, self.button_color, (self.x + self.border_width, self.y + self.border_width + self.button_y, self.size[0], self.size[0]))
        return self.clicked

    def set_value(self, value):
        if value > self.max:
            value = self.max
        if value < self.min:
            value = self.min
        self.value = value
        self.button_y = (self.value - self.min) / (self.max - self.min) * (self.size[1] - self.size[0])

class CheckBox():
    def __init__(self, surface, pos: tuple,
                 options: list,
                 # options: List[
                 #     Tuple[
                 #         Tuple[str, Union[int, float, tuple[int, int]]], # (lokalizacja_obrazu, rozmiar)
                 #         Optional[str], # czcionka
                 #         Optional[int], # rozmiar_czcionki
                 #         Optional[str], # tekst
                 #         Optional[Tuple[int, int, int]] # kolor_tekstu
                 #     ]
                 # ],
                 # [((lokalizacja_obrazu, rozmiar), czcionka, rozmiar_czcionki, tekst, kolor_tekstu)...]
                 # [(('assets/Buttons/not_visible.png', (48, 48)), None, None, None, None), (('assets/Buttons/visible2.png', (48, 48)), None, None, None, None)]
                 real_pos: tuple=None):
        self.surface = surface
        self.x, self.y = pos
        if real_pos:
            self.real_x, self.real_y = real_pos
        else:
            self.real_x, self.real_y = self.x, self.y

        self.buttons = []
        for image, font, font_size, text, text_color in options:
            self.buttons.append(Button(self.surface, (0, 0), image, None, 0, font, font_size, text, text_color))

        self.value = 0

    def draw(self) -> bool:
        self.buttons[self.value].x, self.buttons[self.value].y = self.x, self.y
        self.buttons[self.value].real_x, self.buttons[self.value].real_y = self.real_x, self.real_y
        if self.buttons[self.value].draw():
            self.value += 1
            if self.value >= len(self.buttons):
                self.value = 0
            return True
        else:
            return False

class OptionMenu():
    def __init__(self):
        pass

    def draw(self):
        pass

class ProgressBar():
    def __init__(self, surface, pos: tuple[int, int], size: tuple[int, int], bg_color: tuple[int, int, int],
                 border_width: int, border_color: tuple[int, int, int], color: tuple[int, int, int],
                 min: int=0, max: int=100, init_value: int = 0, real_pos: tuple[int, int]=None):
        self.surface = surface
        self.x, self.y = pos
        if real_pos:
            self.real_x, self.real_y = real_pos
        else:
            self.real_x, self.real_y = self.x, self.y
        self.size = size
        self.bg_color = bg_color
        self.border_width = border_width * variables.ustawienia["Skalowanie"]
        self.border_color = border_color
        self.color = color
        self.min = min
        self.max = max
        self.value = (init_value - self.min) / (self.max - self.min) * self.size[0]
        self.ProgressBar_surface = pygame.Surface((size[0]+self.border_width*2, size[1]+self.border_width*2))
        self.ProgressBar_surface.fill(border_color)
        pygame.draw.rect(self.ProgressBar_surface, self.bg_color, (self.border_width, self.border_width, size[0], size[1]))

    def draw(self):
        self.surface.blit(self.ProgressBar_surface, (self.x, self.y))
        pygame.draw.rect(self.surface, self.color, (self.real_x+self.border_width, self.real_y+self.border_width, self.value, self.size[1]))

    def set_value(self, value):
        if value > self.max:
            value = self.max
        if value < self.min:
            value = self.min
        self.value = (value - self.min) / (self.max - self.min) * self.size[0]

class Tooltip():
    def __init__(self, rect, time: int, font: str, text: str, text_size: int, text_color: tuple, text_bg_color: tuple, text_border_width: int, text_border_color: tuple, spacing: int):
        self.rect = pygame.Rect(rect)
        self.time = time
        self.czas = None
        self.text = pygame.font.Font(font, text_size).render(text, False, text_color, text_bg_color)
        self.text_surface = pygame.Surface((self.text.get_width() + text_border_width*2 + spacing*2, self.text.get_height() + text_border_width*2 + spacing*2))
        self.text_surface.fill(text_border_color)
        pygame.draw.rect(self.text_surface, text_bg_color, (text_border_width, text_border_width, self.text.get_width() + spacing*2, self.text.get_height() + spacing*2))
        self.text_surface.blit(self.text, (text_border_width + spacing, text_border_width + spacing))
        self.text_surface_width = self.text_surface.get_width()
        self.text_surface_height = self.text_surface.get_height()

    def draw(self):
        if self.rect.collidepoint(variables.mouse_x, variables.mouse_y):
            if self.czas is not None:
                if self.czas <= 0:
                    x = variables.mouse_x
                    if x + self.text_surface_width > 1920:
                        x = 1920 - self.text_surface_width

                    y = variables.mouse_y - self.text_surface_height
                    if y < 0:
                        y = 0

                    variables.window.blit(self.text_surface, (x, y))
                else:
                    self.czas -= 1
            else:
                self.czas = self.time
        else:
            self.czas = None

class Joystick():
    def __init__(self, suface, pos: tuple[int, int], radius: int, bg_color: tuple[int, int, int], border_width: int, border_color: tuple[int, int, int],
                 button_radius: int, button_bg_color: tuple[int, int, int], button_border_width: int, button_border_color: tuple[int, int, int], returnToCenter: bool=True, real_pos: tuple[int, int]=None):
        self.suface = suface
        self.x, self.y = pos
        if real_pos:
            self.real_x, self.real_y = real_pos
        else:
            self.real_x, self.real_y = pos
        self.radius = radius
        self.bg_color = bg_color
        self.border_width = border_width
        self.border_color = border_color
        self.button_radius = button_radius
        self.button_bg_color = button_bg_color
        self.button_border_width = button_border_width
        self.button_border_color = button_border_color
        self.returnToCenter = returnToCenter
        self.clicked = False
        self.button_x, self.button_y = self.x, self.y

    def draw(self):
        if self.clicked:
            distance = sqrt((self.real_x - variables.mouse_x) ** 2 + (self.real_y - variables.mouse_y) ** 2)
            self.button_x, self.button_y = variables.mouse_x - self.real_x + self.x, variables.mouse_y - self.real_y + self.y
            if distance >= self.radius:
                dx = self.button_x - self.x
                dy = self.button_y - self.y

                length = sqrt(dx ** 2 + dy ** 2)
                if length != 0:
                    normalized_dx = dx / length
                    normalized_dy = dy / length

                    self.button_x, self.button_y = (int(self.x + normalized_dx * self.radius), int(self.y + normalized_dy * self.radius))

            if variables.mouse_pressed[0] == 0:
                self.clicked = False
                if self.returnToCenter:
                    self.button_x, self.button_y = self.x, self.y

        elif variables.mouse_pressed[0] == 1 and sqrt((self.real_x - self.x + self.button_x - variables.mouse_x) ** 2 + (self.real_y - self.y + self.button_y - variables.mouse_y) ** 2) <= self.button_radius:
            self.clicked = True

        pygame.draw.circle(self.suface, self.border_color, (self.x, self.y), self.radius + self.border_width)
        pygame.draw.circle(self.suface, self.bg_color, (self.x, self.y), self.radius)

        pygame.draw.circle(self.suface, self.button_border_color, (self.button_x, self.button_y), self.button_radius + self.button_border_width)
        pygame.draw.circle(self.suface, self.button_bg_color, (self.button_x, self.button_y), self.button_radius)

        return self.clicked

    def get_direction(self) -> tuple[float, tuple[int, int]]:
        dx = self.button_x - self.x
        dy = self.button_y - self.y
        angle = atan2(dy, dx)
        return angle, (dx, dy)

    def get_distance(self) -> float:
        dx = self.button_x - self.x
        dy = self.button_y - self.y
        return sqrt(dx ** 2 + dy ** 2)

class FPS():
    def __init__(self):
        self.klatki_na_sekunde = []
        self.fps_text = pygame.Surface((0, 0))
        self.fps_text_cien = pygame.Surface((0, 0))
        self.font_fps = pygame.font.Font(None, round(variables.ustawienia['FPS']['Rozmiar FPS'] * variables.ustawienia['Skalowanie']))
        self.font_fps_cien = pygame.font.Font(None, round(variables.ustawienia['FPS']['Rozmiar FPS cienia'] * variables.ustawienia['Skalowanie']))
        self.start = pygame.time.get_ticks()

    def draw(self):
        if variables.ustawienia['FPS']['Pokaż FPS']:
            self.klatki_na_sekunde.append(round(variables.clock.get_fps()))
            if pygame.time.get_ticks() - self.start >= variables.ustawienia["FPS"]["Odświeżanie"]:
                self.fps_text = self.font_fps.render(f'FPS: {round(sum(self.klatki_na_sekunde) / len(self.klatki_na_sekunde))}', False, variables.ustawienia['FPS']['Kolor FPS'])
                self.fps_text_cien = self.font_fps_cien.render(f'FPS: {round(sum(self.klatki_na_sekunde) / len(self.klatki_na_sekunde))}', False, variables.ustawienia['FPS']['Kolor FPS cienia'])
                self.klatki_na_sekunde = []
                self.start = pygame.time.get_ticks()

            variables.window.blit(self.fps_text_cien, (variables.ustawienia['FPS']['xy FPS cienia'][0] * variables.ustawienia['Skalowanie'], variables.ustawienia['FPS']['xy FPS cienia'][1] * variables.ustawienia['Skalowanie']))
            variables.window.blit(self.fps_text, (variables.ustawienia['FPS']['xy FPS'][0] * variables.ustawienia['Skalowanie'], variables.ustawienia['FPS']['xy FPS'][1] * variables.ustawienia['Skalowanie']))
