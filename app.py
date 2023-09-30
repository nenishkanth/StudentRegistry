import csv

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

CSV_FILE = 'student_data.csv'

# Function to get the next available user ID
def get_next_user_id():
    try:
        with open(CSV_FILE, 'r') as file:
            reader = csv.DictReader(file)
            user_ids = [int(row['user_id']) for row in reader]
            if len(user_ids) == 0:
                user_ids.append(0)
            return max(user_ids) + 1
    except FileNotFoundError:
        return 1  # If the file doesn't exist, start with 1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    # Get input datadata = {dict: 7} {'academic_year': '2022', 'department': 'Computer Science', 'dob': '2000-11-05', 'email': 'ezone.dk@gmail.com', 'first_name': 'Dilipkumar', 'last_name': 'Nallusamy', 'phone_number': '9600177834'}
    data = request.get_json()
    user_id = get_next_user_id()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    phonenumber = data.get('phone_number')
    dob = data.get('dob')
    department = data.get('department')
    academicyear = data.get('academic_year')

    # Save data to CSV
    with open(CSV_FILE, 'a', newline='') as file:
        fieldnames = ['user_id', 'first_name', 'last_name', 'email', 'phone_number','dob','department','academic_year']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header row if the file is empty
        if file.tell() == 0:
            writer.writeheader()

        writer.writerow({
            'user_id': user_id,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone_number': phonenumber,
            'dob': dob,
            'department': department,
            'academic_year': academicyear
        })

    return jsonify({"message": "User registered successfully", "user_id": user_id}), 201

# Route for fetching user details by user ID
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # Get the user details using user Id
    test = ''
    # user_id = request.args.get('user_id')
    if user_id is None:
        return jsonify({"message": "User ID is required in the query parameters"}), 400

    try:
        with open(CSV_FILE, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row['user_id']) == int(user_id):
                    return jsonify({
                        "user_id": row['user_id'],
                        "firstname": row['first_name'],
                        "lastname": row['last_name'],
                        "email": row['email'],
                        "phonenumber": row['phone_number'],
                        "dob": row['dob'],
                        "department": row['department'],
                        "academic_year": row['academic_year']
                    })

        return jsonify({"message": "User not found"}), 404
    except FileNotFoundError:
        return jsonify({"message": "No users found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
