# Avalon application

## How to use the RESTful API ?

* Launch the script start_app.sh (you have to install docker-compose before it).
* Then you can send request as follows.
  - Initialize databases (3 tables)
  ```bash
       - method: PUT
       - route: /retart_bdd
       - payload example: {
                              "table1": "rules",
                              "table2": "games",
                              "table3": "players"
                          }
       - response example: {
                               "request": "succeeded"
                           }
  ```
  - Visualize databases (3 tables)
  ```bash
       - method: GET
       - route: /view/<table_name> (table_name is rules or games or players)
       - payload example:
       - response example: {
                               "rules": [
                                   {
                                       "blue": 4,
                                       "id": "31b8ebd2-fb2b-418f-9d33-aaab4f28215e",
                                       "nb_player": 7,
                                       "q1": 2,
                                       "q2": 3,
                                       "q3": 3,
                                       "q4": 4,
                                       "q5": 4,
                                       "red": 3
                                   },
                                   {
                                       ...
                                   },
                                   {
                                       "blue": 6,
                                       "id": "61d2be22-19ba-4edf-95c1-9407f0ba6062",
                                       "nb_player": 9,
                                       "q1": 3,
                                       "q2": 4,
                                       "q3": 4,
                                       "q4": 5,
                                       "q5": 5,
                                       "red": 3
                                   }
                               ]
                           }
  ```
  - Start a new game
  ```bash
       - method: PUT
       - route: /games
       - payload example: {
                              "names": [
                                  "name1",
                                  "name2",
                                  "name3",
                                  "name4",
                                  "name5"
                              ],
                              "roles": [
                                  "oberon",
                                  "perceval",
                                  "morgan"
                              ]
                          }
       - response example: {
                               "id": "2669a9fe-37c4-4139-ab78-8e3f0d0607d0",
                               "players": [
                                   {
                                       "id": "95763b27-de50-4d39-8ac2-2a7010281788",
                                       "ind_player": 0,
                                       "name": "name1",
                                       "role": "assassin",
                                       "team": "red"
                                   },
                                   {
                                       ...
                                   },
                                   {
                                       "id": "83d21d25-f359-4ddc-9048-69ba1e6cf5b5",
                                       "ind_player": 4,
                                       "name": "name5",
                                       "role": "morgan",
                                       "team": "red"
                                   }
                               ]
                           }
  ```
  - Get mp3 file
  ```bash
       - method: GET
       - route: /<game_id>/mp3
       - payload example:
       - response example: response.mpga
  ```












4. Entrer le nom des joueurs d'une partie:
POST: http://localhost/1b8ad78c-da1d-41c1-8552-d2456ae13823/add_roles
Body: {"names": ["Chacha", "Romain", "Elsa", "Mathieu", "Flo", "Eglantine", "Richard", "Quentin", "Thomas"],
       "roles": ["Oberon", "Perceval", "Morgan"]}

5. Nouveau tour:
GET: http://localhost/1b8ad78c-da1d-41c1-8552-d2456ae13823/new_turn
---> {"name_player": "Elsa, "turn": 1, "nb_echec": 2, "nb_mission": 0, "nb_in_mission": 3}
("name_player" --> nom de la personne qui envoie les gens,
 "turn" --> numéro du tour dans la partie compris entre 1 et 5,
 "nb_echec" --> nombre d'échecs pour que la mission échoue,
 "nb_mission" --> nombre de missions échouées (0 car nouveau tour),
 "nb_in_mission" --> nombre de personnes à envoyer en mission)


6. Vote:
POST: http://localhost/1b8ad78c-da1d-41c1-8552-d2456ae13823/vote
Body: {"vote": "refused"}
---> {"request": "succeeded"}

Body: {"vote": "osef"}
--->
{
    "players": [
        {
            "color": "BLUE",
            "ind_player": 0,
            "name": "Chacha",
            "role": "Blue"
        },
        {
            "color": "BLUE",
            "ind_player": 1,
            "name": "Romain",
            "role": "Blue"
        },
        {
            "color": "BLUE",
            "ind_player": 2,
            "name": "Elsa",
            "role": "Perceval"
        },
        {
            "color": "RED",
            "ind_player": 3,
            "name": "Mathieu",
            "role": "Morgan"
        },
        {
            "color": "BLUE",
            "ind_player": 4,
            "name": "Flo",
            "role": "Blue"
        },
        {
            "color": "RED",
            "ind_player": 5,
            "name": "Eglantine",
            "role": "Assassin"
        },
        {
            "color": "BLUE",
            "ind_player": 6,
            "name": "Richard",
            "role": "Blue"
        },
        {
            "color": "RED",
            "ind_player": 7,
            "name": "Quentin",
            "role": "Oberon"
        },
        {
            "color": "BLUE",
            "ind_player": 8,
            "name": "Thomas",
            "role": "Merlin"
        }
    ]
}


7. Nouvelle mission:
GET: http://localhost/1b8ad78c-da1d-41c1-8552-d2456ae13823/new_mission
---> {"name_player": "Elsa, "turn": 1, "nb_echec": 2, "nb_mission": nb_mission, "nb_in_mission": 3}
("name_player" --> nom de la personne qui envoie les gens,
 "turn" --> numéro du tour dans la partie compris entre 1 et 5,
 "nb_echec" --> nombre d'échecs pour que la mission échoue,
 "nb_mission" --> nombre de missions échouées,
 "nb_in_mission" --> nombre de personnes à envoyer en mission)


8. Mélange des votes:
POST: http://localhost/088b2e91-d711-4add-9995-0a4e3ae59275/shuffle_vote
Body: {"Chacha": "FAIL", "Romain":"SUCCESS", "Elsa": "SUCCESS"}
--->
{
    "result": "FAIL",
    "vote1": "FAIL",
    "vote2": "SUCCESS",
    "vote3": "SUCCESS"
}
