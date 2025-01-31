% Respuestas generales según el tipo de PQRS
respuesta(peticion, "Su petición ha sido recibida y será procesada.").  
respuesta(queja, "Hemos registrado su queja y tomaremos acciones.").  
respuesta(reclamo, "Su reclamo ha sido recibido y será analizado.").

% Respuestas personalizadas si la descripción contiene ciertas palabras clave
respuesta_personalizada("demora", "Lamentamos la demora. Estamos trabajando para mejorar los tiempos de respuesta.").
respuesta_personalizada("mala atención", "Tomaremos medidas para mejorar la atención al cliente.").
respuesta_personalizada("reembolso", "Su solicitud de reembolso será evaluada por nuestro equipo.").

% Validar que la cédula tenga entre 8 y 10 dígitos
validar_cedula(Cedula) :- 
    atom_length(Cedula, Longitud),
    Longitud >= 8, Longitud =< 10.

% Obtener la respuesta final
obtener_respuesta(Nombre, Tipo, Cedula, Descripcion, RespuestaFinal) :-
    (validar_cedula(Cedula) ->  
        respuesta(Tipo, RespuestaBase),  
        (buscar_palabra_clave(Descripcion, RespuestaExtra) ->  
            atomic_list_concat([Nombre, ", ", RespuestaBase, " ", RespuestaExtra], RespuestaFinal)
        ;  
            atomic_list_concat([Nombre, ", ", RespuestaBase], RespuestaFinal)  
        )
    ;  
        atomic_list_concat([Nombre, ", el número de cédula ingresado no es válido. Debe tener entre 8 y 10 dígitos."], RespuestaFinal)
    ).

% Buscar palabras clave en la descripción
buscar_palabra_clave(Descripcion, Respuesta) :-
    respuesta_personalizada(Palabra, Respuesta),
    sub_atom(Descripcion, _, _, _, Palabra).  % Verifica si la palabra está en la descripción
