const express = require("express");
const app = express();

const fs = require('fs');
const path = require('path');

const wordsFilePath = path.join(__dirname, 'enable1.txt')

app.set('view engine', 'ejs')
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static('static'))

const words = fs.readFileSync(wordsFilePath).toString().split('\n')

app.get('/', (req, res) => {
    res.render('home')
})

function count(misplaced, val) {
    let count = 0
    misplaced.forEach(el => {
        if (el===val) count++
    });
    return count
}

app.post('/wordfinder', (req, res) => {
    let {correct, misplaced, excluded} = req.body
    
    res.json(words.filter((word) => {
        let isLength = word.length == 5
        let isCount = word.split("").every((val) => count(word.split(""), val)>=count(misplaced, val))
        let isCorrect = correct.every((val, ind) => (val !== '' ? word[ind] === val : true));
        let isMisplaced = misplaced.every((val, ind) => (val !== '' ? word[ind] !== val : true));
        let isExcluded = excluded.split('').every((letter) => (letter !== '' ? word.indexOf(letter) === -1 : true));
        return isLength && isCount && isCorrect && isMisplaced && isExcluded;
    }))
})

const listener = app.listen(
    process.env.PORT || 8080,
    process.env.HOST || "0.0.0.0",
    function () {
        console.log("Express server started");
    }
);