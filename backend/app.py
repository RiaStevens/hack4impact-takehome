from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.
    
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)

@app.route("/shows", methods=['GET'])
def get_all_shows():
	minEpisodes = int(request.args.get('minEpisodes', None))
	allShows = db.get('shows')
	if minEpisodes == None:
		return create_response({"shows": allShows})
	validShows = [show for show in allShows if show['episodes_seen'] >= minEpisodes]
	return create_response({"shows": validShows})

@app.route("/shows/<id>", methods=['DELETE'])
def delete_show(id):
    if db.getById('shows', int(id)) is None:
        return create_response(status=404, message="No show with this id exists")
    db.deleteById('shows', int(id))
    return create_response(message="Show deleted")


# TODO: Implement the rest of the API here!
@app.route("/shows/<id>", methods=['GET'])
def get_show_by_id(id):
	show = db.getById('shows', int(id))
	if show is None:
		return create_response(status=404, message="No show with this id exists")
	return create_response(show)

@app.route("/shows", methods=["POST"])
def post_show():
	show_req = request.get_json()
	if not "name" in show_req.keys():
		return create_response(status=422, message="Show could not be created. Please include a name within the body.")
	if not "episodes_seen" in show_req.keys():
		return create_response(status=422, message="Show could not be created. Please include 'episodes_seen' within the body.")
	show_req = {key: show_req[key] for key in ['name', 'episodes_seen']}
	newShow = db.create('shows', show_req)
	return create_response(newShow, status=201) 

@app.route("/shows/<id>", methods=['PUT'])
def put_show(id):
	show_req = request.get_json()
	show_req = {key: show_req[key] for key in show_req.keys() & ['name', 'episodes_seen']}
	updatedShow = db.updateById('shows', int(id), show_req)
	if updatedShow == None:
		return create_response(status=404, message=f"No show with id {id} could be found.")
	return create_response(updatedShow, status=201)

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(port=8080, debug=True)
