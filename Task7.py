
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# Step 1: Create a sample SQLite database and insert sample sales data
conn = sqlite3.connect("sales_data.db")
cursor = conn.cursor()

# Create the sales table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT,
    quantity INTEGER,
    price REAL
)
""")

# Insert sample data
sample_data = [
    ('Apple', 10, 1.5),
    ('Banana', 20, 0.5),
    ('Orange', 15, 1.0),
    ('Apple', 5, 1.5),
    ('Banana', 10, 0.5),
    ('Orange', 10, 1.0)
]
cursor.executemany("INSERT INTO sales (product, quantity, price) VALUES (?, ?, ?)", sample_data)
conn.commit()

# Step 2: Run SQL query and load into pandas DataFrame
query = """
SELECT product, SUM(quantity) AS total_qty, SUM(quantity * price) AS revenue
FROM sales
GROUP BY product
"""
df = pd.read_sql_query(query, conn)

# Step 3: Print results and plot bar chart
print(df)
plt.figure(figsize=(6, 4))
df.plot(kind='bar', x='product', y='revenue', legend=False)
plt.title("Revenue by Product")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig("sales_chart.png")
plt.close()

# Step 4: Generate PDF report
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Sales Summary Report", ln=True, align='C')

# Add table data
pdf.ln(10)
for index, row in df.iterrows():
    line = f"Product: {row['product']}, Total Quantity: {row['total_qty']}, Revenue: ${row['revenue']:.2f}"
    pdf.cell(200, 10, txt=line, ln=True)

# Add chart image
pdf.image("sales_chart.png", x=30, y=None, w=150)

# Save the PDF
pdf.output("sales_summary_report.pdf")

conn.close()
