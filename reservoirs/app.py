from flask import Flask, render_template
from db_lib import Reservoirs_Data
import flask

app = Flask(__name__)
bd = Reservoirs_Data()

@app.route("/reservoirs")
def reservoirs():
	reservoirs_list = bd.get_reservoirs()
	ret = render_template("reservoirs.html", reservoirs_list = reservoirs_list)
	return ret

@app.route("/reservoirs/<reservoir_id>")
def reservoir(reservoir_id=None):
	reservoir_title = bd.get_reservoir_title(reservoir_id)
	countries_list = bd.get_countries(reservoir_id)
	type = bd.get_type(reservoir_id)
	square = bd.get_square(reservoir_id)
	confluence_list = bd.get_confluence(reservoir_id)
	length = len(confluence_list)
	length_countries = len(countries_list)
	ret = render_template("reservoir.html", reservoir_title=reservoir_title, countries_list=countries_list, type = type, square=square, confluence_list=confluence_list, length = length, length_countries=length_countries)
	return ret

@app.route("/")
def me():
	github = "https://github.com/DariaPetrovaa"
	ret = render_template("home.html", github = github)
	return ret

@app.route("/countries")
def countries():
	Countries_list = bd.get_Countries()
	ret = render_template("countries.html", Countries_list = Countries_list)
	return ret


@app.route("/countries/<country_id>")
def country(country_id=None):
	country_name = bd.get_country_name(country_id)
	reservoirs_list = bd.get_Reservoirs(country_id)
	square = bd.get_Square(country_id)
	population = bd.get_population(country_id)
	length = len(reservoirs_list)
	languages_list = bd.get_languages(country_id)
	ret = render_template("country.html", country_name=country_name, reservoirs_list=reservoirs_list, square=square, population=population, length=length, languages_list = languages_list)
	return ret

@app.route("/create_country", methods=['GET','POST'])
def country_new():
	if flask.request.method == "POST":
		input=dict(**flask.request.form)
		country_id = bd.generate_id_for_Country()
		name = input.pop('name', None)
		square = input.pop('square', None)
		population = input.pop('population', None)
		bd.insert_into_Country(country_id, name, square, population)
		languages_name = flask.request.form.getlist('languages')
		for language in languages_name:
			language_id = bd.get_language_id(language)
			if not language_id:
				language_id = bd.generate_id_for_Language()
			bd.insert_into_Language(language_id, str(language))
			bd.insert_into_Country_Language(country_id, language_id)
		reservoirs_id = flask.request.form.getlist('reservoirs')
		if reservoirs_id:
			for reservoir_id in reservoirs_id:
				#reservoir_id = bd.get_reservoir_id(reservoir)
				#if not reservoir_id:
					#reservoir_id = bd.generate_id_for_Reservoir()
				#bd.insert_into_Reservoir(reservoir_id, str(reservoir))
				bd.insert_into_Reservoir_Country(reservoir_id, country_id)
		return flask.redirect("/")
	reservoirs_list = bd.get_reservoirs()
	length = len(reservoirs_list)
	print(reservoirs_list)
	print(reservoirs_list[0]['id'])
	return flask.render_template("create_country.html", reservoirs_list=reservoirs_list, length=length)

app.run(host='0.0.0.0', port=5029)


