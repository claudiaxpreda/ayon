const express = require('express');
const router = express.Router();

const {
    Activities
} = require('../data')


router.get('/', async(req, res)=> {
    if (req.session.loggedin) {
        const username = req.session.username;
        const user = await Users.findOne({username})

        if (user) {
            const activities = await Activities.find({user: user.id});
            res.status(200).send(activities);
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
            const activity = await Activities.findById(id);
            const user = await Users.findOne({username})

            if (activity.user === user.id) {
                res.status(200).send(activity);
            } else {
                res.status(500).send('Activity not found');
            }
        } catch (err) {
            throw(new Error(err.message));
        };
    } else {
        res.status(401).send('You are not logged in');
    }
});

router.post('/', async(req, res)=> {

    if (req.session.loggedin) {
        const username = req.session.username;
        const params = req.body;
        try {
            const user = await Users.findOne({username});
            params.user = user.id;
            const activity = new Activities(params);
            await activity.save();
            res.status(200).send("Activity added");
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
            const activity = Activities.findById(id);

            if (activity.user === user.id) {
                await Activities.findByIdAndUpdate(id, params);
                res.status(200).send("Activity updated");
            } else {
                res.status(500).send('Activity not found');
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
            const activity = Activities.findById(id);

            if (activity.user === user.id) {
                await Activities.findByIdAndDelete(id);
                res.status(200).send("Activity deleted");
            } else {
                res.status(500).send('Actvity not found');
            }
        } catch (err) {
            throw(new Error(err.message));
        };
    } else {
        res.status(401).send('You are not logged in');
    }
});


module.exports = router;