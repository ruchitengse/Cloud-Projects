'''
Created on Mar 1, 2016

@author: Ruchi.U
'''
import memcache
import db_connection
from collections import OrderedDict
import boto3
import os
def get_k_nearest_cities(country, region, city, k):
    
    memc = memcache.Client(['clouddatabase.6ptthp.0001.usw2.cache.amazonaws.com:11211'], debug=1);
    print "Connected to memcache"
    memcache_key = "knearest" + country + region + city + k;
    memcache_key = memcache_key.replace(" ", "");
    city_dict = memc.get(memcache_key);
    if not city_dict:
        db_conn = db_connection.DatabaseConnection()
        points = db_conn.get_latitude_longitude(country, region, city)
        if points:
            for point in points:
                lat = point[0];
                lon = point[1];
        else:
            return "Invalid Input"
        cities = db_conn.get_k_nearest_cities(country, k, lat, lon)
        city_dict = OrderedDict()
        for city in cities:
            city_dict[city[0]] = city[1];
        memc.set(memcache_key, city_dict)
    else:
        print "Already present in memcache"
    return city_dict

def get_cities_within_a_distance(country, region, city, distance):
    
    memc = memcache.Client(['clouddatabase.6ptthp.0001.usw2.cache.amazonaws.com:11211'], debug=1);
    memcache_key = "withindistance" + country + region + city + distance;
    memcache_key = memcache_key.replace(" ", "");
    city_dict = memc.get(memcache_key);
    if not city_dict:
        db_conn = db_connection.DatabaseConnection()
        points = db_conn.get_latitude_longitude(country, region, city)
        if points:
            for point in points:
                lat = point[0];
                lon = point[1];
        else:
            return "Invalid Input";
        city_dict = OrderedDict()
        cities = db_conn.get_cities_within_a_distance(country, distance, lat, lon)
        for city in cities:
            city_dict[city[0]] = city[1];
        memc.set(memcache_key, city_dict) ## add time to this for expiration
    else:
        print "Already present in memcache"
    return city_dict

def get_item_quota():
    kwargs = {'aws_access_key_id':'AKIAIRAB5ZYWDZMT3PXQ', 'aws_secret_access_key':'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', 'region_name':'us-west-2'}
    aws_resource = boto3.resource('s3', **kwargs)
    bucket = aws_resource.Bucket("logindataaws")
    DOWNLOAD_FOLDER = "/var/www/html/nearestcities"
    file_path = os.path.join(DOWNLOAD_FOLDER, 'filename')
    bucket.download_file(Key='filename', Filename=file_path)
    f = open(file_path)
    for line in f:
        line = line.strip();
        item_size = line.split(",")[0].strip();
        lifetime = line.split(",")[1].strip();
        return item_size, lifetime
    
def check_login(uname=None, pw=None):
    kwargs = {'aws_access_key_id':'AKIAIRAB5ZYWDZMT3PXQ', 'aws_secret_access_key':'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', 'region_name':'us-west-2'}
    aws_resource = boto3.resource('s3', **kwargs)
    bucket = aws_resource.Bucket("logindataaws")
    DOWNLOAD_FOLDER = "/var/www/html/nearestcities"
    file_path = os.path.join(DOWNLOAD_FOLDER, 'filename')
    bucket.download_file(Key='filename', Filename=file_path)
    f = open(file_path)
    for line in f:
        line = line.strip();
        username = line.split(",")[0].strip();
        password = line.split(",")[1].strip();
        if(uname == username and pw == password):
            return True;
        else:
            continue;
    return False;

def get_search_results():
    db_conn = db_connection.DatabaseConnection();
    results = db_conn.get_search_results();
    history = []
    for res in results:
        history.append(res[0]);
    return history;
        
def insert_into_history(link):
    db_conn = db_connection.DatabaseConnection();
    db_conn.insert_into_search_history(link);
    
def get_population(country, city):
    db_conn = db_connection.DatabaseConnection();
    pop = db_conn.display_population_for_city_name(country, city)
    list = []
    for p in pop:
        list.append(p[0])
    return list

def list_cities_in_range(pop_range_1, pop_range_2):
    db_conn = db_connection.DatabaseConnection()
    results = db_conn.display_cities_pop_range(pop_range_1, pop_range_2)
    res_dict = OrderedDict()
    for r in results:
        res_dict[r[0].decode('utf-8').strip()] = r[1]
    return res_dict

def list_all_cities_within_pop_limit(country, city, limit):
    db_conn = db_connection.DatabaseConnection()
    pop = db_conn.display_population_for_city_name(country, city);
    pop_val = 0
    for p in pop:
        pop_val = p[0];
    results = db_conn.list_all_cities_within_pop_limit(pop_val, limit);
    arr = []
    for r in results:
        arr.append(r[0].decode('utf-8').strip())
    return arr
        
def list_cities_group_by_country():
    db_conn = db_connection.DatabaseConnection()
    cities_gp = db_conn.list_cities_group_by_country()
    city_dict = OrderedDict()
    for cg in cities_gp:
        city_dict[cg[0].decode('utf-8').strip()] = cg[1]
    return city_dict