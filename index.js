// Index JS
// Author: SSL - IoT 1
// University of the Philippines - Diliman Electrical and Electronics Engineering Institute



// ------- START NodeJS/Express Setup ------ //
// Require Node.js File System
const fs = require("fs/promises");
// Require Express connection
const express = require("express");
// Require CORS communication *NOT USED, BUT FOR FRONT-END*
const cors = require("cors");
// Require lodash for randomization *NOT USED YET -- ID'S, TOKENS*
const _ = require("lodash");
// Require uuid to Generate Unique IDs *NOT USED YET*
const { v4: uuidv4, parse} = require("uuid");

const corsOptions ={
    origin:'http://localhost:80',
    credentials:true,            //access-control-allow-credentials:true
    optionSuccessStatus:200
}
// Server Start-up
const app = express();
app.use(cors(corsOptions));

// Add middleware to support JSON
app.use(express.json());
// ------- END NodeJS/Express Setup ------ //



// ------- START PostgreSQL Connection Options ------ //
const {Client} = require('pg')

const client = new Client({
    host: "10.158.66.30",   // Requires eduroam or EEE VPN access
    user: "admin",
    port: 32769,
    password: "JXU73zooIoT1",
    database: "postgres"
})

client.connect();
// ------- END PostgreSQL Connection Options ------ //



// ------- START Define REST Endpoints ------ //

// Return all available AIR-1 sensor IDs
app.get("/air-1", async (req,res)=>{
    client.query(`SELECT * FROM air_1`, (err, ids) => {
        if (!err){
            res.json(ids.rows);
        } else {
            console.log(err.message);
        }
        client.end;
    })
})

// Return current (most recent) data of specific MSR-2 sensor
app.get("/air-1/:id", async (req,res)=>{
    const sensor = req.params.id;

    client.query(`SELECT * FROM air_1_${sensor} ORDER BY jsons->> 'timestamp' DESC LIMIT 1`, (err, data) => {
        if (!err){
            res.json(data.rows[0]);
        } else {
            console.log(err.message);
        }
        client.end;
    })
})

// ------- END Define REST Endpoints ------ //

// Server hosted at port 80
app.listen(80, () => console.log("SSL IoT 1 Server Hosted at port 80"));