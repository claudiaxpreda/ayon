const express = require('express');
const router = express.Router();

const {
    Events,
    Users,
} = require('../data')

const axios = require('axios');

router.get('/', async(req, res) => {
    const items = await Users.find().select('username');
    res.status(200).send(items);    
});

router.get('profile/:username', async(req, res) => {
    const {username} = req.params;
    const logged_user = req.session.username;

    if (username === logged_user) {
        const user = await Users.findOne({username}).select('username email');
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
        password,
        email
    } = req.body;

    try{
        const old_user = await Users.findOne({username});

        if (old_user) {
            res.status(500).send("Username already exists");
        } else {
            const user = new Users({username, password, email});
            user.save()
                .then(() => res.status(200).send("User created"))
                .catch(e => res.status(500).send(e.message));
        }
    } catch (err) {
        throw(new Error(err.message));
    };
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
            } else {
                res.status(403).send("Wrong password");
            }
        }else {
            res.status(401).send("Wrong username");
        }
    } catch (err) {
        throw(new Error(err.message));
    };

});

router.post('/reminder', async(req, res) => {
    plans = []
    try{
        if (req.session.loggedin) {     
            date = new Date()
            const user = await Users.findOne({username: req.session.username});
            events = await Events.find({user: user._id});
            for (indx in events) {
                current = events[indx].time;
                value = date.getDate() == current.getDate();
                value = value && (date.getMonth() == current.getMonth());
                value = value && (date.getFullYear() == current.getFullYear());
                
                if (value) {
                    location = events[indx].location;
                    importance = events[indx].importance;
                    location =  location ? location : 'Not specified';
                    importance = importance ? importance : ''
                    plan = {
                        'title': `${events[indx].title} - ${importance}`,
                        'details': events[indx].description,
                        'location': location,
                        'time': current.toUTCString()
                    }
                    plans.push(plan)
                }
            }

            await axios.post(`http://${process.env.EMAILHOST}:${process.env.EMAILPORT}/api/notify`, {
                email: user.email,
                plan: plans,
            })

            res.status(200).send("Succes");
        } else {
            res.status(403).status("Not logged in")
        }
        
    } catch (err) {
        throw(new Error(err.message));
    };

});

module.exports = router;