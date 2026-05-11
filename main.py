from instagrapi import Client
import time
import json
import sys
from datetime import datetime

print("🔥 Instagram Fake Followers Remover Tool")

# ==================== CONFIG ====================
USERNAME = "theharsh_.01"          # ← Yahan apna username daal do
PASSWORD = "HARSHAD00"                      # ← Yahan apna password daal do

if not PASSWORD:
    print("❌ Password nahi diya! Code mein PASSWORD daal ke phir run karo.")
    sys.exit()

cl = Client()
cl.login(USERNAME, PASSWORD)
print("✅ Login Successful!")

user_id = cl.user_id_from_username(USERNAME)
print(f"Your Account: @{USERNAME}")

print("Fetching all followers... (thoda time lagega)")
followers = cl.user_followers(user_id, amount=0)

print(f"Total Followers: {len(followers)}")

fake_list = []

for uid, user in followers.items():
    score = 0
    reasons = []

    if not user.profile_pic_url or "default" in str(user.profile_pic_url):
        score += 3
        reasons.append("No Profile Pic")

    if user.follower_count < 20 and user.following_count > 100:
        score += 2
        reasons.append("Low Followers, High Following")

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

# Results
print("\n" + "="*60)
print(f"🚨 FAKE ACCOUNTS FOUND: {len(fake_list)}")
print("="*60)

for acc in fake_list[:50]:
    print(f"@{acc['username']} | Score: {acc['score']} | Followers: {acc['followers']} | Reasons: {', '.join(acc['reasons'])}")

# Save File
with open("fake_followers.json", "w", encoding="utf-8") as f:
    json.dump(fake_list, f, indent=4, ensure_ascii=False)

print(f"\n✅ Results saved in 'fake_followers.json'")
print("Ab Instagram pe jaake manually unfollow kar sakte ho.")

input("\nPress Enter to exit...")
