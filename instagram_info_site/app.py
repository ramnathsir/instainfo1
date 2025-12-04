from flask import Flask, render_template, request
import instaloader
import os

app = Flask(__name__)

def get_instagram_info(username: str):
    loader = instaloader.Instaloader()
    try:
        # optional login if needed:
        if os.getenv("IG_USER") and os.getenv("IG_PASS"):
            loader.login(os.getenv("IG_USER"), os.getenv("IG_PASS"))

        profile = instaloader.Profile.from_username(loader.context, username)
        info = {
            "Username": profile.username,
            "User ID": profile.userid,
            "Full Name": profile.full_name,
            "Bio": profile.biography,
            "Followers": profile.followers,
            "Following": profile.followees,
            "Posts": profile.mediacount,
            "Verified": profile.is_verified,
            "Private": profile.is_private,
            "Profile Pic URL": profile.profile_pic_url,
        }
        return info
    except Exception as e:
        return {"error": str(e)}

@app.route("/", methods=["GET", "POST"])
def index():
    data, error = None, None
    if request.method == "POST":
        username = request.form.get("username", "").strip().replace("@", "")
        data = get_instagram_info(username)
        if "error" in data:
            error, data = data["error"], None
    return render_template("index.html", data=data, error=error)

if __name__ == "__main__":
    app.run(debug=True)
