from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash
from DAL import DatabaseAccessLayer

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your-secret-key-here'  # Required for flash messages

# Initialize database access layer
dal = DatabaseAccessLayer()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/resume')
def resume():
    return render_template('resume.html')


@app.route('/projects')
def projects():
    projects = dal.get_all_projects()
    return render_template('projects.html', projects=projects)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle form submission
        first_name = request.form.get('firstName', '')
        last_name = request.form.get('lastName', '')
        email = request.form.get('email', '')
        message = request.form.get('message', '')
        
        # Basic validation
        if first_name and last_name and email:
            flash('Thank you for your message!', 'success')
            return redirect(url_for('thankyou'))
        else:
            flash('Please fill in all required fields.', 'error')
    
    return render_template('contact.html')


@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        image_filename = request.form.get('image_filename')
        
        if title and description and image_filename:
            dal.add_project(title, description, image_filename)
            flash('Project added successfully!', 'success')
            return redirect(url_for('projects'))
        else:
            flash('All fields are required!', 'error')
    
    return render_template('add_project.html')


@app.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    # Check if project exists
    if not dal.project_exists(project_id):
        flash('Project not found!', 'error')
        return redirect(url_for('projects'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        image_filename = request.form.get('image_filename')
        
        if title and description and image_filename:
            dal.update_project(project_id, title, description, image_filename)
            flash('Project updated successfully!', 'success')
            return redirect(url_for('projects'))
        else:
            flash('All fields are required!', 'error')
    
    # Get project data for pre-filling the form
    project = dal.get_project_by_id(project_id)
    return render_template('edit_project.html', project=project)


@app.route('/delete_project/<int:project_id>')
def delete_project(project_id):
    if dal.project_exists(project_id):
        dal.delete_project(project_id)
        flash('Project deleted successfully!', 'success')
    else:
        flash('Project not found!', 'error')
    
    return redirect(url_for('projects'))


@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')


# Static asset routes (css, images, script.js)
@app.route('/css/<path:filename>')
def css(filename: str):
    return send_from_directory('static/css', filename)


@app.route('/images/<path:filename>')
def images(filename: str):
    return send_from_directory('static/images', filename)


@app.route('/script.js')
def script_js():
    return send_from_directory('static/js', 'script.js')


if __name__ == '__main__':
    import os
    # Use environment variables for Docker compatibility
    debug_mode = os.environ.get('FLASK_ENV', 'development') == 'development'
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    app.run(host=host, port=port, debug=debug_mode)


