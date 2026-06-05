var express = require('express')
var https = require('https');
var app = express();
var options = {
    headers: {
        'User-Agent': 'request'
    }
}

app.set('view engine', 'ejs')
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use(express.static('static_files'))

app.get('/getweather/', (req, res) => {
    res.render('wform')
})

function ok(status) {
    return status >= 200 && status < 300
}

function getStation(req, res, next) {
    let { latitude, longitude } = req.body;
    let url = `https://api.weather.gov/points/${latitude},${longitude}`

    https.get(url, options, (resp) => {
        var data = '';
        resp.on('data', (chunk) => {
            data += chunk;
        });
        resp.on('end', () => {
            let out = JSON.parse(data)
            if (!('status' in out) || ('status' in out && ok(out['status']))) {
                let station = out["properties"]["forecast"]
                if (station) {
                    res.locals.stationURL = station 
                    res.locals.location = out["properties"]["relativeLocation"]["properties"]
                    next()
                }
                else
                    res.redirect('/getweather')
            }
            else  {
                res.redirect('/getweather')
            }
        })
    })
}

function getForecast(req, res) {
    https.get(res.locals.stationURL, options, (resp) => {
        data = '';
        resp.on('data', (chunk) => {
            data += chunk;
        });
        resp.on('end', () => {
            out = JSON.parse(data)
            if (!('status' in out) || ('status' in out && ok(out['status']))) {
                forecast = out["properties"]["periods"]
                res.render("wshow", {forecast, location: res.locals.location}) 
            }
            else
                res.redirect('/getweather')
        });
    });
}

app.post('/getweather/results', getStation, getForecast);


var listener = app.listen(process.env.PORT || 8080, process.env.HOST || "0.0.0.0", function () {
    console.log("Express server started");
});
