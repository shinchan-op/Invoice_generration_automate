# Steel Merchant Inventory System

A Flask-based web application for managing steel inventory and generating invoices.

## Features

- **Auto-Generated Cart**: Parse voice transcripts to automatically generate shopping carts
- **Inventory Management**: Add, remove, and modify items in the cart
- **PDF Invoice Generation**: Generate professional PDF invoices for orders
- **Real-time Price Calculation**: Automatic subtotal calculations with quantity changes

## Installation

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python app.py
   ```

3. **Access the Application**:
   Open your browser and go to `http://localhost:5000`

## Usage

### Generating a Cart
1. Go to the home page
2. Enter your voice transcript in the text area
3. Enter your pincode for delivery estimation
4. Click "Generate Cart" to create an auto-generated shopping cart

### Managing Cart Items
- **Add Items**: Use the "Add New Item" form to manually add products
- **Modify Quantities**: Use the +/- buttons to adjust quantities
- **Remove Items**: Click the "Remove" button to delete items from cart

### Generating PDF Invoices
1. Ensure your cart has items
2. Click the "Generate Invoice PDF" button
3. The PDF will automatically download with:
   - Company information and branding
   - Invoice details (date, number, customer info)
   - Complete itemized list with prices
   - Total amount calculation
   - Terms and conditions

## PDF Invoice Features

The generated PDF includes:
- **Professional Layout**: Clean, business-ready design
- **Company Branding**: Steel Merchant Inventory System header
- **Invoice Details**: Date, invoice number, and customer information
- **Itemized List**: Product name, specifications, quantity, price per unit, and subtotal
- **Total Calculation**: Automatic sum of all items
- **Terms & Conditions**: Standard business terms included

## File Structure

```
Inventory Management/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── static/
│   └── css/
│       └── style.css     # Application styling
├── templates/
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   └── cart.html         # Cart and invoice page
└── utils/
    ├── db.py             # Database utilities
    ├── estimator.py      # Price estimation logic
    └── parser.py         # Transcript parsing logic
```

## Dependencies

- **Flask**: Web framework
- **reportlab**: PDF generation library
- **Python 3.7+**: Required for all features

## Browser Compatibility

The application works best with modern browsers that support:
- ES6 JavaScript features
- CSS Grid and Flexbox
- Fetch API for AJAX requests
- Blob API for file downloads

## Troubleshooting

### PDF Generation Issues
- Ensure all cart items have valid prices
- Check that the cart is not empty before generating
- Verify internet connection for file download

### Installation Issues
- Make sure Python 3.7+ is installed
- Use virtual environment for clean dependency management
- Install reportlab with: `pip install reportlab`

## License

This project is for educational and business use. 