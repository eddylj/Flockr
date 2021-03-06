"""
Creating routes for the flask server
"""

from json import dumps
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from error import InputError
import auth
import channel
import channels
import message
import user
import other
import standup


def default_handler(err):
    """
    Function for wher there is an error in the code, it will output an error
    """
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__, static_url_path='/src/static/')
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, default_handler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    """
    Route to flask server to repeat what the user inputs
    """
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })


# AUTH FUNCTIONS
@APP.route("/auth/register", methods=['POST'])
def register():
    """
    Route to flask server to register a user to the flockr
    """
    data = request.get_json()
    email = data['email']
    password = data['password']
    first_name = data['name_first']
    last_name = data['name_last']
    return dumps(auth.auth_register(email, password, first_name, last_name))

@APP.route("/auth/login", methods=['POST'])
def login():
    """
    Route to flask server to login a user to the flockr
    """
    data = request.get_json()

    return dumps(
        auth.auth_login(data['email'], data['password'])
    )

@APP.route("/auth/logout", methods=['POST'])
def logout():
    """
    Route to flask server to logout a user from the flockr
    """
    data = request.get_json()

    return dumps(
        auth.auth_logout(data['token'])
    )

@APP.route("/auth/passwordreset/request", methods=['POST'])
def pw_request():
    """
    Route to flask server to request a password reset
    """
    data = request.get_json()

    return dumps(auth.auth_passwordreset_request(data['email']))

@APP.route("/auth/passwordreset/reset", methods=['POST'])
def pw_reset():
    """
    Route to flask server to reset a password
    """
    data = request.get_json()

    return dumps(
        auth.auth_passwordreset_reset(data['reset_code'], data['new_password'])
    )

# CHANNEL FUNCTIONS
@APP.route("/channel/invite", methods=['POST'])
def invite():
    """
    Route to flask server to invite a user to a channel
    """
    data = request.get_json()

    return dumps(
        channel.channel_invite(data['token'], data['channel_id'], data['u_id'])
    )

@APP.route("/channel/details", methods=['GET'])
def details():
    """
    Route to flask server to get all the details of a channel including name of
    the channel and all the members of the channel
    """
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))

    return dumps(channel.channel_details(token, channel_id, request.url_root))

@APP.route("/channel/messages", methods=['GET'])
def messages():
    """
    Route to flask server to get all the messages in the channel
    """
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))
    return dumps(channel.channel_messages(token, channel_id, start))


@APP.route("/channel/leave", methods=['POST'])
def leave():
    """
    Route to flask server to allow users to leave a channel
    """
    data = request.get_json()

    return dumps(
        channel.channel_leave(data['token'], data['channel_id'])
    )

@APP.route("/channel/join", methods=['POST'])
def join():
    """
    Route to flask server to allow users to join a channel
    """
    data = request.get_json()

    return dumps(
        channel.channel_join(data['token'], data['channel_id'])
    )

@APP.route("/channel/addowner", methods=['POST'])
def addowner():
    """
    Route to flask server to add owner to a channel
    """
    data = request.get_json()

    return dumps(
        channel.channel_addowner(data['token'], data['channel_id'], data['u_id'])
    )

@APP.route("/channel/removeowner", methods=['POST'])
def removeowner():
    """
    Route to flask server to remove an owner from a channel
    """
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    u_id = data['u_id']
    return dumps(channel.channel_removeowner(token, channel_id, u_id))

# CHANNELS FUNCTIONS
@APP.route("/channels/list", methods=['GET'])
def clist():
    """
    Route to flask server to list all the channels in the flockr that the user
    is a part of.
    """
    # token = request.args.get('token')

    return dumps(
        channels.channels_list(request.args.get('token'))
    )

@APP.route("/channels/listall", methods=['GET'])
def listall():
    """
    Route to flask server to list out all the channels in the flockr and their
    associated details
    """
    # token = request.args.get('token')

    return dumps(
        channels.channels_listall(request.args.get('token'))
    )

@APP.route("/channels/create", methods=['POST'])
def create():
    """
    Route to flask server to create a channel in the flockr
    """
    data = request.get_json()

    return dumps(
        channels.channels_create(data['token'], data['name'], data['is_public'])
    )


# MESSAGES FUNCTIONS
@APP.route("/message/send", methods=['POST'])
def send():
    """
    Route to server to allow a user to send a message in a channel
    """
    data = request.get_json()

    return dumps(
        message.message_send(data['token'], data['channel_id'], data['message'])
    )

@APP.route("/message/remove", methods=['DELETE'])
def remove():
    """
    Route to flask server to allow a user to remove a message in a channel
    """
    data = request.get_json()

    return dumps(
        message.message_remove(data['token'], data['message_id'])
    )

@APP.route("/message/edit", methods=['PUT'])
def edit():
    """
    Route to flask server to allow a user to edit a message in a channel
    """
    data = request.get_json()

    return dumps(
        message.message_edit(data['token'], data['message_id'], data['message'])
    )

@APP.route("/message/react", methods=['POST'])
def react():
    """
    Route to flask server to allow a user to react to a message in a channel
    """
    data = request.get_json()
    return dumps(
        message.message_react(data['token'], data['message_id'], data['react_id'])
    )

@APP.route("/message/unreact", methods=['POST'])
def unreact():
    """
    Route to flask server to allow a user to unreact a message in a channel
    """
    data = request.get_json()
    return dumps(
        message.message_unreact(data['token'], data['message_id'], data['react_id'])
    )

@APP.route("/message/pin", methods=['POST'])
def pin():
    """
    Route to flask server to allow a user to pin a message in a channel
    """
    data = request.get_json()
    return dumps(
        message.message_pin(data['token'], data['message_id'])
    )

@APP.route("/message/unpin", methods=['POST'])
def unpin():
    """
    Route to flask server to allow a user to unpin a message in a channel
    """
    data = request.get_json()
    return dumps(
        message.message_unpin(data['token'], data['message_id'])
    )

@APP.route("/message/sendlater", methods=['POST'])
def send_later():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    message_str = data['message']
    time_sent = data['time_sent']
    return dumps(
        message.message_send_later(token, channel_id, message_str, time_sent)
    )

# USER FUNCTIONS
@APP.route("/user/profile", methods=['GET'])
def profile():
    """
    Route to flask server to allow a user to look at their profile on flockr
    """
    token = request.args.get('token')
    u_id = request.args.get('u_id')
    return dumps(user.user_profile(token, int(u_id), request.url_root))


@APP.route("/user/profile/setname", methods=['PUT'])
def setname():
    """
    Route to flask server to allow a user to change their name in their profile
    on flockr.
    """
    data = request.get_json()
    token = data['token']
    first_name = data['name_first']
    last_name = data['name_last']
    return dumps(user.user_profile_setname(token, first_name, last_name))

@APP.route("/user/profile/setemail", methods=['PUT'])
def setemail():
    """
    Route to flask server to allow a user to change their email in their profile
    on flockr.
    """
    data = request.get_json()

    return dumps(
        user.user_profile_setemail(data['token'], data['email'])
    )

@APP.route("/user/profile/sethandle", methods=['PUT'])
def sethandle():
    """
    Route to flask server to allow a user to change their handle in their
    profile on flockr.
    """
    data = request.get_json()

    return dumps(
        user.user_profile_sethandle(data['token'], data['handle_str'])
    )

@APP.route("/users/all", methods=['GET'])
def usersall():
    """
    Route to flask server to list out all the users in the flockr and their
    associated details.
    """
    return dumps(other.users_all(request.args.get('token'), request.url_root))

@APP.route("/search", methods=['GET'])
def search():
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    return dumps(other.search(token, query_str))

@APP.route("/user/profile/uploadphoto", methods=['POST'])
def upload_photo():
    """
    Route to set a user's display photo, given a valid URL to an image and
    valid dimensions to crop.
    """
    data = request.get_json()
    token = data['token']
    img_url = data['img_url']
    x_start = data['x_start']
    y_start = data['y_start']
    x_end = data['x_end']
    y_end = data['y_end']
    return dumps(user.user_profile_uploadphoto(
        token, img_url, x_start, y_start, x_end, y_end
    ))

@APP.route("/src/static/<path:path>")
def send_js(path):
    return send_from_directory('', path)

@APP.route("/standup/start", methods=['POST'])
def standup_start():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    length = data['length']
    return dumps(standup.standup_start(token, channel_id, length))

@APP.route("/standup/active", methods=['GET'])
def standup_active():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    return dumps(standup.standup_active(token, channel_id))

@APP.route("/standup/send", methods=['POST'])
def standup_send():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    message = data['message']
    return dumps(standup.standup_send(token, channel_id, message))

if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
