const express = require('express');

const recordRoutes = express.Router();

const dbo = require('../db/conn')

recordRoutes.route("/players").get(async function(req, res){
  const dbConnect = dbo.getDb();

  dbConnect
    .collection("Players")
    .find({}).limit(50)
    .toArray(function(err, result) {
      if(err){
        res.status(400).send("Error fetching data");
      } else {
        res.json(result);
      }
    });
});

recordRoutes.route("/players/:id").get(async function(req, res){
  const dbConnect = dbo.getDb();

  dbConnect
    .collection("Players")
    .find({"player": req.id}).limit(50)
    .toArray(function(err, result) {
      if(err){
        res.status(400).send("Error fetching data");
      } else {
        res.json(result);
      }
    });
});


module.exports = recordRoutes;
