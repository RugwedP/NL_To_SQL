"""
schema.py - Define your database tables here.
Any user can update this file to point to their own tables.
The rest of the system will automatically adapt.

Format:
  TABLES = {
    "table_name": {
      "description": "What this table stores",
      "columns": {
        "column_name": {"type": "data_type", "description": "what it means", "primary_key": True/False, "foreign_key": "table.column" or None}
      }
    }
  }
"""

TABLES = {
    "customers": {
        "description": "Stores information about registered customers",
        "columns": {
            "customer_id":  {"type": "INT",     "description": "Unique customer ID",           "primary_key": True,  "foreign_key": None},
            "name":         {"type": "VARCHAR",  "description": "Full name of the customer",    "primary_key": False, "foreign_key": None},
            "email":        {"type": "VARCHAR",  "description": "Customer email address",       "primary_key": False, "foreign_key": None},
            "country":      {"type": "VARCHAR",  "description": "Country of residence",         "primary_key": False, "foreign_key": None},
            "created_at":   {"type": "DATE",     "description": "Account creation date",        "primary_key": False, "foreign_key": None},
        }
    },

    "products": {
        "description": "Product catalog with pricing and category info",
        "columns": {
            "product_id":   {"type": "INT",      "description": "Unique product ID",            "primary_key": True,  "foreign_key": None},
            "product_name": {"type": "VARCHAR",  "description": "Name of the product",          "primary_key": False, "foreign_key": None},
            "category":     {"type": "VARCHAR",  "description": "Product category (Electronics/Clothing/Books etc.)", "primary_key": False, "foreign_key": None},
            "price":        {"type": "DECIMAL",  "description": "Current list price in USD",    "primary_key": False, "foreign_key": None},
            "stock":        {"type": "INT",      "description": "Units currently in stock",     "primary_key": False, "foreign_key": None},
        }
    },

    "orders": {
        "description": "Stores all customer purchase orders",
        "columns": {
            "order_id":     {"type": "INT",      "description": "Unique order ID",              "primary_key": True,  "foreign_key": None},
            "customer_id":  {"type": "INT",      "description": "References customers table",   "primary_key": False, "foreign_key": "customers.customer_id"},
            "order_date":   {"type": "DATE",     "description": "Date the order was placed",    "primary_key": False, "foreign_key": None},
            "status":       {"type": "VARCHAR",  "description": "Order status (pending/shipped/delivered/cancelled)", "primary_key": False, "foreign_key": None},
            "total_amount": {"type": "DECIMAL",  "description": "Total order value in USD",     "primary_key": False, "foreign_key": None},
        }
    },
    "order_items": {
        "description": "Individual line items within each order",
        "columns": {
            "item_id":      {"type": "INT",      "description": "Unique item ID",               "primary_key": True,  "foreign_key": None},
            "order_id":     {"type": "INT",      "description": "References orders table",      "primary_key": False, "foreign_key": "orders.order_id"},
            "product_id":   {"type": "INT",      "description": "References products table",    "primary_key": False, "foreign_key": "products.product_id"},
            "quantity":     {"type": "INT",      "description": "Number of units ordered",      "primary_key": False, "foreign_key": None},
            "unit_price":   {"type": "DECIMAL",  "description": "Price per unit at time of order", "primary_key": False, "foreign_key": None},
        }
    },
    
}

# Helper: flat set of valid table names
VALID_TABLES = set(TABLES.keys())

# Helper: valid columns per table
VALID_COLUMNS = {table: set(info["columns"].keys()) for table, info in TABLES.items()}