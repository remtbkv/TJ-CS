const express = require('express')
const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('static/sql/database.db');
const app = express()
app.use(express.static('static'))
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.set('view engine', 'ejs')

const cookieParser = require('cookie-parser')
const cookieSessionModule = require('cookie-session')
const cookieInitializationParams = {
    name: 'auth',
    keys: ['password'],
    maxAge: 24 * 60 * 60 * 1000 // 24 hours
}
const cookieSessionMiddleware = cookieSessionModule(cookieInitializationParams)
app.use(cookieSessionMiddleware)
app.use(cookieParser())

function query(query, params = []) {
    return new Promise((resolve, reject) => {
        const fn = (query.split(" ")[0].toUpperCase() === "SELECT") ? 'all' : 'run'
        if (params.length === 0)
            db[fn](query, (err, rows) => {
                if (err) reject(err)
                resolve(rows)
            })
        else
            db[fn](query, params, (err, rows) => {
                if (err) reject(err)
                resolve(rows)
            })
    })
}
module.exports = {query}

const api_router = require("./routes/api_router.js")
const auth_router = require("./routes/auth_router.js")
app.use('/api', api_router)
app.use(auth_router)

async function restrict(req, res, next) {
    if (req.session.user && (await query("SELECT * FROM auth WHERE a_user=?", params = [req.session.user]))[0])
        next()
    else
        res.redirect('/')
}

app.get('/home', restrict, (req, res) => {
    res.render('home', { "user": req.session.user });
});

app.get('/game', restrict, (req, res) => {
    res.render('connect')
})

app.get('/play', restrict, (req, res) => {
    res.render('play')
})

app.get('/request', restrict, (req, res) => {
    res.render('request')
})

app.post("/requestHandler", restrict, async (req, res) => {
    let {username} = req.body
    await query("INSERT INTO requests VALUES (?, ?)", params = [username, req.session.user])
    res.redirect('/home')
})


app.listen(8080, "0.0.0.0", () => { console.log('server started') });
