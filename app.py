import tkinter as tk
from tkinter import ttk
import tkinter.simpledialog as simpledialog
from tkinter import messagebox
import mysql.connector
from getpass import getpass


class StockManagementApp:
    def __init__(self, root, user, password, database):
        self.root = root
        self.root.title("Gestion de Stock")
        self.user = user
        self.password = password
        self.database = database
        self.connection = self.connect_to_database()

        self.create_widgets()

    def connect_to_database(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user=self.user,
                password=self.password,
                database=self.database
            )
            return connection
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur MySQL", f"Erreur de connexion à la base de données : {err}")
            self.root.destroy()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.root, columns=('ID', 'Nom', 'Description', 'Prix', 'Quantité', 'Catégorie'))
        self.tree.heading('#0', text='ID')
        self.tree.heading('#1', text='Nom')
        self.tree.heading('#2', text='Description')
        self.tree.heading('#3', text='Prix')
        self.tree.heading('#4', text='Quantité')
        self.tree.heading('#5', text='Catégorie')

        self.tree.pack(expand=tk.YES, fill=tk.BOTH)

        add_button = tk.Button(self.root, text="Ajouter", command=self.add_product)
        add_button.pack(side=tk.LEFT, padx=5)

        remove_button = tk.Button(self.root, text="Supprimer", command=self.remove_product)
        remove_button.pack(side=tk.LEFT, padx=5)

        update_button = tk.Button(self.root, text="Modifier", command=self.update_product)
        update_button.pack(side=tk.LEFT, padx=5)

        refresh_button = tk.Button(self.root, text="Actualiser", command=self.refresh_data)
        refresh_button.pack(side=tk.LEFT, padx=5)

        self.load_data()

    def load_data(self):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM product INNER JOIN category ON product.id_category = category.id")
        products = cursor.fetchall()
        cursor.close()

        for product in products:
            # Utilisez product['id_category'] au lieu de product['name']
            self.tree.insert('', 'end', values=(
                product['id'],
                product['name'],
                product['description'],
                product['price'],
                product['quantity'],
                product['id_category']  # Utilisez l'ID de la catégorie au lieu du nom
            ))

    def add_product(self):
        name = tk.simpledialog.askstring("Ajouter Produit", "Nom:")
        description = tk.simpledialog.askstring("Ajouter Produit", "Description:")
        price = tk.simpledialog.askfloat("Ajouter Produit", "Prix:")
        quantity = tk.simpledialog.askinteger("Ajouter Produit", "Quantité:")
        category = tk.simpledialog.askstring("Ajouter Produit", "Catégorie:")

        # Validation des données
        try:
            int(quantity)
            float(price)
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez saisir des valeurs numériques pour la quantité et le prix.")
            return

        # Récupération de l'ID de la catégorie
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT id FROM category WHERE name = %s", (category,))
        category_id = cursor.fetchone()
        if not category_id:
            cursor.execute("INSERT INTO category (name) VALUES (%s)", (category,))
            self.connection.commit()
            category_id = cursor.lastrowid

        # Exécution de la requête SQL
        cursor.execute("""
            INSERT INTO product (name, description, price, quantity, id_category)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, description, price, quantity, category_id['id']))
        self.connection.commit()

        # Mise à jour de l'interface
        self.refresh_data()

    def remove_product(self):
        selected_item = self.tree.selection()
        if selected_item:
            product_id = self.tree.item(selected_item, "values")[0]
            confirmation = messagebox.askyesno("Supprimer Produit", f"Voulez-vous vraiment supprimer le produit {product_id}?")
            if confirmation:
                cursor = self.connection.cursor()
                cursor.execute("DELETE FROM product WHERE id = %s", (product_id,))
                self.connection.commit()
                self.refresh_data()

    def update_product(self):
        selected_item = self.tree.selection()
        if selected_item:
            product_id = self.tree.item(selected_item, "values")[0]
            new_quantity = tk.simpledialog.askinteger("Modifier Quantité", "Nouvelle Quantité:")
            new_price = tk.simpledialog.askfloat("Modifier Prix", "Nouveau Prix:")

            # Validation des données
            try:
                int(new_quantity)
                float(new_price)
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez saisir des valeurs numériques pour la quantité et le prix.")
                return

            # Exécution de la requête SQL
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE product
                SET quantity = %s, price = %s
                WHERE id = %s
            """, (new_quantity, new_price, product_id))
            self.connection.commit()

            # Mise à jour de l'interface
            self.refresh_data()

    def refresh_data(self):
        self.tree.delete(*self.tree.get_children())
        self.load_data()

if __name__ == "__main__":
    user_mysql = input("Nom d'utilisateur MySQL: ")
    password_mysql = getpass("Mot de passe MySQL: ")
    database_name = "store"

    root = tk.Tk()
    app = StockManagementApp(root, user_mysql, password_mysql, database_name)
    root.mainloop()
