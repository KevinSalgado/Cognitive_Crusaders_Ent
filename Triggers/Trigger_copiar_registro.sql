CREATE TRIGGER copiar_registro_trigger
AFTER INSERT ON auth_user
FOR EACH ROW
EXECUTE FUNCTION copiar_registro();