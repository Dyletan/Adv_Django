1. Products App
Category
• Fields:
 – id: Auto-generated primary key
 – name: Name of the category (string)
 – description: Optional details (text)

Product
• Fields:
 – id: Auto-generated primary key
 – name: Product name
 – description: Detailed description
 - seller: Foreign Key to User
 – price: Price (decimal)
 – image: URL or file field for product image
 – category: Foreign key to Category
 – stock/availability: Integer field indicating inventory
 – created_at / updated_at: Timestamps

2. Trading App
Order
• Purpose: Captures the intent to transact (either buying or selling).
• Fields:
 – id: Auto-generated primary key
 – product: Foreign key to Product
 – order_type: Choice field
 – quantity: Number of items involved
 – price: Price per unit at the time of order placement
 – status: Current order state
 – timestamp: When the order was placed

Transaction
• Purpose: Represents the event when orders are matched and a trade is executed.
• Fields:
 – id: Auto-generated primary key
 – buy_order: Foreign key linking to the buyer’s Order
 – sell_order: Foreign key linking to the seller’s Order
 – product: Foreign key to Product (for quick reference)
 – quantity: Number of items traded
 – price: Execution price per unit
 – transaction_time: Timestamp of when the transaction occurred

3. Sales App
SalesOrder
• Purpose: Documents the finalized sales transaction after order matching.
• Fields:
 – id: Auto-generated primary key
 – transaction: Foreign key to the Transaction record
 – product: Foreign key to Product
 – quantity: Final quantity sold
 – sale_price: Final price per unit at which the sale was executed
 – status: Sales order state (e.g., processed, shipped, completed)
 – created_at / updated_at: Timestamps

Invoice
• Purpose: Generated as a formal billing document associated with a SalesOrder.
• I am not so sure about the structure of this model
• Fields:
 – id: Auto-generated primary key
 – sales_order: Foreign key linking back to the SalesOrder
 – invoice_number: Unique identifier for the invoice
 – invoice_date: Date/time when the invoice was generated
 – total_amount: Total amount charged (including any applicable fees or taxes)
 – tax_amount: Amount of tax applied
 – payment_status: Status of the payment (e.g., paid, pending, cancelled)
 – billing_address / shipping_address: Details for invoicing and delivery


