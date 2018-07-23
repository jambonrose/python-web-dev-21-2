# Read Me

This repository contains the code for the second class in [Andrew
Pinkham]'s [Python Web Development] series, titled *Building Backend Web
Applications and APIs with Django*. The series is published by Pearson
and may be bought on [InformIT] or viewed on [Safari Books Online]. The
series is for intermediate programmers new to web development or Django.

[Andrew Pinkham]: https://andrewsforge.com
[Python Web Development]: https://pywebdev.com
[InformIT]: https://pywebdev.com/buy-21-2/
[Safari Books Online]: https://pywebdev.com/safari-21-2/

Andrew may be reached at [JamBon Software] for consulting and training.

[JamBon Software]: https://www.jambonsw.com

## Table of Contents

- [Changes Made Post-Recording](#changes-made-post-recording)
- [Technical Requirements](#technical-requirements)
- [Getting Started Instructions](#getting-started-instructions)
  - [Docker Setup](#docker-setup)
  - [Local Setup](#local-setup)
- [Walking the Repository](#walking-the-Repository)
- [Extra Problems](#extra-problems)
- [Testing the Code](#testing-the-code)
- [Deploying the Code](#deploying-the-code)

## Changes Made Post-Recording

1. For security purposes a commit has been added at the end of every
   branch which secures the application using basic login functionality.
   The content of that commit will be discussed in the third Python Web
   Development class - I hope you're looking forward to it!
2. Test dependencies have been included in all branches, so that the
   Docker image may be built once and used on all branches.
3. The Docker image has been updated to use Python 3.7.1 (from 3.7.0)
4. Pre-Commit and Black have been updated to more recent versions
5. The site uses Django's `StaticFilesStorage` instead of the
   `ManifestStaticFilesStorage` shown in Lesson 7 by error.

[🔝 Up to Table of Contents](#table-of-contents)

## Technical Requirements

- [Python] 3.6+ (with SQLite3 support)
- [pip] 10+
- a virtual environment (e.g.: [`venv`], [`virtualenvwrapper`])
- Optional:
  - [Docker] 17.12+ with [Docker-Compose] (or—if unavailable—[PostgreSQL] 10)


[Python]: https://www.python.org/downloads/
[pip]: https://pip.pypa.io/en/stable/installing/
[`venv`]:https://docs.python.org/3/library/venv.html
[`virtualenvwrapper`]: https://virtualenvwrapper.readthedocs.io/en/latest/install.html
[Docker]: https://www.docker.com/get-started
[Docker-Compose]: https://docs.docker.com/compose/
[PostgreSQL]: https://www.postgresql.org/

All other technical requirements are installed by `pip` using the
requirement files included in the repository. This includes [Django 2.1].

[Django 2.1]: https://docs.djangoproject.com/en/2.1/

[🔝 Up to Table of Contents](#table-of-contents)

## Getting Started Instructions

For a full guide to using this code please refer to Lesson 2 of the
class. This lesson demonstrates how to get started locally as well as
how to use the Docker setup.

If you are **unable to run Docker** on your machine skip to the [Local
Setup](#local-setup) section.

### Docker Setup

The use of Docker images allows us to avoid installing all of our
dependencies—including PostgeSQL—locally. Furthermore, as discussed
in the videos, it helps with parity between our development and
production environments.

Our Docker containers expect the existence of an environment file. To
generate it on *nix systems please invoke the `build_docker_env.sh`
script.

```shell
./build_docker_env.sh
```

On Windows please invoke the batch file.

```
build_docker_env
```

If you run into problems please refer to the videos for why we use this
and what is needed in the event these scripts do not work.

To run the Docker containers use the command below.

```shell
docker-compose up
```

If you wish to run the servers in the background use the `-d`
(**d**etached) flag, as demonstrated below.

```shell
docker-compose up -d
```

To turn off the server use Control-C in the terminal window. If running
in the background use the command below.

```shell
docker-compose down
```

To remove all of the assets created by Docker to run the server use the
command below.

```shell
docker-compose down --volumes --rmi local
```

The `--volumes` flag may be shortened to `-v`.

[🔝 Up to Table of Contents](#table-of-contents)

### Local Setup

Use `pip` to install your development dependencies.

```console
$ python3 -m pip install -r requirements/development.txt
```

If you have checked out to an earlier part of the code note that you
will need to use `requirements.txt` instead of
`requirements/development.txt`.

You will need to define the`SECRET_KEY` environment variable. If you
would like to use PostgreSQL locally you will need to set
`DATABASE_URL`.

```shell
export SECRET_KEY=`head -c 75 /dev/urandom | base64 | tr -dc 'a-zA-Z0-9' | head -c 50`
# replace the variables in <> below
export DATABASE_URL='postgres://<USER>:<PASSWORD>@<SERVER>:5432/<DB_NAME>'
```

Please be advised that if you are running code in Lesson 2 you should
expect to see errors. Lesson 2 changes the database structure but
avoids making migrations until the very last moment. What's more,
database settings change in Lesson 2.8. Errors are therefore normal!

[🔝 Up to Table of Contents](#table-of-contents)

## Walking the Repository

To make perusing the code in this repository as simple as possible the
project defines its own `.gitconfig` file with custom commands
(aliases).

To enable the commands you must first point your local git
configuration at the file provided. Either of the two commands below
should work.

```shell
# relative path
git config --local include.path "../.gitconfig"
# absolute path - *nix only!
git config --local include.path "`builtin pwd`/.gitconfig"
```

This will enable the following git commands:

- `git next`: Move to the next example/commit
- `git prev`: Move to the previous example/commit
- `git ci`: shortcut for `git commit`
- `git co`: shortcut for `git checkout`
- `git st`: shortcut for `git status`
- `git ll`: shortcut for `git log --oneline`

These commands can be used on any of the two branches in this
repository, which are listed below.

- `class_material`: contains the code and material seen in the videos,
  as well as solutions to exercises mentioned in Lessons 5 and 6 (see
  section below to review).
- `with_tests`: includes material above, as well as the tests used by
  me to verify the code works

[🔝 Up to Table of Contents](#table-of-contents)

## Extra Problems

At the end of Lessons 5 and 6 I leave you with several optional
exercises.

In Lesson 5:

- Create new `NewsLink` objects in API via POST method (Consider
  [`ViewSets`] vs [`APIView`] subclasses)
- Simplify `PostSerializer` with [`HyperlinkedRelatedField`] (as seen on
  `NewsLinkSerializer`)
- Use [`ViewSets`] and Routers to simplify Post handling in API

[`ViewSets`]: https://www.django-rest-framework.org/api-guide/viewsets/
[`APIView`]: http://www.cdrf.co/3.7/rest_framework.views/APIView.html
[`HyperlinkedRelatedField`]: https://www.django-rest-framework.org/api-guide/relations/#hyperlinkedrelatedfield

In Lesson 6:

- Use [`CreateView`], [`UpdateView`], and [`DeleteView`] to create views
  for `Startup` and `Post` objects (using `StartupForm` and `PostForm`)
- Create a view to create new `NewsLink` objects and associate them
  automatically with `Startup` objects
- Expand this view to handle updating `NewsLink` objects
- Allow for `NewsLink` objects to be deleted

[`CreateView`]: http://ccbv.co.uk/projects/Django/2.0/django.views.generic.edit/CreateView/
[`UpdateView`]: http://ccbv.co.uk/projects/Django/2.0/django.views.generic.edit/UpdateView/
[`DeleteView`]: http://ccbv.co.uk/projects/Django/2.0/django.views.generic.edit/DeleteView/


Below are a few other tasks to test your knowledge.

- Create links in the templates to enable easier navigation across the
  site
- Create a welcome page for the API (see the use of [`DefaultRouter`])

[`DefaultRouter`]: https://www.django-rest-framework.org/api-guide/routers/#defaultrouter

The solutions to all of the tasks above can be found in the
`class_material` git branch or [on Github].

[on Github]: https://github.com/jambonrose/python-web-dev-21-2

[🔝 Up to Table of Contents](#table-of-contents)

## Testing the Code

All of the tests used to build the code can be found in the
[`with_tests` branch] on Github.

[`with_tests` branch]: https://github.com/jambonrose/python-web-dev-21-2/tree/with_tests

The branch (mostly) emulates a Test Driven-Development approach: commits
prefixed with `test` write a test that will fail, while commits with
lesson numbers then fix the failing tests from previous `test` commits.

To run the tests locally use `manage.py`.

```shell
# from root of project
cd src
python3 manage.py test
```

Tests may also be run in Docker.

```shell
# from root of project
docker-compose run --rm django python manage.py test
```

Be advised that running tests in Lesson 2 is tricky. You will generally
need to create migrations before being able to run the tests, and there
are a few commits that break the project's ability to run tests (such as
when changing the database settings).

We will cover material about how to test Django in the next Python Web
Development class. I hope you're looking forward to it!

[🔝 Up to Table of Contents](#table-of-contents)

## Deploying the Code

The project follows [12 Factor App] principles and is configured to be
deployed to [Heroku].

To start you will need to [sign up for Heroku] unless you already have
an account. Make sure you have installed the [Heroku CLI].

[12 Factor App]: https://12factor.net/
[Heroku]: https://www.heroku.com/
[sign up for Heroku]: https://signup.heroku.com/
[Heroku CLI]: https://devcenter.heroku.com/articles/heroku-cli#download-and-install

The following instructions are for *nix systems, and will need to be
adapted for Windows.

Ensure your app is ready for deployment.

```shell
docker-compose run --rm django python manage.py check --deploy --settings="config.settings.production"
```

From the command line create a new app.

```shell
$ heroku create
```

Heroku will give your app a random name (such as
`infinite-tundra-77435`). Assign this name to a variable to be able to use
commands below.

```shell
$ export APP='infinite-tundra-77435' # replace with your actual app name
```

Your git repository should now have a new remote branch named `heroku`.
If it is missing you can add it manually.

```shell
$ heroku git:remote -a $APP
```

Create a PostgreSQL database for your app.

```shell
$ heroku addons:create -a "$APP" heroku-postgresql:hobby-dev
```

Configure your app to use production settings.

```shell
$ heroku config:set -a "$APP" DJANGO_SETTINGS_MODULE='config.settings.production'
$ heroku config:set -a "$APP" SECRET_KEY="$(head -c 75 /dev/urandom | base64 | tr -dc 'a-zA-Z0-9' | head -c 50)"
$ heroku config:set -a "$APP" PYTHONHASHSEED=random
$ heroku config:set -a "$APP" WEB_CONCURRENCY=2
```

You may now deploy your app.

```shell
$ git push heroku class_material:master
$ # you can also deploy the other branch to Heroku using:
$ git push heroku with_tests:master
```

To create a new user use the command below.

```shell
$ heroku run -a $APP python src/manage.py createsuperuser
```

To access the remote shell (to create data on the fly) use the command
below.

```shell
$ heroku run -a $APP python src/manage.py shell_plus
```

To see the app online you may use the command below.

```shell
$ heroku open -a $APP
```

For more about what we've just done please see Heroku's [Getting
Started with Python] documentation. If Lesson 7 does not cover
as much material as you'd like you may be interested in Chapter 29 of
[Django Unleashed].

[Getting Started with Python]: https://devcenter.heroku.com/articles/getting-started-with-python#introduction
[Django Unleashed]: https://django-unleashed.com/

[🔝 Up to Table of Contents](#table-of-contents)
