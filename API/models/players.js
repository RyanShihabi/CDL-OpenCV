const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const PlayerSchema = new Schema({
  _id: {
    type: String,
  },
  clips: {
    type: Array,
  }
});

const Player = mongoose.model('player', PlayerSchema);

module.exports = Player;
