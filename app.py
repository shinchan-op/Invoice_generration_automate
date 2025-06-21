from flask import Flask, render_template, request, jsonify, send_file
from utils.parser import parse_transcript
from utils.estimator import enrich_cart
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
import io
import os

app = Flask(__name__)

# Global variable to store the latest transcription
latest_transcription = ""
transcription_history = []

@app.route('/')
def index():
    return render_template('index.html', latest_transcription=latest_transcription, transcription_history=transcription_history)

@app.route('/receive_transcription', methods=['POST'])
def receive_transcription():
    """Receive transcription from webhook server"""
    global latest_transcription, transcription_history
    
    try:
        data = request.get_json()
        if data and 'transcript' in data:
            transcript_text = data['transcript']
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Update latest transcription
            latest_transcription = transcript_text
            
            # Add to history
            transcription_history.append({
                'text': transcript_text,
                'timestamp': timestamp
            })
            
            # Keep only last 10 transcriptions
            if len(transcription_history) > 10:
                transcription_history = transcription_history[-10:]
            
            print(f"Received transcription at {timestamp}: {transcript_text}")
            return jsonify({'status': 'success', 'message': 'Transcription received'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'No transcript found in request'}), 400
            
    except Exception as e:
        print(f"Error receiving transcription: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/get_latest_transcription', methods=['GET'])
def get_latest_transcription():
    """API endpoint to get the latest transcription and full transcription history"""
    # Concatenate all transcriptions into one full transcript
    full_transcript = ""
    if transcription_history:
        # Join all transcriptions with spaces
        full_transcript = " ".join([item['text'] for item in transcription_history])
    
    return jsonify({
        'transcription': latest_transcription,
        'full_transcript': full_transcript,
        'history': transcription_history
    })

@app.route('/generate_cart', methods=['POST'])
def generate_cart():
    transcript = request.form.get('transcript')
    user_pincode = request.form.get('pincode')

    parsed_items = parse_transcript(transcript)
    enriched_cart = enrich_cart(parsed_items, user_pincode)

    return render_template('cart.html', cart_items=enriched_cart)

@app.route('/generate_invoice', methods=['POST'])
def generate_invoice():
    # Get cart data from the request
    cart_data = request.get_json()
    
    if not cart_data or not cart_data.get('items'):
        return jsonify({'error': 'No cart items found'}), 400
    
    # Create PDF in memory
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    # Add title
    elements.append(Paragraph("INVOICE", title_style))
    elements.append(Spacer(1, 20))
    
    # Add company info
    company_info = [
        ["Steel Merchant Inventory System"],
        ["123 Steel Street, Industrial Area"],
        ["Phone: +91-9876543210 | Email: info@steelmerchant.com"],
        ["GSTIN: 27ABCDE1234F1Z5"]
    ]
    
    company_table = Table(company_info)
    company_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 16),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(company_table)
    elements.append(Spacer(1, 20))
    
    # Add invoice details
    invoice_details = [
        ["Invoice Date:", datetime.now().strftime("%d/%m/%Y")],
        ["Invoice Number:", f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"],
        ["Customer Pincode:", cart_data.get('pincode', 'N/A')]
    ]
    
    invoice_table = Table(invoice_details, colWidths=[2*inch, 3*inch])
    invoice_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(invoice_table)
    elements.append(Spacer(1, 20))
    
    # Prepare cart items for table
    table_data = [['Product', 'Specifications', 'Quantity', 'Price/Unit', 'Subtotal']]
    total_amount = 0
    
    for item in cart_data['items']:
        subtotal = float(item.get('subtotal', 0).replace('₹', '').replace(',', ''))
        total_amount += subtotal
        
        table_data.append([
            item.get('product', ''),
            item.get('specs', ''),
            str(item.get('quantity', 0)),
            f"₹{item.get('price_per_unit', 0)}",
            f"₹{subtotal:,.2f}"
        ])
    
    # Add total row
    table_data.append(['', '', '', 'Total:', f"₹{total_amount:,.2f}"])
    
    # Create cart table
    cart_table = Table(table_data, colWidths=[1.5*inch, 2*inch, 0.8*inch, 1*inch, 1.2*inch])
    cart_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (2, 1), (2, -2), 'CENTER'),  # Quantity column
        ('ALIGN', (3, 1), (-1, -2), 'RIGHT'),  # Price columns
    ]))
    
    elements.append(cart_table)
    elements.append(Spacer(1, 30))
    
    # Add terms and conditions
    terms = [
        "Terms and Conditions:",
        "• Payment is due within 30 days of invoice date",
        "• Delivery will be made as per estimated delivery schedule",
        "• Prices are subject to change without prior notice",
        "• Goods once sold will not be taken back",
        "• For any queries, please contact our customer service"
    ]
    
    for term in terms:
        if term.startswith("•"):
            elements.append(Paragraph(term, styles['Normal']))
        else:
            elements.append(Paragraph(term, styles['Heading2']))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"invoice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
        mimetype='application/pdf'
    )

if __name__ == '__main__':
    app.run(debug=True)
