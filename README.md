# [Blog Restful API](https://blog-osama-mohamed-django.herokuapp.com) By Django

[<img src="https://www.djangoproject.com/s/img/logos/django-logo-negative.png" width="200" title="Blog Restful API" >](https://blog-osama-mohamed-django.herokuapp.com)
[<img src="https://www.mysql.com/common/logos/logo-mysql-170x115.png" width="150" title="Blog Restful API" >](https://blog-osama-mohamed-django.herokuapp.com)


## For live preview :
> [Blog Restful API](https://blog-osama-mohamed-django.herokuapp.com)


## Blog website contains:
### 3 Apps :
    1. Account
    2. Article
    3. Comment
* User register 
* User login
* User logout 
* Add article by admin
* Update article by admin
* Delete article by admin
* Article number of views
* Article expected read time
* Add comment by authenticated user only
* Delete comment by the authenticated owner only
* Thread comments


## Usage :
### Run project by :

``` python

# change database connection information in settings.py DATABASES default values with your info then run 

1. python manage.py migrate

2. python manage.py runserver

# if you want to manage to project just create super user account by :

3. python manage.py createsuperuser

```

That's it.

## Done :

Now the project is running at `http://localhost:8000` and your routes is:


| Route                                                      | HTTP Method 	 | Description                           	        |
|:-----------------------------------------------------------|:--------------|:-----------------------------------------------|
| {host}       	                                             | GET       	   | Home page                                      |
| {host}/admin/  	                                           | GET      	   | Admin control panel                        	  |
| {host}/accounts/register/                                  | POST      	   | User register           	                      |
| {host}/accounts/login/                                     | POST      	   | User login           	                        |
| {host}/accounts/logout/                                    | GET      	   | User logout           	                        |
| {host}/articles/                                           | POST      	   | Articles page          	                      |
| {host}/articles/category/{category}/                       | GET      	   | Search articles by category          	        |
| {host}/articles/article/{slug}/                            | GET & POST	   | Article detail and add comment                 |
| {host}/comments/{id}/                                      | POST      	   | Thread comment           	                    |
| {host}/comments/{id}/delete/                               | POST      	   | Delete comment           	                    |
| {host}/about_me/                                           | GET      	   | About me page           	                      |


| API Route                                                  | HTTP Method 	 | Description                           	        |
|:-----------------------------------------------------------|:--------------|:-----------------------------------------------|
| {host}/api/accounts/register/                              | POST      	   | User register                          	      |
| {host}/api/accounts/login/                                 | POST      	   | User login           	                        |
| {host}/api/articles/                                       | POST      	   | Articles page          	                      |
| {host}/api/articles/category/{category}/                   | GET      	   | Search articles by category          	        |
| {host}/api/articles/article/{slug}/                        | GET      	   | Article detail           	                    |
| {host}/api/comments/add_comment/{id}/                      | POST      	   | Add comment           	                        |
| {host}/api/comments/{id}/                                  | POST      	   | Thread comment           	                    |
| {host}/api/comments/{id}/delete/                           | DELETE      	 | Delete comment           	                    |


For detailed explanation on how project work, read the [Django Docs](https://docs.djangoproject.com/en/1.11/) and [MySQLDB Docs](https://dev.mysql.com/doc/)

## Developer
This project made by [Osama Mohamed](https://www.facebook.com/osama.mohamed.ms)

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT)
