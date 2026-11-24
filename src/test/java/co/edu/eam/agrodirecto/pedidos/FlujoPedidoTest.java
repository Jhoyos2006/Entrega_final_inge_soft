package co.edu.eam.agrodirecto.pedidos;

import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** Prueba de integración: Pedido, EstadoPedido y GestorPedidos en el ciclo completo de una compra. */
class FlujoPedidoTest {

    @Test
    void CP19_pedidoRecorreTodoSuCicloDeVida() {
        GestorPedidos gestor = new GestorPedidos();
        List<Pedido> historial = new ArrayList<>();
        Pedido pedido = new Pedido("A001", "tomate", 5, 1_700_000_000_000L);

        assertTrue(gestor.esValido(pedido));
        assertFalse(gestor.esDuplicado(historial, pedido));
        assertEquals(13_500, gestor.calcularTotal(pedido, 3000, 10), 0.001);
        historial.add(pedido);

        gestor.cambiarEstado(pedido, EstadoPedido.PAGADO);
        gestor.cambiarEstado(pedido, EstadoPedido.ENVIADO);
        assertThrows(IllegalStateException.class, () -> gestor.cambiarEstado(pedido, EstadoPedido.CANCELADO));
        gestor.cambiarEstado(pedido, EstadoPedido.ENTREGADO);

        assertEquals(EstadoPedido.ENTREGADO, pedido.getEstado());
    }
}
