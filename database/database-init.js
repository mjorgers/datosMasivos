db = db.getSiblingDB('palmoildatabase');
db.createUser({
  user: 'palm',
  pwd: 'oil123!',
  roles: [{ role: 'readWrite', db: 'palmoildatabase' }]
});