from urllib.parse import quote


def test_get_activities_returns_data(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_adds_participant(client):
    email = "tester@example.com"
    activity = quote("Chess Club", safe="")
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200

    data = client.get("/activities").json()
    participants = data["Chess Club"]["participants"]
    assert email in participants


def test_unregister_removes_participant(client):
    email = "remover@example.com"
    activity = quote("Programming Class", safe="")
    # sign up first
    r = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r.status_code == 200

    # then remove
    r = client.delete(f"/activities/{activity}/participants", params={"email": email})
    assert r.status_code == 200

    data = client.get("/activities").json()
    assert email not in data["Programming Class"]["participants"]


def test_duplicate_signup_allowed(client):
    email = "dup@example.com"
    activity = quote("Gym Class", safe="")
    r1 = client.post(f"/activities/{activity}/signup", params={"email": email})
    r2 = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r1.status_code == 200 and r2.status_code == 200

    data = client.get("/activities").json()
    occurrences = [p for p in data["Gym Class"]["participants"] if p == email]
    assert len(occurrences) == 2
