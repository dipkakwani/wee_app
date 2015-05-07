# WEE

Wee is a social networking site built with Django. Live preview at http://dipkakwani.pythonanywhere.com/newsfeed/ .
### Version
1.0.0
### Feaures
 - Newsfeed
 - Timeline
 - Search
 - Groups
 - Post
 - Likes, shares, comments

### Installation

You need [Python (2.7)](https://www.python.org/downloads/), [Django (1.7.4)](https://www.djangoproject.com/download/), [MySQL](https://dev.mysql.com/downloads/) and MySQL-Python connector:

```sh
$ pip install mysql-python django
```
#####Building

```sh
$ git clone https://github.com/dipkakwani/wee_app.git
```
Create a database named wee (any other name will also work) from MySQL. Update the database configuration in wee_app/src/wee/settings.py.
```sh
$ cd wee_app/src
$ python manage.py syncdb
$ python manage.py runserver
```
You can see the live demo at 127.0.0.1:8000/home

### Development

Want to contribute? Great!
You can pick one of the Todo task and send a pull request. In case you have a new idea, just raise an issue and start working on the idea and then send a pull request.

### Todo's
*=Challenging
 - Modify design of home page template
 - Add AJAX for likes, comments and shares for a post
 - Complete documentation
 - Write Tests
 - Add friend recommendation*
 - Add real time notifications*
 - Add messages*

##License
----
MIT