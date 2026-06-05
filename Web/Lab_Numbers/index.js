var express = require('express')
var app = express();

app.set('view engine', 'ejs')
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use(
    express.static('static_files')
)

app.get('/', (req, res) => {
    res.render('nform')
})

app.post('/numberFormHandler', (req, res) => {
    let num = parseInt(req.body.number)
    res.redirect(`/numbers/${num}`)
});

app.get('/numbers/:num', (req, res) => {
    let { num } = req.params;
    n = parseInt(num)
    h = n>37
    let nums = {
        N: n,
        F: 1.8 * n + 32,
        K: n + 273,
        H: h
    }
    let { format } = req.query
    if (format != undefined && format=='json')
        res.json(nums)
    else
        res.render('nshow', nums)
})

var listener = app.listen(process.env.PORT || 8080, process.env.HOST || "0.0.0.0", function () {
    console.log("Express server started");
});