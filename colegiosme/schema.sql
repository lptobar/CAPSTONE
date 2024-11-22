--
-- Create model Archivo
--
CREATE TABLE `core_archivo` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `archivo` varchar(100) NOT NULL);
--
-- Create model ArchivoEntrega
--
CREATE TABLE `core_archivoentrega` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `archivo` varchar(100) NOT NULL);
--
-- Create model BloqueHorario
--
CREATE TABLE `core_bloquehorario` (`id_bloque` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre_bloque` varchar(40) NOT NULL, `hora_inicio` time(6) NOT NULL, `hora_fin` time(6) NOT NULL);
--
-- Create model CargoFuncionario
--
CREATE TABLE `core_cargofuncionario` (`id_cargo_funcionario` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre_cargo_funcionario` varchar(40) NOT NULL);
--
-- Create model Comuna
--
CREATE TABLE `core_comuna` (`id_comuna` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre_comuna` varchar(100) NOT NULL);
--
-- Create model DiaSemana
--
CREATE TABLE `core_diasemana` (`id_dia` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre_dia` varchar(40) NOT NULL);
--
-- Create model EstadoAlumno
--
CREATE TABLE `core_estadoalumno` (`id_estado_alumno` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre_estado_alumno` varchar(40) NOT NULL);
--
-- Create model EstadoCurso
--
CREATE TABLE `core_estadocurso` (`id_estado_curso` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre_estado_curso` varchar(40) NOT NULL);
--
-- Create model EstadoMatricula
--
CREATE TABLE `core_estadomatricula` (`id_estado_matricula` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre_estado_matricula` varchar(40) NOT NULL);
--
-- Create model EstadoMensualidad
--
CREATE TABLE `core_estadomensualidad` (`id_estado_mensualidad` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre_estado_mensualidad` varchar(40) NOT NULL);
--
-- Create model EstadoReunion
--
CREATE TABLE `core_estadoreunion` (`id_estado_reunion` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre_estado_reunion` varchar(25) NOT NULL);
--
-- Create model Genero
--
CREATE TABLE `core_genero` (`id_genero` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre_genero` varchar(10) NOT NULL);
--
-- Create model Jornada
--
CREATE TABLE `core_jornada` (`id_jornada` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre_jornada` varchar(10) NOT NULL);
--
-- Create model ListaAsignatura
--
CREATE TABLE `core_listaasignatura` (`id_lista_asignatura` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre_asignatura` varchar(40) NOT NULL);
--
-- Create model ListaCurso
--
CREATE TABLE `core_listacurso` (`id_lista_curso` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre_curso` varchar(40) NOT NULL);
--
-- Create model Nacionalidad
--
CREATE TABLE `core_nacionalidad` (`id_nacionalidad` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre_nacionalidad` varchar(60) NOT NULL);
--
-- Create model NivelAcademico
--
CREATE TABLE `core_nivelacademico` (`id_nivel_academico` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre_nivel_academico` varchar(40) NOT NULL);
--
-- Create model Parentesco
--
CREATE TABLE `core_parentesco` (`id_parentesco` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre_parentesco` varchar(40) NOT NULL);
--
-- Create model PrioridadNoticia
--
CREATE TABLE `core_prioridadnoticia` (`id_prioridad_noticia` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre_prioridad_noticia` varchar(40) NOT NULL);
--
-- Create model Region
--
CREATE TABLE `core_region` (`id_region` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre_region` varchar(100) NOT NULL);
--
-- Create model TipoAnotacion
--
CREATE TABLE `core_tipoanotacion` (`id_tipo_anotacion` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre_tipo_anotacion` varchar(10) NOT NULL);
--
-- Create model TipoAsistencia
--
CREATE TABLE `core_tipoasistencia` (`id_tipo_asistencia` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre_tipo_asistencia` varchar(40) NOT NULL);
--
-- Create model TipoCurso
--
CREATE TABLE `core_tipocurso` (`id_letra_curso` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre_tipo_curso` varchar(1) NOT NULL);
--
-- Create model TipoEspecializacion
--
CREATE TABLE `core_tipoespecializacion` (`id_tipo_especializacion` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `tipo_especializacion` varchar(45) NOT NULL);
--
-- Create model TipoMensualidad
--
CREATE TABLE `core_tipomensualidad` (`id_tipo_mensualidad` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre_tipo_mensualidad` varchar(40) NOT NULL);
--
-- Create model TipoNoticia
--
CREATE TABLE `core_tiponoticia` (`id_tipo_noticia` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre_tipo_noticia` varchar(40) NOT NULL);
--
-- Create model TipoTarea
--
CREATE TABLE `core_tipotarea` (`id_tipo_tarea` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre_tipo_tarea` varchar(25) NOT NULL);
--
-- Create model TipoUsuario
--
CREATE TABLE `core_tipousuario` (`id_tipo_usuario` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre_tipo_usuario` varchar(40) NOT NULL);
--
-- Create model Usuario
--
CREATE TABLE `core_usuario` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `password` varchar(128) NOT NULL, `last_login` datetime(6) NULL, `is_superuser` bool NOT NULL, `username` varchar(150) NOT NULL UNIQUE, `email` varchar(254) NOT NULL, `is_staff` bool NOT NULL, `is_active` bool NOT NULL, `date_joined` datetime(6) NOT NULL);
CREATE TABLE `core_usuario_groups` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `usuario_id` bigint NOT NULL, `group_id` integer NOT NULL);
CREATE TABLE `core_usuario_user_permissions` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `usuario_id` bigint NOT NULL, `permission_id` integer NOT NULL);
--
-- Create model Alumno
--
CREATE TABLE `core_alumno` (`id_alumno` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `alumno_prioritario` bool NOT NULL, `enfermedad_cronica` varchar(45) NOT NULL, `discapacidad_fisica` varchar(45) NOT NULL, `seguro_escolar_particular` varchar(45) NOT NULL, `evaluacion_profesional` bool NOT NULL, `colegio_procedencia` varchar(45) NOT NULL, `razon_cambio_colegio` varchar(45) NOT NULL, `medio_llego_colegio` varchar(45) NOT NULL, `pie` bool NOT NULL, `id_estado_alumno` integer NOT NULL);
--
-- Create model EstadoMensaje
--
CREATE TABLE `core_estadomensaje` (`id_estado_mensaje` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `estado_leido` bool NOT NULL, `fecha_leido` datetime(6) NULL, `destinatario_id` bigint NOT NULL);
--
-- Create model Funcionario
--
CREATE TABLE `core_funcionario` (`id_funcionario` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `id_cargo_funcionario` integer NOT NULL);
--
-- Create model Curso
--
CREATE TABLE `core_curso` (`id_curso` varchar(100) NOT NULL PRIMARY KEY, `anio_curso` integer NOT NULL, `matriculas_disponibles` integer NOT NULL, `id_estado_curso` integer NOT NULL, `id_profesor_jefe` integer NOT NULL, `id_jornada` integer NOT NULL, `id_lista_curso` integer NOT NULL, `id_tipo_curso` integer NOT NULL);
--
-- Create model Asignatura
--
CREATE TABLE `core_asignatura` (`id_asignatura` varchar(100) NOT NULL PRIMARY KEY, `id_curso` varchar(100) NOT NULL, `id_funcionario` integer NOT NULL, `id_lista_asignatura` integer NOT NULL);
--
-- Create model FuncionarioEspecializacion
--
CREATE TABLE `core_funcionarioespecializacion` (`id_funcionario_especializacion` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `id_funcionario` integer NOT NULL);
--
-- Create model HistoriaMensaje
--
CREATE TABLE `core_historiamensaje` (`id_historia_mensaje` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `estado_mensaje_padre_id` integer NOT NULL, `estado_mensaje_respuesta_id` integer NOT NULL);
--
-- Create model Matricula
--
CREATE TABLE `core_matricula` (`id_matricula` varchar(100) NOT NULL PRIMARY KEY, `ultimo_curso_aprobado` varchar(40) NOT NULL, `fecha_matricula` date NOT NULL, `id_alumno` integer NOT NULL, `id_curso` varchar(100) NOT NULL, `id_estado_matricula` integer NOT NULL);
--
-- Create model Mensaje
--
CREATE TABLE `core_mensaje` (`id_mensaje` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `fecha_envio` datetime(6) NOT NULL, `asunto` varchar(255) NOT NULL, `cuerpo` longtext NOT NULL, `permitir_respuestas` bool NOT NULL, `enviar_por_mail` bool NOT NULL, `remitente_id` bigint NOT NULL);
--
-- Add field mensaje to estadomensaje
--
ALTER TABLE `core_estadomensaje` ADD COLUMN `mensaje_id` integer NOT NULL , ADD CONSTRAINT `core_estadomensaje_mensaje_id_3607e1ec_fk_core_mens` FOREIGN KEY (`mensaje_id`) REFERENCES `core_mensaje`(`id_mensaje`);
--
-- Create model Apoderado
--
CREATE TABLE `core_apoderado` (`id_apoderado` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `id_nivel_academico` integer NOT NULL);
--
-- Create model Notas
--
CREATE TABLE `core_notas` (`id_notas` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `nota` double precision NOT NULL, `id_lista_asignatura` integer NOT NULL, `id_matricula` varchar(100) NOT NULL);
--
-- Create model GrupoFamiliar
--
CREATE TABLE `core_grupofamiliar` (`id_grupo_familiar` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `es_responsable` bool NOT NULL, `id_alumno` integer NOT NULL, `id_apoderado` integer NOT NULL, `id_parentesco` integer NOT NULL);
--
-- Create model Persona
--
CREATE TABLE `core_persona` (`id_persona` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `rut` bigint NOT NULL, `p_nombre` varchar(40) NOT NULL, `s_nombre` varchar(40) NOT NULL, `ap_paterno` varchar(40) NOT NULL, `ap_materno` varchar(40) NOT NULL, `email` varchar(45) NOT NULL, `id_genero` integer NOT NULL, `id_nacionalidad` integer NOT NULL);
--
-- Add field persona to funcionario
--
ALTER TABLE `core_funcionario` ADD COLUMN `id_persona` integer NOT NULL , ADD CONSTRAINT `core_funcionario_id_persona_2f467af3_fk_core_persona_id_persona` FOREIGN KEY (`id_persona`) REFERENCES `core_persona`(`id_persona`);
--
-- Create model Direccion
--
CREATE TABLE `core_direccion` (`id_direccion` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre_calle` varchar(45) NOT NULL, `numero` integer NOT NULL, `departamento` varchar(45) NOT NULL, `id_comuna` integer NOT NULL, `id_persona` integer NOT NULL);
--
-- Add field persona to apoderado
--
ALTER TABLE `core_apoderado` ADD COLUMN `id_persona` integer NOT NULL , ADD CONSTRAINT `core_apoderado_id_persona_35646d39_fk_core_persona_id_persona` FOREIGN KEY (`id_persona`) REFERENCES `core_persona`(`id_persona`);
--
-- Add field persona to alumno
--
ALTER TABLE `core_alumno` ADD COLUMN `id_persona` integer NOT NULL , ADD CONSTRAINT `core_alumno_id_persona_31d03f7f_fk_core_persona_id_persona` FOREIGN KEY (`id_persona`) REFERENCES `core_persona`(`id_persona`);
--
-- Add field persona to usuario
--
ALTER TABLE `core_usuario` ADD COLUMN `id_persona` integer NOT NULL , ADD CONSTRAINT `core_usuario_id_persona_86c8024f_fk_core_persona_id_persona` FOREIGN KEY (`id_persona`) REFERENCES `core_persona`(`id_persona`);
--
-- Add field region to comuna
--
ALTER TABLE `core_comuna` ADD COLUMN `id_region` integer NOT NULL , ADD CONSTRAINT `core_comuna_id_region_bd492382_fk_core_region_id_region` FOREIGN KEY (`id_region`) REFERENCES `core_region`(`id_region`);
--
-- Create model Reunion
--
CREATE TABLE `core_reunion` (`id_reunion` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `titulo` varchar(100) NOT NULL, `cuerpo` longtext NOT NULL, `fecha` datetime(6) NOT NULL, `id_destinatario` integer NOT NULL, `id_estado_reunion` integer NOT NULL, `id_remitente` integer NOT NULL);
--
-- Create model Tarea
--
CREATE TABLE `core_tarea` (`id_tarea` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `titulo` varchar(100) NOT NULL, `descripcion` longtext NOT NULL, `fecha_fin` datetime(6) NOT NULL, `id_asignatura` varchar(100) NOT NULL, `curso_id` varchar(100) NOT NULL, `profesor` integer NOT NULL, `id_tipo_tarea` integer NOT NULL);
CREATE TABLE `core_tarea_archivos` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `tarea_id` integer NOT NULL, `archivo_id` bigint NOT NULL);
--
-- Create model EntregaTarea
--
CREATE TABLE `core_entregatarea` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `comentario` longtext NOT NULL, `fecha_entrega` datetime(6) NOT NULL, `alumno_id` integer NOT NULL, `tarea_id` integer NOT NULL);
CREATE TABLE `core_entregatarea_archivos` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `entregatarea_id` bigint NOT NULL, `archivoentrega_id` bigint NOT NULL);
--
-- Create model Anotacion
--
CREATE TABLE `core_anotacion` (`id_anotacion` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `descripcion_anotacion` longtext NOT NULL, `fecha_anotacion` date NOT NULL, `id_lista_asignatura` integer NOT NULL, `id_matricula` varchar(100) NOT NULL, `id_tipo_anotacion` integer NOT NULL);
--
-- Create model Asistencia
--
CREATE TABLE `core_asistencia` (`id_asistencia` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `fecha_asistencia` date NOT NULL, `id_alumno` integer NOT NULL, `id_curso` varchar(100) NOT NULL, `id_tipo_asistencia` integer NOT NULL);
--
-- Create model Especializacion
--
CREATE TABLE `core_especializacion` (`id_especializacion` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `nombre_especializacion` varchar(45) NOT NULL, `id_tipo_especializacion` integer NOT NULL);
--
-- Create model Mensualidad
--
CREATE TABLE `core_mensualidad` (`id_mensualidad` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `monto_total` integer NOT NULL, `fecha_vencimiento` date NOT NULL, `id_estado_mensualidad` integer NOT NULL, `id_matricula` varchar(100) NOT NULL, `id_tipo_mensualidad` integer NOT NULL);
--
-- Create model Noticia
--
CREATE TABLE `core_noticia` (`id_noticia` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `titulo_noticia` varchar(45) NOT NULL, `subtitulo_noticia` varchar(45) NOT NULL, `cuerpo_noticia` varchar(45) NOT NULL, `fecha_noticia` date NOT NULL, `imagen_noticia` varchar(100) NOT NULL, `id_funcionario` integer NOT NULL, `id_prioridad_noticia` integer NOT NULL, `id_tipo_noticia` integer NOT NULL);
--
-- Add field tipo_usuario to usuario
--
ALTER TABLE `core_usuario` ADD COLUMN `id_tipo_usuario` integer NOT NULL , ADD CONSTRAINT `core_usuario_id_tipo_usuario_3e2b0402_fk_core_tipo` FOREIGN KEY (`id_tipo_usuario`) REFERENCES `core_tipousuario`(`id_tipo_usuario`);
--
-- Create model Horario
--
CREATE TABLE `core_horario` (`id_horario` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `id_asignatura` varchar(100) NOT NULL, `id_bloque` integer NOT NULL, `id_curso` varchar(100) NOT NULL, `id_dia` integer NOT NULL, `id_funcionario` integer NOT NULL);
ALTER TABLE `core_usuario_groups` ADD CONSTRAINT `core_usuario_groups_usuario_id_group_id_bde3c750_uniq` UNIQUE (`usuario_id`, `group_id`);
ALTER TABLE `core_usuario_groups` ADD CONSTRAINT `core_usuario_groups_usuario_id_97385234_fk_core_usuario_id` FOREIGN KEY (`usuario_id`) REFERENCES `core_usuario` (`id`);
ALTER TABLE `core_usuario_groups` ADD CONSTRAINT `core_usuario_groups_group_id_55312a9a_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);
ALTER TABLE `core_usuario_user_permissions` ADD CONSTRAINT `core_usuario_user_permis_usuario_id_permission_id_7a048d24_uniq` UNIQUE (`usuario_id`, `permission_id`);
ALTER TABLE `core_usuario_user_permissions` ADD CONSTRAINT `core_usuario_user_pe_usuario_id_ce4108a7_fk_core_usua` FOREIGN KEY (`usuario_id`) REFERENCES `core_usuario` (`id`);
ALTER TABLE `core_usuario_user_permissions` ADD CONSTRAINT `core_usuario_user_pe_permission_id_7f881653_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);
ALTER TABLE `core_alumno` ADD CONSTRAINT `core_alumno_id_estado_alumno_d44c3806_fk_core_esta` FOREIGN KEY (`id_estado_alumno`) REFERENCES `core_estadoalumno` (`id_estado_alumno`);
ALTER TABLE `core_estadomensaje` ADD CONSTRAINT `core_estadomensaje_destinatario_id_347f5598_fk_core_usuario_id` FOREIGN KEY (`destinatario_id`) REFERENCES `core_usuario` (`id`);
ALTER TABLE `core_funcionario` ADD CONSTRAINT `core_funcionario_id_cargo_funcionario_c1716aa7_fk_core_carg` FOREIGN KEY (`id_cargo_funcionario`) REFERENCES `core_cargofuncionario` (`id_cargo_funcionario`);
ALTER TABLE `core_curso` ADD CONSTRAINT `core_curso_id_estado_curso_fa3e73aa_fk_core_esta` FOREIGN KEY (`id_estado_curso`) REFERENCES `core_estadocurso` (`id_estado_curso`);
ALTER TABLE `core_curso` ADD CONSTRAINT `core_curso_id_profesor_jefe_82573745_fk_core_func` FOREIGN KEY (`id_profesor_jefe`) REFERENCES `core_funcionario` (`id_funcionario`);
ALTER TABLE `core_curso` ADD CONSTRAINT `core_curso_id_jornada_912dd8fa_fk_core_jornada_id_jornada` FOREIGN KEY (`id_jornada`) REFERENCES `core_jornada` (`id_jornada`);
ALTER TABLE `core_curso` ADD CONSTRAINT `core_curso_id_lista_curso_02d882fe_fk_core_list` FOREIGN KEY (`id_lista_curso`) REFERENCES `core_listacurso` (`id_lista_curso`);
ALTER TABLE `core_curso` ADD CONSTRAINT `core_curso_id_tipo_curso_cac87172_fk_core_tipo` FOREIGN KEY (`id_tipo_curso`) REFERENCES `core_tipocurso` (`id_letra_curso`);
ALTER TABLE `core_asignatura` ADD CONSTRAINT `core_asignatura_id_curso_da800561_fk_core_curso_id_curso` FOREIGN KEY (`id_curso`) REFERENCES `core_curso` (`id_curso`);
ALTER TABLE `core_asignatura` ADD CONSTRAINT `core_asignatura_id_funcionario_c9095058_fk_core_func` FOREIGN KEY (`id_funcionario`) REFERENCES `core_funcionario` (`id_funcionario`);
ALTER TABLE `core_asignatura` ADD CONSTRAINT `core_asignatura_id_lista_asignatura_70b090f7_fk_core_list` FOREIGN KEY (`id_lista_asignatura`) REFERENCES `core_listaasignatura` (`id_lista_asignatura`);
ALTER TABLE `core_funcionarioespecializacion` ADD CONSTRAINT `core_funcionarioespe_id_funcionario_ef29f5d8_fk_core_func` FOREIGN KEY (`id_funcionario`) REFERENCES `core_funcionario` (`id_funcionario`);
ALTER TABLE `core_historiamensaje` ADD CONSTRAINT `core_historiamensaje_estado_mensaje_padre_7d346aa7_fk_core_esta` FOREIGN KEY (`estado_mensaje_padre_id`) REFERENCES `core_estadomensaje` (`id_estado_mensaje`);
ALTER TABLE `core_historiamensaje` ADD CONSTRAINT `core_historiamensaje_estado_mensaje_respu_3bbb6050_fk_core_esta` FOREIGN KEY (`estado_mensaje_respuesta_id`) REFERENCES `core_estadomensaje` (`id_estado_mensaje`);
ALTER TABLE `core_matricula` ADD CONSTRAINT `core_matricula_id_alumno_87314bae_fk_core_alumno_id_alumno` FOREIGN KEY (`id_alumno`) REFERENCES `core_alumno` (`id_alumno`);
ALTER TABLE `core_matricula` ADD CONSTRAINT `core_matricula_id_curso_f3db9eda_fk_core_curso_id_curso` FOREIGN KEY (`id_curso`) REFERENCES `core_curso` (`id_curso`);
ALTER TABLE `core_matricula` ADD CONSTRAINT `core_matricula_id_estado_matricula_3f2492f7_fk_core_esta` FOREIGN KEY (`id_estado_matricula`) REFERENCES `core_estadomatricula` (`id_estado_matricula`);
ALTER TABLE `core_mensaje` ADD CONSTRAINT `core_mensaje_remitente_id_36255fa9_fk_core_usuario_id` FOREIGN KEY (`remitente_id`) REFERENCES `core_usuario` (`id`);
ALTER TABLE `core_apoderado` ADD CONSTRAINT `core_apoderado_id_nivel_academico_f54a791e_fk_core_nive` FOREIGN KEY (`id_nivel_academico`) REFERENCES `core_nivelacademico` (`id_nivel_academico`);
ALTER TABLE `core_notas` ADD CONSTRAINT `core_notas_id_lista_asignatura_65e1239f_fk_core_list` FOREIGN KEY (`id_lista_asignatura`) REFERENCES `core_listaasignatura` (`id_lista_asignatura`);
ALTER TABLE `core_notas` ADD CONSTRAINT `core_notas_id_matricula_bc73f51f_fk_core_matricula_id_matricula` FOREIGN KEY (`id_matricula`) REFERENCES `core_matricula` (`id_matricula`);
ALTER TABLE `core_grupofamiliar` ADD CONSTRAINT `core_grupofamiliar_id_alumno_a62d9492_fk_core_alumno_id_alumno` FOREIGN KEY (`id_alumno`) REFERENCES `core_alumno` (`id_alumno`);
ALTER TABLE `core_grupofamiliar` ADD CONSTRAINT `core_grupofamiliar_id_apoderado_b0572db0_fk_core_apod` FOREIGN KEY (`id_apoderado`) REFERENCES `core_apoderado` (`id_apoderado`);
ALTER TABLE `core_grupofamiliar` ADD CONSTRAINT `core_grupofamiliar_id_parentesco_65f8bb02_fk_core_pare` FOREIGN KEY (`id_parentesco`) REFERENCES `core_parentesco` (`id_parentesco`);
ALTER TABLE `core_persona` ADD CONSTRAINT `core_persona_id_genero_054d8211_fk_core_genero_id_genero` FOREIGN KEY (`id_genero`) REFERENCES `core_genero` (`id_genero`);
ALTER TABLE `core_persona` ADD CONSTRAINT `core_persona_id_nacionalidad_3f316ee7_fk_core_naci` FOREIGN KEY (`id_nacionalidad`) REFERENCES `core_nacionalidad` (`id_nacionalidad`);
ALTER TABLE `core_direccion` ADD CONSTRAINT `core_direccion_id_comuna_5e6d09ff_fk_core_comuna_id_comuna` FOREIGN KEY (`id_comuna`) REFERENCES `core_comuna` (`id_comuna`);
ALTER TABLE `core_direccion` ADD CONSTRAINT `core_direccion_id_persona_7531d604_fk_core_persona_id_persona` FOREIGN KEY (`id_persona`) REFERENCES `core_persona` (`id_persona`);
ALTER TABLE `core_reunion` ADD CONSTRAINT `core_reunion_id_destinatario_50992d19_fk_core_persona_id_persona` FOREIGN KEY (`id_destinatario`) REFERENCES `core_persona` (`id_persona`);
ALTER TABLE `core_reunion` ADD CONSTRAINT `core_reunion_id_estado_reunion_1687c724_fk_core_esta` FOREIGN KEY (`id_estado_reunion`) REFERENCES `core_estadoreunion` (`id_estado_reunion`);
ALTER TABLE `core_reunion` ADD CONSTRAINT `core_reunion_id_remitente_40d4dacc_fk_core_persona_id_persona` FOREIGN KEY (`id_remitente`) REFERENCES `core_persona` (`id_persona`);
ALTER TABLE `core_tarea` ADD CONSTRAINT `core_tarea_id_asignatura_9e39a4da_fk_core_asig` FOREIGN KEY (`id_asignatura`) REFERENCES `core_asignatura` (`id_asignatura`);
ALTER TABLE `core_tarea` ADD CONSTRAINT `core_tarea_curso_id_3cb5fe98_fk_core_curso_id_curso` FOREIGN KEY (`curso_id`) REFERENCES `core_curso` (`id_curso`);
ALTER TABLE `core_tarea` ADD CONSTRAINT `core_tarea_profesor_136dd745_fk_core_funcionario_id_funcionario` FOREIGN KEY (`profesor`) REFERENCES `core_funcionario` (`id_funcionario`);
ALTER TABLE `core_tarea` ADD CONSTRAINT `core_tarea_id_tipo_tarea_2f9d1bd8_fk_core_tipo` FOREIGN KEY (`id_tipo_tarea`) REFERENCES `core_tipotarea` (`id_tipo_tarea`);
ALTER TABLE `core_tarea_archivos` ADD CONSTRAINT `core_tarea_archivos_tarea_id_archivo_id_7d5ff57f_uniq` UNIQUE (`tarea_id`, `archivo_id`);
ALTER TABLE `core_tarea_archivos` ADD CONSTRAINT `core_tarea_archivos_tarea_id_c5eab0fd_fk_core_tarea_id_tarea` FOREIGN KEY (`tarea_id`) REFERENCES `core_tarea` (`id_tarea`);
ALTER TABLE `core_tarea_archivos` ADD CONSTRAINT `core_tarea_archivos_archivo_id_d511f4c4_fk_core_archivo_id` FOREIGN KEY (`archivo_id`) REFERENCES `core_archivo` (`id`);
ALTER TABLE `core_entregatarea` ADD CONSTRAINT `core_entregatarea_alumno_id_6416fab8_fk_core_alumno_id_alumno` FOREIGN KEY (`alumno_id`) REFERENCES `core_alumno` (`id_alumno`);
ALTER TABLE `core_entregatarea` ADD CONSTRAINT `core_entregatarea_tarea_id_53b1dddd_fk_core_tarea_id_tarea` FOREIGN KEY (`tarea_id`) REFERENCES `core_tarea` (`id_tarea`);
ALTER TABLE `core_entregatarea_archivos` ADD CONSTRAINT `core_entregatarea_archiv_entregatarea_id_archivoe_c5309b7c_uniq` UNIQUE (`entregatarea_id`, `archivoentrega_id`);
ALTER TABLE `core_entregatarea_archivos` ADD CONSTRAINT `core_entregatarea_ar_entregatarea_id_cdf49a6f_fk_core_entr` FOREIGN KEY (`entregatarea_id`) REFERENCES `core_entregatarea` (`id`);
ALTER TABLE `core_entregatarea_archivos` ADD CONSTRAINT `core_entregatarea_ar_archivoentrega_id_e2c16ee4_fk_core_arch` FOREIGN KEY (`archivoentrega_id`) REFERENCES `core_archivoentrega` (`id`);
ALTER TABLE `core_anotacion` ADD CONSTRAINT `core_anotacion_id_lista_asignatura_8b360fad_fk_core_list` FOREIGN KEY (`id_lista_asignatura`) REFERENCES `core_listaasignatura` (`id_lista_asignatura`);
ALTER TABLE `core_anotacion` ADD CONSTRAINT `core_anotacion_id_matricula_678bf122_fk_core_matr` FOREIGN KEY (`id_matricula`) REFERENCES `core_matricula` (`id_matricula`);
ALTER TABLE `core_anotacion` ADD CONSTRAINT `core_anotacion_id_tipo_anotacion_078278a1_fk_core_tipo` FOREIGN KEY (`id_tipo_anotacion`) REFERENCES `core_tipoanotacion` (`id_tipo_anotacion`);
ALTER TABLE `core_asistencia` ADD CONSTRAINT `core_asistencia_id_alumno_5800c28c_fk_core_alumno_id_alumno` FOREIGN KEY (`id_alumno`) REFERENCES `core_alumno` (`id_alumno`);
ALTER TABLE `core_asistencia` ADD CONSTRAINT `core_asistencia_id_curso_39e44b86_fk_core_curso_id_curso` FOREIGN KEY (`id_curso`) REFERENCES `core_curso` (`id_curso`);
ALTER TABLE `core_asistencia` ADD CONSTRAINT `core_asistencia_id_tipo_asistencia_223684c1_fk_core_tipo` FOREIGN KEY (`id_tipo_asistencia`) REFERENCES `core_tipoasistencia` (`id_tipo_asistencia`);
ALTER TABLE `core_especializacion` ADD CONSTRAINT `core_especializacion_id_tipo_especializac_bd13f4a4_fk_core_tipo` FOREIGN KEY (`id_tipo_especializacion`) REFERENCES `core_tipoespecializacion` (`id_tipo_especializacion`);
ALTER TABLE `core_mensualidad` ADD CONSTRAINT `core_mensualidad_id_estado_mensualida_15c16f63_fk_core_esta` FOREIGN KEY (`id_estado_mensualidad`) REFERENCES `core_estadomensualidad` (`id_estado_mensualidad`);
ALTER TABLE `core_mensualidad` ADD CONSTRAINT `core_mensualidad_id_matricula_9c900f45_fk_core_matr` FOREIGN KEY (`id_matricula`) REFERENCES `core_matricula` (`id_matricula`);
ALTER TABLE `core_mensualidad` ADD CONSTRAINT `core_mensualidad_id_tipo_mensualidad_a8d03926_fk_core_tipo` FOREIGN KEY (`id_tipo_mensualidad`) REFERENCES `core_tipomensualidad` (`id_tipo_mensualidad`);
ALTER TABLE `core_noticia` ADD CONSTRAINT `core_noticia_id_funcionario_b8913b0b_fk_core_func` FOREIGN KEY (`id_funcionario`) REFERENCES `core_funcionario` (`id_funcionario`);
ALTER TABLE `core_noticia` ADD CONSTRAINT `core_noticia_id_prioridad_noticia_cfe78078_fk_core_prio` FOREIGN KEY (`id_prioridad_noticia`) REFERENCES `core_prioridadnoticia` (`id_prioridad_noticia`);
ALTER TABLE `core_noticia` ADD CONSTRAINT `core_noticia_id_tipo_noticia_b69d9bda_fk_core_tipo` FOREIGN KEY (`id_tipo_noticia`) REFERENCES `core_tiponoticia` (`id_tipo_noticia`);
ALTER TABLE `core_horario` ADD CONSTRAINT `core_horario_id_funcionario_id_dia_id_bloque_2568983c_uniq` UNIQUE (`id_funcionario`, `id_dia`, `id_bloque`);
ALTER TABLE `core_horario` ADD CONSTRAINT `core_horario_id_asignatura_5f0e9d37_fk_core_asig` FOREIGN KEY (`id_asignatura`) REFERENCES `core_asignatura` (`id_asignatura`);
ALTER TABLE `core_horario` ADD CONSTRAINT `core_horario_id_bloque_49c39cc6_fk_core_bloquehorario_id_bloque` FOREIGN KEY (`id_bloque`) REFERENCES `core_bloquehorario` (`id_bloque`);
ALTER TABLE `core_horario` ADD CONSTRAINT `core_horario_id_curso_e9792f8a_fk_core_curso_id_curso` FOREIGN KEY (`id_curso`) REFERENCES `core_curso` (`id_curso`);
ALTER TABLE `core_horario` ADD CONSTRAINT `core_horario_id_dia_02f910a8_fk_core_diasemana_id_dia` FOREIGN KEY (`id_dia`) REFERENCES `core_diasemana` (`id_dia`);
ALTER TABLE `core_horario` ADD CONSTRAINT `core_horario_id_funcionario_439c2856_fk_core_func` FOREIGN KEY (`id_funcionario`) REFERENCES `core_funcionario` (`id_funcionario`);
