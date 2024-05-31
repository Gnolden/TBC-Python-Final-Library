# library management system

gives the librarians the ability to control the database of books, the process of giving out and returning the books and
the customers are able to register on the site and rent out books from the library

### Prerequisites
- Python 3.10.4
- Django 4.2.13
- pip
- virtualenv 

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Gnolden/TBC-Python-Final-Library
   cd TBC-Python-Final-Library
   
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows use `venv\Scripts\activate`

3. Install the required packages:
   ```bash
   pip install -r requirements.txt

* to fill database for testing run the following command:
* python manage.py populate_library