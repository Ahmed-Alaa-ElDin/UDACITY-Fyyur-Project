#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import distinct, func, Date, cast
from datetime import date
from sqlalchemy.orm import relationship
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database --> Done

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Ahmed1000@localhost:5432/fyyur'
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Show (db.Model):
    __tablename__ = 'show'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    start_time = db.Column(db.DateTime)

    venues = db.relationship('Venue', backref=db.backref('show'))
    artists = db.relationship('Artist', backref=db.backref('show'))

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    genre = db.Column(db.String())
    seeking_venue = db.Column(db.Boolean())
    seeking_description = db.Column(db.String())
    image_link = db.Column(db.String(500))
    def __repr__ (self):
        return f'<Artist: {self.id}, {self.name},{self.city},{self.state},{self.phone},{self.image_link},{self.facebook_link}>'

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genre = db.Column(db.String())
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean())
    seeking_description = db.Column(db.String())
    def __repr__ (self):
        return f'<venue {self.id}, {self.name},{self.city},{self.state},{self.address},{self.phone},{self.image_link},{self.facebook_link}>'


db.create_all()

# TODO: implement any missing fields, as a database migration using Flask-Migrate --> Done
# TODO: implement any missing fields, as a database migration using Flask-Migrate --> Done
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration. --> Done


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/', methods= ["POST","GET","DELETE"])
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues',methods = ["GET","POST","DELETE"])
def venues():

  data = []
  areas_distinct = Venue.query.distinct("city","state").all()
  areas = Venue.query.all()
  for area_distinct in areas_distinct:
      area_list = {}
      area_list['city'] = area_distinct.city
      area_list['state'] = area_distinct.state
      for area in areas:
          data_int = []
          if area_distinct.city == area.city and area_distinct.state == area.state:
              venues_querys = Venue.query.filter_by(city = area_distinct.city , state = area_distinct.state).all()
              for venues_query in venues_querys:
                  vinue_list = {}
                  vinue_list['id'] = venues_query.id
                  vinue_list['name'] = venues_query.name
                  data_int.append(vinue_list)
                  area_list['venues'] = data_int
      data.append(area_list)
  return render_template('pages/venues.html', data=data , areas_distinct=areas_distinct);

# TODO: replace with real venues data.  ----> Done
#       num_shows should be aggregated based on number of upcoming shows per venue.

@app.route('/venues/search', methods=['POST'])
def search_venues():

  # parse the search input
  venue_search_input = request.form.to_dict()["search_term"]

  # search in database
  venue_search_query = Venue.query.filter(Venue.name.ilike('%'+ venue_search_input +'%')).all()

  response = {
      "count":len(venue_search_query),
      "data": []
      }
  for value in venue_search_query:
      response["data"].append(
      {"id": value.id,
      "name": value.name,
      "num_upcoming_shows": 0,}
      )

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

# TODO: implement search on artists with partial string search. Ensure it is case-insensitive. --> Done
# seach for Hop should return "The Musical Hop".  --> Done
# search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee" --> Done

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

  venue_querys = Venue.query.filter(Venue.id == venue_id).first() # --> 1
  if venue_querys.genre != None:
      gen_ven_querys = venue_querys.genre.split(",") # --> 2
      genre_result = []
      for gen_ven_query in gen_ven_querys:
          genre_result.append(gen_ven_query)
  else:
      genre_result = []
  past_shows_querys = db.session.query(Show.id , Show.start_time , Artist.id.label("artist_id"), Artist.name.label("artist_name"), Artist.image_link.label("artist_image_link")  , Venue.name.label("MyName")).join(Artist).join(Venue).filter(Show.artist_id == Artist.id, cast(Show.start_time,Date) < date.today(),Show.venue_id == venue_id).all()
  past_showes = []
  for past_shows_query in past_shows_querys:
      past_shows_one_query = {}
      past_shows_one_query = {
          "artist_id": past_shows_query.artist_id,
          "artist_name": past_shows_query.artist_name,
          "artist_image_link": past_shows_query.artist_image_link,
          "start_time": past_shows_query.start_time
      }
      past_showes.append(past_shows_one_query) # --> 3
  past_showes_count = len(past_shows_querys)
  upcoming_shows_querys = db.session.query(Show.id, Show.start_time , Artist.id.label("artist_id"), Artist.name.label("artist_name"), Artist.image_link.label("artist_image_link")  , Venue.name.label("MyName")).join(Artist).join(Venue).filter(Show.artist_id == Artist.id, cast(Show.start_time,Date) >= date.today(),Show.venue_id == venue_id).all()
  upcoming_shows = []
  for upcoming_shows_query in upcoming_shows_querys:
      upcoming_shows_one_query ={}
      upcoming_shows_one_query = {
          "artist_id": upcoming_shows_query.artist_id,
          "artist_name": upcoming_shows_query.artist_name,
          "artist_image_link": upcoming_shows_query.artist_image_link,
          "start_time": upcoming_shows_query.start_time
      }
      upcoming_shows.append(upcoming_shows_one_query) # --> 4
  upcoming_showes_count = len(upcoming_shows_querys)

  data = {
    "id": venue_id,
    "name": venue_querys.name,
    "genres": genre_result,
    "address": venue_querys.address,
    "city": venue_querys.city,
    "state": venue_querys.state,
    "phone": venue_querys.phone,
    "website": venue_querys.website,
    "facebook_link": venue_querys.facebook_link,
    "seeking_talent": venue_querys.seeking_talent,
    "seeking_description": venue_querys.seeking_description ,
    "image_link": venue_querys.image_link,
    "past_shows": past_showes,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": past_showes_count,
    "upcoming_shows_count": upcoming_showes_count,
  }

  return render_template('pages/show_venue.html', venue=data)

# shows the venue page with the given venue_id --> Done
# TODO: replace with real venue data from the venues table, using venue_id --> Done


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    error = False

    try:
        name = request.form.get("name")
        city = request.form.get("city")
        state = request.form.get("state")
        address = request.form.get("address")
        phone = request.form.get("phone")
        genres = request.form.getlist("genres")
        facebook_link = request.form.get("facebook_link")
        new_venue = Venue(name = name, city = city, genre = ",".join(genres), state = state, address = address, phone = phone, facebook_link = facebook_link)
        db.session.add(new_venue)
        db.session.commit()

    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. Venue ' + request.form.get('name') + ' could not be listed.')

    finally:
        db.session.close()

    if error:
        abort (400)

    flash('Venue ' + request.form.get('name') + ' was successfully listed!')

    return render_template('pages/home.html')

# TODO: insert form data as a new Venue record in the db, instead --> Done
# TODO: modify data to be the data object returned from db insertion --> Done
# on successful db insert, flash success --> Done
# TODO: on unsuccessful db insert, flash an error instead. --> Done
# e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.') --> Done
# see: http://flask.pocoo.org/docs/1.0/patterns/flashing/ --> Done

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
        try:
            delete_item = request.get_json()['id']
            venue_delete = Venue.query.get(delete_item)
            db.session.delete(venue_delete)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()
        return redirect(url_for('venues'))

# TODO: Complete this endpoint for taking a venue_id, and using ---> Done
# SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail. ---> Done
# BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that ---> Done
# clicking that button delete it from the db then redirect the user to the homepage ---> Done
# return None ---> Done


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists',methods = ["GET","POST","DELETE"])
def artists():
  # TODO: replace with real data returned from querying the database ---> Done
  data = []
  artists = Artist.query.all()
  for artist in artists:
      artist_list = {}
      artist_list['id'] = artist.id
      artist_list['name'] = artist.name
      data.append(artist_list)
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive. --> Done
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  # parse the search input
  artist_search_input = request.form.to_dict()["search_term"]

  # search in database
  artist_search_query = Artist.query.filter(Artist.name.ilike('%'+ artist_search_input +'%')).all()

  response = {
      "count":len(artist_search_query),
      "data": []
      }
  for value in artist_search_query:
      response["data"].append(
      {"id": value.id,
      "name": value.name,
      "num_upcoming_shows": 0,}
      )

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id --> Done

    artist_querys = Artist.query.filter(Artist.id == artist_id).first() # --> 1
    if artist_querys.genre != None:
        gen_art_querys = artist_querys.genre.split(",")
        genre_result = [] # --> 2
        for gen_art_query in gen_art_querys:
            genre_result.append(gen_art_query)
    else:
        genre_result = [] # --> 2

    past_shows_querys = db.session.query(Show ,Show.start_time , Venue.id.label("venue_id"), Venue.name.label("venue_name"), Venue.image_link.label("venue_image_link")).join(Artist).join(Venue).filter(Show.artist_id == artist_id, cast(Show.start_time,Date) < date.today(),Show.venue_id == Venue.id).all()
    past_showes = []
    past_shows_one_query = {}
    for past_shows_query in past_shows_querys:
        past_shows_one_query = {
            "venue_id": past_shows_query.venue_id,
            "venue_name": past_shows_query.venue_name,
            "venue_image_link": past_shows_query.venue_image_link,
            "start_time": past_shows_query.start_time
        }
        past_showes.append(past_shows_one_query) # --> 3
    past_showes_count = len(past_shows_querys)
    upcoming_shows_querys = db.session.query(Show , Show.start_time , Venue.id.label("venue_id"), Venue.name.label("venue_name"), Venue.image_link.label("venue_image_link")).join(Artist).join(Venue).filter(Show.artist_id == artist_id, cast(Show.start_time,Date) >= date.today(),Show.venue_id == Venue.id).all()
    upcoming_shows = []
    for upcoming_shows_query in upcoming_shows_querys:
        upcoming_shows_one_query ={}
        upcoming_shows_one_query = {
            "venue_id": upcoming_shows_query.venue_id,
            "venue_name": upcoming_shows_query.venue_name,
            "venue_image_link": upcoming_shows_query.venue_image_link,
            "start_time": upcoming_shows_query.start_time
        }
        upcoming_shows.append(upcoming_shows_one_query) # --> 4
    upcoming_showes_count = len(upcoming_shows_querys)

    data = {
      "id": artist_id,
      "name": artist_querys.name,
      "genres": genre_result,
      "city": artist_querys.city,
      "state": artist_querys.state,
      "phone": artist_querys.phone,
      "website": artist_querys.website,
      "facebook_link": artist_querys.facebook_link,
      "seeking_venue": artist_querys.seeking_venue,
      "seeking_description": artist_querys.seeking_description ,
      "image_link": artist_querys.image_link,
      "past_shows": past_showes,
      "upcoming_shows": upcoming_shows,
      "past_shows_count": past_showes_count,
      "upcoming_shows_count": upcoming_showes_count,
    }

    return render_template('pages/show_artist.html', artist=data)

# DELETE

@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
        try:
            delete_item = request.get_json()['id']
            artist_delete = Artist.query.get(delete_item)
            db.session.delete(artist_delete)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()
        return redirect(url_for('artists'))


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist_query = Artist.query.filter_by(id = artist_id).first()
  genres = artist_query.genre.split(",") if artist_query.genre != None else ""
  artist={
    "id": artist_id,
    "name": artist_query.name,
    "genres": genres,
    "city": artist_query.city,
    "state": artist_query.state,
    "phone": artist_query.phone,
    "website": artist_query.website,
    "facebook_link": artist_query.facebook_link,
    "seeking_venue": artist_query.seeking_venue,
    "seeking_description": artist_query.seeking_description,
    "image_link": artist_query.image_link
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  artist_query = Artist.query.filter_by(id = artist_id).first()
  artist_query.name = request.form.get("name")
  artist_query.city = request.form.get("city")
  artist_query.state = request.form.get("state")
  artist_query.phone = request.form.get("phone")
  artist_query.genre = ",".join(request.form.getlist("genres"))
  artist_query.facebook_link = request.form.get("facebook_link")
  db.session.commit()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue_query = Venue.query.filter_by(id = venue_id).first()
  genres = venue_query.genre.split(",") if venue_query.genre != None else ""
  venue={
    "id": venue_id,
    "name": venue_query.name,
    "genres": genres,
    "address": venue_query.address,
    "city": venue_query.city,
    "state": venue_query.state,
    "phone": venue_query.phone,
    "website": venue_query.website,
    "facebook_link": venue_query.facebook_link,
    "seeking_talent": venue_query.seeking_talent,
    "seeking_description": venue_query.seeking_description,
    "image_link": venue_query.image_link
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
    venue_query = Venue.query.filter_by(id = venue_id).first()
    venue_query.name = request.form.get("name")
    venue_query.address = request.form.get("address")
    venue_query.city = request.form.get("city")
    venue_query.state = request.form.get("state")
    venue_query.phone = request.form.get("phone")
    venue_query.genre = ",".join(request.form.getlist("genres"))
    venue_query.facebook_link = request.form.get("facebook_link")
    db.session.commit()

    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():

    error = False

    try:
        name = request.form.get("name")
        city = request.form.get("city")
        state = request.form.get("state")
        phone = request.form.get("phone")
        genres = request.form.getlist("genres")
        facebook_link = request.form.get("facebook_link")
        new_artist = Artist(name = name, city = city, genre = ",".join(genres), state = state, phone = phone, facebook_link = facebook_link)
        db.session.add(new_artist)
        db.session.commit()

    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())

    finally:
        db.session.close()

    if error:
        abort (400)

  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data. --> Done
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  data = []
  # shows_query = Show.query.all()
  # shows_query = db.session.query(Show).all()
  shows_query = db.session.query(Show ,Show.start_time.label("start_time"), Artist.id.label("artist_id"), Artist.name.label("artist_name"), Artist.image_link.label("artist_image_link")  , Venue.name.label("MyName"), Venue.id.label("venue_id"), Venue.name.label("venue_name"), Venue.image_link.label("venue_image_link")).join(Artist).join(Venue).filter(Show.artist_id == Artist.id, Show.venue_id == Venue.id).all()
  for show_query in shows_query:
      query = {}
      query["venue_id"] = show_query.venue_id
      # venue_querys = Venue.query.filter_by(id = show_query[1]).first()
      query["venue_name"] = show_query.venue_name
      query["artist_id"] = show_query.artist_id
      # artist_querys = Artist.query.filter_by(id = show_query[0]).first()
      query["artist_name"] = show_query.artist_name
      query["artist_image_link"] = show_query.artist_image_link
      query["start_time"] = show_query.start_time
      data.append(query)


  return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():

  # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    error = False

    try:
        artist_id = request.form.get("artist_id")
        venue_id = request.form.get("venue_id")
        start_time = request.form.get("start_time")
        new_show = Show(artist_id = artist_id, venue_id=venue_id, start_time= start_time)
        db.session.add(new_show)
        db.session.commit()

    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())

    finally:
        db.session.close()

        if error:
            abort (400)
    flash('Show was successfully listed!')
    return render_template('pages/home.html')
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
