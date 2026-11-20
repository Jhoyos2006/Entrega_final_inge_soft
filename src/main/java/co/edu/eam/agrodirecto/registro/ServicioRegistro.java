package co.edu.eam.agrodirecto.registro;

import java.util.HashSet;
import java.util.Locale;
import java.util.Set;

/**
 * Registra usuarios aplicando RF-01 a RF-05 en orden. Devuelve "OK" o el mensaje de la primera regla que falla.
 */
public class ServicioRegistro {

    /** Correos ya registrados, guardados sin espacios y en minúscula (RF-05). */
    private final Set<String> correos = new HashSet<>();

    public String registrar(String rol, String finca, String municipio,
                            String celular, boolean aceptaPolitica, String correo) {
        if (!ValidadorRegistro.rolValido(rol)) {
            return "ERROR: rol invalido";
        }
        if (!ValidadorRegistro.datosAgricultorValidos(rol, finca, municipio)) {
            return "ERROR: finca y municipio obligatorios";
        }
        if (!ValidadorRegistro.celularValido(celular)) {
            return "ERROR: celular invalido";
        }
        if (!aceptaPolitica) {
            return "ERROR: politica no aceptada";
        }
        if (!ValidadorRegistro.tieneTexto(correo)) {
            return "ERROR: correo invalido";
        }
        if (!correos.add(correo.trim().toLowerCase(Locale.ROOT))) {
            return "ERROR: correo ya registrado";
        }
        return "OK";
    }

    public int cantidadRegistrados() {
        return correos.size();
    }
}
