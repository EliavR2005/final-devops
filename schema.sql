-- BORRÓN y cuenta nueva
DROP DATABASE IF EXISTS secure_app;
CREATE DATABASE secure_app;
USE secure_app;

-- Creamos la tabla con TODOS los campos
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username        VARCHAR(50) NOT NULL UNIQUE,
  password_hash   TEXT         NOT NULL,
  email_encrypted TEXT         NOT NULL,
  name_encrypted  TEXT         NOT NULL,
  address         TEXT         NOT NULL,
  phone           TEXT         NOT NULL,
  rfc_encrypted   TEXT         NOT NULL,   -- nuevo campo para RFC
  birth_date      DATE         NOT NULL,
  gender          ENUM('Male','Female','Other') NOT NULL,
  role            ENUM('admin','client') NOT NULL DEFAULT 'client'
);
-- (Opcional) Pre‑sembrar tu admin Liav
INSERT INTO users 
  (username, password_hash, email_encrypted, name_encrypted, address, phone, rfc_encrypted, birth_date, gender, role)
SELECT 'Liav',
       'scrypt:32768:8:1$I77r0qJTHcB4wkMu$53dc9a394dc16d20765489740ff09293028d6fd3460577086189baaac5e74fb8682ec13e77e97a353c61dcb6f33fba21eb12abd98ff1f9518780f2daf9787302',  -- hash de ejemplo
       'gAAAAALiavMail',
       'gAAAAALiavName',
       'Av. Principal 1',
       '+52 1 2345 6789',
       'gAAAAARfcLiav',
       '1999-01-01',
       'Other',
       'admin'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE username='Liav');

INSERT INTO users 
  (username, password_hash, email_encrypted, name_encrypted, address, phone, rfc_encrypted, birth_date, gender, role)
VALUES
  ('juan_perez99',    'pbkdf2:sha256:600000$abc123', 'gAAAAABe1', 'gAAAAABn1', 'Av. Reforma 123, CDMX',         '+52 55 1234 5678', 'gAAAAARfc1', '1995-07-22', 'Male',   'client'),
  ('ana_lopez88',     'pbkdf2:sha256:600000$def456', 'gAAAAABe2', 'gAAAAABn2', 'Calle Juárez 45, Monterrey',    '+52 81 5678 9012', 'gAAAAARfc2', '1988-03-15', 'Female', 'client'),
  ('carlos_mendoza77','pbkdf2:sha256:600000$ghi789', 'gAAAAABe3', 'gAAAAABn3', 'Blvd. Independencia 200, Torreón', '+52 871 223 4455', 'gAAAAARfc3', '1977-09-08', 'Male',   'client'),
  ('maria_garcia21',  'pbkdf2:sha256:600000$jkl012', 'gAAAAABe4', 'gAAAAABn4', 'Col. Centro, Guadalajara',       '+52 33 9988 7766', 'gAAAAARfc4', '2001-01-30', 'Female', 'client'),
  ('alex_fernandez03','pbkdf2:sha256:600000$mno345', 'gAAAAABe5', 'gAAAAABn5', 'Zona Dorada, Cancún',            '+52 998 3344 5566','gAAAAARfc5', '2003-12-11', 'Other',  'client'),
  ('roberto_gonzalez85','pbkdf2:sha256:600000$pqr678','gAAAAABe6','gAAAAABn6','Av. Insurgentes Sur 456, CDMX',   '+52 55 6789 0123', 'gAAAAARfc6', '1985-05-10', 'Male',   'client'),
  ('sofia_ramirez92', 'pbkdf2:sha256:600000$stu901', 'gAAAAABe7', 'gAAAAABn7', 'Col. Del Valle, Monterrey',      '+52 81 3344 5566', 'gAAAAARfc7', '1992-09-25', 'Female', 'client'),
  ('diego_torres78',  'pbkdf2:sha256:600000$vwx234', 'gAAAAABe8', 'gAAAAABn8', 'Calle Hidalgo 78, Puebla',       '+52 222 9876 5432','gAAAAARfc8', '1978-02-17', 'Male',   'client'),
  ('laura_martinez99','pbkdf2:sha256:600000$yz1234', 'gAAAAABe9', 'gAAAAABn9', 'Zona Centro, Querétaro',         '+52 442 1122 3344','gAAAAARfc9', '1999-06-30', 'Female', 'client'),
  ('fernando_ruiz04', 'pbkdf2:sha256:600000$xyz567', 'gAAAAABe0', 'gAAAAABn0', 'Col. Americana, Guadalajara',    '+52 33 4455 6677', 'gAAAAARfc0', '2004-11-21', 'Other',  'client');

