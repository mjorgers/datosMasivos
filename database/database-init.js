db = db.getSiblingDB('palmoildatabase');
db.createUser({
  user: 'myuser',
  pwd: 'mypassword',
  roles: [{ role: 'readWrite', db: 'palmoildatabase' }]
});