from flask import Flask, request, redirect
import pyodbc

app = Flask(__name__)

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=ecomsqlserver.database.windows.net;"
    "DATABASE=free-sql-db-8938282;"
    "UID=CloudSA51bf9fc2;"
    "PWD=Password@12345;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
)

@app.route("/")
def home():
    cursor = conn.cursor()
    cursor.execute("SELECT ProductID, ProductName, Price, Quantity FROM Products")
    products = cursor.fetchall()

    rows = ""

    for p in products:
        rows += f"""
        <tr>
            <td>{p.ProductID}</td>
            <td>{p.ProductName}</td>
            <td>₹{p.Price}</td>
            <td>{p.Quantity}</td>
            <td>
                <a href="/delete/{p.ProductID}">
                    Delete
                </a>
            </td>
        </tr>
        """

    return f"""
    <html>

    <head>
        <title>MyEcomm Dashboard</title>

        <style>

        body {{
            font-family: Arial;
            background: #f4f6f9;
            padding: 30px;
        }}

        .container {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            max-width: 900px;
            margin: auto;
            box-shadow: 0 0 10px #ccc;
        }}

        h1 {{
            color: #0078d4;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}

        th, td {{
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }}

        th {{
            background: #0078d4;
            color: white;
        }}

        input {{
            padding: 10px;
            margin: 5px;
        }}

        button {{
            padding: 10px 15px;
            background: #0078d4;
            color: white;
            border: none;
            border-radius: 5px;
        }}

        a {{
            color: red;
            text-decoration: none;
        }}

        </style>

    </head>

    <body>

    <div class="container">

        <h1>MyEcomm Product Dashboard</h1>

        <form method="POST" action="/add">

            <input
                name="name"
                placeholder="Product Name"
                required
            >

            <input
                name="price"
                placeholder="Price"
                required
            >

            <input
                name="quantity"
                placeholder="Quantity"
                required
            >

            <button type="submit">
                Add Product
            </button>

        </form>

        <table>

            <tr>
                <th>ID</th>
                <th>Product</th>
                <th>Price</th>
                <th>Quantity</th>
                <th>Action</th>
            </tr>

            {rows}

        </table>

    </div>

    </body>

    </html>
    """

@app.route("/add", methods=["POST"])
def add():

    name = request.form["name"]
    price = request.form["price"]
    quantity = request.form["quantity"]

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO Products (ProductName, Price, Quantity) VALUES (?, ?, ?)",
        name,
        price,
        quantity
    )

    conn.commit()

    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM Products WHERE ProductID = ?",
        id
    )

    conn.commit()

    return redirect("/")

app.run(host="0.0.0.0", port=5000)