package co.edu.eam.agrodirecto.registro;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.NullAndEmptySource;
import org.junit.jupiter.params.provider.NullSource;
import org.junit.jupiter.params.provider.ValueSource;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** Pruebas unitarias de ValidadorRegistro (RF-01 a RF-03). */
class ValidadorRegistroTest {

    @ParameterizedTest
    @ValueSource(strings = {"AGRICULTOR", "COMPRADOR"})
    void CP01_rolesPermitidosSonAceptados(String rol) {
        assertTrue(ValidadorRegistro.rolValido(rol));
    }

    @ParameterizedTest
    @NullAndEmptySource
    @ValueSource(strings = {"agricultor", "VENDEDOR"})
    void CP02_rolVacioOFueraDeLaListaEsRechazado(String rol) {
        assertFalse(ValidadorRegistro.rolValido(rol));
    }

    // Campo vacío en el CSV = null; '' = texto vacío.
    @ParameterizedTest
    @CsvSource({
            "'   ', Armenia",
            "Finca El Cafe, ''",
            ", Armenia",
            "Finca El Cafe, '\t '"
    })
    void CP03_agricultorSinFincaOMunicipioEsRechazado(String finca, String municipio) {
        assertFalse(ValidadorRegistro.datosAgricultorValidos("AGRICULTOR", finca, municipio));
    }

    @Test
    void CP04_compradorNoNecesitaFincaNiMunicipio() {
        assertTrue(ValidadorRegistro.datosAgricultorValidos("COMPRADOR", null, null));
    }

    @ParameterizedTest
    @ValueSource(strings = {"3000000000", "3124567890", "3999999999"})
    void CP05_celularDe10DigitosQueEmpiezaPor3EsAceptado(String celular) {
        assertTrue(ValidadorRegistro.celularValido(celular));
    }

    @ParameterizedTest
    @NullSource
    @ValueSource(strings = {
            "312345678",    // 9 dígitos
            "31234567890",  // 11 dígitos
            "2999999999",   // empieza por 2
            "4000000000",   // empieza por 4
            "31A4567890",   // tiene una letra (carácter mayor que '9')
            "312 456789",   // tiene un espacio (carácter menor que '0')
            "3１２３４５６７８９" // dígitos de ancho completo (defecto D-01)
    })
    void CP06_celularFueraDeLaReglaEsRechazado(String celular) {
        assertFalse(ValidadorRegistro.celularValido(celular));
    }
}
