import requests,urllib
from keys import ACCESS_TOKEN,USER
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import matplotlib.pyplot as plt

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
    if user_id== None:
        print "No such user exists"
    else:
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
    if user_name==USER:
        request_url = base_url + "users/self/media/recent/?access_token=%s" % (ACCESS_TOKEN)

    else:
        request_url=base_url+"users/search?q=%s&access_token=%s"%(user_name,ACCESS_TOKEN)

    user_info=requests.get(request_url).json()
    if user_info["meta"]["code"]==200:
        if len(user_info["data"]):
            return user_info["data"][0]["id"]
        else :
            return None
    else:
        print  "Error in connection"


def get_post_self():
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


def get_media_id(user_name):
    user_id=get_user_id(user_name)
    request_url = base_url +"users/%s/media/recent/?access_token=%s"%(user_id,ACCESS_TOKEN)
    user_info = requests.get(request_url).json()
    if user_info["meta"]["code"] == 200:
        if len(user_info["data"][0]) > 0:
            return user_info["data"][0]["id"]
        else:
            return None
    else:
        print "Error in connection"
        return  None





def get_post_user(user_name):

    user_id=get_user_id(user_name)
    request_url = base_url +"users/%s/media/recent/?access_token=%s"%(user_id,ACCESS_TOKEN)
    user_info = requests.get(request_url).json()
    if user_info["meta"]["code"] == 200:
        if len(user_info["data"][0]) > 0:
            image_id=get_media_id(user_name)
            image_name =  image_id+ ".jpeg"
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


def get_comments_on_post(user_name):
    media_id=get_media_id(user_name)
    request_url1=base_url+"media/%s/comments?access_token=%s"%(media_id,ACCESS_TOKEN)
    comments_info=requests.get(request_url1).json()
    if comments_info["meta"]["code"]==200:
        comments_list=[]
        if len(comments_info["data"]):
                for i in range(len(comments_info["data"])):
                    text=comments_info["data"][i]["text"]
                    id=comments_info["data"][i]["id"]
                    comments_list.append([text,id])
                return  comments_list
        else:
                print "No comments on post!"


    else:
            print comments_info["meta"]["code"]
            print "error in connection"


def display_comments_on_post(user_name):
    list=get_comments_on_post(user_name)
    print "Comments:"
    for i in list:
        print i[0]


def like_recent_post(user_name):
            image_id = get_media_id(user_name)
            if image_id==None:
                print "No recent media of the user"
            else:
                url=base_url+"media/%s/likes"%(image_id)
                payload={"access_token":ACCESS_TOKEN}
                like=requests.post(url,payload).json()
                if like["meta"]["code"]==200:
                    print "Post liked!!"
                else:
                    print "Error in connection"


def comment_on_post(user_name):

        image_id = get_media_id(user_name)
        url=base_url+"media/%s/comments"%(image_id)
        comment_text=raw_input("your comment:")
        payload={"access_token":ACCESS_TOKEN,"text":comment_text}
        comment=requests.post(url,payload).json()
        if comment["meta"]["code"]==200:
            print "Your comment successfully posted!"
        else:
            print "Error in connection"



def delete_comment(user_name):
    media_id = get_media_id(user_name)
    request_url1 = base_url + "media/%s/comments?access_token=%s" % (media_id, ACCESS_TOKEN)
    comments_info = requests.get(request_url1).json()
    if comments_info["meta"]["code"] == 200:
        comments_list = []
        if len(comments_info["data"]):
            for i in range(len(comments_info["data"])):
                text = comments_info["data"][i]["text"]
                id = comments_info["data"][i]["id"]
                comments_list.append([text, id])
        for i in comments_list:
            text=TextBlob(i[0],analyzer=NaiveBayesAnalyzer())
            print  i[0] + " :" + text.sentiment.classification

        for i in comments_list:
            text = TextBlob(i[0], analyzer=NaiveBayesAnalyzer())
            if text.sentiment.classification=="neg":
                comment_id=i[1]
                request_url=base_url+"media/%s/comments/%s?access_token=%s"%(media_id,comment_id,ACCESS_TOKEN)
                response=requests.delete(request_url).json()
                if response["meta"]["code"]==200:
                    print "Comment deleted!!"

def display_pie_chart(user_name):
    comments_list=get_comments_on_post(user_name)
    pos=0
    neg=0
    for i in comments_list:
        text = TextBlob(i[0], analyzer=NaiveBayesAnalyzer())
        if text.sentiment.classification == "neg":
            neg+=1
        elif text.sentiment.classification == "pos":
            pos+=1

    labels = 'Positive Comments','Negative Comments'
    sizes = [pos,neg]
    colors = ["green","red"]
    explode = (0.1, 0)  # explode 1st slice

    # Plot
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)

    plt.axis('equal')
    plt.show()




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
        print "f.Get a list of comments on the recent post of a user\n"
        print "g.Like the recent post of a user\n"
        print "h.Make a comment on the recent post of a user\n"
        print "i.Delete negative comments from the recent post of a user\n"
        print "j.To display a pie chart displaying postive and negative comments\n"
        print "k.Exit\n"

        choice=raw_input("Enter your choice: ")
        if choice=="a":
            self_info()
        elif choice=="b":
            insta_username = raw_input("Enter the username of the user: ")
            otheruser_info(insta_username)
        elif choice=="c":
            get_post_self()
        elif choice=="d":
            insta_username = raw_input("Enter the username of the user: ")
            get_post_user(insta_username)
        elif choice=="e":
            get_recent_media_liked()
        elif choice=="f":
            user_name=raw_input("Enter the user name: ")
            display_comments_on_post(user_name)
        elif choice=="g":
            user_name=raw_input("Enter the user-name whose post you want to like: ")
            like_recent_post(user_name)
        elif choice=="h":
            user_name=raw_input("Enter the name of the user on whose post you want to comment: ")
            comment_on_post(user_name)
        elif choice=="i":
            user_name=raw_input("Enter the user-name: ")
            delete_comment(user_name)
        elif choice=="j":
            user_name=raw_input("Enter the username: ")
            display_pie_chart(user_name)
        elif choice=="k":
            exit()



start_bot()