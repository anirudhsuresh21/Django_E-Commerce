# WeShop
# Django_E-Commerce


Welcome to the WeShop
Django_E-Commerce repository!

This repository contains a Django web E-Commerce application.

This Appliction allows the user to create an account, login to the account so 
that he can make purchase. In this application I have added a payment gateway feature.
The SuperUser will be able to add more products to the webpage using the Django Admin page.
The User can also reset the password if forgot his previous password.


## Prerequisites

Before you can run this Django application, make sure you have the
following dependencies installed on your system:

-   Python 3.6+
-   pip (Python package manager)
-   virtualenv (recommended for isolating project dependencies)

## Getting Started

Follow these steps to clone and set up the project on your local
machine:

1.  Clone the repository to your local machine using the following
    command:

    ```bash git clone
    https://github.com/yourusername/Django_E-Commerce.git 

2. Navigate to the project directory:
     ```bash Copy code 
     cd Django_E-Commerce

3. Create a virtual environment (optional but recommended):
    ```bash Copy code 
      python -m venv venv 


4. Activate the virtual environment:
   ```bash
   venv\Scripts\activate

5. Install project dependencies:
   ```bash Copy code 
   pip install -r requirements.txt 
   
6. Migrate the database:
    ```bash Copy code 
    python manage.py migrate 

7. Create a superuser (admin) account (you'll be prompted to enter a username, email, and password):
    ```bash Copy code 
    python manage.py createsuperuser 
    
8. Start the development server:
    ```bash Copy code 
    python manage.py runserver 
    
Your Django application should now be running at http://localhost:8000/. You can access the admin interface at http://localhost:8000/admin/.


