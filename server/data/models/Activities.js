const mongoose = require('mongoose');

const Schema = mongoose.Schema;

const ActivitySchema = new Schema({
    steps: {
        type: Number,
        required: false
    },
    kcal: {
        type: Number,
        required: false
    },
    food: {
        type: [String],
        required: false
    },
    date: {
        type: Date,
        default: Date.now(),
        required: false,
    },
    user: {
        type: Schema.Types.ObjectId,
        ref: 'Users',
        required: true
    },
}, { timestamps: true });


const ActivityModel = mongoose.model('Activities', ActivitySchema);
module.exports = ActivityModel;
