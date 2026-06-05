var squareSize = 80;
var gameInProgress = true;
var rows = 6;
var columns = 7;
var board = new Array();
var RED = 1;
var BLACK = 2;
var BLANK = 0;
var turn = RED;
var piece = null;
var player1 = "Human";
var player2 = "Computer";
var player = Math.floor(Math.random() * 2) + 1;
var holder = null;
var TIME = 20;
var moves = 0;
var redMarker = new Object();
redMarker.color = RED;
var blackMarker = new Object();
blackMarker.color = BLACK;
var blankMarker = new Object();
blankMarker.color = BLANK;
var connections = [0, 0, 0, 0, 0];

function addEvent(element, event, fn) 
{
    if (element.addEventListener)
        element.addEventListener(event, fn, false);
    else if (element.attachEvent)
        element.attachEvent('on' + event, fn);
}

function startGame()
{
	//preload images
	if( document.images )
	{
		var img1 = new Image();
		var img2 = new Image();
		var img3 = new Image();
		var img4 = new Image();
		var img5 = new Image();
		var img6 = new Image();
		var img7 = new Image();
		var img8 = new Image();		

		img1.src = 'images/red1.png';
		img2.src = 'images/red2.png';
		img3.src = 'images/red1-high.png';
		img4.src = 'images/red2-high.png';
		
		img5.src = 'images/black1.png';
		img6.src = 'images/black2.png';
		img7.src = 'images/black1-high.png';
		img8.src = 'images/black2-high.png';		
	}

	if( document.getElementById('human').checked )	
		player2 = "Human";	
	else
		player2 = "Computer";	

	piece = createPiece();
	document.getElementById('message').innerHTML = "Player " + player + " Goes First";	
	document.getElementById('player1').innerHTML = "Player 1 (" + player1 + '): ';
	document.getElementById('player2').innerHTML = "Player 2 (" + player2 + '): ';	
	
	var color1 = document.getElementById('color1');
	var color2 = document.getElementById('color2');
	
	if( player == 1 )
	{	
		color1.innerHTML = 'Red';
		color1.style.color = 'Red';			
		color2.innerHTML = 'Black';
	}
	else
	{
		color1.innerHTML = 'Black';
		color2.innerHTML = 'Red';
		color2.style.color = 'Red';
	}	
	
	if( player == 2 && player2 == "Computer" )
	{
		var column = Math.floor( columns / 2 );
		piece.style.left =  (squareSize * column) + "px";
		dropPiece(column);
	}	
	
	document.getElementById('board').onmousemove = hoverPiece;
	document.getElementById('board').onclick = selectSlot;
}

addEvent(window, 'load', startGame );

for( var i = 0; i < rows; i++ )
{
	board[i] = new Array();
	for( var j = 0; j < columns; j++ )
		board[i][j] = blankMarker;
}

function createPiece()
{
	var image = document.createElement('img');
	var number = Math.floor(Math.random()*2+1); //1 or 2
	
	if( turn == RED )
		image.src = 'images/red' + number + '.png';
	else
		image.src = 'images/black' + number + '.png';
	
	image.color = turn;
		
	var parent = document.getElementById('board');
	parent.appendChild(image);		
	image.style.position = 'absolute';
	image.style.left = '0px';
	image.style.top = '0px';
	image.style.zIndex = -1;
	return image;
}


function selectSlot(e)
{		
	if( gameInProgress && piece != null )	
	{
		var position = getPosition(e);
		var slot = Math.round(position / squareSize);
		if( board[0][slot] == blankMarker )		
			dropPiece(slot);		
	}
}

function dropPiece(slot)
{	
	holder = piece;
	piece = null;
	var row = findRow(slot);
		
	holder.style.left = (slot * squareSize) + "px";
	holder.destination = ((row + 1) * squareSize);
	holder.location = 0.0;
	holder.velocity = 0;
	holder.bounces = 0;
	holder.row = row;
	holder.column = slot;
	board[row][slot] = holder;
	
	moves++;
	
	setTimeout( animateDrop, TIME );
}

function animateDrop() {
	holder.velocity += 9.8 * TIME / 1000; //acceleration
	holder.location += holder.velocity * TIME;
	holder.style.top = Math.round(holder.location) + "px";
	if (holder.location >= holder.destination) {
		holder.bounces++;
		holder.location = holder.destination;
		holder.style.top = Math.round(holder.location) + "px";
		if (holder.bounces < 5) {
			holder.velocity = -holder.velocity * .25;
			setTimeout(animateDrop, TIME);
		}
		else
			checkGameState(holder.row, holder.column);
	}
	else
		setTimeout(animateDrop, TIME);
}


function drawBoard() {
	document.write('<div id="board" style="float: left; display: inline-block; padding: 0; width:' + (columns * squareSize) + 'px; height:' + ((rows + 1) * squareSize) + 'px; position: relative;">');

	for (var i = 0; i < rows; i++)
		for (var j = 0; j < columns; j++)
			document.write('<img style="left: ' + (j * squareSize) + 'px; top: ' + ((i + 1) * squareSize) + 'px; position:absolute;" src="images/slot.png"/>');

	document.write('</div>');
}

function hoverPiece(e) {
	if (gameInProgress && piece != null)
		piece.style.left = getPosition(e) + "px";
}


function getPosition(e) {
	e = e || window.event;
	var bound = document.getElementById('board').getBoundingClientRect();
	var position = e.clientX - bound.left - squareSize / 2;
	if (position < 0)
		position = 0;
	if (position > (columns - 1) * squareSize)
		position = (columns - 1) * squareSize;
	return position;
}

function findRow(slot) {
	var i = 0;
	while (i + 1 < rows && board[i + 1][slot] == blankMarker)
		i++;

	return i;
}

function invert(color)
{
	if( color == RED )
		return BLACK;
	else
		return RED;
}

function highlight(row, column)
{
	var checker = board[row][column];
	checker.src = checker.src.slice(0, -4) + "-high.png";	
}

function lightRecursively( row, column, changeRow, changeColumn, color )
{
	if( row >= 0 && row < rows && column >= 0 && column < columns && board[row][column].color == color )
	{
		highlight(row, column);
		lightRecursively( row + changeRow, column + changeColumn, changeRow, changeColumn, color );	
	}
}

function lightUpBoard(row, column)
{
	var color = board[row][column].color;
	highlight( row, column );

	//horizontal
	if( connections[0] >= 4 )
	{
		lightRecursively( row, column - 1, 0, -1, color );
		lightRecursively( row, column + 1, 0, 1, color );
	}
	
	//vertical
	if( connections[1] >= 4 )
	{
		lightRecursively( row - 1, column, -1, 0, color );
		lightRecursively( row + 1, column, 1, 0, color );
	}
	
	// \ diagonal
	if( connections[2] >= 4 )
	{
		lightRecursively( row - 1, column - 1, -1, -1, color );
		lightRecursively( row + 1, column + 1, 1, 1, color );
		
	}
	

	// / diagonal
	if( connections[3] >= 4 )
	{
		lightRecursively( row - 1, column + 1, -1, 1, color );
		lightRecursively( row + 1, column - 1, 1, -1, color );
	}
}

function checkGameState(row, column)
{
	//check game is over
	mostConnected(row, column);
	if( connections[4] >= 4 )
	{
		document.getElementById('message').innerHTML = "Player " + player + " Wins!";
		gameInProgress = false;
		
		lightUpBoard( row, column );		
	}
	else if( moves == rows * columns )
	{
		document.getElementById('message').innerHTML = "Game is a Tie!";
		gameInProgress = false;	
	}
	else
	{		
		turn = invert(turn);
		
		if( player == 1 )			
			player = 2;			
		else
			player = 1;
			
		document.getElementById('message').innerHTML = "Player " + player + "'s Turn";				
				
		if( player == 2 && player2 == "Computer" )
		{
			var boardDiv = document.getElementById('board');
			boardDiv.onmousemove = null;
			boardDiv.onclick = null;
			document.getElementById('status').style.visibility = "visible";	
			//timeout used so that status has time to update
			setTimeout( computerMove, 100 );			
		}
		else
			piece = createPiece();
	}
}

function computerMove()
{
	var column = makeChoice(turn);			
	piece = createPiece();
	piece.style.left = (squareSize * column) + "px";
	dropPiece(column);
	var boardDiv = document.getElementById('board');
	boardDiv.onmousemove = hoverPiece;
	boardDiv.onclick = selectSlot;
	document.getElementById('status').style.visibility = "hidden";		
}

function mostConnected(row, column)
{	
	var color = board[row][column].color;
	
	//reuses global connections array to avoid garbage collection
	for( var i = 0; i < 5; i++ )
		connections[i] = 0;	
	
	//check horizontal
	var spots = 1;
	for( var i = column + 1; i < columns && board[row][i].color == color; i++ )
		spots++;
	for( var i = column - 1; i >= 0 && board[row][i].color == color; i-- )
		spots++;	
	connections[0] = spots;
	connections[4] = spots;
	
	//check vertical
	spots = 1;
	for( var i = row + 1; i < rows && board[i][column].color == color; i++ )
		spots++;
	for( var i = row - 1; i >= 0 && board[i][column].color == color; i-- )
		spots++;	
	connections[1] = spots;
	connections[4] = Math.max( connections[4], spots );
	
	//check \ diagonal		
	
	spots = 1;
	for( var i = 1; row + i < rows && column + i  < columns && board[row + i][column + i].color == color; i++ )
		spots++;
	for( var i = -1; row + i >= 0 && column + i >= 0 && board[row + i][column + i].color == color; i-- )
		spots++;	
	connections[2] = spots;
	connections[4] = Math.max( connections[4], spots );
	

	//check / diagonal
	spots = 1;
	for( var i = 1; row + i < rows && column - i >= 0 && board[row + i][column - i].color == color; i++ )
		spots++;
	for( var i = -1; row + i >= 0 && column - i < columns && board[row + i][column - i].color == color; i-- )
		spots++;	
	connections[3] = spots;
	connections[4] = Math.max( connections[4], spots );
}

function negamax( row, column, color, depth, alpha, beta ) // uses depth to make skill leveled ai
{
	mostConnected( row, column ); //updates connections array
	
	//0 for no connections
	//1 for each 2-connnect
	//5 for each 3-connect
	//25 for a win
	
	if( connections[4] >= 4 )
		return -25;
	
	if( depth == 0 )
	{	
		var sum = 0;
		for( var i = 0; i < 4; i++ )
		{
			if( connections[i] == 2 )
				sum -= 1;
			else if( connections[i] == 3 )
				sum -= 5;
		}
		
		return sum;	
	}
	
	var best = -100;
	color = invert(color);
	var piece;
	
	if( color == RED )
		piece = redMarker;
	else
		piece = blackMarker;
		
	for( var i = 0; i < columns; i++ )
	{
		if( board[0][i] == blankMarker )
		{
			var j = findRow(i);
			board[j][i] = piece;
			best = Math.max( best, -negamax( j, i, color, depth - 1, -beta, -alpha ));
			board[j][i] = blankMarker;
			if( best >= beta )
				break;
			if( best > alpha )
				alpha = best;
		}
	}
	
	if( best == -100 )
		return 0; //no moves (tie)
	else
		return best;		
}

function makeChoice(color)
{
	var choices = new Array();
	for( var i = 0; i < columns; i++ )
		choices[i] = -100;
	
	var dropdown = document.getElementById("difficulty");
	var depth = parseInt(dropdown.options[dropdown.selectedIndex].value);	
	var piece;
	
	if( color == RED )
		piece = redMarker;
	else
		piece = blackMarker;
	
	//try options
	var best = -100;
	for( var i = 0; i < columns; i++ )
	{
		if( board[0][i] == blankMarker )
		{
			var j = findRow(i);
			board[j][i] = piece;
			choices[i] = -negamax(j, i, color, depth - 1, -100, 100);
			best = Math.max( best, choices[i] );
			board[j][i] = blankMarker;
		}
	}
	
	var counter = 0;
	var locations = new Array();
	for( var i = 0; i < columns; i++ )
	{
		//could be many bests, pick randomly!
		if( choices[i] == best )
		{
			locations[counter] = i;
			counter++;		
		}
	}	
	
	return locations[Math.floor(Math.random() * locations.length)];
}
