
from flask import Flask
import sqlite3
from pathlib import Path

app = Flask(__name__)

DATABASE = Path(__file__).parent / "visits.db"


def get_visit_count():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS visits (
                id INTEGER PRIMARY KEY,
                count INTEGER NOT NULL
            )
        """)

        conn.execute(
            "INSERT OR IGNORE INTO visits (id, count) VALUES (1, 0)"
        )

        conn.execute(
            "UPDATE visits SET count = count + 1 WHERE id = 1"
        )

        count = conn.execute(
            "SELECT count FROM visits WHERE id = 1"
        ).fetchone()[0]

        conn.commit()

    return count


@app.route("/viikko2/")
def home():
    visits = get_visit_count()

    return f"""

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>My Python Web App  Week 2</title>

    <style>
        body {{
            max-width: 850px;
            margin: 0px auto;
            padding: 25px;
            background: #151515;
            color: #f2f2f2;
            font-family: Arial, sans-serif;
            line-height: 1.8;
        }}

        h1 {{
            color: #ffd54a;
            font-size: 38px;
        }}

        h2 {{
            color: #ffd54a;
            margin-top: 40px;
        }}

        p {{
            font-size: 16px;
        }}

        .counter {{
            font-size: 42px;
            font-weight: bold;
            color: #ffd54a;
        }}
	a {{
    	    color: #4ade80;
	}}
    </style>
</head>

<body>
<h1>My Python Web Application</h1>

    <p>Welcome to Week 2 of my Linux web server project.</p>

    <h2>Visitor Counter</h2>
    <p class="counter">{visits}</p>

<h2>How does it work?</h2>
<p>
 	This webpage uses Python Flask and an SQLite database.
        Every time the page loads the visitor counter increases
        by one. SQLite saves the count so it is not lost when
        the application restarts.

<h2>Reboot Test</h2>
<p>
	I restarted my Ubuntu server to test the application.
	After the reboot, both my Week 1 and Week 2 websites
	were still working. The visitor counter continued
    	increasing from its previous value instead of
    	resetting, confirming that SQLite stores the count
    	permanently.
</p>

    </p>

<h2>Project Source Code</h2>
<p>
    You can view my Python application on
    <a href="https://github.com/konstaojala/linux-web-server-week2">
        GitHub
    </a>.
</p>

</body>
</html>
    """


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
