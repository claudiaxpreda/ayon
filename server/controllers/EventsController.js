const express = require('express');
const router = express.Router();

const {
    Users,
    Events
} = require('../data')


router.get('/', async(req, res)=> {
    if (req.session.loggedin) {
        const username = req.session.username;
        const user = await Users.findOne({username})

        if (user) {
            const events = await Events.find({user: user.id}).select('title');
            res.status(200).send(events);
        } else {
            res.status(401).send('Please try again');
        }
    } else {
        res.status(401).send('You are not logged in')
    }
});

router.get('/:id', async(req, res)=> {
    const {id} = req.params;
    const username = req.session.username;

    if (req.session.loggedin) {
        try {
            const event = await Events.findById(id);
            const user = await Users.findOne({username})

            if (event.user.toString() === user.id) {
                res.status(200).send(event);
            } else {
                res.status(500).send('Event not found');
            }
        } catch (err) {
            throw(new Error(err.message));
        };
    } else {
        res.status(401).send('You are not logged in');
    }
});

router.post('/', async(req, res)=> {
    console.log(req.session.loggedin)
    if (req.session.loggedin) {
        const username = req.session.username;
        const params = req.body;
        try {
            const user = await Users.findOne({username});
            params.user = user.id;
            const event = new Events(params);
            await event.save();
            res.status(200).send("Event added");
        } catch (err) {
            throw(new Error(err.message));
        }
    } else {
        res.status(401).send('You are not logged in');
    }
});

router.put('/:id', async(req, res)=> {
    const params = req.body;
    const {id} = req.params;
    const username = req.session.username;
    if (req.session.loggedin) {
        try {
            const user = Users.findOne({username});
            const event = Events.findById(id);

            if (event.user === user.id) {
                await Events.findByIdAndUpdate(id, params);
                res.status(200).send("Event updated");
            } else {
                res.status(500).send('Event not found');
            }
        } catch (err) {
            throw(new Error(err.message));
        };
    } else {
        res.status(401).send('You are not logged in');
    }
});

router.delete('/:id', async(req, res)=> {
    const {id} = req.params;
    const username = req.session.username;
    if (req.session.loggedin) {
        try {
            const user = Users.findOne({username});
            const event = Events.findById(id);

            if (event.user === user.id) {
                await Events.findByIdAndDelete(id);
                res.status(200).send("Event deleted");
            } else {
                res.status(500).send('Event not found');
            }
        } catch (err) {
            throw(new Error(err.message));
        };
    } else {
        res.status(401).send('You are not logged in');
    }
});

module.exports = router;