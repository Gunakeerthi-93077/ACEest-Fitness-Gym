from flask import Flask, request, render_template_string
import csv
from pathlib import Path

app = Flask(__name__)

PROGRAMS = {
    "Fat Loss": {
        "workout": "Cardio, brisk walking and full-body strength training",
        "diet": "Balanced meals with vegetables, protein and controlled portions"
    },
    "Muscle Gain": {
        "workout": "Progressive strength training and adequate recovery",
        "diet": "Protein-rich balanced meals with sufficient calories"
    },
    "Beginner": {
        "workout": "Light cardio, mobility exercises and basic strength training",
        "diet": "Balanced meals with fruits, vegetables and protein"
    }
}

PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>ACEest Fitness & Gym</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial; background: #171717; color: white;
               max-width: 850px; margin: 40px auto; padding: 20px; }
        h1 { color: #d4af37; }
        .card { background: #292929; padding: 22px; margin-top: 20px;
                border-radius: 10px; }
        select, button { padding: 10px; margin-top: 12px; }
        button { background: #d4af37; border: 0; cursor: pointer; }
    </style>
</head>
<body>
    <h1>ACEest Fitness & Gym</h1>
    <p>Your personal workout and diet planner</p>
    <div class="card">
        <h2>Select Your Fitness Program</h2>
        <form method="get">
            <select name="program">
                {% for name in programs %}
                <option value="{{ name }}"
                    {% if name == selected %}selected{% endif %}>
                    {{ name }}
                </option>
                {% endfor %}
            </select>
            <button type="submit">View Plan</button>
        </form>
    </div>
    <div class="card">
        <h2>Client Registration</h2>
        <form method="post" action="/client">
            <input name="client_name" placeholder="Client name" required>
            <input name="client_age" type="number" min="1" placeholder="Age" required>
            <button type="submit">Register Client</button>
        </form>
    </div>
    <div class="card">
        <h2>{{ selected }} Plan</h2>
        <h3>Workout</h3>
        <p>{{ plan.workout }}</p>
        <h3>Diet</h3>
        <p>{{ plan.diet }}</p>
    </div>
</body>
</html>
"""

@app.route("/client", methods=["POST"])
def register_client():
    name = request.form.get("client_name", "").strip()
    age = request.form.get("client_age", "").strip()
    if not name or not age:
        return "Client name and age are required", 400
    file_path = Path("clients.csv")
    write_header = not file_path.exists() or file_path.stat().st_size == 0
    with file_path.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if write_header:
            writer.writerow(["name", "age"])
        writer.writerow([name, age])
    return f"Client registered and saved: {name}, age {age}"

@app.route("/")
def home():
    selected = request.args.get("program", "Beginner")
    if selected not in PROGRAMS:
        selected = "Beginner"

    return render_template_string(
        PAGE,
        programs=PROGRAMS,
        selected=selected,
        plan=PROGRAMS[selected]
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
