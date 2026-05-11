from instagrapi import Client
import time

cl = Client()

# Important settings for less detection
cl.set_user_agent("Instagram 289.0.0.0.0 Android")
cl.set_device("android")
cl.set_locale("en_US")
cl.set_timezone_offset(19800)  # IST

USERNAME = "theharsh_.01"
PASSWORD = "HARSHAD00"

try:
    cl.login(USERNAME, PASSWORD)
    print("✅ Login ho gaya!")
except Exception as e:
    print("Error:", e)
