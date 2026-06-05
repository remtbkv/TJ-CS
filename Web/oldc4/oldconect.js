
gameboard = "?".repeat(9)
for (let i = 0; i < 6; i++)
    gameboard += "?" + ".".repeat(7) + "?"
gameboard += "?".repeat(9)
turn = 0

printBoard = () => {
    var out = ""
    for (let i = 0; i < 72; i += 9)
        out += gameboard.substring(i, i + 9) + "\n"
    console.log(out)
}

printBoard1 = () => {
    var out = " 1234567"
    for (let i = 0; i < 72; i += 9)
        out += i / 9 + " " + gameboard.substring(i, i + 9) + "\n"
    console.log(out)
}

let gameState = {
    board: gameboard,
    player_turn: 0,
    end: false,
    players: "XO"
}

arrEqual = (a, b) => {
    return JSON.stringify(a) === JSON.stringify(b)
}

possible_moves = (gameboard) => {
    moves = []
    for (let i = 55; i < 62; i++) {
        cur = i
        while (cur >= 0 && (gameboard[cur] == "x" || gameboard[cur] == "o"))
            cur -= 9
        if (cur >= 0)
            moves.push(cur)
    }
    return moves
}

game_over = () => {
    directions = [1, -1, 8, -9, 9, -9, 10, -10]
    for (player of "xo")
        for (let i = 0; i < 72; i++)
            for (dir of directions) {
                let cur = i, n = 0
                if (gameboard[cur] == player) {
                    while (gameboard[cur] == player && n < 4)
                        cur += dir, n++
                    if (n == 4)
                        return player == "x" ? 1 : -1
                }
            }
    return gameboard.indexOf(".") < 0 ? 0 : null
}

make_move = (player, ind) => {
    board = Array.from(gameboard)
    board[ind] = player
    return board.join("")
}

negamax = (board, player) => {
    if (game_over(board))
        return 100
    opp = player == "x" ? "o" : "x"
    val = -100
    for (ind of possible_moves(board)) {
        val = max(val, -negamax(make_move(board, player), opp))
        if (val == 100)
            break
    }
    return val
}


go = (index) => {
    make_move("x", index)
    turn++
    player_move()
}

aigo = () => {
    moves = dict()
    for (ind of possible_moves()) {
        moves[ind] = negamax(make_move("o", ind), "x")
    }
}


// showInfo = (str, temp = false) => {
//     m = document.querySelector("#message")
//     if (temp) {
//         tmpStr = m.innerHTML
//         m.innerHTML = str
//         setTimeout(() => {
//             m.innerHTML = tmpStr
//         }, 1000);
//     }
//     else {
//         m.innerHTML = str
//     }
// }

// drawShape = (x, y, s) => {
//     b = document.getElementById("board")
//     if (s == "O") {
//         let circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
//         circle.setAttribute("cx", x * 200 + 95);
//         circle.setAttribute("cy", y * 200 + 95);
//         circle.setAttribute("r", "90");
//         circle.setAttribute("fill", "none");
//         circle.setAttribute("stroke", "black");
//         circle.setAttribute("stroke-width", "5");
//         b.append(circle)
//     }
//     else {
//         let x1 = document.createElementNS("http://www.w3.org/2000/svg", "line");
//         let x2 = document.createElementNS("http://www.w3.org/2000/svg", "line");
//         x1.setAttribute("x1", x * 200 + 10);
//         x1.setAttribute("y1", y * 200 + 190);
//         x1.setAttribute("x2", x * 200 + 190);
//         x1.setAttribute("y2", y * 200 + 10);
//         x1.setAttribute("stroke", "black")
//         x1.setAttribute("stroke-width", "5")
//         b.append(x1)
//         x2.setAttribute("x1", x * 200 + 10);
//         x2.setAttribute("y1", y * 200 + 10);
//         x2.setAttribute("x2", x * 200 + 190);
//         x2.setAttribute("y2", y * 200 + 190);
//         x2.setAttribute("stroke", "black")
//         x2.setAttribute("stroke-width", "5")
//         b.append(x2)
//     }
// }