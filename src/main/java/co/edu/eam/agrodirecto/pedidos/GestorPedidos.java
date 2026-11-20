package co.edu.eam.agrodirecto.pedidos;

import java.util.List;

/** Reglas de negocio de los pedidos (RF-06 a RF-09). */
public class GestorPedidos {

    public static final int MIN_KG = 1;
    public static final int MAX_KG = 1000;
    public static final long VENTANA_DUPLICADO_MS = 2 * 60 * 1000;

    /** RF-06: comprador y producto con texto, y cantidad entre 1 y 1000 kg. */
    public boolean esValido(Pedido pedido) {
        return pedido != null
                && tieneTexto(pedido.getCompradorId())
                && tieneTexto(pedido.getProducto())
                && pedido.getCantidadKg() >= MIN_KG
                && pedido.getCantidadKg() <= MAX_KG;
    }

    /** RF-07: total = kg x precio por kg, menos un descuento entre 0 y 100 %. */
    public double calcularTotal(Pedido pedido, double precioKg, int descuento) {
        if (precioKg <= 0) {
            throw new IllegalArgumentException("El precio por kg debe ser mayor que 0");
        }
        if (descuento < 0 || descuento > 100) {
            throw new IllegalArgumentException("El descuento debe estar entre 0 y 100");
        }
        return pedido.getCantidadKg() * precioKg * (100 - descuento) / 100;
    }

    /** RF-08: mismo comprador, producto y cantidad en menos de 2 minutos es un duplicado. */
    public boolean esDuplicado(List<Pedido> recientes, Pedido nuevo) {
        for (Pedido p : recientes) {
            if (p.getCompradorId().equals(nuevo.getCompradorId())
                    && p.getProducto().equals(nuevo.getProducto())
                    && p.getCantidadKg() == nuevo.getCantidadKg()
                    && nuevo.getCreadoEnMs() - p.getCreadoEnMs() < VENTANA_DUPLICADO_MS) {
                return true;
            }
        }
        return false;
    }

    /** RF-09: PENDIENTE -> PAGADO -> ENVIADO -> ENTREGADO. Solo se cancela antes de enviar. */
    public boolean puedePasarA(EstadoPedido actual, EstadoPedido destino) {
        if (actual == null || destino == null) {
            return false;
        }
        return switch (actual) {
            case PENDIENTE -> destino == EstadoPedido.PAGADO || destino == EstadoPedido.CANCELADO;
            case PAGADO -> destino == EstadoPedido.ENVIADO || destino == EstadoPedido.CANCELADO;
            case ENVIADO -> destino == EstadoPedido.ENTREGADO;
            case ENTREGADO, CANCELADO -> false;
        };
    }

    /** Aplica la transición si RF-09 la permite; si no, lanza IllegalStateException. */
    public void cambiarEstado(Pedido pedido, EstadoPedido destino) {
        if (!puedePasarA(pedido.getEstado(), destino)) {
            throw new IllegalStateException(pedido.getEstado() + " -> " + destino + " no está permitido");
        }
        pedido.setEstado(destino);
    }

    private static boolean tieneTexto(String texto) {
        return texto != null && !texto.isBlank();
    }
}
