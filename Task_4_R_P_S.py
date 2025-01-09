import random
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rock Paper Scissors</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #A8E6CF, #DCEDC1);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            text-align: center;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        button {
            margin: 10px;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 5px;
            border: none;
            background-color: #A8E6CF;
            color: #333;
            cursor: pointer;
        }
        button:hover {
            background-color: #85C1A3;
        }
        .result {
            margin-top: 20px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Rock Paper Scissors</h1>
        <p>Choose your move:</p>
        <button onclick="playGame('rock')">Rock</button>
        <button onclick="playGame('paper')">Paper</button>
        <button onclick="playGame('scissors')">Scissors</button>
        <div class="result" id="result"></div>
        <button onclick="restartGame()">Restart Game</button>
    </div>
    <script>
        function playGame(playerChoice) {
            fetch('/play', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ choice: playerChoice })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('result').textContent = `Player: ${data.player} | Computer: ${data.computer} | Result: ${data.result}`;
            });
        }

        function restartGame() {
            document.getElementById('result').textContent = '';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/play', methods=['POST'])
def play():
    data = request.get_json()
    player_choice = data.get('choice')
    computer_choice = random.choice(['rock', 'paper', 'scissors'])

    if player_choice == computer_choice:
        result = "It's a tie!"
    elif (player_choice == 'rock' and computer_choice == 'scissors') or \
         (player_choice == 'scissors' and computer_choice == 'paper') or \
         (player_choice == 'paper' and computer_choice == 'rock'):
        result = "You win!"
    else:
        result = "You lose!"

    return jsonify({
        'player': player_choice,
        'computer': computer_choice,
        'result': result
    })

if __name__ == "__main__":
    app.run(debug=True)
