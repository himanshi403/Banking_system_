

import os  # for creating directories Admin/Customer if it is not exists.
from datetime import date  # for date of account creation when new customer account is created.
import tkinter as tk
from tkinter import *


# Backend python functions code starts :
def is_valid(customer_account_number):
    try:
        customer_database = open("./database/Customer/customerDatabase.txt")
    except FileNotFoundError:
        os.makedirs("./database/Customer/customerDatabase.txt", exist_ok=True)
        print("# Customer database doesn't exists!\n# New Customer database created automatically.")
        customer_database = open("./database/Customer/customerDatabase.txt", "a")
    else:  # if customer account  number is already allocated then this will return false. otherwise true.
        if check_credentials(customer_account_number, "DO_NOT_CHECK", 2, True):
            return False
        else:
            return True
    customer_database.close()


def check_leap(year):
    return ((int(year) % 4 == 0) and (int(year) % 100 != 0)) or (int(year) % 400 == 0)


def check_date(date):
    days_in_months = ["31", "28", "31", "30", "31", "30", "31", "31", "30", "31", "30", "31"]
    days_in_months_in_leap_year = ["31", "29", "31", "30", "31", "30", "31", "31", "30", "31", "30", "31"]

    if date == "":
        return False

    date_elements = date.split("/")
    day = int(date_elements[0])
    month = int(date_elements[1])
    year = int(date_elements[2])
    if (year > 2021 or year < 0) or (month > 12 or month < 1):
        return False
    else:
        if check_leap(year):
            numOfDays = days_in_months_in_leap_year[month - 1]
        else:
            numOfDays = days_in_months[month - 1]
        return int(numOfDays) >= day >= 1


def is_valid_mobile(mobile_number):
    if mobile_number.__len__() == 10 and mobile_number.isnumeric():
        return True
    else:
        return False


def append_data(database_path, data):
    customer_database = open(database_path, "a")
    customer_database.write(data)


def display_account_summary(identity, choice):  # choice 1 for full summary; choice 2 for only account balance.
    flag = 0
    customer_database = open("./database/Customer/customerDatabase.txt")
    output_message = ""
    for line in customer_database:
        if identity == line.replace("\n", ""):
            if choice == 1:
                output_message += "Account number : " + line.replace("\n", "") + "\n"
                customer_database.__next__()  # skipping pin
                output_message += "Current balance : " + customer_database.__next__().replace("\n", "") + "\n"
                output_message += "Date of account creation : " + customer_database.__next__().replace("\n", "") + "\n"
                output_message += "Name of account holder : " + customer_database.__next__().replace("\n", "") + "\n"
                output_message += "Type of account : " + customer_database.__next__().replace("\n", "") + "\n"
                output_message += "Date of Birth : " + customer_database.__next__().replace("\n", "") + "\n"
                output_message += "Mobile number : " + customer_database.__next__().replace("\n", "") + "\n"
                output_message += "Gender : " + customer_database.__next__().replace("\n", "") + "\n"
                output_message += "Nationality : " + customer_database.__next__().replace("\n", "") + "\n"
                output_message += "KYC : " + customer_database.__next__().replace("\n", "") + "\n"
            else:
                customer_database.readline()  # skipped pin
                output_message += "Current balance : " + customer_database.readline().replace("\n", "") + "\n"
            flag = 1
            break

        else:
            for index in range(11):
                fetched_line = customer_database.readline()
                if fetched_line is not None:
                    continue
                else:
                    break
    if flag == 0:
        print("\n# No account associated with the entered account number exists! #")
    return output_message


def delete_customer_account(identity, choice):  # choice 1 for admin, choice 2 for customer
    customer_database = open("./database/Customer/customerDatabase.txt")
    data_collector = ""
    flag = 0
    for line in customer_database:
        if identity == line.replace("\n", ""):
            flag = 1
            for index in range(11):
                customer_database.readline()  # skipping the line
        else:
            data_collector += line
            for index in range(11):
                data_collector += customer_database.readline()
    customer_database = open("./database/Customer/customerDatabase.txt", "w")
    customer_database.write(data_collector)
    if flag == 1:
        output_message = "Account with account no." + str(identity) + " closed successfully!"
        if choice == 1:
            adminMenu.printMessage_outside(output_message)
        print(output_message)
    else:
        output_message = "Account not found !"
        if choice == 1:
            adminMenu.printMessage_outside(output_message)
        print(output_message)


def create_admin_account(identity, password):
    admin_database = open("./database/Admin/adminDatabase.txt", "a")
    admin_id = identity
    admin_password = password
    append_data("./database/Admin/adminDatabase.txt", admin_id + "\n" + admin_password + "\n" + "*\n")
    output_message = "Admin account created successfully !"
    adminMenu.printMessage_outside(output_message)
    print(output_message)
    admin_database.close()


def delete_admin_account(identity):
    admin_database = open("./database/Admin/adminDatabase.txt")
    data_collector = ""
    flag = 0
    for line in admin_database:
        if identity == line.replace("\n", ""):
            flag = 1
            for index in range(2):
                admin_database.readline()
        else:
            data_collector += line
            for index in range(2):
                data_collector += admin_database.readline()
    admin_database = open("./database/Admin/adminDatabase.txt", "w")
    admin_database.write(data_collector)
    if flag == 1:
        output_message = "Account with account id " + identity + " closed successfully!"
        print(output_message)
        adminMenu.printMessage_outside(output_message)
    else:
        output_message = "Account not found :("
        adminMenu.printMessage_outside(output_message)
        print(output_message)


def change_PIN(identity, new_PIN):
    customer_database = open("./database/Customer/customerDatabase.txt")
    data_collector = ""
    for line in customer_database:
        if identity == line.replace("\n", ""):
            data_collector += line  # ID
            data_collector += str(new_PIN) + "\n"  # PIN changed
            customer_database.readline()
            for index in range(10):
                data_collector += customer_database.readline()
        else:
            data_collector += line
            for index in range(11):
                data_collector += customer_database.readline()
    customer_database.close()
    customer_database = open("./database/Customer/customerDatabase.txt", "w")
    customer_database.write(data_collector)

    output_message = "PIN changed successfully."
    customerMenu.printMessage_outside(output_message)
    print(output_message)


def transaction(identity, amount, choice):  # choice 1 for deposit; choice 2 for withdraw
    customer_database = open("./database/Customer/customerDatabase.txt")
    data_collector = ""
    balance = 0
    for line in customer_database:
        if identity == line.replace("\n", ""):
            data_collector += line  # ID
            data_collector += customer_database.readline()  # PIN
            balance = float(customer_database.readline().replace("\n", ""))
            if choice == 2 and balance - amount < 10000:  # Minimum balance 10000
                return -1
            else:
                if choice == 1:
                    balance += amount
                else:
                    balance -= amount
            data_collector += str(balance) + "\n"
            for index in range(9):
                data_collector += customer_database.readline()
        else:
            data_collector += line
            for index in range(11):
                data_collector += customer_database.readline()

    customer_database.close()
    customer_database = open("./database/Customer/customerDatabase.txt", "w")
    customer_database.write(data_collector)
    return balance


def check_credentials(identity, password, choice,
                      admin_access):  # checks credentials of admin/customer and returns True or False
    folder_name = "./database/Admin" if (choice == 1) else "./database/Customer"
    file_name = "/adminDatabase.txt" if (choice == 1) else "/customerDatabase.txt"

    try:
        os.makedirs(folder_name, exist_ok=True)
        database = open(folder_name + file_name, "r")
    except FileNotFoundError:
        print("#", folder_name[2:], "database doesn't exists!\n# New", folder_name[2:],
              "database created automatically.")
        database = open(folder_name + file_name, "a")
        if choice == 1:
            database.write("admin\nadmin@123\n*\n")
    else:
        is_credentials_correct = False
        for line in database:
            id_fetched = line.replace("\n", "")
            password_fetched = database.__next__().replace("\n", "")
            if id_fetched == identity:
                if ((password == "DO_NOT_CHECK_ADMIN" and choice == 1 and admin_access == False) or (
                        password == "DO_NOT_CHECK" and choice == 2 and admin_access == True) or password_fetched == password):
                    is_credentials_correct = True
                    database.close()
                    return True
            if choice == 1:  # skips unnecessary lines in admin database.
                database.__next__()  # skipping line
            else:  # skips unnecessary lines in customer database.
                for index in range(10):
                    fetched_line = database.readline()
                    if fetched_line is not None:
                        continue
                    else:
                        break
        if is_credentials_correct:
            print("Success!")
        else:
            print("Failure!")

    database.close()
    return False


# Backend python functions code ends.
