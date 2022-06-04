import random

import matplotlib.pyplot as plt
import geopy.distance
import math
from random import randrange

# ------------------ Definições ----------------------
min_distancia_alinhar = 1
arquivo = "pizza.txt"
cortar_lista = True


# arquivo = "random"

def dist_pontos(A, B):
    return geopy.distance.geodesic(A, B).km


def dist_reta(A, B, C, ):
    lat1 = math.radians(A[0])
    lon1 = math.radians(A[1])
    lat2 = math.radians(B[0])
    lon2 = math.radians(B[1])
    lat3 = math.radians(C[0])
    lon3 = math.radians(C[1])

    y = math.sin(lon3 - lon1) * math.cos(lat3)
    x = math.cos(lat1) * math.sin(lat3) - math.sin(lat1) * math.cos(lat3) * math.cos(lat3 - lat1)
    bearing1 = math.degrees(math.atan2(y, x))
    bearing1 = 360 - ((bearing1 + 360) % 360)

    y2 = math.sin(lon2 - lon1) * math.cos(lat2)
    x2 = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(lat2 - lat1)
    bearing2 = math.degrees(math.atan2(y2, x2))
    bearing2 = 360 - ((bearing2 + 360) % 360)

    lat1Rads = lat1
    lat3Rads = lat3
    dLon = lon3 - lon1

    distanceAC = math.acos(
        math.sin(lat1Rads) * math.sin(lat3Rads) + math.cos(lat1Rads) * math.cos(lat3Rads) * math.cos(dLon)) * 6371
    min_distance = math.fabs(
        math.asin(math.sin(distanceAC / 6371) * math.sin(math.radians(bearing1) - math.radians(bearing2))) * 6371)

    return min_distance


def make_list_from_geoson(file):
    list = []
    with open(file) as fp:
        for line in fp:
            if "coordinates" in line:
                lon = next(fp)
                lat = next((fp))

                lon = lon.replace(' ', '')
                lon = lon.replace(',', '')
                lon = lon.replace("\n", '')

                lat = lat.replace(' ', '')
                lat = lat.replace("\n", '')

                try:
                    lat = float(lat)
                    lon = float(lon)
                    list.append([lat, lon])
                except:
                    print("Erro em " + str(lat) + " se isso não é coordenada, ignore...")
                    print("Erro em " + str(lon) + " se isso não é coordenada, ignore...")
                    print("------------")


    if cortar_lista:
        while len(list) != 511:
            list.pop(random.randrange(len(list)))

    return list


def produce_random_coord(x0, y0, u, v, radius):
    radiusInDegrees = radius / 111000
    w = radiusInDegrees * math.sqrt(u)
    t = 2 * math.pi * v
    x = w * math.cos(t)
    y = w * math.sin(t)

    foundLatitude = x + x0
    foundLongitude = y + y0

    return (foundLatitude, foundLongitude)


def make_full_random_list(center, radius, total=511):
    lista = []

    for i in range(total):
        random_coord = produce_random_coord(center[0], center[1], random.uniform(0, 1), random.uniform(0, 1), radius)
        lista.append(random_coord)

    print(lista)
    return lista


def make_world_list():
    lista = []
    lista.append()

# ------------------ Código principal ----------------

lista_pontos_aleatoria_uk = make_full_random_list((54.23894321489787, -4.532166166908776), 440000, 1000)

if arquivo != "random":
    lista_pontos = make_list_from_geoson(arquivo)
else:
    lista_valida = make_list_from_geoson("megalitc-uk.geojson")
    lista_pontos = make_full_random_list(lista_valida[0], 243000)

print("0 - Imprimir mapa")
print("1 - Traçar linha de Ley e pontos que fazem parte dela")
print("2 - Checar n linhas de Ley candidatas")
print("3 - Checar se ponto está em uma linha de Ley ou intersecção")
print("4 - Checar se n pontos aleatórios estão em ao menos 3 linhas de Ley")
print("5 - Checar se n direções  aleatórias estão em linhas de Ley")
acao = int(input("O que deseja fazer? "))

if acao == 0:
    fig, ax = plt.subplots()
    ratio = 1.0
    x_left, x_right = ax.get_xlim()
    y_low, y_high = ax.get_ylim()
    ax.set_aspect(abs((x_right - x_left) / (y_low - y_high)) * ratio)

    for candidato in lista_pontos:
        try:
            plt.plot(candidato[1], candidato[0], marker=".", color="b", markersize=2)
        except:
            print("Error in " + str(candidato))
    plt.show()

if acao == 1:

    a = int(input("Insira o indice do ponto A: "))
    b = int(input("Insira o indice do ponto B: "))

    pa = lista_pontos[a]
    pb = lista_pontos[b]

    fig, ax = plt.subplots()
    ratio = 1.0
    x_left, x_right = ax.get_xlim()
    y_low, y_high = ax.get_ylim()
    ax.set_aspect(abs((x_right - x_left) / (y_low - y_high)) * ratio)

    for candidato in lista_pontos:
        if dist_reta(pa, pb, candidato) < min_distancia_alinhar:
            plt.plot(candidato[1], candidato[0], marker=".", color="r", markersize=2)
            print("Um sítio em: " + str(candidato[0]) + "," + str(candidato[1]))
        else:
            plt.plot(candidato[1], candidato[0], marker=".", color="k", markersize=1)

    plt.show()

if acao == 2:

    total = 0
    linhas_ley = 0
    scores = []

    iteracoes = int(input("Quantas tentativas quer fazer? "))

    for i in range(iteracoes):  # Para 100 coordenadas aleatórias da lista

        pA = lista_pontos[randrange(510)]
        pB = lista_pontos[randrange(510)]

        score = 0
        total = total + 1

        for valor in lista_pontos:  # Para cada coordenada na lista

            if valor != pA and valor != pB:

                distancia = dist_reta(pA, pB, valor)  # A coordenada está perto?
                if distancia < min_distancia_alinhar:
                    score = score + 1  # Se sim, score!

        if score > 1:
            linhas_ley = linhas_ley + 1

        scores.append(score)

    print("De um total de " + str(total) + ", " + str(linhas_ley) + " são linhas válidas.")

if acao == 3:
    #latP = float(input("Insira a latitude do local: "))
    #lonP = float(input("Insira a longitude do local: "))

    latP = 52.64167100598063
    lonP = -2.9544208970286885

    fig, ax = plt.subplots()
    ratio = 1.0
    x_left, x_right = ax.get_xlim()
    y_low, y_high = ax.get_ylim()
    ax.set_aspect(abs((x_right - x_left) / (y_low - y_high)) * ratio)

    ponto = (latP, lonP)
    total_linhas = 0

    for candidato_extremidade in lista_pontos:
        lista_na_linha = []
        for candidato_parte in lista_pontos:
            if dist_reta(ponto, candidato_extremidade,
                         candidato_parte) < min_distancia_alinhar and candidato_extremidade != candidato_parte:
                lista_pontos.pop(lista_pontos.index(candidato_parte))
                lista_na_linha.append(candidato_parte)

        if len(lista_na_linha) > 2:
            total_linhas = total_linhas + 1
            if total_linhas == 1:
                for k in lista_na_linha:
                    plt.plot(k[1], k[0], marker=".", color="r", markersize=3)
            elif total_linhas == 2:
                for k in lista_na_linha:
                    plt.plot(k[1], k[0], marker=".", color="b", markersize=3)
            elif total_linhas == 3:
                for k in lista_na_linha:
                    plt.plot(k[1], k[0], marker=".", color="g", markersize=3)

    plt.plot(ponto[1], ponto[0], marker="x", color="k", markersize=5)
    plt.show()

    print(total_linhas)

if acao == 4:
    total_cruz = 0
    total_ao_menos_1 = 0
    for aleatorio in lista_pontos_aleatoria_uk:
        total_linhas = 0
        for candidato_extremidade in lista_pontos:
            total_pontos = 0
            for candidato_parte in lista_pontos:
                if dist_reta(aleatorio, candidato_extremidade,
                             candidato_parte) < min_distancia_alinhar and candidato_extremidade != candidato_parte:
                    total_pontos = total_pontos + 1

            if total_pontos > 3:
                total_linhas = total_linhas + 1

            if total_linhas == 3:
                total_cruz = total_cruz + 1
                break

        if total_linhas > 1:
            total_ao_menos_1 = total_ao_menos_1 + 1

    print(total_cruz)
    print(total_ao_menos_1)

if acao == 5:

    total_direcoes = 0

    for i in range (1000):

        pontoA = lista_pontos_aleatoria_uk[random.randrange(len(lista_pontos_aleatoria_uk))]
        pontoB = lista_pontos_aleatoria_uk[random.randrange(len(lista_pontos_aleatoria_uk))]
        total_pontos = 0

        for candidato_parte in lista_pontos:
            if dist_reta(pontoA, pontoB, candidato_parte) < min_distancia_alinhar:
                total_pontos = total_pontos + 1
        if total_pontos >= 3:
            total_direcoes = total_direcoes + 1

    print(total_direcoes)