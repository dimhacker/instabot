import requests

ACCESS_TOKEN="5653107991.5798332.fed3d45ca97e4bff9b0f4d743679c8fa"
lat=30.62584
long=76.99376
base_url="https://api.instagram.com/v1/"

def get_captions_on_post():
    user_name=raw_input("Enter the name of the user: ")
    user_id=get_user_id(user_name)
    request_url = base_url +"users/%s/media/recent/?access_token=%s"%(user_id,ACCESS_TOKEN)
    user_info = requests.get(request_url).json()
    if user_info["meta"]["code"] == 200:
        if len(user_info["data"]) > 0:
            captions_list=[]
            for i in range(len(user_info["data"])):
                captions_list.append(user_info["data"][i]["caption"]["text"])
            return captions_list
        else:
            return None
    else:
        print  "Error in connection"
        return  None


def analysing_captions():
    captions_list=get_captions_on_post()
    nouns=[]
    for i in captions_list:
        list=TextBlob(i).noun_phrases
        nouns.extend(list)
    print nouns



def getting_nearby_location_id(lat,long):
    request_url="https://api.instagram.com/v1/locations/search?lat=%f&lng=%f&access_token=%s"%(lat,long,ACCESS_TOKEN)
    response=requests.get(request_url).json()
    if response["meta"]["code"]==200:
        for i  in range(len(response["data"])):
            print response["data"][i]["id"] + " : " + response["data"][i]["name"]

def getting_location_coordinates(location_id):
    request_url="https://api.instagram.com/v1/locations/%d?access_token=%s"%(location_id,ACCESS_TOKEN)
    response=requests.get(request_url).json()
    print response["data"]



def get_user_id(user_name):

    request_url=base_url+"users/search?q=%s&access_token=%s"%(user_name,ACCESS_TOKEN)

    user_info=requests.get(request_url).json()
    if user_info["meta"]["code"]==200:
        if len(user_info["data"]):
            return user_info["data"][0]["id"]
        else :
            return None
    else:
        print  "Error in connection"



def get_post_user(user_name):

    user_id=get_user_id(user_name)
    request_url = base_url +"users/%s/media/recent/?access_token=%s"%(user_id,ACCESS_TOKEN)
    user_info = requests.get(request_url).json()
    if user_info["meta"]["code"] == 200:
        if len(user_info["data"]) > 0:
            print "Location id: %s"%(user_info["data"][0]["location"]["id"])
            print "Location id: %s"%(user_info["data"][1]["location"]["id"])



#getting_nearby_location_id(lat=30.6723,long=76.8563)
#getting_location_coordinates(267457779 )
print "next"
#getting_location_coordinates(1210732955646121)
get_post_user("piyush3666")