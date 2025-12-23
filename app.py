from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///christmas_trees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 数据库模型
class ChristmasTree(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_name = db.Column(db.String(100), nullable=False, unique=True)
    tree_data = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<ChristmasTree {self.child_name}>'

# 创建数据库
with app.app_context():
    db.create_all()

# 路由
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form['username']
    password = request.form['password']
    if username == 'test' and password == 'admin':
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid credentials. Please try again.')
        return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/generate-tree', methods=['POST'])
def generate_tree():
    child_name = request.form['child_name']
    # 检查是否已存在该姓名的圣诞树
    existing_tree = ChristmasTree.query.filter_by(child_name=child_name).first()
    if existing_tree:
        return jsonify({'success': True, 'tree_data': existing_tree.tree_data, 'new': False})
    else:
        # 生成新的圣诞树数据（这里使用简单的JSON结构）
        tree_data = {
            'child_name': child_name,
            'tree_type': 'classic',
            'decorations': ['star', 'ornaments', 'lights']
        }
        # 保存到数据库
        new_tree = ChristmasTree(child_name=child_name, tree_data=str(tree_data))
        db.session.add(new_tree)
        db.session.commit()
        return jsonify({'success': True, 'tree_data': str(tree_data), 'new': True})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
