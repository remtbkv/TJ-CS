const fs = require('fs')
let http = require('http')

const express = require('express')
const app = express()

// test urls
// http://127.0.0.1:8080/heros_json
// http://127.0.0.1:8080/update_attack?id=0&attack=1000

let heros = {
    heros: [
        {
            id: 0,
            name: "Archibald",
            wit: 0,
            strength: 7,
            attack: 5,
            defense: 1,
            magic: 0
        }, {
            id: 1,
            name: "Henrik",
            wit: 4,
            strength: 3,
            attack: 3,
            defense: 1,
            magic: 2
        }, {
            id: 2,
            name: "Isadore",
            wit: 2,
            strength: 6,
            attack: 4,
            defense: 0,
            magic: 4
        }, {
            id: 3,
            name: "Lucinda",
            wit: 4,
            strength: 3,
            attack: 1,
            defense: 8,
            magic: 1
        }, {
            id: 4,
            name: "Harold",
            wit: 5,
            strength: 2,
            attack: 3,
            defense: 3,
            magic: 2
        }
    ]
}

async function writeData(fn, data) {
    return new Promise((resolve) => {
        fs.writeFile(fn, data, (err) => {
            if (err) throw err;
            resolve(data)
        })
    })
}

app.get('/update_attack', (req, res) => {
    const { id, attack } = req.query
    try {
        heros.heros[id].attack = Number(attack)
        writeData('herosData.txt', JSON.stringify(heros))
        res.json({ 'ok': true })
    } catch {
        res.json({ 'ok': false })
    }

})

function get_file_content(fn) {
    return new Promise((resolve, reject) => {
        fs.readFile(fn, (err, data) => {
            if (err) throw err;
            resolve(data)
        })
    })
}

async function read_file(res, fn) {
    let data = await get_file_content(fn)
    res.json(JSON.parse(data.toString()))
}

app.get('/heros_json', (req, res) => {
    read_file(res, 'herosData.txt')
})

const listener = app.listen(
    process.env.PORT || 8080,
    process.env.HOST || "0.0.0.0",
    function () {
        console.log("Express server started")
    })