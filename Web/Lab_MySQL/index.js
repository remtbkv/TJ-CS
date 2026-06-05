var express = require('express')
var app = express();

var mysql = require('mysql');

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.set('view engine','ejs')

var sql_params = {
  connectionLimit : 10,
  user            : process.env.DIRECTOR_DATABASE_USERNAME,
  password        : process.env.DIRECTOR_DATABASE_PASSWORD,
  host            : process.env.DIRECTOR_DATABASE_HOST,
  port            : process.env.DIRECTOR_DATABASE_PORT,
  database        : process.env.DIRECTOR_DATABASE_NAME
}

app.locals.pool  = mysql.createPool(sql_params);

function new_promise(res, query, params=[]) {
    return new Promise((resolve, reject) => {
        res.app.locals.pool.query(query, params, function (error, results) {
            if (error) reject(error)
            resolve(results)
        })
    })
}

app.get("/", async (req, res) => {
    var sqlquery = 'SELECT * FROM characters';
    let results = await new_promise(res, sqlquery);
    let dictionary_out = {
        'results': results
    }
    res.render('results', dictionary_out)
})

app.get('/profile/:c_name', async (req, res) => {
    const { c_name } = req.params;
    cq = 'SELECT * FROM characters WHERE c_name=(?)';
    results = await new_promise(res, cq, params = [c_name]);
    cid = results[0]['c_id']
    eq = 'SELECT e_name from equipment INNER JOIN assigned_e WHERE c_id=? AND equipment.e_id=assigned_e.e_id'
    equips = await new_promise(res, eq, params=[cid])
    qu = 'SELECT q_desc from quests INNER JOIN assigned_q WHERE c_id=? AND quests.q_id=assigned_q.q_id'
    quests = await new_promise(res, qu, params=[cid])

    let obj = { 'cinfo': results[0], equips, quests}
    res.render('characters', obj)
})

async function update(res, name, key, value) {
    let query = `UPDATE characters SET ${key}=? WHERE c_name=?`;
    await new_promise(res, query, params = [value, name])
}

async function insert(res, table, value1, value2) {
    let query = `INSERT INTO ${table} VALUES (?, ?)`
    await new_promise(res, query, params = [value1, value2])
}

app.post('/update', async (req, res) => {
    let { c_name } = req.body
    for (const el of Object.keys(req.body))
        if (req.body[el] && el != "c_name")
            await update(res, c_name, el, req.body[el])
    res.redirect('/2025rturatbe')
})

app.get('/equip', async (req, res) => {
    let c = await new_promise(res, 'SELECT * FROM characters');
    let e = await new_promise(res, 'SELECT * FROM equipment');
    res.render('ae_form', {c, e})
})

app.get('/quest', async (req, res) => {
    let c = await new_promise(res, 'SELECT * FROM characters');
    let q = await new_promise(res, 'SELECT * FROM quests');
    res.render('qe_form', {c, q})
})

app.post('/assign', async (req, res) => {
    for (const el of Object.keys(req.body))
        if (el != "character" && el != "table")
            await insert(res, req.body['table'], req.body['character'], el);
    res.redirect('/2025rturatbe');
});

var listener = app.listen(
  process.env.PORT || 8080,
  process.env.HOST || "0.0.0.0",
  function() {
    console.log("Express server started");
  }
);