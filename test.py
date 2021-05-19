import random

def sendOtp():
    email = "rakesh"
    sentOtp = ""
    for i in range(6):
        sentOtp +=  str(random.randrange(0, 10))
    return (email, sentOtp)

def handleSignUp():
  print(sendOtp()[0], sendOtp()[1])

handleSignUp()