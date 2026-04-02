2-04-26

Organización:

├── a-maze-ing
│   ├── README.md
│   ├── __init__.py
│   ├── a_maze_ing.py
│   ├── config
│   │   ├── __init__.py
│   │   ├── parser.py
│   │   └── validator.py
│   ├── config.txt
│   ├── maze.txt
│   ├── mazegen
│   │   ├── __init__.py
│   │   └── maze_generator.py
│   └── ui
│       ├── __init__.py
│       ├── display.py
│       └── header.txt
└── project-notes

5 directories, 13 files

Raiz contiene el main, archivo config.txt, se crea el archivo que contiene la representación en hexadecimal del laberinto y README.md

/config: contiene el script de parseo y el de validación
/mazegen: contiene el script que genera el laberinto. En ese archivo solo debería ir lo estrictamente para generar un laberinto con su solución.
/ui: contiene el script para visualizar el laberinto y el archivo que contiene el header en texto.

Está implementado el algoritmo Kruskal para crear el laberinto y el DFS (Depth-First Search) para encontrar la solución. El kruskal revisa parejas de celdas contiguas, las "añade" a un parent y quita las dos paredes que las unen (ex, si una está al lado de la otra, quita la pared derecha de una y la izquierda de la otra).
*Discplaimer: Esto se supone que crea un laberinto perfecto, pero tengo un vacio de entendimiento porque lo que determina si es perfecto es la celda de entrada y de salida.
El algoritmo DFS es para encontrar la salida: desde la celda entry_xy revisa todas las celdas a las que puede acceder, va guardando de que celda viene y que dirección tomó y guarda tambien las celdas exploradas. Cuando llega a exit_xy tiene guardado el camino que le llevó hasta allí.

Paso a paso rápido:

El programa se inicia ejecutando python3 a_maze_ing.py config.txt

- Se ejecuta el script de parseo que devuelve un diccionario
- Los valores de ese diccionario se usan para inicializar el objeto Maze
- Una vez creado, se ejecuta el método _generate_maze, que verifica qué celdas tendrán el patron 42, crea un grid de objetos "Cell" para las celdas, organiza las tuplas de paredes en una lista que luego "desordena" y aplica el algoritmo Kruskal para eliminar paredes aleatoriamente.
- luego, para mostrarlo usa la función display que recibe el laberinto y el patron 42 para poderlo imprimir. 
- finalmente crea el archivo que guarda la representación hexadecimal del laberinto.



==== Cosas que faltan: ====

- El laberinto debe tener la opción de ser perfecto. Ya se supone que lo es, asi que hay que ver como hacemos que sea imperfecto tambien.
- Falta el script validator, debería verificar que entry_xy y exit_exy esté dentro del rango de width y height y que no esté dentro del patron 42.
- Falta que, si el laberinto es muy pequeño para mostrar el patron 42, salga un mensaje, no tengo claro si tiene que mostrarse el laberinto o no.
- Del parseo falta toda la parte de la interfaz de usuario. El laberinto debería mostrar un menú que permita: mostrar y ocultar la solución, cambiar el laberinto de color, generar un nuevo laberinto y salir.
- En el script de maze_generator.py está la función de crear el archivo maze.txt, no debería estar ahí.
- Todo lo que tenga que ver con la norma, flake8, docstrings, y probablemente hints también.

Y seguramente muchas cosas más, pero eso es lo principal por ahora.