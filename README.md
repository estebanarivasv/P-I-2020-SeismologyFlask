# :earth_americas: Seismology Proyect

Subject: "Programación I"
<br><br>
In 2020, I made a project for a subject called "Programación I" (Programming) at Universidad de Mendoza. 

We worked with the Flask framework (including extensions) and we also learned about how do RESTFUL APIs work with WEB clients.
<br><br>

# :clipboard: Table of Contents
- [:pencil: Description](#-pencil--description)
      - [User-case diagram](#user-case-diagram)
      - [UML Classes diagram](#uml-classes-diagram)
- [:computer: Developing stages](#-computer--developing-stages)
      - [(API) Phase 1: Client–server model](#-api--phase-1--client-server-model)
      - [(API) Phase 2: Data storage](#-api--phase-2--data-storage)
      - [(API) Phase 3: Authentication with JWT and email sending](#-api--phase-3--authentication-with-jwt-and-email-sending)
      - [(WEB) Phase 4: Routes and templates](#-web--phase-4--routes-and-templates)
      - [(WEB) Phase 5: Forms](#-web--phase-5--forms)
      - [(WEB) Phase 6: Sessions and routes permissions](#-web--phase-6--sessions-and-routes-permissions)
- [:information_source: Installation and usage for both API and Web client](#-information-source--installation-and-usage-for-both-api-and-web-client)
      - [1 - Define the environment variables in the .env file](#1---define-the-environment-variables-in-the-env-file)
      - [2 - Install dependencies](#2---install-dependencies)
      - [3 - Launch Flask application](#3---launch-flask-application)
      - [4 - Import requests file for the api in Insomnia or simply launch the web client](#4---import-requests-file-for-the-api-in-insomnia-or-simply-launch-the-web-client)


# :pencil: Description
The aim of this project is simulating a Seismology Institute center where the main actors of the system are seisms, seismologists and the sensors.
<br><br>
@andrea.navarro, my teacher, came up with this idea. She learnt us how do the main system structure works and our job was adapt the project to the requirements.
<br><br>
The project incluides the following items:
- Make requests to sensos.
- Save/modify seisms data (basic CRUD methods) with HTTP requests
- Send emails to administrators of sensors that are not working
- Web and api integration

#### User-case diagram
Here in this scheme, I described the general behaviour of the system. 
Basically we've desplayed the system and three different user types: the administrators, the seismologists and the analists or all the rest of the organization.

Every one of them has specific tasks:<br>
**Administrators** are able to:
- Assign sensors to seismologists.
- Have access to existent sensors: modify, activate or deactivate.
- Register new users.

**Seismologists** can:
- List left seisms to validate.
- List assigned sensors.
- Modify unverified seisms data. 
  - If it is an excessive amount of data to verify, they can download it. 
  - If there are not mistakes left, the users can validate the seism.

**Analists** (or any other institute member) are be able to:
- Access verified seisms.
- Filter and download the sensors data in a CSV or ZIP file.
  
The **system** must:
- Send notifications to administrators whenever any active sensor stops working.

<img src="https://i.ibb.co/VLqc45n/usecase-diag.png"  width="800">

#### UML Classes diagram
Here there are the system classes depicted. We have three main tables: users, seisms and sensors

<img src="https://i.ibb.co/PrvMvqY/uml.png"  width="800">

# :computer: Developing stages

Flask framework natively works with routing, debugguing and WSGI (Web Server Gateway Interface). To make other things work, like for example: auth, you will need to include some extensions.
<br><br>
Basic components layout:
<img src="https://docs.microsoft.com/es-es/dotnet/architecture/microservices/architect-microservice-container-applications/media/direct-client-to-microservice-communication-versus-the-api-gateway-pattern/custom-service-api-gateway.png"  width="800">

#### (API) Phase 1: Client–server model
Flask and API Rest introduction
#### (API) Phase 2: Data storage
SQLAlchemy (ORM: Object-Relational Mapping), modelos
#### (API) Phase 3: Authentication with JWT and email sending
Flask Mail (MTA: Mail Transport Agent), Flask JWT
#### (WEB) Phase 4: Routes and templates
Blueprints, Jinja2, Bootstrap library, macros, stylesheets
#### (WEB) Phase 5: Forms
Flask-WTF, form models
#### (WEB) Phase 6: Sessions and routes permissions
Flask-Login

# :information_source: Installation and usage for both API and Web client
Steps to follow in order to get the Flask app up and running

#### 1 - Define the environment variables in the .env file
You can rename the .env-example file to .env

:exclamation: Remember you need to declare all the variables including the database path. You can know where you are standing and declare them as the database path with these sentences:

#### 2 - Install dependencies
To begin the instalation of libraries and the frameworks needed: `./install.sh`

#### 3 - Launch Flask application
To get the app running: `./boot.sh`

#### 4 - Import requests file for the api in Insomnia or simply launch the web client