const express = require('express');
const mongoose = require('mongoose');

const app = express();

mongoose.connect('mongodb://localhost/CDL');
mongoose.Promise = global.Promise;

app.use(express.static('public'));

app.use(express.json());

app.use('/api', require('./routes/api'));

app.use(function(err, req, res, next){
  res.status(422).send({error: err.message});
});

// app.get("/api", (req, res) => res.send("API is functional"));

app.listen(process.env.port || 27017, function(){
  console.log("Listening for requests");
});

// module.exports = router;
