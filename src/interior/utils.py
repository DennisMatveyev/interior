import mailchimp

api_key = "bad662754d41d4dbf8999d57a17c8324-us12"

def get_mailchimp_api():
    return mailchimp.Mailchimp(api_key)

