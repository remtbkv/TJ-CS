const cols = [[0, 130], [130, 250], [250, 370], [370, 490], [490, 610], [610, 730], [730, 860]]
const game_status = document.getElementById("status")
let end, B, user, opponent

class Board {
    constructor(board = {}) {
        this.board = (board.length) ? board : Array.from({ length: 6 }, () => new Array(7).fill('.'))
        this.height = (this.board)[0].map((_, c) => this.board.filter(row => row[c] !== '.').length)
        this.moves = 42 - this.board.flat().join('').split('.').length + 1
        this.player = this.moves % 2 === 0 ? 'x' : 'o'
    }

    gameResult() {
        let board = "?".repeat(9)
        this.board.forEach(row => {board += "?" + row.join('') + "?"})
        board += "?".repeat(9)
        const directions = [1, -1, -8, 8, -9, 9, 10, -10]
        for (const player of ["x", "o"])
            for (let i = 0; i < 72; i++)
                for (const dir of directions) {
                    let cur = i, n = 0
                    while (board[cur] === player && n < 4)
                        cur += dir, n++
                    if (n === 4)
                        return player === "x" ? 1 : 2
                }
        if (!this.board.flat().includes('.'))
            return 0
        return null
    }

    async makeMove(col) {
        if (this.height[col] < 6) {
            this.board[this.getRow(col)][col] = this.player
            this.height[col]++
            this.moves++
            this.nextPlayer()
            await fetch('http://127.0.0.1:8080/api/update', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({"board": JSON.stringify(this.board)})
            })
        }
    }

    nextPlayer() {
        this.player = this.player === "x" ? "o" : "x"
    }

    getRow(col) {
        return 5 - this.height[col]
    }

    possibleMoves() {
        return [0,1,2,3,4,5,6].filter(col => this.height[col] < 6)
    }

    getPlayerColor() {
        return this.player=="x" ? "red" : "yellow"
    }

    getNumMoves() {
        return this.moves
    }
    
}

function player_move(event) {
    if (B.gameResult()===null) {
        let x = event.offsetX, col = cols.findIndex(([start, end]) => x >= start && x < end)
        if (B.possibleMoves().includes(col)) {
            let row = B.getRow(col)
            document.getElementById(`${row},${col}`).setAttribute('fill', B.getPlayerColor())
            B.makeMove(col)
            updateStatus(B.gameResult())
        }
    }
}

async function updateStatus(r) {
    if (r!==null) {
        game_status.innerHTML = ["It's a tie!", "Red wins!", "Yellow wins!"][r]
        // if (r) { // updates stats (games_won)
        //     let winner = [null, user, oppponent][r]
        //     let n_won = JSON.parse(await fetch('http://127.0.0.1:8080/api/specific_user', {
        //         method: 'POST', 
        //         headers: { 'Content-Type': 'application/json' },
        //         body: JSON.stringify({ "user": winner })
        //     }).then(response => response.json()))["games_won"]

        //     await fetch('http://127.0.0.1:8080/api/update', {
        //         method: 'POST',
        //         headers: { 'Content-Type': 'application/json' },
        //         body: JSON.stringify({ "games_won": n_won+1, "user": winner })
        //     })
        // }
        
        let t = document.createElement("h1")
        t.setAttribute("class", "big")
        t.setAttribute("id", "endgame");
        t.appendChild(document.createTextNode("Press enter to restart game."))
        document.body.after(game_status, t)
        end = true
        // do end game win stuff
    }
    else {
        game_status.innerHTML = ["Red's turn", "Yellow's turn"][B.getNumMoves()%2]
    }
}

async function resetGame() {
    B = new Board()
    for (let r = 0; r < 6; r++)
        for (let c = 0; c < 7; c++)
            document.getElementById(`${r},${c}`).setAttribute('fill', 'white')
    updateStatus(B.gameResult())
    document.getElementById("endgame").remove()
    await fetch('http://127.0.0.1:8080/api/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "board": JSON.stringify(B.board) })
    })
    end = false
}
async function startGame() {
    let b = JSON.parse((await fetch("http://127.0.0.1:8080/api/stats").then(response => response.json()))["game"])
    B = new Board(board = b)
    for (let r=0; r<6; r++)
        for (let c=0; c<7; c++) {
            if (b[r][c]==="x")
                document.getElementById(`${r},${c}`).setAttribute('fill', 'red')
            else if (b[r][c]==="o")
                document.getElementById(`${r},${c}`).setAttribute('fill', 'yellow')
        }
    updateStatus(B.gameResult())
}

startGame()

document.getElementById("board").addEventListener("click", player_move)
window.addEventListener("keydown", (k) => { if (k.key==="Enter" && end) resetGame() })