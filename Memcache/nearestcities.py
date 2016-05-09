'''
Created on Mar 1, 2016

@author: Ruchi.U
'''
from flask import Flask
from flask.templating import render_template
from flask import request
import city_controller

app = Flask(__name__)

@app.route("/")
def main_page():
    return render_template('display_pop.html')

@app.route("/display_pop", methods=["GET"])
def display_pop():
    country = request.args['country']
    city = request.args['city']
    display_pop_val = city_controller.get_population(country, city);
    return render_template("display_pop.html", display_pop_val = display_pop_val)

@app.route("/display_pop_within_range", methods=["GET"])
def display_pop_within_range():
    pop_range_1 = request.args['pop_range_1']
    pop_range_2 = request.args['pop_range_2']
    pop_range_val = city_controller.list_cities_in_range(pop_range_1, pop_range_2)
    return render_template("display_pop.html", pop_range_val = pop_range_val)

@app.route("/display_pop_K", methods=["GET"])
def display_pop_K():
    country = request.args['country']
    city = request.args['city']
    K = request.args['K']
    display_pop_K = city_controller.list_all_cities_within_pop_limit(country, city, K);
    return render_template("display_pop.html", display_pop_K = display_pop_K)

@app.route("/display_no_of_cities", methods=["GET"])
def display_no_of_cities():
    list_of_cities = city_controller.list_cities_group_by_country()
    return render_template("display_pop.html", list_of_cities = list_of_cities)

# @app.route("/cities_within_a_distance", methods=["GET"])
# def get_cities_within_a_distance():
#     if request.method == "GET":
#         print "Get request"
#     country = request.args['country']
#     region = request.args['region']
#     city = request.args['city']
#     distance = request.args['N']
#     url = "/cities_within_a_distance?country=%s&region=%s&city=%s&N=%s" %(country, region, city, distance)
#     city_controller.insert_into_history(url)
#     search_results = city_controller.get_search_results();
#     cities = city_controller.get_cities_within_a_distance(country, region, city, distance)
#     return render_template('main_page.html', cities = cities, search_results = search_results)
#     
# @app.route("/k_nearest_cities", methods=["GET"])
# def get_k_nearest_cities():
#     if request.method == "GET":
#         print "Get request"
#     country = request.args['country']
#     region = request.args['region']
#     city = request.args['city']
#     k = request.args['K']
#     url = "/k_nearest_cities?country=%s&region=%s&city=%s&K=%s" %(country, region, city, k)
#     city_controller.insert_into_history(url)
#     search_results = city_controller.get_search_results();
#     cities = city_controller.get_k_nearest_cities(country, region, city, k)
#     return render_template('main_page.html', cities = cities, search_results = search_results)

if __name__=="__main__":
#     app.add
    app.debug = True;
    app.run()