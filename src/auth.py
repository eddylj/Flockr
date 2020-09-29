from data import data
from error import InputError
import re 
from other import is_active

regex = '^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w{2,3}$'

def auth_login(email, password):
    index = 0
    for user in data['users']:
        index += 1
        if user['email'] == email and user['password'] == password:
            if not is_active(email):
                data['tokens'].append(email)
            return {
                'u_id': index,
                'token': email,
            }
    raise InputError

def auth_logout(token):
    for index in range(len(data['tokens'])):
        if data['tokens'][index] == token:
            data['tokens'].pop(index)
            return {'is_success': True}
    return {'is_success': False}

def auth_register(email, password, name_first, name_last):
    new_user = {
        'email': email,
        'password': password,
        'name_first': name_first,
        'name_last': name_last,
        'handle': (name_first + name_last)[:20]
    }
    # Check if email is valid
    if not is_valid(email):
        raise InputError

    '''
    Check if email is taken. Also checks for people with the same name to
    create unique handles.
    '''
    number = 0
    for user in data['users']:
        if user['email'] == email:
            raise InputError
        if (user['name_first'] == new_user['name_first'] and
            user['name_last'] == new_user['name_last']):
            number += 1

    # Generates a new handle if there are repeated names
    if number != 0:
        new_user['handle'] = new_handle(new_user['handle'], number)
    print(new_user['handle'])

    # Check if password is valid
    if len(new_user['password']) < 6:
        raise InputError

    # Check if first name is valid
    if not 1 <= len(new_user['name_first']) <= 50:
        raise InputError

    # Check if last name is valid
    if not 1 <= len(new_user['name_last']) <= 50:
        raise InputError
    
    data['users'].append(new_user)
    if not is_active(email):
        data['tokens'].append(email)

    return {
        'u_id': len(data['users']),
        'token': email,
    }

# Code provided in project specs, from:
# https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
# Checks if email is valid
def is_valid(email):  
    # pass the regular expression 
    # and the string in search() method 
    if(re.search(regex,email)):
        return True
          
    else:  
        return False

def new_handle(handle, num):
    offset = len(str(num))
    if len(handle) <= (20 - offset):
        return handle + str(num)
    else:
        return str(num).join([handle[:20 - offset], handle[20:]])

# user = ('validemail@gmail.com', '123abc!@#', 'Haydennnnnnnnnn', 'Everest')
# auth_register(*user)
# user1 = ('asdfasd@gmail.com', '123abc!@#', 'Haydennnnnnnnnn', 'Everest')
# auth_register(*user1)
# user2 = ('asdfasda@gmail.com', '123abc!@#', 'Haydennnnnnnnnn', 'Everest')
# auth_register(*user2)
# user3 = ('asdfasdb@gmail.com', '123abc!@#', 'Haydennnnnnnnnn', 'Everest')
# auth_register(*user3)
# user4 = ('asdfasdc@gmail.com', '123abc!@#', 'Haydennnnnnnnnn', 'Everest')
# auth_register(*user4)
# user5 = ('asdfasde@gmail.com', '123abc!@#', 'Haydennnnnnnnnn', 'Everest')
# auth_register(*user5)
# user6 = ('asdfasdf@gmail.com', '123abc!@#', 'Haydennnnnnnnnn', 'Everest')
# auth_register(*user6)
# user7 = ('asdfasdg@gmail.com', '123abc!@#', 'Haydennnnnnnnnn', 'Everest')
# auth_register(*user7)
# user8 = ('asdfasdga@gmail.com', '123abc!@#', 'Haydennnnnnnnnn', 'Everest')
# auth_register(*user8)
# user9 = ('asdfasdgq@gmail.com', '123abc!@#', 'Haydennnnnnnnnn', 'Everest')
# auth_register(*user9)
# user10 = ('asdfasdgb@gmail.com', '123abc!@#', 'Haydennnnnnnnnn', 'Everest')
# auth_register(*user10)
