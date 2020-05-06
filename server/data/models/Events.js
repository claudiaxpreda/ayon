const mongoose = require('mongoose');

const Schema = mongoose.Schema;

const EventSchema = new Schema({
    title: {
        type: String,
        required: true
    },
    time: {
        type: Date,
        required: false,
        default: Date.now
    },
    description: {
        type: String,
        required: true
    },
    user: {
        type: Schema.Types.ObjectId,
        ref: 'Users',
        required: true
    },
    location: {
        type: String,
        required: false
    },
    importance: {
        type: String,
        required: false,
        enum: ['low', 'medium', 'high']
    }
}, { timestamps: true });

const EventModel = mongoose.model('Events', EventSchema);
module.exports = EventModel;