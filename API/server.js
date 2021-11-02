const queryString = require("query-string");
const body_parser = require("body-parser");
const express = require("express");
const url = require("url");
const server = express();

server.use(body_parser.json());

const port = 3000;

const db = require("./db");
const dbName = "CDL";
const collectionName = "Players";

db.initialize(dbName, collectionName, function (dbCollection) { // successCallback
   // get all items
   dbCollection.find().toArray(function (err, result) {
      if (err) throw err;
      console.log(result);

      // << return response to client >>
   });

   // server.get("/players", (req, res) => {
   //    // return updated list
   //    dbCollection.find().toArray((error, result) => {
   //       if (error) throw error;
   //       res.json(result);
   //    });
   // });

   server.get("/players", (req, res) => {
     let name = req.query.name;
     let team = req.query.team;

     if(name && team == undefined){
       dbCollection.findOne({ player: name }, (error, result) => {
         console.log()
         if(error) throw error;
         res.json(result);
       });
     } else if(team && name == undefined) {
       dbCollection.find({ team: `[${team}]` }).toArray((error, result) => {
         if(error) throw error;
         res.json(result);
       });
     }
     else{
       dbCollection.find().toArray((error, result) => {
         if(error) throw error;
         res.json(result);
       });
     }
   });

}, function (err) { // failureCallback
   throw (err);
});

server.listen(port, () => {
   console.log(`Server listening at ${port}`);
});
