# -*- coding: utf-8 -*-
# author: romain.121@hotmail.fr

"""This functions are used is the RESTful web service of Avalon"""

import os
from random import shuffle, choice

from flask import Blueprint, Flask, jsonify, make_response, request, abort, send_file, Response, render_template
from werkzeug.security import generate_password_hash, check_password_hash

# from app import auth
import rethinkdb as r


avalon_blueprint = Blueprint('avalon', __name__)
auth_blueprint = Blueprint('auth', __name__)

users = {"mathieu": generate_password_hash("lebeaugosse"),
         "romain": generate_password_hash("lala")}




@avalon_blueprint.before_request
def before_first_request_func():
    r.RethinkDB().connect("rethinkdb", 28015).repl()


@avalon_blueprint.route('/restart_bdd', methods=['PUT'])
def restart_bdd():
    """
    This function deletes all tables in the post request and initializes them
        - method: PUT
            - route: /restart_bdd
            - example payload: {"table1": "rules", "table2": "games"}
    """

    for key in request.json.values():
        if key in r.RethinkDB().db('test').table_list().run():
            r.RethinkDB().table_drop(key).run()

        # initialize table
        r.RethinkDB().table_create(key).run()

        # fill rules table
        if key == "rules":
            r.RethinkDB().table("rules").insert([
                {"nb_player": 5, "blue": 3, "red": 2,
                 "quest1": 2, "quest2": 3, "quest3": 2, "quest4": 3, "quest5": 3,
                 "echec1": 1, "echec2": 1, "echec3": 1, "echec4": 1, "echec5": 1},
                {"nb_player": 6, "blue": 4, "red": 2,
                 "quest1": 2, "quest2": 3, "quest3": 4, "quest4": 3, "quest5": 4,
                 "echec1": 1, "echec2": 1, "echec3": 1, "echec4": 1, "echec5": 1},
                {"nb_player": 7, "blue": 4, "red": 3,
                 "quest1": 2, "quest2": 3, "quest3": 3, "quest4": 4, "quest5": 4,
                 "echec1": 1, "echec2": 1, "echec3": 1, "echec4": 2, "echec5": 1},
                {"nb_player": 8, "blue": 5, "red": 3,
                 "quest1": 3, "quest2": 4, "quest3": 4, "quest4": 5, "quest5": 5,
                 "echec1": 1, "echec2": 1, "echec3": 1, "echec4": 2, "echec5": 1},
                {"nb_player": 9, "blue": 6, "red": 3,
                 "quest1": 3, "quest2": 4, "quest3": 4, "quest4": 5, "quest5": 5,
                 "echec1": 1, "echec2": 1, "echec3": 1, "echec4": 2, "echec5": 1},
                {"nb_player": 10, "blue": 6, "red": 4,
                 "quest1": 3, "quest2": 4, "quest3": 4, "quest4": 5, "quest5": 5,
                 "echec1": 1, "echec2": 1, "echec3": 1, "echec4": 2, "echec5": 1}]).run()

    return jsonify({"request": "succeeded"})


@avalon_blueprint.route('/view/<table_name>', methods=['GET'])
def view(table_name):
    """
    This function gives a table depending on the input table_name
        - method: GET
            - route: /view/rules or /view/games
            - example payload:
    """

    response = {table_name: []}
    cursor = r.RethinkDB().table(table_name).run()
    for document in cursor:
        response[table_name].append(document)

    return jsonify(response)


@avalon_blueprint.route('/games', methods=['PUT'])
def add_roles():
    """This function adds rules and roles to players randomly
        - method: PUT
            - route: /games
            - example payload: {"names": ["Chacha", "Romain", "Elsa", "Mathieu", "Flo",
                                          "Eglantine", "Richard", "Quentin", "Thomas"],
                                "roles": ["Oberon", "Perceval", "Morgan"]}
    """

    insert = r.RethinkDB().table("games").insert([{"players": [],
                                                   "rules": {}}]).run()

    id_game = insert["generated_keys"][0]

    # add rules
    rules = list(r.RethinkDB().table("rules").filter({"nb_player": len(request.json["names"])}).run())[0]
    del rules["id"]
    del rules["nb_player"]
    bdd_update_value("games", id_game, "rules", rules)

    # add players
    players = roles_and_players(request.json, rules["red"], rules["blue"])
    list_id_player = []
    for player in players:
        insert = r.RethinkDB().table("players").insert(player).run()
        list_id_player.append(insert["generated_keys"][0])

    ind = choice(range(len(request.json["names"])))
    bdd_update_value("games", id_game, "current_ind_player", ind)

    current_id_player = list(r.RethinkDB().table("players").filter({"ind_player": ind}).run())[0]["id"]
    bdd_update_value("games", id_game, "current_id_player", current_id_player)

    current_name_player = list(r.RethinkDB().table("players").filter({"ind_player": ind}).run())[0]["name"]
    bdd_update_value("games", id_game, "current_name_player", current_name_player)

    bdd_update_value("games", id_game, "current_quest", 1)
    bdd_update_value("games", id_game, "nb_mission_unsend", 0)
    bdd_update_value("games", id_game, "players", list_id_player)

    list_players = []
    for id_player in list_id_player:
        list_players.append(list(r.RethinkDB().table("players").get_all(id_player).run())[0])

    return jsonify({"players": list_players, "id": id_game})


@avalon_blueprint.route('/<game_id>/mp3', methods=['GET'])
def post_mp3(game_id):

    list_players_id = bdd_get_value("games", game_id, "players")
    list_roles = []
    for player_id in list_players_id:
        list_roles.append(list(r.RethinkDB().table("players").filter({"id": player_id}).run())[0]["role"])

    create_mp3(list_roles)

    return send_file("resources/roles.mp3", attachment_filename='roles.mp3', mimetype='audio/mpeg')


@avalon_blueprint.route('/<game_id>/new_quest', methods=['POST'])
def new_quest(game_id):

    rules = bdd_get_value("games", game_id, "rules")
    current_ind_player = bdd_get_value("games", game_id, "current_ind_player")
    dict_quest = {"nb_mission_unsend": 0,
                  "current_id_player": bdd_get_value("games", game_id, "current_id_player"),
                  "current_ind_player": bdd_get_value("games", game_id, "current_ind_player"),
                  "current_name_player": bdd_get_value("games", game_id, "current_name_player"),
                  "current_quest": bdd_get_value("games", game_id, "current_quest"),
                  "nb_player_to_send": {key: val for key, val in rules.items() if key[:5] == "quest"},
                  "nb_echec_to_fail": {key: val for key, val in rules.items() if key[:5] == "echec"}}

    return jsonify(dict_quest)





########################################################################################################################
########################################################################################################################
########################################################################################################################


def bdd_get_value(table, ident, key):
    """This function finds the key's value in the table"""

    return r.RethinkDB().table(table).get(ident)[key].run()


def bdd_update_value(table, ident, key, value):
    """This function updates the key's value in the bdd"""

    return r.RethinkDB().table(table).get(ident).update({key: value}).run()


def roles_and_players(dict_names_roles, max_red, max_blue):
    """Check the validity of proposed roles
    cases break rules : - 1. morgan in the game but Perceval is not
                        - 2. perceval in the game but Morgan is not
                        - 3. Unvalid role
                        - 4. Too many red in the game (or too many blue in the game, checked but impossible)"""

    if "morgan" in dict_names_roles["roles"] and "perceval" not in dict_names_roles["roles"]:
        print("ERROR !!! morgan is in the game but perceval is not")

    if "perceval" in dict_names_roles["roles"] and "morgan" not in dict_names_roles["roles"]:
        print("ERROR !!! perceval is in the game but morgan is not")

    nb_red, nb_blue = 1, 1
    list_roles = ["merlin", "assassin"]
    for role in dict_names_roles["roles"]:
        if role in ["mordred", "morgan", "oberon"]:
            nb_red += 1
            list_roles.append(role)
        elif role == "perceval":
            nb_blue += 1
            list_roles.append(role)
        else:
            print("ERROR !!! can't add this role: "+str(role))

    if nb_red <= max_red and nb_blue <= max_blue:
        list_roles.extend(["red"]*(max_red-nb_red))
        list_roles.extend(["blue"]*(max_blue-nb_blue))

    else:
        print("ERROR !!! Too many red or blue")

    shuffle(list_roles)

    list_players = []
    for ind, role in enumerate(list_roles):
        if role in ["merlin", "perceval", "blue"]:
            list_players.append({"ind_player": ind, "name": dict_names_roles["names"][ind],
                                 "team": "blue", "role": role})
        else:
            list_players.append({"ind_player": ind, "name": dict_names_roles["names"][ind],
                                 "team": "red", "role": role})

    return list_players


def create_mp3(list_roles):
    """Create mp3 file depending on roles in the game"""

    list_to_merge = ["init.mp3", "serv_mord.mp3"]
    if "oberon" in list_roles:
        list_to_merge.append("oberon.mp3")
    list_to_merge.append("red_identi.mp3")

    if "morgan" in list_roles and "perceval" in list_roles:
        list_to_merge.append("add_per_mor.mp3")

    list_to_merge.append("serv_mord.mp3")
    if "mordred" in list_roles:
        list_to_merge.append("mordred.mp3")
    list_to_merge.extend(["merlin_identi.mp3", "end.mp3"])

    str_command = "cat "
    for i in range(len(list_to_merge)):
        str_command += "resources/"+list_to_merge[i]+" "
    str_command += " > resources/roles.mp3"
    os.system(str_command)
    print("\n\n----->", str_command)
    mp3_file = open('./resources/roles.mp3', 'rb')
    print(mp3_file)
    #os.system("rm -f /resources/roles.mp3")

    return mp3_file



########################################################################################################################
########################################################################################################################
########################################################################################################################




# def bdd_get_players_value(ident, ind_player, key):
#     """This function finds the key's value in the bdd of players"""
#     with r.RethinkDB().connect(host=host, port=port) as conn:

#         return r.RethinkDB().table("games").get(ident)['players'].filter({"ind_player": ind_player}).run(conn)[0][key]







# @auth_blueprint.login_required
# @avalon_blueprint.route('/<ident>/get/<table>/<key>', methods=['POST'])
# def get(ident, table, key):
#     """This function finds the key's value depending of the table in the bdd"""

#     return r.RethinkDB().table(table).get(ident)[key].run()



#######################################################################################################################
#######################################################################################################################


# @auth_blueprint.verify_password
# def verify_password(username, password):
#     if username in users:
#         return check_password_hash(users.get(username), password)
#     return False



# @avalon_blueprint.route('/<ident>/new_turn', methods=['GET'])
# def new_turn(ident):
#     """This function updates the bdd with a new turn"""

#     with r.RethinkDB().connect(host=host, port=port) as conn:

#         nb_player = len(bdd_get_value(ident, "players"))-1

#         # get current player
#         current_player = bdd_get_value(ident, 'current_player')

#         # get name of current player
#         name_player = bdd_get_players_value(ident, current_player, 'name')

#         # get current turn
#         current_turn = bdd_get_value(ident, "current_turn")

#         # get number of echecs
#         nb_echec_to_fail = 1
#         if current_turn == 4 and nb_player >= 7:
#             nb_echec_to_fail = 2

#         # get number of mission
#         nb_failed_mission = bdd_get_value(ident, "current_echec")

#         # get number of vote
#         nb_in_mission = r.RethinkDB().table("games").get(ident)['rules']['q'+str(current_turn)].run(conn)

#     return jsonify({"name_player": name_player, "turn": current_turn, "nb_echec_to_fail": nb_echec_to_fail,
#                     "nb_failed_mission": nb_failed_mission, "nb_in_mission": nb_in_mission})


# @avalon_blueprint.route('/<ident>/new_mission', methods=['GET'])
# def new_mission(ident):
#     """This function updates the bdd with a new vote"""

#     with r.RethinkDB().connect(host=host, port=port) as conn:

#         nb_player = len(bdd_get_value(ident, "players"))-1

#         # get current player
#         current_player = bdd_get_value(ident, 'current_player')

#         # get name of current player
#         name_player = bdd_get_players_value(ident, current_player, 'name')

#         # get current turn
#         current_turn = bdd_get_value(ident, "current_turn")

#         # get number of echecs
#         nb_echec_to_fail = 1
#         if current_turn == 4 and nb_player >= 7:
#             nb_echec_to_fail = 2

#         # get number of echec
#         nb_failed_mission = bdd_get_value(ident, "current_echec")

#         # get number of vote
#         nb_vote = r.RethinkDB().table("games").get(ident)['rules']['q'+str(current_turn)].run(conn)

#     return jsonify({"name_player": name_player, "turn": current_turn, "nb_echec_to_fail": nb_echec_to_fail,
#                     "nb_failed_mission": nb_failed_mission, "nb_in_mission": nb_in_mission})


# @avalon_blueprint.route('/<ident>/vote', methods=['POST'])
# def vote(ident):
#     """This function gives the answer of a vote"""

#     if request.json["vote"] == "refused":

#         nb_player = len(bdd_get_value(ident, "players"))-1

#         # update current player
#         current_player = bdd_get_value(ident, 'current_player')
#         new_current_player = current_player+1
#         if current_player == nb_player:
#             new_current_player = 0
#         bdd_update_value(ident, "current_player", new_current_player)

#         # update number of echec
#         new_current_echec = bdd_get_value(ident, 'current_echec')+1
#         bdd_update_value(ident, "current_echec", new_current_echec)

#         return jsonify({"request": "succeeded"})

#     return jsonify({"players": bdd_get_value(ident, "players")})


# @avalon_blueprint.route('/<ident>/shuffle_vote', methods=['POST'])
# def shuffle_vote(ident):
#     """This function shuffles vote"""

#     dict_bdd = request.json.copy()
#     nb_player = len(bdd_get_value(ident, "players"))-1

#     # get current turn
#     current_turn = bdd_get_value(ident, "current_turn")

#     # get number of echecs
#     nb_echec_to_fail = 1
#     if current_turn == 4 and nb_player >= 7:
#         nb_echec_to_fail = 2

#     cpt_false = 0
#     for val in dict_bdd.values():
#         if val == "FAIL":
#             cpt_false += 1

#     dict_bdd["result"] = "SUCCESS"
#     if cpt_false >= nb_echec_to_fail:
#         dict_bdd["result"] = "FAIL"

#     bdd_update_value(ident, "mission_"+str(current_turn), dict_bdd)

#     bdd_update_value(ident, "current_turn", current_turn)

#     list_vote = request.json.values()
#     shuffle(list_vote)

#     dict_output = {}
#     for ind, vote in enumerate(list_vote):
#         dict_output["vote"+str(ind+1)] = vote
#     dict_output["result"] = dict_bdd["result"]

#     return jsonify(dict_output)


#######################################################################################################################
#######################################################################################################################








# def create_mp3(list_roles):
#     """Create mp3 file depending on roles in the game"""

#     list_to_merge = ["init.mp3", "serv_mord.mp3"]
#     if "oberon" in list_roles:
#         list_to_merge.append("oberon.mp3")
#     list_to_merge.append("red_identi.mp3")

#     if "morgan" in list_roles and "perceval" in list_roles:
#         list_to_merge.append("add_per_mor.mp3")

#     list_to_merge.append("serv_mord.mp3")
#     if "mordred" in list_roles:
#         list_to_merge.append("mordred.mp3")

#     list_to_merge.extend(["merlin_identi.mp3", "end.mp3"])

#     str_command = "python concat.py "
#     for val in list_to_merge:
#         str_command += "resources/"+val+" "
#     str_command += "> resources/roles.mp3"
#     print(str_command)
#     os.system(str_command)



# @avalon_blueprint.route("/<ident>/mp3_2")
# def streamwav():
#     def generate():
#         with open("data/roles.mp3", "rb") as fwav:
#             data = fwav.read(1024)
#             while data:
#                 yield data
#                 data = fwav.read(1024)
#     return Response(generate(), mimetype="audio/mpeg") # mimetype="audio/x-mp3", mimetype="audio/mp3"



# mp3_file = create_mp3(list_roles)
# print(mp3_file)
# response = make_response(mp3_file)
# response.headers.set('Content-Type', 'audio/mpeg')
# response.headers.set('Content-Disposition', 'attachment', filename='%s.jpg' % pid)





