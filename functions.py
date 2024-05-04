import requests
import io
from PIL import Image
import json
from itertools import chain
import pandas as pd
import math
import numpy as np
from geopy.geocoders import GoogleV3

#------------------------------------------------------------------------------
#The Code in this File is greatly inspired from the website listed below:
#https://towardsdatascience.com/a-python-tool-for-fetching-air-pollution-data-from-google-maps-air-quality-apis-7cf58a7c63cb
#------------------------------------------------------------------------------

#Convert Zipcode to Latitude, Longitude
def zipToLngLat(zipcode,country,key):
    geolocator = GoogleV3(api_key=key)
    locDetails = geolocator.geocode(zipcode,components={'country':country})
    lnglat = {'latitude':locDetails[-1][0],'longitude':locDetails[-1][1]}
    return lnglat

class Client(object):
    DEFAULT_BASE_URL = "https://airquality.googleapis.com"

    def __init__(self, key):
        self.session = requests.Session()
        self.key = key

    def request_post(self, url, params):
        request_url = self.compose_url(url)
        request_header = self.compose_header()
        request_body = params

        response = self.session.post(
            request_url,
            headers=request_header,
            json=request_body,
        )

        return self.get_body(response)

    #Compose a URL given a path, and key
    def compose_url(self, path):
        return self.DEFAULT_BASE_URL + path + "?" + "key=" + self.key

    @staticmethod
    def get_body(response):
        body = response.json()

        if "error" in body:
            return body["error"]

        return body

    @staticmethod
    def compose_header():
        return {
            "Content-Type": "application/json",
        }

    def request_get(self,url):

      request_url = self.compose_url(url)
      response = self.session.get(request_url)

      # for images coming from the heatmap tiles service
      return self.get_image(response)

    def get_image(self, response):

      if response.status_code == 200:
        image_content = response.content
        # note use of Image from PIL here
        # needs from PIL import Image
        image = Image.open(io.BytesIO(image_content))
        return image
      else:
        print("GET request for image returned an error")
        return None
    
    def request_post(self,url,params):

      request_url = self.compose_url(url)
      request_header = self.compose_header()
      request_body = params

      response = self.session.post(
        request_url,
        headers=request_header,
        json=request_body,
      )

      response_body = self.get_body(response)

      # put the first page in the response dictionary
      page = 1
      final_response = {
          "page_{}".format(page) : response_body
      }
      # fetch all the pages if needed
      while "nextPageToken" in response_body:
        # call again with the next page's token
        request_body.update({
            "pageToken":response_body["nextPageToken"]
        })
        response = self.session.post(
            request_url,
            headers=request_header,
            json=request_body,
        )
        response_body = self.get_body(response)
        page += 1
        final_response["page_{}".format(page)] = response_body

      return final_response


def current_conditions(
    client,
    location,
    include_local_AQI=True,
    include_health_suggestion=False,
    include_all_pollutants=True,
    include_additional_pollutant_info=False,
    include_dominent_pollutant_conc=True,
    language=None,
):
    """
    See documentation for this API here
    https://developers.google.com/maps/documentation/air-quality/reference/rest/v1/currentConditions/lookup
    """
    params = {}

    if isinstance(location, dict):
        params["location"] = location
    else:
        raise ValueError(
            "Location argument must be a dictionary containing latitude and longitude"
        )

    extra_computations = []
    if include_local_AQI:
        extra_computations.append("LOCAL_AQI")

    if include_health_suggestion:
        extra_computations.append("HEALTH_RECOMMENDATIONS")

    if include_additional_pollutant_info:
        extra_computations.append("POLLUTANT_ADDITIONAL_INFO")

    if include_all_pollutants:
        extra_computations.append("POLLUTANT_CONCENTRATION")

    if include_dominent_pollutant_conc:
        extra_computations.append("DOMINANT_POLLUTANT_CONCENTRATION")

    if language:
        params["language"] = language

    params["extraComputations"] = extra_computations

    return client.request_post("/v1/currentConditions:lookup", params)


def historical_conditions(
    client,
    location,
    specific_time=None,
    lag_time=None,
    specific_period=None,
    include_local_AQI=True,
    include_health_suggestion=False,
    include_all_pollutants=True,
    include_additional_pollutant_info=False,
    include_dominant_pollutant_conc=True,
    language=None,
):
    """
    See documentation for this API here https://developers.google.com/maps/documentation/air-quality/reference/rest/v1/history/lookup
    """
    params = {}

    if isinstance(location, dict):
        params["location"] = location
    else:
        raise ValueError(
            "Location argument must be a dictionary containing latitude and longitude"
        )

    if isinstance(specific_period, dict) and not specific_time and not lag_time:
        assert "startTime" in specific_period
        assert "endTime" in specific_period

        params["period"] = specific_period

    elif specific_time and not lag_time and not isinstance(specific_period, dict):
        # note that time must be in the "Zulu" format
        # e.g. datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%dT%H:%M:%SZ")
        params["dateTime"] = specific_time

    # lag periods in hours
    elif lag_time and not specific_time and not isinstance(specific_period, dict):
        params["hours"] = lag_time

    else:
        raise ValueError(
            "Must provide specific_time, specific_period or lag_time arguments"
        )

    extra_computations = []
    if include_local_AQI:
        extra_computations.append("LOCAL_AQI")

    if include_health_suggestion:
        extra_computations.append("HEALTH_RECOMMENDATIONS")

    if include_additional_pollutant_info:
        extra_computations.append("POLLUTANT_ADDITIONAL_INFO")

    if include_all_pollutants:
        extra_computations.append("POLLUTANT_CONCENTRATION")

    if include_dominant_pollutant_conc:
        extra_computations.append("DOMINANT_POLLUTANT_CONCENTRATION")

    if language:
        params["language"] = language

    params["extraComputations"] = extra_computations
    # page size default set to 100 here
    params["pageSize"] = 100
    # page token will get filled in if needed by the request_post method
    params["pageToken"] = ""

    return client.request_post("/v1/history:lookup", params)


def historical_conditions_to_df(response_dict):

  chained_pages = list(chain(*[response_dict[p]["hoursInfo"] for p in [*response_dict]]))

  all_indexes = []
  all_pollutants = []
  for i in range(len(chained_pages)):
    # need this check in case one of the timestamps is missing data, which can sometimes happen
    if "indexes" in chained_pages[i]:
      this_element = chained_pages[i]
      # fetch the time
      time = this_element["dateTime"]
      # fetch all the index values and add metadata
      all_indexes += [(time , x["code"],x["displayName"],"index",x["aqi"],None) for x in this_element['indexes']]
      # fetch all the pollutant values and add metadata
      all_pollutants += [(time , x["code"],x["fullName"],"pollutant",x["concentration"]["value"],x["concentration"]["units"]) for x in this_element['pollutants']]

  all_results = all_indexes + all_pollutants
  # generate "long format" dataframe
  res = pd.DataFrame(all_results,columns=["time","code","name","type","value","unit"])
  res["time"]=pd.to_datetime(res["time"])
  return res
