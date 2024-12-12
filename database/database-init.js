// database-init.js

// Connect to admin database first
db = db.getSiblingDB('admin');

// Authenticate as admin
db.auth('admin', 'example');

// Switch to target database
db = db.getSiblingDB('palmoildatabase');

try {
    // Check if user already exists
    const existingUser = db.getUser('palm');
    if (!existingUser) {
        // Create user if it doesn't exist
        db.createUser({
            user: 'palm',
            pwd: 'oil123!',
            roles: [
                { role: 'readWrite', db: 'palmoildatabase' },
                { role: 'dbAdmin', db: 'palmoildatabase' }
            ]
        });
        print('User palm created successfully');
    } else {
        print('User palm already exists');
    }

    // Create collections if they don't exist
    db.createCollection('palmOilData');
    print('Collections initialized');

} catch (error) {
    print('Error during database initialization:');
    print(error);
    throw error;
}

// Verify user was created
const verifyUser = db.getUser('palm');
if (verifyUser) {
    print('Verification successful - User palm exists with roles:');
    printjson(verifyUser.roles);
} else {
    print('Verification failed - User palm was not created');
    throw new Error('User creation verification failed');
}