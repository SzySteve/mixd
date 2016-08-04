# mixd

mixd is a Spotify playlist sharing service.

### Development
* Clone the repo
* Make a new virtualenv and install dependencies from requirements.txt
* Run `manage.py migrate` from the root of the project
* Follow spotipy's credential instuctions here: https://spotipy.readthedocs.io/en/latest/#authorized-requests
* Run `manage.py runserver`

### ToDo:
- [ ] Better development setup instructions
- [ ] Make tagging page submit a form
- [ ] Seed a bunch of tags, and populate the tag page with those
- [ ] Adjust suggest tags to provide betterer results
