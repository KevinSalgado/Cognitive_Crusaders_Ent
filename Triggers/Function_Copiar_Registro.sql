CREATE FUNCTION copiar_registro() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.is_staff = true THEN
        
        INSERT INTO public."Cliente_Usuario_administrador" (id_usuario, username, correo, contrasena, "fk_Rol_id")
        VALUES (NEW.id, NEW.username, NEW.email, NEW.password, 1);
    END IF;

    RETURN NEW; 
END;
$$ LANGUAGE plpgsql;