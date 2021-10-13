const express = require('express');
const router = express.Router();

router.get('/players', function(req, res){
  res.send({type: 'GET'});
});

router.post('/players', function(req, res){
  res.send({
    type: 'POST',
    clip_url: req.body.url,
  });
});
