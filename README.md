# mixd

mixd is a Spotify playlist sharing service which allows you to tag and describe your playlists, rather than simply titling them.
Playlists can then be searched quickly in a more intuitive way than the native spotify client allows.

### Deployment
* Clone the repo
* Run this as a django app
    * Make sure to drop `SPOTIPY_` env variabels in gunicorn config.


### ToDo:
- [ ] Better development setup instructions
- [ ] Seed a bunch of tags, and populate the tag page with those.
- [ ] Adjust suggest tags to provide betterer results
- [ ] Rename views/templates to make some more sense
- [ ] Optimize API calls to spotify
- [ ] Import DRF for search/filter, pagination, etc.
- [ ] Time duration for playlists and tracks
- [ ] Implement 'update on fetch' pattern for playlist metadata
- [ ] Write a makefile or something to ease remote development
    - Scripts for syncing to a remote server, enabling debug mode, etc.
- [x] Refactor models to use many to many fields for quick filtering
- [x] Store CM-type stuff somewhere other than my web server.

Thanks to @dansinger, @treemonaco and @exeivot for their work on the UI/UX!
