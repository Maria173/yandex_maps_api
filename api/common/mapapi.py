#coding:utf-8
import pygame
import requests
import sys
import os


def show_map(ll1=None, ll2=None, map_type="map", add_params=None):
    if ll1 and ll2:
        map_request = "http://static-maps.yandex.ru/1.x/?ll={ll1},{ll2}&z=10&l={map_type}".format(**locals())

    else:
        map_request = "http://static-maps.yandex.ru/1.x/?l={map_type}".format(**locals())

    if add_params:
        map_request += "&" + add_params
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запишем полученное изображение в файл.
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)

    # Инициализируем pygame
    pygame.init() 

    screen = pygame.display.set_mode((600, 450))

    # Рисуем картинку, загружаемую из только что созданного файла.
    screen.blit(pygame.image.load(map_file), (0, 0))
    # Переключаем экран и ждем закрытия окна.
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass

    pygame.quit()
    # Удаляем за собой файл с изображением.
    os.remove(map_file)
