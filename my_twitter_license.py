#Substitute by Twtter OAuth information
#
#Use the access token string as your "oauth_token" and the access token secret as your "oauth_token_secret" to sign requests with your own Twitter account.
#
#Access_token         = '1493882754-hqzlGkz1enG4nhFTUcDZsAIyTTfYjVtHdc4N06b'
#Access_token_secret' =  1yrcMl2xZY2epcmV11DyiTQdo5Knawv9nTvGcu9BFRk'
#
#Your application's OAuth settings. This key should never be human-readable in your application.
#
#Consumer_key         = 'xie7Yc92GxZaqt3vxpPnnw'
#Consumer_secret      = 'htCBt4WW6G9yeHxqrXbgrxpmmCc4L9iHuSTlDit68g'

def get_license():
    my_access_token        = '1493882754-hqzlGkz1enG4nhFTUcDZsAIyTTfYjVtHdc4N06b'
    my_access_token_secret = '1yrcMl2xZY2epcmV11DyiTQdo5Knawv9nTvGcu9BFRk'
    my_consumer_key        = 'xie7Yc92GxZaqt3vxpPnnw'
    my_consumer_secret      = 'htCBt4WW6G9yeHxqrXbgrxpmmCc4L9iHuSTlDit68g'
    license  = (my_consumer_key,
                my_consumer_secret, # secret
                (my_access_token, 
                 my_access_token_secret)) #token
    return license
