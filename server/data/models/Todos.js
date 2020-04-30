const mongoose = require('mongoose')

const Schema = mongoose.Schema

const ItemSchema = new Schema({
  name: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: false
  },  
  done: {
    type: Boolean,
    default: false
  }
}, { timestamps: true })

const TodoSchema = new Schema({
  title: {
    type: String,
    required: true
  },
  user: {
    type: Schema.Types.ObjectId,
    ref: 'Users',
    required: true
  },
  items: [ItemSchema],
}, { timestamps: true })

const TodoModel = mongoose.model('Todos', TodoSchema)
//const ItemModel = mongoose.model('Items', ItemSchema)

module.exports = TodoModel;
