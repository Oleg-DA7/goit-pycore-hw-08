# Завдання 1
# По перше додамо додатковий функціонал до класів з попередньої домашньої роботи:
# Додайте поле birthday для дня народження в клас Record . Це поле має бути класу Birthday. Це поле не обов'язкове, але може бути тільки одне.
# Додайте функціонал роботи з Birthday у клас Record, а саме функцію add_birthday, яка додає день народження до контакту.
# Додайте функціонал перевірки на правильність наведених значень для полів Phone, Birthday.
# Додайте та адаптуйте до класу AddressBook нашу функцію з четвертого домашнього завдання, тиждень 3, get_upcoming_birthdays, 
# яка для контактів адресної книги повертає список користувачів, яких потрібно привітати по днях на наступному тижні.

# Завдання 2
# Для реалізації нового функціоналу також додайте функції обробники з наступними командами:
# add-birthday - додаємо до контакту день народження в форматі DD.MM.YYYY                           +
# show-birthday - показуємо день народження контакту                                                +
# birthdays - повертає список користувачів, яких потрібно привітати по днях на наступному тижні     +

import re
from decorators import error_decorator
import datetime as dt
import pandas as pd

@error_decorator(default_result=[None, None])
def parse_input(user_input):    
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def next_birthday(birthday, date):    
    if birthday.replace(year = date.year) >= date: 
        return birthday.replace(year = date.year)
    else:
        return birthday.replace(year = date.year + 1)

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
class Birthday(Field):
    def __init__(self, value):
        tvalue = dt.datetime.strptime(value, '%d-%m-%Y').date()
        super().__init__(tvalue)

class PhoneNumber(Field):
    def __init__(self, phone_number):
        if re.fullmatch('[0-9]{10}', phone_number) != None:
            super().__init__(phone_number)
        else:
            print("Enter the correct phone number!")
    def __str__(self):
        return f'Phone number - {self.value}'
    
class ContactName(Field):
    def __init__(self, name):
        super().__init__(name)
    def __str__(self):
        return f'{self.value}'

class Contact():
    def __init__(self, args):
        self.name = ContactName(args[0])
        self.phones = []
        self.birthday = None

    def __str__(self):        
        return f'Contact name: {self.name.value}, phones: {[p.value for p in self.phones]}, birthday: {self.birthday}'
    
    @error_decorator(default_result=None)    
    def add_phone(self, args): # Додавання телефонів до контакту
        for i in self.phones:
            if i.value == args[1]:
                print(f'This number {args[1]} already exist in contact: {self.name.value}') 
                return None
        self.phones.append(PhoneNumber(args[1]))

    @error_decorator(default_result=None)  
    def del_phone(self, args): # Видалення телефону у контакта
        found = False
        for i in self.phones:
            if i.phone == args[1]:
                found = True
                self.phones.remove(i)
                print(f'Number {args[1]} deleted in contact: {self.name.value}') 
        if not found:
            print(f'Number {args[1]} not found in contact: {self.name.value}') 
        return None
    
    @error_decorator(default_result=None)          
    def change_phone(self, args): # Редагування телефонів - зміна номеру на інший
        found = False
        for i in self.phones:
            if i.value == args[1]:
                found = True
                i.value = args[2]
                print(f'Phone number {args[1]} changed to {i.value} in contact: {self.name.value}') 
        if not found:
            print(f'Number {args[1]} not found in contact: {self.name.value}') 
        return None
    
    @error_decorator(default_result=None)  
    def find_phone(self, args): # Пошук телефону
        found = False
        for i in self.phones:
            if i.value == args[1]:
                found = True
        if found: 
            return f'{args[1]} found in contact: {self.name.value}'
        else: 
            return f'{args[1]} not found in contact: {self.name.value}'
    
    @error_decorator(default_result=None)  
    def add_birthday(self, args): # Додаемо Birthday
        self.birthday = Birthday(args[1])
        return f'Birthday - {self.birthday.value.strftime('%d-%m-%Y')} added for contact {self.name}'
    
    @error_decorator(default_result=None)  
    def show_birthday(self, args): # Додаемо Birthday        
        return f'{self.birthday.value.strftime('%d-%m-%Y')}'

class ContactList():
    def __init__(self):
        self.contacts = []    

    @error_decorator(default_result = None)
    def add_contact(self, contact):
        self.contacts.append(contact)
        return (f'{contact} added.')
    
    def all_contacts(self):
        for i in self.contacts: 
            print(f'{i}')

    @error_decorator(default_result = None)
    def get_contact(self, args): 
        name = args[0]
        result = None
        for i in self.contacts:
            if i.name.value == name: 
                result = i
        if result == None : print(f'Contact {name} not found !')
        return result

    @error_decorator(default_result = None)
    def del_contact(self, args): 
        found = False
        name = args[0]
        for i in self.contacts:
            if i.name.value == name: 
                found = True
                self.contacts.remove(i)
                print(f'Contact {name} deleted')
        if not found: print(f'Contact {name} not found !')

    @error_decorator(default_result=None)
    def change_contact(self, args):
        result = 'Contact not found'
        for i in self.contacts:
            if i.name.value == args[0]: 
                i.name.value = args[1]
                result = f'Contact updated to {i}'
        return result
    
    def birthdays(self):
        result = []
        now_date = dt.datetime.now().date()
        users = [{'name': i.name.value, 'birthday': i.birthday.value.strftime('%d-%m-%Y')} for i in self.contacts]
        users_df = pd.DataFrame(users)
        users_df['birthday'] =  users_df['birthday'].apply(lambda x: dt.datetime.strptime(x, '%d-%m-%Y').date())
        users_df['next_birthday'] = users_df['birthday'].apply(lambda x: next_birthday(x, now_date))
        users_df['delta'] = users_df['birthday'].apply(lambda x: (next_birthday(x, now_date) - now_date).days)
        for i, r in users_df.iterrows():
            if r['delta'] <= 7:
                congrats_date = r['next_birthday']
                if r['next_birthday'].weekday() in [5, 6]: 
                    congrats_date = r['next_birthday'] + dt.timedelta(days=(7 - r['next_birthday'].weekday()))
                result.append({'name': f'{r['name']}', 'congratulation_date': f'{dt.datetime.strftime(congrats_date, '%d-%m-%Y')}'})
        return result


def main():
    cl = load_data()
#    cl = ContactList()
    print("Welcome to the assistant bot!")
    while True:
         user_input = input("Enter a command: ")
         command, *args = parse_input(user_input)
         match command:
            case "close" | "exit":
                print("Good bye!")
                save_data(cl)
                break
            case "hello":
                print("How can I help you?")

# ContactList command -------------------------------------
            case "del":                
                cl.del_contact(args)  
            case "add":
                c = Contact(args)
                if c != None:
                    print(cl.add_contact(c))  
            case "change":
                result = cl.change_contact(args)                 
                if result != None:
                    print(result)         
            case "find":
                result = cl.get_contact(args)                 
                if result != None:
                    print(result)   
            case "all":
                cl.all_contacts()      
            case "birthdays" | "bs":
                print(cl.birthdays())

# Contact command -----------------------------------------
            case "add_phone":
                c = cl.get_contact(args)
                if c != None:
                    c.add_phone(args)    
            case "del_phone":
                c = cl.get_contact(args)
                if c != None:
                    c.del_phone(args)     
            case "change_phone":
                c = cl.get_contact(args)
                if c != None:
                    c.change_phone(args)                                
            case "find_phone":
                c = cl.get_contact(args)
                if c != None:
                    print(c.find_phone(args))
            case "add_birthday" | "ab":
                c = cl.get_contact(args)
                if c != None:
                    print(c.add_birthday(args))
            case "show_birthday" | "sb":
                c = cl.get_contact(args)
                if c != None:
                    print(c.show_birthday(args))


import pickle

def save_data(contacts, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(contacts, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return ContactList()  


if __name__ == "__main__":
 
    main()


