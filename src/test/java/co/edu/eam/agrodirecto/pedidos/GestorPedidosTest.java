package co.edu.eam.agrodirecto.pedidos;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.ValueSource;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** Pruebas unitarias de GestorPedidos (RF-06 a RF-09). */
class GestorPedidosTest {

    private static final long T0 = 1_700_000_000_000L;
    private static final double PRECIO_KG = 3000;

    private GestorPedidos gestor;

    @BeforeEach
    void setUp() {
        gestor = new GestorPedidos();
    }

    @ParameterizedTest
    @ValueSource(ints = {1, 500, 1000})
    void CP12_cantidadDentroDelRangoEsValida(int kg) {
        assertTrue(gestor.esValido(new Pedido("A001", "tomate", kg, T0)));
    }

    @ParameterizedTest
    @ValueSource(ints = {-5, 0, 1001})
    void CP13_cantidadFueraDelRangoEsInvalida(int kg) {
        assertFalse(gestor.esValido(new Pedido("A001", "tomate", kg, T0)));
    }

    @ParameterizedTest
    @CsvSource({"0, 15000", "10, 13500", "100, 0"})
    void CP14_descuentoEnLosLimitesCalculaElTotal(int descuento, double esperado) {
        Pedido cincoKg = new Pedido("A001", "tomate", 5, T0);

        assertEquals(esperado, gestor.calcularTotal(cincoKg, PRECIO_KG, descuento), 0.001);
    }

    @ParameterizedTest
    @ValueSource(ints = {-1, 101})
    void CP15_descuentoFueraDeRangoEsRechazado(int descuento) {
        Pedido cincoKg = new Pedido("A001", "tomate", 5, T0);

        assertThrows(IllegalArgumentException.class, () -> gestor.calcularTotal(cincoKg, PRECIO_KG, descuento));
    }

    @ParameterizedTest
    @CsvSource({"119999, true", "120000, false"})
    void CP16_bordeDeLaVentanaDeDosMinutos(long msDespues, boolean esperado) {
        Pedido anterior = new Pedido("A001", "tomate", 5, T0);
        Pedido nuevo = new Pedido("A001", "tomate", 5, T0 + msDespues);

        assertEquals(esperado, gestor.esDuplicado(List.of(anterior), nuevo));
    }

    // Reglas R1 a R5 de la tabla de decisión de RF-08. El pedido anterior es (A001, tomate, 5 kg, T0).
    @ParameterizedTest(name = "{0}")
    @CsvSource({
            "R1, A001, tomate, 5, 30000, true",
            "R2, B002, tomate, 5, 30000, false",
            "R3, A001, papa,   5, 30000, false",
            "R4, A001, tomate, 6, 30000, false",
            "R5, A001, tomate, 5, 600000, false"
    })
    void CP17_tablaDeDecisionDeDuplicados(String regla, String comprador, String producto,
                                          int kg, long msDespues, boolean esperado) {
        Pedido anterior = new Pedido("A001", "tomate", 5, T0);
        Pedido nuevo = new Pedido(comprador, producto, kg, T0 + msDespues);

        assertEquals(esperado, gestor.esDuplicado(List.of(anterior), nuevo));
    }

    @ParameterizedTest(name = "{0} -> {1}: {2}")
    @CsvSource({
            "PENDIENTE, PAGADO, true",
            "PENDIENTE, CANCELADO, true",
            "PAGADO, ENVIADO, true",
            "PAGADO, CANCELADO, true",
            "ENVIADO, ENTREGADO, true",
            "PENDIENTE, ENVIADO, false",
            "PAGADO, PENDIENTE, false",
            "ENVIADO, CANCELADO, false",
            "ENTREGADO, CANCELADO, false",
            "CANCELADO, PAGADO, false"
    })
    void CP18_transicionesDeEstado(EstadoPedido actual, EstadoPedido destino, boolean permitido) {
        assertEquals(permitido, gestor.puedePasarA(actual, destino));
    }
}
