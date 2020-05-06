const express = require('express');
const router = express.Router();


const {
    Users,
    Todos,
} = require('../data')


/* Get all todo lists */
router.get('/', async(req, res)=> {
    if (req.session.loggedin) {
        const username = req.session.username;
        const user = await Users.findOne({username})

        if (user) {
            const todolist = await Todos.find({user: user.id});
            res.status(200).send(todolist);
        } else {
            res.status(401).send('Please try again');
        }
    } else {
        res.status(401).send('You are not logged in')
    }
});

/* Get a todolist by id*/
router.get('/:id', async(req, res)=> {
    const {id} = req.params;
    const username = req.session.username;

    if (req.session.loggedin) {
        try {
            const todolist = await Todos.findById(id);
            const user = await Users.findOne({username})

            if (todolist.user.toString() == user.id) {
                res.status(200).send(todolist);
            } else {
                res.status(500).send('Todo list not found');
            }
        } catch (err) {
            throw(new Error(err.message));
        };
    } else {
        res.status(401).send('You are not logged in');
    }
});

/* Add a new todo list */
router.post('/', async(req, res)=> {

    if (req.session.loggedin) {
        const username = req.session.username;
        const params = req.body;
        try {
            const user = await Users.findOne({username});
            params.user = user.id;
            const todolist = new Todos(params);
            await todolist.save();
            res.status(200).send("Todo list created");
        } catch (err) {
            throw(new Error(err.message));
        }
    } else {
        res.status(401).send('You are not logged in');
    }
});

/* Add new item to the list */
router.put('/:id/item', async(req, res)=> {
    const params = req.body;
    const {id} = req.params;
    const username = req.session.username;
    if (req.session.loggedin) {
        try {
            const todolist = await Todos.findOne({_id: id});
            const user = await Users.findOne({username});
            if (todolist && todolist.user.toString() === user.id) {
                await todolist.update(
                    { $push: { items: params } }
                );
                res.status(200).send("Item added");
            } else {
                res.status(500).send('Todo list not found');
            }
        } catch (err) {
            throw(new Error(err.message));
        };
    } else {
        res.status(401).send('You are not logged in');
    }
});

/*Update  title  and description */
router.put('/:id', async(req, res)=> {
    const params = req.body;
    const {id} = req.params;
    const username = req.session.username;
    if (req.session.loggedin) {
        try {
            const todolist = await Todos.findById(id);
            const user = await Users.findOne({username});

            if (todolist.user.toString() === user.id) {
                await Todos.findByIdAndUpdate(id, params);
                res.status(200).send("Todo list updated");
            } else {
                res.status(500).send('Todo list not found');
            }
        } catch (err) {
            throw(new Error(err.message));
        };
    } else {
        res.status(401).send('You are not logged in');
    }
});

/* Delete a todo list */
router.delete('/:id', async(req, res)=> {
    const {id} = req.params;
    const username = req.session.username;
    if (req.session.loggedin) {
        try {
            const user = Users.findOne({username});
            const todolist = Todos.findById(id);

            if (todolist.user.toString() === user.id) {
                await Todos.findByIdAndDelete(id);
                res.status(200).send("Todo list deleted");
            } else {
                res.status(500).send('Todo list not found');
            }
        } catch (err) {
            throw(new Error(err.message));
        };
    } else {
        res.status(401).send('You are not logged in');
    }
});

/*Delete an item */
router.put('/:id/item/delete/:itemid', async(req, res)=> {
    const {id, itemid} = req.params;
    const username = req.session.username;

    if (req.session.loggedin) {
        try {
            const user = await Users.findOne({username});
            const todolist = await Todos.findById(id);

            if (todolist.user.toString() === user.id) {
                await Todos.findByIdAndUpdate(
                    id, 
                    { "$pull": { "items": { "_id": itemid } }},
                    { safe: true, multi:true });
                res.status(200).send("Item deleted");
            } else {
                res.status(500).send('Todo list not found');
            }
        } catch (err) {
            throw(new Error(err.message));
        };
    } else {
        res.status(401).send('You are not logged in');
    }
});

/* Update status for an item */
router.put('/:id/item/:itemid', async(req, res)=> {
    const {id, itemid} = req.params;
    const {done} = req.body;
    const username = req.session.username;

    if (req.session.loggedin && !done) {
        try {
            const user = await Users.findOne({username});
            const todolist = await Todos.findById(id);

            if (todolist.user.toString() === user.id) {
                await Todos.findOneAndUpdate({_id: id, items: {$elemMatch: {_id: itemid}}},
                    {$set: {'items.$.done': done}},
                    {'new': true, 'safe': true, 'upsert': true});
                res.status(200).send("Item status updated");
            } else {
                res.status(500).send('Todo list not found');
            }
        } catch (err) {
            throw(new Error(err.message));
        };
    } else {
        res.status(401).send('You are not logged in');
    }
});



module.exports = router;