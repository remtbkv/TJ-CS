const express = require('express')
const app = express()

const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('database.db');

app.set('view engine', 'ejs')

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

function query_promise(query, params = []) {
    return new Promise((resolve, reject) => {
        const fn = (query.split(" ")[0].toUpperCase() === "SELECT") ? 'all' : 'run'
        if (params.length === 0) {
            db[fn](query, (err, rows) => {
                if (err) reject(err);
                resolve(rows);
            })
        } else {
            db[fn](query, params, (err, rows) => {
                if (err) reject(err);
                resolve(rows);
            })
        }
    })
}

app.get('/', async (req, res) => {
    let sqlquery = 'SELECT * FROM characters';
    let results = await query_promise(sqlquery);

    let dictionary_out = {
        'results': results
    }
    res.render('results', dictionary_out)
})

app.get('/profile/:c_name', async (req, res) => {
    const { c_name } = req.params;
    cq = 'SELECT * FROM characters WHERE c_name=(?)';
    results = await query_promise(cq, params = [c_name]);
    cid = results[0]['c_id']
    eq = 'SELECT e_name from equipment INNER JOIN assigned_e WHERE c_id=? AND equipment.e_id=assigned_e.e_id'
    equips = await query_promise(eq, params = [cid])
    qu = 'SELECT q_desc from quests INNER JOIN assigned_q WHERE c_id=? AND quests.q_id=assigned_q.q_id'
    quests = await query_promise(qu, params = [cid])

    let obj = { 'cinfo': results[0], equips, quests }
    res.render('characters', obj)
})

async function update(name, key, value) {
    let query = `UPDATE characters SET ${key}=? WHERE c_name=?`;
    await query_promise(query, params = [value, name])
}

async function insert(table, value1, value2) {
    let query = `INSERT INTO ${table} VALUES (?, ?)`
    await query_promise(query, params = [value1, value2])
}

app.post('/update', async (req, res) => {
    let { c_name } = req.body
    Object.keys(req.body).forEach(element => {
        if (req.body[element] && element != "c_name")
            update(c_name, element, req.body[element])
    });
    res.redirect('/')
})

app.get('/equip', async (req, res) => {
    let c = await query_promise('SELECT * FROM characters');
    let e = await query_promise('SELECT * FROM equipment');
    res.render('ae_form', { c, e })
})

app.get('/quest', async (req, res) => {
    let c = await query_promise('SELECT * FROM characters');
    let q = await query_promise('SELECT * FROM quests');
    res.render('qe_form', { c, q })
})

app.post('/assign', async (req, res) => {
    Object.keys(req.body).forEach(el => {
        if (el != "character" && el != "table")
            insert(req.body['table'], req.body['character'], el)
    });
    res.redirect('/')
})

app.listen(8080, "0.0.0.0", () => { console.log('server started') });
