# Entrega: OpenRAVE
Este repositorio contiene la generación de laberinto con un robot en Python, moviendo el robot desde el origen hasta la meta. Este desplazamiento se consigue mediante el uso de un script de Python que mueve al robot utilizando OpenAI.

Autor: **Pedro Arias Pérez**

Link: [pariaspe/openai-playground](https://github.com/pariaspe/openai-playground)


## Índice
- [1. Descripción](#1-descripción)
- [2. Estructura de Carpetas](#2-estructura-de-carpetas)
- [3. Base](#3-base)
- [4. Extras](#4-extras)
    - [4.1. Extra 1](#extra-1-vídeo-parte-base)
    - [4.2. Extra 2](#extra-2-algoritmos-de-planificación)
    - [4.3. Extra 3](#extra-3-nuevo-entorno)
    - [4.4. Extra 4](#extra-4-vídeo-parte-extra)

---

## 1. Descripción
Para la práctica se han realizado los siguientes hitos:

- **Base**:
    1. Se presenta un script de python que controla al robot para que alcance la meta sobre un mapa sencillo (map1).

- **Extra**:
    1. Se presenta un **vídeo** que muestra la ejecución de la parte base.
    2. Se añade un **planificador** que calcula la ruta a seguir por el robot.
    3. Se ha creado un **nuevo entorno** de OpenAi Gym.
    4. Se adjunta un **vídeo** que muestra la ejecución de la parte extra.

## 2. Estructura de carpetas
El esquema de organización del repositorio es el siguiente:
```
.
+-- docs (imgs..)
+-- gym-csv
    +-- examples
        +-- gym-csv-display.py
        +-- gym-csv-loop.py
        +-- map1.csv
    +-- gym_csv
        +-- envs
            +-- __init__.py
            +-- csv_env.py
            +-- csv_pygame_env.py
            +-- csv_colored_env.py
        +-- __init__.py
    +-- README.md
    +-- setup.py
+-- tools
    +-- alg_hub.py
    +-- astar.py
    +-- bfs.py
    +-- dfs-py
    +-- dijkstra.py
    +-- utils.py
+-- base.py
+-- extra-py
+-- map1.csv
+-- README.md
```

## 3. Base
Tras finalizar la instalación del entorno `gym-csv` se calculan las dimensiones del mapa:

```bash
parias@parias-msi:~/repos/gazebo-tools$ python3
Python 3.6.9 (default, Oct  8 2020, 12:12:24)
[GCC 8.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> x = len("arias")*2
>>> y = len("perez")*2
>>> print(x, y)
10 10
>>>
```

Dadas estas dimensiones `(10x10)` se ha construído el siguiente mapa en formato csv `(map1.csv)`:

```bash
parias@parias-msi:~/repos/openai-playground$ cat gym-csv/examples/map1.csv
1,1,1,1,1,1,1,1,1,1
1,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,1
1,1,1,1,0,0,0,0,0,1
1,1,1,1,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,1
1,1,1,1,1,1,1,1,1,1
```

Se ha elegido un mapa muy sencillo con una resolución de un metro por caracter. El inicio será la posición `[2,2]` (fila 3, columna 3), mientras que la meta será en la posición `[7,7]` (fila 8, columna 8), siguiendo las intrucciones que indican las posiciones de inicio y final.

Utilizando `gym-csv-dipslay.py` se muestra el mapa generado:

```bash
parias@parias-msi:~/repos/openai-playground/gym-csv/examples$ python gym-csv-display.py
pygame 2.0.0 (SDL 2.0.12, python 3.6.9)
Hello from the pygame community. https://www.pygame.org/contribute.html
[[1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]
 [1. 0. 0. 0. 0. 0. 0. 0. 0. 1.]
 [1. 0. 2. 0. 0. 0. 0. 0. 0. 1.]
 [1. 0. 0. 0. 0. 0. 0. 0. 0. 1.]
 [1. 1. 1. 1. 0. 0. 0. 0. 0. 1.]
 [1. 1. 1. 1. 0. 0. 0. 0. 0. 1.]
 [1. 0. 0. 0. 0. 0. 0. 0. 0. 1.]
 [1. 0. 3. 0. 0. 0. 0. 0. 0. 1.]
 [1. 0. 0. 0. 0. 0. 0. 0. 0. 1.]
 [1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]]
```

Utilizando el entorno `csv-pygame-v0` ligeramente modificado, obtenemos:

![csv-pygame-v0](/docs/env.png)

Tras tener el entorno listo se crea el siguiente código (`base.py`) en python que se encarga de controlar al robot para que llegue a su destino. En primer lugar se carga el entorno, en este caso utilizamos `csv-pygame-v0`, pero el algoritmo sería el mismo para otros entornos. A continuación, se ejecutan dos bucles que se encargan de mover al robot (actualizando el estado) primero a la derecha y después hacia abajo hasta llegar a la meta.

**NOTA**: El entorno ha sido modificado, ya que según el archivo csv original, las columnas y filas estaban intercambiadas en el entorno. Este pequeño error también se puede observar entre ambos entornos, donde el mapa no es idéntico, ya que las filas y columnas se encuentran intercambiadas.

```python
#!/usr/bin/env python

import gym
import gym_csv

import numpy as np
import time

# X points down (rows)(v), Y points right (columns)(>), Z would point outwards.
RIGHT = 0  # > Increase Y (column)
UP = 1  # ^ Decrease X (row)
LEFT = 2 # < Decrease Y (column)
DOWN = 3    # v Increase X (row)

SIM_PERIOD_MS = 500.0

env = gym.make('csv-pygame-v0')
state = env.reset()
print("state: " + str(state))
env.render()
time.sleep(0.5)

for i in range(5):
    new_state, reward, done, _ = env.step(RIGHT)
    env.render()
    print("new_state: " + str(new_state) + ", reward: " + str(reward) + ", done: " + str(done))
    time.sleep(SIM_PERIOD_MS/1000.0)


for i in range(6):
    new_state, reward, done, _ = env.step(DOWN)
    env.render()
    print("new_state: " + str(new_state) + ", reward: " + str(reward) + ", done: " + str(done))
    time.sleep(SIM_PERIOD_MS/1000.0)
```

## 4. Extras
### Extra 1: Vídeo parte base

Se muestra en vídeo el resultado de la ejecución de la parte base.

[![OpenAI Gym Base](http://img.youtube.com/vi/-FdJp9hCBXU/0.jpg)](http://www.youtube.com/watch?v=-FdJp9hCBXU)

### Extra 2: Algoritmos de planificación

Se añade un planificador que calcula la ruta a seguir por el robot para alcanzar la meta. El algoritmo de planificación utilizado puede elegirse entre DFS, BFS, Dijkstra y A*, modificando el parametro `alg` de la función `get_route`. La parte más relevante del nuevo código se muestra a continuación:

```python
env = gym.make('csv-pygame-v0')
state = env.reset()
print("state: " + str(state))
env.render()
time.sleep(0.5)

# Algorithms available: dfs, bfs, dijkstra, astar
route = alg_hub.get_route("map1", START, GOAL, alg="dijkstra")

done = False
while not done:
    try:
        pos = route.pop(0)  # next step
        next_state = pos[0] + pos[1]*10
        command = get_command(state, next_state)
        if command == 4:  # actual pos, continue
            continue
        elif command == -1:
            print("[Error] Bad command.")
            break
    except IndexError:
        command = 0  # no more steps

    state, reward, done, _ = env.step(command)
    env.render()
    print("new_state: " + str(state) + ", reward: " + str(reward) + ", done: " + str(done))
    time.sleep(SIM_PERIOD_MS/1000.0)
```

### Extra 3: Nuevo entorno

Se ha creado un nuevo entorno para OpenAI Gym. El nuevo entorno es un entorno de texto con caracteres ANSI que permiten aportar colores para consolas UNIX. El entorno no aporta grandes mejoras, pero se ha explorado la opción de crear nuevos entornos.

Para crear un entorno, se ha registrado el nuevo entorno en `gym-csv/gym_csv/__init__.py`:

```python
from gym.envs.registration import register

register(
    id='csv-v0',
    entry_point='gym_csv.envs:CsvEnv',
)
register(
    id='csv-pygame-v0',
    entry_point='gym_csv.envs:CsvPyGameEnv',
)
register(
    id='csv-colored-v0',
    entry_point='gym_csv.envs:CsvColoredEnv',
)
```

Además, se ha añadido el import con `CsvColoredEnv` al fichero `gym-csv/gym_csv/envs/__init__.py`:

```python
from gym_csv.envs.csv_env import CsvEnv
from gym_csv.envs.csv_pygame_env import CsvPyGameEnv
from gym_csv.envs.csv_colored_env import CsvColoredEnv
```
El código completo del entorno se puede ver en el fichero `csv_colored_env.py`.
Si ejecutamos el script `gym-csv-display.py` observamos el siguiente entorno:

![csv-colored-v0](/docs/new_env.png)

### Extra 4: Vídeo Parte Extra

El siguiente vídeo muestra un planificador Dijkstra sobre el nuevo entorno creado.

[![OpenAI Gym Extra](http://img.youtube.com/vi/0z0vXWQ-Y64/0.jpg)](http://www.youtube.com/watch?v=0z0vXWQ-Y64)
