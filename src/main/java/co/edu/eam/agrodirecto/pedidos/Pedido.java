package co.edu.eam.agrodirecto.pedidos;

/** Orden de compra de un comprador. Solo GestorPedidos puede cambiar su estado. */
public class Pedido {

    private final String compradorId;
    private final String producto;
    private final int cantidadKg;
    private final long creadoEnMs;
    private EstadoPedido estado = EstadoPedido.PENDIENTE;

    public Pedido(String compradorId, String producto, int cantidadKg, long creadoEnMs) {
        this.compradorId = compradorId;
        this.producto = producto;
        this.cantidadKg = cantidadKg;
        this.creadoEnMs = creadoEnMs;
    }

    public String getCompradorId() {
        return compradorId;
    }

    public String getProducto() {
        return producto;
    }

    public int getCantidadKg() {
        return cantidadKg;
    }

    public long getCreadoEnMs() {
        return creadoEnMs;
    }

    public EstadoPedido getEstado() {
        return estado;
    }

    void setEstado(EstadoPedido estado) {
        this.estado = estado;
    }
}
