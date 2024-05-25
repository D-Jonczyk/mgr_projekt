from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:root@localhost/mydatabase'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db = SQLAlchemy(app)

    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(80), nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)

        def __repr__(self):
            return f'<User {self.name}>'

        def serialize(self):
            return {
                'id': self.id,
                'name': self.name,
                'email': self.email
            }

    with app.app_context():
        db.create_all()

    @app.route('/user', methods=['POST'])
    def add_user():
        data = request.json
        new_user = User(name=data['name'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.serialize()), 201

    @app.route('/user/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        user = User.query.get(user_id)
        if user:
            return jsonify(user.serialize())
        return jsonify({'message': 'User not found'}), 404

    @app.route('/user/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        user = User.query.get(user_id)
        if user:
            data = request.json
            user.name = data['name']
            user.email = data['email']
            db.session.commit()
            return jsonify(user.serialize())
        return jsonify({'message': 'User not found'}), 404

    @app.route('/user/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'User deleted'})
        return jsonify({'message': 'User not found'}), 404

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=8080)
