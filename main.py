from instagrapi import Client
import time
import random
import sys

print("🔥 Instagram Fake Followers Remover Tool + Proxy System")

USERNAME = "lagxd71@gmail.com"
PASSWORD = "HARSHAD00"   # ← Yahan password daal do

# ==================== PROXIES ====================
proxies = [
    "http://1351:IBd1Fk5CuUNZ@p101.squidproxies.com:9088",
    # Agar aur proxies hain to yahan add kar sakte ho
]

def try_login():
    for attempt in range(5):
        proxy = random.choice(proxies)
        print(f"🌐 Attempt {attempt+1} | Proxy: {proxy[:50]}...")

        cl = Client()
        cl.set_proxy(proxy)

        try:
            cl.login(USERNAME, PASSWORD)
            print("✅ Login Successful!")
            return cl
        except Exception as e:
            print(f"❌ Failed: {e}")
            time.sleep(8)

    print("❌ Sab proxies fail ho gaye.")
    sys.exit()

# Login
cl = try_login()

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
unfollowed = 0
max_limit = 25

for username in fake_list:
    if unfollowed >= max_limit:
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
