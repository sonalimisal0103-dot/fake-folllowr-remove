from instagrapi import Client
import time
import random
import sys
import os

print("🔥 Instagram Fake Followers Remover Tool")

# Exact Username (extra dot nahi hai)
USERNAME = "theharsh_.01"
PASSWORD = "HARSHAD00"   # ← Yahan apna password daal do

# Old session delete
if os.path.exists("session.json"):
    os.remove("session.json")

cl = Client()

try:
    print(f"Trying login with @{USERNAME}...")
    cl.login(USERNAME, PASSWORD)
    print("✅ Login Successful!")
    cl.dump_settings("session.json")
except Exception as e:
    print(f"❌ Login Failed: {e}")
    print("\nSuggestions:")
    print("1. Mobile data pe Instagram app se login kar")
    print("2. 2FA on hai to code daal")
    print("3. 1 ghanta wait kar ke phir try kar")
    sys.exit()

print(f"\nFetching followers of @{USERNAME}...")

followers = cl.user_followers(cl.user_id, amount=0)
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

print(f"\n🚨 Found {len(fake_list)} fake accounts")

unfollowed = 0
max_limit = 25

for username in fake_list:
    if unfollowed >= max_limit:
        print("Daily safe limit reached.")
        break
    try:
        uid = cl.user_id_from_username(username)
        cl.user_unfollow(uid)
        unfollowed += 1
        print(f"✅ Unfollowed @{username} ({unfollowed}/{max_limit})")
        time.sleep(random.uniform(40, 70))
    except:
        time.sleep(25)

print(f"\n🎉 Done! Total unfollowed: {unfollowed}")
