# Django Conference Management System

This Django project is a conference management system that allows users to manage participants, departments, staff, sessions, and attendance for a conference.

## Features

- Admin panel for managing various aspects of the conference
- User authentication and login functionality
- CRUD operations for managing participants, departments, staff, sessions, and subjects
- Notification system for sending notifications to staff and participants
- Attendance tracking for staff and participants
- Leave management for staff and participants

## Installation

1. Clone the repository:
git clone https://github.com/your-username/django-conference-management.git

markdown
Copy code

2. Install the required dependencies:
pip install -r requirements.txt

markdown
Copy code

3. Set up the database:
- Configure the database settings in the project's `settings.py` file.
- Migrate the database:
  ```
  python manage.py migrate
  ```

4. Run the development server:
 python manage.py runserver

5. Access the application in your web browser at `http://localhost:8000/`

## Usage

- Visit the admin panel at `http://localhost:8000/admin/` to manage the conference data.
- Staff members can access their home page at `http://localhost:8000/Staff/Home`.
- Participants can access their home page at `http://localhost:8000/Participant/Home`.

## Contributing

Contributions are welcome! If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your forked repository.
5. Submit a pull request to the main repository.

## License

This project is licensed under the @hassan-abidar.

LOGIN : 
![image](https://github.com/hassan-abidar/Conference_management/assets/71274391/e214c2e6-e03f-4c10-8f5b-e4c627aad10c)
HOME : 
![image](https://github.com/hassan-abidar/Conference_management/assets/71274391/7a252d45-0848-4f29-a7de-978c3eab5611)
STAFF HOME : 
![image](https://github.com/hassan-abidar/Conference_management/assets/71274391/56b60f29-6beb-4327-91fb-bafbf0b0e42a)
PARTICIPANT HOME : 
![image](https://github.com/hassan-abidar/Conference_management/assets/71274391/92435aa1-d660-47e9-8776-093a19fb173d)




