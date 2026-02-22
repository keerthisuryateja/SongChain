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
    "Global Hits": [
        "Shape of You Ed Sheeran video song",
        "Blinding Lights The Weeknd video song",
        "Levitating Dua Lipa video song",
        "Dance Monkey Tones and I",
        "Stay The Kid LAROI Justin Bieber",
        "Believer Imagine Dragons",
        "Watermelon Sugar Harry Styles",
        "As It Was Harry Styles"
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
