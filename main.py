from instagrapi import Client
import time
import random
import sys

print("🔥 Instagram Fake Followers Auto Unfollow Tool")

USERNAME = "theharsh_.01"
PASSWORD = "HARSHAD00"   # ← Yahan apna password daal do

# Proxy set kiya hai
PROXY = "http://1351:IBd1Fk5CuUNZ@p101.squidproxies.com:9088"

cl = Client()

if PROXY:
    cl.set_proxy(PROXY)
    print(f"🌐 Proxy Connected: p101.squidproxies.com:9088")

try:
    cl.login(USERNAME, PASSWORD)
    print("✅ Login Successful!")
except Exception as e:
    print(f"❌ Login Failed: {e}")
    print("Proxy change karo ya mobile data use karo")
    sys.exit()

user_id = cl.user_id_from_username(USERNAME)
print(f"Fetching followers of @{USERNAME}...")

followers = cl.user_followers(user_id, amount=0)
print(f"Total Followers: {len(followers)}")

fake_list = []

for uid, user in followers.items():
    score = 0
    if not user.profile_pic_url or "default" in str(user.profile_pic_url):
        score += 4
    if user.follower_count < 25 and user.following_count > 150:
        score += 3
    if user.media_count == 0:
        score += 3

    if score >= 6:
        fake_list.append(user.username)

print(f"Found {len(fake_list)} fake accounts")

# Slow Unfollow
print("\nStarting slow unfollow...")

unfollowed = 0
max_limit = 25   # Safe limit

for username in fake_list:
    if unfollowed >= max_limit:
        print("Daily limit reached.")
        break

    try:
        uid = cl.user_id_from_username(username)
        cl.user_unfollow(uid)
        unfollowed += 1
        print(f"✅ Unfollowed @{username} ({unfollowed}/{max_limit})")

        delay = random.uniform(40, 65)
        time.sleep(delay)

    except Exception as e:
        print(f"Error on @{username}: {e}")
        time.sleep(25)

print(f"\n🎉 Done! Total unfollowed: {unfollowed}")
