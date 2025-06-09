from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'danmu.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Danmu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)

with app.app_context():
    db.create_all()

# 获取所有弹幕
@app.route('/danmus', methods=['GET'])
def get_danmus():
    danmus = Danmu.query.all()
    return jsonify({'list': [{'id': d.id, 'text': d.text} for d in danmus]})

# 添加弹幕（GET + 参数 text）
@app.route('/danmus/add', methods=['GET'])
def add_danmu():
    text = request.args.get('text', '').strip()
    if text:
        new_danmu = Danmu(text=text)
        db.session.add(new_danmu)
        db.session.commit()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Empty text'}), 400

# 删除弹幕（GET + 参数 id）
@app.route('/danmus/delete', methods=['GET'])
def delete_danmu():
    id_str = request.args.get('id')
    if id_str and id_str.isdigit():
        danmu = Danmu.query.get(int(id_str))
        if danmu:
            db.session.delete(danmu)
            db.session.commit()
            return jsonify({'status': 'deleted'})
        return jsonify({'status': 'error', 'message': 'Danmu not found'}), 404
    return jsonify({'status': 'error', 'message': 'Invalid ID'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
