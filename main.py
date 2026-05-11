from instagrapi import Client
import time
import random
import sys
import os

print("🔥 Instagram Login Tool - Email / Username Support")

# Yahan email ya username daal sakte ho
LOGIN_ID = "lagxd71@gmail.com"   # Ya email bhi daal sakte ho jaise "example@gmail.com"
PASSWORD = "HARSHAD00"               # Password daal do

# Proxy (optional)
PROXY = "http://1351:IBd1Fk5CuUNZ@p101.squidproxies.com:9088"

def try_login(login_id, password):
    for attempt in range(1, 6):
        print(f"\n🔄 Login Attempt {attempt}/5")

        if os.path.exists("session.json"):
            os.remove("session.json")

        cl = Client()
        if PROXY:
            cl.set_proxy(PROXY)
            print(f"🌐 Proxy use ho raha hai")

        try:
            cl.login(login_id, password)
            cl.dump_settings("session.json")
            print("✅ Login Successful!")
            return cl
        except Exception as e:
            print(f"❌ Attempt {attempt} Failed: {e}")
            time.sleep(random.randint(8, 20))

    print("❌ All attempts failed.")
    sys.exit()

# ==================== LOGIN ====================
cl = try_login(LOGIN_ID, PASSWORD)

print(f"\nFetching followers of @{LOGIN_ID}...")

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
