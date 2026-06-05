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
    let sqlquery = 'SELECT * FROM characters WHERE c_name=(?)';
    let sqlparams = [c_name];
    let results = await query_promise(sqlquery, params=sqlparams);
    res.render('characters', results[0])
})

async function update(name, key, value) {
    let query = `UPDATE characters SET ${key}=? WHERE c_name=?`;
    await query_promise(query, params = [value, name])
}

app.post('/update', async (req, res) => {
    let {c_name} = req.body
    Object.keys(req.body).forEach(element => {
        if (req.body[element] && element!="c_name")
            update(c_name, element, req.body[element])
    });
    res.redirect('/')
})

app.listen(8080, "0.0.0.0", () => { console.log('server started') });

