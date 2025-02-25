from vpython import *
import asyncio
import math
import random

scene = canvas(title="Movimiento y Transformaciones en VPython", width=800, height=600)


conos = []
cabezas = []
for i in range(5):
    cono = cone(pos=vector(-5 + i * 1.5, 0, 0), radius=0.8 ** i, length=1.6 * (0.8 ** i), axis=vector(0,1,0), color=color.blue)
    cabeza = sphere(pos=vector(-5 + i * 1.5, 1.6 * (0.8 ** i), 0), radius=(0.4 * (0.8 ** i)), color=color.yellow)
    conos.append(cono)
    cabezas.append(cabeza)


cubo = box(pos=vector(-2, 0, 0), size=vector(1, 1, 1), color=color.red)
esfera = sphere(pos=vector(0, 0, 0), radius=1, color=color.green)

time_step = 0.05  
direccion_conos = 1  

def reset_positions():
    for i in range(len(conos)):
        conos[i].pos = vector(-5 + i * 1.5, 0, 0)
        cabezas[i].pos = vector(-5 + i * 1.5, 1.6 * (0.8 ** i), 0)

def change_colors():
    for i in range(len(conos)):
        conos[i].color = vector(random.random(), random.random(), random.random())
        cabezas[i].color = vector(random.random(), random.random(), random.random())

def handle_key(evt):
    if evt.key == "r":
        reset_positions()
    elif evt.key == "c":
        change_colors()

scene.bind("keydown", handle_key)

async def mover_y_cambiar_objeto(objeto, cabeza, tipo):
    t = 0
    global direccion_conos
    while True:
        if tipo == "cubo":
            objeto.pos.z = 2 * math.sin(t)  
            objeto.size = vector(1 + 0.5 * math.cos(t), 1, 1)  
            objeto.color = vector(abs(math.cos(t)), 0.2, abs(math.sin(t)))  
        elif tipo == "esfera":
            objeto.pos.x = 2 * math.cos(t)
            objeto.pos.y = 2 * math.sin(t) 
            objeto.radius = 0.5 + 0.5 * abs(math.sin(t))  
            objeto.color = vector(0.2, abs(math.sin(t)), abs(math.cos(t))) 
        elif tipo == "conos":
            objeto.pos.x += direccion_conos * 0.1
            cabeza.pos.x += direccion_conos * 0.1  
            if objeto.pos.x > 3 or objeto.pos.x < -5:
                direccion_conos *= -1  
        
        t += time_step
        await asyncio.sleep(time_step)

async def main():
    task1 = asyncio.create_task(mover_y_cambiar_objeto(cubo, None, "cubo"))
    task2 = asyncio.create_task(mover_y_cambiar_objeto(esfera, None, "esfera"))
    tasks_conos = [asyncio.create_task(mover_y_cambiar_objeto(conos[i], cabezas[i], "conos")) for i in range(len(conos))]
    await asyncio.gather(task1, task2, *tasks_conos)

asyncio.run(main())