## Vendor Management System
===========================

Setup project
------------------------------------------
1. Python
2. Install Virtualenv - pip install virtualenv
3. Create Virtualenv - python3 -m venv venv or virtualenv venv
4. Activate Virtualenv - source venv/bin/activate
6. Install requirements.txt file - pip install -r requiremetnts.txt
7. Setup Database connection-
    Note :-
        If your using postgressql you need to change the name, username, and password
        else you want to change the all.

8. Migrate the models - python manage.py makemigrations
                        python manage.py migrate

9. Run the project - python manage.py runserver


### Explore API Endpoints:

    You can explore and test your API endpoints using tools like Swagger, which is integrated into your project.

    Access Swagger UI: http://localhost:8000/swagger/
    Explore and test your API endpoints interactively.



### API Endpoints
1. Vendor Profile Management
    Create a new vendor:
        POST /api/vendors/

    List all vendors:
        GET /api/vendors/

    Retrieve a specific vendor's details:
        GET /api/vendors/{vendor_id}/

    Update a vendor's details:
        PUT /api/vendors/{vendor_id}/

    Delete a vendor:
        DELETE /api/vendors/{vendor_id}/

2. Purchase Order Tracking
    Create a purchase order:
        POST /api/purchase_orders/

    List all purchase orders with an option to filter by vendor:
        GET /api/purchase_orders/

    Retrieve details of a specific purchase order:
        GET /api/purchase_orders/{po_id}/

    Update a purchase order:
        PUT /api/purchase_orders/{po_id}/

    Delete a purchase order:
        DELETE /api/purchase_orders/{po_id}/

3. Vendor Performance Evaluation
    Retrieve a vendor's performance metrics:
        GET /api/vendors/{vendor_id}/performance/

4. Authentication
    Token-based authentication is used to secure API endpoints.

    Login:
    POST /api/login/

    Register:
    POST /api/register/
