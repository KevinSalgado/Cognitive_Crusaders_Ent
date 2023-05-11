INSERT INTO public."Cliente_Usuario_usuario" (id_usuario, nombre, apellido, telefono, correo, contrasena, "fk_Rol_id") 
VALUES 
(1, 'Marcela', 'González', '555-6789', 'mgonzalez@example.com', 'password123', 3),
(2, 'Carlos', 'Martínez', '555-0123', 'cmartinez@example.com', 'password456', 3),
(3, 'Sofía', 'Sánchez', '555-4567', 'ssanchez@example.com', 'password789', 3);


INSERT INTO public."Cliente_Usuario_cliente" (usuario_ptr_id, "Observaciones") 
VALUES 
(1, 'Sabe de DataScience'),
(2, 'Ignorante de la informatica'),
(3, 'Apasionado de la tecno');

SELECT Usuario.nombre, Usuario.apellido, Administrador."Sueldo"
FROM public."Cliente_Usuario_administrador" AS Administrador
JOIN public."Cliente_Usuario_usuario" AS Usuario ON Administrador.usuario_ptr_id = Usuario.id_usuario;



delete from public."Cliente_Usuario_usuario"

select * from public."Cliente_Usuario_usuario"

SELECT trabajador."Sueldo" AS Sueldo, usuario.nombre as nombreAdmin, usuario2.nombre as nombreTrabajador 
FROM public."Cliente_Usuario_trabajador" as trabajador
join public."Cliente_Usuario_administrador" as administrador on trabajador."fk_Administrador_id" = administrador.usuario_ptr_id
join public."Cliente_Usuario_usuario" as usuario on administrador.usuario_ptr_id = usuario.id_usuario
join public."Cliente_Usuario_usuario" as usuario2 ON usuario2.id_usuario = trabajador.usuario_ptr_id
where usuario.id_usuario = trabajador."fk_Administrador_id"

select * from public."Cliente_Usuario_"









