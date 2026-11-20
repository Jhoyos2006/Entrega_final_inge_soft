package co.edu.eam.agrodirecto.pedidos;

/** Ciclo de vida de un pedido. Todo pedido nace en PENDIENTE. */
public enum EstadoPedido {
    PENDIENTE,
    PAGADO,
    ENVIADO,
    ENTREGADO,
    CANCELADO
}
