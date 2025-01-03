-- In this SQL file, write (and comment!) the typical SQL queries users will run on your database

-- Now time to optimize our queries using indexes
-- Turn scans to searches!
-- EXPLAIN QUERY PLAN (doesn't actually run the query!)

-- Searching for a username
SELECT "username" FROM "users";
--Optimized using userName index

-- Searching an id using a username
SELECT "id" FROM "users"
WHERE "username" = 'admin';
-- Optimized using userName index

-- Searching for a password using id
SELECT "password" FROM "users"
WHERE "id" = 1;
-- Optimized because id is a primary key

-- Getting data about user's wallets
SELECT "name", "amount" FROM "wallets"
WHERE "user_id" = 1;
-- Optimized using userID_index

-- Deposit [2]
UPDATE "wallets"
SET "amount" = "amount" + 50
WHERE "name" = 'meow'
AND "user_id" = 2;
-- Optimized using userID_index

-- Withdraw [3]
UPDATE "wallets"
SET "amount" = "amount" - 50
WHERE "name" = 'meow'
AND "user_id" = 2;
-- Optimized using userID_index

-- Deleting a wallet[6]
DELETE FROM "wallets"
WHERE "name" = 'temporary'
AND "user_id" = 3;
-- Optimized using userID_index

-- Changing Password [7]
UPDATE "users"
SET "password" = '12'
WHERE "id" = 3;
-- Optimized because id is a primary key

-- Deleting an account [9]
DELETE FROM "users"
WHERE "id" = 3;
-- Optimized by both id being a primary key + wallets being cascaded(due to foreign key constraint), and optimized using userID_index
