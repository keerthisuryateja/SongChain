import httpx

try:
    with httpx.Client() as client:
        print("Testing fetch...")
        r = client.post("http://127.0.0.1:5000/api/search", json={"query": "never gonna give you up"})
        print(f"Status: {r.status_code}")
        print(r.json())
        
        print("Testing status...")
        r = client.get("http://127.0.0.1:5000/api/status")
        print(r.json())

except Exception as e:
    print(f"Error: {e}")
