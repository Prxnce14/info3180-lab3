from app import app
from flask import render_template, request, redirect, url_for, flash
from app import mail 
from flask_mail import Message



# When using Flask-WTF we need to import the Form Class that we created in forms.py
from .forms import ContactForm


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Nicholas Joiles")


@app.route('/tester-form', methods = ['GET', 'POST'])
def tester():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        message = request.form['message']

        return render_template('results.html',
                                firstname=firstname,
                                lastname=lastname,
                                email=email,
                                message=message)

    return render_template('tester.html')

@app.route('/contact/', methods = ['GET', 'POST' ])
def contact():

    joiles_form = ContactForm()
    # This shows the debug message in your development server
    app.logger.debug(joiles_form)
    if request.method == 'POST':
        #This function validate_on_submit() checks if the generated string matches what is has in it's session 
  
        if joiles_form.validate_on_submit():
            # Note the difference when retrieving form data using Flask-WTF
            # Here we use joiles_form.name instead of request.form['firstname']
            alias = joiles_form.name.data
            elec_mail =  joiles_form.email.data
            subs = joiles_form.subject.data
            sms =  joiles_form.message.data

            msg = Message(subs,  
            sender=(alias, elec_mail), 
            recipients=["to@example.com"]) 
            msg.body = sms 
            mail.send(msg)

            flash('Completed', 'success')
            return redirect(url_for('home'))
            #This return is to improves user experience. gives the user feedback based on form completed.
            # return render_template('results.html', name = alias,
            #                                         email = elec_mail,
            #                                         subj = subs,
            #                                         mess = sms)
        flash_errors(joiles_form)
    
    """Render the website's contact page"""
    #This return Displays the form if the method is a GET request 
    return render_template('contact.html', temp = joiles_form )
    



###
# The functions below should be applicable to all Flask apps.
###


# Flash errors from the form if validation fails
# This loops over all form errors in the form and flash the error when the page is reloaded 
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
