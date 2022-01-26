
Save New Duplicate & Edit Just Text Twitter
import sqlite3
from sqlite3 import Error
import re

class employee_database():
    def __init__(self, connection):
        self.connection = connection
        self.mycursor = connection.cursor()
        self.commit = self.connection
        self.code = 402179

    def delete_employee(self):
        #Checks user has Admin code.
        while True:
            try:
                verify_code = int(input('Admin code required (To exit type 0): '))
                if verify_code == self.code:
                    option = input(f"Remove user by 'email' or 'id")
                    if option not in['email', 'id']:
                        print('Invalid response.')
                    elif option == 'id':
                        user_id = int(input('To remove all data, enter ID: '))
                        self.mycursor.execute(f"DELETE FROM employees WHERE id = {user_id}")
                        self.connection.commit()
                        break
                    elif option == 'email':
                        user_email = int(input('To remove all data, enter e-mail: '))
                        self.mycursor.execute(f"DELETE FROM employees WHERE id = {user_email}")
                        self.connection.commit()
                        break
                elif verify_code == 0:
                    break
                else:
                    print('Incorrect code.')
            except Error:
                print(f'Error: {Error}')


    def display_employee(self):
        self.mycursor.execute("SELECT * FROM employees")
        result = self.mycursor.fetchall()
        for row in result:
            print(f"""==========================================================
User ID = {row[0]}
==========================================================
Name = {row[1]}
Surname = {row[2]}
Age = {row[3]}
E-Mail = {row[4]}
Number = {row[5]}
Country = {row[6]}
City = {row[7]}
Role = {row[8]}""")


    def create_employee(self):
        while True:
            name = input('Enter first name: ')
            if re.match("[A-Za-z]+$", name.lower()): break
            else: print('Incorrect input. Letters only.')

        while True:
            surname = input('Enter last name: ')
            if re.match("[A-Za-z]+$", surname.lower()): break
            else: print('Incorrect input. Letters only.')

        while True:
            country = input('Enter country: ')
            if re.match("[A-Za-z ]+$", country.lower()): break
            else: print('Incorrect input. Letters only.')

        while True:
            city = input('Enter city: ')
            if re.match("[A-Za-z ]+$", city.lower()): break
            else: print('Incorrect input. Letters only.')

        while True:
            try:
                age = int(input('Enter age: '))
                break
            except ValueError:
                print('Error in response. Numbers only.')

        while True:
            try:
                number = int(input('Enter phone number: '))
                break
            except ValueError:
                print('Error in response. Numbers only.')

        while True:
            regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
            email = input('Enter e-mail address: ').lower()
            if re.fullmatch(regex, email): break
            else: print('E-Mail contained illegal characters, try again.')

        while True:
            role = input('Enter your role: ').lower()
            if re.match("[A-Za-z ]+$", role.lower()):
                pass
            else:
                print('No numbers/special characters allowed.')
            if role in ['admin', 'manager']:
                check_code = int(input('Role requires Admin code, enter code: '))
                if check_code == self.code:
                    print('Role granted.')
                    break
                else:
                    print('Incorrect code, try again.')
            else:
                break

        # Performs Query
        try:
            values = f"'{name}', '{surname}', '{age}', '{email}', '{number}', '{country}', '{city}', '{role}'"
            query = f"INSERT INTO employees (name, surname, age, email, number, country, city, role) VALUES ({values})"
            self.mycursor.execute(query)
            # Saves data to localhost
            self.connection.commit()
            print('// ALL INFORMATION HAS BEEN STORED')
        except ValueError:
            print('Error while storing data. Try again.')

    def edit_employee(self):
        while True:
            try:
                verify_code = int(input('Admin code required to edit - (To exit type 0): '))
                if verify_code == self.code:
                    user_id = input('Enter ID: ')
                    user_decide = input(f"""ENTER WHICH INFORMATION YOU WANT TO CHANGE FROM THE FOLLOWING:
Name, Surname, Age, EMail, Number, Country, City, Role
: """)
                    varchar = ['name', 'surname', 'email', 'country', 'city', 'role']
                    integer = ['age', 'number']
                    if user_decide in varchar:
                        new_value = input(f'Enter new {user_decide}: ')
                        query = 'UPDATE employees SET {0} = ? WHERE id = ?'.format(user_decide.lower())
                        self.mycursor.execute(query, (new_value, user_id))
                        self.connection.commit()
                        print('Information updated.')
                    elif user_decide in integer:
                        new_value = input(f'Enter new {user_decide}: ')
                        query = f"UPDATE employees SET {user_decide}='{new_value}' WHERE id={user_id}"
                        self.mycursor.execute(query)
                        self.connection.commit()
                        print('Information updated.')
                    else: print('Incorrect response, ')
                elif verify_code == 0: break
                else: print('Incorrect code.')
            except Error:
                print(f'Error: {Error}')

def main():
    connection = None
    try:
        connection = sqlite3.connect('skies-db.db')
        print('Connection successfull to Skies Database')
    except Error as e:
        print(f'The error {e} occurred.')

    database = employee_database(connection)

    while True:
        user_decide = input(f"""==========================================================
// EMPLOYEE DATABASE
To display current database type 'display'
To add new user information type 'create'
To edit existing information type 'edit'
To remove a user from database type 'delete'
To close application type 'quit'
: """).lower()
        if user_decide in ['display', 'create', 'delete', 'edit', 'quit']:
            if user_decide == 'quit':
                exit()
            else:
                action = getattr(database, f'{user_decide}_employee')()
        else:
            print('Invalid input')

if __name__ == '__main__':
    main()
