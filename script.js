// Game state
let board = ['', '', '', '', '', '', '', '', ''];
let scores = { 'X': 0, 'O': 0 };
let gameOver = false;
let isComputerTurn = false;

// DOM elements
const cells = document.querySelectorAll('.cell');
const status = document.querySelector('.status');
const scoreX = document.getElementById('scoreX');
const scoreO = document.getElementById('scoreO');

// Initialize the game
function initGame() {
    cells.forEach(cell => {
        cell.addEventListener('click', () => makeMove(parseInt(cell.dataset.index)));
    });
}

// Check for winner
function checkWinner(board) {
    // Check rows
    for (let i = 0; i < 9; i += 3) {
        if (board[i] && board[i] === board[i + 1] && board[i] === board[i + 2]) {
            return board[i];
        }
    }

    // Check columns
    for (let i = 0; i < 3; i++) {
        if (board[i] && board[i] === board[i + 3] && board[i] === board[i + 6]) {
            return board[i];
        }
    }

    // Check diagonals
    if (board[0] && board[0] === board[4] && board[0] === board[8]) {
        return board[0];
    }
    if (board[2] && board[2] === board[4] && board[2] === board[6]) {
        return board[2];
    }

    // Check for draw
    if (!board.includes('')) {
        return 'draw';
    }

    return null;
}

// Get available moves
function getAvailableMoves(board) {
    return board.map((cell, index) => cell === '' ? index : null).filter(index => index !== null);
}

// Computer move
function computerMove() {
    const availableMoves = getAvailableMoves(board);

    // 1. Check if computer can win
    for (const move of availableMoves) {
        board[move] = 'O';
        if (checkWinner(board) === 'O') {
            board[move] = '';
            return move;
        }
        board[move] = '';
    }

    // 2. Check if human can win and block
    for (const move of availableMoves) {
        board[move] = 'X';
        if (checkWinner(board) === 'X') {
            board[move] = '';
            return move;
        }
        board[move] = '';
    }

    // 3. Take center if available
    if (availableMoves.includes(4)) {
        return 4;
    }

    // 4. Take corners if available
    const corners = [0, 2, 6, 8];
    const availableCorners = corners.filter(corner => availableMoves.includes(corner));
    if (availableCorners.length > 0) {
        return availableCorners[Math.floor(Math.random() * availableCorners.length)];
    }

    // 5. Take any available side
    return availableMoves[Math.floor(Math.random() * availableMoves.length)];
}

// Make a move
function makeMove(index) {
    if (gameOver || board[index] !== '' || isComputerTurn) return;

    // Human move
    board[index] = 'X';
    cells[index].textContent = 'X';
    cells[index].classList.add('X');

    const winner = checkWinner(board);
    if (winner) {
        handleGameEnd(winner);
    } else {
        // Computer's turn
        isComputerTurn = true;
        document.querySelector('.board').classList.add('computer-thinking');
        status.textContent = 'Computer thinking...';

        setTimeout(() => {
            const computerIndex = computerMove();
            board[computerIndex] = 'O';
            cells[computerIndex].textContent = 'O';
            cells[computerIndex].classList.add('O');

            const computerWinner = checkWinner(board);
            if (computerWinner) {
                handleGameEnd(computerWinner);
            } else {
                document.querySelector('.board').classList.remove('computer-thinking');
                status.textContent = 'Your turn (X)';
                isComputerTurn = false;
            }
        }, 500);
    }
}

// Handle game end
function handleGameEnd(winner) {
    gameOver = true;
    document.querySelector('.board').classList.add('game-over');

    if (winner !== 'draw') {
        scores[winner]++;
        updateScore(winner);
        triggerConfetti();
        document.querySelectorAll('.cell').forEach(cell => {
            if (cell.textContent === winner) {
                cell.classList.add('winner');
            }
        });
        status.textContent = `Player ${winner} wins!`;
    } else {
        status.textContent = "It's a draw!";
    }

    setTimeout(resetGame, 3000);
}

// Update score
function updateScore(winner) {
    if (winner === 'X') {
        scoreX.textContent = scores.X;
    } else {
        scoreO.textContent = scores.O;
    }
}

// Trigger confetti
function triggerConfetti() {
    confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 }
    });
}

// Reset game
function resetGame() {
    board = ['', '', '', '', '', '', '', '', ''];
    gameOver = false;
    isComputerTurn = false;

    cells.forEach(cell => {
        cell.textContent = '';
        cell.classList.remove('X', 'O', 'winner');
    });

    document.querySelector('.board').classList.remove('game-over', 'computer-thinking');
    status.textContent = 'Your turn (X)';
}

// Initialize the game when the page loads
initGame(); 