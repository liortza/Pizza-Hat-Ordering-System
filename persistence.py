import sqlite3


# region DTO
class Hat:
    def __init__(self, id, topping, supplier, quantity):
        self.id = id
        self.topping = topping
        self.supplier = supplier
        self.quantity = quantity


class Supplier:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Order:
    def __init__(self, id, location, hat):
        self.id = id
        self.location = location
        self.hat = hat


# endregion


# region DAO
class _Hats:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, hat):
        self._conn.execute("INSERT INTO hats (id, topping, supplier, quantity) VALUES (?, ?, ?, ?)",
                           [hat.id, hat.topping, hat.supplier, hat.quantity])

    def order_next(self, topping):
        cursor = self._conn.cursor()
        cursor.execute("SELECT id, topping, supplier, quantity FROM hats WHERE topping = ? ORDER BY supplier ASC",
                       [topping])
        hat = Hat(*cursor.fetchone())
        if hat.quantity > 1:
            self._conn.execute("UPDATE hats SET quantity = ? WHERE id = ?", [hat.quantity - 1, hat.id])
        else:
            self._conn.execute("DELETE FROM hats WHERE id = ?", [hat.id])
        return hat


class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("INSERT INTO suppliers (id, name) VALUES (?, ?)", [supplier.id, supplier.name])

    def find(self, supplier_id):
        c = self._conn.cursor()
        c.execute("SELECT id, name FROM suppliers WHERE id = ?", [supplier_id])
        return Supplier(*c.fetchone())


class _Orders:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, order):
        self._conn.execute("INSERT INTO orders (id, location, hat) VALUES (?, ?, ?)",
                           [order.id, order.location, order.hat])

# endregion


# region REPOSITORY
class _Repository:
    def __init__(self, db):
        self._conn = sqlite3.connect(db)
        self.hats = _Hats(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.orders = _Orders(self._conn)

    def close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
        CREATE TABLE suppliers (
            id          INT     PRIMARY KEY,
            name        STRING  NOT NULL       
        );

        CREATE TABLE hats (
            id          INT     PRIMARY KEY,
            topping     STRING  NOT NULL,
            supplier    INT     NOT NULL,
            quantity    INT     NOT NULL,
            FOREIGN KEY(supplier)   REFERENCES suppliers(id)
        );

        CREATE TABLE orders (
            id          INT     PRIMARY KEY,
            location    STRING  NOT NULL,
            hat         INT     NOT NULL,
            FOREIGN KEY(hat)        REFERENCES hats(id)
        );
        """)
# endregion
