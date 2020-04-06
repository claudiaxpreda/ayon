const express = require('express');
const router = express.Router();
const {
    hash,
    compare
 } = require('bcrypt');

const {
    Users,
    Events
} = require('../data');


router.get('/', async(req, res) => {
    const items = await Users.find().select('username');
    res.status(200).send(items);    
});

router.get('profile/:username', async(req, res) => {
    const {username} = req.params;
    const logged_user = req.session.username;

    if (username === logged_user) {
        const user = await Users.findOne({username}).select('username');
        res.status(200).send(user);
    } else {
        res.status(403).send("You do not have access to this profile");
    }
});

router.get('/logged', (req, res) => {
    if ( req.session.loggedin && req.session.username) {
        res.status(200).send('Welcome back');
    } else {
        res.send("Redirect to login");
    }
});

router.post('/register', async(req, res) => {
    const {
        username,
        password
    } = req.body;

    try{
        const old_user = await Users.findOne({username});

        if (old_user) {
            res.status(500).send("Username already exists");
        } else {
            const user = new Users({username, password});
            user.save()
                .then(() => res.status(200).send("User created"))
                .catch(e => res.status(500).send(e.message));
        }
    } catch (err) {
        throw(new Error(err.message));
    }
});


router.post('/login', async(req, res) => {
    const {
        username,
        password
    } = req.body;

    try{
        const user = await Users.findOne({username});
        if (user) {
            if (user.password  === password) {
                req.session.loggedin = true;
                req.session.username = username;
                res.status(200).send("Succes");
            }
        }else {
            res.status(401).send("Wrong username or password");
        }
    } catch (err) {
        throw(new Error(err.message));
    }
});

router.get('/events', async(req, res)=> {
    if (req.session.loggedin) {
        const username = req.session.username;
        const user = await Users.findOne({username});

        if (user) {
            const events = await Events.find({user: user.id});
            res.status(200).send(events);
        } else {
            res.status(401).send('Please try again');
        }
    } else {
        res.status(401).send('You are not logged in')
    }
});

router.get('/events/:id', async(req, res)=> {
    const {id} = req.params;
    const username = req.session.username;

    if (req.session.loggedin) {
        try {
            const event = await Events.findById(id);
            const user = await Users.findOne({username});

            if (event.user === user.id) {
                res.status(200).send(event);
            } else {
                res.status(500).send('Event not found');
            }
        } catch (err) {
            throw(new Error(err.message));
        }
    } else {
        res.status(401).send('You are not logged in');
    }
});

router.post('/events', async(req, res)=> {

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

router.put('/events/:id', async(req, res)=> {
    const params = req.body;
    const {id} = req.params;
    const username = req.session.username;
    if (req.session.loggedin) {
        try {
            const user = Users.findOne({username});
            const event = Events.findById(id);

            if (event.user === user.id) {
                await Events.findByIdAndUpdate(id, params);
                res.status(200).send("Event updated it");
            } else {
                res.status(500).send('Event not found');
            }
        } catch (err) {
            throw(new Error(err.message));
        }
    } else {
        res.status(401).send('You are not logged in');
    }
});

router.delete('/events/:id', async(req, res)=> {
    const {id} = req.params;
    const username = req.session.username;
    if (req.session.loggedin) {
        try {
            const user = Users.findOne({username});
            const event = Events.findById(id);

            if (event.user === user.id) {
                await Events.findByIdAndDelete(id);
                res.status(200).send("Event deleted it");
            } else {
                res.status(500).send('Event not found');
            }
        } catch (err) {
            throw(new Error(err.message));
        }
    } else {
        res.status(401).send('You are not logged in');
    }
});

module.exports = router;