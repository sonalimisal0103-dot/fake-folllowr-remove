from instagrapi import Client
import time
import random
import sys
import os

print("🔥 Instagram Fake Followers Remover Tool (2FA Support)")

USERNAME = "theharsh_.01"
PASSWORD = "HARSHAD00"   # ← Yahan apna password daal do

proxies = [
    "http://1351:IBd1Fk5CuUNZ@p101.squidproxies.com:9088",
]

def login_with_2fa():
    for attempt in range(3):
        print(f"\n🔄 Login Attempt {attempt+1}/3")

        if os.path.exists("session.json"):
            os.remove("session.json")

        cl = Client()

        proxy = random.choice(proxies)
        cl.set_proxy(proxy)
        print(f"🌐 Using Proxy → {proxy[:40]}...")

        try:
            cl.login(USERNAME, PASSWORD)
            cl.dump_settings("session.json")
            print("✅ Login Successful!")
            return cl

        except Exception as e:
            error_str = str(e).lower()
            if "two_factor" in error_str or "2fa" in error_str or "verification" in error_str:
                print("🔐 2FA Code Required!")
                code = input("Enter 2FA Code from Instagram: ").strip()
                if code:
                    try:
                        cl.login(USERNAME, PASSWORD, verification_code=code)
                        cl.dump_settings("session.json")
                        print("✅ 2FA Login Successful!")
                        return cl
                    except Exception as e2:
                        print(f"❌ 2FA Failed: {e2}")
                else:
                    print("❌ Code nahi diya")
            else:
                print(f"❌ Attempt Failed: {e}")

            time.sleep(10)

    print("❌ All attempts failed.")
    sys.exit()

# ==================== LOGIN ====================
cl = login_with_2fa()

user_id = cl.user_id_from_username(USERNAME)
print(f"\nFetching followers of @{USERNAME}...")

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
        time.sleep(25)

print(f"\n🎉 Done! Total unfollowed: {unfollowed}")
