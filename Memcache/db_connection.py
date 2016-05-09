'''
Created on Mar 1, 2016

@author: Ruchi.U
'''
import MySQLdb
class DatabaseConnection:
    
    def __init__(self):
        self.connection = MySQLdb.connect(host="clouddatabase.cmac8hwmegyk.us-west-2.rds.amazonaws.com",user="ruchitengse",passwd="cloudpassword",db="cities",port=3306)
        self.cursor = self.connection.cursor()
    
    def get_latitude_longitude(self, country, region, city):
        sql = "SELECT latitude, longitude FROM city_info WHERE country = '%s' and region = '%s' and city = '%s'" % (country, region, city)
        try:
            self.cursor.execute(sql);
            results = self.cursor.fetchall();
            return results
        except:
            print "Error"
            
    def get_k_nearest_cities(self, country, k, latitude, longitude):
        sql = "SELECT city_info.city, ROUND((6371 * acos( cos( radians(%f)) * cos(radians(city_info.latitude)) * cos( radians(city_info.longitude) - radians(%f)) + sin(radians(%f)) * sin( radians(city_info.latitude)))), 3) AS distance FROM city_info WHERE city_info.country = '%s'  HAVING distance <= 50 AND distance > 0 ORDER BY distance ASC LIMIT %s" % (latitude, longitude, latitude, country, k)
        self.cursor.execute(sql);
        results = self.cursor.fetchall();
        return results
                
    def get_cities_within_a_distance(self, country, distance, latitude, longitude):
        sql = "SELECT city_info.city, ROUND((6371 * acos( cos( radians(%f)) * cos(radians(city_info.latitude)) * cos( radians(city_info.longitude) - radians(%f)) + sin(radians(%f)) * sin( radians(city_info.latitude)))), 3) AS distance FROM city_info WHERE city_info.country = '%s'  HAVING distance <= %s AND distance > 0 ORDER BY distance ASC" %(latitude, longitude, latitude, country, distance)  
        self.cursor.execute(sql);
        results = self.cursor.fetchall();
        return results
    
    def insert_into_search_history(self, link, login_name="default"):
        sql = "INSERT INTO search_history (login_name, link) VALUES ('%s', '%s')" % (login_name, link);
        try:
            self.cursor.execute(sql);
            self.connection.commit();
        except:
            self.connection.rollback();
            
    def get_search_results(self, login_name="default"):
        sql = "SELECT link FROM search_history WHERE login_name = '%s'" % login_name;
        self.cursor.execute(sql);
        results = self.cursor.fetchall();
        return results
        
    def display_population_for_city_name(self, country, city):
        sql = "SELECT pop FROM city_pop WHERE country = '%s' and city='%s'" %(country, city)
        print sql
        self.cursor.execute(sql);
        results = self.cursor.fetchall();
        return results
    
    def display_cities_pop_range(self, pop_range_1, pop_range_2):
        sql = "SELECT city, pop FROM city_pop WHERE pop >= %s and pop <= %s order by pop limit 10" % (pop_range_1, pop_range_2);
        print sql
        self.cursor.execute(sql);
        results = self.cursor.fetchall();
        return results
    
    def list_all_cities_within_pop_limit(self, pop_val, limit):
        pop_val_low_range = pop_val - 20;
        pop_val_up_range = pop_val + 20;
        sql = "SELECT DISTINCT city, pop FROM city_pop WHERE pop >= %s and pop <= %s order by pop limit %s" % (pop_val_low_range, pop_val_up_range, limit);
        print sql
        self.cursor.execute(sql);
        results = self.cursor.fetchall();
        return results
    
    def list_cities_group_by_country(self):
        sql = "SELECT country, COUNT(city) AS num FROM city_pop WHERE sex = 'Both Sexes' and year = 2015 GROUP BY country ORDER BY num";
        print sql
        self.cursor.execute(sql);
        results = self.cursor.fetchall();
        return results