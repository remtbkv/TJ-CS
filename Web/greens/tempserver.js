const express = require('express')
const app = express()
const cookieParser = require('cookie-parser')
const cookieSessionModule = require('cookie-session')

app.set('view engine', 'ejs')
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser())

const cookieInitializationParams = {
    name: 'visits',
    keys: ['password'],
    maxAge: 24 * 60 * 60 * 1000 // 24 hours
}

const cookieSessionMiddleware = cookieSessionModule(cookieInitializationParams)
app.use(cookieSessionMiddleware)

app.get('/login', (req, res) => {
    let {logged_in} = req.session
    logged_in ||= true
    req.session.logged_in = logged_in
    res.render('logged_in')
})

app.get('/logout', (req, res) => {
    req.session.logged_in = false
    res.render('logged_out')
})

app.use((req, res, next) => {
    let { visits, logged_in } = req.session;
    logged_in ||= false
    visits ||= 0;
    visits += 1
    req.session.visits = visits;
    next();
})


app.get('/premium', (req, res)=> {
    let { visits, logged_in } = req.session
    res.render('premium', dct = { "visits": visits, "logged_in": logged_in })
    // res.render('page', dct = { "number": visits })
}) 

app.get('/cookiepage', (req, res) => {
    var {number} = req.cookies
    if (isNaN(number)) {
        number = 0
    }
    else {
        number = Number(number);
        number += 1;
    }
    const expirationDate = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000);
    res.cookie("number", number, {
        expires: expirationDate,
    });
    res.render('page', dct={"number": number})
})

var listener = app.listen(process.env.PORT || 8080, process.env.HOST || "0.0.0.0", function () {
    console.log("Express server started");
});