from instagrapi import Client
import json
import sys

print("🔥 Instagram Fake Followers Remover Tool")

USERNAME = "theharsh_.01"
PASSWORD = "HARSHAD00"                    # ← Yahan apna password daal do

# Proxy set kiya hai
PROXY = "http://1351:IBd1Fk5CuUNZ@p101.squidproxies.com:9088"

if not PASSWORD:
    print("❌ Password daal do code mein!")
    sys.exit()

cl = Client()
cl.set_proxy(PROXY)
print(f"🌐 Proxy Connected: p101.squidproxies.com:9088")

try:
    cl.login(USERNAME, PASSWORD)
    print("✅ Login Successful!")
except Exception as e:
    print(f"❌ Login Failed: {e}")
    print("\nTips:")
    print("1. Password sahi hai ya nahi check kar")
    print("2. 2FA enabled hai to code bhi daalna padega")
    print("3. Agar phir bhi nahi ho raha to proxy change karo")
    sys.exit()

print(f"\nFetching followers of @{USERNAME}...")

followers = cl.user_followers(cl.user_id, amount=0)
print(f"Total Followers: {len(followers)}")

fake_list = []

for uid, user in followers.items():
    score = 0
    reasons = []

    if not user.profile_pic_url or "default" in str(user.profile_pic_url):
        score += 3
        reasons.append("No DP")

    if user.follower_count < 20 and user.following_count > 100:
        score += 2
        reasons.append("Ghost")

    if user.media_count == 0:
        score += 2
        reasons.append("No Posts")

    if score >= 4:
        fake_list.append({
            "username": user.username,
            "score": score,
            "reasons": reasons,
            "followers": user.follower_count,
            "following": user.following_count
        })

print("\n" + "="*55)
print(f"🚨 FAKE ACCOUNTS FOUND: {len(fake_list)}")
print("="*55)

for acc in sorted(fake_list, key=lambda x: x , reverse=True)[:40]:
    print(f"@{acc :20} | Score: {acc } | Followers: {acc }")

# Save results
with open("fake_followers.json", "w", encoding="utf-8") as f:
    json.dump(fake_list, f, indent=4, ensure_ascii=False)

print(f"\n✅ Results saved in 'fake_followers.json'")
print("Ab Instagram pe jaake manually unfollow kar sakte ho.")
