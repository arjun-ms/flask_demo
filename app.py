from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import flash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"id={self.id}, name='{self.name}', email='{self.email}', message='{self.message}')>"

# doing it manually
# with app.app_context():
#     db.create_all()

@app.route('/')
def index():
    return render_template('contact.html', submitted=False)

@app.route('/submit', methods=['POST'])
def submit_contact():

    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    new_contact = Contact(name=name, email=email, message=message)

    db.session.add(new_contact)
    db.session.commit()

    print("++"*20)
    print(f"New contact added: {new_contact}")
    print("++"*20)

    flash('Your record has been submitted.')

    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
