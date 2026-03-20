from models import User

# This function creates a new user with the provided username, email, and password.
def create_user(username, email, password):
    
    # Here we create a new user instance
    user = User(username=username, email=email, password=password)

    # Here we save the user to the database
    user.save()

    # After saving the user, we return a success message
    return {"message": "User created successfully"}