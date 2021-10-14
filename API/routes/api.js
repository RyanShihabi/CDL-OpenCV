const express = require('express');
const Player = require('../models/players');
const router = express.Router();

router.get('/players', function(req, res, next){
  Player.find({}).then(function(players){
    res.send(players);
  }).catch(next);
});

router.post('/players', function(req, res, next){
  Player.create(req.body).then(function(player){
    res.send(player);
  }).catch(next);
});

router.put('/players/:id', function(req, res, next){
  Player.findOneAndUpdate({_id: req.params.id}, req.body).then(function(student){
    Player.findOne({_id: req.params.id}).then(function(player){
      res.send(player);
    });
  });
});

router.delete('/players/:id', function(req, res, next){
  Player.findOneAndDelete({_id: req.params.id}).then(function(player){
    res.send(player)
  });
});

module.exports = router;
