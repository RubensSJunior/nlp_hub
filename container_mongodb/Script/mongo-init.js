db = db.getSiblingDB('db_nlp');
db.createCollection('collection_twittes');
db.createCollection('collection_termos');
db.createCollection('collection_clean_twittes_text');

db.createUser(
    {
        user: "user_twitter_dash",
        pwd:  "pass_twitter_dash",
        roles:[
            {
                role: "readWrite",
                db:   "db_nlp"
            }
        ]
    }
);

db.createUser(
    {
        user: "user_twitter_script",
        pwd:  "pass_twitter_script",
        roles:[
            {
                role: "readWrite",
                db:   "db_nlp"
            }
        ]
    }
);