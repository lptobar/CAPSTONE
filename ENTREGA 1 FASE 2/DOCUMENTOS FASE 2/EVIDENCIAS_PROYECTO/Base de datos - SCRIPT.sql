INSERT INTO core_genero (nombre_genero) VALUES ('Masculino'), ('Femenino');
INSERT INTO core_jornada (nombre_jornada) VALUES ('Diurno'), ('Vespertino');
INSERT INTO core_estadocurso (nombre_estado_curso) VALUES ('Cerrado'), ('Activo'), ('Borrado');
INSERT INTO core_prioridadnoticia (nombre_prioridad_noticia) VALUES ('Alta'), ('Media'), ('Baja');
INSERT INTO core_listacurso (nombre_curso) VALUES ('1° Basico'), ('2° Basico'), ('3° Basico'), ('4° Basico'), ('5° Basico'), ('6° Basico'), ('7° Basico'), ('8° Basico');
INSERT INTO core_region (nombre_region) VALUES ('Arica y Parinacota'), ('Tarapacá'), ('Antofagasta'), ('Atacama'), ('Coquimbo'), ('Valparaíso'), ('Metropolitana de Santiago'), ('OHiggins'), ('Maule'), ('Biobío'), ('La Araucanía'), ('Los Ríos'), ('Los Lagos'), ('Aysén del General Carlos Ibáñez del Campo'), ('Magallanes y de la Antártica Chilena');
INSERT INTO core_tipoanotacion (nombre_tipo_anotacion) VALUES ('Negativa'), ('Positiva');
INSERT INTO core_tipoasistencia (nombre_tipo_asistencia) VALUES ('Ausente'), ('Presente'), ('Justificado');
INSERT INTO core_tipocurso (nombre_tipo_curso) VALUES ('A'), ('B');
INSERT INTO core_tipomensualidad (nombre_tipo_mensualidad) VALUES ('Matricula'), ('Mensual');
INSERT INTO core_tipousuario (nombre_tipo_usuario) VALUES ('Alumno'), ('Apoderado'), ('Profesor'), ('Secretaria'), ('Administrador');
INSERT INTO core_listaasignatura (nombre_asignatura) VALUES ('Lenguaje'), ('Matematica'), ('Historia'), ('Ingles'), ('Ciencias');

-- POR MIENTRAS
INSERT INTO core_cargofuncionario (nombre_cargo_funcionario) VALUES ('Profesor'), ('Administrador');
INSERT INTO core_estadoalumno (nombre_estado_alumno) VALUES ('Inactivo'), ('Activo');
INSERT INTO core_estadomatricula (nombre_estado_matricula) VALUES ('Inactiva'), ('Activa');
INSERT INTO core_estadomensualidad (nombre_estado_mensualidad) VALUES ('Pendiente'), ('Pagada');
INSERT INTO core_nacionalidad (nombre_nacionalidad) VALUES ('Chileno');
INSERT INTO core_nivelacademico (nombre_nivel_academico) VALUES ('Nivel academico 1');
INSERT INTO core_tipoespecializacion (tipo_especializacion) VALUES ('Especializacion 1');
INSERT INTO core_tiponoticia (nombre_tipo_noticia) VALUES ('Comunidad');
INSERT INTO core_diasemana (nombre_dia) VALUES ('Lunes'), ('Martes'), ('Miércoles'), ('Jueves'), ('Viernes');
INSERT INTO core_parentesco (nombre_parentesco) VALUES ('Padre'), ('Madre'), ('Abuelo'), ('Abuela'), ('Tio'), ('Tia');
INSERT INTO core_estadoreunion (nombre_estado_reunion) VALUES ('Pendiente'), ('Rechazada'), ('Aceptada'), ('Terminada');

INSERT INTO core_region (nombre_region) VALUES ('Región Metropolitana');
INSERT INTO core_comuna (id_comuna, nombre_comuna, id_region) VALUES (4, 'La Florida', 1);