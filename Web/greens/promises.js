const fs = require('fs')
let https = require('https')
let http = require('http')
const express = require('express')
const app = express()


function download(url) {
    return new Promise((resolve, reject) => {
        http.get(url, (response) => {
            let data = ""
            response.on('data', (chunk)=> {data+=chunk})
            response.on('end', () => {resolve(data)})
        }).on('error', (err) => {
            reject(err)
        })
    })
}


async function write(fn, data) {
    return new Promise((resolve) => {
        fs.writeFile(fn, data, (err) => {
            if (err) throw err;
            resolve(data)
        })
    })
}

async function main() {
    let url = 'http://127.0.0.1:8080/'
    let output = await download(url)
    await write('bob.txt', output)
    console.log('done')
}

main()