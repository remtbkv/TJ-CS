var express = require('express')
var app = express();

app.set('view engine', 'ejs')
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

let https = require('https')


app.use(
    express.static('static_files')
)

app.get('/forecast/', (req, res) => {
    let resp = '';
    let url = 'https://api.weather.gov/points/38.8186,-77.1689'
    https.get(url, (response) => {
        response.on('data', (chunk) => {
            console.log('new chunk')
            resp += chunk;
        });

        response.on('end', () => {
            console.log('donwload complete')
            console.log(resp)
            res.render('show', resp)
        });
    })
})

var listener = app.listen(process.env.PORT || 8080, process.env.HOST || "0.0.0.0", function () {
    console.log("Express server started");
});
