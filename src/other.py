'''
Different Functions used throughout the program
'''

from data import data
from error import InputError, AccessError

def clear():
    '''
    Function to clear the data
    '''
    data['users'].clear()
    data['channels'].clear()
    data['tokens'].clear()

def get_active(token):
    """
    Checks if a token is active. Returns the corresponding u_id if it is active,
    None otherwise.

    Parameters:
        token (str) : Caller's authorisation hash.

    Returns:
        u_id (int)  : The corresponding u_id if token is active.
        None        : If token isn't active.
    """
    if token in data['tokens']:
        # Written in this redundant way because token will be changed in the future
        return data['users'][int(token)]['u_id']
    return None

def users_all(token):
    '''
    Function for returning all the information of the users
    '''
    return {
        'users': [
            {
                'u_id': 1,
                'email': 'cs1531@cse.unsw.edu.au',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'hjacobs',
            },
        ],
    }

def admin_userpermission_change(token, u_id, permission_id):
    '''
    Function for changing admin user permission
    '''
    
    # Invalid u_id
    owner_id = get_active(token)
    if owner_id is None:
        raise InputError

    # Invalid permission_id
    if permission_id not in (1, 2):
        raise InputError

    # Not an owner of flockr
    if data['users'][owner_id] == 2:
        raise AccessError

    # Change permission_id of u_id
    data['users'][u_id]['permission_id'] = permission_id

    return {}

def search(token, query_str):
    '''
    Function to find the information about messages
    '''
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }
