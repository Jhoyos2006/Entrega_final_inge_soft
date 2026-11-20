package co.edu.eam.agrodirecto.registro;

/**
 * Reglas del registro de usuarios. Cada método revisa una sola regla y no depende de otras clases.
 */
public final class ValidadorRegistro {

    private ValidadorRegistro() {
    }

    /** RF-01: el rol debe ser exactamente AGRICULTOR o COMPRADOR. */
    public static boolean rolValido(String rol) {
        return "AGRICULTOR".equals(rol) || "COMPRADOR".equals(rol);
    }

    /** RF-02: si es AGRICULTOR, finca y municipio deben tener texto. Al COMPRADOR no se le exigen. */
    public static boolean datosAgricultorValidos(String rol, String finca, String municipio) {
        if (!"AGRICULTOR".equals(rol)) {
            return true;
        }
        return tieneTexto(finca) && tieneTexto(municipio);
    }

    /** RF-03: exactamente 10 dígitos (0-9) y empieza por 3. */
    public static boolean celularValido(String celular) {
        if (celular == null || celular.length() != 10) {
            return false;
        }
        if (celular.charAt(0) != '3') {
            return false;
        }
        for (char c : celular.toCharArray()) {
            if (c < '0' || c > '9') {
                return false;
            }
        }
        return true;
    }

    /** No nulo, no vacío y no solo espacios. */
    static boolean tieneTexto(String texto) {
        return texto != null && !texto.isBlank();
    }
}
