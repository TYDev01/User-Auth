# Django Authentication System with Password Reset
<hr>

This project is a basic authentication system built using Django. It includes features like user registration, login, logout, password reset via email, and validation checks on user data. It also handles common errors like incorrect login details or expired password reset links.

## Features

- **User Registration**: Allows users to create an account with their first name, last name, username, email, and password.
- **User Login**: Users can log in using their username and password.
- **User Logout**: Users can log out of the system.
- **Forgot Password**: Users can request a password reset link, which is sent to their email.
- **Password Reset**: Users can reset their password using the link sent to their email.
- **Form Validation**: Checks for common errors like username/email already taken, passwords that don’t match, or weak passwords.

## Views Overview

### 1. `home_view`
- **URL**: `/`
- **Description**: Renders the homepage. Only accessible if the user is logged in.
- **Decorator**: `@login_required` ensures that the user is authenticated before accessing this view.

### 2. `signup_view`
- **URL**: `/register/`
- **Description**: Handles user registration. It checks if the username or email is already in use, validates password confirmation, and ensures the password is at least 8 characters long. On successful registration, the user is redirected to the login page.

### 3. `login_view`
- **URL**: `/login/`
- **Description**: Authenticates the user using their username and password. If successful, the user is logged in and redirected to the homepage. If the login fails, an error message is shown.

### 4. `logout_view`
- **URL**: `/logout/`
- **Description**: Logs the user out and redirects them to the homepage.

### 5. `forgot_password_view`
- **URL**: `/forgot/`
- **Description**: Allows users to request a password reset by providing their email. If the email exists in the system, a reset link is sent to the user's email. An error message is shown if the email is not found.

### 6. `password_reset_sent`
- **URL**: `/password-reset-sent/<reset_id>/`
- **Description**: Displays a confirmation page when the reset email is sent. If the reset ID is valid, a success message is shown; otherwise, an error message is displayed.

### 7. `password_reset`
- **URL**: `/reset-password/<reset_id>/`
- **Description**: Handles the password reset process. Users provide a new password and confirm it. The system ensures that the reset link hasn’t expired, passwords match, and the new password is strong.

### Error Handling and Validation
- Validates email and username during signup to ensure uniqueness.
- Ensures the password is at least 8 characters long and that both passwords match during registration and reset.
- Catches exceptions like `User.DoesNotExist` for forgotten password or invalid reset links.
- Handles expired reset links by deleting them and showing a relevant message.

## Models

### 1. **PasswordReset**
- **Fields**:
  - `user`: A foreign key to the `User` model, representing the user requesting a password reset.
  - `reset_id`: A unique ID to identify the reset link.
  - `created_on`: A timestamp indicating when the reset request was made.

- **Description**: This model stores reset IDs and is used for password reset functionality. It tracks reset requests and ensures the reset links expire after 10 minutes.

## Setup Instructions

### 1. Clone the repository:
```bash
git clone https://github.com/TYDev01/User-Auth.git
cd your-repository-link

### Install dependencies
- pip install -r requirements.txt

### Run migrations:
- python manage.py migrate


### Run the development server
- python manage.py runserver

### Access the application
- Open your browser and go to http://127.0.0.1:8000/