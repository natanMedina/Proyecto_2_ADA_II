% - Parámetros
int: n; % número de personas
int: m; % número de opiniones
array[1..m] of 0..n: p; % distribución inicial de personas por opinión
array[1..m] of float: v; % valor de las opiniones
array[1..m] of float: ce; % costo extra de cada movimiento
array[1..m, 1..m] of float: c; % matriz de costos entre movimientos 
float: ct; % costo máximo permitido
int: maxM; % máximo número de movimientos permitidos

% - Variables
array[1..m, 1..m] of var 0..n: x; % movimiento de personas entre opiniones
array[1..m] of var 0..1: aux = [if p[j] > 0 then 0 else 1 endif | j in 1..m]; % valor booleano
array[1..m, 1..m] of var float: costoMovimiento;
var float: costoTotal = sum(i,j in 1..m) (costoMovimiento[i,j]);
var 0..maxM: movimientosTotales = sum(i,j in 1..m) (abs(j-i) * x[i,j]);

% - Nueva distribución de personas después de los movimientos
array[1..m] of var 0..n: p_final;
constraint forall(j in 1..m)(
    p_final[j] = sum(i in 1..m) (x[i, j])
);

% - Cálculo de la mediana sobre p_final
int: posmed = if n mod 2 != 0 then (n + 1) div 2 else n div 2 endif; % posición de la mediana
array[1..m] of var int: acumulado_final; % array para almacenar la suma acumulada de p_final
var 1..m: indice_limite; % variable para el índice donde se supera posmed
var float: mediana = v[indice_limite]; % mediana

% - Restricciones
constraint costoTotal <= ct;
constraint movimientosTotales <= maxM;

% Restricciones para los movimientos de personas entre opiniones
constraint forall(i in 1..m)(
    sum(j in 1..m) (x[i, j]) = p[i] % No mover más personas de las que hay en cada i
);

% -- Restricciones para costoMovimiento
constraint forall(i in 1..m, j in 1..m)(
    costoMovimiento[i, j] = c[i, j] * (1 + (p[i] / n)) * x[i, j] + (ce[j] * x[i, j] * aux[j])
);

% -- Restricciones para la mediana usando p_final
constraint acumulado_final[1] = p_final[1]; % inicialización del primer valor acumulado
constraint forall(i in 2..m)( acumulado_final[i] = acumulado_final[i-1] + p_final[i] ); % cálculo de la suma acumulada
constraint acumulado_final[indice_limite] >= posmed /\
          forall(j in 1..indice_limite-1) (acumulado_final[j] < posmed); % restricción para encontrar el índice donde acumulado_final es mayor o igual a posmed

% - Función objetivo
var float: polarizacion = sum(i in 1..m) (p_final[i] * abs(v[i]-mediana));
solve minimize polarizacion;

% Output
output [
    "Aux: ", show(aux), "\n",
    "Pos: ", show(posmed), "\n",
    "Indice: ", show(indice_limite), "\n",
    "Mediana: ", show(mediana), "\n",
    "p_final: ", show(p_final), "\n",
    "Movimientos: ", show(x), "\n",
    "MovimientosTotales: ", show(movimientosTotales), "\n",
    "CostoMovimiento: ", show(costoMovimiento), "\n",
    "CostoTotal: ", show(costoTotal), "\n",
    "Polarizacion: ", show(polarizacion)
];
