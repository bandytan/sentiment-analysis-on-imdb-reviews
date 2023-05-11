require('dotenv').config();

const yup = require('yup');             // Schema validation
const shell = require('shelljs');       // Shell execution
const fs = require('fs');               // Filesystem access
const express = require('express');     // Web framework 
const mysql = require('mysql2');        // MySQL driver
const app = express();

// Some basic middleware
app.use(express.json());

// Database connection setup
const db_conn = mysql.createConnection({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: 'movie_reviews'
});

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
const schemaValidator = async (req, res, next) => {
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
const limitValidator = async (req, res, next) => {
    let q = req.query.limit ?? 0;
    let lim = Math.floor(Number(q));
    return (!q || (lim !== Infinity && String(lim) === q && lim > 0))
        ? next()
        : res.status(400).send(`Invalid limit: ${q}`);
}

app.get('/', (req, res) => res.send('This app is online!'));

app.post('/submit', schemaValidator, (req, res) => {
    let body = JSON.stringify(req.body);
    fs.writeFileSync('scripts/req.json', body, { flag: 'w' });
    let { stdout } = shell.cd('scripts').exec('./pipeline.sh');
    shell.cd('..');
    res.setHeader('Content-Type', 'application/json');
    res.send(stdout);
});

app.get('/stats/:movie', (req, res) => {
    let { movie } = req.params;
    const query = `
    SELECT * FROM movies
    WHERE movies.movie_name = ?`;
    db_conn.query(query, [movie], (err, result, fields) => {
        if (err)
            throw err;
        res.setHeader('Content-Type', 'application/json');
        res.send(JSON.stringify(result[0]));
    });
});

app.get('/reviews/:movie', limitValidator, (req, res) => {
    let { movie } = req.params;
    let { limit } = req.query ?? 1000;
    const query = `
    SELECT * FROM reviews
    WHERE reviews.movie_name = ?
    LIMIT ?`;
    db_conn.query(query, [movie, Number(limit)], (err, result, fields) => {
        if (err)
            throw err;
        res.setHeader('Content-Type', 'application/json');
        res.send(JSON.stringify(result));
    });
});

app.get('/top-words/:movie', (req, res) => {
    let { movie } = req.params;
    const query = `
    SELECT * FROM tfidf_words
    WHERE tfidf_words.movie_name = ?
    ORDER BY tfidf_words.tfidf DESC`;
    db_conn.query(query, [movie], (err, result, fields) => {
        if (err)
            throw err;
        res.setHeader('Content-Type', 'application/json');
        res.send(JSON.stringify(result));
    });
});

// API setup
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Listening on port ${PORT}...`);
});
