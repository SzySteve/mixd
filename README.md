# mixd

mixd is a Spotify playlist sharing service which allows you to tag and describe your playlists, rather than simply titling them.
Playlists can then be searched quickly in a more intuitive way than the native spotify client allows.

### Development
* Clone the repo
* Make a new virtualenv and install dependencies from requirements.txt
* Run `manage.py migrate` from the root of the project
* Follow spotipy's credential instructions here: https://spotipy.readthedocs.io/en/latest/#authorized-requests
* Run `manage.py runserver`

### ToDo:
- [ ] Better development setup instructions
- [ ] Seed a bunch of tags, and populate the tag page with those
- [ ] Adjust suggest tags to provide betterer results
- [ ] Rename views/templates ot make some more sense
- [ ] Optimize API calls to spotify
- [ ] Employ DRF to get a really nice search going
