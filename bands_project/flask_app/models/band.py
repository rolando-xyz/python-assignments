import imp
from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
from flask import flash
import math
from flask_app.models import user

class Band:
    db_name = 'bands_schema'
    def __init__(self,data):
        self.id = data['id']
        self.band_name = data['band_name']
        self.genre = data['genre']
        self.city = data['city']
        self.founded_by = data['founded_by']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = user.User.get_one({'id': data['id']})


    @classmethod
    def save_band(cls,data):
        query = "INSERT INTO bands (band_name,genre,city,founded_by,founder_id) VALUES (%(band_name)s,%(genre)s,%(city)s,%(founded_by)s,%(founder_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_bands(cls,data):
        query = "SELECT * FROM bands;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        bands = []
        for r in results:
            bands.append( cls(r) )
        return bands

    @classmethod
    def get_band(cls,data):
        query = "SELECT * FROM bands WHERE id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(result[0])

    @classmethod
    def update(cls,data):
        query = 'UPDATE bands SET band_name=%(band_name)s,genre=%(genre)s,city=%(city)s,updated_at=NOW() WHERE id = %(id)s;'
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM bands WHERE bands.id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_band(band):
        is_valid = True
        if len(band['band_name']) < 2:
            is_valid = False
            flash("Band name must be at least 2 characters","band")
        if len(band['genre']) < 2:
            is_valid = False
            flash("Genre must be at least 2 characters","band")
        if len(band['city']) < 2:
            is_valid = False
            flash("City must be at least 2 characters","band")
        return is_valid