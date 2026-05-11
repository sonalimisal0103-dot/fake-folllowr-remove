from instagrapi import Client
import time
import random
import sys
import os

print("🔥 Instagram Login Tool (Forgot Password + 2FA Support)")

USERNAME = "lagxd71@gmail.com"
PASSWORD = "HARSHAD00"   # ← Yahan password daal do (agar yaad hai)

proxies = [
    "http://1351:IBd1Fk5CuUNZ@p101.squidproxies.com:9088",
]

def login_with_recovery():
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
            error = str(e).lower()
            if "challenge" in error or "verification" in error or "2fa" in error or "code" in error:
                print("🔐 Verification Code Required!")
                code = input("Instagram se aaya code yahan daal: ").strip()
                if code:
                    try:
                        cl.login(USERNAME, PASSWORD, verification_code=code)
                        cl.dump_settings("session.json")
                        print("✅ 2FA / Recovery Code Login Successful!")
                        return cl
                    except Exception as e2:
                        print(f"❌ Code Failed: {e2}")
                else:
                    print("❌ Code nahi diya")
            else:
                print(f"❌ Normal Login Failed: {e}")

            time.sleep(10)

    print("❌ Sab attempts fail ho gaye.")
    print("Forgot Password wala full flow Instagram app se karo.")
    sys.exit()

# ==================== LOGIN ====================
cl = login_with_recovery()

print(f"\nFetching followers of @{USERNAME}...")

followers = cl.user_followers(cl.user_id, amount=0)
print(f"Total Followers: {len(followers)}")

# Fake detection + unfollow code (pehle wala)
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
        time.sleep(20)

print(f"\n🎉 Done! Total unfollowed: {unfollowed}")
