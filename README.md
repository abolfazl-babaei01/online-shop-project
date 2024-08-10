# Online Shop

This is a Django online shop allowing users to browse, search, and purchase products. It includes features like product categories, user authentication, shopping cart, and order management.

## Key Features
- **User Authentication**: Secure user registration and login system with one-time password (OTP) verification for enhanced security.
-  **Product Management**: Dynamic product catalog with search and filter functionalities.
-  **Shopping Cart**: Users can add/remove products to/from their shopping cart and view the cart summary.
-  **Order Processing**: Complete order management system with detailed order summaries and invoice generation in PDF format.
-  **AJAX-powered Likes and Comments**: Users can like products and leave comments, all managed through AJAX for a seamless user experience.



## Prerequisites
- Python 
- Django 
- SQLite (default) or PostgreSQL
- jQuery (for AJAX-powered features) 
- A web browser


## Additional Notes

- **Payment Gateway**: Due to security considerations, the payment gateway integration has not been included in this project. Implementing a secure payment gateway requires additional measures to ensure the safety of users' financial information. It's recommended to integrate a trusted payment provider and follow best practices for securing transactions if you decide to implement this feature.

- **Styling**: The styling in this project is minimal and primarily intended for demonstration purposes. The focus has been on the backend functionality, and the frontend design is basic. For a production-ready application, consider investing in more refined styling and UI/UX design.



## Installation & Setup
```bash
# Clone the repository
git clone https://github.com/abolfazl-babaei01/online-shop-project.git

# Navigate to the project directory
cd online-shop-project

# Create and activate a virtual environment
python3 -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run the development server
python manage.py runserver

