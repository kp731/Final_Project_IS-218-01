import simplejson as json
from flask import request, Response, redirect, make_response, url_for
from flask import render_template
from flask import current_app as app
from app.app import mysql
from application.home.forms import ContactForm
from flask import Blueprint
from datetime import datetime as dt
from flask import current_app as app
from .application.home.models import db, User

#Blueprint Configuration
home_bp = Blueprint(
    'home_dp', __name__,
    template_folder='templates'
)
@app.route('/', methods=['GET'])
def user_records():
    """Create a user via query string parameters."""
    username = request.args.get('user')
    email = request.args.get('email')
    if username and email:
        existing_user = User.query.filter(
            User.username == username or User.email == email
        ).first()
        if existing_user:
            return make_response(
                f'{username} ({email}) already created!'
            )
        new_user = User(
            username=username,
            email=email,
            created=dt.now(),
            bio="In West Philadelphia born and raised, \
            on the playground is where I spent most of my days",
            admin=False
        )  # Create an instance of the User class
        db.session.add(new_user)  # Adds new User record to database
        db.session.commit()  # Commits all changes
        redirect(url_for('user_records'))
    return render_template(
        'users.jinja2',
        users=User.query.all(),
        title="Show Users"
    )
@app.route('/', methods=['GET'])
def create_user():
    """Create a user."""
    ...
    return render_template(
        'users.jinja2',
        users=User.query.all(),
        title="Show Users"
    )
# Blueprint Configuration
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates'
)

@home_bp.route('/', methods=['GET'])
def index():
    user = {'username': "Kartavya's Project"}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM airtravel')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, travels=result)


@home_bp.route('/view/<int:travel_id>', methods=['GET'])
def record_view(travel_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM airtravel WHERE id=%s', travel_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', travel=result[0])


@home_bp.route('/edit/<int:travel_id>', methods=['GET'])
def form_edit_get(travel_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM airtravel WHERE id=%s', travel_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', travel=result[0])


@home_bp.route('/edit/<int:travel_id>', methods=['POST'])
def form_update_post(travel_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Month'), request.form.get('Column_1958'), request.form.get('Column_1959'),
                 request.form.get('Column_1960'), travel_id)
    sql_update_query = """UPDATE airtravel t SET t.Month = %s, t.Column_1958 = %s, t.Column_1959 = %s, t.Column_1960 = 
    %s  WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@home_bp.route('/travel/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Person Form')


@home_bp.route('/travel/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Month'), request.form.get('Column_1958'), request.form.get('Column_1959'),
                 request.form.get('Column_1960'))
    sql_insert_query = """INSERT INTO airtravel (Month,Column_1958,Column_1959,Column_1960) VALUES (%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@home_bp.route('/delete/<int:airtravel_id>', methods=['POST'])
def form_delete_post(airtravel_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM airtravel WHERE id = %s """
    cursor.execute(sql_delete_query, airtravel_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@home_bp.route('/api/v1/travel', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM airtravel')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@home_bp.route('/api/v1/travel/<int:travel_id>', methods=['GET'])
def api_retrieve(travel_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM airtravel WHERE id=%s', travel_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@home_bp.route('/api/v1/travel/', methods=['POST'])
def api_add() -> str:
    content = request.json
    cursor = mysql.get_db().cursor()
    inputData = (content['Month'], content['Column_1958'], content['Column_1959'], content['Column_1960'])
    sql_insert_query = """INSERT INTO airtravel(Month,Column_1958,Column_1959,Column_1960) VALUES (%s, %s,%s, %s)"""
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@home_bp.route('/api/v1/travel/<int:travel_id>', methods=['PUT'])
def api_edit(travel_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['Month'], content['Column_1958'], content['Column_1959'], content['Column_1960'], travel_id)
    sql_update_query = """UPDATE airtravel t SET t.Month=%s, t.Column_1958=%s, t.Column_1959=%s, t.Column_1960=%s WHERE t.id = %s"""
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@home_bp.route('/api/travel/<int:travel_id>', methods=['DELETE'])
def api_delete(travel_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM airtravel WHERE id=%s"""
    cursor.execute(sql_delete_query, travel_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@home_bp.route('/contact', methods = ['GET', 'POST'])
def contact():
    form = ContactFrom()
    if form.validate_on_submit():
        return redirect("/", code=302)
    return render_template("contact.html", form=form)

@home_bp.errorhandler(404)
def not_found():
    """Page not found."""
    return make_response(
        'SORRY. THIS PAGE IS NOT FOUND.',
        404
     )

@home_bp.errorhandler(400)
def bad_request():
    """Bad request."""
    return make_response(
        'BAD REQUEST! THIS SERVER DOES NOT SUPPORT YOUR REQUEST.',
        400
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)