from flask import Flask, jsonify, request
from getTwitterImage import get_user_from_user_name, get_images


app = Flask(__name__)

@app.route('/api/getData', methods=['GET'])
def search_keyword():
	if request.method == 'GET':
		users = request.args.get('users')
		if not users:
			return jsonify({"status": "error", "message": "なんか文字入れて"})
		
		users = users.split(",")
		tw_users = []

		for user in users:
			tw_users.append(get_user_from_user_name(user))

		res = get_images(tw_users)

		return jsonify({"data" : res, "status": "ok"})
	else:
		return jsonify({"status": "error", "message": "POST やん..."})

@app.route('/', methods=['GET'])
def test():
	return jsonify({"data": "test responce."})

@app.after_request
def after_request(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

if __name__ == "__main__":
	app.run(debug=True)

