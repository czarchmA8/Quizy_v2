from time import time
from colorama import Fore, Style
import json
import pygame
pygame.init()

import variables
from locations import Locations
from widgets import zaladuj_obraz

def main():
    print(f'[{Fore.YELLOW}Main{Style.RESET_ALL}] {Fore.YELLOW}Ładowanie...{Style.RESET_ALL}')
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
        # if variables.ustawienia['Wysokość'] > variables.ustawienia['Szerokość']:
        variables.ustawienia['Skalowanie'] = variables.ustawienia['Wysokość'] / 1000
        # else:
        #     variables.ustawienia['Skalowanie'] = variables.ustawienia['Szerokość'] / 1000

    print(f'[{Fore.GREEN}Info{Style.RESET_ALL}] Rozdzielczość okna: {variables.ustawienia["Szerokość"]} x {variables.ustawienia["Wysokość"]}{Style.RESET_ALL}')
    print(f'[{Fore.GREEN}Info{Style.RESET_ALL}] Skalowanie: {variables.ustawienia["Skalowanie"]}{Style.RESET_ALL}')
    print(f'[{Fore.GREEN}Info{Style.RESET_ALL}] Język: {variables.ustawienia["Język"]}{Style.RESET_ALL}')

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
    variables.window.blit(zaladuj_obraz('assets/Background/loading.png', (variables.ustawienia['Szerokość'], variables.ustawienia['Wysokość'])), (0, 0))
    pygame.display.update()
    variables.Locations = Locations()

    print(f'[{Fore.YELLOW}Main{Style.RESET_ALL}] {Fore.GREEN}Załadowano w {round(time() - loading_time, 3)}s{Style.RESET_ALL}')

    variables.clock = pygame.time.Clock()
    variables.pressed_keys = {}
    while variables.run:
        variables.mouse_pressed = list(pygame.mouse.get_pressed())
        variables.mouse_pressed[0] = int(variables.mouse_pressed[0])
        variables.mouse_pressed[1] = int(variables.mouse_pressed[1])
        variables.mouse_pressed[2] = int(variables.mouse_pressed[2])

        usun_key = []
        for key in variables.pressed_keys:
            if variables.pressed_keys[key][1] == 1:
                variables.pressed_keys[key][1] = 2
            elif variables.pressed_keys[key][1] == 3:
                usun_key.append(key)
        for key in usun_key:
            variables.pressed_keys.pop(key)

        variables.TextInput = []
        variables.mouse_scroll = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                variables.run = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 1 <= event.button <= 3:
                    variables.mouse_pressed[event.button - 1] = 2
            elif event.type == pygame.MOUSEBUTTONUP:
                if 1 <= event.button <= 3:
                    variables.mouse_pressed[event.button - 1] = 3
            elif event.type == pygame.KEYDOWN:
                variables.pressed_keys[pygame.key.name(event.key)] = [event.unicode, 1]
            elif event.type == pygame.KEYUP:
                variables.pressed_keys[pygame.key.name(event.key)] = [event.unicode, 3]
            elif event.type == pygame.TEXTINPUT:
                variables.TextInput.append(event.text)
            elif event.type == pygame.MOUSEWHEEL:
                variables.mouse_scroll = event.y

        variables.mouse_x, variables.mouse_y = pygame.mouse.get_pos()

        variables.window.fill((30, 30, 30))
        variables.Locations.draw()

        pygame.display.update()
        variables.clock.tick(60)
    pygame.display.quit()

if __name__ == '__main__':
    variables.run = True
    variables.lokalizacja = 'Lista'
    print(f"[{Fore.GREEN}Info{Style.RESET_ALL}] Wersja: {variables.wersja}{Style.RESET_ALL}")
    while variables.run:
        main()
        if type(variables.run) is int and variables.run == 0:
            variables.run = True

pygame.quit()