let gameState = {
    board : [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]],
    player_turn : 0,
    end : false,
    players : "XO"
}

arrEqual = (a, b) => {
    return JSON.stringify(a) === JSON.stringify(b)
}

showInfo = (str, temp=false) => {
    m = document.querySelector("#message")
    if (temp) {
        tmpStr = m.innerHTML
        m.innerHTML = str
        setTimeout(() => {
            m.innerHTML = tmpStr
        }, 1000);
    }
    else {
        m.innerHTML = str
    }
}

drawShape = (x, y, s) => {
    b = document.getElementById("board")
    if (s=="O") {
        let circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        circle.setAttribute("cx", x*200 + 95);
        circle.setAttribute("cy", y*200 + 95);
        circle.setAttribute("r", "90");
        circle.setAttribute("fill", "none");
        circle.setAttribute("stroke", "black");
        circle.setAttribute("stroke-width", "5");
        b.append(circle)
    }
    else {
        let x1 = document.createElementNS("http://www.w3.org/2000/svg", "line");
        let x2 = document.createElementNS("http://www.w3.org/2000/svg", "line");
        x1.setAttribute("x1", x * 200 + 10);
        x1.setAttribute("y1", y * 200 + 190);
        x1.setAttribute("x2", x * 200 + 190);
        x1.setAttribute("y2", y * 200 + 10);
        x1.setAttribute("stroke", "black")
        x1.setAttribute("stroke-width", "5")
        b.append(x1)
        x2.setAttribute("x1", x * 200 + 10);
        x2.setAttribute("y1", y * 200 + 10);
        x2.setAttribute("x2", x * 200 + 190);
        x2.setAttribute("y2", y * 200 + 190);
        x2.setAttribute("stroke", "black")
        x2.setAttribute("stroke-width", "5")
        b.append(x2)
    }
}

player_move = (event) => {
    if (gameState.end) return
    let col = Math.floor(event.offsetX / 200), row = Math.floor(event.offsetY / 200)

    let p = gameState.player_turn % 2, s = gameState.players[p]
    if (gameState.board[row][col] != "-")
        showInfo("Cant move there!", temp = true)
    else {
        drawShape(col, row, s)
        gameState.board[row][col] = s
        gameState.player_turn++
        showInfo(gameState.players[gameState.player_turn%2]+"'s turn")
    }
    w = check_game()
    if (w==-1) {
        showInfo("It's a tie!")
        showInfo("Game over! Press r to restart", temp = true)
        gameState.end = true
    }
    if (w>0) {
        showInfo(s+" won!")
        showInfo("Game over! Press r to restart", temp=true)
        gameState.end = true
    }

}

check_game = () => {
    
    let d1row = [], d2row = [], xrow = ["X", "X", "X"], orow = ["O", "O", "O"]
    for (let i=0; i<3; i++) {
        d1row.push(gameState.board[i][i])
        d2row.push(gameState.board[2-i][i])
    }
    if (arrEqual(d1row, xrow) || arrEqual(d2row, xrow))
        return 1 // "X wins!"
    else if (arrEqual(d1row, orow) || arrEqual(d2row, orow))
        return 2// "Y wins!"

    for (let c=0; c<3; c++) {
        let crow = []
        for (let r = 0; r < 3; r++)
            crow.push(gameState.board[r][c])
        if (arrEqual(gameState.board[c], xrow) || arrEqual(crow, xrow))
            return 1 // "X wins!"
        else if (arrEqual(gameState.board[c], orow) || arrEqual(crow, orow))
            return 2 // "O wins!"
    }
    if (gameState.player_turn == 9)
        return -1
    return 0 // "Nobody won"
}

reset = () => {
    gameState.board = [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]
    gameState.end = false
    gameState.player_turn = 0
    document.querySelectorAll("#board>:not(rect)").forEach((el)=>el.remove())
    document.querySelector("#message").innerHTML = "X's turn"
}


document.querySelectorAll("#board>rect").forEach((v) => v.onclick = player_move)
window.addEventListener("keydown", (k) => { if (k.key=="r") reset() })