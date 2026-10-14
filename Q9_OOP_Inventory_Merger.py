"""Q9: Inventory classes with operator overloading and JSON file persistence."""
import json
import sys

class Product:
    def __init__(self, product_id, name, stock, purchase_price, selling_price):
        if stock < 0 or purchase_price < 0 or selling_price < 0:
            raise ValueError("Stock and prices cannot be negative")
        self.product_id, self.name = str(product_id), str(name)
        self.stock, self.purchase_price, self.selling_price = int(stock), float(purchase_price), float(selling_price)

    def merge(self, other):
        if self.product_id != other.product_id: raise ValueError("Product IDs must match")
        if self.name != other.name: raise ValueError("Conflicting product names for same ID")
        return Product(self.product_id, self.name, self.stock + other.stock,
                       min(self.purchase_price, other.purchase_price),
                       max(self.selling_price, other.selling_price))

    @property
    def total_value(self):
        return self.stock * self.purchase_price

    def as_dict(self):
        return {"product_id": self.product_id, "name": self.name, "stock": self.stock,
                "purchase_price": self.purchase_price, "selling_price": self.selling_price}

class Inventory:
    def __init__(self, products=None):
        self.products = {p.product_id: p for p in (products or [])}

    @classmethod
    def load(cls, path):
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
        return cls([Product(**row) for row in data])

    def save(self, path):
        with open(path, "w", encoding="utf-8") as handle:
            json.dump([p.as_dict() for p in self.products.values()], handle, indent=2)

    def add(self, product):
        if product.product_id in self.products: raise ValueError("Product already exists")
        self.products[product.product_id] = product

    def delete(self, product_id):
        if product_id not in self.products: raise KeyError("Product not found")
        del self.products[product_id]

    def update_stock(self, product_id, stock):
        if stock < 0: raise ValueError("Stock cannot be negative")
        self.products[product_id].stock = stock

    @property
    def total_value(self):
        return sum(p.total_value for p in self.products.values())

    def __add__(self, other):
        merged = {key: Product(**p.as_dict()) for key, p in self.products.items()}
        for key, product in other.products.items():
            merged[key] = merged[key].merge(product) if key in merged else Product(**product.as_dict())
        return Inventory(list(merged.values()))

    def print_summary(self):
        for key in sorted(self.products):
            p = self.products[key]
            print(f"{p.product_id} {p.name} stock={p.stock} purchase={p.purchase_price:g} selling={p.selling_price:g}")
        print(f"TOTAL_VALUE {self.total_value:g}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python Q9_OOP_Inventory_Merger.py inventoryA.json inventoryB.json [output.json]")
        print("JSON format: [{\"product_id\":\"P1\",\"name\":\"Pen\",\"stock\":10,\"purchase_price\":5,\"selling_price\":8}]")
        return
    try:
        a, b = Inventory.load(sys.argv[1]), Inventory.load(sys.argv[2])
        merged = a + b
        merged.print_summary()
        if len(sys.argv) >= 4: merged.save(sys.argv[3])
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"Inventory error: {exc}", file=sys.stderr)

if __name__ == "__main__":
    main()
