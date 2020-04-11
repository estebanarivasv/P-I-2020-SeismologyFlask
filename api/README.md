Steps to follow in order to get the Flask app up and running

1- Define the environment variables in the .env file. 
    You can rename the .env-example file to .env
    
    Remember you need to declare the database path. You can know where you are standing and declare them as the database path with these sentences:
    
    import os
    file_path = os.path.abspath(os.getcwd())+"/database.db"

2- Execute:
        ./install.sh 
    to begin the instalation of libraries and the frameworks needed
        ./boot.sh
    to get the app running.

3- Import requests in Insomnia v4