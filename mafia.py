from sys import argv
from random import randrange, shuffle
from flask import Flask, render_template, url_for, request
from flask_httpauth import HTTPBasicAuth
from mafia_params import *

app = Flask(__name__)
auth = HTTPBasicAuth()
id = 0
nPlayers = 0
roles = []
ip2role_index_name = {}

@auth.verify_password
def verify_password(username, password):
    if len(username) > 0:
        return username
    return None

@app.route('/')
@auth.login_required
def index():
    global id, ip2role_index_name
    username = str(auth.current_user())
    role = ""
    image_name = ""
    ip = str(request.remote_addr)

    if ip in ip2role_index_name.keys():
        role = ip2role_index_name[ip][0]
        image_name = ip2role_index_name[ip][0] + "_" + str(ip2role_index_name[ip][1])
    else:
        if id > nPlayers:
            return "Numbers of players out of range!"   #TODO:well defined Error Page
        role = roles[id]
        ip2role_index_name[ip] = (role, str(randrange(1, nRoles[role] + 1)), username)
        image_name = role + "_" + str(ip2role_index_name[ip][1])
        print("*" * 20, "New Player","*" * 20)
        toGod = ip + " : " + str(id) + " : " + username +  " --> " + role
        toGod += "/" + role2fa[role]    #TODO: Just in Farsi Mode
        print(toGod)
        id += 1
    return render_template("index.html",
                            image_name=image_name,
                            role_name=role, role_name_fa=role2fa[role],
                            description=descriptions[role], description_fa=descriptions_fa[role],
                            is_farsi=True)


@app.route('/GOD')
def GOD_PAGE():
    global ip2role_index_name
    return render_template("GOD.html", ip2role_index_name=ip2role_index_name)

 
@app.errorhandler(404) 
def invalid_route(e):
    return render_template("404.html", is_farsi=True)


def help_me():
    usage = "-" * 70 + "\n"
    usage += "mafia - Web Server Application For Mafia Game Playing On Local Network \n\n"
    usage += "-" * 70 + "\n"
    usage += "Usage: python3 mafia number_of_players[int]\n"
    usage += "ex: python3 mafia 5\n"
    usage += "this will tell mafia.py that you want a game for 5 people.\n\n"
    usage += "If you've seen a bug here (or any idea that can help us) feel free to open an issue\n"
    usage += "here at : https://github.com/sadrasabouri/mafia/issues"
    print(usage)
    exit()


if __name__ == "__main__":
    if len(argv) < 2 or argv[1] in ['--help', 'help', '-h']:
        help_me()
    nPlayers = int(argv[1])
    if nPlayers > len(ordered_roles):
        print("Too many players, mafia doesn't support a game with", nPlayers, "player.")
        help_me()
    roles = ordered_roles[:nPlayers]
    shuffle(roles)
    app.run(host="0.0.0.0", \
            port=5000, \
            debug=True)
