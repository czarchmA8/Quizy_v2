from time import time
import json
import pygame
pygame.init()

import variables
from locations import Locations
from widgets import zaladuj_obraz

def main():
    print(f'[Main] Ładowanie...')
    loading_time = time()

    # Wczytywanie ustawień
    with open('settings.json', 'r', encoding='utf-8') as file:
        variables.ustawienia = json.load(file)

    info = pygame.display.Info()
    if type(variables.ustawienia['Szerokość']) is not int:
        variables.ustawienia['Szerokość'] = info.current_w
    if type(variables.ustawienia['Wysokość']) is not int:
        variables.ustawienia['Wysokość'] = info.current_h

    if type(variables.ustawienia['Skalowanie']) is not int and type(variables.ustawienia['Skalowanie']) is not float:
        variables.ustawienia['Skalowanie'] = variables.ustawienia['Wysokość'] / 1000

    print(f'[Info] Rozdzielczość okna: {variables.ustawienia["Szerokość"]} x {variables.ustawienia["Wysokość"]}')
    print(f'[Info] Skalowanie: {variables.ustawienia["Skalowanie"]}')
    print(f'[Info] Język: {variables.ustawienia["Język"]}')

    # Wczytywanie języka
    with open(f'languages/{variables.ustawienia["Język"]}/translation.json', 'r', encoding='utf-8') as file:
        variables.jezyk = json.load(file)

    # Tworzenie okna
    pygame.display.set_caption(variables.jezyk['Nazwa okna'])
    if variables.ustawienia['Pełny ekran']:
        variables.window = pygame.display.set_mode((variables.ustawienia['Szerokość'], variables.ustawienia['Wysokość']), pygame.FULLSCREEN | pygame.SCALED)
    else:
        variables.window = pygame.display.set_mode((variables.ustawienia['Szerokość'], variables.ustawienia['Wysokość']))
    pygame.display.set_icon(zaladuj_obraz('icon.png', (64, 64)))

    # Wczytywanie lokalizacji
    variables.window.blit(zaladuj_obraz('assets/Background/loading.png', (variables.ustawienia['Szerokość'], variables.ustawienia['Wysokość']), False, False), (0, 0))
    pygame.display.update()
    variables.Locations = Locations()

    print(f'[Main] Załadowano w {round(time() - loading_time, 3)}s')

    variables.clock = pygame.time.Clock()
    variables.pressed_keys = {}
    while variables.running:
        variables.mouse_pressed = list(pygame.mouse.get_pressed())
        for i in range(len(variables.mouse_pressed)):
            variables.mouse_pressed[i] = int(variables.mouse_pressed[i]) * 2

        usun_key = []
        for key in variables.pressed_keys:
            if variables.pressed_keys[key]["state"] == 1:
                variables.pressed_keys[key]["state"] = 2
            elif variables.pressed_keys[key]["state"] == 2:
                variables.pressed_keys[key]["key_held_triggered"] = False
                if pygame.time.get_ticks() - variables.pressed_keys[key][
                    "clicked_time"] >= 500 and pygame.time.get_ticks() - variables.pressed_keys[key][
                    "last_trigger_time"] >= 50:
                    variables.pressed_keys[key]["last_trigger_time"] = pygame.time.get_ticks()
                    variables.pressed_keys[key]["key_held_triggered"] = True
            elif variables.pressed_keys[key]["state"] == 3:
                usun_key.append(key)
        for key in usun_key:
            variables.pressed_keys.pop(key)

        variables.TextInput = []
        variables.mouse_scroll = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                variables.running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 1 <= event.button <= 3:
                    variables.mouse_pressed[event.button - 1] = 1
            elif event.type == pygame.MOUSEBUTTONUP:
                if 1 <= event.button <= 3:
                    variables.mouse_pressed[event.button - 1] = 3
            elif event.type == pygame.KEYDOWN:
                variables.pressed_keys[pygame.key.name(event.key)] = {"unicode": event.unicode, "state": 1, "clicked_time": pygame.time.get_ticks(), "last_trigger_time": pygame.time.get_ticks(), "key_held_triggered": False}
            elif event.type == pygame.KEYUP:
                variables.pressed_keys[pygame.key.name(event.key)] = {"unicode": event.unicode, "state": 3}
            elif event.type == pygame.TEXTINPUT:
                variables.TextInput.append(event.text)
            elif event.type == pygame.MOUSEWHEEL:
                variables.mouse_scroll = event.y

        variables.mouse_x, variables.mouse_y = pygame.mouse.get_pos()

        variables.window.fill((30, 30, 30))
        variables.Locations.draw()

        pygame.display.update()
        variables.clock.tick(variables.ustawienia['FPS']['Max FPS'])

if __name__ == '__main__':
    variables.running = True
    variables.lokalizacja = 'Lista'
    print(f"[Info] Wersja: {variables.wersja}")
    while variables.running:
        main()
        if type(variables.running) is int and variables.running == 0:
            variables.running = True
    pygame.display.quit()

pygame.quit()