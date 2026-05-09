Laberintos perfectos e imperfectos. Desde el Maze generator

Verificar errores de impresion estatica y animada segun la resolucion de la pantalla. Averiguar que pasa aqui. 





**El algoritmo**

    *Kruskal*: Algoritmo que consiste en la mezcla de las paredes de cada celda del grafo, de manera aleatoria
    (con el uso de SEED y .random()) Siguiendo las siguientes normas:

        Analizo por cada pared: Las celdas que comparten esta pared, ya estan "conectadas" por otro lado? (por otro camino)
            Si lo estan: Dejo la pared intacta (si la rompo, armaria un bucle de caminos, por lo que el laberitno ya no seria perfecto.
            Si no lo estan: Rompo el muro (uniendo las celdas intervinientes en un mismo conjunto)

        Consideraciones: de toda celda que se analiza por primera vez, se convierte en Jefa de si misma:
            self.parent = self. Cada vez que esta habre un muro e interconecta una nueva celda, esta pasa a referenciar
            al mismo jefe que el de la anterior, que siempre sera la primera desde la que se inicio el cojunto, del cual
            ahora, pasara a ser parte.


        En cuanto a la salida. EL formato del output del maze-generator es en numeros hexadecimales, en la que cada
            valor representa el status de la totalidad de los muros que conforman una celda, donde se utiliza una
            mascara de bits y cada bit equivale a un muro segun su direccion cardinal:

            Bit 1 = N = 1
            Bit 2 = E = 2
            Bit 3 = S = 4
            Bit 4 = W = 8

        Entonces, la suma total de los valores relativos a cada Bit, señalaran el estado de los muros de la selda. Bit
        encendido(1) igual a muro existente(cerrado), bit apagado(0) igual a muro inexistente(abierto)


**COLOR_PALETTE & display()**

    Ambas estructuras utilizan la formula \033[. Esta  Indica que lo que sigue no es texto comun, sino un comando de control.

    En el caso de los colores, estos estan definidos por 3 valores, ej: "48;5;229m" Sus valores corresponden a:

        La estructura usa 3 partes principales separadas por punto y coma (;):

        1ro: Tipo de objetivo (48 o 38):
            38 significa Foreground (color del texto / letra).
            48 significa Background (color de fondo).

        2do: Formato elegido (5):
            El 5 le indica a la terminal que vas a usar la paleta extendida estándar de 256 colores (la paleta de 8 bits).

        3ro: Índice exacto del color (del 0 al 255):
            Ese número es el color específico que consultas de la tabla estándar de la terminal.

        Ejemplos:

            \033[48;5;17m: 48 (pinta el fondo), 5 (en modo 256 colores), 17 (que en la tabla es azul noche marino).
            \033[38;5;214m: 38 (pinta el texto), 5 (en modo 256 colores), 214 (que es el color naranja/oro vibrante).

        Al final siempre llevan la letra m, que es la manera de cerrar el comando de color o estilo en el estándar ANSI.


    Navegacion por cursor de la terminal:

        En el caso de la navegacion a travez del cursor, por la terminal, tenemos otros comandos como
        "\033[{n_moves_up}A" en el que estoy indicandole una orden de movimiento al cursor de la terminal N veces
        en direccion hacia arriba, de fila en fila. En este caso, al haber primero impreso el maze, el cursor se
        encontrara en la ultima posicion, es decir en al ultima fila de la ultima columna. Por otro lado, al avanzar
        un movimiento en direccion hacia arriba el cursor automaticamente sube una fila Y se posiciona en la primer
        columna de la misma, (viajando a la linea superior en su primera posicion).

        Comandos:

            A es el comando estándar ANSI para "Mover el Cursor Hacia Arriba".
            C es el comando para "Mover el Cursor Hacia la Derecha".

            B es abajo
            D es izquierda.

        Ejs:
            Si digo \033[10A el cursor subira diez posiciones y se hubicara en la primera posicion de esta linea,
            a la izquierda del todo.


    Comandos de CheckPoint: (save o unsave/return_to_checkpoint)

        El comandos de control \033[s (save checkpoint): 

            Lo que hace es grabar la posicion actual del cursor en la consola a modo checkpoint,
            para poder reubicar el cursor a esta posicion con una sola accion: comando de control \033[u


        El comando de control \033[u (un-save/restore_checkpoint):

            Lo que hace es retornar el cursor, de donde sea la posicion en que se encuentre en la terminal a la ultima
            posicion guardada de \033[s


    Respecto a "flush=True": 
        Lo que estamos indicando aquí, en contexto de print() es que si utilizamos la flag end="" para neutralizar
        el \n por defecto de print(), lo que sucede es que print no soltara los printeos almacenados en su buffer
        interno, sino hasta que este se llene o aparezca un \n que fuerza el flush. Con esta flag, el print siempre
        que tenga algo por imprimir lo devolvera de manera directa una vez leida la linea, sin importarle cuantos datos
        se encuentran en ese momento en el buffer ni su ocupacion actual.  


**from typing import TypedDict**

    Imaginate un diccionario normal (dict[str, Any]). Es como una caja de matemáticas donde tirás cualquier cosa. Python no sabe qué claves
    tiene ni de qué tipo son los valores adentro. Si vos en otra parte de tu código (por ejemplo en display.py) intentás leer config['widht']
    (con la 'dht' mal escrita) o asumís que config['width'] te devuelve un número pero resulta que le metiste un string, ¡PUM! Te expota el
    programa en la cara en tiempo de ejecución. Eso es laburar a ciegas.

    Ahí es donde entra la locura cósmica de TypedDict. En tiempo de ejecución sigue siendo un diccionario común y corriente, cero penalty de
    performance. Pero para tu IDE (VS Code) y para el Linter, es un CONTRATO ARQUITECTÓNICO.

    Fijate para qué sirve exactamente:

    Si en el bloque gigante de tu archivo asignás config['width'] = "10" (un string en vez de un entero), el editor te lo subraya en ROJO antes
    de que siquiera guardes el archivo diciéndote "Ey, el contrato dice que esto es un int". Cortamos el error de raíz antes de ejecutar. Documentamos
    con código, no con comentarios.

    n diccionario que tiene distinto tipo de valor por cada clave (heterogéneo y estructurado) no existe como objeto base de Python.
    TypedDict es una herramienta puramente de análisis estático que pertenece a typing y simula el comportamiento de las Interfaces de TypeScript.
    Pasamos de tener una caja oscura donde rogamos que el dato esté y sea del tipo correcto, a tener un contrato blindado


----
**El porqué de deque** (collections)

    Como programador en C, estás acostumbrado a pensar en cómo se aloja la memoria. En Python, una list está implementada internamente
    como un array dinámico (contiguo en memoria).

    En el método solve(), estás haciendo una búsqueda a lo ancho (BFS - Breadth-First Search) para encontrar el camino más corto. Para
    que el BFS funcione, necesitas una cola FIFO (First-In, First-Out).

    ¿Qué pasa si usas una list normal como me propusiste?

        Si usas lista.pop(0) para sacar el primer elemento, Python tiene que desplazar todos los elementos restantes de la lista un espacio
        hacia la izquierda. Eso cuesta  𝑂(𝑁). Si el laberinto es enorme, tu algoritmo se vuelve cuadradito y lentísimo.
        Si usas lista.pop() (saca el último, que es 𝑂(1), acabas de convertir tu cola en una pila (LIFO). Tu algoritmo ya no es BFS, es
        DFS (búsqueda en profundidad), que te va a encontrar un camino, pero rara vez el más corto.

    ¿Por qué deque?

        deque (Double-Ended Queue) está implementado en C como una lista doblemente enlazada de bloques (un híbrido muy eficiente). Permite hacer
        popleft() o append() en ambos extremos en tiempo constante 𝑂(1).

**Resolucion de laberintos Imperfectos**

    Partimos desde la base de un laberinto perfecto.

    El algoritmo consiste en 3 etapas:

    -   is_3x3_open(start-coord-x, start-coord-y)
        """
            Escanea un bloque 3x3 desde su esquina superior izquierda (sx, sy)

            Retorna true si TODAS las paredes internas estan rotas, respetando
                los limites del maze e ignorando el bloque_42.

            Siempre que encuentre al menos un muro cerrado retornará False,
                lo que significa que estamos ante un Bloque seguro.
        """
        
    -   _check_zones_3x3(c1, c2)
        """
            Generador que devuelve una por uno los offsets o puntos de 
                referencia validos como inicio del bloque 3x3 en relacion al
                muro divisorio entre c1 y c2, respetando los limites de la 
                matriz.

            Analiza si el muro de referencia es vertical u horizontal y
                establece el conjunto celdas de 3x2 que estan viculados
        """

    -   add_cycles(self)
        """
            Intenta derribar paredes intactas que sobrevivieron al Krustal.

            Garantiza que no genere pasillos abiertos de 3x3.
        """

Analicis de las funciones:

    A. Qué hace _check_zones_3x3(c1, c2)?

        Esta función calcula matemáticamente cuáles son esos 6 posibles
            orígenes (sx, sy) basándose en las posiciones de c1 y c2.

        Identifica el eje: 
            Determina si la pared que estamos analizando es vertical
            (las celdas están una al lado de la otra en X) o horizontal
            (una arriba de la otra en Y).

        Calcula los offsets:
            Si es una pared vertical entre X=2 y X=3, los bloques de 3x3
            afectados solo pueden empezar en la columna X=1 o en la columna
            X=2.
            En el eje Y, pueden empezar 2 filas más arriba, 1 fila más arriba,
            o en la misma fila.

        Filtro de bordes (En Python te daría un IndexError.):
             Esta función evalúa: "Si el bloque empezara en (-1, 0), ¿se sale
                del mapa? Sí. Entonces lo descarto y no lo devuelvo".

        Generación (yield):
            En lugar de crear una lista con los 6 pares de coordenadas (lo
            cual haría malloc en Python), hace yield. Esto pausa la función,
            envía el par (sx, sy) al bucle for, y cuando el bucle pide el
            siguiente, retoma la ejecución. Es un iterador perezoso (lazy).

    B. Que hace _is_3x3_open(sx, sy)?

        Esta es la inspectora. Recibe un punto de origen (sx, sy). Sabe que
        un bloque de 3x3 ocupa desde sx hasta sx + 2 en ancho, y desde sy
        hasta sy + 2 en alto.

        En lugar de contar si hay 9 celdas libres, busca la manera más rápida de
        fallar (fail-fast). Un área de 3x3 se considera "completamente abierta"
        solo si ninguna de las celdas dentro de ese perímetro tiene paredes que
        las separen.

        Escanea las paredes verticales internas. Por ejemplo, mira si la celda
        (sx, sy) tiene su pared Este (E) intacta. Si encuentra una sola pared en
        estado True dentro de la zona, detiene toda la comprobación inmediatamente
        (return False). Esa zona NO ES un pasillo de 3x3 puro; tiene al menos un
        tabique. Si ambos bucles for (el de paredes verticales internas y
        horizontales internas) terminan sin haber encontrado ni una sola pared
        levantada, significa que ese espacio es un bloque de 3x3 completamente
        vacío. Retorna True.

Resumen del flujo de ejecucion:

    1- En _add_cycles recopilamos los muros que quedaron intactos desde las
        aperturas generadas por el Kruskal (el maze en origen estaba
        totalmente cerrado) Una vez obtenida la lista de tuplas conformadas
        cada una por celda1, celda2, muro de c1(por ej: 'E'), muro de c2 que
        colinda (su opuesto: 'W').

    2- add_cycles intenta romper muros en esta lista de muros en pié del maze,
        comprobando en cada uno de estos muros, (usando los datos de la lista
        de tuplas), rompiendolos provisoriamente y una vez evaluados con las
        funciones auxiliares, define si permanecen rotos o si los revierte,
        volciendolos a levantar (wall = True).

    3- Comprobacion de self.check_zones_3x3: recibidas las celdas que comparten
        el muro colindante, esta funcion hace un escaneo de todos los posibles
        origenes de un 3x3, por definicion estan predefinidos, asi es que sim-
        plemente itera por el rango de x e y hasta analizar cada 3x3 construi-
        bles a partir de sus 6 offsets.

        Durante la iteracion en cada eje, chequea en cada offset si este gene-
        raria o no un pasillo abierto de 3x3 llamando a _is_3x3_open, si
        resulta true, suspende las iteraciones, revierte la destruccion del
        del muro y avanza al siguiente muro de la lista de tuplas
        "intact_walls", si resulta false, continua al siguiente offset del
        bucle hasta completarlos. Si finaliza el recorrido sin ningun bloque
        3x3 abierto, el muro roto por add_cycles permanecera abierto permanen-
        temente. Luego salta a la siguiente comprobacion en el "intact_walls"


Pasos para construir el _add_cycles():

1- Inicializar bloque 42
2- Inicializar la lista vacia de tuplas (celda, celda, muro(E/S), muro(O/N))
3- Iterar el eje x, dentro iterar el eje y
4- Inicializamos c1 en la posicion actual(partiendo de arriba a la izquierda
    = x=0, y=0) y chequeamos que no este en pattern42.
5- Chequeamos el vecino del este (siguiente en x) y miramos si el muro esta
    intacto y si estamos dentro de los limites del maze (c1 <= self.width - 1)
    
    c2 = self.grid[x+1][y]

   - Si los requisitos se cumplen(c1 y c2 =No42block, muro1 y muro2 =True)
        añadimos muros a la lista (c1,c2,E/S,O/N)
6- Chequeamos vecino del sur. Mismas condiciones y pasos.

7- Acabadas las iteraciones, Mezclamos la lista con random.suffle(intact_walls)
8- Empieza simulacion de ruptura de muros:

    1- Rompemos el primer par de muros de la lista
    2- Verificamos en bloque for los posibles origenes del 3x3 a partir de 
        sx, sy (start x, start y)

        - Se iterara por cada posible origen y se comprueba si 
            "post-ruptura del muro" is_3x3_open() = true

        - Si falla, marcamos un boolean que ntofica el creates_3x3, rompe el 
            bucle con break, saliendo del iterador sx, sy de esa dupla
            de muro y pasamos al mismo analicis de la prox dupla de la lista.

    3- Comprobacion del boolean creates 3x3, si resulta true, revertimos
        la simulacion y toca levantar nuevamente el muro, si no, el muro se
        queda derrumbado indefinidamente.
