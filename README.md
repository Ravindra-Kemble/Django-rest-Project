# django-rest-api
A REST api written in Django

## Installation
* If you wish to run your own build, first ensure you have python globally installed in your computer. If not, you can get python [here](https://www.python.org").
* After doing this, confirm that you have installed virtualenv globally as well. If not, run this:
    ```sh
        pip install virtualenv
    ```
* Then, Git clone this repo to your PC
    ```sh
        git clone https://github.com/Ravindra-Kemble/Django-rest-Project.git
    ```

* #### Dependencies
    1. Create and fire up your virtual environment:
        ```sh
             virtualenv  venv -p python3
             venv/scripts/activate
        ```
    3. Install the dependencies needed to run the app:
        ```sh
             cd myproject
             pip install -r requirements.txt
        ```
    4. Make those migrations work
        ```sh
            python manage.py makemigrations
            python manage.py migrate
        ```

* #### Run It
    Fire up the server using this one simple command:
    ```sh
        python manage.py runserver
    ```
    You can now access the file api service on your browser by using
    ```
        http://localhost:8000/api/
    ```
    
    ### Users Endpoints

1. **User Registration**:
   - POST /api/register/
     - Request: { "username": "Robert", "email": "robert@gmai.com", "password": 1235, "password_confirm": 1235}
     - Response: { "message": "Registration successful." }

2. **User Login**:
   - POST /api/login/
     - Request: { "username": "Robert", "password": "1235"  }
     - Response: { "message": "User Logged-in", "token": "srg45s4dv68d4fs8d64c" }
    
    ### Clients Endpoints

*. **List of all Clients**:
   - GET /api/clients/
     - Response: [{
         'id' : 1,
         'client_name' : 'Nimap',
         'created_at' : '2024-10-24T11:03:55.931739+05:30',
         'created_by' : 'Karan'
     },
     {
         'id' : 2,
         'client_name' : 'Infotech',
         'created_at' : '2024-10-24T11:03:55.931739+05:30',
         'created_by' : 'Karan'
     }

]

*. **Create a new clientP**:
   - POST /api/clients/
     - Request: {'client_name' : 'company A'}
     - Response:  {
                      'id' : 3,
                      'client_name' : 'company A',
                      'created_at' : '2024-10-24T11:03:55.931739+05:30',
                      'created_by' : 'Rohit'

       }

*. **Retrieve info of a client along with projects assigned to its users**:
   - GET /api/clients/id
   - Response: {
                    'id' : 2,
                    'client_name' : 'Infotech',
                    'projects' : [{
                                       'id' : 1,
                                       'name' : 'project A'
                                    }

]
                      'created_at' : '2024-10-24T11:03:55.931739+05:30',
                      'created_by' : 'Karan'
                      'updated_at' : '2024-10-24T11:03:55.931739+05:30',

}


*. **Update info of a client**:
   - PUT /api/clients/id
   - Request: { "client_name" : "company A"  }
   - Response: {
                    'id' : 3,
                    'client_name' : 'company A',
                    'created_at' : '2019-12-24T11:03:55.931739+05:30',
                    'created_by' : 'Karan',
                    'updated_at' : '2019-12-24T11:03:55.931739+05:30'

}

*. **Delete client**:
   - DELETE /clients/:id

*. **Create a new project**
     - POST /api/clients/id/projects/
     - Request: {'project_name' : 'Project A'
                 'users' : [
                     {
                         'id' : 1,
                         'name' : 'Rohit'
                         }

]

}                         
     - Response: {
                      'id' : 3,
                      'project_name' : 'Project A',
                      'client' : 'Nimap'
                      'users' : [
                          {
                               'id' : 1,
                               'name' : 'Rohit'

  }
  ]
  'created_at' : '2019-12-24T11:03:55.931739+05:30'
  'created_by' : 'Ganesh'
}

*. **List of all projects assigned to the logged-in user**:
   - GET /api/projects/
     - Response: [
           {
               'id' : 1,
               'project_name' : 'Project A',
               'created_at' : '2019-12-24T11:03:55.931739+05:30',
               'created_by' : 'Ganesh'

} 
