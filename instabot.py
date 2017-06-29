import requests,urllib
from keys import ACCESS_TOKEN
base_url="https://api.instagram.com/v1/"

def self_info():
    request_url=base_url+"users/self/?access_token=%s"  %ACCESS_TOKEN
    user_info=requests.get(request_url).json()
    if user_info["meta"]["code"]==200:
        print "Username:%s"%(user_info["data"]["username"])
        print "Full name:%s"%(user_info["data"]["full_name"])
        print "User ID:%s"%user_info["data"]["id"]
        print "Follows:%s" % user_info["data"]["counts"]["follows"]
        print "Followed By:%s"%(user_info["data"]["counts"]["followed_by"])
        print 'No. of posts: %s' % (user_info['data']['counts']['media'])
    else:
        print "No such user exists!"


def otheruser_info(user_name):
    user_id=get_user_id(user_name)
    request_url=base_url+"users/%s/?access_token=%s"% (user_id,ACCESS_TOKEN)
    user_info=requests.get(request_url).json()
    if user_info["meta"]["code"]==200:
        if len(user_info["data"])>0:
            print "Username:%s" % (user_info["data"]["username"])
            print "Full name:%s" % (user_info["data"]["full_name"])
            print "User ID:%s" % user_info["data"]["id"]
            print "Follows:%s"%(user_info["data"]["counts"]["follows"])
            print "Followed By:%s" % (user_info["data"]["counts"]["followed_by"])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            "This user doesn't have any data."
    else:
        print "Error in connecting to web!"


def get_user_id(user_name):
    request_url=base_url+"users/search?q=%s&access_token=%s"%(user_name,ACCESS_TOKEN)
    user_info=requests.get(request_url).json()
    if user_info["meta"]["code"]==200:
        return user_info["data"][0]["id"]


def get_recent_post_self():
    request_url=base_url+"users/self/media/recent/?access_token=%s"%(ACCESS_TOKEN)
    user_info = requests.get(request_url).json()
    if user_info["meta"]["code"] == 200:
        if len(user_info["data"][0])>0:
            image_name=user_info["data"][0]["id"]+".jpeg"
            image_url=user_info["data"][0]["images"]["standard_resolution"]["url"]
            urllib.urlretrieve(image_url,image_name)

        else:
            print "No recent post!!"
    else:
        print "Error in connecting to web!"


def get_post_user(user_name):
    user_id=get_user_id(user_name)
    request_url = base_url +"users/%s/media/recent/?access_token=%s"%(user_id,ACCESS_TOKEN)
    user_info = requests.get(request_url).json()
    if user_info["meta"]["code"] == 200:
        if len(user_info["data"][0]) > 0:
            image_name = user_info["data"][0]["id"] + ".jpeg"
            image_url = user_info["data"][0]["images"]["standard_resolution"]["url"]
            urllib.urlretrieve(image_url, image_name)
            print "Picture downloaded!!"

        else:
            print "No recent post!!"
    else:
        print "Error in connecting to web!"


def get_recent_media_liked():
    request_url=base_url+"users/self/media/liked?access_token=%s"%ACCESS_TOKEN
    media_info=requests.get(request_url).json()
    if media_info["meta"]["code"]==200:
        url=media_info["data"][0]["images"]["standard_resolution"]["url"]+".jpeg"
        url_id=media_info["data"][0]["id"]
        urllib.urlretrieve(url,url_id)
        print "Your recently liked image downloaded!"


def get_comments_on_your_recentpost():
    request_url=base_url+"users/self/media/recent/?access_token=%s"%(ACCESS_TOKEN)
    user_info = requests.get(request_url).json()
    if user_info["meta"]["code"] == 200:
        media_id=user_info["data"][0]["id"]
        request_url1=base_url+"media/%s/comments"%(media_id)
        comments_info=requests.get(request_url1).json()
        if comments_info["meta"]["code"]==200:

            comments_list=[]
            for i in range(len(user_info["data"])):

                comments_list.append(user_info["data"][i]["text"])
            return  comments_list



        else:
            print comments_info["meta"]["code"]
            print "error in connection"


def like_recent_post(user_name):
    user_id=get_user_id(user_name)
    request_url = base_url +"users/%s/media/recent/?access_token=%s"%(user_id,ACCESS_TOKEN)
    user_info = requests.get(request_url).json()
    if user_info["meta"]["code"] == 200:
        if len(user_info["data"][0]) > 0:
            image_id = user_info["data"][0]["id"]
            url=base_url+"media/%s/likes"%(ACCESS_TOKEN)
            payload={"access_token":ACCESS_TOKEN}
            like=requests.post(url,payload).json()
            if like["meta"]["code"]==200:
                print "Post liked!!"
            else:
                print "Error in connection"
        else:
            print "No recent post!"
    else:
        print "Error in connection"


def comment_on_post(user_name):
    user_id=get_user_id(user_name)
    request_url = base_url +"users/%s/media/recent/?access_token=%s"%(user_id,ACCESS_TOKEN)
    user_info = requests.get(request_url).json()
    if user_info["meta"]["code"] == 200:
        image_id = user_info["data"][0]["id"]
        url=base_url+"media/%s/comments"%(image_id)
        comment_text=raw_input("your comment:")
        payload={"access_token":ACCESS_TOKEN,"text":comment_text}
        comment=requests.post(url,payload).json()
        if comment["meta"]["code"]==200:
            print "Your comment successfully posted!"
        else:
            print "Error in connection"

    else:
        print "Error in connection"


def delete_comment():
    list=get_comments_on_your_recentpost()
    inappropriate_words=[]
    for i in list:
        pass






def start_bot():
    while True:
        print '\n'
        print 'Hey! Welcome to instaBot!'
        print 'Here are your menu options:'
        print "a.Get your own details\n"
        print "b.Get details of a user by username\n"
        print "c.Get your own recent post\n"
        print "d.Get the recent post of a user by username\n"
        print "e.Get the recent media like by the user\n"
        print "f.Comments on your recent post\n"
        print "g.Get a list of comments on the recent post of a user\n"
        print "h.Like the recent post of a user\n"

        print "i.Make a comment on the recent post of a user\n"
        print "j.Delete negative comments from the recent post of a user\n"
        print "k.Exit\n"

        choice=raw_input("Enter your choice: ")
        if choice=="a":
            self_info()
        elif choice=="b":
            insta_username = raw_input("Enter the username of the user: ")
            otheruser_info(insta_username)
        elif choice=="c":
            get_recent_post_self()
        elif choice=="d":
            insta_username = raw_input("Enter the username of the user: ")
            get_post_user(insta_username)
        elif choice=="e":
            get_recent_media_liked()
        elif choice=="f":
            list=get_comments_on_your_recentpost()
            print "Comments:"
            for i in list:
                print i



        elif choice=="h":
            user_name=raw_input("Enter the user-name whose post you want to like:")
            like_recent_post(user_name)
        elif choice=="i":
            user_name=raw_input("Enter the name of the user on whose post you want to comment:")
            like_recent_post(user_name)

        elif choice=="j":
            exit()


start_bot()