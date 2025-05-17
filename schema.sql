CREATE DATABASE secure_app;

USE secure_app;

-- Creamos la tabla con TODOS los campos
-- Elimina la tabla `users` si ya existe
DROP TABLE IF EXISTS users;

USE secure_app;


CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,          -- Nombre de usuario único
  password_hash TEXT NOT NULL,                   -- Contraseña cifrada
  email_encrypted TEXT NOT NULL,                 -- Email cifrado
  name TEXT NOT NULL,                            -- Nombre del usuario
  address TEXT NOT NULL,                         -- Dirección
  phone TEXT NOT NULL,                           -- Teléfono
  rfc_encrypted TEXT NOT NULL,                   -- RFC cifrado
  birth_date DATE NOT NULL,                      -- Fecha de nacimiento
  gender ENUM('Male', 'Female', 'Other') NOT NULL, -- Género
  role ENUM('admin', 'client') NOT NULL DEFAULT 'client' -- Rol del usuario
);

INSERT INTO users 
  (username, password_hash, email_encrypted, name, address, phone, rfc_encrypted, birth_date, gender, role)
VALUES
  ('Liav', 
   'pbkdf2:sha256:600000$admin050430$e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', -- Contraseña: admin050430
   'liav@example.com', 
   'Liav Administrador', 
   'Av. Principal 123, Ciudad', 
   '+52 55 1234 5678', 
   'LIAV050430XYZ', 
   '2005-04-30', 
   'Male', 
   'admin');

-- Inserta 10 usuarios con datos reales (ficticios pero plausibles)
INSERT INTO users 
  (username, password_hash, email_encrypted, name, address, phone, rfc_encrypted, birth_date, gender, role)
VALUES
  ('juan_perez99',    'pbkdf2:sha256:600000$abc123', 'juan.perez99@gmail.com',    'Juan Pérez',      'Av. Reforma 123, CDMX',      '+52 55 1234 5678', 'LWPJ950722ABC', '1995-07-22', 'Male',   'client'),
  ('ana_lopez88',     'pbkdf2:sha256:600000$def456', 'ana.lopez88@gmail.com',     'Ana López',       'Calle Juárez 45, Monterrey', '+52 81 5678 9012', 'LOPA880315XYZ', '1988-03-15', 'Female', 'client'),
  ('carlos_mendoza77','pbkdf2:sha256:600000$ghi789', 'carlos.mendoza77@yahoo.com','Carlos Mendoza',  'Blvd. Independencia 200, Torreón', '+52 871 223 4455', 'MOC770908QWE', '1977-09-08', 'Male', 'client'),
  ('maria_garcia21',  'pbkdf2:sha256:600000$jkl012', 'maria.garcia21@outlook.com','María García',    'Col. Centro, Guadalajara',  '+52 33 9988 7766', 'GAM010130RTY', '2001-01-30', 'Female', 'client'),
  ('alex_fernandez03','pbkdf2:sha256:600000$mno345', 'alex.fernandez03@protonmail.com','Alex Fernández','Zona Dorada, Cancún',       '+52 998 3344 5566', 'FEL031211UIO', '2003-12-11', 'Other', 'client'),
  ('roberto_gonzalez85','pbkdf2:sha256:600000$pqr678','roberto.gonzalez85@mail.com','Roberto González','Av. Insurgentes Sur 456, CDMX', '+52 55 6789 0123', 'GZR850510PAS', '1985-05-10', 'Male', 'client'),
  ('sofia_ramirez92', 'pbkdf2:sha256:600000$stu901', 'sofia.ramirez92@hotmail.com','Sofía Ramírez',  'Col. Del Valle, Monterrey', '+52 81 3344 5566', 'RZS920925BVC', '1992-09-25', 'Female', 'client'),
  ('diego_torres78',  'pbkdf2:sha256:600000$vwx234', 'diego.torres78@empresa.com','Diego Torres',    'Calle Hidalgo 78, Puebla',  '+52 222 9876 5432', 'TRD780217NMK', '1978-02-17', 'Male', 'client'),
  ('laura_martinez99','pbkdf2:sha256:600000$yz1234', 'laura.martinez99@dominio.mx','Laura Martínez', 'Zona Centro, Querétaro',    '+52 442 1122 3344', 'MZL990630HGT', '1999-06-30', 'Female', 'client'),
  ('fernando_ruiz04', 'pbkdf2:sha256:600000$xyz567', 'fernando.ruiz04@correo.com','Fernando Ruiz',   'Col. Americana, Guadalajara', '+52 33 4455 6677', 'RUF041121ZXC', '2004-11-21', 'Other', 'client');

select * from users;

