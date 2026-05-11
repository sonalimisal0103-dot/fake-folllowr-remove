from instagrapi import Client
import time
import random
import sys
import os

print("🔥 Instagram Fake Followers Remover Tool (Improved Login)")

USERNAME = "theharsh_.01"
PASSWORD = "HARSHAD00"   # ← Yahan password daal do

proxies = [
    "http://1351:IBd1Fk5CuUNZ@p101.squidproxies.com:9088",
    # Agar aur proxies hain to yahan add kar sakte ho
]

def login_with_retry():
    for attempt in range(3):
        proxy = random.choice(proxies) if proxies else None
        cl = Client()
        
        if proxy:
            cl.set_proxy(proxy)
            print(f"🌐 Attempt {attempt+1} | Proxy: {proxy[:30]}...")

        try:
            # Session forget karne ke liye
            if os.path.exists("session.json"):
                os.remove("session.json")
            
            cl.login(USERNAME, PASSWORD)
            cl.dump_settings("session.json")   # session save kar diya
            print("✅ Login Successful!")
            return cl
            
        except Exception as e:
            print(f"❌ Attempt {attempt+1} Failed: {e}")
            time.sleep(10)

    print("❌ All attempts failed. Proxy change karo ya 1-2 ghante baad try karo.")
    sys.exit()

# Login karo
cl = login_with_retry()

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

    except Exception as e:
        print(f"Error on @{username}: {e}")
        time.sleep(30)

print(f"\n🎉 Done! Total unfollowed: {unfollowed}")
