#!/usr/bin/env python3

import json
import locale
import sys
import operator
import reports
import emails

def load_data(filename):
  """Loads the contents of filename as a JSON file."""
  with open(filename) as json_file:
    data = json.load(json_file)
  return data


def format_car(car):
  """Given a car dictionary, returns a nicely formatted name."""
  return "{} {} ({})".format(
      car["car_make"], car["car_model"], car["car_year"])


def process_data(data):
  """Analyzes the data, looking for maximums.

  Returns a list of lines that summarize the information.
  """
  max_revenue = {"revenue": 0}
  max_sales = {"total_sales": 0}
  yearly_sales = {"2000": 0}
  for item in data:
    # Calculate the revenue generated by this model (price * total_sales)
    # We need to convert the price from "$1234.56" to 1234.56
    item_price = locale.atof(item["price"].strip("$"))
    item_revenue = item["total_sales"] * item_price
    if item_revenue > max_revenue["revenue"]:
      item["revenue"] = item_revenue
      max_revenue = item
    # TODO: also handle max sales
    item_sales = item["total_sales"]
    if item_sales > max_sales["total_sales"]:
      max_sales = item
    # TODO: also handle most popular car_year
    if item.get("car").get("car_year") in yearly_sales:
      yearly_sales[item.get("car").get("car_year")] = yearly_sales[item.get("car").get("car_year")] + item["total_sales"]
    else:
      yearly_sales[item.get("car").get("car_year")] = item["total_sales"]

  most_popular_year = max(yearly_sales.items(), key=operator.itemgetter(1))[0]

  summary = [
    "The {} generated the most revenue: ${}".format(
      format_car(max_revenue["car"]), max_revenue["revenue"]),
    "The {} had the most sales: {}".format(
      format_car(max_sales["car"]), max_sales["total_sales"]),
    "The most popular year was {} with {} sales.".format(
      most_popular_year, yearly_sales[most_popular_year]),
  ]

  return summary


def cars_dict_to_table(car_data):
  """Turns the data in car_data into a list of lists."""
  table_data = [["ID", "Car", "Price", "Total Sales"]]
  for item in car_data:
    table_data.append([item["id"], format_car(item["car"]), item["price"], item["total_sales"]])
  return table_data


def main(argv):
  """Process the JSON data and generate a full report out of it."""
  data = load_data("car_sales.json")
  data = sorted(data, key = lambda k: k["total_sales"])
  summary = process_data(data)
  print(summary)
  # TODO: turn this into a PDF report
  car_make_sales = {"BMW": 0}
  for item in data:
      if item.get("car").get("car_make") in car_make_sales:
        car_make_sales[item.get("car").get("car_make")] = car_make_sales[item.get("car").get("car_make")] + item["total_sales"]
      else:          
        car_make_sales[item.get("car").get("car_make")] = item["total_sales"]
  reports.generate("/tmp/cars.pdf", "Car Sales Overview", "<br/>".join(summary), cars_dict_to_table(data), reports.generate_pie_chart(car_make_sales))
  # TODO: send the PDF report as an email attachment
  message = emails.generate("automation@example.com", "student-00-9ed7de238eb5@example.com", "Sales summary for last month", body = "\n".join(summary),attachment_path = "/tmp/cars.pdf")
  emails.send(message)

if __name__ == "__main__":
  main(sys.argv)
