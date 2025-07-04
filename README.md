# 🏗️ Steel Merchant Inventory System

A **Flask-based web application** for managing steel inventory, parsing voice transcripts into orders, and generating professional PDF invoices.

---

## ✨ Features

* 🎙️ **Auto-Generated Cart**
  Parse voice transcripts to automatically generate shopping carts.

* 📦 **Inventory Management**
  Add, remove, and update items in the cart with quantity adjustments.

* 🧾 **PDF Invoice Generation**
  Generate professionally designed invoices with branding and item details.

* 🧮 **Real-Time Price Calculation**
  Subtotals and totals are auto-calculated when quantities or prices change.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/steel-inventory-system.git
cd steel-inventory-system
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python app.py
```

### 4. Open in Browser

Visit [http://localhost:5000](http://localhost:5000) to access the application.

---

## 🧠 How to Use

### 🔊 Generate a Cart from Voice Transcript

1. Go to the home page (`/`).
2. Paste your voice transcript in the text area.
3. Enter your delivery pincode.
4. Click **"Generate Cart"** to populate the shopping cart.

### ✍️ Manage Cart Items

* **Add Items**: Use the form to add custom products manually.
* **Update Quantity**: Use `+` or `–` buttons beside each item.
* **Remove Items**: Click the 🗑️ **Remove** button to delete items.

### 📄 Generate Invoice (PDF)

1. Make sure your cart is filled with valid items and quantities.
2. Click **"Generate Invoice PDF"**.
3. A professional invoice will be downloaded automatically.

---

## 🧾 PDF Invoice Features

The generated PDF invoice includes:

* ✅ Clean, professional layout
* 🏢 Company branding with logo/header
* 📅 Invoice details: date, number, customer info
* 📝 Itemized product list: name, spec, quantity, price, subtotal
* 💰 Grand total calculation
* 📌 Terms and conditions section

---

## 📂 Project Structure

```
steel-inventory-system/
├── app.py                 # Main Flask app
├── requirements.txt       # Python dependencies
├── README.md              # Documentation
├── static/
│   └── css/
│       └── style.css      # App styling
├── templates/
│   ├── base.html          # Base layout
│   ├── index.html         # Transcript input
│   └── cart.html          # Cart & Invoice page
└── utils/
    ├── db.py              # Simple DB/data storage
    ├── estimator.py       # Price & delivery logic
    └── parser.py          # Voice transcript parser
```

---

## 🧰 Dependencies

| Library     | Purpose                  |
| ----------- | ------------------------ |
| Flask       | Web framework            |
| reportlab   | PDF invoice generation   |
| Python 3.7+ | Minimum required version |

Install `reportlab` manually if needed:

```bash
pip install reportlab
```

---

## 🌐 Browser Compatibility

Compatible with all modern browsers:

* ✅ JavaScript ES6 support
* ✅ CSS Grid & Flexbox
* ✅ Fetch API for dynamic updates
* ✅ Blob API for downloading PDF files

---

## 🛠️ Troubleshooting

### PDF Not Downloading?

* Make sure cart is not empty.
* Ensure all items have valid prices.
* Check internet connection or browser settings.

### Installation Issues?

* Use Python 3.7 or higher.
* Prefer using a virtual environment:

  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  pip install -r requirements.txt
  ```

---

## 📄 License

This project is provided for **educational and business use**. For commercial deployment, consider license compliance and legal review.

