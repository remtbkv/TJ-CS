const express = require('express')
const bcrypt = require('bcrypt')
const saltRounds = 10
const auth_router = express.Router()
const query = (require('../index.js'))['query']


async function storeInfo(user, pass) {
    const hashed = await bcrypt.hash(pass, saltRounds)
    await query("INSERT INTO auth (a_user, hashed_pass) VALUES (?, ?)", params = [user, hashed])
    await query("INSERT INTO stats (s_user) VALUES (?)", params = [user])
}

async function authenticate(user, pass) {
    const hashedPass = await query("SELECT hashed_pass FROM auth WHERE a_user=?", params = [user])
    return (hashedPass[0]) ? await bcrypt.compare(pass, hashedPass[0]["hashed_pass"]) : false
}

auth_router.get('/logout', function (req, res) {
    req.session.user = null
    res.redirect('/')
})

async function alreadyLogged(req, res, next) {
    if (req.session.user && (await query("SELECT * FROM auth WHERE a_user=?", params = [req.session.user]))[0])
        res.redirect('/home')
    else
        next()
}

// auth_router.use(alreadyLogged)

auth_router.get("/", alreadyLogged, (req, res) => {
    res.render("authpage")
})

auth_router.get("/login", alreadyLogged, (req, res) => {
    res.render("login")
})

auth_router.post("/loginHandler", alreadyLogged, async (req, res) => {
    let { username, password } = req.body
    try {
        let match = await authenticate(username, password)
        if (match) {
            req.session.user = username
            res.redirect('/home')
        }
        else
            res.redirect('/login')
    }
    catch (error) {
        console.log(error)
        res.redirect('/login')
    }
})

auth_router.get("/signup", alreadyLogged, async (req, res) => {
    res.render('signup')
})

auth_router.post("/signupHandler", alreadyLogged, async (req, res) => {
    let { username, password } = req.body
    const exists = (await query("SELECT * FROM auth WHERE a_user==?", params=[username]))[0]
    if (exists)
        res.redirect('/')
    else {
        await storeInfo(username, password)
        req.session.user = username
        res.redirect('/login')
    }
})

module.exports = auth_router