from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import markdown

app = Flask(__name__)

# Database connection
conn = psycopg2.connect(
    database="myprojects",
    user="postgres",
    password="tdk2hdD!",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Create projects table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100),
        description TEXT,
        link VARCHAR(255),
        image VARCHAR(255)
    );
""")
conn.commit()

@app.route('/')
def home():
    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()
    return render_template('index.html', projects=projects)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        title = request.form['project-title']
        description = request.form['project-description']  # Markdown content
        link = request.form['project-link']
        image = request.form['project-image']
        project_id = request.form.get('project-id')
        
        if project_id:  # Update existing project
            cursor.execute("""
                UPDATE projects
                SET title = %s, description = %s, link = %s, image = %s
                WHERE id = %s
            """, (title, description, link, image, project_id))
        else:  # Add new project
            cursor.execute("""
                INSERT INTO projects (title, description, link, image)
                VALUES (%s, %s, %s, %s)
            """, (title, description, link, image))
        
        conn.commit()
        return redirect(url_for('admin'))

    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()
    return render_template('dashboard.html', projects=projects)

@app.route('/delete/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    cursor.execute("DELETE FROM projects WHERE id = %s", (project_id,))
    conn.commit()
    return redirect(url_for('admin'))

@app.route('/edit/<int:project_id>')
def edit_project(project_id):
    cursor.execute("SELECT * FROM projects WHERE id = %s", (project_id,))
    project = cursor.fetchone()
    return render_template('dashboard.html', project=project)

@app.route('/project/<int:project_id>')
def view_project(project_id):
    cursor.execute("SELECT * FROM projects WHERE id = %s", (project_id,))
    project = cursor.fetchone()
    project_html = markdown.markdown(project[2])  # Convert Markdown to HTML
    return render_template('project.html', project=project, project_html=project_html)

if __name__ == '__main__':
    app.run(debug=True)
