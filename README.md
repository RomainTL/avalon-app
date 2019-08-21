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
  - Visualize board
  ```bash
       - method: GET
       - route: /<game_id>/board
       - payload example:
       - response example: {
                               "current_id_player": "79d33eb2-199c-40a2-8205-27cc3511aede",
                               "current_ind_player": 1,
                               "current_name_player": "name2",
                               "current_quest": 1,
                               "nb_echec_to_fail": {
                                   "echec1": 1,
                                   "echec2": 1,
                                   "echec3": 1,
                                   "echec4": 1,
                                   "echec5": 1
                               },
                               "nb_mission_unsend": 0,
                               "nb_player_to_send": {
                                   "quest1": 2,
                                   "quest2": 3,
                                   "quest3": 2,
                                   "quest4": 3,
                                   "quest5": 3
                               }
                           }
  ```
  - Send new mission
  ```bash
       - method: POST
       - route: /<game_id>/mission
       - payload example1: {
                               "status": "send"
                           }
       - response example1: {
                                "players": [
                                    {
                                        "id": "147ff90f-9988-45f3-bf39-c98d9fc48e3a",
                                        "ind_player": 0,
                                        "name": "name1"
                                    },
                                    {
                                        ...
                                    },
                                    {
                                        "id": "d8cc0522-5389-4d15-9f2c-9c377b6260df",
                                        "ind_player": 4,
                                        "name": "name5"
                                    }
                                ]
                            }
       - payload example2: {
                               "status": "unsend"
                           }
       - response example2: {
                                "request": "succeeded"
                            }
  ```
  - Send new vote
  ```bash
       - method: POST
       - route: /<game_id>/vote
       - payload example1: {
                               "vote": ["SUCCESS", "FAIL"]
                           }
       - response example1: {
                                "result": "FAIL",
                                "vote": [
                                    "FAIL",
                                    "SUCCESS"
                                ]
                            }
       - payload example2: {
                               "vote": ["SUCCESS", "SUCCESS"]
                           }
       - response example2: {
                                "result": "SUCCESS",
                                "vote": [
                                    "SUCCESS",
                                    "SUCCESS"
                                ]
                            } 
  ```

