# AgroDirecto

Marketplace que conecta a agricultores del Eje Cafetero con compradores de ciudad, sin intermediarios.
Este repositorio contiene los dos módulos implementados (registro de usuarios y pedidos) y sus pruebas JUnit 5.

## Requisitos para compilar

- JDK 17 o superior
- Maven 3.9 o superior

## Compilar y ejecutar las pruebas

Desde esta carpeta (donde está `pom.xml`):

```bash
mvn clean test
```

Resultado esperado:

```
Tests run: 61, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```

Los reportes de JUnit quedan en `target/surefire-reports/` y el de cobertura (JaCoCo, sentencias y ramas por método) en `target/site/jacoco/index.html`. Una sola clase: `mvn test -Dtest=ServicioRegistroTest`.

## Estructura

```
src/main/java/co/edu/eam/agrodirecto/
  registro/ValidadorRegistro.java   RF-01 a RF-03 (una regla por método)
  registro/ServicioRegistro.java    aplica RF-01 a RF-05 en orden
  pedidos/Pedido.java               datos del pedido
  pedidos/EstadoPedido.java         PENDIENTE, PAGADO, ENVIADO, ENTREGADO, CANCELADO
  pedidos/GestorPedidos.java        RF-06 a RF-09
src/test/java/co/edu/eam/agrodirecto/
  registro/ValidadorRegistroTest.java  unitarias      CP-01 a CP-06
  registro/ServicioRegistroTest.java   integración    CP-07 a CP-11
  pedidos/GestorPedidosTest.java       unitarias      CP-12 a CP-18
  pedidos/FlujoPedidoTest.java         integración    CP-19
docs/
  ISII_GrupoX_Entregable.pdf        documento de la entrega final
  evidencias/                       salida de Maven antes y después de corregir, reportes de JUnit y de cobertura
```

Cada método de prueba empieza con el código del caso del plan (por ejemplo `CP10_...`).

## Requisitos funcionales

| Código | Requisito |
|--------|-----------|
| RF-01 | El rol es AGRICULTOR o COMPRADOR. |
| RF-02 | Si es AGRICULTOR, finca y municipio son obligatorios (no vacíos ni solo espacios). |
| RF-03 | Celular de exactamente 10 dígitos 0-9 que empieza por 3. |
| RF-04 | Se debe aceptar la política de tratamiento de datos. |
| RF-05 | El correo es obligatorio y no se repite (se ignoran mayúsculas y espacios). |
| RF-06 | Un pedido tiene comprador, producto y cantidad entera de 1 a 1000 kg. |
| RF-07 | Total = kg × precio por kg, con descuento de 0 a 100 %. El precio debe ser mayor que 0. |
| RF-08 | Mismo comprador, producto y cantidad en menos de 2 minutos es un pedido duplicado. |
| RF-09 | Estados: PENDIENTE → PAGADO → ENVIADO → ENTREGADO. Solo se cancela antes de enviar. |
