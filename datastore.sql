-- Création de la base de données
CREATE DATABASE IF NOT EXISTS store;

-- Utilisation de la base de données
USE store;

-- Création de la table "category"
CREATE TABLE IF NOT EXISTS category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Création de la table "product"
CREATE TABLE IF NOT EXISTS product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price INT,
    quantity INT,
    id_category INT,
    FOREIGN KEY (id_category) REFERENCES category(id)
);

-- Insertion de catégories
INSERT INTO category (name) VALUES
('Électronique'),
('Vêtements'),
('Alimentation');

-- Insertion de produits
INSERT INTO product (name, description, price, quantity, id_category) VALUES
('Téléviseur', 'Écran plat 4K', 800, 10, 1),
('Chemise', 'Chemise en coton', 30, 50, 2),
('Pommes', 'Pommes biologiques', 2, 100, 3);
