from app import app

def test_home_page():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"ACEest Fitness &amp; Gym" in response.data or b"ACEest Fitness & Gym" in response.data

def test_fat_loss_plan():
    response = app.test_client().get("/?program=Fat%20Loss")
    assert response.status_code == 200
    assert b"Fat Loss Plan" in response.data

def test_muscle_gain_plan():
    response = app.test_client().get("/?program=Muscle%20Gain")
    assert response.status_code == 200
    assert b"Muscle Gain Plan" in response.data

def test_invalid_program_falls_back_to_beginner():
    response = app.test_client().get("/?program=invalid")
    assert response.status_code == 200
    assert b"Beginner Plan" in response.data
