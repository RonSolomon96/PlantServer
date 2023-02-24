import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask, request, jsonify


# Use a service account.
cred = credentials.Certificate("plantitdb1-firebase-adminsdk-y2grh-c4930ddb02.json")

firebase_admin.initialize_app(cred)

db = firestore.client()


# Initialize Flask app
app = Flask(__name__)


# Define routes for CRUD operations
@app.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user with the given data.
    """
    data = request.get_json()
    user_ref = db.collection('Plants').document(data['Common_name'])
    user_ref.set(data)
    return jsonify({"message": "User created successfully."}), 201


@app.route('/users', methods=['GET'])
def read_users():
    """
    Retrieve all users from Firestore DB.
    """
    users = [doc.to_dict() for doc in db.collection('users').stream()]
    return jsonify(users), 200


@app.route('/users/<user_id>', methods=['GET'])
def read_user(user_id):
    """
    Retrieve a specific user by ID from Firestore DB.
    """
    user_doc = db.collection('users').document(user_id).get()
    if user_doc.exists:
        return jsonify(user_doc.to_dict()), 200
    else:
        return jsonify({"message": "User not found."}), 404


@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update a specific user by ID with the given data.
    """
    data = request.get_json()
    user_ref = db.collection('users').document(user_id)
    user_ref.update(data)
    return jsonify({"message": "User updated successfully."}), 200


@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a specific user by ID from Firestore DB.
    """
    user_ref = db.collection('users').document(user_id)
    user_ref.delete()
    return jsonify({"message": "User deleted successfully."}), 200


# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)


