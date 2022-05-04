import sys
import csv
import re

#function to validate name data
def validate_name(name):
    reg = "^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{1,150}$"
    pattern = re.compile(reg)
    return pattern.match(name)

#function to validate phone data
def validate_phone(num):

    #country code
    reg = "([+][1-9]{1,3})?[-\s\.]{0,1}"

    #area code
    reg += "([(]{0,1}\d{2,4}[)]{0,1})\s{0,1}"

    #additional identifying numbers
    reg += "[-\s\.0-6]{1}[-\s\.0-9]{4,9}"

    #extension
    reg += "([,]?[\\s]?ext[\\s]?\\d{1,20})?$"

    pattern = re.compile(reg)
    return pattern.match(num)

#fuction to format name data for easy checking
def format_name(name):
    if ',' in name:
        name = name.split(', ')[1].strip() + " " + name.split(', ')[0]
    name = name.lower()
    nameFinal = ""
    for c in name:
        if(re.compile("[^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]").match(c)):
            nameFinal += c
    return nameFinal

#function to formate phone data for easy comparison
def format_number(num):
    return re.sub('[^0-9]','', num)

#function to return key for any value
def get_key(val):
    for key, value in phoneBook.items():
        if val ==  value:  
            return key
    return "Key doesn't exist"

#function to add a new person to the database
def add_person(name, number):
    if(validate_name(name)):
        if(validate_phone(number)):
            name = format_name(name)
            number = format_number(number)
            phoneBook[name] = number
            print(name + " added")
        else:
            print("Invalid Phone Number")
    else:
        print("Invalid Name")

#function to remove someone from the database by name
def remove_person(name):
    if(validate_name(name)):
        name = format_name(name)
        for key, value in phoneBook.items():
            if name == key:  
                print("Person Removed")
                phoneBook.pop(name)
                return
        print("Person does not exist")
    else:
        print("Invalid name")
        

#function to remove someone from the database by telephone number
def remove_number(number):
    if(validate_phone(number)):
        number = format_number(number)
        find = get_key(number)
        remove_person(find)
    else:
        print("Invalid Phone NumberS")

#function to produce a list of the members of the database
def list_members():
    members = []
    for key, value in phoneBook.items():
        members.append(key + ": " + value)
    return members

#function to read user input from terminal and execute desired command
def get_user_input():
    print("Enter which option you would like to run : \n")
    print("0 - add user, 1 - remove user by name, 2 - remove user by number, 3 - list all members, 4 - quit")
    inp = input()

    while inp != '4':
        if inp != '0' and inp != '1' and  inp != '2' and  inp != '3' and inp != '4':
            print("Please enter a valid number betwen 0-4\n")
        else:
            if inp == '0':
                print("Please enter a valid name")
                name = input()
                print("Enter a valid phone number")
                num = input() 
                add_person(name, num)
            if inp == '1':
                print("Enter the name of the person to remove")
                name = input()
                remove_person(name)
            if inp == '2':
                print("Enter the phone number of the person to remove")
                num = input()
                remove_number(num)
            if inp == '3':
                members = list_members()
                for n in members:
                    print(n)  

        print("Enter which option you would like to run :")
        print("0 - add user, 1 - remove user by name, 2 - remove user by number, 3 - list all members, 4 - quit")
        inp = input()  

#function to parse data from a csv file
def parse_data(inputfile):
    with open(inputfile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            name = row[0]
            n = 1
            while(re.compile("[^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,}$").match(row[n])):
                name += ", " + row[n]
                n += 1
            add_person(name, row[n])

#driver function
if __name__ == "__main__":
    
    phoneBook = {}
    try:
        inputfile = sys.argv[1]
    except:
        print('InputValidation.py <inputfile>')
        sys.exit(2)
    parse_data(inputfile)
    get_user_input()