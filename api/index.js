const yup = require('yup');
const shell = require('shelljs');
const fs = require('fs');
const express = require('express');
const app = express();

// Some basic middleware
app.use(express.json());

// Routes
const schema = yup.object({
    movie: yup.string().required(),
    reviews: yup.array(yup.object({
        rating:  yup.number().positive().max(10).required(),
        helpful: yup.number().positive().required(),
        title:   yup.string().required(),
        review:  yup.string().required()
    })).required()
});
const validator = async (req, res, next) => {
    try {
        await schema.validate(req.body);
        return next();
    } catch (err) {
        return res.status(400).json({
            name: err.name,
            message: err.message
        });
    }
}

app.post('/submit', validator, (req, res) => {
    let body = JSON.stringify(req.body);
    fs.writeFileSync('scripts/req.json', body);
    let { stdout } = shell.cd('scripts').exec('./pipeline.sh');
    res.setHeader('Content-Type', 'application/json');
    res.send(stdout);
});

// API setup
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Listening on port ${PORT}...`);
})
