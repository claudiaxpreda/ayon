const express = require('express');
const router = express.Router();
const {
    hash,
    compare
 } = require('bcrypt');

const {
    Users,
} = require('../data')


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
            }
        }else {
            res.status(401).send("Wrong username or password");
        }
    } catch (err) {
        throw(new Error(err.message));
    };

});

module.exports = router;