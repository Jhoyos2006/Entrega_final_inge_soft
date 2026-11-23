"""Genera docs/ISII_GrupoX_Entregable.pdf. Uso: python docs/generar_pdf.py  (requiere reportlab)."""
import os
import re
import textwrap

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph, Preformatted, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(AQUI, "ISII_GrupoX_Entregable.pdf")

# ---------- fuentes (Calibri en Windows; Helvetica en otro sistema) ----------
F, FB, FI, MONO = "Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Courier"
try:
    w = "C:/Windows/Fonts/"
    pdfmetrics.registerFont(TTFont("Cal", w + "calibri.ttf"))
    pdfmetrics.registerFont(TTFont("CalB", w + "calibrib.ttf"))
    pdfmetrics.registerFont(TTFont("CalI", w + "calibrii.ttf"))
    pdfmetrics.registerFont(TTFont("Cons", w + "consola.ttf"))
    pdfmetrics.registerFontFamily("Cal", normal="Cal", bold="CalB", italic="CalI", boldItalic="CalB")
    F, FB, FI, MONO = "Cal", "CalB", "CalI", "Cons"
except Exception:
    pass

base = ParagraphStyle("base", fontName=F, fontSize=11, leading=15, alignment=TA_JUSTIFY, spaceAfter=6)
centro = ParagraphStyle("centro", parent=base, alignment=TA_CENTER)
h1 = ParagraphStyle("h1", parent=base, fontName=FB, fontSize=14, leading=18, spaceBefore=10, spaceAfter=8,
                    alignment=0, keepWithNext=1)
h2 = ParagraphStyle("h2", parent=base, fontName=FB, fontSize=12, leading=15, spaceBefore=8, spaceAfter=4,
                    alignment=0, keepWithNext=1)
celda = ParagraphStyle("celda", fontName=F, fontSize=9, leading=11)
celda_b = ParagraphStyle("celda_b", parent=celda, fontName=FB)
lista = ParagraphStyle("lista", parent=base, leftIndent=14, bulletIndent=4, spaceAfter=3)
ref = ParagraphStyle("ref", parent=base, leftIndent=24, firstLineIndent=-24, alignment=0)
codigo = ParagraphStyle("codigo", fontName=MONO, fontSize=8, leading=10)

story = []
n_tabla = [0]
n_fig = [0]


def p(texto, estilo=base):
    story.append(Paragraph(texto, estilo))


def h(texto, estilo=h1):
    story.append(Paragraph(texto, estilo))


def items(lineas):
    for t in lineas:
        story.append(Paragraph(t, lista, bulletText="•"))


def tabla(titulo, filas, anchos, fs=9):
    n_tabla[0] += 1
    st = ParagraphStyle("c", parent=celda, fontSize=fs, leading=fs + 2)
    stb = ParagraphStyle("cb", parent=st, fontName=FB)
    datos = [[Paragraph(str(c), stb if i == 0 else st) for c in fila] for i, fila in enumerate(filas)]
    t = Table(datos, colWidths=[a * cm for a in anchos], repeatRows=1)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#808080")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E7E6E6")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(KeepTogether([Paragraph(f"<b>Tabla {n_tabla[0]}</b>", h2_sin_espacio),
                               Paragraph(f"<i>{titulo}</i>", base), t]))
    story.append(Spacer(1, 8))


def figura(titulo, texto):
    n_fig[0] += 1
    lineas = []
    for linea in texto.splitlines():
        lineas += textwrap.wrap(linea, 104, subsequent_indent="      ", drop_whitespace=False) or [""]
    texto = "\n".join(lineas)
    caja = Table([[Preformatted(texto, codigo)]], colWidths=[17 * cm])
    caja.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.4, colors.HexColor("#808080")),
                              ("LEFTPADDING", (0, 0), (-1, -1), 5), ("TOPPADDING", (0, 0), (-1, -1), 4),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    story.append(KeepTogether([Paragraph(f"<b>Figura {n_fig[0]}</b>", h2_sin_espacio),
                               Paragraph(f"<i>{titulo}</i>", base), caja]))
    story.append(Spacer(1, 8))


def captura(titulo, archivo, ancho_cm=17, alto_px=None):
    """Figura con una captura de docs/evidencias, escalada al ancho indicado.
    alto_px muestra solo la parte de arriba de la imagen (el archivo original no se modifica)."""
    n_fig[0] += 1
    ruta = os.path.join(AQUI, "evidencias", archivo)
    if alto_px:
        from io import BytesIO
        from PIL import Image as PILImage
        recorte = PILImage.open(ruta)
        recorte = recorte.crop((0, 0, recorte.width, alto_px))
        ruta = BytesIO()
        recorte.save(ruta, format="PNG")
        ruta.seek(0)
    w, h_px = ImageReader(ruta).getSize()
    if alto_px:
        ruta.seek(0)
    img = Image(ruta, width=ancho_cm * cm, height=ancho_cm * cm * h_px / w)
    img.hAlign = "LEFT"
    story.append(KeepTogether([Paragraph(f"<b>Figura {n_fig[0]}</b>", h2_sin_espacio),
                               Paragraph(f"<i>{titulo}</i>", base), img]))
    story.append(Spacer(1, 8))


h2_sin_espacio = ParagraphStyle("h2s", parent=base, fontName=FB, spaceAfter=0, spaceBefore=4, alignment=0)

# =====================================================================================
# PORTADA
# =====================================================================================
story.append(Spacer(1, 3 * cm))
p("<b>Plan de aseguramiento de calidad del proyecto AgroDirecto</b>", ParagraphStyle(
    "t", parent=centro, fontSize=15, leading=20))
p("Entregable final", centro)
story.append(Spacer(1, 2 * cm))
for linea in ["Jonathan David Ceballos Jiménez", "Leonardo Argoty", "Owen Fernando Bareño",
              "Juan Andrés Hoyos Cruz"]:
    p(linea, ParagraphStyle("i", parent=centro, spaceAfter=0))
story.append(Spacer(1, 2 * cm))
p("Docente: David Cano Baquero", centro)
story.append(Spacer(1, 2 * cm))
for linea in ["Ingeniería de Software II", "Ingeniería en Desarrollo de Software", "Institución Universitaria EAM",
              "Armenia, Quindío", "23 de noviembre de 2026"]:
    p(linea, ParagraphStyle("i2", parent=centro, spaceAfter=0))
story.append(PageBreak())

# =====================================================================================
# 1-2. DESCRIPCIÓN Y REQUISITOS
# =====================================================================================
h("1. Descripción del proyecto")
p("AgroDirecto es un marketplace web y móvil que conecta a pequeños agricultores y ganaderos de zonas rurales "
  "con compradores urbanos, sin intermediarios. Los agricultores publican sus productos con precios justos y "
  "los compradores reciben productos frescos sabiendo de qué finca vienen. Lo usarían productores del Eje "
  "Cafetero y consumidores de ciudades como Armenia o Pereira.")
p("Hoy el proyecto tiene dos módulos en Java 17, sin interfaz gráfica: <b>registro de usuarios</b> "
  "(paquete <i>registro</i>: ValidadorRegistro y ServicioRegistro) y <b>pedidos</b> (paquete <i>pedidos</i>: "
  "Pedido, EstadoPedido y GestorPedidos). Todo el plan de esta entrega se hace sobre esos dos módulos.")

h("2. Requisitos")
p("En la guía anterior trabajamos cinco requisitos, todos del registro. Para esta entrega los ampliamos a "
  "nueve, porque el módulo de pedidos ya existía en el código pero no tenía requisitos escritos y no se podía "
  "probar contra nada.")
tabla("Requisitos funcionales del proyecto (versión corregida)", [
    ["Código", "Requisito", "Módulo"],
    ["RF-01", "Al registrarse, el usuario escoge el rol AGRICULTOR o COMPRADOR. Un rol vacío o distinto se rechaza.", "Registro"],
    ["RF-02", "Si el rol es AGRICULTOR, el nombre de la finca y el municipio son obligatorios y no pueden ser solo espacios. Al COMPRADOR no se le piden.", "Registro"],
    ["RF-03", "El celular tiene exactamente 10 dígitos del 0 al 9 y empieza por 3.", "Registro"],
    ["RF-04", "El usuario debe aceptar la política de tratamiento de datos personales para terminar el registro.", "Registro"],
    ["RF-05", "El correo es obligatorio y no puede repetirse. Se compara sin tener en cuenta mayúsculas ni espacios al inicio o al final.", "Registro"],
    ["RF-06", "Un pedido tiene comprador, producto y una cantidad entera entre 1 y 1000 kg.", "Pedidos"],
    ["RF-07", "El total del pedido es kilos × precio por kilo, menos un descuento entre 0 y 100 %. El precio debe ser mayor que 0.", "Pedidos"],
    ["RF-08", "Si el mismo comprador pide el mismo producto y la misma cantidad en menos de 2 minutos, el pedido se trata como duplicado.", "Pedidos"],
    ["RF-09", "Un pedido pasa de PENDIENTE a PAGADO, ENVIADO y ENTREGADO, en ese orden. Solo se puede cancelar si está PENDIENTE o PAGADO.", "Pedidos"],
], [1.6, 13.2, 2.2])
tabla("Nota de cambios respecto a la guía anterior", [
    ["Cambio", "Por qué"],
    ["RF-03: se aclaró que los dígitos son del 0 al 9.", "En la guía 1 encontramos que el código aceptaba dígitos de ancho completo (defecto D-01). El requisito decía \"dígitos numéricos\" y eso se podía leer de dos formas."],
    ["RF-05: el correo pasa a ser obligatorio y se ignoran los espacios.", "En la guía 2 la prueba exploratoria mostró que un correo vacío se aceptaba y que \"ana@mail.com \" no se veía como repetido. Ningún requisito lo decía, así que primero se corrigió el requisito."],
    ["Se agregaron RF-06 a RF-09.", "El módulo de pedidos ya estaba programado desde el primer parcial pero no tenía requisitos verificables."],
    ["RF-06: la cantidad pasó de \"mayor que 0\" (decimal) a entero entre 1 y 1000 kg.", "Sin un tope no había valores límite claros, y comparar decimales con == para detectar duplicados era frágil."],
    ["Se quitaron del código el cálculo de envío y la suma de kilos por comprador, y las clases duplicadas de una entrega anterior.", "No respondían a ningún requisito. Las clases duplicadas hacían que se ejecutaran 45 pruebas repetidas."],
], [6.5, 10.5])

# =====================================================================================
# 3. RESULTADOS DE LA GUÍA ANTERIOR
# =====================================================================================
h("3. Resultados de la guía anterior")
h("3.1 Error, defecto y fallo", h2)
tabla("Error, defecto y fallo en AgroDirecto", [
    ["Req.", "Error (persona)", "Defecto (código)", "Fallo (lo que ve el usuario)"],
    ["RF-03", "Suponer que Character.isDigit solo reconoce los dígitos 0-9.", "celularValido usaba Character.isDigit, que también acepta dígitos Unicode como los de ancho completo.", "Se registra un celular pegado desde otro teclado que se ve bien pero al que no se le puede llamar ni escribir. Real: lo encontró la prueba U-19."],
    ["RF-05", "Entender \"mismo correo\" como \"texto idéntico\".", "Comparar con equals en lugar de equalsIgnoreCase.", "Ana se registra con ana@mail.com y luego con ANA@mail.com, y queda con dos cuentas. Posible: no se presentó."],
], [1.3, 4.5, 5.2, 6.0])
h("3.2 Pruebas por nivel", h2)
tabla("Pruebas de la guía 1 por nivel y resultado", [
    ["Nivel", "Qué se probó", "Casos", "Ejecución 1", "Ejecución 2 (tras corregir)"],
    ["Unitario", "Cada regla de ValidadorRegistro por separado (U-01 a U-25) y los límites de GestorPedidos (U-26 a U-33).", "33", "32 aprobadas, 1 fallida (U-19)", "33 aprobadas"],
    ["Integración", "ServicioRegistro con ValidadorRegistro y la lista de correos (I-01 a I-05).", "5", "4 aprobadas, 1 fallida (I-05)", "5 aprobadas"],
    ["Sistema", "No ejecutado: el registro no tiene interfaz (ni consola ni web).", "0", "No ejecutado", "No ejecutado"],
    ["Aceptación", "No alcanzado en la guía 1. Se completa en 3.3.", "-", "-", "-"],
], [2.2, 7.3, 1.4, 3.0, 3.1])
p("En esta entrega esas 38 pruebas se reorganizaron en los casos CP-01 a CP-19 del plan (sección 5). Las que "
  "probaban lo mismo con datos parecidos se juntaron en una sola prueba parametrizada.")
h("3.3 Simulación de aceptación", h2)
p("La guía pedía que otro equipo escribiera los criterios. No logramos hacer el intercambio, así que la "
  "simulación se hizo dentro del equipo: escribimos los criterios desde el punto de vista de un agricultor y "
  "de un comprador, en lenguaje de usuario, y los comprobamos con los casos automatizados.")
tabla("Simulación de aceptación (hecha por el equipo, no por otro grupo)", [
    ["Criterio del usuario", "Cómo se comprueba", "Resultado", "¿Acepta?"],
    ["\"Como agricultor me quiero registrar con mi finca y mi municipio.\"", "CP-11", "Registro OK", "Sí"],
    ["\"Nadie más se puede registrar con mi correo, aunque lo escriba con mayúsculas o con un espacio.\"", "CP-08, CP-09", "Rechazado como repetido", "Sí, después de corregir D-04"],
    ["\"Si escribo mal el celular, no me debe dejar seguir.\"", "CP-05, CP-06", "Rechazado", "Sí"],
    ["\"Si por error toco dos veces comprar, no me deben hacer dos pedidos.\"", "CP-16, CP-17", "Segundo pedido marcado como duplicado", "Sí"],
    ["\"Un pedido que ya salió de la finca no se puede cancelar.\"", "CP-18, CP-19", "La cancelación se rechaza", "Sí"],
    ["\"Si algo está mal, el mensaje me dice qué corregir.\"", "Revisión de los mensajes de ServicioRegistro", "\"ERROR: celular invalido\" no dice cuál es la regla", "No. Queda pendiente (CP-20)"],
], [6.6, 3.0, 4.2, 3.2])

# =====================================================================================
# 4. ETAPA 1
# =====================================================================================
story.append(PageBreak())
h("4. Etapa 1. Métodos de prueba: caja negra y caja blanca")
h("4.1 Investigación", h2)
p("En las pruebas de <b>caja negra</b> los casos salen del requisito, sin mirar el código. La <b>partición de "
  "equivalencia</b> divide los valores posibles de una entrada en grupos que el programa debería tratar igual. "
  "Basta con un caso por grupo, porque si un valor del grupo falla, lo más probable es que los demás también "
  "fallen (Myers et al., 2012). Se separan particiones válidas e inválidas, y las inválidas se prueban de a una "
  "para que un error no esconda a otro.")
p("El <b>análisis de valores límite</b> completa lo anterior. Los defectos se acumulan en los bordes de las "
  "particiones, por ejemplo un &lt; escrito donde iba un &lt;=, así que se prueba el valor justo en el borde y "
  "el que queda inmediatamente afuera (International Software Testing Qualifications Board [ISTQB], 2023).")
p("Una <b>tabla de decisión</b> sirve cuando el resultado depende de varias condiciones a la vez. Se listan "
  "las condiciones, todas sus combinaciones (2<super>n</super> si son n condiciones de sí o no) y la acción "
  "esperada en cada una. Las combinaciones que llevan a la misma acción se pueden juntar marcando con un "
  "guion las condiciones que no importan (Copeland, 2004).")
p("En <b>caja blanca</b> los casos salen de la estructura del código. La <b>cobertura de sentencias</b> es el "
  "porcentaje de instrucciones que se ejecutaron al menos una vez. La <b>cobertura de ramas</b> es el porcentaje "
  "de salidas de cada decisión (verdadero y falso) que se ejecutaron. Cubrir todas las ramas implica cubrir "
  "todas las sentencias, pero no al revés: un if sin else se cubre en sentencias con un solo caso y necesita "
  "dos para cubrir sus ramas (ISTQB, 2023; Pressman y Maxim, 2020).")

h("4.2 Particiones de equivalencia y valores límite", h2)
p("Escogimos tres requisitos que tienen rangos o formatos: RF-03 (celular), RF-06 (cantidad del pedido) y "
  "RF-07 (descuento). Para RF-07 el pedido es de 5 kg a $3.000 el kilo.")
tabla("RF-03: celular", [
    ["Partición", "Tipo", "Valores de prueba", "Esperado", "Caso"],
    ["10 caracteres, empieza por 3, solo dígitos 0-9", "Válida", "3124567890", "Aceptado", "CP-05"],
    ["Menos de 10 caracteres", "Inválida", "312345678 (límite: 9)", "Rechazado", "CP-06"],
    ["Más de 10 caracteres", "Inválida", "31234567890 (límite: 11)", "Rechazado", "CP-06"],
    ["Empieza por un dígito distinto de 3", "Inválida", "2999999999 y 4000000000 (límites del primer dígito)", "Rechazado", "CP-06"],
    ["Primer dígito 3 en sus extremos", "Válida", "3000000000 y 3999999999 (menor y mayor permitido)", "Aceptado", "CP-05"],
    ["Contiene una letra", "Inválida", "31A4567890", "Rechazado", "CP-06"],
    ["Contiene un espacio", "Inválida", "312 456789", "Rechazado", "CP-06"],
    ["Contiene dígitos que no son 0-9", "Inválida", "\"3\" + 9 dígitos de ancho completo", "Rechazado", "CP-06"],
    ["Nulo", "Inválida", "null", "Rechazado", "CP-06"],
], [5.4, 1.7, 5.2, 2.2, 1.5])
tabla("RF-06: cantidad del pedido (1 a 1000 kg)", [
    ["Partición", "Tipo", "Valores de prueba", "Esperado", "Caso"],
    ["Menor que 1", "Inválida", "-5, 0 (límite)", "Pedido no válido", "CP-13"],
    ["Entre 1 y 1000", "Válida", "1 (límite), 500, 1000 (límite)", "Pedido válido", "CP-12"],
    ["Mayor que 1000", "Inválida", "1001 (límite)", "Pedido no válido", "CP-13"],
], [5.4, 1.7, 5.2, 2.2, 1.5])
tabla("RF-07: descuento (0 a 100 %) sobre 5 kg a $3.000", [
    ["Partición", "Tipo", "Valores de prueba", "Esperado", "Caso"],
    ["Menor que 0", "Inválida", "-1 (límite)", "IllegalArgumentException", "CP-15"],
    ["Entre 0 y 100", "Válida", "0 (límite) → 15000; 10 → 13500; 100 (límite) → 0", "Total calculado", "CP-14"],
    ["Mayor que 100", "Inválida", "101 (límite)", "IllegalArgumentException", "CP-15"],
], [5.4, 1.7, 5.2, 2.2, 1.5])

h("4.3 Tabla de decisión: RF-08 pedidos duplicados", h2)
p("RF-08 es el requisito con más condiciones combinadas: cuatro. Con cuatro condiciones hay 16 combinaciones, "
  "pero basta con que una sea falsa para que el pedido no sea duplicado. Por eso se reducen a cinco reglas: "
  "R2 cubre 8 combinaciones, R3 cubre 4, R4 cubre 2, y R5 y R1 una cada una (8+4+2+1+1 = 16). El pedido "
  "anterior siempre es del comprador A001, tomate, 5 kg.")
tabla("Tabla de decisión de RF-08 (S = sí, N = no, - = no importa)", [
    ["Condición / acción", "R1", "R2", "R3", "R4", "R5"],
    ["C1. Mismo comprador", "S", "N", "S", "S", "S"],
    ["C2. Mismo producto", "S", "-", "N", "S", "S"],
    ["C3. Misma cantidad", "S", "-", "-", "N", "S"],
    ["C4. Menos de 2 minutos desde el anterior", "S", "-", "-", "-", "N"],
    ["Acción: marcar como duplicado", "X", "", "", "", ""],
    ["Acción: aceptar como pedido nuevo", "", "X", "X", "X", "X"],
    ["Dato de prueba (CP-17)", "A001, tomate, 5 kg, a los 30 s", "B002", "papa", "6 kg", "a los 10 min"],
], [6.2, 2.6, 2.0, 2.0, 2.0, 2.2])
p("El borde de C4 se prueba aparte en CP-16: a los 119 999 ms el pedido es duplicado y a los 120 000 ms ya no.")

h("4.4 Caja blanca: ValidadorRegistro.celularValido", h2)
figura("Método probado, con sus decisiones numeradas", """public static boolean celularValido(String celular) {
    if (celular == null || celular.length() != 10) {   // D1
        return false;
    }
    if (celular.charAt(0) != '3') {                     // D2
        return false;
    }
    for (char c : celular.toCharArray()) {
        if (c < '0' || c > '9') {                       // D3
            return false;
        }
    }
    return true;
}""")
tabla("Caminos de celularValido y caso para cada uno", [
    ["Camino", "Decisiones", "Entrada", "Esperado", "Caso"],
    ["P1", "D1 verdadera", "\"312345678\" (9 caracteres); también null", "false", "CP-06"],
    ["P2", "D1 falsa, D2 verdadera", "\"2999999999\"", "false", "CP-06"],
    ["P3", "D1 y D2 falsas, D3 verdadera en algún carácter", "\"31A4567890\" (letra, mayor que '9') y \"312 456789\" (espacio, menor que '0')", "false", "CP-06"],
    ["P4", "D1 y D2 falsas, D3 falsa en todos los caracteres", "\"3124567890\"", "true", "CP-05"],
], [1.5, 5.0, 6.0, 2.0, 2.5])
p("D1 y D3 son condiciones compuestas (||). Para cubrir todas las ramas no basta con que cada if sea verdadero "
  "y falso: cada parte del || tiene que decidir el resultado al menos una vez. Por eso en P1 también se prueba "
  "null, y en P3 hay un carácter mayor que '9' y otro menor que '0'.")

h("4.5 Cobertura medida con JaCoCo", h2)
p("Para no quedarnos con el cálculo a mano, agregamos el plugin JaCoCo al pom.xml. Cada vez que se corre "
  "mvn test, JaCoCo genera un reporte de cobertura de sentencias y de ramas por método en "
  "target/site/jacoco/index.html. Una copia quedó en docs/evidencias/cobertura-jacoco.")
p("La primera medición nos corrigió. En celularValido teníamos 100 % de sentencias pero solo 11 de 12 ramas. "
  "Faltaba el caso en que c &lt; '0' es verdadero: ninguna prueba tenía un carácter menor que '0'. En la "
  "guía 1 sí estaba (U-17, celular con espacio), pero se perdió al juntar las pruebas. Lo agregamos a CP-06 y "
  "la cobertura de ramas del método subió a 12 de 12. El reporte también mostró que en ServicioRegistro no se "
  "probaban, en integración, los mensajes de rol, finca y celular; por eso CP-07 se amplió a una prueba "
  "parametrizada con una fila por regla.")
tabla("Cobertura por método medida con JaCoCo (ejecución final)", [
    ["Clase y método", "Sentencias (instrucciones)", "Ramas", "Qué falta"],
    ["ValidadorRegistro.rolValido", "12/12", "4/4", "-"],
    ["ValidadorRegistro.datosAgricultorValidos", "16/16", "6/6", "-"],
    ["ValidadorRegistro.celularValido", "42/42", "12/12", "- (antes 11/12)"],
    ["ServicioRegistro.registrar", "38/38", "12/12", "- (antes 9/12)"],
    ["GestorPedidos.esDuplicado", "40/40", "10/10", "-"],
    ["GestorPedidos.cambiarEstado", "20/20", "2/2", "-"],
    ["GestorPedidos.puedePasarA", "38/40", "16/18", "Estado actual o destino null."],
    ["GestorPedidos.esValido (y tieneTexto)", "30/31", "9/14", "Pedido null, comprador o producto vacíos: las particiones de RF-06 solo se hicieron sobre la cantidad."],
    ["GestorPedidos.calcularTotal", "27/32", "5/6", "Precio por kg menor o igual a 0."],
    ["Total del proyecto", "357/365 (97,8 %)", "80/88 (90,9 %)", ""],
], [5.6, 3.4, 2.4, 5.6], fs=8.5)
p("Las ramas que faltan están todas en el módulo de pedidos y son entradas inválidas que no salieron de "
  "nuestras particiones. Las dejamos a la vista en vez de esconderlas: son los próximos casos que agregaríamos. "
  "Una cobertura alta tampoco prueba que no haya defectos; solo dice qué partes del código nunca se ejecutaron.")
captura("Reporte de JaCoCo abierto en el navegador después de mvn clean test (captura del equipo)",
        "captura_jacoco.png", ancho_cm=17, alto_px=245)

# =====================================================================================
# 5. ETAPA 2
# =====================================================================================
story.append(PageBreak())
h("5. Etapa 2. Plan de pruebas y casos de prueba")
h("5.1 Investigación", h2)
p("La norma IEEE 829 (IEEE, 2008) define qué documentos acompañan las pruebas y qué lleva cada uno. Su plan "
  "de pruebas tiene estas secciones: identificador, introducción, elementos a probar, características que se "
  "prueban y las que no, enfoque, criterios de aprobación o fallo, criterios de suspensión y reanudación, "
  "entregables, tareas, necesidades de entorno, responsables, personal, cronograma, riesgos y aprobaciones. "
  "La ISO/IEC/IEEE 29119-3 (2021) reemplazó a la IEEE 829 y organiza los documentos en tres grupos: los de la "
  "organización, los de gestión (plan, informe de avance e informe de cierre) y los del proceso dinámico "
  "(especificación de diseño, casos, procedimientos e informes de incidentes). Su plan conserva lo esencial: "
  "alcance, riesgos, estrategia, personal y cronograma.")
p("Una <b>matriz de trazabilidad</b> es una tabla que relaciona cada requisito con los casos que lo prueban. "
  "Se lee en las dos direcciones: un requisito sin casos no está probado, y un caso sin requisito no tiene "
  "razón de existir. También dice qué casos hay que repetir cuando un requisito cambia (Sommerville, 2016).")

h("5.2 Plan de pruebas de AgroDirecto", h2)
p("<b>Identificación.</b> PP-AGRO-01, versión 1.0, noviembre de 2026.")
p("<b>Alcance.</b> Entran las cinco clases de los módulos de registro y pedidos y los requisitos RF-01 a "
  "RF-09. Quedan por fuera: la interfaz web y móvil, porque no existe; la base de datos, porque los correos se "
  "guardan en memoria; los pagos y el despacho, porque no están programados; y las pruebas de carga y de "
  "seguridad más allá de validar entradas, porque necesitan un servidor desplegado.")
p("<b>Requisitos a probar.</b> RF-01 a RF-09 (Tabla 1). Prioridad alta: RF-03, RF-05, RF-07, RF-08 y RF-09, "
  "porque un error ahí deja usuarios sin contacto, cuentas duplicadas o cobros mal hechos. Prioridad media: "
  "RF-01, RF-02, RF-04 y RF-06.")
tabla("Enfoque por nivel y tipo", [
    ["Nivel o tipo", "Qué se prueba", "Técnica"],
    ["Unitario", "ValidadorRegistro y GestorPedidos, cada método por separado.", "Particiones, valores límite, tabla de decisión y caminos (Etapa 1). Automatizado con JUnit 5."],
    ["Integración", "ServicioRegistro con ValidadorRegistro; Pedido, EstadoPedido y GestorPedidos en el flujo completo.", "Casos de flujo. Automatizado con JUnit 5."],
    ["Sistema", "No se ejecuta: no hay interfaz.", "-"],
    ["Aceptación", "Criterios escritos desde el usuario (sección 3.3).", "Simulación dentro del equipo."],
    ["Regresión", "Todos los casos automatizados después de cada cambio.", "mvn clean test"],
    ["Confirmación", "El caso que falló, después de corregir el defecto.", "mvn test -Dtest=Clase"],
    ["Usabilidad", "Mensajes de error frente a usuarios reales.", "Manual, con observación (CP-20)."],
], [2.6, 7.4, 7.0])
p("<b>Entorno y herramientas.</b> Windows 11 y Ubuntu 22.04, JDK 17.0.19 (Temurin), Apache Maven 3.9.15, "
  "JUnit 5.10.2, Maven Surefire 3.2.5, JaCoCo 0.8.12 (cobertura), IntelliJ IDEA y Visual Studio Code, Git y GitHub.")
p("<b>Criterios de entrada.</b> El proyecto compila con mvn clean test; los requisitos RF-01 a RF-09 están "
  "escritos y revisados por el equipo; los casos están diseñados con su resultado esperado.")
p("<b>Criterios de salida.</b> Todos los casos automatizados se ejecutaron; no queda ningún defecto de "
  "severidad alta abierto; cada requisito tiene al menos un caso aprobado; los casos no ejecutados tienen su "
  "razón escrita.")
p("<b>Criterios de suspensión y reanudación.</b> Se suspende si el proyecto no compila, si falla CP-11 o CP-19 "
  "(los flujos principales, que bloquean el resto) o si un defecto deja el servicio inutilizable, como pasó con "
  "D-02. Se reanuda cuando el defecto se corrige y el proyecto vuelve a compilar.")
tabla("Responsables", [
    ["Integrante", "Responsabilidad en el plan"],
    ["Juan Andrés Hoyos Cruz", "Automatización de las pruebas de registro, ejecución y reporte de JUnit, README."],
    ["Jonathan David Ceballos Jiménez", "Corrección de requisitos, matriz de trazabilidad, CMMI y definición de terminado."],
    ["Leonardo Argoty", "Diseño de casos: particiones, valores límite, tabla de decisión y caja blanca."],
    ["Owen Fernando Bareño", "Plan de pruebas, registro de defectos, automatización de pedidos e ISO/IEC 25010."],
], [5.5, 11.5])
tabla("Cronograma", [
    ["Fecha (nov. 2026)", "Actividad"],
    ["Lunes 16", "Revisión de la guía anterior y corrección de requisitos."],
    ["Martes 17", "Etapa 1: particiones, valores límite, tabla de decisión y caminos."],
    ["Miércoles 18", "Etapa 2: plan, casos y matriz de trazabilidad."],
    ["Jueves 19", "Etapa 3: automatización y primera ejecución."],
    ["Viernes 20", "Corrección de defectos, segunda ejecución (confirmación y regresión)."],
    ["Sábado 21", "Etapa 4 y armado del documento."],
    ["Domingo 22", "Grabación del video."],
    ["Lunes 23", "Revisión final y envío antes de las 23:55."],
], [4.0, 13.0])
tabla("Riesgos del plan", [
    ["Riesgo", "Efecto", "Qué hacemos"],
    ["Poco tiempo por entregas de otras materias.", "Casos sin ejecutar.", "Se ejecutan primero los de prioridad alta."],
    ["No hay interfaz.", "No se pueden hacer pruebas de sistema.", "Se compensa con pruebas de integración y se declara \"no ejecutado\"."],
    ["Un integrante no logra correr Maven.", "No puede ejecutar ni revisar.", "README con versiones fijas y pasos exactos."],
    ["Cambian los requisitos.", "Casos desactualizados.", "La matriz de trazabilidad dice qué casos repetir."],
    ["Pruebas que dependen de la hora del equipo.", "Resultados que cambian entre ejecuciones.", "Se usa una marca de tiempo fija (T0) en las pruebas de duplicados."],
], [5.2, 4.8, 7.0])

h("5.3 Casos de prueba", h2)
p("Se documentaron 21 casos. Los que vienen de la Etapa 1 son CP-05, CP-06 y CP-12 a CP-17. Los resultados "
  "obtenidos son los de la segunda ejecución; en CP-09 y CP-10 se deja también lo que pasó en la primera.")
SN = "Servicio nuevo, sin usuarios"
tabla("Casos de prueba", [
    ["ID", "Req.", "Precondición", "Datos", "Pasos", "Resultado esperado", "Resultado obtenido", "Estado"],
    ["CP-01", "RF-01", "Ninguna", "AGRICULTOR; COMPRADOR", "Llamar rolValido con cada dato", "true", "true", "Aprobado"],
    ["CP-02", "RF-01", "Ninguna", "null; \"\"; agricultor; VENDEDOR", "Llamar rolValido con cada dato", "false", "false", "Aprobado"],
    ["CP-03", "RF-02", "Rol AGRICULTOR", "finca \"   \"; municipio \"\"; finca null; municipio tabulador", "Llamar datosAgricultorValidos", "false", "false", "Aprobado"],
    ["CP-04", "RF-02", "Rol COMPRADOR", "finca y municipio null", "Llamar datosAgricultorValidos", "true", "true", "Aprobado"],
    ["CP-05", "RF-03", "Ninguna", "3000000000; 3124567890; 3999999999", "Llamar celularValido", "true", "true", "Aprobado"],
    ["CP-06", "RF-03", "Ninguna", "null; 9 y 11 dígitos; empieza por 2 y por 4; con letra; con espacio; ancho completo", "Llamar celularValido", "false", "false", "Aprobado"],
    ["CP-07", "RF-01 a RF-04", SN, "Una fila por regla rota: rol VENDEDOR; finca vacía; celular de 9 dígitos; política no aceptada", "Llamar registrar con cada fila", "El mensaje de esa regla; 0 registrados", "Igual al esperado", "Aprobado"],
    ["CP-08", "RF-05", "ana@mail.com registrado", "ANA@Mail.com", "Registrar el segundo usuario", "ERROR: correo ya registrado; 1 registrado", "Igual al esperado", "Aprobado"],
    ["CP-09", "RF-05", "ana@mail.com registrado", "\" ana@mail.com \"", "Registrar el segundo usuario", "ERROR: correo ya registrado", "Ejec. 1: OK (D-04). Ejec. 2: igual al esperado", "Aprobado tras corregir"],
    ["CP-10", "RF-05", SN, "Correo null, \"\" y \"   \"; luego leo@mail.com", "Registrar con el correo vacío y luego otro usuario", "ERROR: correo invalido; después OK", "Ejec. 1: OK y NullPointerException (D-02, D-03). Ejec. 2: igual al esperado", "Aprobado tras corregir"],
    ["CP-11", "RF-01 a RF-05", SN, "AGRICULTOR, Finca La Esperanza, Calarcá, 3104567890, acepta, rosa@mail.com", "Llamar registrar", "OK; 1 registrado", "Igual al esperado", "Aprobado"],
    ["CP-12", "RF-06", "Ninguna", "1; 500; 1000 kg", "Llamar esValido", "true", "true", "Aprobado"],
    ["CP-13", "RF-06", "Ninguna", "-5; 0; 1001 kg", "Llamar esValido", "false", "false", "Aprobado"],
    ["CP-14", "RF-07", "Pedido de 5 kg, $3.000/kg", "Descuento 0; 10; 100", "Llamar calcularTotal", "15000; 13500; 0", "Igual al esperado", "Aprobado"],
    ["CP-15", "RF-07", "Pedido de 5 kg, $3.000/kg", "Descuento -1; 101", "Llamar calcularTotal", "IllegalArgumentException", "IllegalArgumentException", "Aprobado"],
    ["CP-16", "RF-08", "Pedido anterior A001, tomate, 5 kg en T0", "Mismo pedido en T0+119 999 ms y T0+120 000 ms", "Llamar esDuplicado", "true; false", "true; false", "Aprobado"],
    ["CP-17", "RF-08", "Pedido anterior A001, tomate, 5 kg en T0", "Reglas R1 a R5 (Tabla 9)", "Llamar esDuplicado", "R1 true; R2 a R5 false", "Igual al esperado", "Aprobado"],
    ["CP-18", "RF-09", "Ninguna", "10 pares (estado actual, destino)", "Llamar puedePasarA", "5 permitidas y 5 prohibidas según RF-09", "Igual al esperado", "Aprobado"],
    ["CP-19", "RF-06 a RF-09", "Historial vacío", "A001, tomate, 5 kg, $3.000/kg, 10 %", "Validar, revisar duplicado, calcular total, pagar, enviar, intentar cancelar, entregar", "Válido; no duplicado; 13500; cancelar lanza IllegalStateException; termina ENTREGADO", "Igual al esperado", "Aprobado"],
    ["CP-20", "RF-03", "Formulario de registro en un celular", "Celular con espacios: 312 456 7890", "Tres personas ajenas al equipo se registran sin ayuda", "Entienden el mensaje y corrigen el dato", "-", "No ejecutado: no existe la interfaz"],
    ["CP-21", "RF-01 a RF-05", "Aplicación desplegada", "Agricultor nuevo", "Registro completo desde el navegador del celular", "Cuenta creada", "-", "No ejecutado: no hay interfaz ni servidor"],
], [1.15, 1.35, 2.2, 2.9, 2.5, 2.6, 2.5, 1.8], fs=7.5)

h("5.4 Matriz de trazabilidad", h2)
casos = {
    "RF-01": [1, 2, 7, 11, 21], "RF-02": [3, 4, 7, 11, 21], "RF-03": [5, 6, 7, 11, 20, 21], "RF-04": [7, 11, 21],
    "RF-05": [8, 9, 10, 11, 21], "RF-06": [12, 13, 19], "RF-07": [14, 15, 19], "RF-08": [16, 17, 19],
    "RF-09": [18, 19],
}
cab = ["Req."] + [f"{i:02d}" for i in range(1, 22)]
filas = [cab] + [[rf] + ["X" if i in lst else "" for i in range(1, 22)] for rf, lst in casos.items()]
n_tabla[0] += 1
st7 = ParagraphStyle("m", parent=celda, fontSize=7.5, leading=9, alignment=TA_CENTER)
mt = Table([[Paragraph(c, st7) for c in f] for f in filas], colWidths=[1.25 * cm] + [0.75 * cm] * 21)
mt.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#808080")),
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E7E6E6")),
                        ("LEFTPADDING", (0, 0), (-1, -1), 1), ("RIGHTPADDING", (0, 0), (-1, -1), 1)]))
story.append(KeepTogether([Paragraph(f"<b>Tabla {n_tabla[0]}</b>", h2_sin_espacio),
                           Paragraph("<i>Matriz de trazabilidad: requisitos contra casos CP-01 a CP-21</i>", base),
                           mt]))
story.append(Spacer(1, 6))
p("Los nueve requisitos tienen al menos un caso automatizado y aprobado. CP-20 y CP-21 están en la matriz pero "
  "no se ejecutaron.")

h("5.5 Registro de defectos", h2)
p("Solo están los defectos que aparecieron al ejecutar casos. D-01 viene de la guía 1. D-02, D-03 y D-04 "
  "aparecieron en la primera ejecución de esta entrega, al correr CP-09 y CP-10 contra la lógica original de "
  "ServicioRegistro (Figura 6). D-02 ya se había visto en la prueba exploratoria de la guía 2 (hallazgos E-4 "
  "y E-5) pero no se había corregido.")
tabla("Registro de defectos", [
    ["ID", "Descripción", "Severidad", "Cómo reproducirlo", "Estado", "Confirmación"],
    ["D-01", "celularValido acepta dígitos de ancho completo porque usa Character.isDigit.", "Media", "celularValido(\"3\" + nueve dígitos de ancho completo) devuelve true.", "Cerrado (guía 1)", "U-19 e I-05 en la guía 1; hoy CP-06."],
    ["D-02", "Un correo null se acepta y se guarda. El siguiente registro lanza NullPointerException y el servicio queda inutilizable para todos.", "Alta", "registrar(..., null) y luego registrar(..., \"leo@mail.com\").", "Cerrado", "CP-10 con null: aprobado en la ejecución 2."],
    ["D-03", "Un correo vacío o de solo espacios se acepta como válido.", "Media", "registrar(..., \"\") devuelve OK.", "Cerrado", "CP-10 con \"\" y \"   \": aprobado."],
    ["D-04", "Un correo con espacios al inicio o al final no se reconoce como repetido.", "Media", "Registrar ana@mail.com y luego \" ana@mail.com \": devuelve OK.", "Cerrado", "CP-09: aprobado."],
], [1.1, 4.6, 1.5, 4.3, 1.9, 3.6], fs=8.5)
p("<b>Corrección.</b> En ServicioRegistro se agregó la revisión de que el correo tenga texto antes de RF-05, y "
  "la lista de correos se cambió por un HashSet que guarda cada correo sin espacios y en minúscula. Con eso se "
  "cerraron los tres defectos. Como efecto adicional, la búsqueda de duplicados dejó de recorrer la lista "
  "completa, que era el problema de rendimiento que se midió en la guía 2.")

# =====================================================================================
# 6. ETAPA 3
# =====================================================================================
story.append(PageBreak())
h("6. Etapa 3. Automatización de pruebas")
h("6.1 Investigación", h2)
p("Conviene automatizar lo que se repite muchas veces y tiene un resultado esperado claro: reglas de negocio, "
  "cálculos, casos con muchos datos (como los valores límite) y la regresión que se corre después de cada "
  "cambio. No conviene automatizar lo que depende del juicio de una persona, como la usabilidad o la prueba "
  "exploratoria, lo que se va a probar una sola vez o una interfaz que todavía cambia mucho, porque mantener "
  "la prueba cuesta más que ejecutarla a mano (ISTQB, 2023).")
p("JUnit 5 ejecuta como prueba todo método marcado con <b>@Test</b>. <b>@BeforeEach</b> marca un método que se "
  "corre antes de cada prueba, para que todas empiecen con objetos nuevos y no dependan unas de otras. "
  "<b>@ParameterizedTest</b> ejecuta el mismo método varias veces con datos distintos que vienen de una fuente "
  "como @ValueSource, @CsvSource o @NullSource. La clase <b>Assertions</b> trae los métodos que deciden si la "
  "prueba pasa: assertEquals (con una tolerancia para números decimales), assertTrue, assertFalse y "
  "assertThrows, que verifica que se lance una excepción (JUnit Team, 2024).")
p("Con Maven, las pruebas van en src/test/java y las ejecuta el plugin <b>Surefire</b> en la fase test. "
  "Surefire busca por defecto las clases cuyo nombre termina en Test, las ejecuta y deja un reporte en texto y "
  "XML en target/surefire-reports. Si una prueba falla, el comando mvn test termina en BUILD FAILURE (Apache "
  "Maven Project, 2024).")

h("6.2 Aplicación", h2)
p("Automatizamos 19 de los 21 casos en cuatro clases JUnit 5, separadas del código del proyecto. Cada método "
  "empieza con el código del caso, por ejemplo CP13_cantidadFueraDelRangoEsInvalida. Los valores límite usan "
  "@ParameterizedTest, por eso 19 casos dan 61 ejecuciones. La misma corrida genera el reporte de cobertura "
  "de JaCoCo (sección 4.5).")
tabla("Clases de prueba automatizadas", [
    ["Clase", "Casos", "Nivel", "Clases reales que usa", "Ejecuciones"],
    ["ValidadorRegistroTest", "CP-01 a CP-06", "Unitario", "ValidadorRegistro", "22"],
    ["ServicioRegistroTest", "CP-07 a CP-11", "Integración", "ServicioRegistro + ValidadorRegistro", "10"],
    ["GestorPedidosTest", "CP-12 a CP-18", "Unitario", "GestorPedidos (con Pedido como dato)", "28"],
    ["FlujoPedidoTest", "CP-19", "Integración", "Pedido + EstadoPedido + GestorPedidos", "1"],
    ["Total", "19 casos", "", "", "61"],
], [4.2, 2.8, 2.2, 5.8, 2.0])
figura("Ejemplo de caso de valores límite automatizado (GestorPedidosTest)", """@ParameterizedTest
@ValueSource(ints = {-5, 0, 1001})
void CP13_cantidadFueraDelRangoEsInvalida(int kg) {
    assertFalse(gestor.esValido(new Pedido("A001", "tomate", kg, T0)));
}""")

captura("Reporte de JUnit en consola con mvn clean test (ejecución 2, código corregido): 61 pruebas, 0 fallos",
        "captura_mvn_clean_test.png", ancho_cm=16)
captura("Árbol de pruebas en Visual Studio Code: cada método lleva el código del caso (CP01 a CP19)",
        "captura_arbol_pruebas.png", ancho_cm=16)

antes = open(os.path.join(AQUI, "evidencias", "salida_antes_de_corregir.txt"), encoding="utf-8").read()
antes = "\n".join(l for l in antes.splitlines() if "ERROR]   " in l or "Tests run: 57" in l or "BUILD" in l)
antes = antes.replace("\ufffd", "-")
figura("Ejecución 1, con la lógica original de ServicioRegistro: aparecen D-02, D-03 y D-04 (en ese momento "
       "había 57 ejecuciones; las 4 de más salieron después, con la medición de cobertura)", antes)

p("<b>Casos manuales.</b> CP-20 y CP-21 quedaron manuales. CP-20 es una prueba de usabilidad: necesita ver a "
  "personas reales leyendo el mensaje de error, y eso no lo puede decidir una aserción. CP-21 necesita la "
  "aplicación desplegada con su interfaz, que todavía no existe. Los dos quedan como \"no ejecutados\".")
p("Para repetir todo: <font face='%s'>mvn clean test</font> desde la carpeta del proyecto. El README del "
  "repositorio tiene los pasos y las versiones." % MONO)

# =====================================================================================
# 7. ETAPA 4
# =====================================================================================
story.append(PageBreak())
h("7. Etapa 4. Calidad del software")
h("7.1 Investigación", h2)
p("La ISO/IEC 25010 (International Organization for Standardization [ISO], 2023) define un modelo de calidad del producto: una lista de características que "
  "dicen qué significa que un software sea \"de calidad\", cada una dividida en subcaracterísticas que se "
  "pueden evaluar. La versión 2023 tiene nueve: adecuación funcional, eficiencia de desempeño, compatibilidad, "
  "capacidad de interacción (antes usabilidad), fiabilidad, seguridad, mantenibilidad, flexibilidad (antes "
  "portabilidad) y protección. No todas pesan lo mismo en todos los proyectos; el modelo sirve para escoger "
  "cuáles importan y medirlas.")
p("CMMI describe qué tan maduro es el proceso con que una organización hace software, en cinco niveles "
  "(CMMI Product Team, 2010). <b>Nivel 1, inicial:</b> el trabajo sale, pero depende del esfuerzo de las "
  "personas y no se puede predecir. <b>Nivel 2, gestionado:</b> cada proyecto se planea, se controlan sus "
  "requisitos y se hace seguimiento. <b>Nivel 3, definido:</b> la organización tiene procesos estándar que todos "
  "los proyectos adaptan. <b>Nivel 4, gestionado cuantitativamente:</b> el proceso se controla con mediciones. "
  "<b>Nivel 5, en optimización:</b> se mejora de forma continua a partir de esas mediciones.")
p("En Scrum la calidad no se deja para el final. La <b>definición de terminado</b> es la lista de condiciones "
  "que debe cumplir un incremento para considerarse terminado; si no las cumple, no se presenta (Schwaber y "
  "Sutherland, 2020). La <b>revisión de código</b> entre compañeros encuentra defectos antes de ejecutar y "
  "reparte el conocimiento. La <b>integración continua</b> consiste en integrar los cambios varias veces al día "
  "con una compilación automática que corre todas las pruebas, para que un error se vea en minutos y no al "
  "final (Fowler, 2006).")

h("7.2 Características de ISO/IEC 25010 para AgroDirecto", h2)
tabla("Características escogidas", [
    ["Característica", "Subcaracterísticas", "Por qué importa en AgroDirecto", "Cómo la cubrimos"],
    ["Adecuación funcional", "Corrección funcional", "El sistema calcula totales y maneja el estado de pedidos que el agricultor cobra. Un total mal calculado o un pedido duplicado es plata perdida para alguien.", "CP-12 a CP-19, valores límite y tabla de decisión."],
    ["Fiabilidad", "Tolerancia a fallos", "Un solo dato raro no puede tumbar el servicio para todos. D-02 mostró justo eso: un correo vacío dejaba el registro inservible.", "CP-10 comprueba que, después de un dato inválido, el siguiente registro funciona."],
    ["Capacidad de interacción", "Protección contra errores del usuario; autodescripción", "Muchos usuarios son personas del campo con poca experiencia digital. El sistema debe atajar sus errores y decir con claridad qué corregir.", "CP-01 a CP-06 atajan datos mal escritos. El mensaje del celular todavía no explica la regla (CP-20 pendiente)."],
], [3.0, 3.2, 6.3, 4.5], fs=8.5)
p("Dejamos por fuera la seguridad aunque manejamos datos personales, porque hoy el proyecto no guarda "
  "contraseñas ni datos en un servidor; será la siguiente característica cuando exista la base de datos.")

h("7.3 Nivel de madurez CMMI del equipo", h2)
tabla("Cómo trabajamos este semestre", [
    ["Práctica", "Lo que hicimos realmente"],
    ["Requisitos", "Sí estaban escritos (RF-01 a RF-05), pero los de pedidos no existían hasta esta entrega y los cambios no se registraban."],
    ["Planeación", "No había plan de pruebas ni cronograma antes de esta entrega; se trabajaba para la fecha de cada guía."],
    ["Pruebas", "Probábamos, pero al final y no siempre antes de entregar. El defecto D-02 se vio en la guía 2 y quedó abierto."],
    ["Revisión de código", "No revisábamos el código de los demás de forma sistemática."],
    ["Control de versiones", "El repositorio tenía un solo commit con todo el proyecto, y quedaron clases duplicadas de entregas viejas."],
], [3.5, 13.5])
p("Con estos hechos nos ubicamos en el <b>nivel 1 (inicial)</b>. Las cosas salieron, pero por el esfuerzo de "
  "cada uno y no por un proceso que se pueda repetir. Tenemos algunas prácticas de nivel 2, como requisitos "
  "escritos y ahora un plan de pruebas, pero no las aplicamos de forma constante.")
p("Para subir al nivel 2 tendríamos que: planear cada entrega con tareas, responsables y fechas, y revisar "
  "cada semana cómo vamos; llevar un registro de cambios de requisitos; trabajar con commits pequeños de cada "
  "integrante y revisar el código de los demás antes de unirlo; y correr las pruebas antes de cada entrega, no "
  "después.")

h("7.4 Definición de terminado", h2)
p("De aquí en adelante, una funcionalidad está terminada cuando cumple todo esto:")
items([
    "Responde a un requisito escrito y verificable.",
    "Compila sin errores con mvn clean test.",
    "Tiene pruebas JUnit con el código del caso en el nombre, incluidos sus valores límite, y todas pasan.",
    "El reporte de JaCoCo no muestra ramas sin probar en el código nuevo, o las que quedan están justificadas.",
    "Las pruebas que ya existían siguen pasando (regresión).",
    "Otro integrante revisó el código antes de unirlo a la rama principal.",
    "No deja defectos de severidad alta abiertos.",
    "Está en el repositorio con un commit que dice qué se hizo, y la matriz de trazabilidad está actualizada.",
])

# =====================================================================================
# 8-11. CIERRE
# =====================================================================================
h("8. Conclusiones y lecciones aprendidas")
p("Lo más claro que nos deja este trabajo es que los defectos estaban en los bordes. Las pruebas con datos "
  "\"normales\" pasaron desde la primera guía; los problemas aparecieron con los dígitos de ancho completo, el "
  "correo vacío y el correo con un espacio al final. Diseñar con particiones y valores límite nos obligó a "
  "pensar en esos casos antes de escribir la prueba.")
p("También aprendimos que encontrar un defecto no sirve de mucho si no se registra y se corrige. El correo "
  "nulo lo vimos en la guía 2, lo anotamos como hallazgo y siguió ahí hasta esta entrega. Con un registro de "
  "defectos y una definición de terminado eso no habría pasado.")
p("La medición de cobertura nos enseñó a no confiar en el análisis hecho a mano: creíamos tener 100 % de ramas "
  "en celularValido y JaCoCo mostró que faltaba una, justo la de un caso que ya habíamos probado en la guía 1 y "
  "perdimos al reorganizar las pruebas.")
p("Escribir los requisitos de pedidos nos mostró código que no respondía a nada (el costo de envío, la suma de "
  "kilos) y clases duplicadas que inflaban el número de pruebas. Al quitarlas, el proyecto quedó más corto y "
  "más fácil de explicar. Por último, ubicarnos en el nivel 1 de CMMI fue incómodo pero honesto: lo primero que "
  "cambiaríamos es trabajar con commits y revisiones de todos durante la semana, y no solo antes de entregar.")

h("9. Aportes por integrante")
tabla("Aportes por integrante", [
    ["Integrante", "Qué hizo"],
    ["Juan Andrés Hoyos Cruz", "Depuración del código, automatización de las pruebas de registro (CP-01 a CP-11), ejecución y evidencias de JUnit, README."],
    ["Jonathan David Ceballos Jiménez", "Corrección y ampliación de requisitos, nota de cambios, matriz de trazabilidad, CMMI y definición de terminado."],
    ["Leonardo Argoty", "Etapa 1: particiones, valores límite, tabla de decisión de RF-08 y caminos de celularValido. Simulación de aceptación."],
    ["Owen Fernando Bareño", "Plan de pruebas, casos de prueba, registro de defectos, automatización de pedidos (CP-12 a CP-19) e ISO/IEC 25010."],
], [5.5, 11.5])

h("10. Declaración de uso de herramientas de IA")
p("Usamos Claude (Anthropic) como asistente en tres partes: para revisar y simplificar el código del proyecto "
  "(quitar clases duplicadas, métodos sin requisito y la clase que comparaba con System.out.println), para "
  "proponer la estructura de las clases de prueba JUnit y para redactar un primer borrador de este documento. "
  "Revisamos todo lo que propuso, ejecutamos las pruebas nosotros mismos y ajustamos los textos. Los "
  "resultados de ejecución y los defectos que aparecen son reales y salen de la salida de Maven que está en la "
  "carpeta de evidencias del repositorio.")

h("11. Referencias")
for r in [
    "Apache Maven Project. (2024). <i>Maven Surefire Plugin</i>. https://maven.apache.org/surefire/maven-surefire-plugin/",
    "CMMI Product Team. (2010). <i>CMMI for Development, version 1.3</i> (CMU/SEI-2010-TR-033). Software Engineering Institute, Carnegie Mellon University.",
    "Copeland, L. (2004). <i>A practitioner's guide to software test design</i>. Artech House.",
    "Fowler, M. (2006). <i>Continuous integration</i>. https://martinfowler.com/articles/continuousIntegration.html",
    "IEEE. (2008). <i>IEEE standard for software and system test documentation</i> (IEEE Std 829-2008). https://doi.org/10.1109/IEEESTD.2008.4578383",
    "International Organization for Standardization. (2023). <i>Systems and software engineering. Systems and software Quality Requirements and Evaluation (SQuaRE). Product quality model</i> (ISO/IEC 25010:2023).",
    "International Software Testing Qualifications Board. (2023). <i>Certified Tester Foundation Level syllabus</i> (versión 4.0).",
    "ISO/IEC/IEEE. (2021). <i>Software and systems engineering. Software testing. Part 3: Test documentation</i> (ISO/IEC/IEEE 29119-3:2021).",
    "JUnit Team. (2024). <i>JUnit 5 user guide</i>. https://junit.org/junit5/docs/current/user-guide/",
    "Myers, G. J., Sandler, C. y Badgett, T. (2012). <i>The art of software testing</i> (3.ª ed.). John Wiley &amp; Sons.",
    "Pressman, R. S. y Maxim, B. R. (2020). <i>Software engineering: A practitioner's approach</i> (9.ª ed.). McGraw-Hill Education.",
    "Schwaber, K. y Sutherland, J. (2020). <i>La guía de Scrum</i>. https://scrumguides.org/",
    "Sommerville, I. (2016). <i>Software engineering</i> (10.ª ed.). Pearson.",
]:
    p(r, ref)


def pie(canvas, doc):
    if doc.page > 1:
        canvas.setFont(F, 9)
        canvas.drawRightString(LETTER[0] - 2.2 * cm, 1.3 * cm, str(doc.page))


doc = SimpleDocTemplate(SALIDA, pagesize=LETTER, leftMargin=2.3 * cm, rightMargin=2.3 * cm,
                        topMargin=2.2 * cm, bottomMargin=2.2 * cm,
                        title="Plan de aseguramiento de calidad - AgroDirecto",
                        author="Ceballos, Argoty, Bareño, Hoyos")
doc.build(story, onFirstPage=pie, onLaterPages=pie)
print("PDF generado:", SALIDA)
