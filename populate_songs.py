import httpx
import time

SONG_CATEGORIES = {
    "Telugu Pop": [
        "Ramuloo Ramulaa full video song",
        "Butta Bomma full video song",
        "Naatu Naatu video song RRR",
        "Srivalli pushpa video song telugu",
        "Oo Antava Mava Oo Oo Antava Mava video song",
        "Kurchi Madathapetti Mahesh Babu video song",
        "Hukum Jailer video song telugu",
        "Arabic Kuthu video song Beast telugu",
        "Kalaavathi Sarkaru Vaari Paata video song"
    ],
    "Hindi Hits": [
        "Tum Hi Ho Aashiqui 2 video song",
        "Chaleya Jawan video song",
        "Kesariya Brahmastra video song",
        "Raabta title track video song",
        "Param Sundari Mimi video song",
        "Zaalima Raees video song",
        "Kal Ho Naa Ho title track video song",
        "Kabira Yeh Jawaani Hai Deewani video song",
        "Nashe Si Chadh Gayi Befikre video song"
    ],
    "Telugu Melodies": [
        "Inkem Inkem Inkem Kaavaale Geetha Govindam",
        "Undiporaadhey Husharu",
        "Vachindamma Geetha Govindam",
        "Nijame Ne Chebutunna Oru Manam",
        "Priyathama Priyathama Majili",
        "Ninnu Kori Title Song",
        "Adiga Adiga Ninnu Kori",
        "Mellaga Tellarindoi Sankar Dada MBBS"
    ],
    "English Songs": [
        "Shape of You Ed Sheeran video song",
        "Blinding Lights The Weeknd video song",
        "Levitating Dua Lipa video song",
        "Dance Monkey Tones and I",
        "Stay The Kid LAROI Justin Bieber",
        "Believer Imagine Dragons",
        "Watermelon Sugar Harry Styles",
        "As It Was Harry Styles"
    ],
    "Entertainment": [
        "Pathaan - Jhoome Jo Pathaan Video Song",
        "Pushpa 2 - Angaaron Video Song",
        "Animal - Arjan Vailly Video Song",
        "Leo - Badass Video Song",
        "Fighter - Sher Khul Gaye Video Song"
    ],
    "Break Up": [
        "Channa Mereya Ae Dil Hai Mushkil",
        "Pachtaoge Arijit Singh",
        "Bekhayali Kabir Singh",
        "Agar Tum Saath Ho Tamasha",
        "Hamari Adhuri Kahani Title Track"
    ],
    "Still / Chill": [
        "Lofi Hip Hop Radio Beats to Relax",
        "Slow Reverb Bollywood Songs 2024",
        "Mellow Chill Beats for Study",
        "Nature Sounds Rain and Thunderstorm",
        "Acoustic Guitar Cover Popular Songs"
    ],
    "Recent Hits": [
        "Soulmate Badshah Arijit Singh",
        "O Maahi Dunki Video Song",
        "Vidaamuyarchi Song Ajith Kumar",
        "Illuminati Aavesham Video Song",
        "Tauba Tauba Bad Newz Video Song"
    ],
    "Trending": [
        "Pushpa Pushpa Pushpa 2 The Rule",
        "Fear Song Devara Movie",
        "Sooseki Pushpa 2 Song",
        "Manasilaayo Vettaiyan Song",
        "Tilasmi Bahein Heeramandi"
    ]
}

def populate():
    print("Starting backend population script...")
    with httpx.Client(timeout=30.0) as client:
        # Check backend
        try:
            client.get("http://127.0.0.1:5000/api/status")
        except httpx.ConnectError:
            print("Backend is not running at http://127.0.0.1:5000")
            return

        for category, queries in SONG_CATEGORIES.items():
            print(f"\n--- Populating {category} ---")
            for q in queries:
                print(f"Fetching '{q}'...")
                payload = {
                    "query": q,
                    "category": category
                }
                try:
                    r = client.post("http://127.0.0.1:5000/api/search", json=payload)
                    if r.status_code == 200:
                        data = r.json()
                        if data.get("success"):
                            node = data.get("node", {})
                            print(f"  -> Added {node.get('title')} ")
                        else:
                            print(f"  -> Error API returned: {data}")
                    else:
                        print(f"  -> Error HTTP {r.status_code}: {r.text}")
                except Exception as e:
                    print(f"  -> Request Exception: {e}")
                time.sleep(1) # Be nice to yt-dlp API

if __name__ == '__main__':
    populate()
