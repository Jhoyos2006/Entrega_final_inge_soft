package co.edu.eam.agrodirecto.registro;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.NullAndEmptySource;
import org.junit.jupiter.params.provider.ValueSource;

import static org.junit.jupiter.api.Assertions.assertEquals;

/** Pruebas de integración: ServicioRegistro trabajando con ValidadorRegistro (RF-01 a RF-05). */
class ServicioRegistroTest {

    private ServicioRegistro servicio;

    @BeforeEach
    void setUp() {
        servicio = new ServicioRegistro();
    }

    // Cada fila rompe una sola regla; las demás son válidas.
    @ParameterizedTest(name = "{5}")
    @CsvSource({
            "VENDEDOR,   Finca El Cafe, Armenia, 3124567890, true,  ERROR: rol invalido",
            "AGRICULTOR, '',            Armenia, 3124567890, true,  ERROR: finca y municipio obligatorios",
            "AGRICULTOR, Finca El Cafe, Armenia, 312345678,  true,  ERROR: celular invalido",
            "AGRICULTOR, Finca El Cafe, Armenia, 3124567890, false, ERROR: politica no aceptada"
    })
    void CP07_datoInvalidoSeRechazaConSuMensajeYNoSeRegistra(String rol, String finca, String municipio,
                                                            String celular, boolean politica, String mensaje) {
        String r = servicio.registrar(rol, finca, municipio, celular, politica, "pedro@mail.com");

        assertEquals(mensaje, r);
        assertEquals(0, servicio.cantidadRegistrados());
    }

    @Test
    void CP08_correoRepetidoConMayusculasEsRechazado() {
        servicio.registrar("COMPRADOR", "", "", "3124567890", true, "ana@mail.com");

        String r = servicio.registrar("COMPRADOR", "", "", "3109876543", true, "ANA@Mail.com");

        assertEquals("ERROR: correo ya registrado", r);
        assertEquals(1, servicio.cantidadRegistrados());
    }

    @Test
    void CP09_correoRepetidoConEspaciosEsRechazado() {
        servicio.registrar("COMPRADOR", "", "", "3124567890", true, "ana@mail.com");

        String r = servicio.registrar("COMPRADOR", "", "", "3109876543", true, " ana@mail.com ");

        assertEquals("ERROR: correo ya registrado", r);
    }

    @ParameterizedTest
    @NullAndEmptySource
    @ValueSource(strings = "   ")
    void CP10_correoVacioEsRechazadoYElServicioSigueFuncionando(String correo) {
        String r = servicio.registrar("COMPRADOR", "", "", "3124567890", true, correo);
        String siguiente = servicio.registrar("COMPRADOR", "", "", "3124567890", true, "leo@mail.com");

        assertEquals("ERROR: correo invalido", r);
        assertEquals("OK", siguiente);
    }

    @Test
    void CP11_agricultorConTodosLosDatosQuedaRegistrado() {
        String r = servicio.registrar("AGRICULTOR", "Finca La Esperanza", "Calarca", "3104567890", true, "rosa@mail.com");

        assertEquals("OK", r);
        assertEquals(1, servicio.cantidadRegistrados());
    }
}
