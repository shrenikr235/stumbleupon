# StumbleUpon
StumbleUpon lets you create and discover chat rooms on a specific topic. See live conversations and participants, search for rooms, topics and users to discover like-minded people.

## Installation
Assuming you have Python 3.6+ and pip installed already:

  - Clone the project
  ```bash
  git clone https://github.com/shrenikr235/stumbleupon.git
  ```
  - Install virtualenv
  ```bash
  pip install virtualenv
  ```
  - Create a virtual environment **"env"** inside the project folder
  ```bash
  cd stumbleupon
  virtualenv env
  ```
  - Activate the virtual environment
  ```bash
  cd env\Scripts\
  .\Activate.bat
  ```
  - Install project requirements 
  ```bash
  cd ..\..\stumbleupon
  pip install -r requirements.txt
  ```
  - Run server
  ```bash
  python manage.py runserver
  ```
  - You should now see the project running on **"localhost:8000"**
