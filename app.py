from flask import Flask, render_template, request, redirect, url_for,jsonify
import csv
from flask_mail import Mail, Message

app = Flask(__name__)

# Configure Flask-Mail for sending emails via Gmail SMTP
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'rathinatarajan23@gmail.com'
app.config['MAIL_PASSWORD'] = 'sweetrathi'

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    # Get form data
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone_number = request.form['phone_number']
    dob = request.form['dob']
    department = request.form['department']
    academic_year = request.form['academic_year']

    # Save data to CSV
    with open('student_data.csv', 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([first_name, last_name, email, phone_number, dob, department, academic_year])

    # # Send confirmation email
    # msg = Message('Registration Confirmation', sender='your_email@gmail.com', recipients=[email])
    # msg.body = f'Dear {first_name},\n\nYou have been successfully registered.'
    # #mail.send(msg)

    return redirect(url_for('index'))

# @app.route('/student-details', methods=['GET', 'POST'])
# def student_details():
#     if request.method == 'POST':
#         email_to_search = request.form['email_to_search']
#         student_data = []
#
#         # Search for student data in the CSV
#         with open('student_data.csv', 'r') as csvfile:
#             csv_reader = csv.reader(csvfile)
#             for row in csv_reader:
#                 if row[2] == email_to_search:
#                     student_data = row
#                     break
#
#         return render_template('index.html', student_data=student_data)
#     return render_template('index.html')

@app.route('/student-details', methods=['GET'])
def get_student_details():
    # Get the email parameter from the request
    email_to_search = request.args.get('email')

    # Search for student details by email
    with open('student_data.csv', 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                for row in csv_reader:
                    if row[2] == email_to_search:
                        student_data = row
                        break

    student_details = None
    for student in student_data:
        if student['email'] == email_to_search:
            student_details = student
            break

    if student_details:
        return jsonify(student_details)
    else:
        return jsonify({"error": "Student not found"})

if __name__ == '__main__':
    app.run(debug=True)
