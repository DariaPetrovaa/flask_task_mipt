from sqlalchemy import create_engine, text
#from flask_wtf import FlaskForm
#from wtforms import StringField
#from wtforms.validators import DataRequired

class Reservoirs_Data(object):
	def __init__(self):
		self._engine=create_engine("sqlite:///reservoirs_data.db", echo=True)
	def get_reservoirs(self):
		sql = text("select Reservoir.id as id, Reservoir.title as title, Reservoir.square as square, Type.name as type from Type join Reservoir on Reservoir.type_id = Type.id;")
		sql_result = self._engine.execute(sql)
		ret = []
		for record in sql_result:
			ret.append(dict(record))
		return ret

#bd = Reservoirs_Data()
#print(bd.get_reservoirs())
	def get_countries(self, reservoir_id):
		sql = text("select Country.name as countries, Country.id as id from Reservoir_Country inner join Country on Country.id = Reservoir_Country.country_id where Reservoir_Country.reservoir_id = " + str(reservoir_id) +" ;")
		sql_result = self._engine.execute(sql)
		ret = []
		for record in sql_result:
			ret.append(dict(record))
		return ret
#bd = Reservoirs_Data()
#print(bd.get_countries(4))
	def get_languages(self, country_id):
		sql = text("select group_concat(Language.name, \", \") as Languages from Country_Language inner join Language on Country_Language.language_id = Language.id where Country_Language.country_id = "+ str(country_id) +";")
		sql_result = self._engine.execute(sql)
		for record in sql_result:
			dictionary = dict(record)
		return dictionary["Languages"]

	def get_reservoir_title(self, reservoir_id):
		sql = text("select * from Reservoir where id = "+str(reservoir_id) +";")
		sql_result = self._engine.execute(sql)
		for reser in sql_result:
			res = str(reser["title"])
		return res

	def get_type(self, reservoir_id):
		sql = text("select Type.name as type_name from Type inner join Reservoir on Reservoir.type_id = Type.id where Reservoir.id = "+str(reservoir_id) +";")
		sql_result = self._engine.execute(sql)
		for record in sql_result:
			dictionary = dict(record)
		return dictionary["type_name"]

	def get_square(self, reservoir_id):
		sql = text("select Reservoir.square as square from Reservoir where id="+str(reservoir_id) +";")
		sql_result = self._engine.execute(sql)
		for record in sql_result:
			dictionary = dict(record)
		return dictionary["square"]

	def get_confluence(self, reservoir_id):
		sql = text("with qq as (select Reservoir_Confluence.reservoir1_id, Reservoir_Confluence.reservoir2_id from Reservoir left join Reservoir_Confluence on Reservoir.id = Reservoir_Confluence.reservoir1_id or Reservoir.id = Reservoir_Confluence.reservoir2_id where id="+ str(reservoir_id) +") select Reservoir.title as reservoirs, Reservoir.id as id from Reservoir where Reservoir.id in ( select iif(qq.reservoir1_id = "+ str(reservoir_id) +",qq.reservoir2_id, qq.reservoir1_id) from qq);")
		sql_result = self._engine.execute(sql)
		ret = []
		for record in sql_result:
			ret.append(dict(record))
		return ret

	def get_Countries(self):
		sql = text("select Country.id as id, Country.name as name, Country.square as square, Country.population as population from Country;")
		sql_result = self._engine.execute(sql)
		ret = []
		for record in sql_result:
			ret.append(dict(record))
		return ret

	def get_Square(self, country_id):
		sql = text("select Country.square as Square from Country where id="+ str(country_id) +";")
		sql_result = self._engine.execute(sql)
		for record in sql_result:
			dictionary = dict(record)
		return dictionary["Square"]

	def get_population(self, country_id):
		sql = text("select Country.population as population from Country where id="+str(country_id) +";")
		sql_result = self._engine.execute(sql)
		for record in sql_result:
			dictionary = dict(record)
		return dictionary["population"]

	def get_Reservoirs(self, country_id):
		sql = text("select Reservoir.title as Reservoirs, Reservoir.id as id from Reservoir inner join Reservoir_Country on Reservoir_Country.reservoir_id = Reservoir.id where Reservoir_Country.country_id = "+ str(country_id) +";")
		sql_result = self._engine.execute(sql)
		ret = []
		for record in sql_result:
			ret.append(dict(record))
		return ret

	def get_country_name(self, country_id):
		sql = text("select * from Country where id = "+str(country_id) +";")
		sql_result = self._engine.execute(sql)
		for country in sql_result:
			res = str(country["name"])
		return res

	def generate_id_for_Country(self):
		sql = text("select id+1 as id from Country order by id desc limit 1;")
		sql_result = self._engine.execute(sql)
		for record in sql_result:
			dictionary = dict(record)
		return dictionary["id"]

	def insert_into_Country(self, id, name, square, population):
		sql = ("insert into Country(id, name, square, population) values (:id, :name, :square, :population);")
		sql_result = self._engine.execute(sql, {'id':id, 'name':name, 'square':square, 'population':population})


	def insert_into_Language(self, id, name):
		sql = text("insert into Language(id, name) values (:id, :name);")
		sql_result = self._engine.execute(sql, {'id':id, 'name':name})

	def generate_id_for_Language(self):
		sql = text("select id+1 as id from Language order by id desc limit 1;")
		sql_result = self._engine.execute(sql)
		for record in sql_result:
			dictionary = dict(record)
		return dictionary["id"]

	def generate_id_for_reservoir(self):
		sql = text("select id+1 as id from Reservoir order by id desc limit 1;")
		sql_result = self._engine.execute(sql)
		for record in sql_result:
			dictionary = dict(record)
		return dictionary["id"]

	def insert_into_reservoir(self, id, title, type_id, square):
		sql = text("insert into Reservoir(id, title, type_id, square) values (:id, :title,:type_id, :square);")
		sql_result = self._engine.execute(sql, {'id':id, 'title':title, 'type_id':type_id, 'square':square})

	def insert_into_Country_Language(self, country_id, language_id):
		sql = text("insert into Country_Language(country_id, language_id) values (:country_id,:language_id);")
		sql_result = self._engine.execute(sql, {'country_id':country_id, 'language_id':language_id})

	def insert_into_Reservoir_Country(self, reservoir_id, country_id):
		sql = text("insert into Reservoir_Country(reservoir_id, country_id) values (:reservoir_id,:country_id);")
		sql_result = self._engine.execute(sql, {'reservoir_id':reservoir_id, 'country_id':country_id})

	def get_language_id(self, language_name):
		sql = text("with qq as (select id as id from Language where name = :language_name) select iif(count(qq.id=0), 0, qq.id) as id from qq;")
		sql_result = self._engine.execute(sql, {'language_name':str(language_name)})
		print(sql_result)
		if sql_result:
			for record in sql_result:
				dictionary = dict(record)
			return dictionary["id"]
		return False

	#def get_reservoir_id(self, reservoir_name):
		#sql = text("with qq as (select id as id from Reservoir where title = :reservoir_name) select iif(count(qq.id)=0, 0, qq.id) as id from qq;")
		#sql_result = self._engine.execute(sql, {'reservoir_name':str(reservoir_name)})
		#if sql_result:
			#for record in sql_result:
				#dictionary = dict(record)
			#return dictionary["id"]
		#return False

	def get_types(self):
		sql = text("select Type.id as id, Type.name as name from Type;")
		sql_result = self._engine.execute(sql)
		ret = []
		for record in sql_result:
			ret.append(dict(record))
		return ret 

	def insert_into_Reservoir_Confluence(self, reservoir1_id, reservoir2_id):
		sql = text("insert into Reservoir_Confluence(reservoir1_id, reservoir2_id) values(:reservoir1_id, :reservoir2_id);")
		sql_result = self._engine.execute(sql, {'reservoir1_id':reservoir1_id, 'reservoir2_id':reservoir2_id})
