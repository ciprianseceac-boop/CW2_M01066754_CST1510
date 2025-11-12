import bcrypt

def hash_password(pwd):
    password_bytes = pwd.encode('utf-8')        
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)    
    return hashed.decode('utf-8')

def validate_password(pwd, hashed):
    password_bytes = pwd.encode('utf-8')
    hashed_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def register_user():
    user_name = input("Enter username: ")
    password = input("Enter password: ")  
    hashed_pwd = hash_password(password)
    with open('users.txt', 'a') as f:
        f.write(f"{user_name},{hashed_pwd}\n")
    print("user registered successfully.")

def login_user():
    user_name = input("Enter username: ")
    password = input("Enter password: ")  
    with open('users.txt', 'r') as f:
        users = f.readlines()
    for user in users:
        stored_user, stored_hashed_pwd = user.strip().split(',')
        if stored_user == user_name:
            return validate_password(password, stored_hashed_pwd)
            

def main():
    print(" Welcome to the system!")
    while True:
        print("\nPlease choose an option:")
        print("1. Register a new user")
        print("2. Login with existing user")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ").strip()
        if choice == "1":
            register_user()
        elif choice == "2":
            if login_user():
                print("Login successful!")
            else:
                print("Login failed. Invalid username or password.")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()