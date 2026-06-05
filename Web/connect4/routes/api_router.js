const express = require('express')
const api_router = express.Router()
api_router.use(express.json());
api_router.use(express.urlencoded({ extended: true }));
const query = (require('../index.js'))['query']


api_router.get('/', (req, res) => {
    res.render("api")
})

api_router.get("/all_users", async (req, res) => {
    res.json((await query("SELECT a_user FROM auth")).map(e => e["a_user"]))
})

api_router.post("/specific_user", async (req, res) => {
    res.json((await query("SELECT * FROM stats WHERE s_user=?", params = [req.body.user]))[0])
})

api_router.post('/update', async (req, res) => {
    let {board, games_won, user} = req.body
    user ||= req.session.user
    if (board)
        await query("UPDATE stats SET game=? WHERE s_user=?", params = [board, user])
    if (games_won)
        await query("UPDATE stats SET games_won=? WHERE s_user=?", params = [games_won, user])
})

api_router.post('/updateGame', async (req, res) => {
    await query("UPDATE stats SET game=? WHERE s_user=?", params = [req.body.board, req.session.user])
})

async function restrict(req, res, next) {
    if (req.session.user && (await query("SELECT * FROM auth WHERE a_user=?", params = [req.session.user]))[0])
        next()
    else
        res.redirect('/api')
}

api_router.use(restrict)

api_router.get('/stats', async (req, res) => {
    res.json((await query("SELECT * FROM stats WHERE s_user=?", params = [req.session.user]))[0])
})

api_router.get('/requests', async (req, res) => {
    res.send(await query("SELECT challenger FROM requests WHERE challenged=?", params = [req.session.user]))
})

module.exports = api_router