from flask import Flask, render_template_string, request, jsonify
import random
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key')

# Initialize the game board and scores
board = [''] * 9
scores = {'X': 0, 'O': 0}
game_over = False

def check_winner(board):
    # Check rows
    for i in range(0, 9, 3):
        if board[i] == board[i+1] == board[i+2] != '':
            return board[i]
    
    # Check columns
    for i in range(3):
        if board[i] == board[i+3] == board[i+6] != '':
            return board[i]
    
    # Check diagonals
    if board[0] == board[4] == board[8] != '':
        return board[0]
    if board[2] == board[4] == board[6] != '':
        return board[2]
    
    # Check for draw
    if '' not in board:
        return 'draw'
    
    return None

def get_available_moves(board):
    return [i for i, cell in enumerate(board) if cell == '']

def computer_move(board):
    # Get available moves
    available_moves = get_available_moves(board)
    
    # 1. Check if computer can win
    for move in available_moves:
        board[move] = 'O'
        if check_winner(board) == 'O':
            board[move] = ''
            return move
        board[move] = ''
    
    # 2. Check if human can win and block
    for move in available_moves:
        board[move] = 'X'
        if check_winner(board) == 'X':
            board[move] = ''
            return move
        board[move] = ''
    
    # 3. Take center if available
    if 4 in available_moves:
        return 4
    
    # 4. Take corners if available
    corners = [0, 2, 6, 8]
    available_corners = [corner for corner in corners if corner in available_moves]
    if available_corners:
        return random.choice(available_corners)
    
    # 5. Take any available side
    return random.choice(available_moves)

@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Tic Tac Toe</title>
            <style>
                body {
                    font-family: 'Arial', sans-serif;
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    min-height: 100vh;
                    margin: 0;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                }
                .container {
                    background: white;
                    padding: 2rem;
                    border-radius: 15px;
                    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
                    text-align: center;
                }
                .scoreboard {
                    display: flex;
                    justify-content: space-around;
                    margin-bottom: 20px;
                    font-size: 1.5rem;
                }
                .score {
                    padding: 10px 20px;
                    border-radius: 10px;
                    background: #f0f0f0;
                }
                .board {
                    display: grid;
                    grid-template-columns: repeat(3, 100px);
                    gap: 5px;
                    margin: 20px auto;
                    width: 310px;
                }
                .cell {
                    width: 100px;
                    height: 100px;
                    border: 2px solid #333;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 40px;
                    cursor: pointer;
                    background-color: #fff;
                    transition: all 0.3s ease;
                    border-radius: 5px;
                }
                .cell:hover {
                    background-color: #f0f0f0;
                    transform: scale(1.05);
                }
                .cell.X {
                    color: #2196F3;
                }
                .cell.O {
                    color: #FF5722;
                }
                .status {
                    text-align: center;
                    font-size: 24px;
                    margin: 20px;
                    font-weight: bold;
                }
                .reset {
                    display: block;
                    margin: 20px auto;
                    padding: 12px 24px;
                    font-size: 18px;
                    background: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }
                .reset:hover {
                    background: #45a049;
                    transform: scale(1.05);
                }
                .winner {
                    animation: winner 0.5s ease infinite;
                }
                @keyframes winner {
                    0% { transform: scale(1); }
                    50% { transform: scale(1.1); }
                    100% { transform: scale(1); }
                }
                .game-over {
                    pointer-events: none;
                    opacity: 0.7;
                }
                .computer-thinking {
                    pointer-events: none;
                    opacity: 0.7;
                }
            </style>
            <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
        </head>
        <body>
            <div class="container">
                <div class="scoreboard">
                    <div class="score">You: <span id="scoreX">0</span></div>
                    <div class="score">Computer: <span id="scoreO">0</span></div>
                </div>
                <div class="status">Your turn (X)</div>
                <div class="board">
                    {% for i in range(9) %}
                    <div class="cell" onclick="makeMove({{ i }})" id="cell-{{ i }}"></div>
                    {% endfor %}
                </div>
                <button class="reset" onclick="resetGame()">Reset Game</button>
            </div>

            <script>
                let gameOver = false;
                
                function triggerConfetti() {
                    confetti({
                        particleCount: 100,
                        spread: 70,
                        origin: { y: 0.6 }
                    });
                }

                function updateScore(winner) {
                    if (winner === 'X' || winner === 'O') {
                        const scoreElement = document.getElementById(`score${winner}`);
                        scoreElement.textContent = parseInt(scoreElement.textContent) + 1;
                    }
                }

                function makeMove(index) {
                    if (gameOver) return;
                    
                    fetch('/move', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({index: index})
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.valid) {
                            // Human move
                            const cell = document.getElementById(`cell-${index}`);
                            cell.textContent = 'X';
                            cell.classList.add('X');
                            
                            if (data.winner) {
                                handleGameEnd(data.winner);
                            } else {
                                // Computer's turn
                                document.querySelector('.board').classList.add('computer-thinking');
                                document.querySelector('.status').textContent = 'Computer thinking...';
                                
                                // Make computer move immediately
                                fetch('/computer_move', {
                                    method: 'POST'
                                })
                                .then(response => response.json())
                                .then(data => {
                                    if (data.valid) {
                                        const cell = document.getElementById(`cell-${data.index}`);
                                        cell.textContent = 'O';
                                        cell.classList.add('O');
                                        
                                        if (data.winner) {
                                            handleGameEnd(data.winner);
                                        } else {
                                            document.querySelector('.board').classList.remove('computer-thinking');
                                            document.querySelector('.status').textContent = 'Your turn (X)';
                                        }
                                    }
                                });
                            }
                        } else {
                            alert(data.message);
                        }
                    });
                }

                function handleGameEnd(winner) {
                    gameOver = true;
                    document.querySelector('.board').classList.add('game-over');
                    updateScore(winner);
                    
                    if (winner !== 'draw') {
                        triggerConfetti();
                        document.querySelectorAll('.cell').forEach(cell => {
                            if (cell.textContent === winner) {
                                cell.classList.add('winner');
                            }
                        });
                    }
                    
                    setTimeout(resetGame, 3000);
                }

                function resetGame() {
                    fetch('/reset', {
                        method: 'POST'
                    })
                    .then(response => response.json())
                    .then(data => {
                        document.querySelectorAll('.cell').forEach(cell => {
                            cell.textContent = '';
                            cell.classList.remove('X', 'O', 'winner');
                        });
                        document.querySelector('.board').classList.remove('game-over', 'computer-thinking');
                        document.querySelector('.status').textContent = 'Your turn (X)';
                        gameOver = false;
                    });
                }
            </script>
        </body>
        </html>
    ''')

@app.route('/move', methods=['POST'])
def make_move():
    global board, scores, game_over
    data = request.get_json()
    index = data['index']
    
    if game_over or board[index] != '':
        return jsonify({'valid': False, 'message': 'Invalid move!'})
    
    board[index] = 'X'
    winner = check_winner(board)
    
    if winner:
        if winner == 'draw':
            message = "It's a draw!"
        else:
            message = f"Player {winner} wins!"
            scores[winner] += 1
        game_over = True
        return jsonify({'valid': True, 'message': message, 'winner': winner})
    
    return jsonify({'valid': True, 'message': 'Computer thinking...'})

@app.route('/computer_move', methods=['POST'])
def computer_move_endpoint():
    global board, scores, game_over
    if game_over:
        return jsonify({'valid': False, 'message': 'Game is over!'})
    
    move = computer_move(board)
    board[move] = 'O'
    
    winner = check_winner(board)
    if winner:
        if winner == 'draw':
            message = "It's a draw!"
        else:
            message = f"Player {winner} wins!"
            scores[winner] += 1
        game_over = True
        return jsonify({'valid': True, 'index': move, 'message': message, 'winner': winner})
    
    return jsonify({'valid': True, 'index': move, 'message': 'Your turn (X)'})

@app.route('/reset', methods=['POST'])
def reset_game():
    global board, game_over
    board = [''] * 9
    game_over = False
    return jsonify({'message': 'Game reset'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000))) 