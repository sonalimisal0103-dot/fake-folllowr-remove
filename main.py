from instagrapi import Client
import time
import random
import sys
import os

print("🔥 Instagram Fake Followers Remover Tool - Unlimited Login Try")

USERNAME = "theharsh_.01"
PASSWORD = "HARSHAD00"   # ← Yahan apna password daal do

def unlimited_login():
    attempt = 0
    while True:
        attempt += 1
        print(f"\n🔄 Login Attempt #{attempt}")

        # Purani session delete
        if os.path.exists("session.json"):
            os.remove("session.json")

        cl = Client()

        try:
            cl.login(USERNAME, PASSWORD)
            cl.dump_settings("session.json")
            print("✅ Login Successful!")
            return cl
        except Exception as e:
            print(f"❌ Attempt #{attempt} Failed: {e}")

            # Random safe delay
            wait = random.randint(15, 40)
            print(f"   Waiting {wait} seconds before next try...")
            time.sleep(wait)

            if attempt % 10 == 0:
                print("   10 attempts ho gaye... Thoda break le raha hoon (1 minute)")
                time.sleep(60)

# ==================== UNLIMITED LOGIN ====================
cl = unlimited_login()

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

# Slow Unfollow
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
